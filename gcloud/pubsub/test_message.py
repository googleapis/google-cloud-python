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


class TestMessage(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.message import Message
        return Message

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_no_attrs(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        message = self._makeOne(data=DATA, message_id=MESSAGE_ID)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attrs, {})

    def test_ctor_w_attrs(self):
        DATA = b'DEADBEEF'
        MESSAGE_ID = b'12345'
        ATTRS = {'a': 'b'}
        message = self._makeOne(data=DATA, message_id=MESSAGE_ID,
                                attributes=ATTRS)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attrs, ATTRS)

    def test_from_api_repr_no_attrs(self):
        from base64 import b64encode as b64
        DATA = b'DEADBEEF'
        B64_DATA = b64(DATA)
        MESSAGE_ID = '12345'
        api_repr = {'data': B64_DATA, 'messageId': MESSAGE_ID}
        message = self._getTargetClass().from_api_repr(api_repr)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attrs, {})

    def test_from_api_repr_w_attrs(self):
        from base64 import b64encode as b64
        DATA = b'DEADBEEF'
        B64_DATA = b64(DATA)
        MESSAGE_ID = '12345'
        ATTRS = {'a': 'b'}
        api_repr = {'data': B64_DATA,
                    'messageId': MESSAGE_ID,
                    'attributes': ATTRS}
        message = self._getTargetClass().from_api_repr(api_repr)
        self.assertEqual(message.data, DATA)
        self.assertEqual(message.message_id, MESSAGE_ID)
        self.assertEqual(message.attrs, ATTRS)
