from twilio.rest import Client
import random
import boto3 
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    users = getUsers()
    print('Users Collected: {}'.format(users))
    cookie = getCookie()
    print('Cookie found: {}'.format(cookie))

    for user in users:
        phoneNum = user['Phone_Num']

        # Not all users have a personal message so we have to check if it exists before trying to parse it.
        try:
            personalMessage = user['Personal_Message_Tx']
            print('Personal Message: {}'.format(personalMessage))
            print('Sending to Number: {}'.format(phoneNum))

            try:
                sendSMS(phoneNum, cookie, personalMessage=personalMessage)
            except Exception as e:
                print(e)
                pass # doing nothing on exception
        except:
            print('Sending to Number: {}'.format(phoneNum))

            try:
                sendSMS(phoneNum, cookie)
            except Exception as e:
                print(e)
                pass # doing nothing on exception
            
        

def getUsers():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')

    try:
        response = table.scan()
        items = response['Items']
        
        return(items)
            
    except Exception as e:
        print(e)

def getCookie():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DisciplineJar')

    try:
        response = table.scan()
        items = response['Items']
            
    except Exception as e:
        print(e)
    
    numCookies = len(items)-1
    cookieNum = random.randint(0,numCookies)

    cookie = items[cookieNum]

    return(cookie['Cookie_Tx'])


def sendSMS(phoneNum, cookieTx, *args, **kwargs):
    print('Kwargs: {}'.format(kwargs))
    personalMessage = kwargs.get('personalMessage', None)
    print(personalMessage)

    if(personalMessage == None):
        smsText = 'Here is your daily cookie from the Discipline Jar. Submit your own cookie at https://disciplinejar.io. \n \n{}'.format(cookieTx)
    else:
        smsText = 'Here is your daily cookie from the Discipline Jar. Submit your own cookie at https://disciplinejar.io. \n \n{} \n \n{}'.format(cookieTx, personalMessage)        

    account_sid = ''
    auth_token = ''
    fromSid = ''
    
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body= smsText,
                        from_= fromSid,
                        to='+12154507196'
                    )

    print(message.sid)