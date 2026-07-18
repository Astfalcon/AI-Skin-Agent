# Step1 : Record audio from microphone
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio_from_microphone(file_path, timeout=20, phrase_time_limit=None):
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        logging.info("Recording audio from microphone...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        logging.info("Audio recording complete.")

    # Convert audio data to WAV format
    audio_bytes = BytesIO(audio_data.get_wav_data())
    audio_segment = AudioSegment.from_file(audio_bytes, format="wav")
    audio_segment.export(file_path, format="wav")
    logging.info(f"Audio saved to {file_path}")

audio_file_path = "patient_voice_text.mp3"
record_audio_from_microphone(audio_file_path, timeout=20, phrase_time_limit=10)

# Step2 : Convert audio to text 

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)
with open(audio_file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model=os.environ.get("WHISPER_MODEL", "whisper-large-v3"),
    )

    print(transcription.text)
    