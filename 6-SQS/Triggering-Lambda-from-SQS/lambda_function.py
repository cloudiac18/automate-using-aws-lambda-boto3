import json
import os
from datetime import datetime

import boto3

QUEUE_NAME = os.environ['QUEUE_NAME']
MAX_QUEUE_MESSAGES = os.environ['MAX_QUEUE_MESSAGES']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

sqs = boto3.client('sqs',region_name="us-west-2")
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print(event)
    # Receive messages from SQS queue
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=int(MAX_QUEUE_MESSAGES),
        WaitTimeSeconds=10,
    )
    print(f"Number of messages received: {len(response.get('Messages', []))}")
    
    for message in response.get('Messages', []):
        # Write message to DynamoDB
        print(message)
        receipt_handle = message['ReceiptHandle']
        table = dynamodb.Table(DYNAMODB_TABLE)
        dynamo_response = table.put_item(
            Item={
                'MessageId': message["MessageId"],
                'Body': message["Body"],
                'Timestamp': datetime.now().isoformat()
            }
        )
        print("Wrote message to DynamoDB:", json.dumps(dynamo_response))
        response=delete_queue_message(queue_url,receipt_handle)
        print('Queue Message delete response...: ',response)

def delete_queue_message(queue_url, receipt_handle):
    """
    Deletes the specified message from the specified queue.
    """
    try:
        response = sqs.delete_message(QueueUrl=queue_url,
                                             ReceiptHandle=receipt_handle)
    except ClientError:
        logger.exception(
            f'Could not delete the meessage from the - {queue_url}.')
        raise
    else:
        return response