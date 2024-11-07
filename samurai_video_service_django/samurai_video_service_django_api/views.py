from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoTranslation
from .serializers import VideoTranslationSerializer, VideoTranslationCreateDTO
from .download_audio import download_audio
from .transcribe_translate import transcribe_or_translate
from .utils.S3uploader import S3Uploader
import os

class VideoTranslationCreateView(APIView):
    def post(self, request):
        dto_serializer = VideoTranslationCreateDTO(data=request.data)
        if dto_serializer.is_valid():
            user_id = dto_serializer.validated_data['user_id']
            start_minute = dto_serializer.validated_data['start_minute']
            end_minute = dto_serializer.validated_data['end_minute']
            video_url = dto_serializer.validated_data['video_url']

            start_time = f"{int(start_minute // 60):02}:{int(start_minute % 60):02}:00"
            end_time = f"{int(end_minute // 60):02}:{int(end_minute % 60):02}:00"

            audio_file_path = download_audio(video_url, start_time, end_time)

            if not audio_file_path:
                return Response({"error": "Failed to download or trim audio"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            transcription_text, output_type = transcribe_or_translate(audio_file_path)

            os.remove(audio_file_path)

            try:
                s3_uploader = S3Uploader()
                s3_file_url = s3_uploader.upload_transcription(transcription_text)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            video_translation = VideoTranslation.objects.create(
                user_id=user_id,
                start_minute=start_minute,
                end_minute=end_minute,
                video_url=video_url,
                translated_transcription=transcription_text,
                s3_file_url=s3_file_url
            )

            response_serializer = VideoTranslationSerializer(video_translation)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(dto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
