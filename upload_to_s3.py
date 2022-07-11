from cv_bankas_parser import cv_bankas_parser
from cv_market_parser import cv_market_parser
from cv_online_parser import cv_online_parser
import boto3, os

sites = ['bankas', 'online', 'market']

def upload_to_s3():
    
    def get_client():
        os.environ.setdefault('AWS_DEFAULT', 'valdas')
        return boto3.client('s3')

    def upload_to_s3(body, bucket, file):
        s3_client = get_client()
        return s3_client.put_object(Bucket=bucket, Key=file, Body=body)    

    for site in sites:  
        file = f'raw/cv_{site}.json'
        # evaluates string to function name
        parse_res = eval(f'cv_{site}_parser()')
        bucket = 'talent-lab'
        upload_to_s3(parse_res, bucket, file)

if __name__ == "__main__":
    upload_to_s3()