# Copyright 2016 Google Inc.
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

import datetime

import mock
import pytest

from google.auth import credentials
try:
    import google.auth.transport.grpc
    HAS_GRPC = True
except ImportError:  # pragma: NO COVER
    HAS_GRPC = False


pytestmark = pytest.mark.skipif(not HAS_GRPC, reason='gRPC is unavailable.')


class MockCredentials(credentials.Credentials):
    def __init__(self, token='token'):
        super(MockCredentials, self).__init__()
        self.token = token
        self.expiry = None

    def refresh(self, request):
        self.token += '1'


class TestAuthMetadataPlugin(object):
    def test_call_no_refresh(self):
        credentials = MockCredentials()
        request = mock.Mock()

        plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, request)

        context = mock.Mock()
        callback = mock.Mock()

        plugin(context, callback)

        assert callback.called_once_with(
            [('authorization', 'Bearer {}'.format(credentials.token))], None)

    def test_call_refresh(self):
        credentials = MockCredentials()
        credentials.expiry = datetime.datetime.min
        request = mock.Mock()

        plugin = google.auth.transport.grpc.AuthMetadataPlugin(
            credentials, request)

        context = mock.Mock()
        callback = mock.Mock()

        plugin(context, callback)

        assert credentials.token == 'token1'
        assert callback.called_once_with(
            [('authorization', 'Bearer {}'.format(credentials.token))], None)


@mock.patch('grpc.composite_channel_credentials', autospec=True)
@mock.patch('grpc.metadata_call_credentials', autospec=True)
@mock.patch('grpc.ssl_channel_credentials', autospec=True)
@mock.patch('grpc.secure_channel', autospec=True)
def test_secure_authorized_channel(
        secure_channel, ssl_channel_credentials, metadata_call_credentials,
        composite_channel_credentials):
    credentials = mock.Mock()
    request = mock.Mock()
    target = 'example.com:80'

    channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, request, target, options=mock.sentinel.options)

    # Check the auth plugin construction.
    auth_plugin = metadata_call_credentials.call_args[0][0]
    assert isinstance(
        auth_plugin, google.auth.transport.grpc.AuthMetadataPlugin)
    assert auth_plugin._credentials == credentials
    assert auth_plugin._request == request

    # Check the ssl channel call.
    assert ssl_channel_credentials.called

    # Check the composite credentials call.
    composite_channel_credentials.assert_called_once_with(
        ssl_channel_credentials.return_value,
        metadata_call_credentials.return_value)

    # Check the channel call.
    secure_channel.assert_called_once_with(
        target, composite_channel_credentials.return_value,
        options=mock.sentinel.options)
    assert channel == secure_channel.return_value


@mock.patch('grpc.composite_channel_credentials', autospec=True)
@mock.patch('grpc.metadata_call_credentials', autospec=True)
@mock.patch('grpc.ssl_channel_credentials', autospec=True)
@mock.patch('grpc.secure_channel', autospec=True)
def test_secure_authorized_channel_explicit_ssl(
        secure_channel, ssl_channel_credentials, metadata_call_credentials,
        composite_channel_credentials):
    credentials = mock.Mock()
    request = mock.Mock()
    target = 'example.com:80'
    ssl_credentials = mock.Mock()

    google.auth.transport.grpc.secure_authorized_channel(
        credentials, request, target, ssl_credentials=ssl_credentials)

    # Check the ssl channel call.
    assert not ssl_channel_credentials.called

    # Check the composite credentials call.
    composite_channel_credentials.assert_called_once_with(
        ssl_credentials,
        metadata_call_credentials.return_value)
