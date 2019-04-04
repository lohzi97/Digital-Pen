print("Started...")

# import the required modules/files
import cv2
import numpy as np
import time
from bluetooth import *
import os
from gpiozero import Button, LED

from getCorners import getCorners
from genPaperScrn import genPaperScrn
from genBuffer import genBuffer
from getPaperCoor import getPaperCoor
import LEDindicator
from readMode import readMode

#======================================================
# pin setup
#======================================================

LED_1 = 22
LED_2 = 10
LED_3 = 9
LED_4 = 11

#======================================================
# parameters to tweak
#======================================================
penRadius = 1
eraserRadius = 4
resolution = 1 # pixel/mm (this means 1 pixel = 1 mm on paper)
perspective_ratio = 3 # how many near pixel will equalvalent to far pixel (quite difficult to explain)
hold_time = 0.3

#======================================================
# DIGITAL PEN PROGRAM
#======================================================

# object setup
led_1 = LED(LED_1)
led_2 = LED(LED_2)
led_3 = LED(LED_3)
led_4 = LED(LED_4)

# bluetooth setup.
port = 1
HC06_addr = '00:18:E5:04:15:74'
connect = False

# LED pattern to indicate searching...
print("Searching for Pen...")
LEDindicator.bluetoothScan(led_1, led_2, led_3, led_4)

# find and connect to the HC06 bluetooth module
while True:

    # scan nearby devices
    nearby_devices = discover_devices(duration=8,lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        if name == "HC-06" and addr == HC06_addr:
            
            try:
                sock = BluetoothSocket(RFCOMM)
                sock.connect((HC06_addr, port))
                sock.setblocking(0)
            except:
                LEDindicator.bluetoothFailed(led_1, led_2, led_3, led_4)
                print("Unable to connect to Pen... ")
                sock.close()
            else:
                LEDindicator.bluetoothConnected(led_1, led_2, led_3, led_4)
                print("Connected...")
                connect = True
                break

    if connect:
        break

# start the camera
cap = cv2.VideoCapture(0)

try:
    while True:

        # get the corner of the paper/screen
        print("Locating paper/screen corners...")
        corners = getCorners(cap, sock, led_1, led_2, led_3, led_4)

        # generate the actual paper/screen
        # (because of the camera viewing perspective, stretching out the corners is required)
        paperScrnMat = genPaperScrn(corners, resolution, perspective_ratio, cap.get(4))

        # set the paper buffer
        # (use for storing current Note's page)
        paperBuffer = genBuffer(paperScrnMat)
        paperBufferCopy = np.copy(paperBuffer)

        # initialize previous coordinate variable
        # (use for linking 2 dot together during continuous writing)
        prev_coor = None

        # initialize time variable
        # (use to detect if user is writing with one stroke or separate stroke)
        w_time = None

        # set flag and counter for file name
        dateTime = time.gmtime()
        pref = str(dateTime[0]) + str(dateTime[1]) + str(dateTime[2]) + "-" + str(dateTime[3]) + str(dateTime[4]) + str(dateTime[5])
        num_file = 1
        path = '/home/pi/notes'

        LEDindicator.started(led_1, led_2, led_3, led_4)
        print("Recording pen movement...")

        while True:

            try:
                # convert the pen location in camera into paper coordinates
                X, Y = getPaperCoor(cap, paperScrnMat)
                print("(" + str(X) + ", " + str(Y) + ")")

                # read the button pressed command from Pen.
                pen_mode = sock.recv(1024)
                print(pen_mode[0])

            except KeyboardInterrupt:
                cap.release()
                exit()
            except:
                continue

            # check for mode, whether is "note taking" or "computer mouse"
            # this depends on the button on rpi. 
            mode = readMode()
            print("mode: " + mode)

            if X != 0 and Y != 0:

                # for notes taking mode:
                if mode == "1":
            
                    X = int(round(X))
                    Y = int(round(Y))

                    # write mode:
                    if pen_mode[0] == 49:
                        print("marked.")
                        cv2.circle(paperBuffer,(X, Y), penRadius, (0,0,0), -1)
                        if w_time is not None and time.time() - w_time > hold_time:
                            prev_coor = None
                        if prev_coor is not None:
                            cv2.line(paperBuffer,(X, Y), prev_coor, (0,0,0), penRadius*2)
                        prev_coor = (X, Y)
                        w_time = time.time()

                    # erase mode:
                    elif pen_mode[0] == 50:
                        print("deleted.")
                        cv2.circle(paperBuffer,(X, Y), eraserRadius, (255,255,255), -1)

                    # save current page:
                    elif pen_mode[0] == 51:
                        print("saved")
                        filename = pref + "_" + str(num_file) + ".png"
                        cv2.imwrite(os.path.join(path, filename),paperBuffer)
                        time.sleep(1)

                    # next page:
                    elif pen_mode[0] == 52:
                        print("new page.")
                        filename = pref + "_" + str(num_file) + ".png"
                        cv2.imwrite(os.path.join(path, filename),paperBuffer)
                        paperBuffer = np.copy(paperBufferCopy)
                        num_file += 1
                        time.sleep(2)

                    #cv2.imshow("paperBuffer", paperBuffer)
                    #cv2.waitKey(50)

                # for computer touchscreen-mouse mode:
                elif mode == "2":

                    print("do something")
            
            else:
                print("Pen is not in range...")

            ## reset program:
            #if keyboard.is_pressed('r'):
            #    break

            ## exit program:
            ## (save and shutdown rpi)
            #elif keyboard.is_pressed('q'):
            #    cap.release()
            #    cv2.destroyAllWindows()
            #    exit()
except:
    cap.release()
    exit()
