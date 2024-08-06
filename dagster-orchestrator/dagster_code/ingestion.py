
import os
from dagster import asset, define_asset_job, AssetSelection ,op,job # import the `dagster` library
import json
import requests
import time
import boto3
import io






@op
def fetch_and_write_data_to_s3_bucket(context):


        url = os.getenv('API_URL')
        bucket_name = os.getenv('AWS_S3_BUCKET')
        object_name = f"{os.getenv('INPUT_S3_PATH')}/timestamp_{time.time()}.json"

        s3_client = boto3.client('s3',
                                 aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        )

        response = requests.get(url)
        json_data = response.json()

        # Use an in-memory file-like object
        json_buffer = io.BytesIO()
        json_bytes = json.dumps(json_data).encode('utf-8')
        json_buffer.write(json_bytes)
        json_buffer.seek(0)

        # Upload the in-memory file to S3
        s3_client.upload_fileobj(json_buffer, bucket_name, object_name)

        context.log.info(f"Object '{object_name}' uploaded successfully to bucket '{bucket_name}'")


@job
def  near_real_time_data_ingestion():
    fetch_and_write_data_to_s3_bucket()