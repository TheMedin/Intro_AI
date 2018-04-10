import cv2
import numpy as np
import argparse as ap
from sklearn.externals import joblib
from skimage.feature import hog
import glob

def callback(x):
    pass

def log_function(values):
    return np.log(np.abs(values))*np.sign(values)

if __name__=='__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("-c", "--classiferPath", help="Path to Classifier File", required="True")
    args = vars(parser.parse_args())
    # Ladtaan luokittelija
    clf, pp = joblib.load(args["classiferPath"])
    cv2.namedWindow('HSV')
    cv2.resizeWindow('HSV', 300,400)
    # Luodaan säätöikkunat väriarvojen säätämiseksi
    cv2.createTrackbar('MinH','HSV',255,255, callback)  # Muokkaa rivien 23-28 cv2.createTrackbar() kolmansia argumentteja löydettyäsi sopivat HSV-värimallin vaihteluvälit
    cv2.createTrackbar('MaxH','HSV',18,255, callback)
    cv2.createTrackbar('MinS','HSV',114,255, callback)
    cv2.createTrackbar('MaxS','HSV',248,255, callback)
    cv2.createTrackbar('MinV','HSV',16,255, callback)
    cv2.createTrackbar('MaxV','HSV',152,255, callback)
    filelist = glob.glob('testimages/*')
    while True:
        for j in range(len(filelist)):
            # Muutetaan kuvan kokoa
            im = cv2.imread(filelist[j]) 
            im = cv2.resize(im,(320,480))
            # Otetaan ylös alustettu arvo kuudelle värien säätämismuutujalle
            MinH = cv2.getTrackbarPos('MinH','HSV')
            MaxH = cv2.getTrackbarPos('MaxH','HSV')
            MinS = cv2.getTrackbarPos('MinS','HSV')
            MaxS = cv2.getTrackbarPos('MaxS','HSV')
            MinV = cv2.getTrackbarPos('MinV','HSV')
            MaxV = cv2.getTrackbarPos('MaxV','HSV')
            # Sumennetaan kuvaa
            blur = cv2.blur(im,(3,3))
            # Toteutetaan bgr-hsv muunnos ja AND operaatio
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            lower = np.array([0, MinS, MinV])
            upper = np.array([MaxH, MaxS, MaxV])
            mask2 = cv2.inRange(hsv,lower,upper)
            lower1 = np.array([MinH, MinS, MinV])
            upper1 = np.array([255, MaxS, MaxV])
            mask1 = cv2.inRange(hsv,lower1,upper1)
            mask = cv2.bitwise_or(mask1,mask2)        
            # Toteutetaan morfologisia operaatioita suodattaakseen pois taustakohina    
            kernel_square = np.ones((11,11),np.uint8)
            kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            dilation = cv2.dilate(mask,kernel_ellipse,iterations = 1)
            erosion = cv2.erode(dilation,kernel_square,iterations = 1)    
            dilation2 = cv2.dilate(erosion,kernel_ellipse,iterations = 1)    
            filtered = cv2.medianBlur(dilation2,5)
            kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
            dilation2 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
            kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            dilation3 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
            median = cv2.medianBlur(dilation2,5)
            ret,thresh = cv2.threshold(filtered,127,255,0)
            im2, contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            max_area=100
            ci=0	
            for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
            # Kuvan suurin alue   	  
            cnts = contours[ci]
            rect = cv2.boundingRect(cnts)
            x1,y1,w1,h1 = rect
            # Selvitään kämmenen keskipiste
            maxdistance=0
            pt=(0,0)
            for index_y in range(int(y1+0.1*h1),int(y1+0.8*h1)):
                for index_x in range(int(x1+0.1*w1),int(x1+0.8*w1)):
                    distance=cv2.pointPolygonTest(cnts,(index_x,index_y), True)
                    if(distance>maxdistance):
                        maxdistance=distance
                        pt = (index_x,index_y)
            radius = int(maxdistance)
            cv2.circle(im,pt,radius,(255,0,0),2)
            cv2.rectangle(im, (x1,y1),(x1+w1,pt[1]+radius), (0,0,255), 3)
            cropped_image = thresh[y1-10:pt[1]+radius,x1-10:x1+w1+10]
            # Lasketaan Hu moment invariantit
            roi = cv2.resize(cropped_image, (320, 480), interpolation=cv2.INTER_AREA)
            humoments = log_function(cv2.HuMoments(cv2.moments(roi)).flatten())
            humoments = pp.transform(np.array([humoments], 'float64'))
            nbr = clf.predict(humoments)
            cv2.putText(im, str(nbr[0]), (x1,y1),cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 3)
            cv2.imshow('Output{}'.format(j), im)
            c= cv2.waitKey(5)
        if c==27:
            break
    cv2.destroyAllWindows()


