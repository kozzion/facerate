import uuid
import itertools
import os
import face_recognition
import requests

from Persistency import Persistency
from ModelFaceLinear import ModelFaceLinear


class SystemFaceRate(object):
    """docstring for SystemFaceRate."""
    def __init__(self, persistency):
        super(SystemFaceRate, self).__init__()
        self.ratingModel = ModelFaceLinear()
        self.persistency = persistency
        X,Y = self.persistency.loadDataSet('meanrating')
        self.ratingModel.fit(X,Y)

    def downloadImage(self, url):
        filePath = self.persistency.getImageFilePath(url)
        response = requests.get(url, allow_redirects=True)
        with open(filePath, 'wb') as file:
            file.write(response.content)

    def processUrl(self, url):
        imageResult = self.persistency.loadImageResult(url)
        if imageResult:
            return imageResult

        imageFilePath = self.persistency.getImageFilePath(url)
        if not os.path.isfile(imageFilePath) :
            self.downloadImage(url)

        image = face_recognition.load_image_file(imageFilePath)
        imageResult = self.processImage(image)
        self.persistency.saveImageResult(url, imageResult)
        return imageResult

    def processFilePath(self, imageFilePath):
        image = face_recognition.load_image_file(imageFilePath)
        # os.remove(imageFilePath)
        return self.processImage(image)

    def processImage(self, image):
        locationList = face_recognition.face_locations(image)
        encodingList = face_recognition.face_encodings(image, locationList)
        ratingList = self.ratingModel.predict(encodingList)

        imageResult = {}
        imageResult['faceList'] = []

        for i in range(len(locationList)):
            faceResult = {}
            faceResult['location'] = locationList[i]
            faceResult['encoding'] = encodingList[i].tolist()
            faceResult['rating'] = ratingList[i][0]
            imageResult['faceList'].append(faceResult)

        return imageResult
