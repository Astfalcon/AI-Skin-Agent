# Create API Keys

# Create Client and Send Request
from deepgram import DeepgramClient
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOCTOR_AUDIO = BASE_DIR / "doctor_response.mp3"

def convert_text_to_doctor_audio(text, output_filepath=None):
    if output_filepath is None:
        output_filepath = DEFAULT_DOCTOR_AUDIO

    deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
    deepgram = DeepgramClient(api_key=deepgram_api_key)

    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model=os.environ.get("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en"),
        encoding="mp3",
    )

    output_filepath = Path(output_filepath)

    with output_filepath.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    return output_filepath
import subprocess
import platform
def play_audio(audio_filepath):
    audio_filepath = str(audio_filepath)

    if platform.system() == "Darwin":
        subprocess.run(["afplay", audio_filepath], check=False)
    elif platform.system() == "Windows":
        os.startfile(audio_filepath)
    else:
        subprocess.run(["xdg-open", audio_filepath], check=False)

if __name__ == "__main__":
    text = "Hello! I am Doctor AI. How can I help you today?"

    print("Generating audio...")
    audio_path = convert_text_to_doctor_audio(text)

    print(f"Saved to: {audio_path}")

    print("Playing audio...")
    play_audio(audio_path)

"""api_key = os.environ.get("DEEPGRAM_API_KEY")
text = "Hi, my name is ADWAIT TARPE, who are you?. I am very happy."
api_key = os.environ.get("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(api_key=api_key)
try:
    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="mp3",
    )
    print("Audio generated successfully")
except Exception as e:
    print("Deepgram error:")
    print(e)
    raise

# Save Audio

from pathlib import Path

audio_file="test-output.mp3"
audio_path = Path(__file__).with_name(audio_file)
with audio_path.open("wb") as file:
    for chunk in audio:
        file.write(chunk)

# Play Audio
import platform
import subprocess


if platform.system() == "Darwin":  # macOS
    subprocess.run(["afplay", str(audio_path)])
elif platform.system() == "Windows":
    os.startfile(audio_path)
else:  # Linux
    subprocess.run(["xdg-open", str(audio_path)])"""