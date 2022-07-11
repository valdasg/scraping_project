import boto3, urllib
from pretify_json import pretify_json
from upload_to_s3 import upload_to_s3

def lambda_handler(event, context):
    s3Client = boto3.client('s3')
    bucket = 'talent-lab'
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # # Process it
    body = pretify_json(bucket, key)
    
    #upload to s3://transformed/
    file = f'transformed/{key[4:]}'
    upload_to_s3(body, bucket, file)
    
    
