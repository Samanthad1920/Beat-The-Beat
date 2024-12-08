# -*- coding: utf-8 -*-
"""
[Beat Timing Windows Test]

Created on Sun Dec  8 11:47:40 2024

@author: Sasha Folloso
"""

# Libraries

# Classes
class Beat:
    def __init__(self, beat_time:float):
        """Generates the ATW and PTW for each beat."""
        self.beat_time = beat_time
        self.generateATW()
        self.generatePTW()
        self.generateLeadUp()
    
    def generateATW(self):
        """Generates the upper and lower bounds of the 1 second
        Accurate Time Window (ATW)."""
        self.lower_ATW = round(self.beat_time - (1/3), 3)
        self.upper_ATW = round(self.beat_time + (2/3), 3)
    
    def generatePTW(self):
        """Generates the upper and lower bounds of the 1/2 second
        Precise Time Window (PTW). Awards user double points."""
        self.lower_PTW = round(self.beat_time - (1/6), 3)
        self.upper_PTW = round(self.beat_time + (2/6), 3)
        
    def generateLeadUp(self):
        """Generates the time window in which LEDs should indicate
        the approach of an upcoming beat."""
        self.begin_leadup = round(self.beat_time - 1, 3)
        # do we need to generate a window of time for this or
        # just when to begin the lead up visuals?

# Functions
def testBeatInfo():
    """Prints example beat info."""
    beat1 = Beat(8.345)
    print(f"This is the ATW for beat 1: [{beat1.lower_ATW}s, {beat1.upper_ATW}s]")
    print(f"This is the PTW for beat 1: [{beat1.lower_PTW}s, {beat1.upper_PTW}s]")
    print(f"Lead up begins at {beat1.begin_leadup}s")
    print(f"The actual beat is at {beat1.beat_time}s")
    
def extractBeatTimes(file_name:str):
    """Reads .txt file of beat time values from beat detection algorithm and extracts
    the string data into a list of float values."""
    with open(file_name, 'r') as file:
        data = file.read() # stores content into data variable
        data = data.replace("[","").replace("]","") # removes brackets from data
        float_times = [float(value) for value in data.split()]
    return float_times

def processBeatData(beat_times: list[float]): #input should be a list of float values
    pass



def main():
    testBeatInfo()
    beat_times = extractBeatTimes("beatMap.txt")
    print(beat_times)
    processBeatData(beat_times)

# Main Program
if __name__ == '__main__':
    main()