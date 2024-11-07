from abc import ABC

from rest_framework import serializers
from .models import VideoTranslation


class VideoTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTranslation
        fields = ['user_id', 'start_minute', 'end_minute', 'translated_transcription', 'video_url', 's3_file_url']
        read_only_fields = ['translated_transcription', 's3_file_url']


class VideoTranslationCreateDTO(serializers.Serializer):
    user_id = serializers.IntegerField()
    start_minute = serializers.IntegerField()
    end_minute = serializers.IntegerField()
    video_url = serializers.URLField()

