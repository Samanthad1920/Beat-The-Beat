# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program
Version 3.5 (threads pls pls pls pls pls pls pls WORK)

@author: Sasha Folloso
"""

# Libraries
import numpy as np
import pandas as pd
import random
import time
import threading
from playsound import playsound
from rpi_ws281x import *

# Constants / Configuration
## LEDs
LED_COUNT       = 30      # number of LED pixels per strip
UP_PAD_PIN      = 18 # GPIO Pin 18
RIGHT_PAD_PIN   = 21 # GPIO Pin 21
DOWN_PAD_PIN    = 10 # GPIO Pin 10
LEFT_PAD_PIN    = 12 # GPIO Pin 12
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip_north = Adafruit_NeoPixel(LED_COUNT, UP_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_right = Adafruit_NeoPixel(LED_COUNT, RIGHT_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_south = Adafruit_NeoPixel(LED_COUNT, DOWN_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_left = Adafruit_NeoPixel(LED_COUNT, LEFT_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

## Threads
args_dict = {
    "session_time": time.time(),
    "index": 0
}
update_event = threading.Event()

# Functions
def timekeepThread(song_char_table):
    """Thread that keeps track of the time."""
    global args_dict
    start_time = time.time()
    index = args_dict["index"]
    while(True):
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

def northStripThread(song_char_table):
    """Thread that controls north LED strip."""
    global args_dict
    while True:
        update_event.wait()

        index = args_dict["index"]
        session_time = args_dict["session_time"]

        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and beat_pad != 0:
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
        
        elif session_time >= beat_leadup and beat_pad == 0 and not led_activated:
            leadUpLED(strip_north, Color(255,255,0))
            print("Beat at pad 1!")
            beatLED(strip_north, Color(0,255,0))
            song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
 
        time.sleep(.001)
        
def rightStripThread(song_char_table):
    """Thread that controls right LED strip."""
    global args_dict
    while True:
        update_event.wait()

        index = args_dict["index"]
        session_time = args_dict["session_time"]

        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and beat_pad != 1:
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
        
        elif session_time >= beat_leadup and beat_pad == 1 and not led_activated:
            leadUpLED(strip_right, Color(255,255,0))
            beatLED(strip_right, Color(0,255,0))
            song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
 
        time.sleep(.001)

def southStripThread(song_char_table):
    """Thread that controls south LED strip."""
    global args_dict
    while True:
        update_event.wait()

        index = args_dict["index"]
        session_time = args_dict["session_time"]

        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and beat_pad != 2:
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
        
        elif session_time >= beat_leadup and beat_pad == 2 and not led_activated:
            leadUpLED(strip_south, Color(255,255,0))
            beatLED(strip_south, Color(0,255,0))
            song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
 
        time.sleep(.001)
        
def leftStripThread(song_char_table):
    """Thread that controls south LED strip."""
    global args_dict
    while True:
        update_event.wait()

        index = args_dict["index"]
        session_time = args_dict["session_time"]

        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        
        if session_time >= beat_time and beat_pad != 3:
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
        
        elif session_time >= beat_leadup and beat_pad == 3 and not led_activated:
            leadUpLED(strip_left, Color(255,255,0))
            beatLED(strip_left, Color(0,255,0))
            song_char_table.at[index, 'LED Activated'] = True
            index = index + 1
            args_dict["index"] = index
#             update_event.set() 
#             update_event.clear()
 
        time.sleep(.001)

def play_audio_non_blocking(sound_file):
    """Plays the audio file in a separate thread so the main program continues."""
    thread = threading.Thread(target=playsound, args=(sound_file,), daemon=True)
    thread.start()

def leadUpLED(strip, color, wait_ms=250):
    """Lead up LED indication to alert the user of an incoming beat."""
    for i in range(4):
        strip.setPixelColor(i, color)
        strip.setPixelColor(i+5, color)
        strip.setPixelColor(i+10, color)
        strip.setPixelColor(i+15, color)
        strip.setPixelColor(i+20, color)
        strip.setPixelColor(i+25, color)
        strip.show()
        time.sleep(wait_ms/1000.0) # 250 ms
    
def beatLED(strip, color):
    """On-beat LED indication to show user when the beat occurs."""
    # beat flash animation
    for i in range(5):
        strip.setPixelColor(i, color)
        strip.setPixelColor(i+5, color)
        strip.setPixelColor(i+10, color)
        strip.setPixelColor(i+15, color)
        strip.setPixelColor(i+20, color)
        strip.setPixelColor(i+25, color)
        
    strip.show()
        
    # let beat maintain for half a second
    time.sleep(.5)
    
    # clear led strip after half a second passed after beat
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    
    strip.show()
        
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

def main():
    """Obligatory main function!"""

    # Create NeoPixel object with appropriate configuration.
    #strip_north = Adafruit_NeoPixel(LED_COUNT, UP_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    #strip_left = Adafruit_NeoPixel(LED_COUNT, LEFT_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip_north.begin()
    strip_right.begin()
    strip_south.begin()
    strip_left.begin()
    
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
    north_thread = threading.Thread(target = northStripThread, args = (song_char_table,), daemon = True)
    south_thread = threading.Thread(target = southStripThread, args = (song_char_table,), daemon = True)
    left_thread = threading.Thread(target = leftStripThread, args = (song_char_table,), daemon = True)
    right_thread = threading.Thread(target = rightStripThread, args = (song_char_table,), daemon = True)
    
    # Other important things
    song_in_session:bool = True
    beat_index:int = 0
    start_time = time.time()
    thread_started = False
    
    while(song_in_session):
        if not thread_started:
            north_thread.start()
            south_thread.start()
            left_thread.start()
            right_thread.start()
            timekeep_thread.start()
            thread_started = True

# Main Program
if __name__ == '__main__':
    main()

