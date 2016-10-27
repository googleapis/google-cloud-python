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


class TestClient(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.runtimeconfig.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_config(self):
        PROJECT = 'PROJECT'
        CONFIG_NAME = 'config_name'
        creds = _Credentials()

        client_obj = self._makeOne(project=PROJECT, credentials=creds)
        new_config = client_obj.config(CONFIG_NAME)
        self.assertEqual(new_config.name, CONFIG_NAME)
        self.assertIs(new_config._client, client_obj)
        self.assertEqual(new_config.project, PROJECT)
        self.assertEqual(new_config.full_name,
                         'projects/%s/configs/%s' % (PROJECT, CONFIG_NAME))
        self.assertFalse(new_config.description)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
