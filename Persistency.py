import os
import json
import csv
import codecs
import numpy as np
import hashlib

class Persistency(object):
    """docstring for Persistency."""
    def __init__(self, rootDirPath):
        super(Persistency, self).__init__()
        self.rootDirPath = rootDirPath
        self.imageDirPath = os.path.join(rootDirPath, "image")
        self.imageResultDirPath = os.path.join(rootDirPath, "imageresult")
        self.encodingDirPath = os.path.join(rootDirPath, "encoding")
        self.dataDirPath = os.path.join(rootDirPath, "data")

        os.makedirs(self.rootDirPath, exist_ok=True)
        os.makedirs(self.imageDirPath, exist_ok=True)
        os.makedirs(self.imageResultDirPath, exist_ok=True)
        os.makedirs(self.encodingDirPath, exist_ok=True)
        os.makedirs(self.dataDirPath, exist_ok=True)

    def getImageFilePath(self, url):
        fileName = hashlib.sha256(url.encode('utf-8')).hexdigest() + '.jpg' #TODO in future other extentions
        return os.path.join(self.imageDirPath, fileName)

    def getImageResultFilePath(self, url):
        fileName = hashlib.sha256(url.encode('utf-8')).hexdigest() + '.json'
        return os.path.join(self.imageResultDirPath, fileName)


    def loadImageFilePathList(self):
        return [os.path.join(self.imageDirPath, file) for file in os.listdir(self.imageDirPath) if os.path.isfile(os.path.join(self.imageDirPath, file))]

    def loadUsernameList(self):
        return [os.path.splitext(file)[0] for file in os.listdir(self.imageDirPath) if os.path.isfile(os.path.join(self.imageDirPath, file))]

    def load_rating_list(self) :
        filePath  = os.path.join(self.rootDirPath, 'allratings.csv')
        with open(filePath, 'r') as csvfile:
            return list(csv.reader(csvfile, delimiter=',', quotechar='|'))[1:]


    def save_dataset_dual(self, dataset_name, X, Y):
        filePath = os.path.join(self.dataDirPath, datasetName + '.json')
        with codecs.open(filePath, 'w', encoding='utf-8') as file:
            json.dump((X.tolist(), Y.tolist()), file, separators=(',', ':'), sort_keys=True, indent=4)

    def load_dataset_dual(self, dataset_name):
        filePath = os.path.join(self.dataDirPath , dataset_name + '.json')
        print(filePath)
        if os.path.isfile(filePath):
            with codecs.open(filePath, 'r', encoding='utf-8') as file:
                (Xlist, Ylist) = json.loads(file.read())
                return np.array(Xlist), np.array(Ylist)
        else:
            return None

    def save_dataset(self, dataset_name, dataset):
        filePath = os.path.join(self.dataDirPath, dataset_name + '.json')
        self.saveJson(filePath, dataset)

    def load_dataset(self, dataset_name):
        filePath = os.path.join(self.dataDirPath, dataset_name + '.json')
        return self.loadJson(filePath)

    def loadEncoding(self, username):
        filePath  = os.path.join(self.encodingDirPath, username + '.json')
        return self.loadJson(filePath)


    def saveEncoding(self, username, encoding):
        filePath =  os.path.join(self.encodingDirPath, username + '.json')
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
