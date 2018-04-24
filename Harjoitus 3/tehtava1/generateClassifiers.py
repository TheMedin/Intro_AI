from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn import preprocessing
import numpy as np
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def ModelSVM(hog_features, labels, pp):
    model = "SupportVectorMachine"
    clf = SVC(kernel="rbf")
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model1svm.pkl", compress=3)
    return (model, clf)

def ModelKNN(hog_features, labels, pp):
    model = "k-NearestNeighbors"
    clf = KNeighborsClassifier(n_jobs=-1)
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model2knn.pkl", compress=3)
    return (model, clf)

def ModelDecisionTree(hog_features, labels, pp):
    model = "DecisionTree"
    clf = DecisionTreeClassifier()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model3decisiontree.pkl", compress=3)
    return (model, clf)

def ModelRandomForest(hog_features, labels, pp):
    model = "RandomForest"
    clf = RandomForestClassifier()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model4randomforest.pkl", compress=3)
    return (model, clf)

def ModelAdaboost(hog_features, labels, pp):
    model = "Adaboost"
    clf = AdaBoostClassifier()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model5adaboost.pkl", compress=3)
    return (model, clf)

def ModelGaussianNB(hog_features, labels, pp):
    model = "GaussianNaiveBayes"
    clf = GaussianNB()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model6gaussiannb.pkl", compress=3)
    return (model, clf)
	
def ModelSGD(hog_features, labels, pp):
    model = "StochasticGradientDescent"
    clf = SGDClassifier(n_jobs=-1)
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model7sgd.pkl", compress=3)
    return (model, clf)

def ModelLDA(hog_features, labels, pp):
    model = "LinearDiscriminantAnalysis"
    clf = LinearDiscriminantAnalysis()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model8lda.pkl", compress=3)
    return (model, clf)

def ModelLogisticRegression(hog_features, labels, pp):
    model = "LogisticRegression"
    clf = LogisticRegression(n_jobs=-1)
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model9logisticregression.pkl", compress=3)
    return (model, clf)

def ModelMLP(hog_features, labels, pp):
    model = "MultilayerPerceptron"
    clf = MLPClassifier(activation='relu',hidden_layer_sizes=(200,200),solver='lbfgs',alpha=10,verbose=True)
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model10mlp.pkl", compress=3)
    return (model, clf)
	
def ModelRandomQuessing(hog_features, labels, pp):
    model = "RandomQuessing"
    clf = DummyClassifier()
    clf.fit(hog_features, labels)
    joblib.dump((clf, pp), "model11randomquessing.pkl", compress=3)
    return (model, clf)

def accuracy(modelclf, X_test, Y_test):
    model, clf = modelclf
    predicted = clf.predict(X_test)
    print("Classification report for classifier %s:\n%s\n\n"
      % (model, classification_report(Y_test, predicted)))
    print("Confusion matrix:\n%s\n" % confusion_matrix(Y_test, predicted))

if __name__=='__main__':
    # Ladataan datasetti
    dataset = datasets.fetch_mldata("MNIST Original")
    # Otetaan talteen piirteet ja luokat
    X = np.array(dataset.data, 'int16')
    Y = np.array(dataset.target, 'int')
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
    # Lasketaan HOG-piirteet
    list_X_train = []
    for trainsample in X_train:
        fd = hog(trainsample.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        list_X_train.append(fd)
    X_train = np.array(list_X_train, 'float64')
    pp = preprocessing.StandardScaler().fit(X_train)
    X_train = pp.transform(X_train)
    list_X_test = []
    for testsample in X_test:
        fd = hog(testsample.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        list_X_test.append(fd)
    X_test = np.array(list_X_test, 'float64')
    X_test = preprocessing.StandardScaler().fit(X_test).transform(X_test)
    # Printataan opetus-setin ja testisetin näytteiden lukumäärät
    print ("Count of digits in training dataset", Counter(Y_train))
    print ("Count of digits in test dataset", Counter(Y_test))
    print ("\n\n")
    # Toteutetaan luokittelijat sekä lasketaan niille luokittelutarkkuudet sekä sekaannusmatriisit 
    accuracy(ModelSVM(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelKNN(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelDecisionTree(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelRandomForest(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelAdaboost(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelGaussianNB(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelSGD(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelLDA(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelLogisticRegression(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelMLP(X_train, Y_train, pp),X_test,Y_test)
    accuracy(ModelRandomQuessing(X_train, Y_train, pp),X_test,Y_test)
