# -*- coding: utf-8 -*-
"""
Beat the Beat! System Test Verification
1602 LCD Component
"""

# Libraries
import time
from rpi_lcd import LCD

# Display Word Banks
word_bank = ['skyscraper', 'Taco Bell', 'candlelight', 'cheese grater',
             'hallelujah', 'Thank you!', 'daylight', 'record player', 
             'pirate ship', 'keyboard', 'Detroit, MI', 'fishing rod',
             'top hat', 'conveyor belt', 'sweater weather', '42nd Street',
             'permanent', 'tattoo sleeve', 'scoreboard', 'corn on the cob',
             'milkshake', 'vocalist', 'paperclip', 'microphone', 'highscore',
             'sprained ankle', 'ice cream cone', 'trading card game',
             'dice roll', 'high score', 'jellybeans', 'drive-in movie',
             'prescription', 'doorknob', 'aquarium', 'zookeeper',
             'board game', 'headphones', 'truck driver', 'chalkboard',
             'New York City', 'molecule', 'subway sandwich', 'feather',
             'train ticket', 'hand sanitizer', 'meteor shower', 'penguin',
             'lightbulb', 'chicken nugget'
]

# Main Program
if __name__ == '__main__': 
    lcd = LCD()
    
    option = input("1: Legibility Test \n2: Refresh Rate Test \n3: Exit Program\n")
    option = int(option)
    
    if option == 1: # Test 1: Legibility Test
        for i in range(50):
            print(f'Current word: {word_bank[i]}')
            lcd.text('Word {i} of 50:',1)
            lcd.text(str(word_bank[i]),2)
            input() # Press enter to proceed onto the next word.
            
    elif option == 2: # Test 2: Refresh Rate Test
        lcd.text('Refresh Rate Test',1)
        for i in range(100):
            num = (1 + i) * 11111
            print(num)
            lcd.text(str(num),2)
            time.sleep(.01)
    
    elif option == 3: # Exit Program
        exit()
