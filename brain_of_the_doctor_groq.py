import base64
import os
import sys
from io import BytesIO
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from PIL import Image

# Load environment variables from .env file
load_dotenv()


def encode_image_for_groq(filepath: str) -> str:
    """
    Open an image, resize it to at most 1024x1024,
    convert to JPEG and return a base64-encoded string.
    """
    image = Image.open(filepath)
    image.thumbnail((1024, 1024))

    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def brain_of_the_doctor(
    patient_text: str,
    image_filepath: Optional[str] = None,
    video_filepath: Optional[str] = None,
) -> str:
    """
    Send a patient's description and a skin image to Groq's vision model.
    Returns a short, natural doctor‑style response (no markdown).
    The video parameter is ignored; Groq cannot process video directly.
    """
    # --- Validation ---
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env or environment")

    if not image_filepath:
        raise ValueError("Groq vision requires an image. Please upload a skin image.")

    # --- Prepare image ---
    image_data = encode_image_for_groq(image_filepath)

    # --- Build the prompt ---
    prompt = (
        "You are a confident, natural doctor specializing in skin care. "
        "Speak with the reassurance, clarity, and authority of a real doctor. "
        "Limit your entire response to two or three sentences maximum. "
        "If the patient has provided a video, explain that you are reviewing the uploaded image "
        "because this model cannot process video directly. "
        "Do not use any special characters, symbols, asterisks, or markdown formatting "
        "because your response will be converted directly to audio.\n\n"
        f"Patient text: {patient_text}"
    )

    if video_filepath:
        prompt += "\nThe patient also uploaded a video, but use the provided image as the visual reference."

    # --- Create client and send request ---
    client = Groq(api_key=groq_api_key)
    model = os.environ.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

    response = client.chat.completions.create(
        model=model,
        max_completion_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": "You are a careful skin care assistant. Give general information, not a diagnosis.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                        },
                    },
                ],
            },
        ],
    )

    # --- Handle the possible None return from the API ---
    result = response.choices[0].message.content
    if result is None:
        # Return a fallback message or raise an exception, depending on your needs.
        return "I'm sorry, I couldn't generate a response at this moment."
    return result


# ----------------------------------------------------------------------
# Example usage (run directly as a script)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Default test values – change these or pass via command line
    test_patient_text = "I have a red, itchy patch on my arm. What should I do?"
    test_image_path = "sample-skin-image.jpg"   # <-- Replace with your image
    test_video_path = None                      # optional, ignored

    # Allow command line arguments: python brain_of_the_doctor.py "text" "image.jpg"
    if len(sys.argv) > 1:
        test_patient_text = sys.argv[1]
    if len(sys.argv) > 2:
        test_image_path = sys.argv[2]
    if len(sys.argv) > 3:
        test_video_path = sys.argv[3]

    try:
        answer = brain_of_the_doctor(
            patient_text=test_patient_text,
            image_filepath=test_image_path,
            video_filepath=test_video_path,
        )
        print(answer)
    except Exception as e:
        print(f"Error: {e}")


"""# Install and import dependencies
from groq import Groq
from dotenv import load_dotenv
from groq.types.chat import ChatCompletionMessageParam
from typing import cast
import os
import base64
import mimetypes

load_dotenv()

# Create Client
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Create Text Message

messages: list[ChatCompletionMessageParam] = [
    {
        "role": "user",
        "content": "Hello, what is your name groq?"
    }
]

# Create Image Message

folder = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(folder, "luffy.jpg")

with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

message_image = cast(
    list[ChatCompletionMessageParam],
    [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What do you see in this image? and which anime character is this?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        }
    ],
)

# Create Image Message

folder = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(folder, "luffy.jpg")

with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

message_image = cast(
    list[ChatCompletionMessageParam],
    [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What do you see in this image? and which anime character is this?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        }
    ],
)

# Send Message
 
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=message_image,
    max_tokens=100
)

# Print Response

print(response.choices[0].message.content)"""