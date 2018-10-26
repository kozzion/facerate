import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import face_recognition
import sklearn as svm
import sklearn.model_selection

from Persistency import Persistency

ps = Persistency()
X,Y = ps.loadDataSet('meanrating')

Xtrain, Xtest, Ytrain, Ytest = sklearn.model_selection.train_test_split(X, Y)
clf = sklearn.svm.SVR()
clf.fit(Xtrain, Ytrain)
Ypredicted = clf.predict(Xtest)

print(sklearn.metrics.mean_squared_error(Ytest, Ypredicted))
#
plt.scatter(Ytest, Ypredicted)
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.show()
