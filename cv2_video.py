"""
    **************************************
    *         OpenCV Video class         *
    **************************************

    Initialize face recognizer and Frontal face cascade

    Functions:
    Check if trainer configuration file exists
    Load trainer configuration file
    Start capturing video from the PiCam
    Release PiCam and stop capturing
    Convert the picture to grey
"""

import cv2
import os


class CV2Video:

    video = None
    # Initializing face recognizer from OpenCV library
    face_detector = cv2.face.LBPHFaceRecognizer_create()
    # Using Frontal Face cascade for facial recognition
    cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

    @staticmethod
    # Function to check if the trainer configuration file exists
    def trainer_exists():
        return os.path.exists('trainer.yml')

    # Function to load the existing trainer file
    @staticmethod
    def load_trainer():
        if CV2Video.trainer_exists() is True:
            CV2Video.face_detector.read('trainer.yml')

    # Function to start capturing video from PiCam using OpenCV library
    @staticmethod
    def capture():
        if CV2Video.video is None:
            CV2Video.video = cv2.VideoCapture(0)

    # Function to release/stop capturing video from PiCam
    @staticmethod
    def release():
        if CV2Video.video is not None:
            CV2Video.video.release()
            CV2Video.video = None

    # Function to convert the captured picture to grey
    @staticmethod
    def convert_to_grey(picture):
        return cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)


# Load the trainer function
CV2Video.load_trainer()
