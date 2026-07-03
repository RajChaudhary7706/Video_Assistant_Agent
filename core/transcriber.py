#Here we use whisper key for transcription and translation of 
# audio files. We define functions to load the model, transcribe
# a single chunk, and transcribe all chunks. The model is loaded
# only once for efficiency.

import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    global _model

    if _model is None:
        _model = whisper.load_model(WHISPER_MODEL)

    return _model


def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    model = load_model()

    result = model.transcribe(
        chunk_path,
        task="translate" if translate else "transcribe"
    )

    return result["text"]


def transcribe_all(chunks: list, translate: bool = False) -> str:
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + " "

    return full_transcript.strip()