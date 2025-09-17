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
            attempt_direct_path=True
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(
            credentials=mock_creds, channel=mock_channel
        )
        mock_transport = mock_transport_cls.return_value
        mock_async_storage_client.assert_called_once_with(
            credentials=mock_creds,
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
            attempt_direct_path=False
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(
            credentials=mock_creds, channel=mock_channel
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_grpc_client_property(self, mock_async_storage_client):
        from google.cloud.storage._experimental.asyncio import async_grpc_client

        mock_creds = _make_credentials()

        client = async_grpc_client.AsyncGrpcClient(credentials=mock_creds)

        retrieved_client = client.grpc_client

        self.assertIs(retrieved_client, mock_async_storage_client.return_value)
