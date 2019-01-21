import sys

sys.path.append('./model/')

import numpy as np
import matplotlib.pyplot as plt
import face_recognition
import sklearn
import sklearn.model_selection
from sklearn.metrics import roc_curve, auc

from persistency import Persistency
from model_face_linear_multy import ModelFaceLinearMulty

ps = Persistency('C:/DataSets/SCUTFBP5500')

X,Y = ps.loadDataSet('rating')

# Xtrain, Xtest, Ytrain, Ytest = sklearn.model_selection.train_test_split(X, Y)
model = ModelFaceLinearMulty()
model.fit(X, Y)
Ypredicted = np.zeros((X.shape[0], 7))
for i in range(X.shape[0]):
    encoding = np.transpose(X[i,:, None])
    Ypredicted[i,:] = model.predict(encoding)[:,0]


Saf = np.logical_and(Y[:,1] == 0, Y[:,2] == 0)
Sam = np.logical_and(Y[:,1] == 0, Y[:,2] == 1)
Scf = np.logical_and(Y[:,1] == 1, Y[:,2] == 0)
Scm = np.logical_and(Y[:,1] == 1, Y[:,2] == 1)


# rating all
plt.scatter(Y[:,0], Ypredicted[:,0])
plt.xlim(1, 5)
plt.ylim(0, 1.1)
#plt.show()


#scatter
plt.figure()
plt.scatter(Y[Saf,0], Ypredicted[Saf,0])
plt.scatter(Y[Sam,0], Ypredicted[Sam,0])
plt.scatter(Y[Scf,0], Ypredicted[Scf,0])
plt.scatter(Y[Scm,0], Ypredicted[Scm,0])
plt.xlim(1, 5)
plt.ylim(0, 1.1)
plt.legend(['af', 'am', 'cf', 'cm'])
#plt.show()


#histogram
plt.figure()
n, bins, patches = plt.hist(x=Ypredicted[Saf,0], bins='auto')
n, bins, patches = plt.hist(x=Ypredicted[Sam,0], bins='auto')
n, bins, patches = plt.hist(x=Ypredicted[Scf,0], bins='auto')
n, bins, patches = plt.hist(x=Ypredicted[Scm,0], bins='auto')
plt.legend(['af', 'am', 'cf', 'cm'])
plt.show()

# ROC
fprc, tprc, _ = roc_curve(Y[:, 1], Ypredicted[:, 1])
roc_aucc = auc(fprc, tprc)
print(roc_aucc)

fprm, tprm, _ = roc_curve(Y[:, 2], Ypredicted[:, 2])
roc_aucm = auc(fprm, tprm)
print(roc_aucm)
