# Copyright 2015 Google Inc.
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


class TestMessage(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.message import Message

        return Message

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_no_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        message = self._make_one(data=DATA, message_id=MESSAGE_ID)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attributes, {})
        self.assertIsNone(message.service_timestamp)

    def test_ctor_w_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        ATTRS = {'a': 'b'}
        message = self._make_one(data=DATA, message_id=MESSAGE_ID,
                                 attributes=ATTRS)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attributes, ATTRS)
        self.assertIsNone(message.service_timestamp)

    def test_timestamp_no_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        message = self._make_one(data=DATA, message_id=MESSAGE_ID)

        def _to_fail():
            return message.timestamp

        self.assertRaises(ValueError, _to_fail)

    def test_timestamp_wo_timestamp_in_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        ATTRS = {'a': 'b'}
        message = self._make_one(data=DATA, message_id=MESSAGE_ID,
                                 attributes=ATTRS)

        def _to_fail():
            return message.timestamp

        self.assertRaises(ValueError, _to_fail)

    def test_timestamp_w_timestamp_in_attributes(self):
        from datetime import datetime
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud._helpers import UTC

        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        TIMESTAMP = '2015-04-10T18:42:27.131956Z'
        naive = datetime.strptime(TIMESTAMP, _RFC3339_MICROS)
        timestamp = naive.replace(tzinfo=UTC)
        ATTRS = {'timestamp': TIMESTAMP}
        message = self._make_one(data=DATA, message_id=MESSAGE_ID,
                                 attributes=ATTRS)
        self.assertEqual(message.timestamp, timestamp)

    def test_from_api_repr_missing_data(self):
        MESSAGE_ID = '12345'
        api_repr = {'messageId': MESSAGE_ID}
        message = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(message.data, b'')
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attributes, {})
        self.assertIsNone(message.service_timestamp)

    def test_from_api_repr_no_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = '12345'
        TIMESTAMP = '2016-03-18-19:38:22.001393427Z'
        api_repr = {
            'data': DATA,
            'messageId': MESSAGE_ID,
            'publishTime': TIMESTAMP,
        }
        message = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attributes, {})
        self.assertEqual(message.service_timestamp, TIMESTAMP)

    def test_from_api_repr_w_attributes(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = '12345'
        ATTRS = {'a': 'b'}
        TIMESTAMP = '2016-03-18-19:38:22.001393427Z'
        api_repr = {
            'data': DATA,
            'messageId': MESSAGE_ID,
            'publishTime': TIMESTAMP,
            'attributes': ATTRS,
        }
        message = self._get_target_class().from_api_repr(api_repr)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.service_timestamp, TIMESTAMP)
        self.assertEqual(message.attributes, ATTRS)
