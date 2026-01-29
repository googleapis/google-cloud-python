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
from google.api_core import client_options as client_options_lib
from google.cloud.storage import grpc_client


def _make_credentials(spec=None):
    if spec is None:
        return mock.Mock(spec=auth_credentials.Credentials)
    return mock.Mock(spec=spec)


class TestGrpcClient(unittest.TestCase):
    @mock.patch("google.cloud.client.ClientWithProject.__init__")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_constructor_defaults_and_options(
        self, mock_storage_client, mock_base_client
    ):

        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials(spec=["_base", "_get_project_id"])
        mock_client_info = mock.Mock()
        client_options_dict = {"api_endpoint": "test.endpoint"}

        mock_base_instance = mock_base_client.return_value
        mock_base_instance._credentials = mock_creds

        client = grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_info=mock_client_info,
            client_options=client_options_dict,
        )

        # 1. Assert that the base class was initialized correctly.
        mock_base_client.assert_called_once_with(
            project="test-project", credentials=mock_creds
        )

        # 2. Assert DirectPath is ON by default.
        mock_storage_client.get_transport_class.assert_called_once_with("grpc")
        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=True
        )

        # 3. Assert the GAPIC client was created with the correct options.
        mock_transport = mock_transport_cls.return_value
        mock_storage_client.assert_called_once_with(
            credentials=mock_creds,
            transport=mock_transport,
            client_info=mock_client_info,
            client_options=client_options_dict,
        )

        # 4. Assert the client instance holds the mocked GAPIC client.
        self.assertIs(client.grpc_client, mock_storage_client.return_value)

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_constructor_disables_direct_path(
        self, mock_storage_client, mock_base_client
    ):

        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_base_instance = mock_base_client.return_value
        mock_base_instance._credentials = mock_creds

        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            attempt_direct_path=False,
        )

        mock_transport_cls.create_channel.assert_called_once_with(
            attempt_direct_path=False
        )

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_constructor_initialize_with_api_key(
        self, mock_storage_client, mock_base_client
    ):

        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_creds.project_id = None

        mock_base_instance = mock_base_client.return_value
        mock_base_instance._credentials = mock_creds

        # Instantiate with just the api_key.
        grpc_client.GrpcClient(
            project="test-project", credentials=mock_creds, api_key="test-api-key"
        )

        # Assert that the GAPIC client was called with client_options
        # that contains the api_key.
        mock_transport = mock_transport_cls.return_value
        mock_storage_client.assert_called_once_with(
            credentials=mock_creds,
            transport=mock_transport,
            client_info=None,
            client_options={"api_key": "test-api-key"},
        )

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_grpc_client_property(self, mock_storage_client, mock_base_client):

        mock_creds = _make_credentials()
        mock_base_client.return_value._credentials = mock_creds

        client = grpc_client.GrpcClient(project="test-project", credentials=mock_creds)

        retrieved_client = client.grpc_client

        self.assertIs(retrieved_client, mock_storage_client.return_value)

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_constructor_with_api_key_and_client_options(
        self, mock_storage_client, mock_base_client
    ):

        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_transport = mock_transport_cls.return_value

        mock_creds = _make_credentials()
        mock_base_instance = mock_base_client.return_value
        mock_base_instance._credentials = mock_creds

        client_options_obj = client_options_lib.ClientOptions(
            api_endpoint="test.endpoint"
        )
        self.assertIsNone(client_options_obj.api_key)

        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_options=client_options_obj,
            api_key="new-test-key",
        )

        mock_storage_client.assert_called_once_with(
            credentials=mock_creds,
            transport=mock_transport,
            client_info=None,
            client_options=client_options_obj,
        )
        self.assertEqual(client_options_obj.api_key, "new-test-key")

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_constructor_with_api_key_and_dict_options(
        self, mock_storage_client, mock_base_client
    ):

        mock_creds = _make_credentials()
        mock_base_instance = mock_base_client.return_value
        mock_base_instance._credentials = mock_creds
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_transport = mock_transport_cls.return_value

        client_options_dict = {"api_endpoint": "test.endpoint"}

        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_options=client_options_dict,
            api_key="new-test-key",
        )

        expected_options = {
            "api_endpoint": "test.endpoint",
            "api_key": "new-test-key",
        }
        mock_storage_client.assert_called_once_with(
            credentials=mock_creds,
            transport=mock_transport,
            client_info=None,
            client_options=expected_options,
        )
