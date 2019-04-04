import numpy as np
from computeLength import computeLength
from genLineLoc import genLineLoc
from math import floor

def genPaperScrn(corners, resolution, perspective_ratio, frame_height):

	# get the length of the user defined side
	length_AB = computeLength(corners[0],corners[1])
	length_BC = computeLength(corners[1],corners[2])
	length_CD = computeLength(corners[2],corners[3])
	length_AD = computeLength(corners[3],corners[0])

	# the shorter side will define how large the normalize matrix is,
	# then divide width & hieight with the predefined resolution value
	width = floor(min(length_AB,length_CD)/resolution)
	height = floor(min(length_BC,length_AD)/resolution)
	
	# define normalize matrix size
	mat = np.zeros((height,width,4))

	# fill in the first and last row of the normalize matrix
	nptemp = genLineLoc(corners[0], corners[1], width)
	nptemp = nptemp.T
	mat[0,:,0] = nptemp[0,:]
	mat[0,:,1] = nptemp[1,:]
	nptemp = genLineLoc(corners[3], corners[2], width)
	nptemp = nptemp.T
	mat[(height-1),:,0] = nptemp[0,:]
	mat[(height-1),:,1] = nptemp[1,:]

	# using the value of first as last row as two point, 
	# fill in the remaining col
	for step in range(width):
		nptemp = genLineLoc((mat[0,step,0],mat[0,step,1]), (mat[height-1,step,0],mat[height-1,step,1]), height)
		mat[:,step,0] = nptemp[:,0]
		mat[:,step,1] = nptemp[:,1]

	# defined stretched normalize matrix size
	# (this matrix define the location on the paper)
	npadder = np.linspace(0, perspective_ratio, frame_height)

	# fill in x values of the stretched matrix
	xtemp = [range(width)] * height
	xtemp = np.array(xtemp)
	mat[:,:,2] = xtemp

	# fill in y-values of the stretched matrix
	for step in range(width):
		start = round(mat[0,step,1])
		if start >= height:
			par_npadder = npadder[int(start-height):int(start)]
		else:
			par_npadder = npadder[0:int(height)]
		mat[:,step,3] = np.array(range(height)) + par_npadder

	return mat