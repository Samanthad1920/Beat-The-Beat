# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program Modularized
LED Controller
Version 1.0 

0: north
1: right
2: south
3: left

@author: Samantha DuBois
"""
import time
from rpi_ws281x import Adafruit_NeoPixel, Color

class LEDController:
    def __init__(self, strip):
        self.strip = strip

    def leadUpLED(self, color, pad, wait_ms=250):
        """Lead up LED indication to alert the user of an incoming beat."""
        if pad == 0 or pad == 2: # north or south
            for i in range(4):
                self.strip.setPixelColor(i, color)
                self.strip.setPixelColor(i+5, color)
                self.strip.setPixelColor(i+10, color)
                self.strip.setPixelColor(i+15, color)
                self.strip.setPixelColor(i+20, color)
                self.strip.setPixelColor(i+25, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
        elif pad == 1 or pad == 3:
            for i in range(4): # right or left
                self.strip.setPixelColor(30 + i, color)
                self.strip.setPixelColor(30 + i + 5, color)
                self.strip.setPixelColor(30 + i + 10, color)
                self.strip.setPixelColor(30 + i + 15, color)
                self.strip.setPixelColor(30 + i + 20, color)
                self.strip.setPixelColor(30 + i + 25, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def beatLED(self, color, pad):
        """On-beat LED indication to show the user when the beat occurs."""
        if pad == 0 or pad == 2:
            for i in range(5):
                self.strip.setPixelColor(i, color)
                self.strip.setPixelColor(i + 5, color)
                self.strip.setPixelColor(i + 10, color)
                self.strip.setPixelColor(i + 15, color)
                self.strip.setPixelColor(i + 20, color)
                self.strip.setPixelColor(i + 25, color)
            self.strip.show()
        elif pad == 1 or pad == 3:
            for i in range(5):
                self.strip.setPixelColor(30 + i, color)
                self.strip.setPixelColor(30 + i + 5, color)
                self.strip.setPixelColor(30 + i + 10, color)
                self.strip.setPixelColor(30 + i + 15, color)
                self.strip.setPixelColor(30 + i + 20, color)
                self.strip.setPixelColor(30 + i + 25, color)
            self.strip.show()
        
        # Wait for 0.5 seconds and then clear the LEDs
        time.sleep(0.5)
        self.clear_leds()

    def clear_leds(self):
        """Clears all LEDs by turning them off."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
