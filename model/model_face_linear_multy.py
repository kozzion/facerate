import numpy as np

from model_face_linear import ModelFaceLinear

class ModelFaceLinearMulty(object):
    """docstring for ModelFaceLinearMulty."""
    def __init__(self):
        super(ModelFaceLinearMulty, self).__init__()
        self.modelList = []
        self.ratingNameList = []

    def fit(self, X, Y):
        xList, yList, ratingNameList = self.splitData(X, Y)
        self.ratingNameList = ratingNameList
        for i in range(len(xList)):
            model = ModelFaceLinear()
            model.fit(xList[i], yList[i])
            self.modelList.append(model)

    def splitData(self, X, Y):
        xList = []
        yList = []
        ratingNameList = []
        xList.append(X)
        yList.append(Y[:,0])
        ratingNameList.append('rating_all')

        xList.append(X)
        yList.append(Y[:,1])
        ratingNameList.append('rating_c')

        xList.append(X)
        yList.append(Y[:,2])
        ratingNameList.append('rating_m')

        S = np.logical_and(Y[:,1] == 0, Y[:,2] == 0)
        xList.append(X[S,:])
        yList.append(Y[S,0])
        ratingNameList.append('rating_af')

        S = np.logical_and(Y[:,1] == 0, Y[:,2] == 1)
        xList.append(X[S,:])
        yList.append(Y[S,0])
        ratingNameList.append('rating_am')

        S = np.logical_and(Y[:,1] == 1, Y[:,2] == 0)
        xList.append(X[S,:])
        yList.append(Y[S,0])
        ratingNameList.append('rating_cf')

        S = np.logical_and(Y[:,1] == 1, Y[:,2] == 1)
        xList.append(X[S,:])
        yList.append(Y[S,0])
        ratingNameList.append('rating_cm')

        return xList, yList, ratingNameList


    def predict(self, encodingList):
        modelCount = len(self.modelList)
        Y = np.zeros((modelCount, 1))
        for i in range(modelCount):
            Y[i, 0] = self.modelList[i].predict(encodingList)[0]
        return Y
