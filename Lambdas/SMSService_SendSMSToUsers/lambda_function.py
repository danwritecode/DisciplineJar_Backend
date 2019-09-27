import nexmo
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


def sendSMS(phoneNum, cookieTx):
    client = nexmo.Client(key='', secret='')
    smsText = 'Here is your daily cookie from the Discipline Jar. Submit your own cookie at https://disciplinejar.io. \n \n{}'.format(cookieTx)
    response = client.send_message({
        'from': '19283273015',
        'to': phoneNum,
        'text': smsText,
    })
    print(response)