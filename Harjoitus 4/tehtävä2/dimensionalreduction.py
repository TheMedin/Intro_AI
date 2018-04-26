import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
import numpy as np
import pickle
from skimage.transform import resize
from time import time

def Load_handdetection_dataset():
    """
    Ladataan tässä funktiossa käsimerkki-data
    """
    with open("handdetection-dataset.pkl", "rb") as f:
        data = pickle.load(f) 
    X_orig1,y = data[0], data[1]
#    X_data1 = np.reshape(X_orig1, (700, 15000))
    X_data1 = np.reshape(X_orig1, (403, 15000))
    y_labels1 = ['${}$'.format(x) for x in y]

    chars = ["1","2","3","4","5","6"]
    for i,j in enumerate(chars):
        y1 = list(s.replace(j, "{}".format(i)) for s in y)
    return X_data1, X_orig1, y_labels1, y1
	
def Load_mnist_dataset():
    """
    Ladataan tässä funktiossa MNIST data
    """
    digits = load_digits(10)
    X_orig2 = digits.images
    X_data2,y2 = digits.data, digits.target
    y_labels2 = ['${}$'.format(x) for x in y2]
    return X_data2, X_orig2, y_labels2, y2
	
def MinMaxScaling(data):
    """
    Toteutaan datan normalisointi välille [0,1] dimensionaalisuuden vähentämisen jälkeen
    """
    x_min, x_max = np.min(data,0), np.max(data,0)
    X_scaled = (data - x_min)/(x_max - x_min)
    return X_scaled
	
def Train_tsne(X_data):
    """
    Toteuta t-SNE algoritmin opettaminen. Normalisoi datanäytteet välille [0,1] pisteiden piirtämistä varten MinMaxScaling funktiolla. Laske myös algoritmin käyttämä suoritusaika.
    
    Funktio ottaa argumenttina datan ja palauttaa redusoidun ja skaalatun datan sekä ajan, joka algoritmin ajamiseen kesti.
    """
    ###### SINUN KOODISI TÄHÄN  ########
    t0 = time()
    X_tsne = TSNE(n_components=2, metric='sqeuclidean').fit_transform(X_data)
    t1 = time()
    X_scaled = MinMaxScaling(X_tsne)
    return X_scaled, t1 - t0

def Train_PCA(X_data):
    """
    Toteuta PCA algoritmin opettaminen. Normalisoi datanäytteet välille [0,1] pisteiden piirtämistä varten MinMaxScaling funktiolla. Laske myös algoritmin käyttämä suoritusaika.
    
    Funktio ottaa argumenttina datan ja palauttaa redusoidun ja skaalatun datan sekä ajan, joka algoritmin ajamiseen kesti.
    """
    ###### SINUN KOODISI TÄHÄN  ########
    t0 = time()
    X_PCA = PCA(n_components=2).fit_transform(X_data)
    t1 = time()
    X_scaled = MinMaxScaling(X_PCA)
    return X_scaled, t1 - t0

	
def Train_MDS(X_data):
    """
    Toteuta MDS algoritmin opettaminen. Normalisoi datanäytteet välille [0,1] pisteiden piirtämistä varten MinMaxScaling funktiolla. Laske myös algoritmin käyttämä suoritusaika.
    
    Funktio ottaa argumenttina datan ja palauttaa redusoidun ja skaalatun datan sekä ajan, joka algoritmin ajamiseen kesti.
    """
	###### SINUN KOODISI TÄHÄN  ########	
    t0 = time()
    X_MDS = MDS().fit_transform(X_data)
    t1 = time()
    X_scaled = MinMaxScaling(X_MDS)
    return X_scaled, t1 - t0
	
def Evaluation(X_data, truelabels):
    """
    Tämä funktio luo knn-luokittelijan dimensinaalisuuden redusointi algoritmin käsitellystä datasta ja laskee sille F1-scoren arvon. F1-scoren arvon tarkoitus on ainoastaan antaa mitta redusoidun datan kompleksisuudelle
    """
    clf = KNeighborsClassifier(n_neighbors=49).fit(X_data, truelabels)
    y_pred = clf.predict(X_data)
    print("F1_score:%s\n" % f1_score(truelabels, y_pred, average='micro'))

def Draw_example_pictures_to_figure(X_orig,X, X_scaled, ax, mnistdata):
    """
    Piirretään esimerkki kuvia kuvaajaan minimietäisyyden välein
    """
    shown_images = np.array([[1., 1.]])
    for i in range(X_orig.shape[0]):
        dist = np.sum((X_scaled[i] - shown_images) ** 2, 1)
        if np.min(dist) < 6e-3:     # don't show points that are too close
            continue
        shown_images = np.r_[shown_images, [X_scaled[i]]]
        if mnistdata:
            imagebox = offsetbox.AnnotationBbox(offsetbox.OffsetImage(resize(X_orig[i], (60,60), order=1, preserve_range=True), cmap=plt.cm.gray_r),X_scaled[i])
        else:
            imagebox = offsetbox.AnnotationBbox(offsetbox.OffsetImage(resize(X_orig[i], (120,80), order=1, preserve_range=True), cmap=plt.cm.gray_r),X_scaled[i])
        ax.add_artist(imagebox)
	
def Draw_datasamples_to_figure(X_scaled, y_labels, y, colors):
    """
    Plotataan datan pisteet kuvaajaan. Datanäytteiden luokkia on kuvattu eri numeroilla ja väreillä 
    """
    for (X_plot, Y_plot, color, y_label) in zip(X_scaled[:,0], X_scaled[:,1], y, y_labels):
        plt.scatter(X_plot, Y_plot, color=colors[int(color)], marker=y_label, s=320)
    
def main():
    colors1 = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']
    colors2 = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
    X_data1, X_orig1, y_labels1, y1 = Load_handdetection_dataset()
    X_data2, X_orig2, y_labels2, y2 = Load_mnist_dataset()
	
    X_data1_tsne, time1 = Train_tsne(X_data1)
    print("t-SNE for hand gesture dataset:\ntime:{} sec".format(time1))
    fig1, ax1 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig1, X_data1, X_data1_tsne, ax1, mnistdata=False)
    Draw_datasamples_to_figure(X_data1_tsne, y_labels1, y1, colors1)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the hand gesture dataset using t-SNE', fontsize=96)
    Evaluation(X_data1_tsne, y1)
    
    X_data1_PCA, time2 = Train_PCA(X_data1)
    print("PCA for hand gesture dataset:\ntime:{} sec".format(time2))
    fig2, ax2 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig1, X_data1, X_data1_PCA, ax2, mnistdata=False)
    Draw_datasamples_to_figure(X_data1_PCA, y_labels1, y1, colors1)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the hand gesture dataset using PCA', fontsize=96)
    Evaluation(X_data1_PCA, y1)
	
    X_data1_MDS, time3 = Train_MDS(X_data1)
    print("MDS for hand gesture dataset:\ntime:{} sec".format(time3))
    fig3, ax3 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig1, X_data1, X_data1_MDS, ax3, mnistdata=False)
    Draw_datasamples_to_figure(X_data1_MDS, y_labels1, y1, colors1)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the hand gesture dataset using MDS', fontsize=96)
    Evaluation(X_data1_MDS, y1)
	
    X_data2_tsne, time4 = Train_tsne(X_data2)
    print("t-SNE for MNIST:\ntime:{} sec".format(time4))
    fig4, ax4 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig2, X_data2, X_data2_tsne, ax4, mnistdata=True)
    Draw_datasamples_to_figure(X_data2_tsne, y_labels2, y2, colors2)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the MNIST dataset using t-SNE', fontsize=96)
    Evaluation(X_data2_tsne, y2)
	
    X_data2_PCA, time5 = Train_PCA(X_data2)
    print("PCA for MNIST:\ntime:{} sec".format(time5))
    fig5, ax5 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig2, X_data2, X_data2_PCA, ax5, mnistdata=True)
    Draw_datasamples_to_figure(X_data2_PCA, y_labels2, y2, colors2)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the MNIST dataset using PCA', fontsize=96)
    Evaluation(X_data2_PCA, y2)
	
    X_data2_MDS, time6 = Train_MDS(X_data2)
    print("MDS for MNIST:\ntime:{} sec".format(time6))
    fig6, ax6 = plt.subplots(figsize=(150, 100),dpi=40)
    Draw_example_pictures_to_figure(X_orig2, X_data2, X_data2_MDS, ax6, mnistdata=True)
    Draw_datasamples_to_figure(X_data2_MDS, y_labels2, y2, colors2)
    plt.xticks([]), plt.yticks([])
    plt.title('2-D visualization of the MNIST dataset using MDS', fontsize=96)
    Evaluation(X_data2_MDS, y2)

    plt.show()

if __name__ == '__main__':
    main()