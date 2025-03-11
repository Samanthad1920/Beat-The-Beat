# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program Modularized
Version 1.0
@author: Sasha Folloso and Samantha DuBois
"""
# Libraries ==================================================================
import numpy as np
import pandas as pd
import random
import time
import threading
import RPi.GPIO as GPIO
import multiprocessing
from playsound import playsound 
from rpi_ws281x import Adafruit_NeoPixel, Color
from multiprocessing import Lock
from LEDController import LEDController
from TimeKeeper import TimeKeeper

# Constants / Configuration ==================================================
global args_dict
lock = Lock()

## LEDs
LED_COUNT       = 30      # number of LED pixels per strip
NR_LED_PIN      = 21 # GPIO Pin 18
SL_LED_PIN      = 18 # GPIO Pin 21
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define the GPIO pin connected to the e-stop button
ESTOP_PIN = 7 # GPIO4 - Pin 7 - default Pull-Up

## Define LED Strips
strip_northright = Adafruit_NeoPixel(LED_COUNT, NR_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip_southleft = Adafruit_NeoPixel(LED_COUNT, SL_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Make the processes global
timekeep_process = None
northright_process = None
southleft_process = None

# Multiprocessing shared objects
update_event = multiprocessing.Event()
stop_event = multiprocessing.Event()
args_queue = multiprocessing.Queue()

# Functions ==================================================================
def timekeepProcess(song_char_table):
    """Thread that keeps track of the time."""
    start_time = time.time()
    index = args_dict["index"]
    while not stop_event.is_set():
        current_time = time.time()
        session_time = current_time - start_time
        with lock: # Ensures safe access to shared data
            args_dict["session_time"] = session_time
            beat_time = song_char_table.loc[index, 'Beat Time (s)']
            if session_time >= beat_time:
                index += 1
            args_dict["index"] = index
        update_event.set()  # Notify threads of the update
        time.sleep(0.01)

def play_audio_non_blocking(sound_file):
    """Plays the audio file in a separate thread so the main program continues."""
    thread = threading.Thread(target=playsound, args=(sound_file,), daemon=True)
    thread.start()

def extractTimes(filename:str):
    """Extracts beat times from beat generation algorithm output."""
    try:
        with open(filename, 'r') as file:
            data = file.read()
            data = data.replace("[","").replace("]","")
            time_list = [round(float(value), 3) for value in data.split()]
        file.close()
        return time_list
    except FileNotFoundError:
        print(f'ERror: {filename} not found')
        return []
    except ValueError as e:
        print(f'Error: Invalid data format in {filename}. {e}')
        return []
    except Exception as e:
        print(f'Unexpected error while reading {filename}: {e}')
        return []

def storeCharTable(beat_times:list, beat_leadup:list, atw_start:list, atw_end:list, ptw_start:list, ptw_end:list):
    """Calculates the characteristics of every beat and stores in table."""
    beats_data = []
    previous_pad = None
    prevprev_pad = None

    for i in enumerate(beat_times):
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

def button_callback(channel):
    print(f"Button pressed on pin {channel}!")
    if channel == ESTOP_PIN:
        print("Emergency stop triggered! Stopping all threads.")
        stop_processes()
        
def LEDStripProcess(song_char_table, args_queue, strip, pad_numbers):
    """Process that controls LED strips (north-right or south-left)."""
    led_controller = LEDController(strip)  # Instantiate the LED controller
    
    while not stop_event.is_set():
        update_event.wait()  # waits for flag set by timekeep process
        index = args_dict["index"]
        session_time = args_dict["session_time"]
        if index >= len(song_char_table):
            print("Reached end of song characteristic table.")
            break
        beat_time = song_char_table.loc[index, 'Beat Time (s)']
        beat_leadup = song_char_table.loc[index, 'Lead Up Start (s)']
        beat_pad = song_char_table.loc[index, 'Pad #']
        led_activated = song_char_table.loc[index, 'LED Activated']
        if session_time >= beat_time and beat_pad not in pad_numbers:
            index += 1
            args_dict["index"] = index
        elif session_time >= beat_leadup and beat_pad in pad_numbers and not led_activated:
            if beat_pad in pad_numbers:
                led_controller.leadUpLED(Color(255, 255, 0), beat_pad)  # Call lead-up function
                led_controller.beatLED(Color(0, 255, 0), beat_pad)  # Call beat function
                song_char_table.at[index, 'LED Activated'] = True
            index += 1
            args_dict["index"] = index
        time.sleep(0.001)

def stop_processes():
    """Stops all LED processes and turns off LEDs."""
    stop_event.set()  # Signal processes to stop
    print("Stopping all processes...")

    # Turn off all LEDs
    for strip in [strip_northright, strip_southleft]:
        led_controller = LEDController(strip)
        led_controller.clear_leds()

    print("All LEDs turned off.")

    # TODO: STOPS MUSIC HERE!!!!!!!!!!!!!!!

     # Terminate and join the processes to ensure proper shutdown
    timekeep_process.terminate()
    northright_process.terminate()
    southleft_process.terminate()

    timekeep_process.join()
    northright_process.join()
    southleft_process.join()

    # print("All processes stopped.")

def main():
    """Obligatory main function!"""

    # GPIO Pin Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ESTOP_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300) # ESTOP Flag

    global timekeep_process, northright_process, southleft_process

    with multiprocessing.Manager() as manager:
        # Shared dictionary for managing session time and index
        args_dict = manager.dict({
            "session_time": 0.0,
            "index": 0
        })

    # Create NeoPixel object with appropriate configuration.
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

    # Process creation for the TimeKeeper
    timekeeper = TimeKeeper(song_char_table, args_dict, lock, update_event, stop_event)
    timekeep_process = multiprocessing.Process(target=timekeeper.run, daemon=True)
    
    # Process creation for LED Strips
    northright_process = multiprocessing.Process(target=LEDStripProcess, args=(song_char_table, args_queue, strip_northright, [0, 1]), daemon=True)
    southleft_process = multiprocessing.Process(target=LEDStripProcess, args=(song_char_table, args_queue, strip_southleft, [2, 3]), daemon=True)

    # Start the processes
    timekeep_process.start()
    northright_process.start()
    southleft_process.start()

    # Join the processes to the main thread
    timekeep_process.join()
    northright_process.join()
    southleft_process.join()

    # Other important things
    song_in_session:bool = True

    while(song_in_session):
        # Monitor the current time of the song (checking for completion)
        if args_dict["index"] >= len(song_char_table):  # If the song is complete
            print("Song has finished.")
            stop_processes()
            song_in_session = False  # End the session

        # Monitor user input or any other events (emergency stop)
        if GPIO.input(ESTOP_PIN) == GPIO.LOW:  # Emergency stop button pressed
            print("Emergency stop triggered. Exiting...")
            stop_processes()  # Call stop function
            song_in_session = False  # End the session

        time.sleep(0.1)
    print("Exiting Main Program")

# Main Program
if __name__ == '__main__':
    main()