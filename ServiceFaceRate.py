#!flask/bin/python
import sys
import logging
import requests

from flask import Flask
from flask import jsonify
from flask import request

import string
import random
import base64

from SystemFaceRate import SystemFaceRate
from Persistency import Persistency

apiKey = ''
with open('apikey.txt', 'r') as file:
    apiKey = file.read()

if(apiKey == ''):
    print('must define api key in apikey.txt')
    exit()

app = Flask(__name__, static_folder='./html/')

@app.route('/facerate/1.0/health', methods=['get'])
def health():
    return jsonify(status='OK')

@app.route('/facerate/1.0/index', methods=['get'])
def index():
    return app.send_static_file('index.html')

#work with url
@app.route('/facerate/1.0/imageresultforurl', methods=['post'])
def imageresultforurl():
    jsonObject = request.get_json()
    #validate data
    isValid, responsePayload, statusCode =  validate(jsonObject, ['url'])
    if not isValid:
        return jsonify(responsePayload), statusCode

    url = jsonObject['url']

    imageResult = system.processUrl(url)
    return jsonify(imageResult)


# work with uploaded file (for phone....)
@app.route('/facerate/1.0/imageresultforimagebase64', methods=['post'])
def imageresultforimagebase64():
    jsonObject = request.get_json()
    #validate data
    isValid, responsePayload, statusCode =  validate(jsonObject, ['imagebase64'])
    if not isValid:
        return jsonify(responsePayload), statusCode

    imagebase64 = jsonObject['imagebase64']
    fileContent = base64.b64decode(imagebase64)
    randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(256))
    filePath = persistency.getImageFilePath(randomString)
    with open(filePath, 'wb') as file:
        file.write(fileContent)

    imageResult = system.processFilePath(filePath)
    
    return jsonify(imageResult)


def validate(jsonObject, requiredFieldList):
    if jsonObject == None:
        responsePayload = {'message':'no json payload'}
        return False, responsePayload, 400

    if not 'apikey' in jsonObject:
        responsePayload = {'message':'missing field: apikey'}
        return False, responsePayload, 400

    for requiredField in requiredFieldList:
        if not requiredField in jsonObject:
            responsePayload = {'message':'missing field: ' + requiredField}
            return False, responsePayload, 400

    if not(apiKey == jsonObject['apikey']):
        responsePayload = {'message':'apikey incorrect'}
        return False, responsePayload, 403

    return True, None, 200

rootDirPath = './persitency/'
if (1 < len(sys.argv)) :
    rootDirPath = sys.argv[1]
persistency = Persistency(rootDirPath)
system = SystemFaceRate(persistency)

if __name__ == '__main__':
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5004)
