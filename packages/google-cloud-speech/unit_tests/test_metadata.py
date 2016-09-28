# Copyright 2016 Google Inc.
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

import unittest


class TestMetadata(unittest.TestCase):
    OPERATION_ID = 123456789

    def _getTargetClass(self):
        from google.cloud.speech.metadata import Metadata
        return Metadata

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor(self):
        last_update = 'last_update'
        start_time = 'start_time'
        progress_percent = 23
        metadata = self._makeOne(last_update, start_time, progress_percent)
        self.assertEqual('last_update', metadata.last_update)
        self.assertEqual('start_time', metadata.start_time)
        self.assertEqual(23, metadata.progress_percent)

    def test_from_api_repr(self):
        import datetime
        from google.cloud._helpers import _rfc3339_to_datetime
        from unit_tests._fixtures import OPERATION_INCOMPLETE_RESPONSE as DATA
        METADATA = DATA['metadata']

        start_time = _rfc3339_to_datetime(METADATA['startTime'])
        last_update = _rfc3339_to_datetime(METADATA['lastUpdateTime'])
        metadata = self._getTargetClass().from_api_repr(METADATA)
        self.assertIsInstance(metadata.last_update, datetime.datetime)
        self.assertEqual(last_update, metadata.last_update)
        self.assertIsInstance(metadata.start_time, datetime.datetime)
        self.assertEqual(start_time, metadata.start_time)
        self.assertEqual(27, metadata.progress_percent)
