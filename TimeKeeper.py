# -*- coding: utf-8 -*-
"""
Beat the Beat! Main Program Modularized
Time Keeper
Version 1.0 

@author: Samantha DuBois
"""
import time
import logging

class TimeKeeper:
    def __init__(self, song_char_table, args_dict, lock, update_event, stop_event):
        """
        Initialize the TimeKeeper.
        
        song_char_table: The table containing beat timings and other data.
        args_dict: Shared dictionary for storing session time and index.
        lock: Lock for synchronizing access to shared data.
        update_event: Event to notify other processes when time is updated.
        stop_event: Event to signal when the e-stop button is pressed.
        """
        self.song_char_table = song_char_table
        self.args_dict = args_dict
        self.lock = lock
        self.update_event = update_event
        self.stop_event = stop_event
        self.index = args_dict["index"]
        self.start_time = time.time()
        
        # Logging Setup
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s : %(message)s")
        
    def run(self):
        """Main loop to track the time and update beat index."""
        while not self.stop_event.isSet():
            # Track the current session time
            current_time = time.time()
            session_time = current_time - self.start_time

            with self.lock:  # Ensure safe access to shared data
                self.args_dict["session_time"] = session_time
                beat_time = self.song_char_table.loc[self.index, 'Beat Time (s)']
                
                if session_time >= beat_time:
                    self.index += 1
                    self.args_dict["index"] = self.index
                    logging.debug(f"Index Updated: {self.index}, \tSession Time: {session_time}")

            self.update_event.set()  # Notify other processes of the update
            time.sleep(0.01)  # Small sleep to prevent high CPU usage
