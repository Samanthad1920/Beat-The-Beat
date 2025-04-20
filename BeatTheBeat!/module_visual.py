# -*- coding: utf-8 -*-
"""
========================================
Beat the Beat! Visual Module
version: 1.0
========================================
"""
# Libraries
import time
from rpi_lcd import LCD
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_ws281x import *

# Create LCD object
#lcd = LCD()

# LED Configuation
LED_COUNT       = 60      # number of LED pixels per strip
NR_LED_PIN      = 21      # GPIO Pin 18
SL_LED_PIN      = 18      # GPIO Pin 21
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS  = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Functions
# def i2cSafeExit(signum, frame):
#     """Handles safe exit on termination signals."""
#     exit(1)
#     
# def setupScoreLCD():
#     """Registers signal handlers for safe exit.
#     Initial score printing to LCD component."""
#     signal(SIGTERM, i2cSafeExit)
#     signal(SIGHUP, i2cSafeExit)
#     lcd.text('Current Score:', 1)   
#     lcd.text('0', 2)
#     
# def updateScoreLCD(current_score:int):
#     """Prints current score to LCD component."""
#     if current_score != prev_score:
#         lcd.text(str(current_score), 2)
#         prev_score = current_score
    
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
    
def main():
    """Main testing function for visual module."""
    lcd = LCD()
    #i2cSafeExit()
    #signal(SIGTERM, i2cSafeExit)
    #signal(SIGHUP, i2cSafeExit)
    lcd.text("test",1)
if __name__ == '__main__':
    main()

