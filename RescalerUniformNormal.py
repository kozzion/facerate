import numpy as np
from scipy.stats import norm

class RescalerUniformNormal(object):
    """docstring for RescalerUniformNormal."""
    def __init__(self):
        super(RescalerUniformNormal, self).__init__()
        self.mean = 0
        self.sdev = 0

    def fit(self, sample):
        self.mean = np.mean(sample)
        self.sdev = np.std(sample)

    def transform(self, sample):
        return norm.cdf(sample, self.mean, self.sdev)

    def fitTransform(self, sample):
        self.fit(self, sample)
        return self.transform(sample)
