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


class Test__format_timestamp(unittest2.TestCase):

    def _callFUT(self, timestamp):
        from gcloud.monitoring._helpers import _format_timestamp
        return _format_timestamp(timestamp)

    def test_naive(self):
        from datetime import datetime
        TIMESTAMP = datetime(2016, 4, 5, 13, 30, 0)
        timestamp = self._callFUT(TIMESTAMP)
        self.assertEqual(timestamp, '2016-04-05T13:30:00Z')

    def test_with_timezone(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        TIMESTAMP = datetime(2016, 4, 5, 13, 30, 0, tzinfo=UTC)
        timestamp = self._callFUT(TIMESTAMP)
        self.assertEqual(timestamp, '2016-04-05T13:30:00Z')
