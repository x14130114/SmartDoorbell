"""
    **************************************
    *           NewFace class            *
    **************************************

    Uses OpenCV library to take pictures of a persons face, associate the person to an ID
    Train the faces and IDs and update the trainer.yml configuration file to be used for Facial recognition
    Communicate with Firebase real time database to update the adding face status

"""

import os
from time import sleep
import random
from cv2_video import CV2Video
import cv2
import numpy as np
from PIL import Image

# NewFace Class
class NewFace:

    # Initializing the NewFace is_active variable
    is_active = False

    # private variable for directory path
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _images_dir = os.path.join(_BASE_DIR, "user")

    # Initializing Firebase
    def __init__(self, fb):
        self._fb = fb

    # Function to train faces
    def train_faces(self):
        # Empty array for faces arrays
        faces = []
        # Empty array for user's id
        ids = []

        # loop through images in the /user folder
        for root, dirs, images in os.walk(self._images_dir):
            for img in images:
                # if img ends with .jpg
                if img.endswith("jpg"):

                    # setting face_id out of the folder name
                    face_id = int(os.path.basename(root))
                    # setting path from image number and root folder
                    path = os.path.join(root, img)
                    # convert image to gray
                    grey_img = Image.open(path).convert('L')
                    # creating numpy array of the image
                    img_arr = np.array(grey_img, 'uint8')

                    # Detects the face on the currently loaded image.
                    temp = CV2Video.cascade.detectMultiScale(img_arr)
                    for (x, y, w, h) in temp:
                        # Append the face's to faces array
                        faces.append(img_arr[y:y + h, x:x + w])
                        # Append id to the ids array
                        ids.append(face_id)

        # Uses OpenCV FaceRecognizer training algorithm to train the faces in the array
        CV2Video.face_detector.train(faces, np.array(ids))
        # Save the trained data to trainer.yml
        CV2Video.face_detector.save('trainer.yml')
        print("COMPLETE")

    # Function to take 30 pictures and add them to /user folder under their own specific ID
    def take_pictures(self):
        # Set the NewFace status to True
        self.is_active = True
        # Start the video
        CV2Video.capture()
        # Countdown timer before taking pictures
        ct = 5
        while ct > 0:
            print('Please look at the camera now. Pictures will be taken in %s' % ct)
            sleep(1)
            ct = ct - 1
            os.system('clear')

        # Check for the user folder and create if it cant be found
        if os.path.exists('user') is False:
            os.mkdir('user')

        # Use random generator to generate random ID for newly added face
        user_id = random.SystemRandom().randint(10000, 99999)
        while True:
            if os.path.exists('user/%s' % user_id) is False:
                os.mkdir('user/%s' % user_id)
                break
            else:
                user_id = random.SystemRandom().randint(10000, 99999)

        # Initialize counter variable
        counter = 0

        # Loop for taking pictures
        while True:
            # ret = boolean, frame = current camera frame
            ret, frame = CV2Video.video.read()
            # Convert picture to greyscale
            gray = CV2Video.convert_to_grey(frame)
            # faces = CV2Video.cascade.detectMultiScale(gray, 1.5, 5)  # detect faces
            # Detect faces using frontal face cascade
            faces = CV2Video.cascade.detectMultiScale(gray, 1.2, 5)

            # loop through detected faces
            for (x, y, w, h) in faces:
                # write the detected faces with the user id and counter value to the user folder
                cv2.imwrite("user/%s/%s.jpg" % (user_id, counter), gray[y: y + h, x: x + w])
                counter = counter + 1
                print(counter)

            # Stop taking pictures after 30 are taken
            if counter == 30:
                # Run the train faces function
                self.train_faces()

                print('Your profile was created! Thanks!')
                # Release video
                CV2Video.release()
                # Load updated trainer configuration
                CV2Video.load_trainer()
                # Update Firebase adding face status
                self._fb.update_data({
                    'doorbell/face/start_new': "complete",
                    'doorbell/face/start_new': 0
                })
                # Setting NewFace status to False
                self.is_active = False
                break
