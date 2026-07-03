from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://youtu.be/O4GorB4N2Kg?si=bNQRW6aIJpfxBcd7"

source = process_input(source)

print(transcribe_all(source, translate=False))