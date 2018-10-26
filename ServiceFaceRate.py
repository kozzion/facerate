#!flask/bin/python
import sys
import logging
import requests

from flask import Flask
from flask import jsonify
from flask import request

import string
import random

from SystemFaceRate import SystemFaceRate
from Persistency import Persistency


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
    if jsonObject == None:
        return jsonify('no json payload'), 500
    if not 'url' in jsonObject:
        return jsonify('missing: url'), 500

    url = jsonObject['url']

    imageResult = system.processUrl(url)
    return jsonify(imageResult)

# work with uploaded file (for phone....)
@app.route('/facerate/1.0/imageresultforimagefile', methods=['post'])
def imageresultforimagefile():
    if not 'imageFile' in request.files:
        return jsonify('no file payload: imageFile'), 500

    imageFile = request.files['imageFile']
    randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(256))
    filePath = persistency.getImageFilePath(randomString)
    imageFile.save(filePath)

    imageResult = system.processFilePath(filePath)
    return jsonify(imageResult)

rootDirPath = './persitency/'
if (1 < len(sys.argv)) :
    rootDirPath = sys.argv[1]
persistency = Persistency(rootDirPath)
system = SystemFaceRate(persistency)

if __name__ == '__main__':
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)
