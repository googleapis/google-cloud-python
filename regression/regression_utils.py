from __future__ import print_function
import os
import sys

from gcloud import datastore
from gcloud import storage


# Defaults from shell environ. May be None.
PROJECT_ID = os.getenv('GCLOUD_TESTS_PROJECT_ID')
DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CLIENT_EMAIL = os.getenv('GCLOUD_TESTS_CLIENT_EMAIL')
KEY_FILENAME = os.getenv('GCLOUD_TESTS_KEY_FILE')
CACHED_RETURN_VALS = {}

ENVIRON_ERROR_MSG = """\
To run the regression tests, you need to set some environment variables.
Please check the Contributing guide for instructions.
"""


def get_environ(require_datastore=False, require_storage=False):
    if require_datastore:
        if DATASET_ID is None or CLIENT_EMAIL is None or KEY_FILENAME is None:
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)

    if require_storage:
        if PROJECT_ID is None or CLIENT_EMAIL is None or KEY_FILENAME is None:
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)

    return {
        'project_id': PROJECT_ID,
        'dataset_id': DATASET_ID,
        'client_email': CLIENT_EMAIL,
        'key_filename': KEY_FILENAME,
    }


def get_dataset():
    environ = get_environ(require_datastore=True)
    get_dataset_args = (environ['dataset_id'], environ['client_email'],
                        environ['key_filename'])
    key = ('get_dataset', get_dataset_args)
    if key not in CACHED_RETURN_VALS:
        # Cache return value for the environment.
        CACHED_RETURN_VALS[key] = datastore.get_dataset(*get_dataset_args)
    return CACHED_RETURN_VALS[key]


def get_storage_connection():
    environ = get_environ(require_storage=True)
    get_connection_args = (environ['project_id'], environ['client_email'],
                           environ['key_filename'])
    key = ('get_storage_connection', get_connection_args)
    if key not in CACHED_RETURN_VALS:
        # Cache return value for the environment.
        CACHED_RETURN_VALS[key] = storage.get_connection(*get_connection_args)
    return CACHED_RETURN_VALS[key]
