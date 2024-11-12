import boto3
dynamodb=boto3.resource('dynamodb')
def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        
    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

if __name__ == '__main__':
    movie_table=create_movie_table()
    print("Table Status:", movie_table.table_status)

print('Table status:', movie_table.table_status)
print('Waiting for', movie_table.name, 'to complete creating...')
movie_table.meta.client.get_waiter('table_exists').wait(TableName='Movies')
print('Table status:', dynamodb.Table('Movies').table_status)
