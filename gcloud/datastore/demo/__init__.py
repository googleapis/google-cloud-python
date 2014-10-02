import os
from gcloud import datastore

__all__ = ['get_dataset', 'CLIENT_EMAIL', 'DATASET_ID', 'PRIVATE_KEY_PATH']

CLIENT_EMAIL = ('754762820716-gimou6egs2hq1rli7el2t621a1b04t9i'
                '@developer.gserviceaccount.com')
DATASET_ID = 'gcloud-datastore-demo'
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.key')


def get_dataset():  # pragma NO COVER
    return datastore.get_dataset(DATASET_ID, CLIENT_EMAIL, PRIVATE_KEY_PATH)
