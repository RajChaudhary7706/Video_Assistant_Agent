#Here we use whisper key for transcription and translation of 
# audio files. We define functions to load the model, transcribe
# a single chunk, and transcribe all chunks. The model is loaded
# only once for efficiency.

import whisper
import os
import requests
from pydub import AudioSegment

SARVAM_PIECE_SECONDS = 25

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
SARVAM_STTT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text"

_model = None


def _normalize_env_value(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip().strip('"').strip("'")


def get_sarvam_api_key() -> str | None:
    return _normalize_env_value(os.getenv("SARVAM_API_KEY"))


def get_sarvam_model() -> str:
    model = _normalize_env_value(os.getenv("SARVAM_STT_MODEL"))
    if not model:
        return "saaras:v3"
    if model in {"saaras:v2.5", "saarika:v2.5"}:
        return "saaras:v3"
    return model


def load_model():
    global _model

    if _model is None:
        _model = whisper.load_model(WHISPER_MODEL)

    return _model

def transcribe_chunk_whisper(chunk_path: str, translate: bool = False) -> str:
    model = load_model()

    result = model.transcribe(
        chunk_path,
        task="translate" if translate else "transcribe"
    )

    return result["text"]

def _send_to_sarvam(chunk_path: str)->str:
    sarvam_api_key = get_sarvam_api_key()

    headers = {
        "api-subscription-key": sarvam_api_key,
    }
    with open(chunk_path, "rb") as f:
        files = {"file": (os.path.basename(chunk_path), f, "audio/wav")}
        data = {"model": get_sarvam_model(), "mode": "translate", "with_diarization": "false"}
        response = requests.post(
            SARVAM_STTT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )
        
    if not response.ok:
        print(f"\n❌ Sarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()
        
    return response.json().get("transcript","")

def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio. We split this chunk into
    25-second pieces, send each separately, and join the transcripts.
    """
    if not get_sarvam_api_key():
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""
    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start: start + piece_ms]
        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """Route one chunk to whiaper or sarvam based on the language parameter.
    -english: Whisper(local model)
    - hinglish:Sarvam (translate to english)
    """
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)    
    return transcribe_chunk_whisper(chunk_path)

def transcribe_all(chunks: list, language: str = "english") -> str:
    full_transcript = ""
    
    engine = "SARVAM AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        text = transcribe_chunk(chunk, language=language)
        full_transcript += text + " "

    return full_transcript.strip()