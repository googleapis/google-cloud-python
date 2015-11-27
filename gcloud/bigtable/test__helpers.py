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


class TestMetadataTransformer(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable._helpers import MetadataTransformer
        return MetadataTransformer

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud.bigtable.client import Client
        from gcloud.bigtable.client import DATA_SCOPE

        credentials = _Credentials()
        project = 'PROJECT'
        user_agent = 'USER_AGENT'
        client = Client(project=project, credentials=credentials,
                        user_agent=user_agent)
        transformer = self._makeOne(client)
        self.assertTrue(transformer._credentials is credentials)
        self.assertEqual(transformer._user_agent, user_agent)
        self.assertEqual(credentials._scopes, [DATA_SCOPE])

    def test___call__(self):
        from gcloud.bigtable.client import Client
        from gcloud.bigtable.client import DATA_SCOPE
        from gcloud.bigtable.client import DEFAULT_USER_AGENT

        access_token_expected = 'FOOBARBAZ'
        credentials = _Credentials(access_token=access_token_expected)
        project = 'PROJECT'
        client = Client(project=project, credentials=credentials)

        transformer = self._makeOne(client)
        result = transformer(None)
        self.assertEqual(
            result,
            [
                ('Authorization', 'Bearer ' + access_token_expected),
                ('User-agent', DEFAULT_USER_AGENT),
            ])
        self.assertEqual(credentials._scopes, [DATA_SCOPE])
        self.assertEqual(len(credentials._tokens), 1)


class Test_get_certs(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable._helpers import get_certs
        return get_certs(*args, **kwargs)

    def test_it(self):
        import tempfile
        from gcloud._testing import _Monkey
        from gcloud.bigtable import _helpers as MUT

        # Just write to a mock file.
        filename = tempfile.mktemp()
        contents = b'FOOBARBAZ'
        with open(filename, 'wb') as file_obj:
            file_obj.write(contents)

        with _Monkey(MUT, SSL_CERT_FILE=filename):
            result = self._callFUT()

        self.assertEqual(result, contents)


class Test_make_stub(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable._helpers import make_stub
        return make_stub(*args, **kwargs)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable import _helpers as MUT

        mock_result = object()
        stub_inputs = []

        CLIENT_CREDS = object()
        CHANNEL = object()

        class _ImplementationsModule(object):

            def __init__(self):
                self.ssl_client_credentials_args = None
                self.secure_channel_args = None

            def ssl_client_credentials(self, *args, **kwargs):
                self.ssl_client_credentials_args = (args, kwargs)
                return CLIENT_CREDS

            def secure_channel(self, *args, **kwargs):
                self.secure_channel_args = (args, kwargs)
                return CHANNEL

        implementations_mod = _ImplementationsModule()

        def mock_stub_factory(channel, metadata_transformer=None):
            stub_inputs.append((channel, metadata_transformer))
            return mock_result

        transformed = object()
        clients = []

        def mock_transformer(client):
            clients.append(client)
            return transformed

        host = 'HOST'
        port = 1025
        certs = 'FOOBAR'
        client = object()
        with _Monkey(MUT, get_certs=lambda: certs,
                     implementations=implementations_mod,
                     MetadataTransformer=mock_transformer):
            result = self._callFUT(client, mock_stub_factory, host, port)

        self.assertTrue(result is mock_result)
        self.assertEqual(stub_inputs, [(CHANNEL, transformed)])
        self.assertEqual(clients, [client])
        ssl_cli_kwargs = {'private_key': None, 'certificate_chain': None}
        self.assertEqual(implementations_mod.ssl_client_credentials_args,
                         ((certs,), ssl_cli_kwargs))
        self.assertEqual(implementations_mod.secure_channel_args,
                         ((host, port, CLIENT_CREDS), {}))


class _Credentials(object):

    _scopes = None

    def __init__(self, access_token=None):
        self._access_token = access_token
        self._tokens = []

    def get_access_token(self):
        from oauth2client.client import AccessTokenInfo
        token = AccessTokenInfo(access_token=self._access_token,
                                expires_in=None)
        self._tokens.append(token)
        return token

    def create_scoped(self, scope):
        self._scopes = scope
        return self
