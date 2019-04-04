import numpy as np
from math import ceil

def genBuffer(mat):
	
	# get the height and width of the paper/screen
	w = mat[mat.shape[0]-1,mat.shape[1]-1,2]
	h = mat[mat.shape[0]-1,mat.shape[1]-1,3]

	# generate the paper/screen buffer
	return np.ones((ceil(h),ceil(w)),dtype=np.uint8)*255