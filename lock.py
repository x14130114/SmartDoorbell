"""
    **************************************
    *        Solenoid Lock class         *
    **************************************

    Setup GPIO Pin to connect to lock
    Unlock Door function

"""

import RPi.GPIO as GPIO
import time
from firebase import Firebase

fb = Firebase()
global timer
lock = 21


# Solenoid Class
class Solenoid:

    # Function to unlock the solenoid lock for 10 seconds
    @staticmethod
    def unlock_door():
        # Firebase reference
        data = fb.get_data()
        # setting timer variable to firebase timer value
        timer = data['doorbell']['lock']['timer']

        print("in lock")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(lock, GPIO.OUT)

        # Unlock door for as many seconds as the timer is set
        GPIO.output(lock, GPIO.LOW)
        time.sleep(timer)
        # Cleanup GPIO pin to lock solenoid
        GPIO.cleanup(21)
        # Update Firebase database lock status to 0
        fb.update_data({
            'doorbell/lock/state': 0
        })
        print("finish")

