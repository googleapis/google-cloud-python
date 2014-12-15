# Copyright 2014 Google Inc. All rights reserved.
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


class TestCredentials(unittest2.TestCase):

    def test_get_for_service_account_wo_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account(CLIENT_EMAIL,
                                                            file_obj.name)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': None,
        }
        self.assertEqual(client._called_with, expected_called_with)

    def test_get_for_service_account_w_scope(self):
        from tempfile import NamedTemporaryFile
        from gcloud import credentials
        from gcloud._testing import _Monkey
        CLIENT_EMAIL = 'phred@example.com'
        PRIVATE_KEY = 'SEEkR1t'
        SCOPE = 'SCOPE'
        client = _Client()
        with _Monkey(credentials, client=client):
            with NamedTemporaryFile() as file_obj:
                file_obj.write(PRIVATE_KEY)
                file_obj.flush()
                found = credentials.get_for_service_account(
                    CLIENT_EMAIL, file_obj.name, SCOPE)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class _Client(object):
    def __init__(self):
        self._signed = object()

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed
