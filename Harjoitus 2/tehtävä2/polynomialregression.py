# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as sm
from sklearn.model_selection import train_test_split

def performance(Y_test, X_test, coeffs, f):
    print("The performance of fit:")
    print("Mean absolute error={}".format(round(sm.mean_absolute_error(Y_test, f(X_test))), 3))
    print("Mean squared error={}".format(round(sm.mean_squared_error(Y_test, f(X_test))), 3))
    print("Explained variance score={}".format(sm.explained_variance_score(Y_test, f(X_test))))
    print("R2 score={}".format(sm.r2_score(Y_test, f(X_test))))
    print(coeffs)

def main():
    inputfile = "data_weather_oulu.txt"    # Ladataan datasetti
    X= np.loadtxt(inputfile, delimiter=",", usecols=[0])
    Y= np.loadtxt(inputfile, delimiter=",", usecols=[1])
    plt.scatter(X, Y, color="blue",s=5, marker='o') # Plotataan kaikki datasetin pisteet kuvaajaan
    #########################################################################
	#SINUN KOODISI TÄHÄN
    #########################################################################
    #performance(Y_test, X_test, coeffs, function)
    plt.grid()   # Plotataan kuvaajaan ruudukko 
    plt.show()   # Näytetään kuvaaja
	
	
if __name__ == '__main__':
    main()
