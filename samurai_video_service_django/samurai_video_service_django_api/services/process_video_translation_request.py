import json
import traceback

from ..models import VideoTranslation, Status
from ..utils.download_audio import download_audio
from ..utils.rabbitmq_producer import publish_to_queue
from ..utils.transcribe_translate import transcribe_or_translate
from ..utils.S3uploader import S3Uploader
import os


def process_video_translation_request(ch, method, properties, body):
    """
    consume message , publish message and process in between .
    """
    data = json.loads(body)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    video_translation, created = VideoTranslation.objects.get_or_create(
        request_id=data['request_id'],
        defaults={
            'user_id': data['user_id'],
            'start_minute': data['start_minute'],
            'end_minute': data['end_minute'],
            'video_url': data['video_url'],
            'status': Status.RECEIVED
        }
    )

    try:
        video_translation.status = Status.IN_PROGRESS
        video_translation.save()

        start_time = decimal_to_hhmmss(data['start_minute'])
        end_time = decimal_to_hhmmss(data['end_minute'])

        audio_file_path = download_audio(data['video_url'], start_time, end_time)
        if not audio_file_path:
            video_translation.status = Status.ERROR_OCCURRED
            raise ValueError("Failed to process , try again LOL.")

        transcription_text, output_type = transcribe_or_translate(audio_file_path)
        os.remove(audio_file_path)

        try:
            s3_uploader = S3Uploader()
            s3_file_url = s3_uploader.upload_transcription(transcription_text)
        except Exception as e:
            video_translation.status = Status.ERROR_OCCURRED
            raise ValueError(f"a failure happened from our cloud provider side , try again LOL")

        video_translation.translated_transcription = transcription_text
        video_translation.s3_file_url = s3_file_url
        video_translation.status = Status.READY
        video_translation.save()

        message = {
            "request_id": str(video_translation.request_id),
            "user_id": video_translation.user_id,
            "s3_file_url": video_translation.s3_file_url,
            "transcription_text": video_translation.translated_transcription,
            "status": video_translation.status.name
        }

        if not publish_to_queue(queue_name='ready_for_vectorization', message=message) :
            video_translation.status = Status.ERROR_OCCURRED
            video_translation.save()
            raise ValueError(f"a failure happened from my side i admit it , try again LOL")

        video_translation.status = Status.DELIVERED
        video_translation.save()

    except Exception as e:
        video_translation.status = Status.ERROR_OCCURRED
        video_translation.save()
        print(f"Error processing video translation request: {e}")
        traceback.print_exc()


def decimal_to_hhmmss(decimal_minutes):
    """
    convert decimal minute to hh:mm:ss format so i use with ffmpeg ( some weird ass audio shit that i hate but it's useful )  .
    """
    total_seconds = int(decimal_minutes * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
