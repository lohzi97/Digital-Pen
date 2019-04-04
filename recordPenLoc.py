import cv2

def recordPenLoc(X, Y, penRadius, paperBuffer):
	#paperBuffer[X,Y] = 0
	return cv2.circle(paperBuffer,(X, Y), penRadius, (0,0,0))