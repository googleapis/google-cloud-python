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


class Test_entry_from_resource(unittest.TestCase):

    @staticmethod
    def _call_fut(resource, client, loggers):
        from google.cloud.logging._helpers import entry_from_resource

        return entry_from_resource(resource, client, loggers)

    def test_unknown_type(self):
        with self.assertRaises(ValueError):
            self._call_fut({}, None, {})

    def _payload_helper(self, key, class_name):
        import mock

        resource = {key: 'yup'}
        client = object()
        loggers = {}
        mock_class = EntryMock()

        name = 'google.cloud.logging._helpers.' + class_name
        with mock.patch(name, new=mock_class):
            result = self._call_fut(resource, client, loggers)

        self.assertIs(result, mock_class.sentinel)
        self.assertEqual(mock_class.called, (resource, client, loggers))

    def test_text_payload(self):
        self._payload_helper('textPayload', 'TextEntry')

    def test_json_payload(self):
        self._payload_helper('jsonPayload', 'StructEntry')

    def test_proto_payload(self):
        self._payload_helper('protoPayload', 'ProtobufEntry')


class EntryMock(object):

    def __init__(self):
        self.sentinel = object()
        self.called = None

    def from_api_repr(self, resource, client, loggers):
        self.called = (resource, client, loggers)
        return self.sentinel
