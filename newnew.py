import cv2
import numpy as np
import time
import os
import handtracking as htm


folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
header = overlayList[0]

cap = cv2.VideoCapture(1)
cap.set(3,1288)
cap.set(4,728)

while True:
    #import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # setting the header image
    #img[0:125, 0:1280] = header
    cv2.imshow("Image",img)
    cv2.waitKey(1)





