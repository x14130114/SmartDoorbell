"""
    **************************************
    * Doorbell Push Button Thread class *
    **************************************

    Class runs as its own Thread
    Connects securely to Push Bullet API
    Set which device to send notifications
    Take picture from the PiCam when the Doorbell Push Button is pressed
    Attach the image to a push notification and upload it to PushBullet APi
    PushBullet sends the notification to the device connected
"""

from picamera import PiCamera
from datetime import datetime
import time
import os
from pushbullet import Pushbullet
from gpiozero import Button
from threading import Thread

class BellButton(Thread):
    # connecting to push bullet api
    _pb = Pushbullet("<API-KEY>")

    # print the available devices
    print(_pb.devices)
    # set your device
    _huawei = _pb.get_device('<DEVICE-NAME>')

    # Setting Button to GPIO Pin 18
    button = Button(18)
    filename = ''

    # Function to take photo using the PiCam and run the push_notification function
    # Function only runs if AWS stream and Adding new faces is not already in use
    def take_photo(self):

        if self.aws.is_active is False and self.nf.is_active is False:
            # Turn Facial recognition off - releasing camera
            self.switch_face_check_off()
            time.sleep(.2)
            print('taking pictures')
            global filename
            camera = PiCamera()
            # Setting the filename and extension
            filename = 'bell.jpg'
            camera.resolution = (800, 600)
            # Capture image from PiCam and store it in location with the file name
            camera.capture('/home/pi/PyCharms/DoorFinal/' + filename)
            # Close the camera instance - releasing camera
            camera.close()
            # Run the push notification function
            BellButton.push_notification(self)
            time.sleep(.2)
            # Turn Facial recognition on
            self.switch_face_check_on()

    # Function to upload image with notification to PushBullet APi and send to the connected device
    def push_notification(self):
        print('sending push notification with image...')
        with open("bell.jpg", "rb") as pic:
            img = self._pb.upload_file(pic, "Visitor at the door")
        self._huawei.push_file(**img)
        print('sent........')

    # Function to check the status of the button, if pressed run the take photo function
    def run(self):
        while True:
            btn = self.button.value
            if btn is True:
                os.system("omxplayer ding-dong-1.8.mp3")
                self.take_photo()

    # Constructor to initialize other class instances
    def __init__(self, aws, nf, switch_face_check_on, switch_face_check_off):
        super().__init__()
        self.aws = aws
        self.nf = nf
        self.switch_face_check_on = switch_face_check_on
        self.switch_face_check_off = switch_face_check_off

