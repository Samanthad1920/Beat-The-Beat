# -*- coding: utf-8 -*-
"""
========================================
Beat the Beat! Song Processing Module
version: 1.0
========================================
"""

# Libraries
import random
import pandas as pd

# Functions
def extractTimes(filename:str):
    """Extracts beat times from beat generation algorithm output."""
    with open(filename, 'r') as file:
        data = file.read()
        data = data.replace("[","").replace("]","")
        time_list = [round(float(value), 3) for value in data.split()]
    file.close()  
    return time_list

def storeCharTable(beat_times:list, beat_leadup:list, atw_start:list, atw_end:list, ptw_start:list, ptw_end:list):
    """Calculates the characteristics of every beat and stores in table."""
    beats_data = []
    previous_pad = None
    prevprev_pad = None
    
    for i, beat_time in enumerate(beat_times):
        possible_pads = [0, 1, 2, 3]
        if prevprev_pad is not None:
            possible_pads.remove(prevprev_pad)
        if previous_pad is not None:
            possible_pads.remove(previous_pad)
            prevprev_pad = previous_pad
        pad_number = random.choice(possible_pads)
        previous_pad = pad_number
            
        beats_data.append({
            'Beat Number': i + 1,
            'Pad #': pad_number,
            'User Hit': False,
            'LED Activated': False,
            'Lead Up Start (s)': beat_leadup[i],
            'ATW Start (s)': atw_start[i],
            'PTW Start (s)': ptw_start[i],
            'Beat Time (s)': beat_times[i],
            'PTW End (s)': ptw_end[i],
            'ATW End (s)': atw_end[i]  
        })
        
    song_char_table = pd.DataFrame(beats_data)
    print(song_char_table)
    return song_char_table