import json
import boto3
import datetime
import calendar
import time
import uuid

def lambda_handler(event, context):
    print(event)

    PhoneNumber_Tx = event['phone_number']
    
    #create timestamp in EPOCH
    epochCurrent = calendar.timegm(time.gmtime())
    
    #create user Dict that will be passed to DynamoDB
    user = {}
    user["Phone_Num"] = PhoneNumber_Tx
    user["CreatedOn_Dt"] = epochCurrent
    
    print("Writing to Dynamo, here is the Object that is being written: {}".format(user))
    dynamoResponse = writeToDynamo(user)
    print("Wrote to Dynamo, here is the response: {}".format(dynamoResponse))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


def writeToDynamo(user):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')

    try:
        #write to dynamo
        dynamoResponse = table.put_item(Item=user)
        return(dynamoResponse)

    except Exception as e:
        return(e)