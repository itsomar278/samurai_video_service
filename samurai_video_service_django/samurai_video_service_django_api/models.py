from django.db import models

class VideoTranslation(models.Model):
    user_id = models.IntegerField()
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    translated_transcription = models.TextField(blank=True, null=True)
    video_url = models.URLField()
    s3_file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Translation for video at {self.video_url} from {self.start_minute} to {self.end_minute} by user {self.user_id}"
