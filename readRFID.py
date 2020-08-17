#!/usr/bin/python3
#https://github.com/sakearzoo
#https://github.com/abhisheksarkar30
#By Sheikh Nawab Arzoo & Abhishek Sarkar
import sys
sys.path.insert(0, "/home/pi/pi-rc522/ChipReader")
import RFID
import signal
import time

rdr = RFID.RFID()
util = rdr.util()
util.debug = False

while True:
    #Request tag
    (error, data) = rdr.request()
    if not error:
        print ("\nDetected")
        
   (error, uid) = rdr.anticoll()
        if not error:
            #Print UID
            print ("Card read UID: "+str(uid[0])+", "+str(uid[1])+", "+str(uid[2])+", "+str(uid[3]))

            time.sleep(1)
