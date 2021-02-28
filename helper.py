import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
import random
import time

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def upload_to_s3(file, bucket_name):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ContentType': file.content_type
            }
        )
    except Exception as e:
        print('Something Happened: ', e)
        return e

    return f'{S3_BUCKET}{file.filename}'

def start_transcribe(s3file):
    transcribe_client = boto3.client('transcribe')
    file_uri = f'https://reedtranscribetesting.s3.amazonaws.com/{s3file}'
    job_name = f'job{random.randint(1,10000)}'
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp4',
        LanguageCode='en-US',
        OutputBucketName='reedtranscriberesults',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 5
        }
    )
    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    

