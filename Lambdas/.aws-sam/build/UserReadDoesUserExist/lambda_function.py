import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print(event)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')
        
    try:
        phoneNum = event['queryStringParameters']['phoneNum']
        phoneNumFormatted = '+' + phoneNum[1:]
        print('Phone Number is: {}'.format(phoneNumFormatted))
        
        response = table.get_item(Key = {'Phone_Num':phoneNumFormatted})
        print(response)
        try:
            item = response['Item']
            print(item)
            return { 'statusCode' : 200, 
                    'headers': { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin' : '*' }, 
                    'body' : True }
        except:
            return { 'statusCode' : 200, 
                    'headers': { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin' : '*' }, 
                    'body' : False }

        
            
    except Exception as e:
        print(e)