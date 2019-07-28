# **Advanced Motion Detection System**
![](https://img.shields.io/badge/Release-V1.0.0-blue.svg)  ![](https://img.shields.io/badge/Build-Stable-green.svg) ![](https://img.shields.io/badge/License-MIT-red.svg) ![](https://img.shields.io/badge/By-Sheikh%20Nawab%20Arzoo-red.svg?style=social&logo=appveyor)

------------


It&#39;s a motion detection system refers to the capability of the surveillance system to detect motion and capture the events. Motion detection is usually a software - hardware based monitoring algorithm which, when it detects motions will signal the surveillance camera to begin capturing the event. Also called activity detection. An advanced motion detection surveillance system can also send the mail and sms notification as well as video clip will be uploaded to internet alternatively we can also live stream the current situation and have a RFID based system which keeps a track of the authorised person entering in the area hence camera will not be activated and no false notification will be send.

**How it works ?**
Motion detection system is the first essential process in the extraction of information regarding moving objects and makes use of stabilization in functional areas, such as tracking, classification, recognition, and so on. In this project, we propose an idea and accurate approach to motion detection for the automatic video surveillance system. Our method achieves complete detection of moving objects by involving significant parts: motion detection by a sensitive PIR sensor, recording video footage by a camera module, all these are controlled by a raspberry pi. When a motion is detected by the PIR sensor then it sends a signal to the raspberry pi and then raspberry pi activates the camera and starts recording until the motion stopped. A mail notification is send to a given mail address and video footage is processed and then it will be uploaded to dropbox and then at last an sms notification is being send to the registered number.

The RFID is used to detect if the user is authorized by TAGS. If the user is authorised then the script will pause and hence no notification will be send. The entry and exit of the person will be LOGGED for further reference. If the owner wants to view the live video then also he/she can watch directly via browser/app.

#### PRE-REQUISITE:

`$sudo apt-get update`
`$sudo apt-get upgrade`
`$sudo apt-get install python-picamera`
`$apt-get install ssmtp`
`$apt-get install mailutils`

#### Edit the SSMTP configuration file:

````
hostname=raspberrypi
AuthUser=YOUR GMAIL USERNAME@gmail.com
AuthPass=YOUR GMAIL PASSWORD
UseSTARTTLS=YES
UseTLS=YES
````
###### Optional lines:
`$rewriteDomain=your.domain`
Specify this if you would like the outgoing emails to appear to be sent from your.domain (instead of from [gmail.com](http://gmail.com/)).
`FromLineOverride=YES`

###### You need to edit Boot Config file:
`$sudo nano /boot/config.txt`

Add the following entry to the end of the file:
`dtoverlay=spi-bcm2708`

Open the `raspi-config` tool from the Terminal:
Select Enable camera and hit Enter, then go to Finish and you&#39;ll be prompted to reboot.

#### Configure raspberry pi with Dropbox
Download and uncompress the Python SDK. To install the dropbox module and any dependencies, run the setup script (you may need sudo).
`$python setup.py install`

Alternatively, you can use pip to automatically download and install the module.
`$pip install dropbox`

#### How to use Dropbox with Raspberry Pi

You must then create an &quot;App&quot; on the Dropbox server:
https://www.dropbox.com/developers/apps/create

Select **&quot;Dropbox API app&quot;**
Select **&quot;files and datastores&quot;**
Select **&quot;Yes&quot;** for the &quot;**Can your app be limited to its own, private folder?&quot;**
Enter an appname that is unique
Select the **&quot;Create App&quot;** button

The Dropbox Server will then present you a web page filled with a variety of information.  You will need the contents of the fields labelled:
**App key**
**App secret**

###### One more step to test:
Test the Dropbox program on the Raspberry Pi by uploading a file (anything will do).


#### Live video script:

To watch live we just need to paste this piece of code into the terminal of the raspberry pi:

`$sudo modprobe bcm2835-v4l2`

````
ffserver -f /etc/ffserver.conf &amp; ffmpeg -v verbose -r 5 -s 600x480 -f video4linux2 -i /dev/video0 http://localhost:9090/feed1.ffm
````

`localhost:9090/test.mjpg`

##### Next make the Python file executable and then you can run it:
`chmod +x pirtest.py`



### Run the main script
`$sudo ./amdsv2.py`


------------

