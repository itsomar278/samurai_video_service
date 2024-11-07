import yt_dlp
import subprocess
import os
import uuid

TEMP_DOWNLOADS_PATH = "./temp_downloads"

def download_audio(youtube_url, start_time="00:00", end_time="01:00"):
    """Download and trim audio from a YouTube video, saving it with a unique file name."""
    os.makedirs(TEMP_DOWNLOADS_PATH, exist_ok=True)

    unique_filename = str(uuid.uuid4())
    output_path = os.path.join(TEMP_DOWNLOADS_PATH, unique_filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'postprocessor_args': [
            '-ar', '16000'
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

    downloaded_file_path = output_path + ".wav"
    trimmed_path = os.path.join(TEMP_DOWNLOADS_PATH, f"trimmed_{unique_filename}.wav")

    try:
        subprocess.run([
            'ffmpeg', '-i', downloaded_file_path,
            '-ss', start_time, '-to', end_time,
            '-c', 'copy', trimmed_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error trimming audio: {e}")
        return None

    os.remove(downloaded_file_path)

    return trimmed_path
