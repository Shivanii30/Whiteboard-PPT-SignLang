import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class PresentationViewer:
    def __init__(self, folder_path="Presentation", detection_con=0.8, max_hands=1):
        self.folder_path = folder_path
        self.detector = HandDetector(detectionCon=detection_con, maxHands=max_hands)
        self.width, self.height = 1280, 720
        self.hs, self.ws = int(120 * 1), int(213 * 1)
        self.gesture_threshold = 300
        self.annotations = [[]]
        self.annotation_number = -1
        self.annotation_start = False
        self.img_number = 0
        self.button_pressed = False
        self.button_counter = 0
        self.button_delay = 30

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, self.width)
        cap.set(4, self.height)

        path_images = sorted(os.listdir(self.folder_path), key=len)

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)

            path_full_image = os.path.join(self.folder_path, path_images[self.img_number])
            img_current = cv2.imread(path_full_image)

            hands, img = self.detector.findHands(img)
            cv2.line(img, (0, self.gesture_threshold), (self.width, self.gesture_threshold), (0, 255, 0), 10)

            if hands and not self.button_pressed:
                hand = hands[0]
                fingers = self.detector.fingersUp(hand)
                cy = hand['center'][1]

                if cy <= self.gesture_threshold:  # if hand is at the height of the face
                    self.annotation_start = False
                    # Gesture 1 - Left
                    if fingers == [0, 1, 1, 0, 0]:
                        self.annotation_start = False
                        print("Left")
                        if self.img_number > 0:
                            self.button_pressed = True
                            self.annotations = [[]]
                            self.annotation_number = -1
                            self.img_number -= 1

                    # Gesture 2 - Right
                    if fingers == [0, 0, 1, 1, 0]:
                        self.annotation_start = False
                        print("Right")
                        if self.img_number < len(path_images) - 1:
                            self.button_pressed = True
                            self.annotations = [[]]
                            self.annotation_number = -1
                            self.img_number += 1

                    # Gesture 3 - Exit
                    if fingers == [1, 0, 0, 0, 0]:
                        return True # Exit presentation viewer

            # Button Pressed iterations
            if self.button_pressed:
                self.button_counter += 1
                if self.button_counter > self.button_delay:
                    self.button_counter = 0
                    self.button_pressed = False

            for i in range(len(self.annotations)):
                for j in range(len(self.annotations[i])):
                    if j != 0:
                        cv2.line(img_current, self.annotations[i][j - 1], self.annotations[i][j], (0, 0, 200), 12)

            # Adding webcam image on the slides
            img_small = cv2.resize(img, (self.ws, self.hs))
            h, w, _ = img_current.shape
            img_current[0:self.hs, w - self.ws:w] = img_small
            cv2.imshow("Image", img)
            cv2.imshow("Slides", img_current)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                return False # Exit presentation viewer

if __name__ == "__main__":
    presentation_viewer = PresentationViewer()
    presentation_viewer.run()
