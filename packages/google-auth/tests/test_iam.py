# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import datetime
import json

import mock
import pytest
from six.moves import http_client

from google.auth import exceptions
from google.auth import iam
from google.auth import transport
import google.auth.credentials


def make_request(status, data=None):
    response = mock.Mock(spec=transport.Response)
    response.status = status

    if data is not None:
        response.data = json.dumps(data).encode('utf-8')

    return mock.Mock(return_value=response, spec=transport.Request)


def make_credentials():
    class CredentialsImpl(google.auth.credentials.Credentials):
        def __init__(self):
            super(CredentialsImpl, self).__init__()
            self.token = 'token'
            # Force refresh
            self.expiry = datetime.datetime.min

        def refresh(self, request):
            pass

    return CredentialsImpl()


class TestSigner(object):
    def test_constructor(self):
        request = mock.sentinel.request
        credentials = mock.Mock(spec=google.auth.credentials.Credentials)

        signer = iam.Signer(
            request, credentials, mock.sentinel.service_account_email)

        assert signer._request == mock.sentinel.request
        assert signer._credentials == credentials
        assert (signer._service_account_email ==
                mock.sentinel.service_account_email)

    def test_key_id(self):
        key_id = '123'
        request = make_request(http_client.OK, data={'keyId': key_id})
        credentials = make_credentials()

        signer = iam.Signer(
            request, credentials, mock.sentinel.service_account_email)

        assert signer.key_id == '123'
        auth_header = request.call_args[1]['headers']['authorization']
        assert auth_header == 'Bearer token'

    def test_sign_bytes(self):
        signature = b'DEADBEEF'
        encoded_signature = base64.b64encode(signature).decode('utf-8')
        request = make_request(
            http_client.OK, data={'signature': encoded_signature})
        credentials = make_credentials()

        signer = iam.Signer(
            request, credentials, mock.sentinel.service_account_email)

        returned_signature = signer.sign('123')

        assert returned_signature == signature

    def test_sign_bytes_failure(self):
        request = make_request(http_client.UNAUTHORIZED)
        credentials = make_credentials()

        signer = iam.Signer(
            request, credentials, mock.sentinel.service_account_email)

        with pytest.raises(exceptions.TransportError):
            signer.sign('123')
