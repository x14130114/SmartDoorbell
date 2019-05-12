import unittest
from pushbullet import Pushbullet

"""
Test class for PushBullet API

"""

class TestPushBullet(unittest.TestCase):
    # connecting to push bullet api
    _pb = Pushbullet("<API-KEY>")
    # push = pb.push_note("Title","body")

    # check the available devices
    print(_pb.devices)
    # set your device
    _huawei = _pb.get_device('<DEVICE-NAME>')

    def test_pushbullet(self):
        print('sending push notification with image...')
        with open("cameratest.jpg", "rb") as pic:
            img = self._pb.upload_file(pic, "Test Notification")
        self._huawei.push_file(**img)
        print('Notification successfully pushed to the device via PushBullet')


if __name__ == '__main__':
    unittest.main()