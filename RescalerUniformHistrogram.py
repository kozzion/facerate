import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class RescalerUniformHistrogram(object):
    """docstring for RescalerUniformHistrogram."""
    def __init__(self, binCount = 20):
        super(RescalerUniformHistrogram, self).__init__()
        self.binCount = binCount
        self.xVals = None
        self.yVals = []

    def fit(self, sample):
        histTemp, binEdges = np.histogram(sample, self.binCount)
        self.xVals = binEdges
        hist = [0]
        hist.extend(histTemp)
        self.yVals = np.cumsum(hist) / len(sample)

    def transform(self, sample):
        return np.interp(sample, self.xVals, self.yVals)

    def fitTransform(self, sample):
        self.fit(sample)
        return self.transform(sample)
