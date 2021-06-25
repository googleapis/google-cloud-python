# Copyright 2021 Google LLC
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


class TestStatus(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.error import Status

        return Status

    @staticmethod
    def _make_status_pb(**kwargs):
        from google.rpc.status_pb2 import Status

        return Status(**kwargs)

    def _make_one(self, status_pb):
        return self._get_target_class()(status_pb)

    def test_ctor(self):
        status_pb = self._make_status_pb()
        status = self._make_one(status_pb)
        self.assertIs(status.status_pb, status_pb)

    def test_code(self):
        code = 123
        status_pb = self._make_status_pb(code=code)
        status = self._make_one(status_pb)
        self.assertEqual(status.code, code)

    def test_message(self):
        message = "message"
        status_pb = self._make_status_pb(message=message)
        status = self._make_one(status_pb)
        self.assertEqual(status.message, message)

    def test___eq___self(self):
        status_pb = self._make_status_pb()
        status = self._make_one(status_pb)
        self.assertTrue(status == status)

    def test___eq___other_hit(self):
        status_pb = self._make_status_pb(code=123, message="message")
        status = self._make_one(status_pb)
        other = self._make_one(status_pb)
        self.assertTrue(status == other)

    def test___eq___other_miss(self):
        status_pb = self._make_status_pb(code=123, message="message")
        other_status_pb = self._make_status_pb(code=456, message="oops")
        status = self._make_one(status_pb)
        other = self._make_one(other_status_pb)
        self.assertFalse(status == other)

    def test___eq___wrong_type(self):
        status_pb = self._make_status_pb(code=123, message="message")
        status = self._make_one(status_pb)
        other = object()
        self.assertFalse(status == other)

    def test___ne___self(self):
        status_pb = self._make_status_pb()
        status = self._make_one(status_pb)
        self.assertFalse(status != status)

    def test___ne___other_hit(self):
        status_pb = self._make_status_pb(code=123, message="message")
        status = self._make_one(status_pb)
        other = self._make_one(status_pb)
        self.assertFalse(status != other)

    def test___ne___other_miss(self):
        status_pb = self._make_status_pb(code=123, message="message")
        other_status_pb = self._make_status_pb(code=456, message="oops")
        status = self._make_one(status_pb)
        other = self._make_one(other_status_pb)
        self.assertTrue(status != other)

    def test___ne___wrong_type(self):
        status_pb = self._make_status_pb(code=123, message="message")
        status = self._make_one(status_pb)
        other = object()
        self.assertTrue(status != other)
