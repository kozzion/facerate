import uuid
import itertools

import face_recognition

from Persistency import Persistency
from ModelFaceLinear import ModelFaceLinear


class SystemFaceStream(object):
    """docstring for SystemFaceStream."""
    def __init__(self, rootDirPath = './persitency/', memorySize = 10):
        super(SystemFaceStream, self).__init__()
        self.memorySize = memorySize
        self.streamDict = {}
        self.ratingModel = ModelFaceLinear()
        self.frameIndex = 0

        ps = Persistency(rootDirPath)
        X,Y = ps.loadDataSet('meanrating')
        self.ratingModel.fit(X,Y)


    # def labelImage(self, streamName):
    def findGuid(self, streamName, encoding):
        userguidMatchList = []
        for i in range(self.memorySize):
            if i in self.streamDict[streamName]['frameDict']:
                frame = self.streamDict[streamName]['frameDict'][i]
                encodingList = frame['encodingList']
                userguidList = frame['userguidList']
                matches = face_recognition.compare_faces(encodingList, encoding)
                userguidMatchList.extend(list(itertools.compress(userguidList, matches)))
        if (len(userguidMatchList) == 0):
            return str(uuid.uuid4())
        else:
            return userguidMatchList[0]

    def addStreamFrame(self, streamName, encodingList, userguidList, ratingList):
        frame = {}
        frame['encodingList'] = encodingList
        frame['userguidList'] = userguidList
        self.streamDict[streamName]['frameDict'][self.frameIndex] = frame

        for i in range(len(userguidList)):
            userguid = userguidList[i]
            if not userguid in self.streamDict[streamName]['userguidDict']:
                user = {}
                user['ratingList'] = []
                self.streamDict[streamName]['userguidDict'][userguid] = user
            self.streamDict[streamName]['userguidDict'][userguid]['ratingList'].append(ratingList[i])
            if(20 < len(self.streamDict[streamName]['userguidDict'][userguid]['ratingList'])):
                self.streamDict[streamName]['userguidDict'][userguid]['ratingList'].pop(0)
        #TODO add averges


    def processStreamImage(self, streamName, image):
        self.frameIndex = (self.frameIndex + 1) % self.memorySize

        if not streamName in self.streamDict:
            self.streamDict[streamName] = {}
            self.streamDict[streamName]['frameDict'] = {}
            self.streamDict[streamName]['userguidDict'] = {}


        # TODO rescale image to manageble size
        locationList = face_recognition.face_locations(image)
        encodingList = face_recognition.face_encodings(image, locationList)
        userguidList = [self.findGuid(streamName, encoding) for encoding in encodingList]
        ratingList = self.ratingModel.predict(encodingList)

        self.addStreamFrame(streamName, encodingList, userguidList, ratingList)

        imageResult = {}
        imageResult['faceList'] = []


        for i in range(len(locationList)):
            # TODO just get old data
            location = locationList[i]
            userguid = userguidList[i]

            userRatingList = self.streamDict[streamName]['userguidDict'][userguid]['ratingList']
            rating = sum(userRatingList) / len(userRatingList)

            faceResult = {}
            faceResult['location'] = location
            faceResult['userguid'] = userguid
            faceResult['username'] = 'unknown'
            faceResult['rating'] = rating

            imageResult['faceList'].append(faceResult)



        return imageResult

    def closeStream(self, streamName):
        if streamName in self.streamDict:
            del self.streamDict[streamName]
