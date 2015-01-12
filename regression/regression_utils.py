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
import types

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


class RetryTestsMetaclass(type):

    NUM_RETRIES = 2
    FLAKY_ERROR_CLASSES = (AssertionError,)

    @staticmethod
    def _wrap_class_attr(class_attr):
        if not (isinstance(class_attr, types.FunctionType) and
                class_attr.__name__.startswith('test_')):
            return class_attr

        def retry_function(self):
            num_attempts = 0
            while num_attempts < RetryTestsMetaclass.NUM_RETRIES:
                try:
                    return class_attr(self)
                except RetryTestsMetaclass.FLAKY_ERROR_CLASSES:
                    num_attempts += 1
                    if num_attempts == RetryTestsMetaclass.NUM_RETRIES:
                        raise

        return retry_function

    def __new__(mcs, name, bases, attrs):
        new_attrs = {}
        for attr_name, value in attrs.items():
            new_attrs[attr_name] = mcs._wrap_class_attr(value)

        return super(RetryTestsMetaclass, mcs).__new__(
            mcs, name, bases, new_attrs)


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


def get_storage_connection():
    environ = get_environ(require_storage=True)
    project_id = environ['project_id']
    key = ('get_storage_connection', project_id)
    if key not in CACHED_RETURN_VALS:
        # Cache return value for the environment.
        CACHED_RETURN_VALS[key] = storage.get_connection(project_id)
    return CACHED_RETURN_VALS[key]
