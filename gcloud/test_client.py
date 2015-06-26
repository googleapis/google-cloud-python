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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_explict(self):
        CREDENTIALS = object()
        HTTP = object()
        CLIENT_OBJ = self._makeOne(credentials=CREDENTIALS, http=HTTP)
        self.assertTrue(CLIENT_OBJ.credentials is CREDENTIALS)
        self.assertTrue(CLIENT_OBJ.http is HTTP)

    def test_from_service_account_json(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        _CALLED = []

        def mock_creds(arg1):
            _CALLED.append((arg1,))
            return CREDENTIALS

        BOGUS_ARG = object()
        with _Monkey(client, get_for_service_account_json=mock_creds):
            CLIENT_OBJ = KLASS.from_service_account_json(BOGUS_ARG)

        self.assertTrue(CLIENT_OBJ.credentials is CREDENTIALS)
        self.assertEqual(_CALLED, [(BOGUS_ARG,)])

    def test_from_service_account_json_fail(self):
        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_json, None,
                          credentials=CREDENTIALS)

    def test_from_service_account_p12(self):
        from gcloud._testing import _Monkey
        from gcloud import client

        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        _CALLED = []

        def mock_creds(arg1, arg2):
            _CALLED.append((arg1, arg2))
            return CREDENTIALS

        BOGUS_ARG1 = object()
        BOGUS_ARG2 = object()
        with _Monkey(client, get_for_service_account_p12=mock_creds):
            CLIENT_OBJ = KLASS.from_service_account_p12(BOGUS_ARG1, BOGUS_ARG2)

        self.assertTrue(CLIENT_OBJ.credentials is CREDENTIALS)
        self.assertEqual(_CALLED, [(BOGUS_ARG1, BOGUS_ARG2)])

    def test_from_service_account_p12_fail(self):
        KLASS = self._getTargetClass()
        CREDENTIALS = object()
        self.assertRaises(TypeError, KLASS.from_service_account_p12, None,
                          None, credentials=CREDENTIALS)
