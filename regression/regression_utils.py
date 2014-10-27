import os
import sys

from gcloud import datastore


# Defaults from shell environ. May be None.
DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CLIENT_EMAIL = os.getenv('GCLOUD_TESTS_CLIENT_EMAIL')
KEY_FILENAME = os.getenv('GCLOUD_TESTS_KEY_FILE')
DATASETS = {}

ENVIRON_ERROR_MSG = """\
To run the regression tests, you need to set some environment variables.
Please check the Contributing guide for instructions.
"""


def get_environ():
    if DATASET_ID is None or CLIENT_EMAIL is None or KEY_FILENAME is None:
        print >> sys.stderr, ENVIRON_ERROR_MSG
        sys.exit(1)

    return {
        'dataset_id': DATASET_ID,
        'client_email': CLIENT_EMAIL,
        'key_filename': KEY_FILENAME,
    }


def get_dataset():
    environ = get_environ()
    get_dataset_args = (environ['dataset_id'], environ['client_email'],
                        environ['key_filename'])
    if get_dataset_args not in DATASETS:
        # Cache return value for the environment.
        DATASETS[get_dataset_args] = datastore.get_dataset(*get_dataset_args)
    return DATASETS[get_dataset_args]
