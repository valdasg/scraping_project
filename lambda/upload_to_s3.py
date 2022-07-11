# from cv_bankas_parse import cv_bankas_parse
import boto3, os

def get_client():
    return boto3.client('s3')

def upload_to_s3(body, bucket, key ):
    s3_client = get_client()
    return s3_client.put_object(Body = body, Bucket=bucket, Key=key)