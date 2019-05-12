import os
import unittest

"""
Test class for playing audio file from the speaker

"""

class TestMic(unittest.TestCase):

    def test_microphone(self):
        os.system("arecord -d 5 -D hw:2,0 -f S16_LE -r 44100 testrecord.mp3")
        print("Audio recorded successfully")


if __name__ == '__main__':
    unittest.main()