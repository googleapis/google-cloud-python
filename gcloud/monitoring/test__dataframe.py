# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2


class Test__sorted_resource_labels(unittest2.TestCase):

    def _callFUT(self, labels):
        from gcloud.monitoring._dataframe import _sorted_resource_labels
        return _sorted_resource_labels(labels)

    def test_empty(self):
        self.assertEqual(self._callFUT([]), [])

    def test_sorted(self):
        from gcloud.monitoring._dataframe import TOP_RESOURCE_LABELS
        EXPECTED = TOP_RESOURCE_LABELS + ['other-1', 'other-2']
        self.assertEqual(self._callFUT(EXPECTED), EXPECTED)

    def test_reversed(self):
        from gcloud.monitoring._dataframe import TOP_RESOURCE_LABELS
        EXPECTED = TOP_RESOURCE_LABELS + ['other-1', 'other-2']
        INPUT = list(reversed(EXPECTED))
        self.assertEqual(self._callFUT(INPUT), EXPECTED)
