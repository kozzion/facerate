import os

import face_recognition
import numpy as np

from persistency import Persistency

ps = Persistency('C:/DataSets/SCUTFBP5500')

encodingDict = {}
imageFilePathList = ps.loadImageFilePathList()
# print(imageFilePathList)
encodingDict = {}
ratingDictDict = {}


# create missing encoding
for imageFilePath in imageFilePathList:
    username = os.path.splitext(os.path.basename(imageFilePath))[0]
    encoding = ps.loadEncoding(username)
    if(encoding == None):
        encodingList = face_recognition.face_encodings(face_recognition.load_image_file(imageFilePath))
        if(len(encodingList) == 1):
            encoding = encodingList[0]
            ps.saveEncoding(username, encoding.tolist())
        else:
            print(username)
    encodingDict[username] = encoding
    ratingDictDict[username] = {}

ratingList = ps.loadRatingList()
for rating in ratingList:
    rater = rating[0]
    username = os.path.splitext(rating[1])[0]
    ratingDictDict[username][rater] = float(rating[2])

ratingDict = {}
for username in ratingDictDict:
    ratingList = [ratingDictDict[username][rater] for rater in ratingDictDict[username]]
    meanRating = sum(ratingList) / len(ratingList)
    ratingDict[username] = meanRating


#build matrix 1 = C 1 = M
encodingSize = 128
usernameList = ps.loadUsernameList()
X = np.zeros((len(usernameList), encodingSize))
Y = np.zeros((len(usernameList), 3))
for i in range(len(usernameList)):
    username = usernameList[i]
    print(username)
    X[i,:] = encodingDict[username]
    Y[i,0] = ratingDict[username]
    if username[0] == 'C':
        Y[i,1] = 1
    if username[1] == 'M':
        Y[i,2] = 1
selection = ~(np.nansum(X, 1) == 0)
X = X[selection, :]
Y = Y[selection, :]
print(X.shape)
ps.saveDataSet('rating', X, Y)
