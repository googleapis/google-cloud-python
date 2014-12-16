# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import os
import sys

from gcloud import datastore
from gcloud import storage


# From shell environ. May be None.
PROJECT_ID = os.getenv('GCLOUD_TESTS_PROJECT_ID')
DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
CACHED_RETURN_VALS = {}

ENVIRON_ERROR_MSG = """\
To run the regression tests, you need to set some environment variables.
Please check the Contributing guide for instructions.
"""


def get_environ(require_datastore=False, require_storage=False):
    if require_datastore:
        if DATASET_ID is None or not os.path.isfile(CREDENTIALS):
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)

    if require_storage:
        if PROJECT_ID is None or not os.path.isfile(CREDENTIALS):
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)

    return {
        'project_id': PROJECT_ID,
        'dataset_id': DATASET_ID,
    }


def get_dataset():
    environ = get_environ(require_datastore=True)
    dataset_id = environ['dataset_id']
    key = ('get_dataset', dataset_id)
    if key not in CACHED_RETURN_VALS:
        # Cache return value for the environment.
        CACHED_RETURN_VALS[key] = datastore.get_dataset(dataset_id)
    return CACHED_RETURN_VALS[key]


def get_storage_connection():
    environ = get_environ(require_storage=True)
    project_id = environ['project_id']
    key = ('get_storage_connection', project_id)
    if key not in CACHED_RETURN_VALS:
        # Cache return value for the environment.
        CACHED_RETURN_VALS[key] = storage.get_connection(project_id)
    return CACHED_RETURN_VALS[key]
