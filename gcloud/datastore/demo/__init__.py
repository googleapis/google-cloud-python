# pragma NO COVER
import os
from gcloud import datastore

__all__ = ['get_dataset', 'CLIENT_EMAIL', 'DATASET_ID', 'KEY_FILENAME']


DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CLIENT_EMAIL = os.getenv('GCLOUD_TESTS_CLIENT_EMAIL')
KEY_FILENAME = os.getenv('GCLOUD_TESTS_KEY_FILE')


def get_dataset():  # pragma NO COVER
    return datastore.get_dataset(DATASET_ID, CLIENT_EMAIL, KEY_FILENAME)
