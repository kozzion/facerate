import numpy as np

from rescaler_uniform_histrogram import RescalerUniformHistrogram

class ModelFaceLinear(object):
    """docstring for ModelFaceLinear."""
    def __init__(self):
        super(ModelFaceLinear, self).__init__()
        self.weigths = None
        self.rescaler = None

    def fit(self, X,Y):
        Xaug = np.ones((X.shape[0],X.shape[1] + 1))
        Xaug[:,0:X.shape[1]] = X;
        Xn = np.matmul(np.transpose(Xaug),Xaug)
        Yn = np.matmul(np.transpose(Xaug),Y)
        self.weigths = np.linalg.solve(Xn, Yn)
        Ys = np.matmul(Xaug, self.weigths)

        self.rescaler = RescalerUniformHistrogram()
        self.rescaler.fit(Ys)

    def predict(self, encodingList):
        if(len(encodingList) == 0):
            return []
        X = np.array(encodingList)
        Xaug = np.ones((X.shape[0],X.shape[1] + 1))
        Xaug[:,0:X.shape[1]] = X;
        Y = np.matmul(Xaug, self.weigths)
        return self.rescaler.transform(Y)
