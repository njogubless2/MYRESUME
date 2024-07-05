import json
import boto3

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='<YOUR_AWS_ACCESS_KEY_ID>',
    aws_secret_access_key='<YOUR_AWS_SECRET_ACCESS_KEY>',
    region_name='<YOUR_AWS_REGION>'
)

# Initialize DynamoDB resource
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('MyResume')

# Load the resume data from the JSON file
with open('resume_data.json') as json_file:
    resume_data = json.load(json_file)

# Insert the resume data into the DynamoDB table
table.put_item(Item=resume_data)

print('Resume data inserted successfully.')
