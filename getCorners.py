from processCamFrame import processCamFrame
import time

def getCorners(cap, sock, led_1, led_2, led_3, led_4):
	
	# initialize the corners variables
	corners = []
	start_time = None

	led_1.blink(on_time=0.35, off_time=0.35)

	while True:

		try:
			
			# read video frame
			_, frame = cap.read()

			# get the current white blob centroid
			cX, cY = processCamFrame(frame)

			print("centroid: "+ str(cX) + ", " + str(cY))

			pen_mode = sock.recv(1024)
			print(pen_mode[0])

		except KeyboardInterrupt:
			cap.release()
			exit()

		except:
			continue			
		

		# read bluetooth data the send from the pen, 
		# if "write" button is pressed, then save the current pen location. 
		if pen_mode[0] == 49:
			if cX != 0 and cY != 0:

				# check if the "write" button is press.
				debounce = 0.5
				if start_time is None:
					start_time = time.time()
					corners.append((cX, cY))
					led_1.on()
					led_2.blink(on_time=0.35, off_time=0.35)
					print("corner: " + str(corners))
				elif time.time() - start_time > debounce:
					corners.append((cX, cY))
					if len(corners) == 1:
						led_1.on()
						led_2.blink(on_time=0.35, off_time=0.35)
					elif len(corners) == 2:
						led_2.on()
						led_3.blink(on_time=0.35, off_time=0.35)
					elif len(corners) == 3:
						led_3.on()
						led_4.blink(on_time=0.35, off_time=0.35)
					print("corner: " + str(corners))
					start_time = time.time()

		elif pen_mode[0] == 50:
			if len(corners) == 1:
				corners.pop()
				led_1.blink(on_time=0.35, off_time=0.35)
				led_2.off()
			elif len(corners) == 2:
				corners.pop()
				led_2.blink(on_time=0.35, off_time=0.35)
				led_3.off()
			elif len(corners) == 3:
				corners.pop()
				led_3.blink(on_time=0.35, off_time=0.35)
				led_4.off()
			print("corner: " + str(corners))

		if len(corners)>=4:
			led_4.on()
			break

		cX = 0
		cY = 0

	return corners
