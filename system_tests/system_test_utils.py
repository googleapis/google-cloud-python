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

from gcloud.environment_vars import CREDENTIALS as TEST_CREDENTIALS
from gcloud.environment_vars import TESTS_DATASET
from gcloud.environment_vars import TESTS_PROJECT


# From shell environ. May be None.
PROJECT_ID = os.getenv(TESTS_PROJECT)
DATASET_ID = os.getenv(TESTS_DATASET)
CREDENTIALS = os.getenv(TEST_CREDENTIALS)

ENVIRON_ERROR_MSG = """\
To run the system tests, you need to set some environment variables.
Please check the CONTRIBUTING guide for instructions.

Missing variables: %s
"""


def check_environ(*requirements):

    missing = []

    if 'dataset_id' in requirements:
        if DATASET_ID is None:
            missing.append(TESTS_DATASET)

    if 'project' in requirements:
        if PROJECT_ID is None:
            missing.append(TESTS_PROJECT)

    if 'credentials' in requirements:
        if CREDENTIALS is None or not os.path.isfile(CREDENTIALS):
            missing.append(TEST_CREDENTIALS)

    if missing:
        print(ENVIRON_ERROR_MSG % ', '.join(missing), file=sys.stderr)
        sys.exit(1)
