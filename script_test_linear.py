import numpy as np
import matplotlib.pyplot as plt
import face_recognition
from persistency import Persistency
import sklearn
import sklearn.model_selection

ps = Persistency('C:/DataSets/SCUTFBP5500')

X,Y = ps.loadDataSet('meanrating')

Xtrain, Xtest, Ytrain, Ytest = sklearn.model_selection.train_test_split(X, Y)

Xaug = np.ones((Xtrain.shape[0],Xtrain.shape[1] + 1))
Xaug[:,0:Xtrain.shape[1]] = Xtrain
Xn = np.matmul(np.transpose(Xaug),Xaug)
Yn = np.matmul(np.transpose(Xaug),Ytrain)
Maug = np.linalg.solve(Xn, Yn)


Xaug = np.ones((Xtest.shape[0],Xtest.shape[1] + 1))
Xaug[:,0:Xtest.shape[1]] = Xtest
Ypredicted = np.matmul(Xaug,Maug)

print(sklearn.metrics.mean_squared_error(Ytest, Ypredicted))

plt.scatter(Ytest, Ypredicted)
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.show()
