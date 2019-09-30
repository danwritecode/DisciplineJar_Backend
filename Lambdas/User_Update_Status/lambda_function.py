import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')

    primaryKey = event['PhoneNum']
    status = event['Active']

    try:
        dynamoResponse = table.update_item(
                Key={'Phone_Num': primaryKey},
                UpdateExpression='SET Active = :Status',
                ExpressionAttributeValues={
                    ':Status': status,
                }
            )
        
        print(dynamoResponse)

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully updated status.')
        }

    except Exception as e:
        print(e)
        return(e)
        


