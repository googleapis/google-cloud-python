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

import pytest
from google.api_core import client_options as client_options_lib
from google.auth import credentials as auth_credentials

from google.cloud.storage import grpc_client


@pytest.fixture(autouse=True)
def _hermetic_env(monkeypatch):
    """Keeps the runner's environment from changing host or DirectPath resolution."""
    monkeypatch.delenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", raising=False)


def _make_credentials(spec=None):
    if spec is None:
        return mock.Mock(
            spec=auth_credentials.Credentials, universe_domain="googleapis.com"
        )
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

        # 2. Assert DirectPath is ON by default and endpoint/credentials are forwarded.
        mock_storage_client.get_transport_class.assert_called_once_with("grpc")
        mock_transport_cls.create_channel.assert_called_once_with(
            host="test.endpoint",
            credentials=mock_creds,
            attempt_direct_path=True,
        )

        # 3. Assert the GAPIC client was created with the correct options.
        mock_transport = mock_transport_cls.return_value
        mock_storage_client.assert_called_once_with(
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
            host="storage.googleapis.com",
            credentials=mock_creds,
            attempt_direct_path=False,
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
            transport=mock_transport,
            client_info=None,
            client_options=expected_options,
        )

    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_universe_domain_routing_and_direct_path_disabled(
        self, mock_storage_client
    ):
        other_creds = _make_credentials()
        other_creds.universe_domain = "example.com"
        anon_creds = auth_credentials.AnonymousCredentials()
        cases = [
            (
                {},
                other_creds,
                {"universe_domain": "example.com", "quota_project_id": "qp"},
                "storage.example.com",
                {"quota_project_id": "qp"},
            ),
            (
                {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "example.com"},
                other_creds,
                None,
                "storage.example.com",
                {},
            ),
            (
                {},
                other_creds,
                client_options_lib.ClientOptions(
                    universe_domain="example.com", api_endpoint="custom.example.com:443"
                ),
                "custom.example.com:443",
                {},
            ),
            (
                {},
                anon_creds,
                {"universe_domain": "example.com", "api_endpoint": "localhost:8888"},
                "localhost:8888",
                {},
            ),
        ]
        for env, creds, opts, expected_host, extra_kw in cases:
            mock_transport_cls = mock.MagicMock()
            mock_storage_client.get_transport_class.return_value = mock_transport_cls
            with (
                self.subTest(expected_host=expected_host, opts=opts),
                mock.patch.dict("os.environ", env, clear=False),
            ):
                client = grpc_client.GrpcClient(
                    project="test-project",
                    credentials=creds,
                    client_options=opts,
                    attempt_direct_path=True,
                )
            self.assertEqual(client.universe_domain, "example.com")
            mock_transport_cls.create_channel.assert_called_once_with(
                host=expected_host,
                credentials=creds,
                attempt_direct_path=False,
                **extra_kw,
            )
            mock_transport_cls.assert_called_once_with(
                host=expected_host,
                channel=mock_transport_cls.create_channel.return_value,
            )

    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_empty_universe_domain_error(self, mock_storage_client):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls

        with self.assertRaisesRegex(
            ValueError, "Universe Domain cannot be an empty string"
        ):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=_make_credentials(),
                client_options={"universe_domain": ""},
            )
        mock_transport_cls.create_channel.assert_not_called()

    @mock.patch("google.auth.default")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_universe_domain_validation_errors(
        self, mock_storage_client, mock_auth_default
    ):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        other_creds = _make_credentials()
        other_creds.universe_domain = "example.com"
        mock_auth_default.return_value = (other_creds, "test-project")

        with self.assertRaisesRegex(ValueError, "example.com"):
            grpc_client.GrpcClient(project="test-project", credentials=other_creds)
        with self.assertRaisesRegex(ValueError, "example.com"):
            grpc_client.GrpcClient(project="test-project")
        mock_transport_cls.create_channel.assert_not_called()

    @mock.patch("google.api_core.grpc_helpers.create_channel")
    def test_real_gapic_client_integration_non_default_universe(
        self, mock_create_channel
    ):
        import grpc

        mock_create_channel.return_value = mock.MagicMock(spec=grpc.Channel)
        mock_creds = _make_credentials()
        mock_creds.universe_domain = "example.com"
        client = grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_options={"universe_domain": "example.com"},
        )
        self.assertEqual(client.universe_domain, "example.com")
        self.assertEqual(client.grpc_client.universe_domain, "example.com")
        self.assertEqual(client.grpc_client.api_endpoint, "storage.example.com:443")
        self.assertEqual(mock_create_channel.call_args.args[0], "storage.example.com")
        self.assertFalse(mock_create_channel.call_args.kwargs["attempt_direct_path"])


@pytest.mark.parametrize("creds_universe", ["__missing__", None, 123])
@mock.patch("google.cloud._storage_v2.StorageClient")
def test_grpc_client_universe_domain_validation_unusable_creds(
    mock_storage_client, creds_universe
):
    mock_transport_cls = mock.MagicMock()
    mock_storage_client.get_transport_class.return_value = mock_transport_cls
    creds = _make_credentials()
    if creds_universe == "__missing__":
        del creds.universe_domain
    else:
        creds.universe_domain = creds_universe

    with pytest.raises(ValueError, match="does not match"):
        grpc_client.GrpcClient(
            project="test-project",
            credentials=creds,
            client_options={"universe_domain": "example.com"},
        )
    mock_transport_cls.create_channel.assert_not_called()


@mock.patch("google.cloud._storage_v2.StorageClient")
def test_grpc_client_unconfigured_mock_credentials_allowed(mock_storage_client):
    mock_transport_cls = mock.MagicMock()
    mock_storage_client.get_transport_class.return_value = mock_transport_cls
    mock_creds = mock.Mock(spec=auth_credentials.Credentials)

    client = grpc_client.GrpcClient(project="test-project", credentials=mock_creds)

    assert client.universe_domain == "googleapis.com"
    mock_transport_cls.create_channel.assert_called_once_with(
        host="storage.googleapis.com",
        credentials=mock_creds,
        attempt_direct_path=True,
    )


@mock.patch("google.cloud.client.ClientWithProject.__init__", return_value=None)
@mock.patch("google.cloud._storage_v2.StorageClient")
def test_grpc_client_none_effective_credentials(mock_storage_client, mock_base_init):
    mock_transport_cls = mock.MagicMock()
    mock_storage_client.get_transport_class.return_value = mock_transport_cls

    client = grpc_client.GrpcClient(project="test-project")

    assert client.universe_domain == "googleapis.com"
    mock_transport_cls.create_channel.assert_called_once_with(
        host="storage.googleapis.com",
        credentials=None,
        attempt_direct_path=True,
    )
