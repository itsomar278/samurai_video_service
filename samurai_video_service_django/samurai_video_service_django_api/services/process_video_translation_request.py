import json
from ..models import VideoTranslation
from ..utils.download_audio import download_audio
from ..utils.transcribe_translate import transcribe_or_translate
from ..utils.S3uploader import S3Uploader
import os


def process_video_translation_request(ch, method, properties, body):
    data = json.loads(body)

    video_translation, created = VideoTranslation.objects.get_or_create(
        request_id=data['request_id'],
        defaults={
            'user_id': data['user_id'],
            'start_minute': data['start_minute'],
            'end_minute': data['end_minute'],
            'video_url': data['video_url'],
            'status': VideoTranslation.Status.RECEIVED
        }
    )

    try:
        video_translation.status = VideoTranslation.Status.IN_PROGRESS
        video_translation.save()

        start_time = decimal_to_hhmmss(data['start_minute'])
        end_time = decimal_to_hhmmss(data['end_minute'])

        audio_file_path = download_audio(data['video_url'], start_time, end_time)
        if not audio_file_path:
            raise ValueError("Failed to download or trim audio.")

        transcription_text, output_type = transcribe_or_translate(audio_file_path)
        os.remove(audio_file_path)

        s3_uploader = S3Uploader()
        s3_file_url = s3_uploader.upload_transcription(transcription_text)

        video_translation.translated_transcription = transcription_text
        video_translation.s3_file_url = s3_file_url
        video_translation.status = VideoTranslation.Status.READY
        video_translation.save()

    except Exception as e:
        video_translation.status = VideoTranslation.Status.ERROR_OCCURRED
        video_translation.save()
        print(f"Error processing video translation request: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def decimal_to_hhmmss(decimal_minutes):
    total_seconds = int(decimal_minutes * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
