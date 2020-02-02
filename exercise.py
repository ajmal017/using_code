import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

df = pd.read_csv('basketball.csv')
train, test = train_test_split(df, test_size=0.2)




def svc_param_selection(X, y, nfolds):
    svm_parameters= [
        {'kernel': ['rbf'],
         'gamma': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1],
         'C': [0.01, 0.1, 1, 10, 100, 1000]
         }]

    clf = GridSearchCV(SVC(), svm_parameters, cv=10)
    clf.fit(X_train, y_train.values.ravel())
    print(clf.best_params_)

    return clf


X_train = train[['3P', 'BLK']]
y_train = train[['Pos']]

clf = svc_param_selection(X_train, y_train.values.ravel(), 10)
print(clf)


C_candidates = []
C_candidates.append(clf.best_params_['C'] * 0.01)
C_candidates.append(clf.best_params_['C'])
C_candidates.append(clf.best_params_['C']*100)


gamma_candidates = []
gamma_candidates.append(clf.best_params_['gamma'] * 0.01)
gamma_candidates.append(clf.best_params_['gamma'])
gamma_candidates.append(clf.best_params_['gamma']*100)

X = train[['3P', 'BLK']]
Y = train['Pos'].tolist()
position = []
for gt in Y:
    if gt == 'C':
        position.append(0)
    else: position.append(1)

classifiers = []

for C in C_candidates:
    for gamma in gamma_candidates:
        clf= SVC(C=C, gamma=gamma)
        clf.fit(X, Y)
        classifiers.append((C, gamma, clf))

plt.figure(figsize=(18,18))
xx, yy = np.meshgrid(np.linspace(0,4,100), np.linspace(0,4,100))

for (k, (C,gamma, clf)) in enumerate(classifiers):
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.subplot(len(C_candidates), len(gamma_candidates), k+1)
    plt.title("gamma=10^%d, C=10^%d" % (np.log10(gamma), np.log10(C)), size='medium')

    plt.pcolormesh(xx, yy, -Z, cmap=cm.RdBu)
    plt.scatter(X['3P'], X['BLK'], c=position, cmap=cm.RdBu_r, edgecolors='k')

X_test = test[['3P', 'BLK']]
y_test = test[['Pos']]

y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))
print()
print(accuracy_score(y_true, y_pred))