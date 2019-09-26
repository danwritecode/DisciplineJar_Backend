import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print(event)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')
        
    try:
        User_Id = event['queryStringParameters']['User_Id']
        
        response = table.get_item(Key = {'User_Id':User_Id})
        item = response['Item']
        print(item)
        return { 'statusCode' : 200, 'headers': { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin' : '*' }, 'body' : json.dumps(item, indent=2, default=str) }
            
    except Exception as e:
        print(e)
    

        
    
    
