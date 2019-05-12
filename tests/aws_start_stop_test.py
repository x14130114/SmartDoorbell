import subprocess
import unittest
import os
from time import sleep

"""
Test class for starting and stopping the live audio and video stream with GStreamer using Amazon Kinesis Video Streams

"""


class TestAws(unittest.TestCase):

    _pid = None

    def test_start(self):
        # Subprocess bash command running GStreamer to start the AWS audio and video stream.  Running in the background
        subprocess.call('nohup gst-launch-1.0 -v v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,width=640,'
                        'height=480,framerate=30/1,format=I420 ! omxh264enc periodicty-idr=45 inline-header=FALSE ! '
                        'h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink name=sink '
                        'stream-name="<STREAM-NAMW>" access-key="<ACCESS-KEY>" '
                        'secret-key="<SECRET-ACCESS-KEY>" '
                        'alsasrc device=hw:2,0 ! audioconvert ! avenc_aac ! queue ! sink. >/dev/null 2>&1 &',
                        shell=True)
        print("Audio and Video stream successfully started on Amazon Kinesis Video Streams")
        sleep(3)

    def test_stop(self):
        get_pid = subprocess.Popen("ps aux | pgrep gst-launch-1.0", shell=True, stdout=subprocess.PIPE).stdout
        self._pid = get_pid.read()
        print("My process id is %s" % self._pid.decode())
        print('stopping')
        os.system('kill -9 %s' % self._pid.decode())
        print("Stream successfully terminated")


if __name__ == '__main__':
    unittest.main()