"""
    **************************************
    *   OpenCV Facial Recognition class  *
    **************************************

    Uses OpenCV library to capture video and detect faces
    Uses Frontal Face cascade detection
    Detects faces that have been added

"""

from cv2_video import CV2Video

# Facial Recognition class
class Recognition:

    # Function to start facial recognizer
    @staticmethod
    def recognize():
        # ret = boolean and frame = current frame captured
        ret, frame = CV2Video.video.read()
        # Convert picture to greyscale
        gray = CV2Video.convert_to_grey(frame)
        # detect faces through the cascade instructions
        faces = CV2Video.cascade.detectMultiScale(gray, 1.3, 5)

        # iterating through faces if face detected on the camera
        for (x, y, w, h) in faces:
            # if User ID is associated with the face set active user
            face_id, score = CV2Video.face_detector.predict(gray[y: y + h, x: x + w])
            # Return face id and score accuracy of the face
            return [face_id, score]