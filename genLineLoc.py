import numpy as np

def genLineLoc(p1,p2,length):

	# find how many pixel represent every mm
	unit_x = abs((p1[0]-p2[0])/length)
	unit_y = abs((p1[1]-p2[1])/length)

	# this is the loc array that will be returned.
	loc = []

	# the first point in the line is just the first point.	
	loc.append(p1)

	# here set some flag on whether the x-axis and y-axis of the 
	# next point should add/sub the unit_x/unit_y with current point value.
	if p1[0]>p2[0]:
		flag_x = 's'
	else:
		flag_x = 'a'

	if p1[1]>p2[1]:
		flag_y = 's'
	else:
		flag_y = 'a'

	# complete the loc array
	for step in range(1,length):
		if flag_x == 's':
			x= loc[step-1][0] - unit_x
		else:
			x = loc[step-1][0] + unit_x
		if flag_y =='s':
			y = loc[step-1][1] - unit_y
		else:
			y = loc[step-1][1] + unit_y
		loc.append((x,y))

	return np.array(loc)