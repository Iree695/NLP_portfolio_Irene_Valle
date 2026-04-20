# Lab 4: Speech Recognition and Synthesis
import sounddevice as sd
import soundfile as sf
import whisper
from gtts import gTTS
import os

# Recording audio:
SAMPLE_RATE = 16000
CHANNELS = 1
TEMP_WAV = "recording.wav"

def record_audio(seconds = 4):
    print("Recording...")
    recording = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    sf.write(TEMP_WAV, recording, SAMPLE_RATE)
    print("Recording saved as", TEMP_WAV)
    return TEMP_WAV

# Structures
# Local Stt using Whisper:
def local_stt(wav_path):
    model = whisper.load_model("base")
    result = model.trascribe(wav_path)
    return result["text"]

def demo_local_stt():
    wav = record_audio()
    text = local_stt(wav)
    print("Transcribed Text:", text)

# Local TTS using gTTS:
def demo_local_tts():
    ...

def demo_external_stt():
    ...

def demo_external_tts():
    ...

def demo_extra_speech_task():
    ...

def main():
    while True:
        print("1. Local STT")
        print("2. Local TTS")
        print("3. External STT")
        print("4. External TTS")
        print("5. Extra Speech Task")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            demo_local_stt()
        elif choice == '2':
            demo_local_tts()
        elif choice == '3':
            demo_external_stt()
        elif choice == '4':
            demo_external_tts()
        elif choice == '5':
            demo_extra_speech_task()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

