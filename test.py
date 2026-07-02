from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://youtu.be/kYkZI3oj2W4?si=w1ZLfu0k-Fu7BCUn"

source = process_input(source)

transcribe_all(source, translate=False)