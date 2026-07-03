# Video Assistant Agent

A simple AI-powered video assistant project for downloading, converting, transcribing, and summarizing audio from video sources.

## Project Structure

- `core/`
  - `extractor.py` - Builds language model chains for extracting action items, decisions, and questions from transcripts.
  - `summary.py` - Splits transcripts, summarizes chunks, combines summaries, and generates meeting titles.
  - `transcriber.py` - Uses OpenAI Whisper and Sarvam APIs for audio transcription and translation.
  - `vector_store.py` - Placeholder module for vector store logic (currently empty).
- `utils/`
  - `audio_processor.py` - Downloads audio from YouTube, converts audio files to WAV, and chunks audio for processing.
- `downloads/` - Default directory for downloaded audio files.
- `test.py` - Example script that loads environment variables, processes an input source, and transcribes audio.

## Requirements

The project depends on the following packages:

- `openai-whisper`
- `yt-dlp`
- `pydub`
- `ffmpeg-python`
- `deep-translator`
- `langchain`
- `langchain-community`
- `langchain-mistralai`
- `mistralai`
- `chromadb`
- `sentence-transformers`
- `huggingface-hub`
- `streamlit`
- `fpdf2`
- `reportlab`
- `python-dotenv`
- `requests`
- `numpy`
- `torch`
- `torchaudio`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Create a `.env` file in the repo root and set the required API keys:

```bash
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
WHISPER_MODEL=small
```

2. Run `test.py` to download, convert, chunk, and transcribe a sample video source:

```bash
python test.py
```

3. Use the functions in `utils/audio_processor.py` and `core/transcriber.py` to integrate video/audio processing with transcription and summarization.

## Notes

- `core/vector_store.py` is currently empty and can be extended with retrieval-augmented generation (RAG) or similarity search logic.
- `core/transcriber.py` supports local Whisper transcription and Sarvam translation/transcription for Hinglish audio.
- `core/summary.py` is designed to summarize long transcripts by splitting them into chunks and combining partial summaries.
