# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program

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

# Constants
# LED Configuration
LED_COUNT      = 30      # number of LED pixels per strip
UP_PAD_PIN     = 18 # GPIO Pin 18
LEFT_PAD_PIN   = 21 # GPIO Pin 21
#DOWN_PAD_PIN   = # GPIO Pin
#RIGHT_PAD_PIN  = # GPIO Pin
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Classes

# Functions
def run_beatLeadUp(strip, color):
    """Threaded wrapper for beatLeadUp function."""
    beatLeadUp(strip, color)

def play_audio_non_blocking(sound_file):
    """Plays the audio file in a separate thread so the main program continues."""
    thread = threading.Thread(target=playsound, args=(sound_file,), daemon=True)
    thread.start()
    
def beatLeadUp(strip, color, wait_ms=250):
    """Lead up LED indication to alert the user of an incoming beat."""
    # beat lead up animation
    for i in range(4):
        strip.setPixelColor(i, color)
        strip.setPixelColor(i+5, color)
        strip.setPixelColor(i+10, color)
        strip.setPixelColor(i+15, color)
        strip.setPixelColor(i+20, color)
        strip.setPixelColor(i+25, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
    # beat flash animation
    for i in range(5):
        strip.setPixelColor(i, Color(0,255,0))
        strip.setPixelColor(i+5, Color(0,255,0))
        strip.setPixelColor(i+10, Color(0,255,0))
        strip.setPixelColor(i+15, Color(0,255,0))
        strip.setPixelColor(i+20, Color(0,255,0))
        strip.setPixelColor(i+25, Color(0,255,0))
        strip.show()
  
    # let beat maintain for half a second
    time.sleep(.5)
    
    # clear led strip after half a second passed after beat
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
    
def beatLight(strip, color, wait_ms=1):
    """LED indication to alert the user of the actual beat time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set all pixels to off
        strip.show
        
def beatLightv2(strip, color, irregular_beat:bool):
    """LED flash indicator that includes both lead up and beat time indication."""
    if not irregular_beat:
        pass
    elif irregular_beat:
        pass

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
    """The main program where everything happens."""
    # Create NeoPixel object with appropriate configuration.
    strip_north = Adafruit_NeoPixel(LED_COUNT, UP_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip_left = Adafruit_NeoPixel(LED_COUNT, LEFT_PAD_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip_north.begin()
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

    # Other prior song session functions/config
    
    # Entering the song session
    
    # testing tomfoolery
    song_in_session:bool = True
    flip:bool = True
    start_time = time.time()
    play_audio_non_blocking("test9.mp3")
    index:int = 0
    
    while(song_in_session and index < len(song_char_table)):
        current_time = time.time()
        session_time = current_time - start_time  # Round to match stored beat times
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        
        if session_time >= beat_leadup:
            threads = [] # list of threads
            
            if song_char_table.loc[index, 'Pad #'] == 0:
                t1 = threading.Thread(target=run_beatLeadUp, args=(strip_north, Color(255, 255, 0)))
                threads.append(t1)
                t1.start()
                print(f"bop! at {beat_time} at LEFT LED")
                index += 1                
            elif song_char_table.loc[index, 'Pad #'] == 1:
                t2 = threading.Thread(target=run_beatLeadUp, args=(strip_left, Color(255, 255, 0)))
                threads.append(t2)
                t2.start()
                print(f"bop! at {beat_time} at RIGHT LED")
                index += 1
            else:
                print(f"bop! at {beat_time}!")
                index += 1
                
#             if flip == True:
#                 if song_char_table.loc[index, 'Pad #'] == 0: 
#                     print(f"bop! at {beat_time} at LEFT LED")
#                 elif song_char_table.loc[index, 'Pad #'] == 1: 
#                     print(f"bop! at {beat_time} at RIGHT LED")
#                 else: 
#                     print(f"bop! at {beat_time}")
#                 #colorWipe(strip, Color(255, 0, 0))
#                 index += 1
#                 flip = False
#             elif flip == False:
#                 if song_char_table.loc[index, 'Pad #'] == 0: 
#                     print(f"bop! at {beat_time} at LEFT LED")
#                 elif song_char_table.loc[index, 'Pad #'] == 1: 
#                     print(f"bop! at {beat_time} at RIGHT LED")
#                 else: 
#                     print(f"bop! at {beat_time}")
#                 #colorWipe(strip, Color(0, 255, 0))
#                 index += 1
#                 flip = True  
        time.sleep(0.001)
                        
# Main Program
if __name__ == '__main__':
    main()