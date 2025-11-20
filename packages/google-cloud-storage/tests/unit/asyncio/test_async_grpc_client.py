# Copyright 2025 Google LLC
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
from unittest import mock
from google.auth import credentials as auth_credentials
from google.auth.credentials import AnonymousCredentials


def _make_credentials(spec=None):
    if spec is None:
        return mock.Mock(spec=auth_credentials.Credentials)
    return mock.Mock(spec=spec)


class TestAsyncGrpcClient(unittest.TestCase):
    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_default_options(self, mock_async_storage_client):
        from google.cloud.storage._experimental.asyncio import async_grpc_client

        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        async_grpc_client.AsyncGrpcClient(credentials=mock_creds)

        mock_async_storage_client.get_transport_class.assert_called_once_with(
            "grpc_asyncio"
        )
        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=True, credentials=mock_creds
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(channel=mock_channel)
        mock_transport = mock_transport_cls.return_value
        mock_async_storage_client.assert_called_once_with(
            transport=mock_transport,
            client_options=None,
            client_info=None,
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_disables_directpath(self, mock_async_storage_client):
        from google.cloud.storage._experimental.asyncio import async_grpc_client

        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds, attempt_direct_path=False
        )

        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=False, credentials=mock_creds
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(channel=mock_channel)

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_grpc_client_property(self, mock_grpc_gapic_client):
        from google.cloud.storage._experimental.asyncio import async_grpc_client

        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_grpc_gapic_client.get_transport_class.return_value = mock_transport_cls
        channel_sentinel = mock.sentinel.channel

        mock_transport_cls.create_channel.return_value = channel_sentinel
        mock_transport_cls.return_value = mock.sentinel.transport

        mock_creds = _make_credentials()
        mock_client_info = mock.sentinel.client_info
        mock_client_options = mock.sentinel.client_options
        mock_attempt_direct_path = mock.sentinel.attempt_direct_path

        # Act
        client = async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds,
            client_info=mock_client_info,
            client_options=mock_client_options,
            attempt_direct_path=mock_attempt_direct_path,
        )

        mock_grpc_gapic_client.get_transport_class.return_value = mock_transport_cls

        mock_transport_cls.create_channel.return_value = channel_sentinel
        mock_transport_instance = mock.sentinel.transport
        mock_transport_cls.return_value = mock_transport_instance

        retrieved_client = client.grpc_client

        # Assert
        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=mock_attempt_direct_path, credentials=mock_creds
        )
        mock_transport_cls.assere_with(channel=channel_sentinel)
        mock_grpc_gapic_client.assert_called_once_with(
            transport=mock_transport_instance,
            client_info=mock_client_info,
            client_options=mock_client_options,
        )
        self.assertIs(retrieved_client, mock_grpc_gapic_client.return_value)

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_grpc_client_with_anon_creds(self, mock_grpc_gapic_client):
        from google.cloud.storage._experimental.asyncio import async_grpc_client

        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_grpc_gapic_client.get_transport_class.return_value = mock_transport_cls
        channel_sentinel = mock.sentinel.channel

        mock_transport_cls.create_channel.return_value = channel_sentinel
        mock_transport_cls.return_value = mock.sentinel.transport

        # Act
        anonymous_creds = AnonymousCredentials()
        client = async_grpc_client.AsyncGrpcClient(credentials=anonymous_creds)
        retrieved_client = client.grpc_client

        # Assert
        self.assertIs(retrieved_client, mock_grpc_gapic_client.return_value)

        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=True, credentials=anonymous_creds
        )
        mock_transport_cls.assert_called_once_with(channel=channel_sentinel)
