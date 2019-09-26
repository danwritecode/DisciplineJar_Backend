import json
import boto3
import datetime
import calendar
import time

def lambda_handler(event, context):
    print(event)
    """
    The exepcted input from Event looks like the below: 
        {
            'version': '1',
            'region': 'us-east-2',
            'userPoolId': 'us-east-2_MYl8RjcVh',
            'userName': 'nelsynelz2',
            'callerContext': {
                'awsSdkVersion': 'aws-sdk-unknown-unknown',
                'clientId': '5gohu17a9hrp6t6ueqkkeame1m'
            },
            'triggerSource': 'PostConfirmation_ConfirmSignUp',
            'request': {
                'userAttributes': {
                    'sub': '4ef24f6c-59f3-4923-b760-e95df1d07dfd',
                    'cognito:user_status': 'CONFIRMED',
                    'email_verified': 'true',
                    'phone_number_verified': 'false',
                    'phone_number': '+12154507196',
                    'email': 'dnelson4993@gmail.com'
                }
            },
            'response': {}
        }
    
    This function takes that input and extracts the "sub" attribute which is then written to the DynamoDB Users Table along with other important attributes.
    """
    #Extract key User Data points from Event object and assign to variables
    UserId = event['request']['userAttributes']['sub']
    UserName = event['userName']
    Email_Tx = event['request']['userAttributes']['email']
    PhoneNumber_Tx = event['request']['userAttributes']['phone_number']
    
    #create timestamp in EPOCH
    epochCurrent = calendar.timegm(time.gmtime())
    
    #create user Dict that will be passed to DynamoDB
    user = {}
    
    user["User_Id"] = UserId
    user["User_Nm"] = UserName

    user["Email_Tx"] = Email_Tx
    user["PhoneNumber_Tx"] = PhoneNumber_Tx
    user["CreatedOn_Dt"] = epochCurrent
    
    print("Writing to Dynamo, here is the Object that is being written: {}".format(user))
    dynamoResponse = writeToDynamo(user)
    print("Wrote to Dynamo, here is the response: {}".format(dynamoResponse))
    
    return(event)


def writeToDynamo(user):
    """
    This function receives the below Dict object from the handler lambda function and posts this object to DynamoDB using the Put_Item method in boto3.
    
        {
            'User_Id': '55042c68-85bc-4943-899d-3051b46fd032', 
            'User_Nm': 'adellaragione', 
            'Email_Tx': 'dnelson4993@gmail.com', 
            'CreatedOn_Dt': 1560972185
        }
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')

    try:
        #write to dynamo
        dynamoResponse = table.put_item(Item=user)
        return(dynamoResponse)

    except Exception as e:
        return(e)