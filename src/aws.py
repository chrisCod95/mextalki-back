import json
import os

import boto3

# Credentials
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Queues
SUBSCRIBE_MAILCHIMP_USER_QUEUE_URL = 'SUBSCRIBE_MAILCHIMP_USER_QUEUE_URL'
SEND_NOTIFICATION_EMAIL_QUEUE_URL = 'SEND_NOTIFICATION_EMAIL_QUEUE_URL'


def enqueue(env_queue_url, message_body):
    client = boto3.client(
        'sqs',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )
    queue_url = os.getenv(env_queue_url)

    return client.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(message_body),
    )
