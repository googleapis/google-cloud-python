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


class Test_get_for_service_account_p12(unittest2.TestCase):

    def _callFUT(self, client_email, private_key_path, scope=None):
        from gcloud.credentials import get_for_service_account_p12
        return get_for_service_account_p12(client_email, private_key_path,
                                           scope=scope)

    def test_wo_scope(self):
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
                found = self._callFUT(CLIENT_EMAIL, file_obj.name)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': None,
        }
        self.assertEqual(client._called_with, expected_called_with)

    def test_w_scope(self):
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
                found = self._callFUT(CLIENT_EMAIL, file_obj.name,
                                      scope=SCOPE)
        self.assertTrue(found is client._signed)
        expected_called_with = {
            'service_account_name': CLIENT_EMAIL,
            'private_key': PRIVATE_KEY,
            'scope': SCOPE,
        }
        self.assertEqual(client._called_with, expected_called_with)


class Test__store_user_credential(unittest2.TestCase):

    def _callFUT(self, credential):
        from gcloud.credentials import _store_user_credential
        return _store_user_credential(credential)

    def test_user_input_no(self):
        import six.moves
        from gcloud._testing import _Monkey

        _called_messages = []

        def fake_input(message):
            _called_messages.append(message)
            # 'y' or 'Y' are the only acceptable values.
            return 'neither yes nor no'

        with _Monkey(six.moves, input=fake_input):
            self._callFUT(None)

        self.assertEqual(
            _called_messages,
            ['Would you like to store your tokens for future use? [y/n] '])

    def test_user_input_yes(self):
        import json
        import six.moves
        import tempfile

        from gcloud._testing import _Monkey
        from oauth2client.client import OAuth2Credentials

        _called_messages = []
        # In reverse order so we can use .pop().
        TEMPFILE = tempfile.mktemp()
        responses = [TEMPFILE, 'y']

        def fake_input(message):
            _called_messages.append(message)
            return responses.pop()

        CLIENT_ID = 'FOO'
        CLIENT_SECRET = 'BAR'
        REFRESH_TOKEN = 'BAZ'
        CREDENTIALS = OAuth2Credentials(None, CLIENT_ID, CLIENT_SECRET,
                                        REFRESH_TOKEN, None, None, None)
        with _Monkey(six.moves, input=fake_input):
            self._callFUT(CREDENTIALS)

        self.assertEqual(
            _called_messages,
            ['Would you like to store your tokens for future use? [y/n] ',
             'Please name the file where you wish to store them: '])

        with open(TEMPFILE, 'r') as file_obj:
            STORED_CREDS = json.load(file_obj)

        expected_creds = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'type': 'authorized_user',
        }
        self.assertEqual(STORED_CREDS, expected_creds)


class Test_get_credentials_from_user_flow(unittest2.TestCase):

    def _callFUT(self, scope, client_secrets_file=None):
        from gcloud.credentials import get_credentials_from_user_flow
        return get_credentials_from_user_flow(
            scope, client_secrets_file=client_secrets_file)

    def test_no_tty(self):
        import sys
        from gcloud._testing import _Monkey

        STDOUT = _MockStdout(isatty=False)
        with _Monkey(sys, stdout=STDOUT):
            with self.assertRaises(EnvironmentError):
                self._callFUT(None)

    def test_no_filename(self):
        import os
        import sys

        from gcloud._testing import _Monkey

        STDOUT = _MockStdout(isatty=True)
        FAKE_ENVIRON = {}
        GCLOUD_KEY = 'GCLOUD_CLIENT_SECRETS'

        _called_keys = []

        def fake_getenv(key):
            _called_keys.append(key)
            return FAKE_ENVIRON.get(key)

        with _Monkey(sys, stdout=STDOUT):
            with _Monkey(os, getenv=fake_getenv):
                with self.assertRaises(ValueError):
                    self._callFUT(None)

        self.assertEqual(_called_keys, [GCLOUD_KEY])

    def test_filename_from_environ(self):
        import os
        import sys

        from gcloud._testing import _Monkey
        from oauth2client import client

        STDOUT = _MockStdout(isatty=True)
        FILENAME = 'FOO'
        GCLOUD_KEY = 'GCLOUD_CLIENT_SECRETS'
        FAKE_ENVIRON = {GCLOUD_KEY: FILENAME}

        _called_keys = []

        def fake_getenv(key):
            _called_keys.append(key)
            return FAKE_ENVIRON.get(key)

        _called_filenames = []

        def fake_loadfile(filename):
            _called_filenames.append(filename)
            return 'NOT_INSTALLED_TYPE', None

        with _Monkey(sys, stdout=STDOUT):
            with _Monkey(os, getenv=fake_getenv):
                with _Monkey(client.clientsecrets, loadfile=fake_loadfile):
                    with self.assertRaises(ValueError):
                        self._callFUT(None)

        self.assertEqual(_called_keys, [GCLOUD_KEY])
        self.assertEqual(_called_filenames, [FILENAME])

    def test_succeeds(self):
        import argparse
        import sys

        from gcloud._testing import _Monkey
        from gcloud import credentials
        from oauth2client import client
        from oauth2client.file import Storage
        from oauth2client import tools

        STDOUT = _MockStdout(isatty=True)
        SCOPE = 'SCOPE'
        FILENAME = 'FILENAME'
        REDIRECT_URI = 'REDIRECT_URI'
        MOCK_CLIENT_INFO = {'redirect_uris': [REDIRECT_URI]}
        FLOW = object()
        CLIENT_ID = 'FOO'
        CLIENT_SECRET = 'BAR'
        REFRESH_TOKEN = 'BAZ'
        CREDENTIALS = client.OAuth2Credentials(None, CLIENT_ID, CLIENT_SECRET,
                                               REFRESH_TOKEN, None, None, None)

        _called_loadfile = []

        def fake_loadfile(*args, **kwargs):
            _called_loadfile.append((args, kwargs))
            return client.clientsecrets.TYPE_INSTALLED, MOCK_CLIENT_INFO

        _called_flow_from_clientsecrets = []

        def mock_flow(client_secrets_file, scope, redirect_uri=None):
            _called_flow_from_clientsecrets.append(
                (client_secrets_file, scope, redirect_uri))
            return FLOW

        _called_run_flow = []

        def mock_run_flow(flow, storage, flags):
            _called_run_flow.append((flow, storage, flags))
            return CREDENTIALS

        _called_store_user_credential = []

        def store_cred(credential):
            _called_store_user_credential.append(credential)

        with _Monkey(sys, stdout=STDOUT):
            with _Monkey(client.clientsecrets, loadfile=fake_loadfile):
                with _Monkey(client, flow_from_clientsecrets=mock_flow):
                    with _Monkey(tools, run_flow=mock_run_flow):
                        with _Monkey(credentials,
                                     _store_user_credential=store_cred):
                            with _Monkey(argparse,
                                         ArgumentParser=_MockArgumentParser):
                                self._callFUT(SCOPE,
                                              client_secrets_file=FILENAME)

        self.assertEqual(_called_loadfile, [((FILENAME,), {})])
        self.assertEqual(_called_flow_from_clientsecrets,
                         [(FILENAME, SCOPE, REDIRECT_URI)])

        # Unpack expects a single output
        run_flow_input, = _called_run_flow
        self.assertEqual(len(run_flow_input), 3)
        self.assertEqual(run_flow_input[0], FLOW)
        self.assertTrue(isinstance(run_flow_input[1], Storage))
        self.assertTrue(run_flow_input[2] is _MockArgumentParser._MARKER)

        self.assertEqual(_called_store_user_credential, [CREDENTIALS])


class _Credentials(object):

    service_account_name = 'testing@example.com'

    def create_scoped(self, scopes):
        self._scopes = scopes
        return self


class _Client(object):
    def __init__(self):
        self._signed = _Credentials()

        class GoogleCredentials(object):
            @staticmethod
            def get_application_default():
                self._get_app_default_called = True
                return self._signed

        self.GoogleCredentials = GoogleCredentials

    def SignedJwtAssertionCredentials(self, **kw):
        self._called_with = kw
        return self._signed


class _MockStdout(object):

    def __init__(self, isatty=True):
        self._isatty = isatty

    def isatty(self):
        return self._isatty


class _MockArgumentParser(object):

    _MARKER = object()

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def parse_args(self):
        return self._MARKER
