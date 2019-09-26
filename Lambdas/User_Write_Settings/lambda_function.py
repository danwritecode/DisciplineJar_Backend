import boto3
import json
import calendar
import time

def lambda_handler(event, context):
    print(event)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')
    
    epochCurrent = calendar.timegm(time.gmtime())
    
    #Assign Variables for all values passed in by event
    User_Id = event['UserId']
    receiveMotivVid = event['Settings']['ReceiveMotivationalVideo']
    receiveWorkoutPlan = event['Settings']['ReceiveWorkoutPlan']
    personalizedMessage = event['Settings']['PersonalizedMessage']
    
    response = table.update_item(
        Key={'User_Id': User_Id},
        UpdateExpression='SET Modified_On = :time, Receive_MotivtnlVid_Bool = :receiveMotivVid, Receive_Workout_Bool = :receiveWorkoutPlan, Personal_Message_Tx = :personalizedMessage',
        ExpressionAttributeValues={
            ':time': epochCurrent,
            ':receiveMotivVid': receiveMotivVid,
            ':receiveWorkoutPlan': receiveWorkoutPlan,
            ':personalizedMessage': personalizedMessage
        }
    )
    
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!!!')
    }