# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program

@author: Sasha Folloso
"""

# Libraries
import numpy as np
import pandas as pd
import random
import time

# Classes

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
    
    for i, beat_time in enumerate(beat_times):
        possible_pads = [0, 1, 2, 3]
        if previous_pad is not None:
            possible_pads.remove(previous_pad)
        pad_number = random.choice(possible_pads)
        previous_pad = pad_number
            
        beats_data.append({
            'Beat Number': i + 1,
            'Pad #': pad_number,
            'User Hit': False,
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
    
def main():
    """The main program where everything happens."""
    # Pandas Dataframe Configuration
    pd.set_option('display.max_columns', None)  # shows all columns
    pd.set_option('display.max_rows', None)  # shows all rows
    pd.set_option('display.expand_frame_repr', False)  # disables line wrapping
    pd.set_option('display.width', 0)  # automatically adjusts width to the console size
    
    # Extract data from laptop program
    beat_times = extractTimes("generatedMap.txt")
    beat_leadup = extractTimes("beatLeadUp.txt")
    atw_start = extractTimes("atwBefore.txt")
    atw_end = extractTimes("atwAfter.txt")
    ptw_start = extractTimes("ptwBefore.txt")
    ptw_end = extractTimes("ptwAfter.txt")
    
    # Store in local table for visual indication module and user interaction module to reference
    storeCharTable(beat_times, beat_leadup, atw_start, atw_end, ptw_start, ptw_end)
    
    # Other prior song session functions/config
    
    # Entering the song session

# Main Program
if __name__ == '__main__':
    main()