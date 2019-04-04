#!/usr/bin/env python3

from gpiozero import Button, LED
from signal import pause
import os, sys

#======================================================
# pin and parameter setup
#======================================================

offGPIO = 17
holdTime = 3
ledGPIO = 27

#======================================================
# Functions
#======================================================

def when_pressed():

    # start blinking with 1/2 second rate
    led.blink(on_time=0.5, off_time=0.5)

def when_released():

    # be sure to turn the LEDs back on if we release early
    led.on()

def shutdown():

    os.system("sudo poweroff")

#======================================================
# main program
#======================================================

# craete LED and button object.
led = LED(ledGPIO)
btn = Button(offGPIO, hold_time=holdTime)

# light up LED when this program run，to indicate raspberry pi started.
led.on()

# set event for button.
btn.when_held = shutdown
btn.when_pressed = when_pressed
btn.when_released = when_released

# let the program pause so that it can continuously run at background.
pause()
