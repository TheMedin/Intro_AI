# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
import math
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
import matplotlib.cm as cm


def Silhouette_score(X):
    """
    Tämä funktio ottaa argumenttina datanäytteet ja palauttaa optimaalisen klustereiden lukumäärän
	"""
    ###### SINUN KOODISI TÄHÄN  ########
    best_score = -2
    best_cluster_num = 0
    for i in range(5, 11):
        classifier = KMeans(n_clusters=i, n_init=100).fit(X)
        silhouette = metrics.silhouette_score(X, classifier.labels_, metric='euclidean')

        if silhouette > best_score:
            best_score = silhouette
            best_cluster_num = i


    return best_cluster_num

def Kmeans(X, num_clusters):
    """
    Tämä funktio ottaa argumenttina datanäytteet sekä optimaalisen määrän klustereita ja opettaa Kmeans luokittelijan ja lopuksi palauttaa luokiteltujen datanäytteiden ennustetut ryhmät sekä klusterikeskipisteiden arvot
    """
	###### SINUN KOODISI TÄHÄN  ########
    kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=100).fit(X)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    return labels, cluster_centers

def Dbscan(X):
    """
    Tämä funktio ottaa argumenttina datanäytteet ja opettaa DBSCAN luokittelijan ja lopuksi palauttaa luokiteltujen datanäytteiden ennustetut ryhmät
    """
	###### SINUN KOODISI TÄHÄN  ########
    dbscan = DBSCAN(eps=0.07, min_samples=16).fit(X)
    labels = dbscan.labels_
    return labels

def Agglomerative_clustering(X, num_clusters):
    """
    Tämä funktio ottaa argumenttina datanäytteet sekä optimaalisen määrän klustereita ja opettaa kokoavan hierarkkisen klusteroinnin luokittelijan ja lopuksi palauttaa luokiteltujen datanäytteiden ennustetut
    """
	###### SINUN KOODISI TÄHÄN  ########
    model = AgglomerativeClustering(linkage='ward', n_clusters=num_clusters).fit(X)
    labels = model.labels_
    return labels

def main():
    backgroundimage = plt.imread("worldmap.jpg", format='jpg')                
    inputfile = "normalizedcoordinates.txt"
    latitude= np.loadtxt(inputfile, dtype=float, delimiter=",", usecols=[0])
    longitude= np.loadtxt(inputfile, dtype=float, delimiter=",", usecols=[1])
    X = []
    for i in range(len(latitude)):                                            
        X.append((longitude[i], latitude[i]))
    X = np.asarray(X)
	######### Alkuperäinen data  ##############
    fig, ax = plt.subplots()
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    for j in range(len(X)):     
        plt.scatter(X[j, 0], X[j, 1], c=cm.jet(0),s=7, marker='o')
    ax.imshow(backgroundimage, extent=[x0,x1,y0,y1], aspect='auto', alpha=0.8)
    plt.title("Earthquakes around the world in July 2017 (Original data)")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    ######## Silhouette score  ################
    num_clusters = Silhouette_score(X)
    ##########  K-Means  ########################	
    fig1, ax1 = plt.subplots()
    x0,x1 = ax1.get_xlim()
    y0,y1 = ax1.get_ylim()
	
    print("Best value for number of clusters based on silhouette_score was {}".format(num_clusters))
    labels, cluster_centers = Kmeans(X, num_clusters)
    for j in range(len(labels)):     
        plt.scatter(X[j, 0], X[j, 1], c=cm.jet(labels[j]/num_clusters),s=7, marker='o') #Piirretään näytteet kuvaajaan eri väreillä kmeans luokittelutiedon perusteella
    for i in range(len(cluster_centers)):
        plt.scatter(cluster_centers[i,0], cluster_centers[i,1], marker='x', s=140, linewidth=3, c = cm.jet(i/num_clusters), zorder = 10) #Piirretään myös kuvaajan kmeans algoritmin klusterikeskipisteet
    ax1.imshow(backgroundimage, extent=[x0,x1,y0,y1], aspect='auto', alpha=0.8)
    plt.title("Clustering with K-means")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
	################# DBSCAN  ###########################
    fig2, ax2 = plt.subplots()
    x0,x1 = ax2.get_xlim()
    y0,y1 = ax2.get_ylim()
	
    labels = Dbscan(X)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters for DBSCAN: {}'.format(n_clusters))
	
    unique_labels = set(labels)
    for k in range(len(labels)):
        if labels[k] == -1:
            plt.scatter(X[k, 0], X[k, 1], c=cm.gray(0), s=7,marker = 'o')
        else:
            plt.scatter(X[k, 0], X[k, 1], c=cm.jet(labels[k]/len(unique_labels)), s=5,marker = 'o')	

    ax2.imshow(backgroundimage, extent=[x0,x1,y0,y1], aspect='auto', alpha=0.8)
    plt.title("Clustering with DBSCAN")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
	############## Kokoava hierarkinen klusterointi ###########################
    fig3, ax3 = plt.subplots()
    x0,x1 = ax3.get_xlim()
    y0,y1 = ax3.get_ylim()
	
    labels = Agglomerative_clustering(X, num_clusters)
    for k in range(len(labels)):    
        plt.scatter(X[k, 0], X[k, 1], c=cm.jet(labels[k]/num_clusters),s=7, marker='o')
    ax3.imshow(backgroundimage, extent=[x0,x1,y0,y1], aspect='auto', alpha=0.8)
    plt.title("Clustering with AgglomerativeClustering")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
		
    plt.show()
	
if __name__ == '__main__':
    main()