import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def main():
    width, height = 1280, 720
    folderPath = "Presentation"

    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Get the list of presentation images
    pathImages = sorted(os.listdir(folderPath), key=len)
    print(pathImages)
    # Variables
    imgNumber = 0
    hs, ws = int(120 * 1), int(213 * 1)
    gestureThreshold = 300
    buttonPressed = False
    buttonCounter = 0
    buttonDelay = 30
    annotations = [[]]
    annotationNumber = -1
    annotationStart = False

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:
        # Import Images
        success, img = cap.read()
        img = cv2.flip(img, 1)

        pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
        imgCurrent = cv2.imread(pathFullImage)

        hands, img = detector.findHands(img)
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
        print(annotationNumber)
        if hands and not buttonPressed:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']

            # Constrain values for easier drawing
            indexFinger = lmList[8][0], lmList[8][1]
            xVal = int(np.interp(lmList[8][0], [width // 2, ws], [0, width]))
            yVal = int(np.interp(lmList[8][0], [150, height - 150], [0, height]))
            indexFinger = xVal, yVal

            if cy <= gestureThreshold:  # if hand is at the height of the face
                annotationStart = False
                # Gesture 1 - Left
                if fingers == [0, 1, 1, 0, 0]:
                    annotationStart = False
                    print("Left")
                    if imgNumber > 0:
                        buttonPressed = True
                        annotations = [[]]
                        annotationNumber = -1
                        imgNumber -= 1

                # Gesture 2 - Right
                if fingers == [0, 0, 1, 1, 0]:
                    annotationStart = False
                    print("Right")
                    if imgNumber < len(pathImages) - 1:
                        buttonPressed = True
                        annotations = [[]]
                        annotationNumber = -1
                        imgNumber += 1
                     # Gesture 3 - Exit
                if fingers == [1, 0, 0, 0, 0]:
                    annotationStart = False
                    break
                   # cap.release()

        # Button Pressed iterations
        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False

        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)

        # Adding webcam image on the slides
        imgSmall = cv2.resize(img, (ws, hs))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:hs, w - ws:w] = imgSmall
        cv2.imshow("Image", img)
        cv2.imshow("Slides", imgCurrent)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

if __name__ == "__main__":
    main()


#this is the final class of ppt viewer and slides vala code runs properly