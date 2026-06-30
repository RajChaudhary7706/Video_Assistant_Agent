import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """
    Download YouTube audio as WAV.
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".wav"

    return filename


def convert_to_wav(input_path: str) -> str:
    """
    Convert audio to 16kHz mono WAV.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)

    audio.export(output_path, format="wav")

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list[str]:
    """
    Split WAV into chunks.
    """

    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"File not found: {wav_path}")

    audio = AudioSegment.from_wav(wav_path)

    chunk_ms = chunk_minutes * 60 * 1000

    print(f"Audio Length : {len(audio)} milliseconds")
    print(f"Chunk Size   : {chunk_minutes} minutes")

    chunks = []

    base_name = os.path.splitext(wav_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        end = min(start + chunk_ms, len(audio))

        chunk = audio[start:end]

        chunk_filename = f"{base_name}_chunk_{i+1}.wav"

        chunk.export(chunk_filename, format="wav")

        chunks.append(chunk_filename)

        print(f"Created: {chunk_filename}")

    return chunks


if __name__ == "__main__":

    url = "https://youtu.be/k5jYwyhDMxA?si=zwCaYPKKqrEjIrWk"

    # Step 1: Download
    downloaded_file = download_youtube_audio(url)
    print("Downloaded:", downloaded_file)

    # Step 2: Convert
    converted_file = convert_to_wav(downloaded_file)
    print("Converted:", converted_file)

    # Step 3: Split into chunks
    chunks = chunk_audio(converted_file, chunk_minutes=10)

    print("\nChunks Created:")
    for chunk in chunks:
        print(chunk)