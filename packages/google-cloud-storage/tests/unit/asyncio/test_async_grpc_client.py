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

import asyncio
from unittest import mock

import grpc
import pytest
from google.api_core import client_info as client_info_lib
from google.api_core import client_options
from google.auth import credentials as auth_credentials
from google.auth.credentials import AnonymousCredentials

from google.cloud.storage import __version__, _opentelemetry_metrics
from google.cloud.storage.asyncio import async_grpc_client


def _make_credentials(spec=None):
    if spec is None:
        return mock.Mock(spec=auth_credentials.Credentials)
    return mock.Mock(spec=spec)


class TestAsyncGrpcClient:
    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_default_options(self, mock_async_storage_client):
        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        # Act
        async_grpc_client.AsyncGrpcClient(credentials=mock_creds)

        # Assert
        mock_async_storage_client.get_transport_class.assert_called_once_with(
            "grpc_asyncio"
        )
        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        agent_version = f"gcloud-python/{__version__}"
        assert agent_version in client_info.user_agent
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=True,
            credentials=mock_creds,
            options=expected_options,
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(channel=mock_channel)
        mock_transport = mock_transport_cls.return_value
        assert kwargs["transport"] is mock_transport
        assert kwargs["client_options"] is None

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_with_client_info(self, mock_async_storage_client):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()
        client_info = client_info_lib.ClientInfo(
            client_library_version="1.2.3",
        )

        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds, client_info=client_info
        )

        agent_version = f"gcloud-python/{__version__}"
        assert agent_version in client_info.user_agent
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=True,
            credentials=mock_creds,
            options=expected_options,
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_with_quota_project_and_endpoint(
        self, mock_async_storage_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        from google.api_core import client_options

        mock_client_options = client_options.ClientOptions(
            api_endpoint="custom-endpoint.com", quota_project_id="my-quota-project"
        )

        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds, client_options=mock_client_options
        )

        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="custom-endpoint.com",
            quota_project_id="my-quota-project",
            attempt_direct_path=True,
            credentials=mock_creds,
            options=expected_options,
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_constructor_disables_directpath(self, mock_async_storage_client):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds, attempt_direct_path=False
        )

        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        agent_version = f"gcloud-python/{__version__}"
        assert agent_version in client_info.user_agent
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=False,
            credentials=mock_creds,
            options=expected_options,
        )
        mock_channel = mock_transport_cls.create_channel.return_value
        mock_transport_cls.assert_called_once_with(channel=mock_channel)

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_metrics_properties(self, mock_async_storage_client):
        from google.cloud.storage import _opentelemetry_metrics

        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=True,
        ):
            client = async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_metrics=True,
                enable_debug_metrics=True,
            )
            assert client.metrics_enabled is True
            assert client.debug_metrics_enabled is True

            client_base_false = async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_metrics=False,
                enable_debug_metrics=True,
            )
            assert client_base_false.metrics_enabled is False
            assert client_base_false.debug_metrics_enabled is True

            client_both_false = async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_metrics=False,
                enable_debug_metrics=False,
            )
            assert client_both_false.metrics_enabled is False
            assert client_both_false.debug_metrics_enabled is False

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=False,
        ):
            client = async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_metrics=True,
                enable_debug_metrics=True,
            )
            assert client.metrics_enabled is False
            assert client.debug_metrics_enabled is False

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_ctor_w_invalid_enable_metrics_raises_type_error(
        self, mock_async_storage_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        with pytest.raises(TypeError):
            async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_metrics="true",
            )
        with pytest.raises(TypeError):
            async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                enable_debug_metrics="true",
            )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_ctor_metrics_defaults_and_env_fallback(self, mock_async_storage_client):
        from google.cloud.storage import _opentelemetry_metrics

        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        with mock.patch.multiple(
            _opentelemetry_metrics,
            HAS_OPENTELEMETRY_METRICS=True,
            _ENABLE_METRICS_DEV_GATE=True,
        ):
            with mock.patch.dict("os.environ", {}, clear=True):
                client = async_grpc_client.AsyncGrpcClient(credentials=mock_creds)
                assert client._enable_metrics is None
                assert client._enable_debug_metrics is None
                assert client.metrics_enabled is False
                assert client.debug_metrics_enabled is False

            with mock.patch.dict(
                "os.environ",
                {
                    "GCP_STORAGE_PYTHON_ENABLE_OTEL_METRICS": "true",
                    "GCP_STORAGE_PYTHON_ENABLE_OTEL_DEBUG_METRICS": "true",
                },
                clear=True,
            ):
                client = async_grpc_client.AsyncGrpcClient(credentials=mock_creds)
                assert client.metrics_enabled is True
                assert client.debug_metrics_enabled is True

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_grpc_client_property(self, mock_grpc_gapic_client):
        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_grpc_gapic_client.get_transport_class.return_value = mock_transport_cls
        channel_sentinel = mock.sentinel.channel
        mock_transport_cls.create_channel.return_value = channel_sentinel
        mock_transport_instance = mock.sentinel.transport
        mock_transport_cls.return_value = mock_transport_instance

        mock_creds = _make_credentials()
        # Use a real ClientInfo instance instead of a mock to properly test user agent logic
        client_info = client_info_lib.ClientInfo(user_agent="test-user-agent")
        mock_client_options = mock.sentinel.client_options
        mock_attempt_direct_path = mock.sentinel.attempt_direct_path

        # Act
        client = async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds,
            client_info=client_info,
            client_options=mock_client_options,
            attempt_direct_path=mock_attempt_direct_path,
        )
        retrieved_client = client.grpc_client  # This is what is being tested

        # Assert - verify that gcloud-python agent version was added
        agent_version = f"gcloud-python/{__version__}"
        assert agent_version in client_info.user_agent
        # Also verify original user_agent is still there
        assert "test-user-agent" in client_info.user_agent

        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=mock_attempt_direct_path,
            credentials=mock_creds,
            options=expected_options,
        )
        mock_transport_cls.assert_called_once_with(channel=channel_sentinel)
        mock_grpc_gapic_client.assert_called_once_with(
            transport=mock_transport_instance,
            client_info=client_info,
            client_options=mock_client_options,
        )
        assert retrieved_client is mock_grpc_gapic_client.return_value

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @mock.patch(
        "google.cloud.storage.asyncio.async_grpc_client.grpc.aio.insecure_channel"
    )
    def test_grpc_client_with_anon_creds(
        self, mock_insecure_channel, mock_async_storage_client
    ):
        # Arrange
        mock_channel = mock.MagicMock()
        mock_insecure_channel.return_value = mock_channel

        # Act
        client = async_grpc_client.AsyncGrpcClient(
            client_options=client_options.ClientOptions(
                api_endpoint="my-grpc-endpoint"
            ),
            credentials=AnonymousCredentials(),
        )

        # Assert
        assert client.grpc_client is mock_async_storage_client.return_value
        mock_insecure_channel.assert_called_once_with("my-grpc-endpoint")

        kwargs = mock_async_storage_client.call_args.kwargs
        transport = kwargs["transport"]
        assert isinstance(transport._credentials, AnonymousCredentials)

    def test_grpc_client_with_anon_creds_no_client_options(self):
        # Act & Assert
        message = "Either client_options or `client_option.api_endpoint` is None. Please provide api_endpoint when `AnonymousCredentials` is used "
        with pytest.raises(ValueError, match=message):
            async_grpc_client.AsyncGrpcClient(
                credentials=AnonymousCredentials(),
            )

    def test_grpc_client_with_anon_creds_empty_client_options(self):
        # Act & Assert
        message = "Either client_options or `client_option.api_endpoint` is None. Please provide api_endpoint when `AnonymousCredentials` is used "
        with pytest.raises(ValueError, match=message):
            async_grpc_client.AsyncGrpcClient(
                client_options=client_options.ClientOptions(),
                credentials=AnonymousCredentials(),
            )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_user_agent_with_custom_client_info(self, mock_async_storage_client):
        """Test that gcloud-python user agent is appended to existing user agent.

        Regression test similar to test__http.py::TestConnection::test_duplicate_user_agent
        """
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        # Create a client_info with an existing user_agent
        client_info = client_info_lib.ClientInfo(user_agent="custom-app/1.0")

        # Act
        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds,
            client_info=client_info,
        )

        # Assert - verify that gcloud-python version was appended
        agent_version = f"gcloud-python/{__version__}"
        expected_user_agent = f"custom-app/1.0 {agent_version} "
        assert client_info.user_agent == expected_user_agent

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @pytest.mark.asyncio
    async def test_delete_object(self, mock_async_storage_client):
        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_gapic_client = mock.AsyncMock()
        mock_async_storage_client.return_value = mock_gapic_client

        client = async_grpc_client.AsyncGrpcClient(credentials=_make_credentials())

        bucket_name = "bucket"
        object_name = "object"
        generation = 123
        if_generation_match = 456
        if_generation_not_match = 789
        if_metageneration_match = 111
        if_metageneration_not_match = 222

        # New parameters
        metadata = (("x-goog-api-client", "test-ua"),)
        timeout = 10.0
        retry = mock.Mock()

        # Act
        await client.delete_object(
            bucket_name,
            object_name,
            generation=generation,
            if_generation_match=if_generation_match,
            if_generation_not_match=if_generation_not_match,
            if_metageneration_match=if_metageneration_match,
            if_metageneration_not_match=if_metageneration_not_match,
            metadata=metadata,
            timeout=timeout,
            retry=retry,
        )

        # Assert
        call_args, call_kwargs = mock_gapic_client.delete_object.call_args
        request = call_kwargs["request"]
        assert request.bucket == "projects/_/buckets/bucket"
        assert request.object == "object"
        assert request.generation == generation
        assert request.if_generation_match == if_generation_match
        assert request.if_generation_not_match == if_generation_not_match
        assert request.if_metageneration_match == if_metageneration_match
        assert request.if_metageneration_not_match == if_metageneration_not_match
        assert call_kwargs["metadata"] == metadata
        assert call_kwargs["timeout"] == timeout
        assert call_kwargs["retry"] == retry

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @pytest.mark.asyncio
    async def test_get_object(self, mock_async_storage_client):
        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_gapic_client = mock.AsyncMock()
        mock_async_storage_client.return_value = mock_gapic_client

        client = async_grpc_client.AsyncGrpcClient(credentials=_make_credentials())

        bucket_name = "bucket"
        object_name = "object"

        # Act
        await client.get_object(
            bucket_name,
            object_name,
        )

        # Assert
        call_args, call_kwargs = mock_gapic_client.get_object.call_args
        request = call_kwargs["request"]
        assert request.bucket == "projects/_/buckets/bucket"
        assert request.object == "object"
        assert request.soft_deleted is False

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @pytest.mark.asyncio
    async def test_get_object_with_all_parameters(self, mock_async_storage_client):
        # Arrange
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_gapic_client = mock.AsyncMock()
        mock_async_storage_client.return_value = mock_gapic_client

        client = async_grpc_client.AsyncGrpcClient(credentials=_make_credentials())

        bucket_name = "bucket"
        object_name = "object"
        generation = 123
        if_generation_match = 456
        if_generation_not_match = 789
        if_metageneration_match = 111
        if_metageneration_not_match = 222
        soft_deleted = True

        # New parameters
        metadata = (("x-goog-api-client", "test-ua"),)
        timeout = 10.0
        retry = mock.Mock()

        # Act
        await client.get_object(
            bucket_name,
            object_name,
            generation=generation,
            if_generation_match=if_generation_match,
            if_generation_not_match=if_generation_not_match,
            if_metageneration_match=if_metageneration_match,
            if_metageneration_not_match=if_metageneration_not_match,
            soft_deleted=soft_deleted,
            metadata=metadata,
            timeout=timeout,
            retry=retry,
        )

        # Assert
        call_args, call_kwargs = mock_gapic_client.get_object.call_args
        request = call_kwargs["request"]
        assert request.bucket == "projects/_/buckets/bucket"
        assert request.object == "object"
        assert request.generation == generation
        assert request.if_generation_match == if_generation_match
        assert request.if_generation_not_match == if_generation_not_match
        assert request.if_metageneration_match == if_metageneration_match
        assert request.if_metageneration_not_match == if_metageneration_not_match
        assert request.soft_deleted is True
        assert call_kwargs["metadata"] == metadata
        assert call_kwargs["timeout"] == timeout
        assert call_kwargs["retry"] == retry

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_metadata, expected_exc",
        [
            ("not-a-sequence", TypeError),
            ([("key_only",)], ValueError),
            ([("too", "many", "items")], ValueError),
            ([(123, "val")], TypeError),
            ([("key", 456)], TypeError),
        ],
    )
    async def test_delete_object_invalid_metadata(self, invalid_metadata, expected_exc):
        client = async_grpc_client.AsyncGrpcClient(credentials=_make_credentials())
        with pytest.raises(expected_exc):
            await client.delete_object("bucket", "object", metadata=invalid_metadata)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_metadata, expected_exc",
        [
            ("not-a-sequence", TypeError),
            ([("key_only",)], ValueError),
            ([("too", "many", "items")], ValueError),
            ([(123, "val")], TypeError),
            ([("key", 456)], TypeError),
        ],
    )
    async def test_get_object_invalid_metadata(self, invalid_metadata, expected_exc):
        client = async_grpc_client.AsyncGrpcClient(credentials=_make_credentials())
        with pytest.raises(expected_exc):
            await client.get_object("bucket", "object", metadata=invalid_metadata)

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_async_grpc_client_attempt_direct_path_xds_over_interconnect(
        self, mock_async_storage_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds,
            attempt_direct_path_xds_over_interconnect=True,
        )

        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage-direct.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
            credentials=mock_creds,
            options=expected_options,
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_create_gapic_client_custom_client_options_with_interconnect(
        self, mock_async_storage_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        client_options_obj = client_options.ClientOptions(
            api_endpoint="custom.endpoint.com",
            quota_project_id="my-quota-proj",
        )
        async_grpc_client.AsyncGrpcClient(
            credentials=mock_creds,
            client_options=client_options_obj,
            attempt_direct_path_xds_over_interconnect=True,
        )

        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="custom.endpoint.com",
            quota_project_id="my-quota-proj",
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
            credentials=mock_creds,
            options=expected_options,
        )

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    def test_async_grpc_client_interconnect_env_override(
        self, mock_async_storage_client
    ):
        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_creds = _make_credentials()

        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": "true"},
        ):
            async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                attempt_direct_path=False,
                attempt_direct_path_xds_over_interconnect=False,
            )

        kwargs = mock_async_storage_client.call_args.kwargs
        client_info = kwargs["client_info"]
        primary_user_agent = client_info.to_user_agent()
        expected_options = (("grpc.primary_user_agent", primary_user_agent),)

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage-direct.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=True,
            attempt_direct_path_xds_over_interconnect=True,
            credentials=mock_creds,
            options=expected_options,
        )

        mock_transport_cls.create_channel.reset_mock()
        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": " FALSE "},
        ):
            async_grpc_client.AsyncGrpcClient(
                credentials=mock_creds,
                attempt_direct_path_xds_over_interconnect=True,
            )

        mock_transport_cls.create_channel.assert_called_once_with(
            host="storage.googleapis.com",
            quota_project_id=None,
            attempt_direct_path=True,
            credentials=mock_creds,
            options=expected_options,
        )

        with mock.patch.dict(
            "os.environ",
            {"GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT": "invalid"},
        ):
            with pytest.raises(ValueError):
                async_grpc_client.AsyncGrpcClient(credentials=mock_creds)

    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @pytest.mark.asyncio
    async def test_metrics_interceptors_and_client_lifecycle(
        self, mock_async_storage_client, monkeypatch
    ):
        monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", True)
        monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)

        mock_transport_cls = mock.MagicMock()
        mock_async_storage_client.get_transport_class.return_value = mock_transport_cls
        mock_gapic_client = mock.AsyncMock()
        mock_gapic_client.transport = mock.MagicMock()
        mock_gapic_client.transport.close = mock.AsyncMock()
        mock_async_storage_client.return_value = mock_gapic_client

        client = async_grpc_client.AsyncGrpcClient(
            credentials=_make_credentials(),
            client_options={"api_endpoint": "custom.storage.googleapis.com:443"},
            enable_metrics=True,
        )
        assert client.metrics_enabled is True
        assert client._metrics_recorder.server_address == "custom.storage.googleapis.com"
        assert client._grpc_client._metrics_recorder is client._metrics_recorder

        create_channel_kwargs = mock_transport_cls.create_channel.call_args.kwargs
        assert "interceptors" in create_channel_kwargs
        assert len(create_channel_kwargs["interceptors"]) == 4

        mock_recorder = mock.MagicMock()
        mock_recorder.standard_enabled = True
        client._metrics_recorder = mock_recorder

        await client.delete_object("b", "o")
        mock_recorder.record_logical_operation.assert_called_once()
        _, del_kwargs = mock_recorder.record_logical_operation.call_args
        assert (
            del_kwargs["client_method"]
            == "storage.asyncio.AsyncGrpcClient.delete_object"
        )
        assert del_kwargs["rpc_method"] == "google.storage.v2.Storage/DeleteObject"
        assert del_kwargs["error_type"] == "OK"

        mock_recorder.record_logical_operation.reset_mock()
        await client.get_object("b", "o")
        mock_recorder.record_logical_operation.assert_called_once()
        _, get_kwargs = mock_recorder.record_logical_operation.call_args
        assert (
            get_kwargs["client_method"] == "storage.asyncio.AsyncGrpcClient.get_object"
        )
        assert get_kwargs["rpc_method"] == "google.storage.v2.Storage/GetObject"
        assert get_kwargs["error_type"] == "OK"

        async with client as entered:
            assert entered is client
        mock_gapic_client.transport.close.assert_awaited_once()
        mock_recorder.shutdown.assert_called_once()

    @mock.patch(
        "google.cloud._storage_v2.services.storage.transports.StorageGrpcAsyncIOTransport"
    )
    @mock.patch("google.cloud._storage_v2.StorageAsyncClient")
    @mock.patch("grpc.aio.insecure_channel")
    def test_anonymous_client_with_metrics_enabled(
        self,
        mock_insecure_channel,
        mock_async_storage_client,
        mock_transport,
        monkeypatch,
    ):
        monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", True)
        monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
        opts = client_options.ClientOptions(api_endpoint="localhost:9000")
        client = async_grpc_client.AsyncGrpcClient(
            credentials=auth_credentials.AnonymousCredentials(),
            client_options=opts,
            enable_metrics=True,
        )
        assert client.metrics_enabled is True
        _, kwargs = mock_insecure_channel.call_args
        assert "interceptors" in kwargs
        assert len(kwargs["interceptors"]) == 4

    @pytest.mark.asyncio
    async def test_tracked_calls_and_interceptors(self):
        assert (
            async_grpc_client._extract_rpc_operation(
                b"/google.storage.v2.Storage/GetObject"
            )
            == "google.storage.v2.Storage/GetObject"
        )
        assert async_grpc_client._extract_rpc_operation(None) == "UNKNOWN"
        assert async_grpc_client._extract_rpc_operation("/") == "UNKNOWN"

        status_code, err_type = async_grpc_client._resolve_status_and_error(
            asyncio.CancelledError()
        )
        assert (status_code, err_type) == ("CANCELLED", "CANCELLED")

        class _FakeRpcError(Exception):
            def code(self):
                return grpc.StatusCode.UNAVAILABLE

        assert async_grpc_client._resolve_status_and_error(_FakeRpcError()) == (
            "UNAVAILABLE",
            "UNAVAILABLE",
        )

        from google.api_core import exceptions as api_exceptions

        assert async_grpc_client._resolve_status_and_error(
            api_exceptions.NotFound("missing")
        ) == ("NOT_FOUND", "NOT_FOUND")
        assert async_grpc_client._resolve_status_and_error(
            api_exceptions.Conflict("conflict")
        ) == ("ABORTED", "ABORTED")

        recorder = mock.MagicMock()
        recorder.standard_enabled = True
        u_u, u_s, s_u, s_s = async_grpc_client._create_metrics_interceptors(recorder)

        details = mock.MagicMock(method="/google.storage.v2.Storage/GetObject")

        # 1. Unary-Unary success and methods delegation
        class _AwaitableCall:
            def __init__(self, result=None, exc=None):
                self._result = result
                self._exc = exc
                self._done_writing_flag = False
                self.wait_for_connection = mock.AsyncMock()
                self.cancel = mock.MagicMock(return_value=True)
                self.cancelled = mock.MagicMock(return_value=False)
                self.done = mock.MagicMock(return_value=True)
                self.add_done_callback = mock.MagicMock()
                self.time_remaining = mock.MagicMock(return_value=5.0)
                self.initial_metadata = mock.AsyncMock(return_value=(("k", "v"),))
                self.trailing_metadata = mock.AsyncMock(return_value=(("t", "v"),))
                self.code = mock.AsyncMock(return_value=grpc.StatusCode.OK)
                self.details = mock.AsyncMock(return_value="ok")
                self.debug_error_string = mock.AsyncMock(return_value="dbg")
                self.write = mock.AsyncMock()
                self.done_writing = mock.AsyncMock()

            async def _coro(self):
                if self._exc:
                    raise self._exc
                return self._result

            def __await__(self):
                return self._coro().__await__()

        raw_uu = _AwaitableCall(result="resp")
        tracked_uu = await u_u.intercept_unary_unary(
            mock.AsyncMock(return_value=raw_uu), details, "req"
        )
        await tracked_uu.wait_for_connection()
        assert tracked_uu.cancelled() is False
        assert tracked_uu.done() is True
        tracked_uu.add_done_callback(lambda c: None)
        assert tracked_uu.time_remaining() == 5.0
        assert await tracked_uu.initial_metadata() == (("k", "v"),)
        assert await tracked_uu.trailing_metadata() == (("t", "v"),)
        assert await tracked_uu.code() == grpc.StatusCode.OK
        assert await tracked_uu.details() == "ok"
        assert await tracked_uu.debug_error_string() == "dbg"
        assert await tracked_uu == "resp"
        recorder.record_rpc_attempt.assert_called_once()
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"

        # 2. Stream-Unary error and continuation error
        recorder.record_rpc_attempt.reset_mock()
        raw_su = _AwaitableCall(exc=_FakeRpcError())
        tracked_su = await s_u.intercept_stream_unary(
            mock.AsyncMock(return_value=raw_su), details, iter([])
        )
        tracked_su._done_writing_flag = True
        assert tracked_su._done_writing_flag is True
        await tracked_su.write("chunk")
        await tracked_su.done_writing()
        with pytest.raises(_FakeRpcError):
            await tracked_su
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "UNAVAILABLE"
        )

        for interceptor, method_name in (
            (u_u, "intercept_unary_unary"),
            (u_s, "intercept_unary_stream"),
            (s_u, "intercept_stream_unary"),
            (s_s, "intercept_stream_stream"),
        ):
            recorder.record_rpc_attempt.reset_mock()
            with pytest.raises(_FakeRpcError):
                await getattr(interceptor, method_name)(
                    mock.AsyncMock(side_effect=_FakeRpcError()), details, "req"
                )
            recorder.record_rpc_attempt.assert_called_once()

        # 3. Unary-Stream __aiter__ and Stream-Stream read() + clean close
        class _StreamCall(_AwaitableCall):
            def __init__(self, items):
                super().__init__()
                self._items = list(items)

            def __aiter__(self):
                async def _gen():
                    for item in self._items:
                        if isinstance(item, BaseException):
                            raise item
                        yield item

                return _gen()

            async def read(self):
                if not self._items:
                    return grpc.aio.EOF
                item = self._items.pop(0)
                if isinstance(item, BaseException):
                    raise item
                return item

        recorder.record_rpc_attempt.reset_mock()
        tracked_us = await u_s.intercept_unary_stream(
            mock.AsyncMock(return_value=_StreamCall(["a", "b"])), details, "req"
        )
        collected = [x async for x in tracked_us]
        assert collected == ["a", "b"]
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"

        recorder.record_rpc_attempt.reset_mock()
        tracked_ss = await s_s.intercept_stream_stream(
            mock.AsyncMock(return_value=_StreamCall(["x"])), details, iter([])
        )
        assert await tracked_ss.read() == "x"
        assert await tracked_ss.read() == grpc.aio.EOF
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"

        # Clean close vs abnormal cancel (including _interceptors_task, cycle, and non-dict object)
        recorder.record_rpc_attempt.reset_mock()
        tracked_ss_clean = await s_s.intercept_stream_stream(
            mock.AsyncMock(return_value=_StreamCall([])), details, iter([])
        )
        done_fut = asyncio.get_running_loop().create_future()
        done_fut.set_result(tracked_ss_clean)
        wrapper = mock.MagicMock(_call=42, _interceptors_task=done_fut)
        wrapper._wrapped = wrapper  # cycle
        async_grpc_client._mark_call_closing_cleanly(None)
        async_grpc_client._mark_call_closing_cleanly(wrapper)
        assert tracked_ss_clean._closing_cleanly is True
        tracked_ss_clean.cancel()
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"

        # Error paths in wait_for_connection, read, write, done_writing
        err_call = _StreamCall([_FakeRpcError()])
        err_call.wait_for_connection = mock.AsyncMock(side_effect=_FakeRpcError())
        err_call.write = mock.AsyncMock(side_effect=_FakeRpcError())
        err_call.done_writing = mock.AsyncMock(side_effect=_FakeRpcError())

        for op_fn in (
            lambda c: c.wait_for_connection(),
            lambda c: c.read(),
            lambda c: c.write("x"),
            lambda c: c.done_writing(),
        ):
            recorder.record_rpc_attempt.reset_mock()
            c = await s_s.intercept_stream_stream(
                mock.AsyncMock(
                    return_value=_StreamCall([_FakeRpcError()])
                    if op_fn
                    else err_call
                ),
                details,
                iter([]),
            )
            c._call = err_call
            err_call._items = [_FakeRpcError()]
            with pytest.raises(_FakeRpcError):
                await op_fn(c)
            recorder.record_rpc_attempt.assert_called_once()

        # CancelledError when _closing_cleanly is True records OK
        recorder.record_rpc_attempt.reset_mock()
        clean_cancel_call = await s_s.intercept_stream_stream(
            mock.AsyncMock(return_value=_StreamCall([asyncio.CancelledError()])),
            details,
            iter([]),
        )
        clean_cancel_call._closing_cleanly = True
        with pytest.raises(asyncio.CancelledError):
            await clean_cancel_call.read()
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"

        recorder.record_rpc_attempt.reset_mock()
        tracked_ss_cancel = await s_s.intercept_stream_stream(
            mock.AsyncMock(return_value=_StreamCall([])), details, iter([])
        )
        tracked_ss_cancel.cancel()
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "CANCELLED"
        )

        # Early break from __aiter__ (clean vs cancelled) and peer() network_path detection
        recorder.record_rpc_attempt.reset_mock()
        stream_with_peer = _StreamCall(["a", "b", "c"])
        stream_with_peer.peer = lambda: b"ipv6:[2001:4860:8040::1]:443"
        tracked_early = await u_s.intercept_unary_stream(
            mock.AsyncMock(return_value=stream_with_peer), details, "req"
        )
        ait = tracked_early.__aiter__()
        assert await ait.__anext__() == "a"
        await ait.aclose()
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "CANCELLED"
        )
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["network_path"] == "directpath"
        )

        recorder.record_rpc_attempt.reset_mock()
        stream_cloud = _StreamCall(["a", "b"])
        stream_cloud.peer = lambda: "ipv4:142.250.1.1:443"
        tracked_early_clean = await u_s.intercept_unary_stream(
            mock.AsyncMock(return_value=stream_cloud), details, "req"
        )
        tracked_early_clean._closing_cleanly = True
        ait_clean = tracked_early_clean.__aiter__()
        assert await ait_clean.__anext__() == "a"
        await ait_clean.aclose()
        assert recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "OK"
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["network_path"] == "cloudpath"
        )

        # Mid-iteration exception in __aiter__
        recorder.record_rpc_attempt.reset_mock()
        tracked_err_iter = await u_s.intercept_unary_stream(
            mock.AsyncMock(return_value=_StreamCall(["a", _FakeRpcError()])),
            details,
            "req",
        )
        with pytest.raises(_FakeRpcError):
            _ = [x async for x in tracked_err_iter]
        assert (
            recorder.record_rpc_attempt.call_args.kwargs["status_code"] == "UNAVAILABLE"
        )
