# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service import (
    AnalyticsHubServiceAsyncClient,
    AnalyticsHubServiceClient,
    pagers,
    transports,
)
from google.cloud.bigquery_data_exchange_v1beta1.types import dataexchange


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert AnalyticsHubServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        AnalyticsHubServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsHubServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsHubServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsHubServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsHubServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (AnalyticsHubServiceClient, "grpc"),
        (AnalyticsHubServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_analytics_hub_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("analyticshub.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AnalyticsHubServiceGrpcTransport, "grpc"),
        (transports.AnalyticsHubServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_analytics_hub_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (AnalyticsHubServiceClient, "grpc"),
        (AnalyticsHubServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_analytics_hub_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("analyticshub.googleapis.com:443")


def test_analytics_hub_service_client_get_transport_class():
    transport = AnalyticsHubServiceClient.get_transport_class()
    available_transports = [
        transports.AnalyticsHubServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = AnalyticsHubServiceClient.get_transport_class("grpc")
    assert transport == transports.AnalyticsHubServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AnalyticsHubServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceClient),
)
@mock.patch.object(
    AnalyticsHubServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceAsyncClient),
)
def test_analytics_hub_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AnalyticsHubServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AnalyticsHubServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AnalyticsHubServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceClient),
)
@mock.patch.object(
    AnalyticsHubServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_analytics_hub_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [AnalyticsHubServiceClient, AnalyticsHubServiceAsyncClient]
)
@mock.patch.object(
    AnalyticsHubServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceClient),
)
@mock.patch.object(
    AnalyticsHubServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsHubServiceAsyncClient),
)
def test_analytics_hub_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_hub_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_analytics_hub_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_analytics_hub_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.transports.AnalyticsHubServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AnalyticsHubServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            AnalyticsHubServiceClient,
            transports.AnalyticsHubServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_analytics_hub_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "analyticshub.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=None,
            default_host="analyticshub.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.ListDataExchangesRequest,
        dict,
    ],
)
def test_list_data_exchanges(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListDataExchangesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListDataExchangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataExchangesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_data_exchanges_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        client.list_data_exchanges()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListDataExchangesRequest()


@pytest.mark.asyncio
async def test_list_data_exchanges_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.ListDataExchangesRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListDataExchangesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListDataExchangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataExchangesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_data_exchanges_async_from_dict():
    await test_list_data_exchanges_async(request_type=dict)


def test_list_data_exchanges_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListDataExchangesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        call.return_value = dataexchange.ListDataExchangesResponse()
        client.list_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_data_exchanges_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListDataExchangesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListDataExchangesResponse()
        )
        await client.list_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_data_exchanges_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListDataExchangesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_data_exchanges(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_data_exchanges_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_data_exchanges(
            dataexchange.ListDataExchangesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_data_exchanges_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListDataExchangesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListDataExchangesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_data_exchanges(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_data_exchanges_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_data_exchanges(
            dataexchange.ListDataExchangesRequest(),
            parent="parent_value",
        )


def test_list_data_exchanges_pager(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_data_exchanges(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataexchange.DataExchange) for i in results)


def test_list_data_exchanges_pages(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_data_exchanges(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_data_exchanges_async_pager():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_data_exchanges(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataexchange.DataExchange) for i in responses)


@pytest.mark.asyncio
async def test_list_data_exchanges_async_pages():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_exchanges),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_data_exchanges(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.ListOrgDataExchangesRequest,
        dict,
    ],
)
def test_list_org_data_exchanges(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListOrgDataExchangesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_org_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListOrgDataExchangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgDataExchangesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_org_data_exchanges_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        client.list_org_data_exchanges()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListOrgDataExchangesRequest()


@pytest.mark.asyncio
async def test_list_org_data_exchanges_async(
    transport: str = "grpc_asyncio",
    request_type=dataexchange.ListOrgDataExchangesRequest,
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListOrgDataExchangesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_org_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListOrgDataExchangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrgDataExchangesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_org_data_exchanges_async_from_dict():
    await test_list_org_data_exchanges_async(request_type=dict)


def test_list_org_data_exchanges_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListOrgDataExchangesRequest()

    request.organization = "organization_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        call.return_value = dataexchange.ListOrgDataExchangesResponse()
        client.list_org_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "organization=organization_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_org_data_exchanges_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListOrgDataExchangesRequest()

    request.organization = "organization_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListOrgDataExchangesResponse()
        )
        await client.list_org_data_exchanges(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "organization=organization_value",
    ) in kw["metadata"]


def test_list_org_data_exchanges_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListOrgDataExchangesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_org_data_exchanges(
            organization="organization_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].organization
        mock_val = "organization_value"
        assert arg == mock_val


def test_list_org_data_exchanges_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_org_data_exchanges(
            dataexchange.ListOrgDataExchangesRequest(),
            organization="organization_value",
        )


@pytest.mark.asyncio
async def test_list_org_data_exchanges_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListOrgDataExchangesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListOrgDataExchangesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_org_data_exchanges(
            organization="organization_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].organization
        mock_val = "organization_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_org_data_exchanges_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_org_data_exchanges(
            dataexchange.ListOrgDataExchangesRequest(),
            organization="organization_value",
        )


def test_list_org_data_exchanges_pager(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("organization", ""),)),
        )
        pager = client.list_org_data_exchanges(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataexchange.DataExchange) for i in results)


def test_list_org_data_exchanges_pages(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_org_data_exchanges(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_org_data_exchanges_async_pager():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_org_data_exchanges(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataexchange.DataExchange) for i in responses)


@pytest.mark.asyncio
async def test_list_org_data_exchanges_async_pages():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_org_data_exchanges),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[],
                next_page_token="def",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListOrgDataExchangesResponse(
                data_exchanges=[
                    dataexchange.DataExchange(),
                    dataexchange.DataExchange(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_org_data_exchanges(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.GetDataExchangeRequest,
        dict,
    ],
)
def test_get_data_exchange(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            listing_count=1410,
            icon=b"icon_blob",
        )
        response = client.get_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


def test_get_data_exchange_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        client.get_data_exchange()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetDataExchangeRequest()


@pytest.mark.asyncio
async def test_get_data_exchange_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.GetDataExchangeRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                listing_count=1410,
                icon=b"icon_blob",
            )
        )
        response = await client.get_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


@pytest.mark.asyncio
async def test_get_data_exchange_async_from_dict():
    await test_get_data_exchange_async(request_type=dict)


def test_get_data_exchange_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.GetDataExchangeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        call.return_value = dataexchange.DataExchange()
        client.get_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_data_exchange_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.GetDataExchangeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        await client.get_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_data_exchange_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_exchange(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_data_exchange_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_exchange(
            dataexchange.GetDataExchangeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_exchange_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_exchange(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_data_exchange_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_exchange(
            dataexchange.GetDataExchangeRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.CreateDataExchangeRequest,
        dict,
    ],
)
def test_create_data_exchange(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            listing_count=1410,
            icon=b"icon_blob",
        )
        response = client.create_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


def test_create_data_exchange_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        client.create_data_exchange()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateDataExchangeRequest()


@pytest.mark.asyncio
async def test_create_data_exchange_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.CreateDataExchangeRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                listing_count=1410,
                icon=b"icon_blob",
            )
        )
        response = await client.create_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


@pytest.mark.asyncio
async def test_create_data_exchange_async_from_dict():
    await test_create_data_exchange_async(request_type=dict)


def test_create_data_exchange_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.CreateDataExchangeRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        call.return_value = dataexchange.DataExchange()
        client.create_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_data_exchange_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.CreateDataExchangeRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        await client.create_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_data_exchange_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_data_exchange(
            parent="parent_value",
            data_exchange=dataexchange.DataExchange(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].data_exchange
        mock_val = dataexchange.DataExchange(name="name_value")
        assert arg == mock_val


def test_create_data_exchange_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_data_exchange(
            dataexchange.CreateDataExchangeRequest(),
            parent="parent_value",
            data_exchange=dataexchange.DataExchange(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_data_exchange_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_data_exchange(
            parent="parent_value",
            data_exchange=dataexchange.DataExchange(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].data_exchange
        mock_val = dataexchange.DataExchange(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_data_exchange_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_data_exchange(
            dataexchange.CreateDataExchangeRequest(),
            parent="parent_value",
            data_exchange=dataexchange.DataExchange(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.UpdateDataExchangeRequest,
        dict,
    ],
)
def test_update_data_exchange(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            listing_count=1410,
            icon=b"icon_blob",
        )
        response = client.update_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


def test_update_data_exchange_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        client.update_data_exchange()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateDataExchangeRequest()


@pytest.mark.asyncio
async def test_update_data_exchange_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.UpdateDataExchangeRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                listing_count=1410,
                icon=b"icon_blob",
            )
        )
        response = await client.update_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.DataExchange)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.listing_count == 1410
    assert response.icon == b"icon_blob"


@pytest.mark.asyncio
async def test_update_data_exchange_async_from_dict():
    await test_update_data_exchange_async(request_type=dict)


def test_update_data_exchange_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.UpdateDataExchangeRequest()

    request.data_exchange.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        call.return_value = dataexchange.DataExchange()
        client.update_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_exchange.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_data_exchange_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.UpdateDataExchangeRequest()

    request.data_exchange.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        await client.update_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_exchange.name=name_value",
    ) in kw["metadata"]


def test_update_data_exchange_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_data_exchange(
            data_exchange=dataexchange.DataExchange(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_exchange
        mock_val = dataexchange.DataExchange(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_data_exchange_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_data_exchange(
            dataexchange.UpdateDataExchangeRequest(),
            data_exchange=dataexchange.DataExchange(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_data_exchange_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.DataExchange()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.DataExchange()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_data_exchange(
            data_exchange=dataexchange.DataExchange(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_exchange
        mock_val = dataexchange.DataExchange(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_data_exchange_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_data_exchange(
            dataexchange.UpdateDataExchangeRequest(),
            data_exchange=dataexchange.DataExchange(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.DeleteDataExchangeRequest,
        dict,
    ],
)
def test_delete_data_exchange(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_data_exchange_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        client.delete_data_exchange()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteDataExchangeRequest()


@pytest.mark.asyncio
async def test_delete_data_exchange_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.DeleteDataExchangeRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteDataExchangeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_data_exchange_async_from_dict():
    await test_delete_data_exchange_async(request_type=dict)


def test_delete_data_exchange_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.DeleteDataExchangeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        call.return_value = None
        client.delete_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_data_exchange_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.DeleteDataExchangeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_data_exchange(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_data_exchange_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_data_exchange(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_data_exchange_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_data_exchange(
            dataexchange.DeleteDataExchangeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_data_exchange_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_exchange), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_data_exchange(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_data_exchange_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_data_exchange(
            dataexchange.DeleteDataExchangeRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.ListListingsRequest,
        dict,
    ],
)
def test_list_listings(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListListingsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_listings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListListingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListListingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_listings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        client.list_listings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListListingsRequest()


@pytest.mark.asyncio
async def test_list_listings_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.ListListingsRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListListingsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_listings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.ListListingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListListingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_listings_async_from_dict():
    await test_list_listings_async(request_type=dict)


def test_list_listings_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListListingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        call.return_value = dataexchange.ListListingsResponse()
        client.list_listings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_listings_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.ListListingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListListingsResponse()
        )
        await client.list_listings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_listings_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListListingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_listings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_listings_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_listings(
            dataexchange.ListListingsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_listings_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.ListListingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.ListListingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_listings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_listings_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_listings(
            dataexchange.ListListingsRequest(),
            parent="parent_value",
        )


def test_list_listings_pager(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListListingsResponse(
                listings=[],
                next_page_token="def",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_listings(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataexchange.Listing) for i in results)


def test_list_listings_pages(transport_name: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_listings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListListingsResponse(
                listings=[],
                next_page_token="def",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_listings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_listings_async_pager():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_listings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListListingsResponse(
                listings=[],
                next_page_token="def",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_listings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataexchange.Listing) for i in responses)


@pytest.mark.asyncio
async def test_list_listings_async_pages():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_listings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
                next_page_token="abc",
            ),
            dataexchange.ListListingsResponse(
                listings=[],
                next_page_token="def",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                ],
                next_page_token="ghi",
            ),
            dataexchange.ListListingsResponse(
                listings=[
                    dataexchange.Listing(),
                    dataexchange.Listing(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_listings(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.GetListingRequest,
        dict,
    ],
)
def test_get_listing(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            state=dataexchange.Listing.State.ACTIVE,
            icon=b"icon_blob",
            categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
            request_access="request_access_value",
        )
        response = client.get_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


def test_get_listing_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        client.get_listing()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetListingRequest()


@pytest.mark.asyncio
async def test_get_listing_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.GetListingRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                state=dataexchange.Listing.State.ACTIVE,
                icon=b"icon_blob",
                categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
                request_access="request_access_value",
            )
        )
        response = await client.get_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.GetListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


@pytest.mark.asyncio
async def test_get_listing_async_from_dict():
    await test_get_listing_async(request_type=dict)


def test_get_listing_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.GetListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        call.return_value = dataexchange.Listing()
        client.get_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_listing_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.GetListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        await client.get_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_listing_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_listing_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_listing(
            dataexchange.GetListingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_listing_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_listing_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_listing(
            dataexchange.GetListingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.CreateListingRequest,
        dict,
    ],
)
def test_create_listing(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            state=dataexchange.Listing.State.ACTIVE,
            icon=b"icon_blob",
            categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
            request_access="request_access_value",
        )
        response = client.create_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


def test_create_listing_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        client.create_listing()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateListingRequest()


@pytest.mark.asyncio
async def test_create_listing_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.CreateListingRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                state=dataexchange.Listing.State.ACTIVE,
                icon=b"icon_blob",
                categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
                request_access="request_access_value",
            )
        )
        response = await client.create_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.CreateListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


@pytest.mark.asyncio
async def test_create_listing_async_from_dict():
    await test_create_listing_async(request_type=dict)


def test_create_listing_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.CreateListingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        call.return_value = dataexchange.Listing()
        client.create_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_listing_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.CreateListingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        await client.create_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_listing_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_listing(
            parent="parent_value",
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].listing
        mock_val = dataexchange.Listing(
            bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                dataset="dataset_value"
            )
        )
        assert arg == mock_val


def test_create_listing_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_listing(
            dataexchange.CreateListingRequest(),
            parent="parent_value",
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_listing_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_listing(
            parent="parent_value",
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].listing
        mock_val = dataexchange.Listing(
            bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                dataset="dataset_value"
            )
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_listing_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_listing(
            dataexchange.CreateListingRequest(),
            parent="parent_value",
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.UpdateListingRequest,
        dict,
    ],
)
def test_update_listing(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            primary_contact="primary_contact_value",
            documentation="documentation_value",
            state=dataexchange.Listing.State.ACTIVE,
            icon=b"icon_blob",
            categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
            request_access="request_access_value",
        )
        response = client.update_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


def test_update_listing_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        client.update_listing()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateListingRequest()


@pytest.mark.asyncio
async def test_update_listing_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.UpdateListingRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                primary_contact="primary_contact_value",
                documentation="documentation_value",
                state=dataexchange.Listing.State.ACTIVE,
                icon=b"icon_blob",
                categories=[dataexchange.Listing.Category.CATEGORY_OTHERS],
                request_access="request_access_value",
            )
        )
        response = await client.update_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.UpdateListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.Listing)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.primary_contact == "primary_contact_value"
    assert response.documentation == "documentation_value"
    assert response.state == dataexchange.Listing.State.ACTIVE
    assert response.icon == b"icon_blob"
    assert response.categories == [dataexchange.Listing.Category.CATEGORY_OTHERS]
    assert response.request_access == "request_access_value"


@pytest.mark.asyncio
async def test_update_listing_async_from_dict():
    await test_update_listing_async(request_type=dict)


def test_update_listing_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.UpdateListingRequest()

    request.listing.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        call.return_value = dataexchange.Listing()
        client.update_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "listing.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_listing_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.UpdateListingRequest()

    request.listing.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        await client.update_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "listing.name=name_value",
    ) in kw["metadata"]


def test_update_listing_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_listing(
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].listing
        mock_val = dataexchange.Listing(
            bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                dataset="dataset_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_listing_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_listing(
            dataexchange.UpdateListingRequest(),
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_listing_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.Listing()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.Listing()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_listing(
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].listing
        mock_val = dataexchange.Listing(
            bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                dataset="dataset_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_listing_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_listing(
            dataexchange.UpdateListingRequest(),
            listing=dataexchange.Listing(
                bigquery_dataset=dataexchange.Listing.BigQueryDatasetSource(
                    dataset="dataset_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.DeleteListingRequest,
        dict,
    ],
)
def test_delete_listing(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteListingRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_listing_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        client.delete_listing()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteListingRequest()


@pytest.mark.asyncio
async def test_delete_listing_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.DeleteListingRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.DeleteListingRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_listing_async_from_dict():
    await test_delete_listing_async(request_type=dict)


def test_delete_listing_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.DeleteListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        call.return_value = None
        client.delete_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_listing_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.DeleteListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_listing_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_listing_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_listing(
            dataexchange.DeleteListingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_listing_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_listing), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_listing_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_listing(
            dataexchange.DeleteListingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataexchange.SubscribeListingRequest,
        dict,
    ],
)
def test_subscribe_listing(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.SubscribeListingResponse()
        response = client.subscribe_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.SubscribeListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.SubscribeListingResponse)


def test_subscribe_listing_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        client.subscribe_listing()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.SubscribeListingRequest()


@pytest.mark.asyncio
async def test_subscribe_listing_async(
    transport: str = "grpc_asyncio", request_type=dataexchange.SubscribeListingRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.SubscribeListingResponse()
        )
        response = await client.subscribe_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataexchange.SubscribeListingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataexchange.SubscribeListingResponse)


@pytest.mark.asyncio
async def test_subscribe_listing_async_from_dict():
    await test_subscribe_listing_async(request_type=dict)


def test_subscribe_listing_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.SubscribeListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        call.return_value = dataexchange.SubscribeListingResponse()
        client.subscribe_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_subscribe_listing_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataexchange.SubscribeListingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.SubscribeListingResponse()
        )
        await client.subscribe_listing(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_subscribe_listing_flattened():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.SubscribeListingResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.subscribe_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_subscribe_listing_flattened_error():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.subscribe_listing(
            dataexchange.SubscribeListingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_subscribe_listing_flattened_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.subscribe_listing), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataexchange.SubscribeListingResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataexchange.SubscribeListingResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.subscribe_listing(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_subscribe_listing_flattened_error_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.subscribe_listing(
            dataexchange.SubscribeListingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        client.get_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()


@pytest.mark.asyncio
async def test_get_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async_from_dict():
    await test_get_iam_policy_async(request_type=dict)


def test_get_iam_policy_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        client.set_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()


@pytest.mark.asyncio
async def test_set_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async_from_dict():
    await test_set_iam_policy_async(request_type=dict)


def test_set_iam_policy_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
                "update_mask": field_mask_pb2.FieldMask(paths=["paths_value"]),
            }
        )
        call.assert_called()


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions(request_type, transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )
        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        client.test_iam_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()


@pytest.mark.asyncio
async def test_test_iam_permissions_async(
    transport: str = "grpc_asyncio",
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )
        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async_from_dict():
    await test_test_iam_permissions_async(request_type=dict)


def test_test_iam_permissions_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )
        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsHubServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsHubServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AnalyticsHubServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AnalyticsHubServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsHubServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AnalyticsHubServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AnalyticsHubServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = AnalyticsHubServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AnalyticsHubServiceGrpcTransport,
    )


def test_analytics_hub_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AnalyticsHubServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_analytics_hub_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.transports.AnalyticsHubServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AnalyticsHubServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_data_exchanges",
        "list_org_data_exchanges",
        "get_data_exchange",
        "create_data_exchange",
        "update_data_exchange",
        "delete_data_exchange",
        "list_listings",
        "get_listing",
        "create_listing",
        "update_listing",
        "delete_listing",
        "subscribe_listing",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_analytics_hub_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.transports.AnalyticsHubServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsHubServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_analytics_hub_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigquery_data_exchange_v1beta1.services.analytics_hub_service.transports.AnalyticsHubServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsHubServiceTransport()
        adc.assert_called_once()


def test_analytics_hub_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnalyticsHubServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_hub_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_hub_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.AnalyticsHubServiceGrpcTransport, grpc_helpers),
        (transports.AnalyticsHubServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_analytics_hub_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "analyticshub.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=["1", "2"],
            default_host="analyticshub.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_hub_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_analytics_hub_service_host_no_port(transport_name):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticshub.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("analyticshub.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_analytics_hub_service_host_with_port(transport_name):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticshub.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("analyticshub.googleapis.com:8000")


def test_analytics_hub_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsHubServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_analytics_hub_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsHubServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_hub_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsHubServiceGrpcTransport,
        transports.AnalyticsHubServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_hub_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_data_exchange_path():
    project = "squid"
    location = "clam"
    data_exchange = "whelk"
    expected = (
        "projects/{project}/locations/{location}/dataExchanges/{data_exchange}".format(
            project=project,
            location=location,
            data_exchange=data_exchange,
        )
    )
    actual = AnalyticsHubServiceClient.data_exchange_path(
        project, location, data_exchange
    )
    assert expected == actual


def test_parse_data_exchange_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "data_exchange": "nudibranch",
    }
    path = AnalyticsHubServiceClient.data_exchange_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_data_exchange_path(path)
    assert expected == actual


def test_dataset_path():
    project = "cuttlefish"
    dataset = "mussel"
    expected = "projects/{project}/datasets/{dataset}".format(
        project=project,
        dataset=dataset,
    )
    actual = AnalyticsHubServiceClient.dataset_path(project, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "winkle",
        "dataset": "nautilus",
    }
    path = AnalyticsHubServiceClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_dataset_path(path)
    assert expected == actual


def test_listing_path():
    project = "scallop"
    location = "abalone"
    data_exchange = "squid"
    listing = "clam"
    expected = "projects/{project}/locations/{location}/dataExchanges/{data_exchange}/listings/{listing}".format(
        project=project,
        location=location,
        data_exchange=data_exchange,
        listing=listing,
    )
    actual = AnalyticsHubServiceClient.listing_path(
        project, location, data_exchange, listing
    )
    assert expected == actual


def test_parse_listing_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "data_exchange": "oyster",
        "listing": "nudibranch",
    }
    path = AnalyticsHubServiceClient.listing_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_listing_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AnalyticsHubServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = AnalyticsHubServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = AnalyticsHubServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = AnalyticsHubServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = AnalyticsHubServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = AnalyticsHubServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = AnalyticsHubServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = AnalyticsHubServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = AnalyticsHubServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = AnalyticsHubServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsHubServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AnalyticsHubServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AnalyticsHubServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AnalyticsHubServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AnalyticsHubServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_list_locations(transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc"):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = AnalyticsHubServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = AnalyticsHubServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = AnalyticsHubServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = AnalyticsHubServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (AnalyticsHubServiceClient, transports.AnalyticsHubServiceGrpcTransport),
        (
            AnalyticsHubServiceAsyncClient,
            transports.AnalyticsHubServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
