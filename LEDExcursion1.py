# -*- coding: utf-8 -*-
"""
Excursion 1: LEDs

Acquire LEDs, PI 4 processor, and relevant software tools.
>> Integrate LEDs and processor.  
>> Load software tools. 
>> Create a simple program to time the lighting of LEDs and receive timed input from the board.
>> Calculate an initial latency from input to score based on user accuracy.

The results of this excursion will be used to define:
>> Requirement for multiple LEDs to light up according to a random sequence.
>> The overall timing for the indicator LED lights for a given sequence.
>> How much delay is needed between a given LED output to user input.
"""

# =============================================================================
# import time
# from rpi_ws281x import *
# import argparse
# 
# # LED strip configuration:
# LED_COUNT      = 30     # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
# LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
# =============================================================================

# Libraries
import time
from pynput.keyboard import Key, Listener

# Parameters to Set
accuracyWindow = 2 #in seconds [just a placeholder for now]

# Function Definitions
def testBeatMap():
    testBeatTimes = [1]
    return testBeatTimes

def resetScore():
    """Resets the current score to zero."""
    currentScore = 0
    print('Score has been reset!\n')
    

def beatIndicator():
    """Flashes the LED and awaits input from user"""
    expectingInput = true
    #PUT LED FLASH CODE HERE
    flashTime = time.time() #takes the current time
    

def checkAccuracy(flashTime, inputTime):
    """Calculates and prints time between LED flash and key press."""
    global currentScore
    reactionTime = inputTime - flashTime #obtains difference in time (in seconds)
    print(reactionTime)
    
    if reactionTime <= accuracyWindow:
        currentScore += 1
        print("Hit! +1 added to score! \n")
        print("Current Score: ", currentScore, "\n")
        
    elif reactionTime > accuracyWindow:
        print("Miss!\n")
        
def userInput(key): #detects the time in which the spacebar was pressed
    if key == Key.space:
        print("Detected user input!\n")
        inputTime = time.time()
        print(inputTime, "\n")

        
  
# Main Program
if __name__ == '__main__':
    resetScore()
      
    # Set up the listener for keyboard events
    with Listener(on_press=userInput, on_release=None) as listener:
        listener.join()
    
