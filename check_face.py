"""
    **************************************
    *        Facial Check class          *
    **************************************

    Class runs as its own Thread
    Checks faces and prints recognized faces if they have an accuracy of less than 80
    Face is true if one face id and score of less than 40 is detected 20+ frames in a row


"""

from threading import Thread
from time import sleep
from recognition import Recognition
from cv2_video import CV2Video
from lock import Solenoid

# Face check class
class FaceCheck(Thread):

    # Initializing Lock object
    lock = Solenoid()
    # Initializing perform action variable
    perform_action = False
    # Initialize using camera variable
    using_camera = False
    # Private variable for face
    _face = True
    # Private variable of frames detected
    _frames_checked = 0
    # Private variable for face id
    _id = 0
    _counter_seconds = 5

    # Function to start a counter that counts to 5 1 second at a time
    def counter(self):
        c = 0
        while c < self._counter_seconds and self.perform_action is True:
            c = c + 1
            sleep(1)

    # Function to check
    def check(self):
        c = Thread(target=self.counter)
        c.daemon = True
        c.start()
        self._frames_checked = 0
        while c.is_alive():
            res = Recognition.recognize()
            if res is not None:
                self._frames_checked = self._frames_checked + 1
                print("%s, %s" % (res[0], res[1]))
                if self._id != res[0]:
                    self._face = False
                    print(self._face)
                    break
                elif self._id == res[0] and res[1] > 60:
                    self._face = False
                    print(self._face)
                    break

    # Function to start capturing from camera
    def capture_camera(self):
        CV2Video.capture()
        self.using_camera = True

    # Function to stop capturing and release camera
    def release_camera(self):
        CV2Video.release()
        self.using_camera = False

    # Function to run face check and unlock door if faces meet the criteria of true greater than 20 frames in a row
    def run(self):
        while True:
            # If face check is turned on and camera is off, start capturing video from camera
            if self.perform_action is True and self.using_camera is False:
                self.capture_camera()
            # If face check if off and camera instance is on, release camera
            elif self.perform_action is False and self.using_camera is True:
                self.release_camera()

            # If camera is true
            if self.using_camera is True:
                # set face recognizer values[ID, accuracy] to res
                res = Recognition.recognize()
                # If res is not None and accuracy is less than 70
                if res is not None and res[1] < 70:
                    # Set id to res id
                    self._id = res[0]
                    # Set face to true
                    self._face = True
                    # Setup thread to run the check function
                    t = Thread(target=self.check)
                    # Start the thread
                    t.start()
                    # Join the thread to the main thread
                    t.join()
                    # Release the camera
                    self.release_camera()
                    # If face is true for 20 frames that are detected in a row
                    if self._face is True and self._frames_checked >= 10:
                        # unlock door
                        self.lock.unlock_door()
                        print(self._id)
                        print(self._face)
                        sleep(10)