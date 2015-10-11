__author__ = 'alliemeng'

from flask import Flask, request
import json
import boto3

app = Flask(__name__)
snsresource = boto3.resource('sns', region_name='us-east-1')
snsclient = boto3.client('sns', region_name='us-east-1')

#dict for tokens/arns
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
@app.route('/', methods=['GET', 'POST'])
def hey():
    return "HI"

@app.route('/add', methods=['GET', 'POST'])
def addstuffs():
    addentries=request.get_json(force=True)
    for token in addentries:
        addtotable(token)
    return "done add!"

@app.route('/send', methods=['GET', 'POST'])
def sendstuffs():
    sendentries=request.get_json(force=True)
    for token in sendentries:
        addtotable(token["token"])
        sendtotable(token)
    return "done send!"

if __name__ == '__main__':
    app.run()
    '''
    ta = ['6e6aad5a e119d3d4 74ff474a 4b280c84 45398261 bf0e6a29 6c2b43a8 0778f729',
                 '6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1']
    ts = [{'token':'6e6aad5a e119d3d4 74ff474a 4b280c84 45398261 bf0e6a29 6c2b43a8 0778f729', 'message':'THIS SHIT WORKS'},
                {'token': '6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1','message':'THIS SHIT WORKS'}]
    #intake(ta)
    intake(ts)
    '''
    #curl -X POST --data '[{"token":"798c038792891ae421d8987f8c3d3d354566785648655dd09599237c0eafa7e7","message":"Hi, how can I help?"}]' http://localhost:5000/send

    #curl -H "Content-Type: application/json" -X POST -d '[{"token":"6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1","message":"YOU ARE DUMBBB"}]' ec2-52-88-2-41.us-west-2.compute.amazonaws.com/send
    #curl -X POST --data '[{"token":"6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1","message":"I'm the angel twin"}, {"token":"6e6aad5ae119d3d474ff474a4b280c8445398261bf0e6a296c2b43a80778f729", "message": "I'm the angel twin"}]' http://localhost:5000/send
    #curl -X POST --data '[{"token":"6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1","message":"Hi, how can I help?"}]' http://localhost:5000/send
    #curl -X POST --data '[{"token":"6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1","message":"I'm the angel twin"}]' http://localhost:5000/send
    #curl -X POST --data '["6fc41ab30bf0e7e66995bb3962f134f5945e55ac9e5a07f41fde14049bee2ff1"]' http://localhost:5000/add
    #curl -X POST --data '["6e6aad5ae119d3d474ff474a4b280c8445398261bf0e6a296c2b43a80778f729"]' http://localhost:5000/add