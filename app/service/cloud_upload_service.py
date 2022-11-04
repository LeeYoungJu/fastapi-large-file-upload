import boto3

from app.config.setting import settings


class CloudUploadService:

    def __init__(self):
        self.s3_client = boto3.client('s3',
                                      endpoint_url=settings.AWS_ENDPOINT_URL,
                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    def upload(self, file_path: str, bucket: str, object_name: str):
        self.s3_client.upload_file(file_path, bucket, object_name)

