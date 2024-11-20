# -*- coding: utf-8 -*-
"""
Excursion 2: Displaying to LCD

Definition of Excursion:
- Acquire a display, PI 4 processor, and relevant software tools
- Integrate the display with the Raspberry Pi  
- Create a simple program that sends text and numbers to the display 
- Decide what character spaces will be reserved for which values to ensure legibility of important data to a user that is one foot away

The results of this excursion will be used to define:
- The expected readability of the display
- The refresh rate to ensure real-time feedback
- The expected display latency and clarity

@author: Sasha Folloso, Samantha DuBois
"""

# Libraries
import numpy as np
import threading
import time
from rpi_lcd import LCD
from signal import signal, SIGTERM, SIGHUP, pause
from pynput.keyboard import Key, Listener

keyPress = False
# Functions
def safe_exit(signum, frame):
    exit(1)
    
def userInput(key): #works fine ??
    """Detects the time in which the user hits the Spacebar."""
    if key == Key.space:
        global keyPress
        global inputTime
        keyPress = True    
        inputTime = time.time()
        
def stopUserInput(key): #works fine
    """Stops listening for user inputs when Esc is pressed."""
    if key == Key.esc:
        return False
    
def listenForInput(): #works fine
    """Enables input monitoring."""
    with Listener(on_press=userInput, on_release=stopUserInput) as listener:
        listener.join()

def main():
    lcd = LCD()
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    
    global keyPress
    
    displayTest = True
    menu = True
    option1 = False
    option2 = False
    option3 = False
    
    lcd.clear()
    lcd.text("Welcome to", 1)
    lcd.text("Excursion 2!", 2)
    time.sleep(5)
    
    while displayTest == True:
        while menu == True:
            #Prompts for a test mode
            lcd.clear()
            lcd.text("Choose a mode:", 1)
            lcd.text("1, 2, or 3", 2)
            option = int(input('Console message: Choose a mode: 1, 2, or 3'))
            match option:
                case 1:
                    option1 = True
                    menu = False
                    break
                case 2:
                    option2 = True
                    menu = False
                    break
                case 3:
                    option3 = True
                    menu = False
                    break
                case 4:
                    menu = False
                    break
                case _:
                    print("Console message: not a valid option!")
        
        if option1 == True: # Character Display Mode
            lcd.clear()
            lcd.text("Will now show", 1)
            lcd.text("various chars", 2)
            time.sleep(3)
            lcd.clear()
            lcd.text("0123456789ABCDEF", 1)
            lcd.text("!@#$%^&*()-+=_/;", 2)
            time.sleep(3)
            lcd.clear()
            lcd.text("Returning", 1)
            lcd.text("to main menu", 2)
            time.sleep(3)
            option1 = False
            menu = True
            continue
            
        if option2 == True: # Count Example Mode
            lcd.clear()
            lcd.text("Now showing:", 1)
            lcd.text("Example count", 2)
            time.sleep(3)
            lcd.text("Current score:", 1)
            for x in range(10):
                score = 1200 * x
                lcd.text(str(score), 2)
                time.sleep(.5)            

            lcd.clear()
            lcd.text("Returning", 1)
            lcd.text("to main menu", 2)
            time.sleep(3)
            option2 = False
            menu = True
            continue
        
        if option3 == True: # Reaction Time Mode
            inputThread = threading.Thread(target = listenForInput) 

            inputReceived = False
            lcd.clear()
            lcd.text("Now testing:", 1)
            lcd.text("Reaction time", 2)
            time.sleep(5)
            lcd.clear()
            lcd.text("Press space", 1)
            lcd.text("when u see go!", 2)
            time.sleep(3)
            lcd.clear()
            inputThread.start()
            startTime = time.time()
            lcd.text("Go!", 1, 'center')
            while inputReceived == False:
                if keyPress == True:
                    inputReceived = True
                    continue
            reactionTime = inputTime - startTime
            lcd.clear()
            lcd.text("Reaction time:", 1)
            lcd.text(str(round(reactionTime,3)) + "s", 2)
            time.sleep(5)
            lcd.clear()
            lcd.text("Returning", 1)
            lcd.text("to main menu", 2)
            time.sleep(3)            
            keyPress = False
            option3 = False
            menu = True
            continue
        if (menu == False) and (option1 == False) and (option2 == False) and (option3 == False):
            lcd.clear()
            break # should only run if 4 is pressed in menu

# Main Program
if __name__=='__main__':
    main()
