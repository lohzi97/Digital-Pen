import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if ret:

        print("got something...")

        cv2.imshow('frame', frame)

        

    else:

        print("nothing...")

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break


cap.release()

cv2.destroyAllWindows()

