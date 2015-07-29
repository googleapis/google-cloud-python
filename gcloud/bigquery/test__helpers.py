# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class Test__millis(unittest2.TestCase):

    def _callFUT(self, value):
        from gcloud.bigquery._helpers import _millis
        return _millis(value)

    def test_one_second_from_epoch(self):
        import datetime
        import pytz
        WHEN = datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
        self.assertEqual(self._callFUT(WHEN), 1000)


class Test__datetime_from_prop(unittest2.TestCase):

    def _callFUT(self, value):
        from gcloud.bigquery._helpers import _datetime_from_prop
        return _datetime_from_prop(value)

    def test_w_none(self):
        self.assertTrue(self._callFUT(None) is None)

    def test_w_millis(self):
        import datetime
        import pytz
        from gcloud.bigquery._helpers import _total_seconds
        NOW = datetime.datetime(2015, 7, 29, 17, 45, 21, 123456,
                                tzinfo=pytz.utc)
        EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        MILLIS = _total_seconds(NOW - EPOCH) * 1000
        self.assertEqual(self._callFUT(MILLIS), NOW)


class Test__prop_from_datetime(unittest2.TestCase):

    def _callFUT(self, value):
        from gcloud.bigquery._helpers import _prop_from_datetime
        return _prop_from_datetime(value)

    def test_w_none(self):
        self.assertTrue(self._callFUT(None) is None)

    def test_w_utc_datetime(self):
        import datetime
        import pytz
        from gcloud.bigquery._helpers import _total_seconds
        NOW = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        MILLIS = int(_total_seconds(NOW - EPOCH) * 1000)
        result = self._callFUT(NOW)
        self.assertTrue(isinstance(result, int))
        self.assertEqual(result, MILLIS)

    def test_w_non_utc_datetime(self):
        import datetime
        import pytz
        from gcloud.bigquery._helpers import _total_seconds
        eastern = pytz.timezone('US/Eastern')
        NOW = datetime.datetime(2015, 7, 28, 16, 34, 47, tzinfo=eastern)
        EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        MILLIS = int(_total_seconds(NOW - EPOCH) * 1000)
        result = self._callFUT(NOW)
        self.assertTrue(isinstance(result, int))
        self.assertEqual(result, MILLIS)

    def test_w_naive_datetime(self):
        import datetime
        import pytz
        from gcloud.bigquery._helpers import _total_seconds
        NOW = datetime.datetime.utcnow()
        UTC_NOW = NOW.replace(tzinfo=pytz.utc)
        EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        MILLIS = int(_total_seconds(UTC_NOW - EPOCH) * 1000)
        result = self._callFUT(NOW)
        self.assertTrue(isinstance(result, int))
        self.assertEqual(result, MILLIS)
