#!/usr/bin/python

import RPi.GPIO as GPIO

import time

import picamera

import datetime

import subprocess

import dropbox

import os

import sms

# Get your app key and secret from the Dropbox developer website

app_key = 'dropbox key'

app_secret = 'secret key'

def getFileName():

    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def dropboxAuth():

    accessTokenFileOverwrite = open("accessToken.txt", "w+")

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key,app_secret)

    authorize_url = flow.start()

    # Have the user sign in and authorize this token

    authorize_url = flow.start()

    print '1. Go to: ' + authorize_url

    print '2. Click "Allow" (you might have to log in first)'

    print '3. Copy the authorization code'

    code = raw_input("Enter the authorization code here: ").strip()
    
    try:

    # This will fail if the user enters an invalid authorization code

        access_token, user_id = flow.finish(code)

        accessTokenFileOverwrite.write(access_token)

    except:

        print "failed authorization, restart"

        accessTokenFileOverwrite.close()

        os.remove("accessToken.txt")

    accessTokenFileOverwrite.close()

def dropboxUpload(fileToUpload):

    if not os.path.isfile("accessToken.txt"):

        dropboxAuth()

    #get access token from file

    accessTokenFileRead = open("accessToken.txt", "r")

    access_token = accessTokenFileRead.read()

    accessTokenFileRead.close()

    # make client

    client = dropbox.client.DropboxClient(access_token)

    #upload file

    fileToUploadObject = open(fileToUpload, "rb")

    response = client.put_file(fileToUpload, fileToUploadObject)

    fileToUploadObject.close()

sensorPin = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False

currState = False

cam = picamera.PiCamera()

while True:

    time.sleep(0.1)

    prevState = currState

    currState = GPIO.input(sensorPin)

    if currState != prevState:

        newState = "HIGH" if currState else "LOW"

        print "PIO pin %s is %s" % (sensorPin, newState)

        if currState:

            print "A MOTION HAS BEEN DETECTED !!!"

            fileName = getFileName()

            print "Starting Recording..."

            cam.start_preview()

            cam.start_recording(fileName)

            print (fileName)

        else:

            print "MOTION STOPPED"

            cam.stop_preview()

            cam.stop_recording()

            print "Stopped Recording"

            print "Sending Mail Notification..."

            subprocess.call("mail -s 'Motion Detected' abc@gmail.com < /home/pi/message.txt", shell=True)

            print "Complete"

            print "Uploading the footage to Dropbox..."

            dropboxUpload(fileName)

            print "Complete"

            print "Sending SMS Notification..."

            sms.sendSMS('xxxxxxxxxx')

            sms.sendSMS('xxxxxxxxxx')

            subprocess.call("mail -s 'Motion Detected' xyz@gmail.com < /home/pi/message.txt", shell=True)

            print "Complete"

            print "SMS Notification generally takes upto 1-2 minutes"

            print "But Sometimes due to heavy newtork traffic it can take upto 10 mins"
