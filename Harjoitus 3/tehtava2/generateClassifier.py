from sklearn.externals import joblib
import pickle
import numpy as np
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import svm
from sklearn.externals import joblib
import cv2

def log_function(values):
    return np.log(np.abs(values))*np.sign(values)

if __name__=='__main__':
    # Ladataan datasetti
    with open('handdetectiondataset.pkl', 'rb') as f:
        data = pickle.load(f)
    # Otetaan ylös piirteet ja luokat
    X = data[0]
    Y = data[1]
    X_list = []
    for i in range(X.shape[0]):
        X_list.append(log_function(cv2.HuMoments(cv2.moments(X[i])).flatten()))
    X_train, X_test, Y_train, Y_test = train_test_split(X_list, Y, test_size=0.1)
    print ("Count of digits in dataset", Counter(Y_test))
    print ("Count of digits in dataset", Counter(Y_train))
    pp = preprocessing.StandardScaler().fit(X_train)
    X_train = pp.transform(X_train)
    X_test = preprocessing.StandardScaler().fit(X_test).transform(X_test)
    clf = svm.SVC()
    clf.fit(X_train, Y_train)
    predicted = clf.predict(X_test)
    print("Classification report for classifier SVM:\n%s\n"
      % (classification_report(Y_test, predicted)))
    print("Confusion matrix:\n%s" % confusion_matrix(Y_test, predicted))
    # Luodaan luokittelija
    joblib.dump((clf, pp), "handdetectionmodel1svm.pkl", compress=2)
    


