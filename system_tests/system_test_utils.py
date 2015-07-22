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

from gcloud._environment_vars import _CREDENTIALS_ENV_VAR_NAME
from gcloud._environment_vars import _TESTS_DATASET_ENV_VAR_NAME
from gcloud._environment_vars import _TESTS_PROJECT_ENV_VAR_NAME


# From shell environ. May be None.
PROJECT_ID = os.getenv(_TESTS_PROJECT_ENV_VAR_NAME)
DATASET_ID = os.getenv(_TESTS_DATASET_ENV_VAR_NAME)
CREDENTIALS = os.getenv(_CREDENTIALS_ENV_VAR_NAME)

ENVIRON_ERROR_MSG = """\
To run the system tests, you need to set some environment variables.
Please check the CONTRIBUTING guide for instructions.
"""


def check_environ(require_datastore=False, require_storage=False,
                  require_pubsub=False):
    if require_datastore:
        if DATASET_ID is None or not os.path.isfile(CREDENTIALS):
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)

    if require_storage or require_pubsub:
        if PROJECT_ID is None or not os.path.isfile(CREDENTIALS):
            print(ENVIRON_ERROR_MSG, file=sys.stderr)
            sys.exit(1)
