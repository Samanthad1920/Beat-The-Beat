# 🥁 Beat-The-Beat

**Beat-The-Beat** is a Python-based audio analysis and beatmap generation tool. It processes audio input to detect beats, generate timing data, and provide synchronized visual or interactive output. This project is useful for rhythm game development, music analysis, or creative musical experiments.

---

## 📦 Features

- ⏱️ Beat detection using signal processing libraries (`librosa`, `scipy`)
- 🎧 Audio file handling and playback via `pydub`
- 📊 Modular architecture for visualization, UI interaction, and audio control
- 📁 Support for loading/saving beatmap data to text files
- ⚙️ Emergency stop module (`module_estop.py`) for runtime safety and control

---

## 🧠 Project Structure
<pre lang="markdown"><code>
Beat-The-Beat/
├── BeatTheBeat!/ # Final program folder
│ ├── README.txt
| ├── main.py # Main orchestrator
│ ├── text_audio.mp3
| 
│ ├── atwBefore.txt # Intermediate beat processing output
| ├── atwAfter.txt
| ├── ptwBefore.txt
| ├── ptwAfter.txt
| ├── beatLeadUp.txt # Beat anticipation or lead-in data
| ├── generatedMap.txt # Final generated beatmap (timing events)
| 
| ├── module_sp.py # Signal processing helpers
| ├── module_sound.py # Audio playback and control
| ├── module_visual.py # Visual synchronization or output
| ├── module_ui.py # User interface (console or GUI)
| └── module_estop.py # Emergency stop / kill-switch mechanism
|
├── beatAlgorithm/ #Audio analysis logic
│ ├── AlgorithmCode.py # Core beat detection / analysis logic
│ └── requirements.txt # Dependency list
|
├── Verification and Validation/ # Hardware and functional tests
| ├── ADAFRUIT_TEST
| ├── LCD_test.py
| ├── LED_connection_test.py
| ├── LED_test.py
| ├── Sound_test.py
| ├── Speaker_test.py
| └── test_audio.mp3
|
└── .gitignore 
</code></pre>
---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or newer
- FFmpeg (required by `pydub` for audio decoding)

### Install Python dependencies

```bash
pip install -r beatAlgorithm/requirements.txt
```

If you don't have FFmpeg installed, you can install it via:
- Windows: Download [FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH
- macOS (Homebrew):
```bash
brew install ffmpeg
```
- Linux:
```bash
sudo apt install ffmpeg
```
---
## 🚀 Usage
To run the full system:
```bash
cd BeatTheBeat!
python main.py
```
To run just the beat detection logic:
```bash
cd beatAlgorithm
python AlgorithmCode.py
```
Ensure your audio file is correctly specified in the code (typically via a hardcoded path or passed as an argument).

---

## 📄 Output Files
The following files are generated inside the `BeatTheBeat!/` folder:

|File	| Description |
|-----|-------------|
|`BeatTheBeat!/atwBefore.txt`	|Beat timestamps before adjustment|
|`BeatTheBeat!/atwAfter.txt`	|Processed/shifted timestamps|
|`BeatTheBeat!/ptwBefore.txt`	|Peak timing window data (pre-processed)|
|`BeatTheBeat!/ptwAfter.txt`	|Peak timing window data (post-processed)|
|`BeatTheBeat!/beatLeadUp.txt`	|Lead-in data for beat anticipation (visual/timing aid)|
|`BeatTheBeat!/generatedMap.txt`	|Final exported beatmap, usable in rhythm-based projects|

---

## 👥 Authors

- [follosoraptor](https://github.com/follosoraptor)
- [Samanthad1920](https://github.com/Samanthad1920)
- [rhit-duboissk](https://github.com/rhit-duboissk)
- [singersa9](https://github.com/singersa9)
