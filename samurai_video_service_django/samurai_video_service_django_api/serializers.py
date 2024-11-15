from rest_framework import serializers
from .models import VideoTranslation

class VideoTranslationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=VideoTranslation.Status.choices)

    class Meta:
        model = VideoTranslation
        fields = [
            'user_id', 'start_minute', 'end_minute', 'translated_transcription',
            'video_url', 's3_file_url', 'status'
        ]
        read_only_fields = ['translated_transcription', 's3_file_url', 'status']

class VideoTranslationCreateDTO(serializers.Serializer):
    user_id = serializers.IntegerField()
    start_minute = serializers.FloatField(min_value=0.0)
    end_minute = serializers.FloatField(min_value=0.0)
    video_url = serializers.URLField()
    status = serializers.ChoiceField(choices=VideoTranslation.Status.choices, required=False)
