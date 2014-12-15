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

# pragma NO COVER
import os
from gcloud import datastore

__all__ = ['get_dataset', 'CLIENT_EMAIL', 'DATASET_ID', 'KEY_FILENAME']


DATASET_ID = os.getenv('GCLOUD_TESTS_DATASET_ID')
CLIENT_EMAIL = os.getenv('GCLOUD_TESTS_CLIENT_EMAIL')
KEY_FILENAME = os.getenv('GCLOUD_TESTS_KEY_FILE')


def get_dataset():  # pragma NO COVER
    return datastore.get_dataset(DATASET_ID, CLIENT_EMAIL, KEY_FILENAME)
