import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.model_selection
import sklearn.linear_model

from Persistency import Persistency

ps = Persistency()
X,Y = ps.loadDataSet('meanrating')

Xtrain, Xtest, Ytrain, Ytest = sklearn.model_selection.train_test_split(X, Y)
reg = sklearn.linear_model.Lasso(alpha = 0.001)
reg.fit(Xtrain, Ytrain)
Ypredicted = reg.predict(Xtest)

print(sklearn.metrics.mean_squared_error(Ytest, Ypredicted))
#
plt.scatter(Ytest, Ypredicted)
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.show()
