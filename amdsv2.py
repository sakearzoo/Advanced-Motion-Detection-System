#!/usr/bin/python
#https://github.com/sakearzoo
#https://github.com/abhisheksarkar30
#By Sheikh Nawab Arzoo & Abhishek Sarkar
import RPi.GPIO as GPIO
import time
import picamera
import datetime
import subprocess
import dropbox
import os
import sms
import logging
import signal
import sys
import MFRC522

LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(filename='amdsv2.log', format=LOG_FORMAT, level=logging.INFO)
# Get your app key and secret from the Dropbox developer website
app_key = '*******'    // enter your app here from dropbox
app_secret = '*******' // enter your secret key from dropbox
logging.info("Automated System started!")

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    print "Ctrl+C captured, ending read."
    logging.warning("Automated System terminated!")
    GPIO.cleanup();
    sys.exit(1);

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

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
num1='*********' //enter the 1st number here
num2='*********' //enter the 2nd number here
msg_warn='Motion Detected!!! Get video @ https://www.dropbox.com/home/Apps/ \nFrom PI'
msg_prob='Problem occurred in AMDSv2! Check Log for details!\nFrom PI'
db=[[0x01,0x02],["Abhishek","Arzoo"]]
count=0

while True:
	time.sleep(0.1)
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	(status,uid) = MIFAREReader.MFRC522_Anticoll()
	read=[]
	if status == MIFAREReader.MI_OK:
		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		MIFAREReader.MFRC522_SelectTag(uid)
		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
		if status == MIFAREReader.MI_OK:
			read=MIFAREReader.MFRC522_Read(8)
			if read[0] in db[0]:
				if read[1]==0:
					count+=1
					logging.info("%s entered! %s" %(db[1][db[0].index(read[0])],"Script Paused!" if count==1 else ""))
					print "%s entered! %s" %(db[1][db[0].index(read[0])],"Script Paused!" if count==1 else "")
				else:
					count-=1
					logging.info("%s exited! %s" % (db[1][db[0].index(read[0])],"Script Resumed!" if count==0 else ""))
					print "%s exited! %s" % (db[1][db[0].index(read[0])],"Script Resumed!" if count==0 else "")
				read[1]=1 if read[1]==0 else 0
				MIFAREReader.MFRC522_Write(8, read)
				time.sleep(1)
			else:
				logging.warning("Unauthorised Attempt! %s" % uid)
			MIFAREReader.MFRC522_StopCrypto1()
		else:
			logging.warning("Unauthorised Attempt! %s" % uid)

	if count==0:
		prevState = currState
		currState = GPIO.input(sensorPin)
		if currState != prevState:
			if currState:
				print "A MOTION HAS BEEN DETECTED !!! Recording Started!"
				logging.warning("A MOTION HAS BEEN DETECTED !!! Recording Started!")
				fileName = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
				try:
					cam.start_preview()
					cam.start_recording(fileName)
					print (fileName)
				except Exception, Argument:
					logging.error(Argument)
					sms.sendSMS(num1,msg_prob)
					sms.sendSMS(num2,msg_prob)
			else:
				print "MOTION STOPPED! Recording Stopped!"
				logging.info("Recording Stopped! %s" % fileName)
				try:
					cam.stop_preview()
					cam.stop_recording()
				except Exception, Argument:
					logging.error(Argument)
					sms.sendSMS(num1,msg_prob)
					sms.sendSMS(num2,msg_prob)
				else:
					try:
						print "Sending Mail Notification..."
						subprocess.call("mail -s 'Motion Detected' abcd@gmail.com < /home/pi/message.txt", shell=True)
						print "Uploading the footage to Dropbox..."
						dropboxUpload(fileName)
					except Exception, Argument:
						logging.error(Argument)
						sms.sendSMS(num1,msg_prob)
						sms.sendSMS(num2,msg_prob)
					else:
						print "Sending SMS Notification..."
						sms.sendSMS(num1,msg_warn)
						sms.sendSMS(num2,msg_warn)
						subprocess.call("mail -s 'Motion Detected' abcd@gmail.com < /home/pi/message.txt", shell=True)
						print "Process Completed!"
