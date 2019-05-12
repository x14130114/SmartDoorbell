import unittest
import pyrebase

"""
Test class for Firebase

"""


class TestFirebase(unittest.TestCase):
    # Firebase DB config
    _config = {
        "apiKey": "<API-KEY>",
        "authDomain": "<AUTH-DOMAIN>",
        "databaseURL": "<DATABASE-URL>",
        "projectId": "<PROJECT-ID>",
        "storageBucket": "<STORAGE-BUCKET>",
        "messagingSenderId": "<SENDER-ID>",
        "serviceAccount": "<FILEPATH TO KEY.JSON>"
    }

    # login credentials as private access vars
    _login = "<USERNAME>"
    _password = "<PASSWORD>"

    # Constructor to initialize different firebase instances
    def test__init__(self):
        self._firebase = pyrebase.initialize_app(self._config)
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(self._login, self._password)
        self._db = self._firebase.database()
        self._storage = self._firebase.storage()

    # update data method
    def test_update_data(self, data):
        self._db.update(data)

    # get data method
    def test_get_data(self):
        return self._db.get().val()

    # create user with the firebase credentials
    def test_create_user(self, email, password):
        self._auth.create_user_with_email_and_password(email, password)

    # downloading the audio file uploaded to firebase storage from the android microphone
    def test_get_storage(self):
        return self._storage.child("Audio/visitor_voice.mp3").download("audioVisitor.mp3")


if __name__ == '__main__':
    unittest.main()
