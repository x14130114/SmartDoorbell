import os
import unittest

"""
Test class for playing audio file from the speaker

"""

class TestSpeaker(unittest.TestCase):

    def test_speaker(self):
        os.system("omxplayer audioVisitor.mp3")
        # print ()
        print("Speaker successfully played audio file")


if __name__ == '__main__':
    unittest.main()