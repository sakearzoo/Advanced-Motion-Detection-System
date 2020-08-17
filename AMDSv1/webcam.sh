sudo modprobe bcm2835-v4l2
ffserver -f /etc/ffserver.conf & ffmpeg -v verbose -r 5 -s 600x480 -f video4linux2 -i /dev/video0 http://localhost:9090/feed1.ffm
#localhost:9090/test.mjpg