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
    plt.scatter(X, Y, color="blue",s=5, marker='o', label="ei-koulutus data") # Plotataan kaikki datasetin pisteet kuvaajaan
    #########################################################################
	#SINUN KOODISI TÄHÄN
    #########################################################################

    # testidatan osuus nostettu 0.2:n jotta kunnollinen ylisovittaminen onnistuisi

    # lineaarinen

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    coeffs = np.polyfit(X_train, Y_train, 1)
    function = np.poly1d(coeffs)
    x_line = np.linspace(min(X_train), max(X_train))
    y_line = function(x_line)

    plt.scatter(X_train, Y_train, color="cyan", s=5, marker='x')
    plt.plot(x_line, y_line, color="cyan", label="lineaarinen")
    performance(Y_test, X_test, coeffs, function)


    # sopiva sovitus, 12. asteen toimii yleensä hyvin mutta vaihtelee ajokerran mukaan

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    coeffs = np.polyfit(X_train, Y_train, 6)
    function = np.poly1d(coeffs)
    x_line = np.linspace(min(X_train), max(X_train))
    y_line = function(x_line)

    plt.scatter(X_train, Y_train, color="red", s=5, marker='x')
    plt.plot(x_line, y_line, color="red", label="6. aste, usein sopiva sovitus")
    performance(Y_test, X_test, coeffs, function)

    # ylisovitettu
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    coeffs = np.polyfit(X_train, Y_train, 220)
    function = np.poly1d(coeffs)
    x_line = np.linspace(min(X_train), max(X_train))
    y_line = function(x_line)

    plt.scatter(X_train, Y_train, color="orange", s=5, marker='x')
    plt.plot(x_line, y_line, color="orange", label="220. aste, ylisovitettu")
    performance(Y_test, X_test, coeffs, function)


    plt.title("Lämpötila kellonajan mukaan")
    plt.xlabel("Kellonaika")
    plt.ylabel("Lämpötila, C°")

    #performance(Y_test, X_test, coeffs, function)
    plt.grid()   # Plotataan kuvaajaan ruudukko 
    plt.legend() # Kirjoittaa viivoille legendit
    plt.show()   # Näytetään kuvaaja
	
	
if __name__ == '__main__':
    main()
