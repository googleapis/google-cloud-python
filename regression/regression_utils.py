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


# From shell environ. May be None.
PROJECT_ID = os.getenv('GCLOUD_TESTS_PROJECT_ID')
DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

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
