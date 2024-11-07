import boto3
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class S3Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    def upload_transcription(self, transcription_text):
        try:
            file_name = f"{uuid.uuid4()}.txt"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=transcription_text,
                ContentType='text/plain'
            )
            s3_file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            return s3_file_url
        except Exception as e:
            raise Exception(f"Failed to upload transcription to S3: {str(e)}")
