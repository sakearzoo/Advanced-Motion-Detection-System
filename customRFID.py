#!/usr/bin/env python
# -*- coding: utf8 -*-
#https://github.com/sakearzoo
#By Sheikh Nawab Arzoo

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: ",uid
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        print "\n"

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            data = [0x02]

            # Fill the data with 0xFF
            for x in range(0,15):
                data.append(0x00)
            
            print "Sector 8 looked like this:"
            # Read block 8
            print MIFAREReader.MFRC522_Read(8)
            print "\n"
            
            # Write the data
            MIFAREReader.MFRC522_Write(8, data)
            print "\n"
            
            print "Sector 8 now looks like this:"
            # Read block 8
            print MIFAREReader.MFRC522_Read(8)
            print "\n"

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print "Authentication error"