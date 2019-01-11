import uuid
import itertools
import os
import face_recognition
import requests
import numpy as np
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
        ratingListList = self.ratingModel.predict(encodingList)

        imageResult = {}
        imageResult['imageWidth'] = np.size(image, 1)
        imageResult['imageHeight'] = np.size(image, 0)
        imageResult['imageFeatureList'] = []
        imageResult['imagePropertyMap'] = {}
        imageResult['imageTagMap'] = {}

        for i in range(len(locationList)):
            imageFeature = {}
            imageFeature['featureLocation'] = locationList[i]
            imageFeature['featurePropertyMap'] = {}
            imageFeature['featureTagMap'] = {}

            imageFeature['featurePropertyMap']['rating'] = ratingListList[i][0]

            imageResult['imageFeatureList'].append(imageFeature)

        return imageResult
