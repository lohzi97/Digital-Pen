#!/usr/bin/env python3

from gpiozero import Button, LED
from signal import pause

#======================================================
# pin and parameter setup
#======================================================

BTN_MODE = 26
LED_MODE_PEN = 13
LED_MODE_MOUSE = 19

#======================================================
# Functions
#======================================================

# toggle the value in the mode.txt file 
def changeMode():
    
    # open and read file.
    file = open('mode.txt', 'r+')
    mode = file.read()

    # if current value is 1, then overwrite it to 2,
    # and turn on mouse mode LED.
    if mode == "1":
        file.seek(0)
        file.write("2")
        led_mode_pen.off()
        led_mode_mouse.on()
    
    # if current value is 2, then overwrite it to 1,
    # and turn on the pen mode LED
    elif mode == "2":
        file.seek(0)
        file.write("1")
        led_mode_pen.on()
        led_mode_mouse.off()

    # truncate it and close the file.
    file.truncate()
    file.close()

# get the current mode. 
def initialMode():

    # open and read file.
    file = open('mode.txt', 'r')
    mode = file.read()

    # if mode is 1, then turn on pen mode LED
    if mode == "1":
        led_mode_pen.on()
        led_mode_mouse.off()

    # if mode is 2, then turn on mouse mode LED
    if mode == "2":
        led_mode_pen.off()
        led_mode_mouse.on()

    # close the file
    file.close()

#======================================================
# Main Program
#======================================================

print("Getting previous mode...")

# create LED and Button object 
led_mode_pen = LED(LED_MODE_PEN)
led_mode_mouse = LED(LED_MODE_MOUSE)
btn_mode = Button(BTN_MODE)

# get the current mode.
initialMode()

# if the button is pressed, change the mode.
btn_mode.when_pressed = changeMode

# let the program pause so that it can continuously run at background.
pause()
