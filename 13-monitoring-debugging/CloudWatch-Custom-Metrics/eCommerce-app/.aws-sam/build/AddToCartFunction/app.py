import json
import random

import boto3

cloudwatch = boto3.client('cloudwatch')


def lambda_handler(event, context):

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'ItemsAddedToCart',
                'Value': random.randint(1, 20)
            },
        ],
        Namespace='eCommerceApp'
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {"itemID": "944342"},
                {"itemID": "223604"},
                {"itemID": "809113"}
            ]
        ),
    }
