# pragma NO COVER
import os
from gcloud import storage

__all__ = ['get_connection', 'CLIENT_EMAIL', 'KEY_FILENAME', 'PROJECT_ID']

PROJECT_ID = os.getenv('GCLOUD_TESTS_PROJECT_ID')
CLIENT_EMAIL = os.getenv('GCLOUD_TESTS_CLIENT_EMAIL')
KEY_FILENAME = os.getenv('GCLOUD_TESTS_KEY_FILE')


def get_connection():  # pragma NO COVER.
    return storage.get_connection(PROJECT_ID, CLIENT_EMAIL, KEY_FILENAME)
