import boto3

class S3Context:
    def __init__(self, access_key, secret_key, region, logger):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.logger = logger
        self.logger.log("Initialized S3Context.")
        
    def upload_files(self, bucket_name, file_path, object_name=None):
        if object_name is None:
            object_name = file_path
        try:
            self.s3.upload_file(file_path, bucket_name, object_name)
            self.logger.log(f"Uploaded {file_path} to {bucket_name}/{object_name}")
        except Exception as e:
            self.logger.log(f"Failed to upload {file_path} to {bucket_name}/{object_name}: {e}")
            
    def download_files(self, bucket_name, object_name, file_path):
        try:
            self.s3.download_file(bucket_name, object_name, file_path)
            self.logger.log(f"Downloaded {object_name} from {bucket_name} to {file_path}")
        except Exception as e:
            self.logger.log(f"Failed to download {object_name} from {bucket_name}: {e}")