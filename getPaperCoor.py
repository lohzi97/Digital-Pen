from processCamFrame import processCamFrame
import numpy as np

def getPaperCoor(cap, paperScrnMat):

	# read video frame
	_, frame = cap.read()
	
	# get the current white blob centroid
	cX, cY = processCamFrame(frame)

	if cX == 0 and cY == 0:
		return (0,0)
	else:
		# find the nearest point that can be mapped to
		dist_mat = ((cX - paperScrnMat[:,:,0])**2 + (cY - paperScrnMat[:,:,1])**2)**(1/2)
		min_idx = np.where(dist_mat==dist_mat.min())
		min_idx_x = min_idx[0][0]
		min_idx_y = min_idx[1][0]

		# from the paperScrnMat 3rd and 4th dimension, find the actual location of pen on paper
		X = paperScrnMat[min_idx_x,min_idx_y,2]
		Y = paperScrnMat[min_idx_x,min_idx_y,3]

		return (X, Y)
