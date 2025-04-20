# -*- coding: utf-8 -*-
"""
========================================
Beat the Beat! User Interaction Module
version: 1.0
========================================
"""

# Libraries
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Constants
DEFAULT_PT_VALUE = 1000
PRECISE_PT_VALUE = 2 * DEFAULT_PT_VALUE

N_SWITCH_PIN = 5    # GPIO 5
R_SWITCH_PIN = 26    # GPIO 6
S_SWITCH_PIN = 6   # GPIO 26
L_SWITCH_PIN = 16   # GPIO 16

# Functions
def configSwitch():
    """Configures GPIO pins for each of the four limit switches."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(N_SWITCH_PIN, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(R_SWITCH_PIN, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(S_SWITCH_PIN, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(L_SWITCH_PIN, GPIO.IN, GPIO.PUD_DOWN)

def calculateScore(current_score:int, hit_time:float, atw_start:float, atw_end:float, ptw_start:float, ptw_end:float):
    """Calculates score whenever a hit is detected."""
    if atw_start <= hit_time <= atw_end:
        if ptw_start <= hit_time <= ptw_end:
            new_score = current_score + PRECISE_PT_VALUE
            return new_score
        else:
            new_score = current_score + DEFAULT_PT_VALUE
            return new_score
    else:
        return current_score

def main():
    """Testing main function."""
    configSwitch()
    while(True):
        n_switch_state = GPIO.input(N_SWITCH_PIN)
        r_switch_state = GPIO.input(R_SWITCH_PIN)
        s_switch_state = GPIO.input(S_SWITCH_PIN)
        l_switch_state = GPIO.input(L_SWITCH_PIN)
        if n_switch_state == GPIO.HIGH:
            print("User hit the left pad!")
        elif r_switch_state == GPIO.HIGH:
            print("User hit the north pad!")
        elif s_switch_state == GPIO.HIGH:
            print("User hit the south pad!")
        elif l_switch_state == GPIO.HIGH:
            print("User hit the right pad!")
        time.sleep(0.2)
    
# Main Program
if __name__ == '__main__':
    main()
