from tkinter import filedialog
import cv2
import numpy as np


prompt = filedialog.askopenfilename(initialdir="C:\\Users\\joswa\\Desktop\\Email Apps\\Complete Casscades")
#prompt = str(input("What image?: "))
cameraNo = 0
objectName = str(input("Object name: "))
frameWidth = 640
frameHeight = 480
color = (100,0,45)

cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

#Trackbar
cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight+100)
cv2.createTrackbar("Scale", "Result", 400,1000, empty)
cv2.createTrackbar("Neighbor", "Result", 8,20, empty)
cv2.createTrackbar("Min-Area", "Result", 0,1000000, empty)
cv2.createTrackbar("Brightness", "Result", 180,255, empty)



#image = cv2.imread(prompt)
#resize = cv2.resize(image, (1080,1080))
#Load Cascade
cascade = cv2.CascadeClassifier(f'{prompt}')

while True:
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)

    #Get image and convert to grayscale
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Object detection
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result")/1000)
    neighbor = cv2.getTrackbarPos("Neighbor", "Result")
    objects = cascade.detectMultiScale(gray, scaleVal, neighbor, minSize =(24,24))
    threshold = .8
    #Display Detections
    for (x,y,w,h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min-Area", "Result")
        if area > minArea:
            if area>threshold:
                #cv2.rectangle(img,(x,y), (x+w,y+h), color, 3)
                cv2.circle(img,(x,y), 5, (255,20,100), 2)
                cv2.putText(img, objectName, (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,color,2)
                roi_color = img[y:y+h, x:x+w]
    cv2.imshow("Result", img)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

