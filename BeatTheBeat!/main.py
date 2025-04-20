# -*- coding: utf-8 -*-
"""
==============================================================================
Beat the Beat! Main Program
version: 1.01

       ___           ___           ___           ___     
      /\  \         /\  \         /\  \         /\  \    
     /::\  \       /::\  \       /::\  \        \:\  \   
    /:/\:\  \     /:/\:\  \     /:/\:\  \        \:\  \  
   /::\~\:\__\   /::\~\:\  \   /::\~\:\  \       /::\  \ 
  /:/\:\ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\     /:/\:\__\
  \:\~\:\/:/  / \:\~\:\ \/__/ \/__\:\/:/  /    /:/  \/__/
   \:\ \::/  /   \:\ \:\__\        \::/  /    /:/  /     
    \:\/:/  /     \:\ \/__/        /:/  /     \/__/      
     \::/__/       \:\__\         /:/  /                 
      ~~            \/__/         \/__/                  
                ___           ___           ___          
               /\  \         /\__\         /\  \         
               \:\  \       /:/  /        /::\  \        
                \:\  \     /:/__/        /:/\:\  \       
                /::\  \   /::\  \ ___   /::\~\:\  \      
               /:/\:\__\ /:/\:\  /\__\ /:/\:\ \:\__\     
              /:/  \/__/ \/__\:\/:/  / \:\~\:\ \/__/     
             /:/  /           \::/  /   \:\ \:\__\       
             \/__/            /:/  /     \:\ \/__/       
                             /:/  /       \:\__\         
                             \/__/         \/__/         
       ___           ___           ___           ___     
      /\  \         /\  \         /\  \         /\  \    
     /::\  \       /::\  \       /::\  \        \:\  \   
    /:/\:\  \     /:/\:\  \     /:/\:\  \        \:\  \  
   /::\~\:\__\   /::\~\:\  \   /::\~\:\  \       /::\  \ 
  /:/\:\ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\     /:/\:\__\
  \:\~\:\/:/  / \:\~\:\ \/__/ \/__\:\/:/  /    /:/  \/__/
   \:\ \::/  /   \:\ \:\__\        \::/  /    /:/  /     
    \:\/:/  /     \:\ \/__/        /:/  /     \/__/      
     \::/__/       \:\__\         /:/  /                 
      ~~            \/__/         \/__/     
      
==============================================================================
"""
# GENERAL CONFIGURATION ======================================================
SONG_FILE_NAME = "" # change this

# Libraries and Modules ======================================================
import numpy as np
import pandas as pd
import random
import time
import threading
from rpi_ws281x import *
import RPi.GPIO as GPIO

# Song Processing Module and Sound Module imports
from module_sp import extractTimes, storeCharTable
from module_sound import loadSong, playSong, stopSong

# Visual Module imports
from module_visual import LED_COUNT, NR_LED_PIN, SL_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL
from module_visual import leadUpLED, beatLED
from module_visual import lcd, i2cSafeExit, setupScoreLCD, setupScoreLCD, updateScoreLCD

# User Interaction imports
from module_ui import DEFAULT_PT_VALUE, PRECISE_PT_VALUE, N_SWITCH_PIN, R_SWITCH_PIN, S_SWITCH_PIN, L_SWITCH_PIN
from module_ui import configSwitch, calculateScore

# Emergency Stop imports
#from module_stop import

# Global Declarations + Threads ==============================================
args_dict = {
    "session_time": time.time(),
    "index": 0
}

strip_northright = Adafruit_NeoPixel(LED_COUNT, NR_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_southleft = Adafruit_NeoPixel(LED_COUNT, SL_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
update_event = threading.Event()

# Functions ==================================================================
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
        
def NRStripThread(song_char_table):
    """This thread controls the north (0) and right (1) pad LEDs"""
    global args_dict
    while True:
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
    while True:
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
        
def main():
    global args_dict
    
    # Begin Threads
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
    beat_index:int = 0    
    prev_score = 0
    current_score = 0
    song_in_session:bool = True
    thread_started = False
    start_time = time.time()
    
    # Load and begin song
    #loadSong("") # put song file name in here
    #playSong()
    
    configSwitch()
    
    northright_thread.start()
    southleft_thread.start()
    timekeep_thread.start()
    
    lcd.text("Current Score:",1)
    lcd.text("0", 2)
    
    while(song_in_session):
        index = args_dict["index"]
        
        n_switch_state = GPIO.input(N_SWITCH_PIN)
        r_switch_state = GPIO.input(R_SWITCH_PIN)
        s_switch_state = GPIO.input(S_SWITCH_PIN)
        l_switch_state = GPIO.input(L_SWITCH_PIN)
        
        
        
        if n_switch_state == GPIO.HIGH: # clean this up later to be all in one if statement
            hit_time = time.time() - start_time
            print(f"North pad hit at {hit_time:.2f}")
            current_score = calculateScore(current_score, hit_time, song_char_table.loc[index, 'ATW Start (s)'], song_char_table.loc[index, 'ATW End (s)'], song_char_table.loc[index, 'PTW Start (s)'], song_char_table.loc[index, 'PTW End (s)'])
            #print("User hit the north pad!")
        elif r_switch_state == GPIO.HIGH:
            print("User hit the right pad!")
        elif s_switch_state == GPIO.HIGH:
            hit_time = time.time() - start_time
            print(f"South pad hit at {hit_time:.2f}")
            current_score = calculateScore(current_score, hit_time, song_char_table.loc[index, 'ATW Start (s)'], song_char_table.loc[index, 'ATW End (s)'], song_char_table.loc[index, 'PTW Start (s)'], song_char_table.loc[index, 'PTW End (s)'])
#             print("User hit the south pad!")
        elif l_switch_state == GPIO.HIGH:
            print("User hit the south pad!")
        
#         if current_score != prev_score:
#             print(current_score)
#             updateScoreLCD(current_score)
#             prev_score = current_score
            
        lcd.text(str(current_score),2)

if __name__ == '__main__':
    main()