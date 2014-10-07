# pragma NO COVER
import os
from gcloud import storage

__all__ = ['get_connection', 'CLIENT_EMAIL', 'PRIVATE_KEY_PATH', 'PROJECT']

CLIENT_EMAIL = ('606734090113-6ink7iugcv89da9sru7lii8bs3i0obqg@'
                'developer.gserviceaccount.com')
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.key')
PROJECT = 'gcloud-storage-demo'


def get_connection():  # pragma NO COVER.
    return storage.get_connection(PROJECT, CLIENT_EMAIL, PRIVATE_KEY_PATH)
