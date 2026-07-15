AI Skin Specialist
AI Skin Specialist is a Gradio-based consultation assistant that accepts a patient voice description plus a skin image or video, transcribes the patient audio, sends the visual/text context to an AI model, and returns both a written and spoken doctor-style response.

The current app uses:

Gradio for the web interface.
Groq Whisper for patient voice transcription.
Groq vision model for image-based skin guidance.
Deepgram text-to-speech for the doctor audio response.
uv for Python version, virtual environment, dependency, and lockfile management.
Important: this project provides general informational guidance only. It is not a medical diagnosis and should not replace care from a licensed dermatologist or clinician.