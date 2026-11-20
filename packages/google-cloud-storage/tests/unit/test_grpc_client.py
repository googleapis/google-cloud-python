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
    monkeypatch.delenv(
        "GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT", raising=False
    )


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

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_grpc_client_attempt_direct_path_xds_over_interconnect(
        self, mock_storage_client, mock_base_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_base_client.return_value._credentials = mock_creds

        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            attempt_direct_path_xds_over_interconnect=True,
        )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage-direct.googleapis.com",
            credentials=mock_creds,
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
        )

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_grpc_client_attempt_direct_path_xds_over_interconnect_with_quota_project(
        self, mock_storage_client, mock_base_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_base_client.return_value._credentials = mock_creds

        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_options={"quota_project_id": "my-quota-proj"},
            attempt_direct_path_xds_over_interconnect=True,
        )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage-direct.googleapis.com",
            credentials=mock_creds,
            quota_project_id="my-quota-proj",
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
        )

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_create_gapic_client_custom_client_options_with_interconnect(
        self, mock_storage_client, mock_base_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_base_client.return_value._credentials = mock_creds

        client_options_obj = client_options_lib.ClientOptions(
            api_endpoint="custom.endpoint.com",
            quota_project_id="my-quota-proj",
        )
        grpc_client.GrpcClient(
            project="test-project",
            credentials=mock_creds,
            client_options=client_options_obj,
            attempt_direct_path_xds_over_interconnect=True,
        )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="custom.endpoint.com",
            credentials=mock_creds,
            quota_project_id="my-quota-proj",
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
        )

    @mock.patch("google.cloud.storage.grpc_client.ClientWithProject")
    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_grpc_client_attempt_direct_path_xds_over_interconnect_env_override(
        self, mock_storage_client, mock_base_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        mock_base_client.return_value._credentials = mock_creds

        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": " TRUE "},
        ):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                attempt_direct_path_xds_over_interconnect=False,
            )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage-direct.googleapis.com",
            credentials=mock_creds,
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
        )

        mock_transport_cls.create_channel.reset_mock()
        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": " FALSE "},
        ):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                attempt_direct_path_xds_over_interconnect=True,
            )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            credentials=mock_creds,
            attempt_direct_path=True,
        )

        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": "invalid"},
        ):
            with self.assertRaises(ValueError):
                grpc_client.GrpcClient(
                    project="test-project",
                    credentials=mock_creds,
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
                {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": "true"},
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
                    attempt_direct_path_xds_over_interconnect=True,
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
        with self.assertRaisesRegex(
            ValueError, "Universe Domain cannot be an empty string"
        ):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=other_creds,
                client_options={"universe_domain": ""},
            )

        # Credentials that expose no usable universe domain must not be accepted
        # in a non-default universe.
        missing_universe_creds = _make_credentials()
        del missing_universe_creds.universe_domain
        none_universe_creds = _make_credentials()
        none_universe_creds.universe_domain = None
        for creds in (missing_universe_creds, none_universe_creds):
            with self.assertRaisesRegex(ValueError, "does not match"):
                grpc_client.GrpcClient(
                    project="test-project",
                    credentials=creds,
                    client_options={"universe_domain": "example.com"},
                )
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

    def test_rewrite_host_for_interconnect_delimiters(self):
        cases = [
            ("storage.googleapis.com", "storage-direct.googleapis.com"),
            ("storage.googleapis.com:443", "storage-direct.googleapis.com:443"),
            ("storage.googleapis.com/path", "storage-direct.googleapis.com/path"),
            (
                "storage.googleapis.com?query=val",
                "storage-direct.googleapis.com?query=val",
            ),
            ("storage.googleapis.com#section", "storage-direct.googleapis.com#section"),
            ("https://storage.googleapis.com", "https://storage-direct.googleapis.com"),
            (
                "https://storage.googleapis.com:443?q=1",
                "https://storage-direct.googleapis.com:443?q=1",
            ),
            (
                "dns:///storage.googleapis.com:443",
                "dns:///storage-direct.googleapis.com:443",
            ),
            (
                "storage.googleapis.com.evil.com",
                "storage.googleapis.com.evil.com",
            ),
            (
                "google-c2p:///storage-direct.googleapis.com",
                "google-c2p:///storage-direct.googleapis.com",
            ),
        ]
        for original_host, expected_host in cases:
            self.assertEqual(
                grpc_client._rewrite_host_for_interconnect(original_host),
                expected_host,
            )

    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_metrics_properties(self, mock_storage_client):
        from google.cloud.storage import _opentelemetry_metrics

        mock_creds = _make_credentials()

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=True,
        ):
            client = grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_metrics=True,
                enable_debug_metrics=True,
            )
            self.assertTrue(client.metrics_enabled)
            self.assertTrue(client.debug_metrics_enabled)

            client_base_false = grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_metrics=False,
                enable_debug_metrics=True,
            )
            self.assertFalse(client_base_false.metrics_enabled)
            self.assertTrue(client_base_false.debug_metrics_enabled)

            client_both_false = grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_metrics=False,
                enable_debug_metrics=False,
            )
            self.assertFalse(client_both_false.metrics_enabled)
            self.assertFalse(client_both_false.debug_metrics_enabled)

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=False,
        ):
            client = grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_metrics=True,
                enable_debug_metrics=True,
            )
            self.assertFalse(client.metrics_enabled)
            self.assertFalse(client.debug_metrics_enabled)

    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_ctor_w_invalid_enable_metrics_raises_type_error(self, mock_storage_client):
        mock_creds = _make_credentials()
        with self.assertRaises(TypeError):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_metrics="true",
            )
        with self.assertRaises(TypeError):
            grpc_client.GrpcClient(
                project="test-project",
                credentials=mock_creds,
                enable_debug_metrics="true",
            )

    @mock.patch("google.cloud._storage_v2.StorageClient")
    def test_ctor_metrics_defaults_and_env_fallback(self, mock_storage_client):
        from google.cloud.storage import _opentelemetry_metrics

        mock_creds = _make_credentials()

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=True,
        ):
            with mock.patch.dict("os.environ", {}, clear=True):
                client = grpc_client.GrpcClient(
                    project="test-project",
                    credentials=mock_creds,
                )
                self.assertIsNone(client._enable_metrics)
                self.assertIsNone(client._enable_debug_metrics)
                self.assertFalse(client.metrics_enabled)
                self.assertFalse(client.debug_metrics_enabled)

            with mock.patch.dict(
                "os.environ",
                {
                    "GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS": "true",
                    "GCP_STORAGE_PYTHON_ENABLE_OTEL_DEBUG_METRICS": "true",
                },
                clear=True,
            ):
                client = grpc_client.GrpcClient(
                    project="test-project",
                    credentials=mock_creds,
                )
                self.assertTrue(client.metrics_enabled)
                self.assertTrue(client.debug_metrics_enabled)
