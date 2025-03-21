# -*- coding: utf-8 -*-
"""
========================================
Beat the Beat! Visual Module
version: 1.0
========================================
"""
# Libraries
import time

# Functions
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

