#!/usr/bin/python

import RPi.GPIO as GPIO

import time

sensorPin = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False

currState = False

while True:

    time.sleep(0.1)

    prevState = currState

    currState = GPIO.input(sensorPin)

    if currState != prevState:

        newState = "HIGH" if currState else "LOW"

        print "GPIO pin %s is %s" % (sensorPin, newState)
