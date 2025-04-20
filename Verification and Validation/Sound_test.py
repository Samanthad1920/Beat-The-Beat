# Libraries
from pygame import mixer


# Main Program
if __name__ == '__main__':
    song = "test_audio.mp3"
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()
    input("Press enter to stop music playback!")
    mixer.music.stop()
