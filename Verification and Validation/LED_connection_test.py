"""
LED Solder Connection Test
"""

# Libraries
import time
from rpi_ws281x import *

LED_COUNT       = 60      # number of LED pixels per strip
TEST_LED_PIN1   = 18      # GPIO Pin 18
TEST_LED_PIN2   = 21      # GPIO Pin 21
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS  = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip1 = Adafruit_NeoPixel(LED_COUNT, TEST_LED_PIN1, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0)
strip2 = Adafruit_NeoPixel(LED_COUNT, TEST_LED_PIN2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 0)

if __name__ == '__main__':
    strip1.begin()
    strip2.begin()