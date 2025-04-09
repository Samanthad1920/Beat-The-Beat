# -*- coding: utf-8 -*-
"""
Beat the Beat! System Test Verification
WS2812B LED Component
"""

# Libraries
import time
from rpi_ws281x import *

LED_COUNT       = 30      # number of LED pixels per strip
TEST_LED_PIN    = 18      # GPIO Pin 18
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS  = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

test_strip = Adafruit_NeoPixel(LED_COUNT, TEST_LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

if __name__ == '__main__':
    
    while(1):
        for i in range(30):
            test_strip.setPixelColor(i, Color(255, 0, 0))
        print("LED STRIP IS LIT!\n")
        test_strip.show()
        
        for i in range(30):
            test_strip.setPixelColor(i, Color(0, 0, 0))   
        time.sleep(1)
        print("Turning off LEDs...\n")
        test_strip.show()
        
        time.sleep(1)
