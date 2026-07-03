from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
import os
print("Current Directory:", os.getcwd())
print("SARVAM_API_KEY:", os.getenv("SARVAM_API_KEY"))

source = "https://youtu.be/LxAxV6Eg8mo?si=sNvH3Bbo-CdIY5Ix"
language = "hinglish"  

chunks = process_input(source)
print("\n=== TRANSCRIPTION START ===\n")
print(transcribe_all(chunks, language=language))