"""
    **************************************
    *           Firebase class           *
    **************************************

    Firebase Configuration
    Update data on Firebase real time database
    Retrieve data from Firebase real time database
    Authenticate user using firebase credentials

"""

# imports
import json
import pyrebase
import urllib
import requests
from datetime import datetime

class Firebase:
    # Firebase DB config
    _config = {
        "apiKey": "<API-KEY>",
        "authDomain": "<AUTH-DOMAIN>",
        "databaseURL": "<DATABASE-URL>",
        "projectId": "<PROJECT-ID>",
        "storageBucket": "<STORAGE-BUCKET>",
        "messagingSenderId": "<SENDER-ID>",
        "serviceAccount": "<PATH-TO-KEY.JSON>"
    }
    # Firebase login
    _login = "<USERNAME>"
    _password = "<PASSWORD>"

    # update data method
    def update_data(self, data):
        self._db.update(data)

    # get data method
    def get_data(self):
        return self._db.get().val()

    # create user with the firebase credentials
    def create_user(self, email, password):
        self._auth.create_user_with_email_and_password(email, password)

    # downloading the audio file uploaded to firebase storage from the android microphone
    def get_storage(self):
        return self._storage.child("Audio/visitor_voice.mp3").download("audioVisitor.mp3")

    # Constructor to initialize different firebase instances
    def __init__(self):
        self._firebase = pyrebase.initialize_app(self._config)
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(self._login, self._password)
        self._db = self._firebase.database()
        self._storage = self._firebase.storage()
