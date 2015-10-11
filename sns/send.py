import json
import boto3

snsresource = boto3.resource('sns', region_name='us-east-1')
snsclient = boto3.client('sns', region_name='us-east-1')

tokensandarns = {}


def addtotable(token):
    platform_endpoint=snsclient.create_platform_endpoint(
        PlatformApplicationArn='arn:aws:sns:us-east-1:678216564308:app/APNS_SANDBOX/Modern',
        Token=token
    )
    tokensandarns[token]=platform_endpoint['EndpointArn']

def sendtotable(token):
    arn=tokensandarns[token['token']]
    platform_endpoint = snsresource.PlatformEndpoint(arn)
    platform_endpoint.publish(
        Message=token['message']
    )
