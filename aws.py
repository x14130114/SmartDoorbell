"""
    **************************************
    * Amazon Kinesis Video Streams class *
    **************************************

    Starting live audio and video stream on Amazon Kinesis Video Streams using GStreamer as a background subprocess
    Retrieving HLS Stream URL using Amazon Python SDK Boto3
    Stopping Live stream by finding and killing process id
    Communicating with Firebase database to update the stream values and URL
"""

import subprocess
import os
import boto3
from time import sleep

class AWS:

    # Initializing the process ID variable
    _pid = None

    # Initializing the AWS stream is_active variable
    is_active = False

    # Initializing Firebase
    def __init__(self, fb):
        self._fb = fb

    # Function to start the AWS audio and video stream using GStreamer as a subprocess in the background
    # Stores process id of background subprocess in _pid variable
    # Uses Boto3 Amazon Python SDK to make getRequest to Amazon API to retrieve the GetHLSStreamingSessionURL
    # Communicates with Firebase database to update values such as the stream URL and status
    def start_stream(self):
        self.is_active = True
        self._fb.update_data({
            'doorbell/streaming/start_requested': 0
        })
        # Subprocess bash command running GStreamer to start the AWS audio and video stream.  Running in the background
        subprocess.call('nohup gst-launch-1.0 -v v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,width=640,'
                        'height=480,framerate=30/1,format=I420 ! omxh264enc periodicty-idr=45 inline-header=FALSE ! '
                        'h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink name=sink '
                        'stream-name="<STREAM-NAME>" access-key="<ACCESS-KEY>" '
                        'secret-key="<SECRET-KEY>" '
                        'alsasrc device=hw:2,0 ! audioconvert ! avenc_aac ! queue ! sink. >/dev/null 2>&1 &', shell=True)
        # Subprocess to use bash command to get the process id for a process named 'gst-launch-1.0'
        get_pid = subprocess.Popen("ps aux | pgrep gst-launch-1.0", shell=True, stdout=subprocess.PIPE).stdout
        self._pid = get_pid.read()
        print("My process id is %s" % self._pid.decode())
        sleep(3)

        STREAM_NAME = "<STREAM-NAME>"
        # Using Boto3 to access Amazon Kinesis Video API
        kvs = boto3.client("kinesisvideo")

        # Get the data end point of the stream
        endpoint = kvs.get_data_endpoint(
            APIName="GET_HLS_STREAMING_SESSION_URL",
            StreamName=STREAM_NAME
        )['DataEndpoint']

        # Get the HLS Stream URL using the endpoint
        kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
        url = kvam.get_hls_streaming_session_url(
            StreamName=STREAM_NAME,
            PlaybackMode="LIVE"
        )['HLSStreamingSessionURL']

        print(url)
        # Update Firebase database with the Live Stream HLS URL
        self._fb.update_data({
            'doorbell/streaming/hls_url': url
        })

    # Function to stop the AWS stream by finding the process ID of the GStreamer subprocess and killing that process
    # Communicates with Firebase database to update status of the stream
    def stop_stream(self):
        print('stopping')
        os.system('kill -9 %s' % self._pid.decode())
        sleep(2)
        self.is_active = False
        self._fb.update_data({
            'doorbell/streaming/stop_requested': 0,
            'doorbell/streaming/start_requested': 0
        })
