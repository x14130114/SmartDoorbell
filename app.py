"""
    **********************************************************
    *   Main thread that runs the IoT Doorbell application   *
    **********************************************************

    Main thread runs the Application and links all the features of the doorbell together
    Switch face check On/Off
    Run listen function listening to Firebase real time database changes
    Controls all the features of IoT Doorbell

"""



from aws import AWS
from firebase import Firebase
from time import sleep
from new_face import NewFace
from lock import Solenoid
from bell_button import BellButton
import os
from check_face import FaceCheck

# Function to turn off facial recognition checking and update firebase value
def switch_face_check_off():
    fc.perform_action = False
    fb.update_data({
        'doorbell/facial_recognition/is_active': 0
    })
    sleep(2)

# Function to turn on facial recognition checking and update firebase value
def switch_face_check_on():
    fc.perform_action = True
    fb.update_data({
        'doorbell/facial_recognition/is_active': 1
    })
    sleep(2)

# Function to listen to changes from Firebase real time database
def listen():
    while True:
        # Set data variable to the database root reference
        data = fb.get_data()
        # Get AWS started database status
        aws_start_requested = data['doorbell']['streaming']['start_requested']
        # Get AWS stopped database status
        aws_stop_requested = data['doorbell']['streaming']['stop_requested']
        # Get new face database status
        new_face_request = data['doorbell']['face']['start_new']
        # Get audio database status
        audio = data['doorbell']['audio']['state']
        # Get lock database status
        is_unlocked = data['doorbell']['lock']['state']

        # AWS start check
        if aws_start_requested == 1 and aws.is_active is False:
            # Turn face check off
            switch_face_check_off()
            # Start the AWS stream
            aws.start_stream()

        # AWS stop check
        if aws_stop_requested == 1 and aws.is_active is True:
            # Stop the AWS stream
            aws.stop_stream()
            # Turn face check on
            switch_face_check_on()

        # if new face requested and AWS stream is inactive
        if new_face_request == 1 and nf.is_active is False and aws.is_active is False:
            print("Adding Face")
            # Turn off face check
            switch_face_check_off()
            # Start adding new face
            nf.take_pictures()
            # Turn face check on
            switch_face_check_on()

        # if the lock is set to 1 in Firebase, unlock the door
        if is_unlocked == 1:
            print("Unlocking Door")
            lock.unlock_door()
            print("Door Locked")

        # if audio is set to new in Firebase, download the latest audio file and play it via the speaker
        if audio == "new":
            fb.get_storage()
            os.system("omxplayer audioVisitor.mp3")
            fb.update_data({
                'doorbell/audio/state': 'waiting'
            })

if __name__ == '__main__':
    # Firebase class instance
    fb = Firebase()
    # AWS class instance
    aws = AWS(fb)
    # NewFace class instance
    nf = NewFace(fb)
    # Solenoid Lock class instance
    lock = Solenoid()
    # Face Check class instance
    fc = FaceCheck()
    # Doorbell button class instance
    bb = BellButton(aws, nf, switch_face_check_on, switch_face_check_off)
    # Start the BellButton Thread class
    bb.start()
    # Start the Face Check Thread class
    fc.start()
    # Turn on face check
    switch_face_check_on()
    # Run the listen function
    listen()




