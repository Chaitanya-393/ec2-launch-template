import boto3
import os
import tempfile
from PIL import Image

s3 = boto3.client('s3')

# Destination bucket name
DEST_BUCKET = 'destination-bucket-chaitanya'

def lambda_handler(event, context):
    try:
        # Get bucket and object key from event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        print(f"Processing file: {object_key} from bucket: {source_bucket}")

        # Download the image to a temporary file
        tmp_file = os.path.join(tempfile.gettempdir(), object_key)
        s3.download_file(source_bucket, object_key, tmp_file)

        # Open image using Pillow
        with Image.open(tmp_file) as img:
            print(f"Original image mode: {img.mode}")
            # Convert to grayscale for demo
            grayscale_image = img.convert("L")
            processed_file = os.path.join(tempfile.gettempdir(), f"gray-{object_key}")
            grayscale_image.save(processed_file)

        # Upload processed image to destination bucket
        s3.upload_file(processed_file, DEST_BUCKET, f"processed-{object_key}")
        print(f"Processed file uploaded to {DEST_BUCKET}/processed-{object_key}")

        return {
            'statusCode': 200,
            'body': f"Successfully processed {object_key}"
        }

    except Exception as e:
        print(f"Error: {e}")
        raise e
