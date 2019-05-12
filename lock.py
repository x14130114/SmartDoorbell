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

lock = 21


# Solenoid Class
class Solenoid:

    # Function to unlock the solenoid lock for 10 seconds
    @staticmethod
    def unlock_door():
        print("in lock")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(lock, GPIO.OUT)
        # Unlock door for 10 Seconds
        GPIO.output(lock, GPIO.LOW)
        time.sleep(10)
        # Cleanup GPIO pin to lock solenoid
        GPIO.cleanup(21)
        # Update Firebase database lock status to 0
        fb.update_data({
            'doorbell/lock/state': 0
        })
        print("finish")


#Solenoid.unlock_door()
