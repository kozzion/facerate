import os
import json
import csv
import codecs
import numpy as np
import hashlib

class Persistency(object):
    """docstring for Persistency."""
    def __init__(self, rootPath = 'C:\\DataSets\\SCUTFBP5500\\'):
        super(Persistency, self).__init__()
        self.rootPath = rootPath
        self.imageDirPath = rootPath + 'image\\'
        self.imageResultDirPath = rootPath + 'imageresult\\'
        self.encodingDirPath = rootPath + 'encoding\\'
        self.dataDirPath = rootPath + 'data\\'

    def getImageFilePath(self, url):
        os.makedirs(self.imageDirPath, exist_ok=True)
        fileName = hashlib.sha256(url.encode('utf-8')).hexdigest() + '.jpg' #TODO in future other extentions
        return self.imageDirPath + fileName

    def getImageResultFilePath(self, url):
        os.makedirs(self.imageResultDirPath, exist_ok=True)
        fileName = hashlib.sha256(url.encode('utf-8')).hexdigest() + '.json'
        return self.imageResultDirPath + fileName


    def loadImageFilePathList(self):
        return [os.path.join(self.imageDirPath, file) for file in os.listdir(self.imageDirPath) if os.path.isfile(os.path.join(self.imageDirPath, file))]

    def loadUsernameList(self):
        return [os.path.splitext(file)[0] for file in os.listdir(self.imageDirPath) if os.path.isfile(os.path.join(self.imageDirPath, file))]

    def loadRatingList(self) :
        filePath  = self.rootPath + 'allratings.csv'
        with open(filePath, 'r') as csvfile:
            return list(csv.reader(csvfile, delimiter=',', quotechar='|'))[1:]


    def saveDataSet(self, datasetName, X, Y):
        filePath = self.dataDirPath + datasetName + '.json'
        with codecs.open(filePath, 'w', encoding='utf-8') as file:
            json.dump((X.tolist(), Y.tolist()), file, separators=(',', ':'), sort_keys=True, indent=4)
        # self.saveJson(filePath, (X,Y))

    def loadDataSet(self, datasetName):
        filePath = self.dataDirPath + datasetName + '.json'
        if os.path.isfile(filePath):
            with codecs.open(filePath, 'r', encoding='utf-8') as file:
                (Xlist, Ylist) = json.loads(file.read())
                return np.array(Xlist), np.array(Ylist)
        else:
            return None
        # self.saveJson(filePath, (X,Y))

    def loadEncoding(self, username):
        filePath  = self.encodingDirPath + username + '.json'
        return self.loadJson(filePath)


    def saveEncoding(self, username, encoding):
        filePath =  self.encodingDirPath + username + '.json'
        self.saveJson(filePath, encoding)


    def loadImageResult(self, url):
        filePath  = self.getImageResultFilePath(url)
        return self.loadJson(filePath)


    def saveImageResult(self, url, imageResult):
        filePath  = self.getImageResultFilePath(url)
        self.saveJson(filePath, imageResult)


    def saveJson(self, filePath, jsonObject) :
        # get and delete old file if it exists
        with open(filePath, 'w', encoding="utf-8") as file:
            json.dump(jsonObject, file, ensure_ascii=False)

    def loadJson(self, filePath) :
        if os.path.isfile(filePath):
            with open(filePath, 'r', encoding="utf-8") as file:
                return json.load(file)
        else:
            return None
