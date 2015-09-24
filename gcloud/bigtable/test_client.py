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
        from gcloud.bigtable.client import Client
        return Client

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _constructor_test_helper(self, expected_scopes, creds,
                                 read_only=False, admin=False,
                                 user_agent=None, timeout_seconds=None,
                                 expected_creds=None):
        from gcloud.bigtable import client as MUT

        user_agent = user_agent or MUT.DEFAULT_USER_AGENT
        timeout_seconds = timeout_seconds or MUT.DEFAULT_TIMEOUT_SECONDS
        PROJECT = 'PROJECT'
        client = self._makeOne(project=PROJECT, credentials=creds,
                               read_only=read_only, admin=admin,
                               user_agent=user_agent,
                               timeout_seconds=timeout_seconds)

        expected_creds = expected_creds or creds
        self.assertTrue(client._credentials is expected_creds)
        self.assertEqual(client._credentials._scopes, expected_scopes)

        self.assertEqual(client.project, PROJECT)
        self.assertEqual(client.timeout_seconds, timeout_seconds)
        self.assertEqual(client.user_agent, user_agent)

    def test_constructor_default_scopes(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds)

    def test_constructor_custom_user_agent_and_timeout(self):
        from gcloud.bigtable import client as MUT

        timeout_seconds = 1337
        user_agent = 'custom-application'
        expected_scopes = [MUT.DATA_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds,
                                      user_agent=user_agent,
                                      timeout_seconds=timeout_seconds)

    def test_constructor_with_admin(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.DATA_SCOPE, MUT.ADMIN_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, admin=True)

    def test_constructor_with_read_only(self):
        from gcloud.bigtable import client as MUT

        expected_scopes = [MUT.READ_ONLY_SCOPE]
        creds = _Credentials()
        self._constructor_test_helper(expected_scopes, creds, read_only=True)

    def test_constructor_both_admin_and_read_only(self):
        creds = _Credentials()
        with self.assertRaises(ValueError):
            self._constructor_test_helper([], creds, admin=True,
                                          read_only=True)

    def test_constructor_implict_credentials(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import client as MUT

        creds = _Credentials()
        expected_scopes = [MUT.DATA_SCOPE]

        def mock_get_credentials():
            return creds

        with _Monkey(MUT, get_credentials=mock_get_credentials):
            self._constructor_test_helper(expected_scopes, None,
                                          expected_creds=creds)

    def test_credentials_getter(self):
        credentials = _Credentials()
        project = 'PROJECT'
        client = self._makeOne(project=project, credentials=credentials)
        self.assertTrue(client.credentials is credentials)


class _Credentials(object):

    _scopes = None

    def create_scoped(self, scope):
        self._scopes = scope
        return self
