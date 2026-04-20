# Lab 4
# Libraries:
import sounddevice as sd            # For recording audio
import soundfile as sf              # For saving audio files
import whisper                      # For local speech recognition
from gtts import gTTS               # For local text-to-speech
import os                           # For file operations
from transformers import pipeline   # For external STT and TTS models
import librosa                      # For audio processing 

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "generated_audio")

# Create folder if it doesn't exist
os.makedirs(AUDIO_DIR, exist_ok=True)

# Recording audio:
SAMPLE_RATE = 16000
CHANNELS = 1
TEMP_WAV = os.path.join(AUDIO_DIR, "recording.wav")

def record_audio(seconds = 4):
    print("Recording...")
    recording = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    sf.write(TEMP_WAV, recording, SAMPLE_RATE)
    print("Recording saved as", TEMP_WAV)
    return TEMP_WAV

# Generation of audio files:
def generate_test_audio(text, out_file="test_input.wav"):
    out_path = os.path.join(AUDIO_DIR, out_file)
    temp_mp3 = os.path.join(AUDIO_DIR, "temp.mp3")

    # Convert text to speech
    tts = gTTS(text=text, lang="en")
    tts.save(temp_mp3)

    # Convert mp3 to wav using librosa
    audio, sr = librosa.load(temp_mp3, sr=16000)
    sf.write(out_path, audio, 16000)
    print(f"Test audio generated and saved as {out_path}")
    return out_path

# Local STT using Whisper:
def local_stt(wav_path):
    # Load audio manually to avoid FFmpeg
    audio, sr = librosa.load(wav_path, sr=16000)

    model = whisper.load_model("base")
    result = model.transcribe(audio)
    return result["text"]

def demo_local_stt():
    wav = generate_test_audio("turn on the light")
    text = local_stt(wav)
    print("Transcribed Text:", text)

# Local TTS using gTTS:
def local_tts(text, out_file="local_tts.wav"):
    out_path = os.path.join(AUDIO_DIR, out_file)
    tts = gTTS(text = text, lang= "en")
    tts.save(out_path)
    print("Text-to-Speech saved as", out_path)
    return out_path

def demo_local_tts():
    text = input("Enter text to convert to speech: ")
    local_tts(text)

# External STT:
def external_stt(wav_path):
    stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small", device ="cpu")
    result = stt_pipeline(wav_path)
    return result["text"]

def demo_external_stt():
    wav = generate_test_audio("what time is it?")
    text = external_stt(wav)
    print("Transcribed Text:", text)

# External TTS:
def external_tts(text, out_file="external_tts.wav"):
    out_path = os.path.join(AUDIO_DIR, out_file)
    tts_pipeline = pipeline("text-to-speech", model="espnet/kan-bayashi_ljspeech_vits")
    audio = tts_pipeline(text)
    sf.write(out_path, audio["audio"], audio["sampling_rate"])
    print("Text-to-Speech saved as", out_path)
    return out_path

def demo_external_tts():
    text = input("Enter text to convert to speech: ")
    external_tts(text)

# Extra speech task: speech emotion recognition
def extra_speech_task(wav_path):
    # Load audio manually to avoid FFmpeg
    audio, sr = librosa.load(wav_path, sr=16000)

    emotion_pipeline = pipeline(
        "audio-classification",
        model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
        device="cpu"
    )

    results = emotion_pipeline({"raw": audio, "sampling_rate": sr}, top_k=3)
    return results

def demo_extra_speech_task():
    print("Extra Speech Task: Speech Emotion Recognition")
    print("1. Record audio")
    print("2. Use generated test audio")

    choice = input("Enter your choice: ")

    if choice == "1":
        wav = record_audio()
    elif choice == "2":
        wav = generate_test_audio("I am very happy today")
    else:
        print("Invalid choice. Using generated test audio.")
        wav = generate_test_audio("I am very happy today")

    results = extra_speech_task(wav)

    print("Detected emotions:")
    for item in results:
        print(f"{item['label']}: {item['score']:.2f}")

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

