import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')
destination_bucket = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    # Get object from source bucket
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    if not key.lower().endswith(".jpg") and not key.lower().endswith(".jpeg"):
        print("Only JPEG files are processed.")
        return
    
    response = s3.get_object(Bucket=source_bucket, Key=key)
    image_content = response['Body'].read()
    
    # Open image with Pillow
    image = Image.open(io.BytesIO(image_content))
    
    # Resize image
    image = image.resize((128, 128))
    
    # Save to buffer
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    
    # Upload to destination bucket
    s3.put_object(Bucket=destination_bucket, Key=key, Body=buffer, ContentType='image/jpeg')
    
    print(f"Processed and uploaded {key} to {destination_bucket}")
