## Video Subtitle Translator
This application uses speech recognition to automatically generate and embed Turkish subtitles into your videos.


## Features

- Extracts audio from video files
- Transcribes audio to text using Whisper Large V3 Turbo
- Translates the transcription to Turkish using LLaMA 3.3 70B
- Embeds translated subtitles into the original video
- Simple web interface for easy interaction

## Requirements

- Python 3.6+
- FFmpeg
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/johngunerli/video_whisperr.git
cd video_whisperr
```

2. Install required dependencies:
```bash
pip install gradio groq python-dotenv
```

3. Install FFmpeg if you don't have it already:
   - On Ubuntu: `sudo apt install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

4. Create a `.env` file in the project root and add your Groq API key:
```
GROQ_API_KEY=your-api-key-here
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Open the Gradio interface in your browser (typically at http://127.0.0.1:7860)

3. Upload a video file and the app will:
   - Extract the audio
   - Transcribe it using Whisper
   - Translate the transcription to Turkish
   - Embed the subtitles into the video
   - Return the video with embedded subtitles

## How It Works

The application uses:
- FFmpeg for audio extraction and subtitle embedding
- Groq's Whisper Large V3 Turbo model for speech-to-text transcription
- Groq's LLaMA 3.3 70B model for English to Turkish translation
- Gradio for the web interface

## File Description

- main.py - Main application code
- `.env` - Environment file for storing your Groq API key (not tracked by git)
- input_video.mov - Example input video file
- output_with_subtitles.mp4 - Example output video with subtitles
