import cv2
import numpy as np
import glob
import pickle
import os

def callback(x):
    pass

filelist = glob.glob('inputimages/*.jpg')
filelist.sort()
cv2.namedWindow('HSV')
# Luodaan säätöikkunat väriarvojen säätämiseksi
cv2.createTrackbar('MinH','HSV',360,360, callback)   # Muokkaa rivien 14-19 cv2.createTrackbar() kolmansia argumentteja löydettyäsi sopivat HSV-värimallin vaihteluvälit
cv2.createTrackbar('MaxH','HSV',26,360, callback)
cv2.createTrackbar('MinS','HSV',114,255, callback)
cv2.createTrackbar('MaxS','HSV',248,255, callback)
cv2.createTrackbar('MinV','HSV',16,255, callback)
cv2.createTrackbar('MaxV','HSV',152,255, callback)
counter1 = 0
counter2 = 0
counter3= 0
counter4 = 0
counter5 = 0
counter6 = 0
for filename in filelist:
    if filename[19]=="1":  
        counter1 +=1
        currentcount = counter1
    elif filename[19]=="2":
        counter2 +=1
        currentcount = counter2
    elif filename[19]=="3":
        counter3 +=1
        currentcount = counter3
    elif filename[19]=="4":
        counter4 +=1
        currentcount = counter4
    elif filename[19]=="5":
        counter5 +=1
        currentcount = counter5
    elif filename[19]=="6":
        counter6 +=1
        currentcount = counter6  
    # Muutetaan kuvan kokoa
    im = cv2.imread(filename) 
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
    ret,thresh = cv2.threshold(median,120,255,0)
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
    cv2.rectangle(im, (x1,y1),(x1+w1,y1+h1), (0,255,0), 3)
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
    # Muutetaan muunnetun kuvan kokoa
    cropped_image = cv2.resize(cropped_image, (100, 150))
    outputfilename = "outputimages/gesture{}_{}.bmp".format(filename[19], currentcount)
    cv2.imwrite(outputfilename, cropped_image)
cv2.destroyAllWindows()

