import os
import subprocess
import gradio as gr
from datetime import timedelta
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def extract_audio(video_path, audio_path):
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
    )
    return audio_path


def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    return f"{td.seconds // 3600:02}:{(td.seconds // 60) % 60:02}:{td.seconds % 60:02},{int(td.microseconds / 1000):03}"


def generate_subtitles(audio_file, srt_file):
    client = Groq()
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_file, file.read()),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )
    original_text = transcription.text

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Translate the following text to Turkish:"},
            {"role": "user", "content": original_text},
        ],
        temperature=1,
        top_p=1,
        stream=False,
        stop=None,
    )
    translated_text = completion.choices[0].message.content

    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription.segments):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            f.write(f"{i+1}\n{start} --> {end}\n{translated_text}\n\n")
    return srt_file


def embed_subtitles(video_file, srt_file, output_video):
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_file,
            "-vf",
            f"subtitles={srt_file}:force_style='FontSize=12,PrimaryColour=&HFFFFFF&'",
            "-c",
            "libx264",
            "-c:a",
            "aac",
            "-strict",
            "-2",
            output_video,
            "-y",
        ]
    )
    return output_video


def process_video(video_file):
    # Ensure we get a file path, whether video_file is a file object or a string
    input_video_path = video_file if isinstance(video_file, str) else video_file.name
    output_video = "output_with_subtitles.mp4"
    audio_file = "extracted_audio.m4a"
    srt_file = "subtitles.srt"

    extract_audio(input_video_path, audio_file)
    generate_subtitles(audio_file, srt_file)
    final_video = embed_subtitles(input_video_path, srt_file, output_video)

    os.remove(audio_file)
    os.remove(srt_file)

    return final_video


gr.Interface(
    fn=process_video,
    inputs=gr.Video(),
    outputs=gr.Video(),
    title="Video Subtitle Translator",
    description="Upload a video file, and it will generate and embed Turkish subtitles.",
).launch()
