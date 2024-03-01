import threading
import cv2
import numpy as np
import time
import os
import handtracking as htm
import SlidesClass
import SignClass
import threading
import WhiteboardClass
import os

brushThickness = 15

folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
save = False

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)
eraserthickness = 60

cap = cv2.VideoCapture(0)
cap.set(3, 1288)
cap.set(4, 728)

detector = htm.handDetector(detectionCon=0.85, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)


def slides_thread():
    SlidesClass.main()


def sign_thread():
    SignClass.main()


while True:
    # import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find hand landmarks
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if lmlist is not None:
        if len(lmlist) != 0:
            print(lmlist)
        # tip of index and middle fingers
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If selection mode -2 else 1
        if fingers[1] and fingers[2]:
            print("Selection")
            # checking for the click
            if y1 < 125:
                if 180 < x1 < 400:
                    header = overlayList[0]
                    drawColor = (147, 20, 255)  # purplish colour
                elif 405 < x1 < 580:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)  # blue
                elif 590 < x1 < 700:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)  # green
                elif 720 < x1 < 820:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
                # subprocess.run(["python",])
                elif 880 < x1 < 1020:
                    header = overlayList[4]
                    SlidesClass.main()
                    WhiteboardClass.main()
                    #presentation_viewer_instance = presentation_viewer.PresentationViewer()
                   # presentation_closed = presentation_viewer_instance.run()
#if presentation_closed:
                        #cv2.VideoCapture(0)
                        #continue
                    # SlidesClass.main()
                elif 1040 < x1 < 1190:
                    header = overlayList[5]
                    SignClass.main()

        # cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        # 5 If Drawing Mode - Index Finger is up

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserthickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)  # will draw in black
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    # to binary image
    if imgInv is not None:
        imgInv = cv2.resize(imgInv, (img.shape[1], img.shape[0]))
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    else:
        print("Error : None")
   # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)



    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # setting the header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    k = cv2.waitKey(1)

    if k == ord('s') or k == ord('S'):
        save = True

    if save:
        save = False
        current_time = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"canvas_{current_time}.jpg"
        cv2.imwrite(file_name, imgCanvas)
        print("File  Saved ")
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# this is the final project integrated
