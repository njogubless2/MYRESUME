import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# Define the table creation parameters
table_name = 'MyResume'
params = {
    'TableName': table_name,
    'KeySchema': [
        {'AttributeName': 'ID', 'KeyType': 'HASH'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'ID', 'AttributeType': 'S'}
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
}

# Create the table
try:
    table = dynamodb.create_table(**params)
    print(f'Table {table_name} created successfully')
except Exception as e:
    print(f'Error creating table: {e}')
