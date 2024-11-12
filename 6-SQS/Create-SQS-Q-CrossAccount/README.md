# Creating a Queue Using Cross-Account Permissions

SQS does not allow API calls such as [`CreateQueue`](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html) using [cross-account permissions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-authentication-and-access-control.html#access-control). A workaround is to create and invoke a Lambda function in another account, in order to call that API.)

## Create AWS CLI profiles

Development account admin

```sh
aws configure --profile devadmin
```

Production account admin

```sh
aws configure --profile prodadmin
```

## Create Lambda function in production account

Function name: `CreateSQSQueueCrossAcct`

See [`lambda_function.py`](lambda_function.py) and assign role [`lambda_execution_role.json`](lambda_execution_role.json).

## Assign permissions to Lambda function

Add permissions to the production Lambda function allowing it to be invoked by the development account user:

```sh
aws lambda add-permission \
--function-name CreateSQSQueueCrossAcct \
--statement-id DevAccountAccessToSQSQCreate \
--action 'lambda:InvokeFunction' \
--principal 'arn:aws:iam::797064975082:user/icloudxl-dev' \
--region us-west-2 \
--profile icloudxl-prod
```

To view the policy:

```sh
aws lambda get-policy \
--function-name CreateSQSQueueCrossAcct \
--region us-west-2 \
--profile icloudxl-prod
```

To remove the policy:

```sh
aws lambda remove-permission \
--function-name CreateSQSQueueCrossAcct \
--statement-id DevAccountAccessToSQSQCreate \
--region us-west-2 \
--profile icloudxl-prod
```

## Invoke the production(icloudxl-prod) Lambda function from the development account (icloudxl-dev)

```sh
aws lambda invoke \
--function-name '__LAMBDA_FUNCTION_ARN__' \
--payload '{"QueueName": "MyProdQueue" }' \
--invocation-type RequestResponse \
--profile icloudxl-dev \
--region us-west-2 \
output.txt
```