import uuid

from django.db import models


class Status(models.IntegerChoices):
    RECEIVED = 0, 'Received'
    ERROR_OCCURRED = 1, 'Error Occurred'
    IN_PROGRESS = 2, 'In Progress'
    READY = 3, 'Ready'
    DELIVERED = 4, 'Delivered'


class VideoTranslation(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user_id = models.FloatField()
    start_minute = models.FloatField()
    end_minute = models.FloatField()
    translated_transcription = models.TextField(blank=True, null=True)
    video_url = models.URLField()
    s3_file_url = models.URLField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.RECEIVED)

    def __str__(self):
        return f"Translation for video at {self.video_url} from {self.start_minute} to {self.end_minute} by user {self.user_id}"

