# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as sm
from sklearn.model_selection import train_test_split

def performance(Y_test, X_test, coeffs, f):
    print("The performance of linear fit:")
    print("Mean absolute error={}".format(round(sm.mean_absolute_error(Y_test, f(X_test))), 3))
    print("Mean squared error={}".format(round(sm.mean_squared_error(Y_test, f(X_test))), 3))
    print("Explained variance score={}".format(sm.explained_variance_score(Y_test, f(X_test))))
    print("R2 score={}".format(sm.r2_score(Y_test, f(X_test))))
    print("Fitted line is form y={}x + {}".format(coeffs[0],coeffs[1]))

def main():
    #inputfile = "data_ects_accumulation.txt"    # Ladataan datasetti
    #inputfile = "data_life_expectancy_finland.txt"    # Ladataan datasetti
    #inputfile = "data_population_growth_finland.txt"    # Ladataan datasetti
    inputfile = "data_sea_level.txt"    # Ladataan datasetti
    X= np.loadtxt(inputfile, delimiter=",", usecols=[0])
    Y= np.loadtxt(inputfile, delimiter=",", usecols=[1])
    plt.scatter(X, Y, color="blue",s=5, marker='o') # Plotataan kaikki datasetin pisteet kuvaajaan 
    #########################################################################
	#SINUN KOODISI TÄHÄN

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
    coeffs = np.polyfit(X_train, Y_train, 1)
    function = np.poly1d(coeffs)
    x_line = np.linspace(min(X_train), max(X_train))
    y_line = function(x_line)

    plt.scatter(X_train, Y_train, color="cyan", s=5, marker='x')
    plt.plot(x_line, y_line, color="red")
    plt.title("Opiskelujen eteneminen OP/kesto")
    plt.xlabel("Vuosi")
    plt.ylabel("Opintopisteet")

    # ETCS:
    #print("Opintopisteitä oli kerätty 2 vuoden jälkeen keskimäärin {}".format(round(coeffs[0]*2+coeffs[1])))

    # Life expectancy:
    #print("Suomalaisten eliniänodote vuonna 2030 on {}".format(round(coeffs[0]*2030+coeffs[1])))

    # Population growth:
    #print("Suomen väkiluku vuonna 2030 on {}".format(round(coeffs[0]*2035+coeffs[1])))

    # Sea level:
    print("Vedenpinnakorkeus vuonna 2025 on {}".format(round(coeffs[0]*2025+coeffs[1])))

    #########################################################################
    #performance(Y_test, X_test, coeffs, function)
    plt.grid()   # Plotataan kuvaajaan ruudukko
    plt.show()   # Näytetään kuvaaja
	
	
if __name__ == '__main__':
    main()
