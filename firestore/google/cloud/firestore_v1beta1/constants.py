# Copyright 2017 Google LLC All rights reserved.
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

"""Helpful constants to use for Google Cloud Firestore."""


class sentinel(object):
    """Class for sentinel values, so they print nicely."""

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

    def __eq__(self, other):
        raise NotImplementedError('use "is" to compare sentinels')

    def __ne__(self, other):
        raise NotImplementedError('use "is" to compare sentinels')


DELETE_FIELD = sentinel('DELETE_FIELD')  # Sentinel object.
"""Sentinel value used to delete a field in a document."""

SERVER_TIMESTAMP = sentinel('SERVER_TIMESTAMP')  # Sentinel object.
"""Sentinel value: set a document field to the server timestamp."""
