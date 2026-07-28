from faster_whisper import WhisperModel
import os

# Load the model only once
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def generate_transcript(audio_path):
    """
    Generate transcript from an interview recording.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"{audio_path} not found")

    segments, info = model.transcribe(audio_path)

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return transcript.strip()