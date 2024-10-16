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

# LED strip configuration:
LED_COUNT      = 30     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Libraries
#import argparse # UNCOMMENT BEFORE DEMO!
import numpy as np
import threading
import time
from pynput.keyboard import Key, Listener
#from rpi_ws281x import * # UNCOMMENT BEFORE DEMO!

# LED Strip Configuration

# Parameters to Set
ACCURACY_WINDOW = 2 #in seconds [just a placeholder for now]
currentScore = 0
keyPress = False

# Function Definitions
def testBeatMap(): #works fine; plan on reading .txt file of array of beats
    """Loads array of values (in seconds) in which hypothetical beats would occur."""
    testBeatTimes = np.array([2, 4, 7, 10, 11]) 
    return testBeatTimes


def startCountdown(seconds): #works fine
    """Starts counting down to beginning of song session."""
    while seconds:
        print(seconds)
        time.sleep(1) # waits 1 second
        seconds -= 1
    print("Start!")
    

def resetScore(): #works fine
    """Resets the current score to zero."""
    global currentScore
    currentScore = 0   
    print('Score has been reset!')
    

def colorWipe(strip, color, wait_ms=50): #for LED animation
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def beatIndicator(): #needs led flash code here
    """Flashes the LED."""
    # colorWipe(strip, Color(0, 255, 0)) #UNCOMMENT FOR DEMO
    print("!!!!!!!!!!!!!!!")
    print("LED BLINK RAH")
    print("!!!!!!!!!!!!!!!")     
    

# =============================================================================
# // currently unused
# def checkAccuracy(reactionTime): # needs to be edited cuz i changed stuff around in main
#     """Calculates and prints time between LED flash and key press."""
#     global currentScore
#     reactionTime = timeDifference #obtains difference in time (in seconds)
#     print(reactionTime)
#     
#     if reactionTime <= ACCURACY_WINDOW:
#         currentScore += 1
#         print("Hit! +1 added to score!")
#         print("Current Score: ", currentScore)
#         
#     elif reactionTime > ACCURACY_WINDOW:
#         print("Miss!")
# =============================================================================
           

def userInput(key): #works fine ??
    """Detects the time in which the user hits the Spacebar."""
    if key == Key.space:
        global keyPress
        global inputTime
        keyPress = True    
        inputTime = time.time()
        #print("Detected user input! (Time = ", inputTime, ")")  
        #print(inputTime)
        #return(inputTime)    


def stopUserInput(key): #works fine
    """Stops listening for user inputs when Esc is pressed."""
    if key == Key.esc:
        return False
    
    
def listenForInput(): #works fine
    """Enables input monitoring."""
    with Listener(on_press=userInput, on_release=stopUserInput) as listener:
        listener.join()   
        
        
def liveBeatTimer():
    """Starts timer for live beat. Calculates if inputs were received within defined time window. Updates score accordingly."""
    global currentScore
    global keyPress
    global expectingInput
    flashTime = time.time() #records the beginning of the event
    time.sleep(ACCURACY_WINDOW)      
    with lock:
        reactionTime = inputTime - flashTime
        if keyPress == True and reactionTime <= ACCURACY_WINDOW and reactionTime > 0:
            currentScore += 1  # increases the score if input was received in time
            print("Input received in time! +1 to score. (Reaction Time:", reactionTime,")")
            keyPress = False # resets keyPress flag
        else:
            print("Input not received in time. +0 to score.")
            
  
# Main Program
if __name__ == '__main__':    
    
    # Initialization of new song session
    resetScore() # sets current score equal to zero
    beatMap = testBeatMap() # for demo purposes
    startCountdown(5) # counts down to beginning of session
    songInSession = True
    
    # Initilization of LEDs UNCOMMENT FOR DEMO
# =============================================================================
#     strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#     strip.begin()
# =============================================================================
    
    while songInSession == True:      
        lastBeatTime = 0
        beatWaitTimes = np.array([]) #creates empty array that will be appended
        
        #calculates and creates array for timing LED flashes
        for currentBeatTime in beatMap:
            #print('Last Beat:', lastBeatTime)
            timeDifference = currentBeatTime - lastBeatTime
            lastBeatTime = currentBeatTime
            #print('Current Beat:', currentBeatTime)
            #print('Time Difference:', timeDifference)
            beatWaitTimes = np.append(beatWaitTimes, timeDifference)
            #print('Current beatWaitTimes Array:', beatWaitTimes)
            
        #creates thread to listen for inputs concurrently as program continues
        inputThread = threading.Thread(target = listenForInput) 
        inputThread.start()
        
        #creates thread to lock in order to preserve accurate values
        lock = threading.Lock()
        
        #flashes LEDs and calculates accuracy   
        for x in beatWaitTimes:
            time.sleep(x) 
            beatIndicator()
            liveBeatTimer() 
              
        songInSession = False #ends the song session once all beats were accounted for
        
    print("This is your final score:", currentScore)
        
            
            
    
        
            
    
