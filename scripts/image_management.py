#!/bin/python

import os

import boto3
from botocore.exceptions import NoCredentialsError
import requests

from pathlib import Path


def get_image_path(image_id: str) -> Path:
    """
    Get the path to an image file

    :param image_id: ID of the image
    :return: Path to the image file
    """
    return Path(f'../web/images/{image_id}.png')


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name[7:]

    # Upload the file
    s3_client = boto3.client(
        's3', 
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID_S3"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY_S3")
    )
                             
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True



def download_image(url, file_path):
    """
    Download an image from a URL and save it to a file

    :param url: URL of the image to download
    :param file_path: Path to save the downloaded image
    :return: True if the image was downloaded and saved successfully, else False
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False

