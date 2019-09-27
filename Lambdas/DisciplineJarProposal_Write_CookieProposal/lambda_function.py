import json
import boto3
import datetime
import calendar
import time
import uuid

def lambda_handler(event, context):
    print(event)

    cookieProposal = event
    #create timestamp in EPOCH
    epochCurrent = calendar.timegm(time.gmtime())

    cookieProposal['Proposal_Id'] = str(uuid.uuid4())
    cookieProposal['CreatedOn_Dt'] = epochCurrent
    
    
    print("Writing to Dynamo, here is the Object that is being written: {}".format(cookieProposal))
    dynamoResponse = writeToDynamo(cookieProposal)
    print("Wrote to Dynamo, here is the response: {}".format(dynamoResponse))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


def writeToDynamo(cookieProposal):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DisciplineJar_Proposals')

    try:
        #write to dynamo
        dynamoResponse = table.put_item(Item=cookieProposal)
        return(dynamoResponse)

    except Exception as e:
        return(e)