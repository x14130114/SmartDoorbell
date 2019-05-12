from picamera import PiCamera
import unittest

"""
Test class for taking a picture with the PiCam

"""


class TestCamera(unittest.TestCase):

    def test_camera(self):
        camera = PiCamera()
        filename = 'cameratest.jpg'
        camera.resolution = (800, 600)
        # Capture image from PiCam and store it in location with the file name
        camera.capture('/home/pi/PyCharms/DoorFinal/tests/' + filename)
        # Close the camera instance - releasing camera
        camera.close()
        print("Picture successfully taken")


if __name__ == '__main__':
    unittest.main()
