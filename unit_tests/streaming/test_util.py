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


class Test_calculate_wait_for_retry(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.streaming.util import calculate_wait_for_retry
        return calculate_wait_for_retry(*args, **kw)

    def test_w_negative_jitter_lt_max_wait(self):
        import random
        from google.cloud._testing import _Monkey
        with _Monkey(random, uniform=lambda lower, upper: lower):
            self.assertEqual(self._callFUT(1), 1.5)

    def test_w_positive_jitter_gt_max_wait(self):
        import random
        from google.cloud._testing import _Monkey
        with _Monkey(random, uniform=lambda lower, upper: upper):
            self.assertEqual(self._callFUT(4), 20)


class Test_acceptable_mime_type(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.streaming.util import acceptable_mime_type
        return acceptable_mime_type(*args, **kw)

    def test_pattern_wo_slash(self):
        with self.assertRaises(ValueError) as err:
            self._callFUT(['text/*'], 'BOGUS')
        self.assertEqual(
            err.exception.args,
            ('Invalid MIME type: "BOGUS"',))

    def test_accept_pattern_w_semicolon(self):
        with self.assertRaises(ValueError) as err:
            self._callFUT(['text/*;charset=utf-8'], 'text/plain')
        self.assertEqual(
            err.exception.args,
            ('MIME patterns with parameter unsupported: '
             '"text/*;charset=utf-8"',))

    def test_miss(self):
        self.assertFalse(self._callFUT(['image/*'], 'text/plain'))

    def test_hit(self):
        self.assertTrue(self._callFUT(['text/*'], 'text/plain'))
