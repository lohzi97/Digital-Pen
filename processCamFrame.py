import cv2

def processCamFrame(frame):

	# convert BGR into grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# convert grayscale into binary 
	# (set 254 as threshold value, any pixel higher than this will be converted to 255, else 0)
	retval, threshold = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

	# calculate centriod
	M = cv2.moments(threshold)
	if M["m00"] != 0:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	else:
		cX = 0
		cY = 0

	# draw the centriod out
	# (for debugggin prupose)
	#cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)
	#cv2.imshow('frame',frame)
	#cv2.waitKey(50)

	return [cX, cY]
