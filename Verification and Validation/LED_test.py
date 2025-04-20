# -*- coding: utf-8 -*-
"""
Beat the Beat! System Test Verification
WS2812B LED Component
"""

# Libraries
import time
from rpi_ws281x import *

LED_COUNT       = 10      # number of LED pixels per strip
TEST_LED_PIN1   = 13      # GPIO Pin 18
TEST_LED_PIN2   = 18    # GPIO Pin 21
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS  = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip1 = Adafruit_NeoPixel(LED_COUNT, TEST_LED_PIN1, LED_FREQ_HZ, 11, LED_INVERT, LED_BRIGHTNESS, 1)
strip2 = Adafruit_NeoPixel(LED_COUNT, TEST_LED_PIN2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0)

if __name__ == '__main__':
    strip1.begin()
    strip2.begin()
     
    for i in range(60):
        strip1.setPixelColor(i, Color(100,0,0))
        strip2.setPixelColor(i, Color(100,0,0))
    strip1.show()
    time.sleep(.5)
    strip2.show()
#     
#     time.sleep(5)
# 
#     for i in range(60):
#         strip1.setPixelColor(i, Color(255,i*2,i))
#         strip2.setPixelColor(i, Color(i*2,0,255))
#     print("LEDs are lit!")
#     strip1.show()                                                                                                                                                                      
#     time.sleep(.5)
#     strip2.show()
    ty = 5
    while(ty >= 0):
        for i in range(60):
            strip1.setPixelColor(i, Color(255, i*2, 0))
            strip2.setPixelColor(i, Color(255-(i*4), i*3, 255-(i*4)))
        print("LED STRIP IS LIT!\n")
        strip1.show()
        strip2.show()
        time.sleep(1)
        
        for i in range(60):
            strip1.setPixelColor(i, Color(0, 0, 0))
            strip2.setPixelColor(i, Color(0, 0, 0))
        
        print("Turning off LEDs...\n")
        strip1.show()
        strip2.show()
        time.sleep(1)
        ty = ty - 1
    