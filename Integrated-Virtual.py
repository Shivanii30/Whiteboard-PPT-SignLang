# Slides.py

import cv2
import whiteboard
import Slides
import sign_language

def main():
    # Initialize virtual whiteboard
    whiteboard.main()

    # Initialize PowerPoint viewer
    Slides.main()

    # Initialize sign language recognition
    sign_language.main()

if __name__ == "__main__":
    main()
