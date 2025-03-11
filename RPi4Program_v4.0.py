# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program
Version 4.1 E-Stop attempted! 

@author: Sasha Folloso and Samantha DuBois
"""
# =============================================================================
#       ___           ___           ___           ___     
#      /\  \         /\  \         /\  \         /\  \    
#     /::\  \       /::\  \       /::\  \        \:\  \   
#    /:/\:\  \     /:/\:\  \     /:/\:\  \        \:\  \  
#   /::\~\:\__\   /::\~\:\  \   /::\~\:\  \       /::\  \ 
#  /:/\:\ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\     /:/\:\__\
#  \:\~\:\/:/  / \:\~\:\ \/__/ \/__\:\/:/  /    /:/  \/__/
#   \:\ \::/  /   \:\ \:\__\        \::/  /    /:/  /     
#    \:\/:/  /     \:\ \/__/        /:/  /     \/__/      
#     \::/__/       \:\__\         /:/  /                 
#      ~~            \/__/         \/__/                  
#                ___           ___           ___          
#               /\  \         /\__\         /\  \         
#               \:\  \       /:/  /        /::\  \        
#                \:\  \     /:/__/        /:/\:\  \       
#                /::\  \   /::\  \ ___   /::\~\:\  \      
#               /:/\:\__\ /:/\:\  /\__\ /:/\:\ \:\__\     
#              /:/  \/__/ \/__\:\/:/  / \:\~\:\ \/__/     
#             /:/  /           \::/  /   \:\ \:\__\       
#             \/__/            /:/  /     \:\ \/__/       
#                             /:/  /       \:\__\         
#                             \/__/         \/__/         
#       ___           ___           ___           ___     
#      /\  \         /\  \         /\  \         /\  \    
#     /::\  \       /::\  \       /::\  \        \:\  \   
#    /:/\:\  \     /:/\:\  \     /:/\:\  \        \:\  \  
#   /::\~\:\__\   /::\~\:\  \   /::\~\:\  \       /::\  \ 
#  /:/\:\ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\     /:/\:\__\
#  \:\~\:\/:/  / \:\~\:\ \/__/ \/__\:\/:/  /    /:/  \/__/
#   \:\ \::/  /   \:\ \:\__\        \::/  /    /:/  /     
#    \:\/:/  /     \:\ \/__/        /:/  /     \/__/      
#     \::/__/       \:\__\         /:/  /                 
#      ~~            \/__/         \/__/                  
# =============================================================================

# Libraries ==================================================================
import numpy as np
import pandas as pd
import random
import time
import threading
import RPi.GPIO as GPIO
from playsound import playsound
from rpi_ws281x import *

# Constants / Configuration ==================================================
## LEDs
LED_COUNT       = 30      # number of LED pixels per strip
NR_LED_PIN      = 21 # GPIO Pin 18
SL_LED_PIN      = 18 # GPIO Pin 21
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

## Global Dictionary
args_dict = {
    "session_time": time.time(),
    "index": 0
}

# Define the GPIO pin connected to the e-stop button
ESTOP_PIN = 7 # GPIO4 - Pin 7 - default Pull-Up  

## Threads
strip_northright = Adafruit_NeoPixel(LED_COUNT, NR_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_southleft = Adafruit_NeoPixel(LED_COUNT, SL_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

update_event = threading.Event()
stop_event = threading.Event()

# Functions ==================================================================
def timekeepThread(song_char_table):
    """Thread that keeps track of the time."""
    global args_dict
    start_time = time.time()
    index = args_dict["index"]
    while(not stop_event.is_set()):
        current_time = time.time()
        session_time = current_time - start_time
        args_dict["session_time"] = session_time
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        if session_time >= beat_time:
            #print(f"Beat {index}! at {beat_time} s")
            index = index + 1
        update_event.set()  # Notify threads of the update
#         update_event.clear()  # Reset event after signaling
        time.sleep(.01)
 
def NRStripThread(song_char_table):
    """This thread controls the north (0) and right (1) pad LEDs"""
    global args_dict
    while not stop_event.is_set():
        update_event.wait() #waits for flag set by timekeep thread
        
        index = args_dict["index"]
        session_time = args_dict["session_time"]
        
        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and (beat_pad != 0 or beat_pad != 1):
            index = index + 1
            args_dict["index"] = index
        
        elif session_time >= beat_leadup and (beat_pad == 0 or beat_pad == 1) and not led_activated:
            if beat_pad == 0:
                leadUpLED(strip_northright, Color(255,255,0), 0)
                beatLED(strip_northright, Color(0,255,0), 0)
                song_char_table.at[index, 'LED Activated'] = True
            elif beat_pad == 1:
                leadUpLED(strip_northright, Color(255,255,0), 1)
                beatLED(strip_northright, Color(0,255,0), 1)
                song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
        time.sleep(.001)

def SLStripThread(song_char_table):
    """This thread controls the south (2) and left (3) pad LEDs"""
    global args_dict
    while not stop_event.is_set():
        update_event.wait() #waits for flag set by timekeep thread
        
        index = args_dict["index"]
        session_time = args_dict["session_time"]
        
        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and (beat_pad != 2 or beat_pad != 3):
            index = index + 1
            args_dict["index"] = index
        
        elif session_time >= beat_leadup and (beat_pad == 2 or beat_pad == 3) and not led_activated:
            if beat_pad == 2:
                leadUpLED(strip_southleft, Color(255,255,0), 2)
                beatLED(strip_southleft, Color(0,255,0), 2)
                song_char_table.at[index, 'LED Activated'] = True
            elif beat_pad == 3:
                leadUpLED(strip_southleft, Color(255,255,0), 3)
                beatLED(strip_southleft, Color(0,255,0), 3)
                song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
        
        time.sleep(.001)    
        
def leadUpLED(strip, color, pad, wait_ms=250):
    """New lead up LED indication to alert the user of an incoming beat."""
    if pad == 0 or pad == 2: # north and south are first 30 leds in strip
        for i in range(4):
            strip.setPixelColor(i, color)
            strip.setPixelColor(i+5, color)
            strip.setPixelColor(i+10, color)
            strip.setPixelColor(i+15, color)
            strip.setPixelColor(i+20, color)
            strip.setPixelColor(i+25, color)
            strip.show()
            time.sleep(wait_ms/1000.0) # 250 ms
    elif pad == 1 or pad == 3: # left and right are second 30 leds in strip
        for i in range(4):
            strip.setPixelColor((30+i), color)
            strip.setPixelColor((30+i)+5, color)
            strip.setPixelColor((30+i)+10, color)
            strip.setPixelColor((30+i)+15, color)
            strip.setPixelColor((30+i)+20, color)
            strip.setPixelColor((30+i)+25, color)
            strip.show()
            time.sleep(wait_ms/1000.0) # 250 ms

def beatLED(strip, color, pad):
    """New on-beat LED indication to show user when the beat occurs."""
    if pad == 0 or pad == 2: # north and south are the first 30 leds in strip
        for i in range(5):
            strip.setPixelColor(i, color)
            strip.setPixelColor(i+5, color)
            strip.setPixelColor(i+10, color)
            strip.setPixelColor(i+15, color)
            strip.setPixelColor(i+20, color)
            strip.setPixelColor(i+25, color)
        strip.show()
    elif pad == 1 or pad == 3: # left and right are second 30 leds in strip
        for i in range(5):
            strip.setPixelColor((30+i), color)
            strip.setPixelColor((30+i)+5, color)
            strip.setPixelColor((30+i)+10, color)
            strip.setPixelColor((30+i)+15, color)
            strip.setPixelColor((30+i)+20, color)
            strip.setPixelColor((30+i)+25, color)
        strip.show()

    # let beat maintain for half a second
    time.sleep(.5)
    
    # clear led strip after half a second passed after beat
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))    
    strip.show()        

def play_audio_non_blocking(sound_file):
    """Plays the audio file in a separate thread so the main program continues."""
    thread = threading.Thread(target=playsound, args=(sound_file,), daemon=True)
    thread.start()
        
def extractTimes(filename:str):
    """Extracts beat times from beat generation algorithm output."""
    with open(filename, 'r') as file:
        data = file.read()
        data = data.replace("[","").replace("]","")
        time_list = [round(float(value), 3) for value in data.split()]
    file.close()  
    return time_list

def storeCharTable(beat_times:list, beat_leadup:list, atw_start:list, atw_end:list, ptw_start:list, ptw_end:list):
    """Calculates the characteristics of every beat and stores in table."""
    beats_data = []
    previous_pad = None
    prevprev_pad = None
    
    for i, beat_time in enumerate(beat_times):
        possible_pads = [0, 1, 2, 3]
        if prevprev_pad is not None:
            possible_pads.remove(prevprev_pad)
        if previous_pad is not None:
            possible_pads.remove(previous_pad)
            prevprev_pad = previous_pad
        pad_number = random.choice(possible_pads)
        previous_pad = pad_number
            
        beats_data.append({
            'Beat Number': i + 1,
            'Pad #': pad_number,
            'User Hit': False,
            'LED Activated': False,
            'Lead Up Start (s)': beat_leadup[i],
            'ATW Start (s)': atw_start[i],
            'PTW Start (s)': ptw_start[i],
            'Beat Time (s)': beat_times[i],
            'PTW End (s)': ptw_end[i],
            'ATW End (s)': atw_end[i]  
        })
        
    song_char_table = pd.DataFrame(beats_data)
    print(song_char_table)
    return song_char_table

def stop_threads():
    """Stops all LED threads and turns off LEDs."""
    print("Stopping all LED threads...")
    stop_event.set()  # Signal threads to stop

    # Turn off all LEDs
    for strip in [strip_northright, strip_southleft]:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))  # Set to off
        strip.show()
    
    print("All LEDs turned off.")

def button_callback(channel):
    print(f"Button pressed on pin {channel}!")
    if channel == ESTOP_PIN:
        print("Emergency stop triggered! Stopping all threads.")
        stop_threads()

def main():
    """Obligatory main function!"""

    # GPIO Pin Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ESTOP_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300) # ESTOP Flag

    # Create NeoPixel object with appropriate configuration.
    # Intialize the library (must be called once before other functions).
    strip_northright.begin()
    strip_southleft.begin()
    
    # Pandas Dataframe Configuration
    pd.set_option('display.max_columns', None)  # shows all columns
    pd.set_option('display.max_rows', None)  # shows all rows
    pd.set_option('display.expand_frame_repr', False)  # disables line wrapping
    pd.set_option('display.width', 0)  # automatically adjusts width to the console size 
    
    # Extract data from laptop program
    beat_times = extractTimes("generatedMap.txt")
    beat_leadup = extractTimes("beatLeadUp.txt")
    atw_start = extractTimes("atwBefore.txt")
    atw_end = extractTimes("atwAfter.txt")
    ptw_start = extractTimes("ptwBefore.txt")
    ptw_end = extractTimes("ptwAfter.txt")
    
    # Store in local table for visual indication module and user interaction module to reference
    song_char_table = storeCharTable(beat_times, beat_leadup, atw_start, atw_end, ptw_start, ptw_end)
    
    # Thread creation
    timekeep_thread = threading.Thread(target = timekeepThread, args = (song_char_table,), daemon = True)
    northright_thread = threading.Thread(target = NRStripThread, args = (song_char_table,), daemon = False)
    southleft_thread = threading.Thread(target = SLStripThread, args = (song_char_table,), daemon = False)
    
    # Other important things
    song_in_session:bool = True
    beat_index:int = 0
    start_time = time.time()
    thread_started = False
    
    while(song_in_session):
        if not thread_started:
            northright_thread.start()
            southleft_thread.start()
            timekeep_thread.start()
            thread_started = True

# Main Program
if __name__ == '__main__':
    main()
