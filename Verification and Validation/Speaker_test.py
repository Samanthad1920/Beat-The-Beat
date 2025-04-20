# -*- coding: utf-8 -*-
"""
Beat the Beat! System Test Verification
Speaker Component
"""

# Libraries
from pygame import mixer

SONG_FILE = "test_audio.mp3"

# Functions
def playSong():
    """Plays loaded song file."""
    mixer.music.play()
    
def stopSong():
    """Stops the currently playing song."""
    mixer.music.stop()

# Main Program
if __name__ == '__main__':
    mixer.init()
    mixer.music.load(SONG_FILE)
    playSong()
    input("Press enter to stop music playback!")
    stopSong()    


