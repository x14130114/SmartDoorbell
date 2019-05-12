import RPi.GPIO as GPIO
import unittest

"""
Test class for unlocking the door via the solenoid lock

"""

class TestLock(unittest.TestCase):

    def test_unlock_door(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        # Unlock door
        GPIO.output(21, GPIO.LOW)
        # Cleanup GPIO pin to lock solenoid
        GPIO.cleanup(21)
        print("Door Unlocked and Locked Successfully")


if __name__ == '__main__':
    unittest.main()
