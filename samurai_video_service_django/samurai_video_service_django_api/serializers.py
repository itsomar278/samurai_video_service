from rest_framework import serializers
from .models import VideoTranslation


class VideoTranslationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=VideoTranslation.Status.choices)

    class Meta:
        model = VideoTranslation
        fields = [
            'request_id', 'user_id', 'start_minute', 'end_minute',
            'translated_transcription', 'video_url', 's3_file_url', 'status'
        ]
        read_only_fields = ['translated_transcription', 's3_file_url', 'status']

