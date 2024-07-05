import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyResume')

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        user_id = event['pathParameters']['id']
        response = table.get_item(Key={'ID': user_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

    elif event['httpMethod'] == 'POST':
        item = json.loads(event['body'])
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Resume created'})
        }

    elif event['httpMethod'] == 'PUT':
        user_id = event['pathParameters']['id']
        item = json.loads(event['body'])
        table.update_item(
            Key={'ID': user_id},
            UpdateExpression="set info=:i",
            ExpressionAttributeValues={':i': item['info']},
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Resume updated'})
        }

    elif event['httpMethod'] == 'DELETE':
        user_id = event['pathParameters']['id']
        table.delete_item(Key={'ID': user_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Resume deleted'})
        }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method not allowed'})
        }
