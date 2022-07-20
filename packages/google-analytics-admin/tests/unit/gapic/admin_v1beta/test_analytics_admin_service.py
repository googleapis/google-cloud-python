# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    from unittest.mock import AsyncMock
except ImportError:
    import mock

import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.analytics.admin_v1beta.services.analytics_admin_service import (
    AnalyticsAdminServiceAsyncClient,
    AnalyticsAdminServiceClient,
    pagers,
    transports,
)
from google.analytics.admin_v1beta.types import analytics_admin, resources


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

    assert AnalyticsAdminServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (AnalyticsAdminServiceClient, "grpc"),
        (AnalyticsAdminServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_analytics_admin_service_client_from_service_account_info(
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

        assert client.transport._host == ("analyticsadmin.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AnalyticsAdminServiceGrpcTransport, "grpc"),
        (transports.AnalyticsAdminServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_analytics_admin_service_client_service_account_always_use_jwt(
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
        (AnalyticsAdminServiceClient, "grpc"),
        (AnalyticsAdminServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_analytics_admin_service_client_from_service_account_file(
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

        assert client.transport._host == ("analyticsadmin.googleapis.com:443")


def test_analytics_admin_service_client_get_transport_class():
    transport = AnalyticsAdminServiceClient.get_transport_class()
    available_transports = [
        transports.AnalyticsAdminServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = AnalyticsAdminServiceClient.get_transport_class("grpc")
    assert transport == transports.AnalyticsAdminServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AnalyticsAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceClient),
)
@mock.patch.object(
    AnalyticsAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceAsyncClient),
)
def test_analytics_admin_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
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
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AnalyticsAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceClient),
)
@mock.patch.object(
    AnalyticsAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_analytics_admin_service_client_mtls_env_auto(
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
    "client_class", [AnalyticsAdminServiceClient, AnalyticsAdminServiceAsyncClient]
)
@mock.patch.object(
    AnalyticsAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceClient),
)
@mock.patch.object(
    AnalyticsAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceAsyncClient),
)
def test_analytics_admin_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options_scopes(
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
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_analytics_admin_service_client_client_options_credentials_file(
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


def test_analytics_admin_service_client_client_options_from_dict():
    with mock.patch(
        "google.analytics.admin_v1beta.services.analytics_admin_service.transports.AnalyticsAdminServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AnalyticsAdminServiceClient(
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
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_analytics_admin_service_client_create_channel_credentials_file(
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
            "analyticsadmin.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            scopes=None,
            default_host="analyticsadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetAccountRequest,
        dict,
    ],
)
def test_get_account(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            region_code="region_code_value",
            deleted=True,
        )
        response = client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


def test_get_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        client.get_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()


@pytest.mark.asyncio
async def test_get_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                region_code="region_code_value",
                deleted=True,
            )
        )
        response = await client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


@pytest.mark.asyncio
async def test_get_account_async_from_dict():
    await test_get_account_async(request_type=dict)


def test_get_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        call.return_value = resources.Account()
        client.get_account(request)

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
async def test_get_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        await client.get_account(request)

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


def test_get_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_account(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_account(
            analytics_admin.GetAccountRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_account(
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
async def test_get_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_account(
            analytics_admin.GetAccountRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListAccountsRequest,
        dict,
    ],
)
def test_list_accounts(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAccountsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_accounts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        client.list_accounts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()


@pytest.mark.asyncio
async def test_list_accounts_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListAccountsRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAccountsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_accounts_async_from_dict():
    await test_list_accounts_async(request_type=dict)


def test_list_accounts_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_accounts(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Account) for i in results)


def test_list_accounts_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_accounts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_accounts_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accounts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_accounts(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Account) for i in responses)


@pytest.mark.asyncio
async def test_list_accounts_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accounts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_accounts(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteAccountRequest,
        dict,
    ],
)
def test_delete_account(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        client.delete_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()


@pytest.mark.asyncio
async def test_delete_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.DeleteAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_account_async_from_dict():
    await test_delete_account_async(request_type=dict)


def test_delete_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        call.return_value = None
        client.delete_account(request)

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
async def test_delete_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_account(request)

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


def test_delete_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_account(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_account(
            analytics_admin.DeleteAccountRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_account(
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
async def test_delete_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_account(
            analytics_admin.DeleteAccountRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateAccountRequest,
        dict,
    ],
)
def test_update_account(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            region_code="region_code_value",
            deleted=True,
        )
        response = client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


def test_update_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        client.update_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()


@pytest.mark.asyncio
async def test_update_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.UpdateAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                region_code="region_code_value",
                deleted=True,
            )
        )
        response = await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


@pytest.mark.asyncio
async def test_update_account_async_from_dict():
    await test_update_account_async(request_type=dict)


def test_update_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()

    request.account.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        call.return_value = resources.Account()
        client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "account.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()

    request.account.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "account.name=name_value",
    ) in kw["metadata"]


def test_update_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].account
        mock_val = resources.Account(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].account
        mock_val = resources.Account(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ProvisionAccountTicketRequest,
        dict,
    ],
)
def test_provision_account_ticket(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ProvisionAccountTicketResponse(
            account_ticket_id="account_ticket_id_value",
        )
        response = client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)
    assert response.account_ticket_id == "account_ticket_id_value"


def test_provision_account_ticket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        client.provision_account_ticket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()


@pytest.mark.asyncio
async def test_provision_account_ticket_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ProvisionAccountTicketRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ProvisionAccountTicketResponse(
                account_ticket_id="account_ticket_id_value",
            )
        )
        response = await client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)
    assert response.account_ticket_id == "account_ticket_id_value"


@pytest.mark.asyncio
async def test_provision_account_ticket_async_from_dict():
    await test_provision_account_ticket_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListAccountSummariesRequest,
        dict,
    ],
)
def test_list_account_summaries(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAccountSummariesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_account_summaries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountSummariesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_account_summaries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        client.list_account_summaries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()


@pytest.mark.asyncio
async def test_list_account_summaries_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListAccountSummariesRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAccountSummariesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_account_summaries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountSummariesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_account_summaries_async_from_dict():
    await test_list_account_summaries_async(request_type=dict)


def test_list_account_summaries_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_account_summaries(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.AccountSummary) for i in results)


def test_list_account_summaries_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_account_summaries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_account_summaries_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_account_summaries(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AccountSummary) for i in responses)


@pytest.mark.asyncio
async def test_list_account_summaries_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[],
                next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_account_summaries(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetPropertyRequest,
        dict,
    ],
)
def test_get_property(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
            account="account_value",
        )
        response = client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


def test_get_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        client.get_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()


@pytest.mark.asyncio
async def test_get_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetPropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
                account="account_value",
            )
        )
        response = await client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


@pytest.mark.asyncio
async def test_get_property_async_from_dict():
    await test_get_property_async(request_type=dict)


def test_get_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        call.return_value = resources.Property()
        client.get_property(request)

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
async def test_get_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.get_property(request)

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


def test_get_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_property(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_property(
            analytics_admin.GetPropertyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_property(
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
async def test_get_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_property(
            analytics_admin.GetPropertyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListPropertiesRequest,
        dict,
    ],
)
def test_list_properties(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListPropertiesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_properties_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        client.list_properties()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()


@pytest.mark.asyncio
async def test_list_properties_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListPropertiesRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListPropertiesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_properties_async_from_dict():
    await test_list_properties_async(request_type=dict)


def test_list_properties_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[],
                next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_properties(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Property) for i in results)


def test_list_properties_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[],
                next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_properties(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_properties_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_properties), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[],
                next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_properties(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Property) for i in responses)


@pytest.mark.asyncio
async def test_list_properties_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_properties), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[],
                next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_properties(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreatePropertyRequest,
        dict,
    ],
)
def test_create_property(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
            account="account_value",
        )
        response = client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


def test_create_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        client.create_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()


@pytest.mark.asyncio
async def test_create_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.CreatePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
                account="account_value",
            )
        )
        response = await client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


@pytest.mark.asyncio
async def test_create_property_async_from_dict():
    await test_create_property_async(request_type=dict)


def test_create_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_property(
            property=resources.Property(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].property
        mock_val = resources.Property(name="name_value")
        assert arg == mock_val


def test_create_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_property(
            property=resources.Property(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].property
        mock_val = resources.Property(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeletePropertyRequest,
        dict,
    ],
)
def test_delete_property(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
            account="account_value",
        )
        response = client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


def test_delete_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        client.delete_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()


@pytest.mark.asyncio
async def test_delete_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.DeletePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
                account="account_value",
            )
        )
        response = await client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


@pytest.mark.asyncio
async def test_delete_property_async_from_dict():
    await test_delete_property_async(request_type=dict)


def test_delete_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        call.return_value = resources.Property()
        client.delete_property(request)

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
async def test_delete_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.delete_property(request)

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


def test_delete_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_property(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_property(
            analytics_admin.DeletePropertyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_property(
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
async def test_delete_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_property(
            analytics_admin.DeletePropertyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdatePropertyRequest,
        dict,
    ],
)
def test_update_property(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
            service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
            account="account_value",
        )
        response = client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


def test_update_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        client.update_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()


@pytest.mark.asyncio
async def test_update_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.UpdatePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                property_type=resources.PropertyType.PROPERTY_TYPE_ORDINARY,
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
                service_level=resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD,
                account="account_value",
            )
        )
        response = await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.property_type == resources.PropertyType.PROPERTY_TYPE_ORDINARY
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"
    assert response.service_level == resources.ServiceLevel.GOOGLE_ANALYTICS_STANDARD
    assert response.account == "account_value"


@pytest.mark.asyncio
async def test_update_property_async_from_dict():
    await test_update_property_async(request_type=dict)


def test_update_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()

    request.property.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        call.return_value = resources.Property()
        client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()

    request.property.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property.name=name_value",
    ) in kw["metadata"]


def test_update_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].property
        mock_val = resources.Property(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].property
        mock_val = resources.Property(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateFirebaseLinkRequest,
        dict,
    ],
)
def test_create_firebase_link(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink(
            name="name_value",
            project="project_value",
        )
        response = client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"


def test_create_firebase_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        client.create_firebase_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()


@pytest.mark.asyncio
async def test_create_firebase_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateFirebaseLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink(
                name="name_value",
                project="project_value",
            )
        )
        response = await client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"


@pytest.mark.asyncio
async def test_create_firebase_link_async_from_dict():
    await test_create_firebase_link_async(request_type=dict)


def test_create_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = resources.FirebaseLink()
        client.create_firebase_link(request)

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
async def test_create_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        await client.create_firebase_link(request)

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


def test_create_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].firebase_link
        mock_val = resources.FirebaseLink(name="name_value")
        assert arg == mock_val


def test_create_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].firebase_link
        mock_val = resources.FirebaseLink(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteFirebaseLinkRequest,
        dict,
    ],
)
def test_delete_firebase_link(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_firebase_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        client.delete_firebase_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()


@pytest.mark.asyncio
async def test_delete_firebase_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteFirebaseLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_firebase_link_async_from_dict():
    await test_delete_firebase_link_async(request_type=dict)


def test_delete_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_firebase_link(request)

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
async def test_delete_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_firebase_link(request)

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


def test_delete_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_firebase_link(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_firebase_link(
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
async def test_delete_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListFirebaseLinksRequest,
        dict,
    ],
)
def test_list_firebase_links(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFirebaseLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_firebase_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        client.list_firebase_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()


@pytest.mark.asyncio
async def test_list_firebase_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListFirebaseLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFirebaseLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_firebase_links_async_from_dict():
    await test_list_firebase_links_async(request_type=dict)


def test_list_firebase_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListFirebaseLinksResponse()
        client.list_firebase_links(request)

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
async def test_list_firebase_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )
        await client.list_firebase_links(request)

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


def test_list_firebase_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_firebase_links(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_firebase_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_firebase_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_firebase_links(
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
async def test_list_firebase_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(),
            parent="parent_value",
        )


def test_list_firebase_links_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_firebase_links(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.FirebaseLink) for i in results)


def test_list_firebase_links_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_firebase_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_firebase_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_firebase_links(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.FirebaseLink) for i in responses)


@pytest.mark.asyncio
async def test_list_firebase_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_firebase_links(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateGoogleAdsLinkRequest,
        dict,
    ],
)
def test_create_google_ads_link(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            creator_email_address="creator_email_address_value",
        )
        response = client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.creator_email_address == "creator_email_address_value"


def test_create_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        client.create_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_create_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                creator_email_address="creator_email_address_value",
            )
        )
        response = await client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.creator_email_address == "creator_email_address_value"


@pytest.mark.asyncio
async def test_create_google_ads_link_async_from_dict():
    await test_create_google_ads_link_async(request_type=dict)


def test_create_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()
        client.create_google_ads_link(request)

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
async def test_create_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        await client.create_google_ads_link(request)

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


def test_create_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].google_ads_link
        mock_val = resources.GoogleAdsLink(name="name_value")
        assert arg == mock_val


def test_create_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].google_ads_link
        mock_val = resources.GoogleAdsLink(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateGoogleAdsLinkRequest,
        dict,
    ],
)
def test_update_google_ads_link(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            creator_email_address="creator_email_address_value",
        )
        response = client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.creator_email_address == "creator_email_address_value"


def test_update_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        client.update_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_update_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                creator_email_address="creator_email_address_value",
            )
        )
        response = await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.creator_email_address == "creator_email_address_value"


@pytest.mark.asyncio
async def test_update_google_ads_link_async_from_dict():
    await test_update_google_ads_link_async(request_type=dict)


def test_update_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    request.google_ads_link.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()
        client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    request.google_ads_link.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=name_value",
    ) in kw["metadata"]


def test_update_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].google_ads_link
        mock_val = resources.GoogleAdsLink(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].google_ads_link
        mock_val = resources.GoogleAdsLink(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteGoogleAdsLinkRequest,
        dict,
    ],
)
def test_delete_google_ads_link(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        client.delete_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_delete_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_google_ads_link_async_from_dict():
    await test_delete_google_ads_link_async(request_type=dict)


def test_delete_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_google_ads_link(request)

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
async def test_delete_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_google_ads_link(request)

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


def test_delete_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_google_ads_link(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_google_ads_link(
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
async def test_delete_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListGoogleAdsLinksRequest,
        dict,
    ],
)
def test_list_google_ads_links(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_google_ads_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        client.list_google_ads_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()


@pytest.mark.asyncio
async def test_list_google_ads_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListGoogleAdsLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_google_ads_links_async_from_dict():
    await test_list_google_ads_links_async(request_type=dict)


def test_list_google_ads_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()
        client.list_google_ads_links(request)

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
async def test_list_google_ads_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )
        await client.list_google_ads_links(request)

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


def test_list_google_ads_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_google_ads_links(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_google_ads_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_google_ads_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_google_ads_links(
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
async def test_list_google_ads_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(),
            parent="parent_value",
        )


def test_list_google_ads_links_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_google_ads_links(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in results)


def test_list_google_ads_links_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_google_ads_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_google_ads_links(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in responses)


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[],
                next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_google_ads_links(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetDataSharingSettingsRequest,
        dict,
    ],
)
def test_get_data_sharing_settings(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings(
            name="name_value",
            sharing_with_google_support_enabled=True,
            sharing_with_google_assigned_sales_enabled=True,
            sharing_with_google_any_sales_enabled=True,
            sharing_with_google_products_enabled=True,
            sharing_with_others_enabled=True,
        )
        response = client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)
    assert response.name == "name_value"
    assert response.sharing_with_google_support_enabled is True
    assert response.sharing_with_google_assigned_sales_enabled is True
    assert response.sharing_with_google_any_sales_enabled is True
    assert response.sharing_with_google_products_enabled is True
    assert response.sharing_with_others_enabled is True


def test_get_data_sharing_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        client.get_data_sharing_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()


@pytest.mark.asyncio
async def test_get_data_sharing_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetDataSharingSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings(
                name="name_value",
                sharing_with_google_support_enabled=True,
                sharing_with_google_assigned_sales_enabled=True,
                sharing_with_google_any_sales_enabled=True,
                sharing_with_google_products_enabled=True,
                sharing_with_others_enabled=True,
            )
        )
        response = await client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)
    assert response.name == "name_value"
    assert response.sharing_with_google_support_enabled is True
    assert response.sharing_with_google_assigned_sales_enabled is True
    assert response.sharing_with_google_any_sales_enabled is True
    assert response.sharing_with_google_products_enabled is True
    assert response.sharing_with_others_enabled is True


@pytest.mark.asyncio
async def test_get_data_sharing_settings_async_from_dict():
    await test_get_data_sharing_settings_async(request_type=dict)


def test_get_data_sharing_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = resources.DataSharingSettings()
        client.get_data_sharing_settings(request)

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
async def test_get_data_sharing_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )
        await client.get_data_sharing_settings(request)

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


def test_get_data_sharing_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_sharing_settings(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_data_sharing_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_sharing_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_sharing_settings(
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
async def test_get_data_sharing_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetMeasurementProtocolSecretRequest,
        dict,
    ],
)
def test_get_measurement_protocol_secret(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_get_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        client.get_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_async_from_dict():
    await test_get_measurement_protocol_secret_async(request_type=dict)


def test_get_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetMeasurementProtocolSecretRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.get_measurement_protocol_secret(request)

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
async def test_get_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetMeasurementProtocolSecretRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.get_measurement_protocol_secret(request)

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


def test_get_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_measurement_protocol_secret(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_measurement_protocol_secret(
            analytics_admin.GetMeasurementProtocolSecretRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_measurement_protocol_secret(
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
async def test_get_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_measurement_protocol_secret(
            analytics_admin.GetMeasurementProtocolSecretRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListMeasurementProtocolSecretsRequest,
        dict,
    ],
)
def test_list_measurement_protocol_secrets(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeasurementProtocolSecretsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_measurement_protocol_secrets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        client.list_measurement_protocol_secrets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListMeasurementProtocolSecretsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeasurementProtocolSecretsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_from_dict():
    await test_list_measurement_protocol_secrets_async(request_type=dict)


def test_list_measurement_protocol_secrets_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListMeasurementProtocolSecretsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()
        client.list_measurement_protocol_secrets(request)

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
async def test_list_measurement_protocol_secrets_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListMeasurementProtocolSecretsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse()
        )
        await client.list_measurement_protocol_secrets(request)

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


def test_list_measurement_protocol_secrets_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_measurement_protocol_secrets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_measurement_protocol_secrets_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_measurement_protocol_secrets(
            analytics_admin.ListMeasurementProtocolSecretsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_measurement_protocol_secrets(
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
async def test_list_measurement_protocol_secrets_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_measurement_protocol_secrets(
            analytics_admin.ListMeasurementProtocolSecretsRequest(),
            parent="parent_value",
        )


def test_list_measurement_protocol_secrets_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[],
                next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_measurement_protocol_secrets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.MeasurementProtocolSecret) for i in results)


def test_list_measurement_protocol_secrets_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[],
                next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_measurement_protocol_secrets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[],
                next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_measurement_protocol_secrets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, resources.MeasurementProtocolSecret) for i in responses
        )


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[],
                next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_measurement_protocol_secrets(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateMeasurementProtocolSecretRequest,
        dict,
    ],
)
def test_create_measurement_protocol_secret(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_create_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        client.create_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_async_from_dict():
    await test_create_measurement_protocol_secret_async(request_type=dict)


def test_create_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateMeasurementProtocolSecretRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.create_measurement_protocol_secret(request)

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
async def test_create_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateMeasurementProtocolSecretRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.create_measurement_protocol_secret(request)

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


def test_create_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_measurement_protocol_secret(
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].measurement_protocol_secret
        mock_val = resources.MeasurementProtocolSecret(name="name_value")
        assert arg == mock_val


def test_create_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_measurement_protocol_secret(
            analytics_admin.CreateMeasurementProtocolSecretRequest(),
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_measurement_protocol_secret(
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].measurement_protocol_secret
        mock_val = resources.MeasurementProtocolSecret(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_measurement_protocol_secret(
            analytics_admin.CreateMeasurementProtocolSecretRequest(),
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteMeasurementProtocolSecretRequest,
        dict,
    ],
)
def test_delete_measurement_protocol_secret(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        client.delete_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_async_from_dict():
    await test_delete_measurement_protocol_secret_async(request_type=dict)


def test_delete_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteMeasurementProtocolSecretRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = None
        client.delete_measurement_protocol_secret(request)

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
async def test_delete_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteMeasurementProtocolSecretRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_measurement_protocol_secret(request)

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


def test_delete_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_measurement_protocol_secret(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_measurement_protocol_secret(
            analytics_admin.DeleteMeasurementProtocolSecretRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_measurement_protocol_secret(
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
async def test_delete_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_measurement_protocol_secret(
            analytics_admin.DeleteMeasurementProtocolSecretRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateMeasurementProtocolSecretRequest,
        dict,
    ],
)
def test_update_measurement_protocol_secret(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_update_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        client.update_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_async_from_dict():
    await test_update_measurement_protocol_secret_async(request_type=dict)


def test_update_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateMeasurementProtocolSecretRequest()

    request.measurement_protocol_secret.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "measurement_protocol_secret.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateMeasurementProtocolSecretRequest()

    request.measurement_protocol_secret.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "measurement_protocol_secret.name=name_value",
    ) in kw["metadata"]


def test_update_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_measurement_protocol_secret(
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].measurement_protocol_secret
        mock_val = resources.MeasurementProtocolSecret(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_measurement_protocol_secret(
            analytics_admin.UpdateMeasurementProtocolSecretRequest(),
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_measurement_protocol_secret(
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].measurement_protocol_secret
        mock_val = resources.MeasurementProtocolSecret(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_measurement_protocol_secret(
            analytics_admin.UpdateMeasurementProtocolSecretRequest(),
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.AcknowledgeUserDataCollectionRequest,
        dict,
    ],
)
def test_acknowledge_user_data_collection(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.acknowledge_user_data_collection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.AcknowledgeUserDataCollectionResponse()
        response = client.acknowledge_user_data_collection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AcknowledgeUserDataCollectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.AcknowledgeUserDataCollectionResponse)


def test_acknowledge_user_data_collection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.acknowledge_user_data_collection), "__call__"
    ) as call:
        client.acknowledge_user_data_collection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AcknowledgeUserDataCollectionRequest()


@pytest.mark.asyncio
async def test_acknowledge_user_data_collection_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.AcknowledgeUserDataCollectionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.acknowledge_user_data_collection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AcknowledgeUserDataCollectionResponse()
        )
        response = await client.acknowledge_user_data_collection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AcknowledgeUserDataCollectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.AcknowledgeUserDataCollectionResponse)


@pytest.mark.asyncio
async def test_acknowledge_user_data_collection_async_from_dict():
    await test_acknowledge_user_data_collection_async(request_type=dict)


def test_acknowledge_user_data_collection_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AcknowledgeUserDataCollectionRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.acknowledge_user_data_collection), "__call__"
    ) as call:
        call.return_value = analytics_admin.AcknowledgeUserDataCollectionResponse()
        client.acknowledge_user_data_collection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_acknowledge_user_data_collection_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AcknowledgeUserDataCollectionRequest()

    request.property = "property_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.acknowledge_user_data_collection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AcknowledgeUserDataCollectionResponse()
        )
        await client.acknowledge_user_data_collection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "property=property_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.SearchChangeHistoryEventsRequest,
        dict,
    ],
)
def test_search_change_history_events(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.SearchChangeHistoryEventsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchChangeHistoryEventsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_change_history_events_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        client.search_change_history_events()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()


@pytest.mark.asyncio
async def test_search_change_history_events_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.SearchChangeHistoryEventsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.SearchChangeHistoryEventsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchChangeHistoryEventsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_change_history_events_async_from_dict():
    await test_search_change_history_events_async(request_type=dict)


def test_search_change_history_events_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.SearchChangeHistoryEventsRequest()

    request.account = "account_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        call.return_value = analytics_admin.SearchChangeHistoryEventsResponse()
        client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "account=account_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_change_history_events_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.SearchChangeHistoryEventsRequest()

    request.account = "account_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.SearchChangeHistoryEventsResponse()
        )
        await client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "account=account_value",
    ) in kw["metadata"]


def test_search_change_history_events_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[],
                next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", ""),)),
        )
        pager = client.search_change_history_events(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.ChangeHistoryEvent) for i in results)


def test_search_change_history_events_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[],
                next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_change_history_events(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_change_history_events_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[],
                next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_change_history_events(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ChangeHistoryEvent) for i in responses)


@pytest.mark.asyncio
async def test_search_change_history_events_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[],
                next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.search_change_history_events(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateConversionEventRequest,
        dict,
    ],
)
def test_create_conversion_event(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent(
            name="name_value",
            event_name="event_name_value",
            deletable=True,
            custom=True,
        )
        response = client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.deletable is True
    assert response.custom is True


def test_create_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        client.create_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()


@pytest.mark.asyncio
async def test_create_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent(
                name="name_value",
                event_name="event_name_value",
                deletable=True,
                custom=True,
            )
        )
        response = await client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.deletable is True
    assert response.custom is True


@pytest.mark.asyncio
async def test_create_conversion_event_async_from_dict():
    await test_create_conversion_event_async(request_type=dict)


def test_create_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateConversionEventRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        call.return_value = resources.ConversionEvent()
        client.create_conversion_event(request)

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
async def test_create_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateConversionEventRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        await client.create_conversion_event(request)

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


def test_create_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversion_event(
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_event
        mock_val = resources.ConversionEvent(name="name_value")
        assert arg == mock_val


def test_create_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversion_event(
            analytics_admin.CreateConversionEventRequest(),
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversion_event(
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_event
        mock_val = resources.ConversionEvent(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversion_event(
            analytics_admin.CreateConversionEventRequest(),
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetConversionEventRequest,
        dict,
    ],
)
def test_get_conversion_event(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent(
            name="name_value",
            event_name="event_name_value",
            deletable=True,
            custom=True,
        )
        response = client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.deletable is True
    assert response.custom is True


def test_get_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        client.get_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()


@pytest.mark.asyncio
async def test_get_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent(
                name="name_value",
                event_name="event_name_value",
                deletable=True,
                custom=True,
            )
        )
        response = await client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.deletable is True
    assert response.custom is True


@pytest.mark.asyncio
async def test_get_conversion_event_async_from_dict():
    await test_get_conversion_event_async(request_type=dict)


def test_get_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetConversionEventRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        call.return_value = resources.ConversionEvent()
        client.get_conversion_event(request)

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
async def test_get_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetConversionEventRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        await client.get_conversion_event(request)

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


def test_get_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversion_event(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversion_event(
            analytics_admin.GetConversionEventRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversion_event(
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
async def test_get_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversion_event(
            analytics_admin.GetConversionEventRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteConversionEventRequest,
        dict,
    ],
)
def test_delete_conversion_event(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        client.delete_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()


@pytest.mark.asyncio
async def test_delete_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_conversion_event_async_from_dict():
    await test_delete_conversion_event_async(request_type=dict)


def test_delete_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteConversionEventRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        call.return_value = None
        client.delete_conversion_event(request)

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
async def test_delete_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteConversionEventRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_conversion_event(request)

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


def test_delete_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_conversion_event(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversion_event(
            analytics_admin.DeleteConversionEventRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_conversion_event(
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
async def test_delete_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_conversion_event(
            analytics_admin.DeleteConversionEventRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListConversionEventsRequest,
        dict,
    ],
)
def test_list_conversion_events(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionEventsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversion_events_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        client.list_conversion_events()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()


@pytest.mark.asyncio
async def test_list_conversion_events_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListConversionEventsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionEventsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_conversion_events_async_from_dict():
    await test_list_conversion_events_async(request_type=dict)


def test_list_conversion_events_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListConversionEventsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListConversionEventsResponse()
        client.list_conversion_events(request)

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
async def test_list_conversion_events_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListConversionEventsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse()
        )
        await client.list_conversion_events(request)

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


def test_list_conversion_events_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversion_events(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_conversion_events_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversion_events(
            analytics_admin.ListConversionEventsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversion_events_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversion_events(
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
async def test_list_conversion_events_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversion_events(
            analytics_admin.ListConversionEventsRequest(),
            parent="parent_value",
        )


def test_list_conversion_events_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[],
                next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversion_events(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.ConversionEvent) for i in results)


def test_list_conversion_events_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[],
                next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversion_events(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversion_events_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[],
                next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversion_events(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ConversionEvent) for i in responses)


@pytest.mark.asyncio
async def test_list_conversion_events_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[],
                next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_conversion_events(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateCustomDimensionRequest,
        dict,
    ],
)
def test_create_custom_dimension(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_create_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        client.create_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()


@pytest.mark.asyncio
async def test_create_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_create_custom_dimension_async_from_dict():
    await test_create_custom_dimension_async(request_type=dict)


def test_create_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomDimensionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.create_custom_dimension(request)

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
async def test_create_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomDimensionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.create_custom_dimension(request)

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


def test_create_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_dimension(
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_dimension
        mock_val = resources.CustomDimension(name="name_value")
        assert arg == mock_val


def test_create_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_dimension(
            analytics_admin.CreateCustomDimensionRequest(),
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_dimension(
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_dimension
        mock_val = resources.CustomDimension(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_dimension(
            analytics_admin.CreateCustomDimensionRequest(),
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateCustomDimensionRequest,
        dict,
    ],
)
def test_update_custom_dimension(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_update_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        client.update_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()


@pytest.mark.asyncio
async def test_update_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_update_custom_dimension_async_from_dict():
    await test_update_custom_dimension_async(request_type=dict)


def test_update_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomDimensionRequest()

    request.custom_dimension.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_dimension.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomDimensionRequest()

    request.custom_dimension.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_dimension.name=name_value",
    ) in kw["metadata"]


def test_update_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_dimension(
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_dimension
        mock_val = resources.CustomDimension(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_dimension(
            analytics_admin.UpdateCustomDimensionRequest(),
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_dimension(
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_dimension
        mock_val = resources.CustomDimension(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_dimension(
            analytics_admin.UpdateCustomDimensionRequest(),
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListCustomDimensionsRequest,
        dict,
    ],
)
def test_list_custom_dimensions(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomDimensionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_dimensions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        client.list_custom_dimensions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()


@pytest.mark.asyncio
async def test_list_custom_dimensions_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListCustomDimensionsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomDimensionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_from_dict():
    await test_list_custom_dimensions_async(request_type=dict)


def test_list_custom_dimensions_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomDimensionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListCustomDimensionsResponse()
        client.list_custom_dimensions(request)

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
async def test_list_custom_dimensions_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomDimensionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse()
        )
        await client.list_custom_dimensions(request)

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


def test_list_custom_dimensions_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_dimensions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_custom_dimensions_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_dimensions(
            analytics_admin.ListCustomDimensionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_dimensions_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_dimensions(
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
async def test_list_custom_dimensions_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_dimensions(
            analytics_admin.ListCustomDimensionsRequest(),
            parent="parent_value",
        )


def test_list_custom_dimensions_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_dimensions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CustomDimension) for i in results)


def test_list_custom_dimensions_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_dimensions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_dimensions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CustomDimension) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_custom_dimensions(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ArchiveCustomDimensionRequest,
        dict,
    ],
)
def test_archive_custom_dimension(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_archive_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        client.archive_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()


@pytest.mark.asyncio
async def test_archive_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ArchiveCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_archive_custom_dimension_async_from_dict():
    await test_archive_custom_dimension_async(request_type=dict)


def test_archive_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomDimensionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        call.return_value = None
        client.archive_custom_dimension(request)

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
async def test_archive_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomDimensionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.archive_custom_dimension(request)

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


def test_archive_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.archive_custom_dimension(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_archive_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.archive_custom_dimension(
            analytics_admin.ArchiveCustomDimensionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_archive_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.archive_custom_dimension(
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
async def test_archive_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.archive_custom_dimension(
            analytics_admin.ArchiveCustomDimensionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetCustomDimensionRequest,
        dict,
    ],
)
def test_get_custom_dimension(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_get_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        client.get_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()


@pytest.mark.asyncio
async def test_get_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_get_custom_dimension_async_from_dict():
    await test_get_custom_dimension_async(request_type=dict)


def test_get_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomDimensionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.get_custom_dimension(request)

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
async def test_get_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomDimensionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.get_custom_dimension(request)

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


def test_get_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_dimension(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_dimension(
            analytics_admin.GetCustomDimensionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_dimension(
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
async def test_get_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_dimension(
            analytics_admin.GetCustomDimensionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateCustomMetricRequest,
        dict,
    ],
)
def test_create_custom_metric(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
            restricted_metric_type=[
                resources.CustomMetric.RestrictedMetricType.COST_DATA
            ],
        )
        response = client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


def test_create_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        client.create_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()


@pytest.mark.asyncio
async def test_create_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
                restricted_metric_type=[
                    resources.CustomMetric.RestrictedMetricType.COST_DATA
                ],
            )
        )
        response = await client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


@pytest.mark.asyncio
async def test_create_custom_metric_async_from_dict():
    await test_create_custom_metric_async(request_type=dict)


def test_create_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomMetricRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.create_custom_metric(request)

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
async def test_create_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomMetricRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.create_custom_metric(request)

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


def test_create_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_metric(
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_metric
        mock_val = resources.CustomMetric(name="name_value")
        assert arg == mock_val


def test_create_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_metric(
            analytics_admin.CreateCustomMetricRequest(),
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_metric(
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_metric
        mock_val = resources.CustomMetric(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_metric(
            analytics_admin.CreateCustomMetricRequest(),
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateCustomMetricRequest,
        dict,
    ],
)
def test_update_custom_metric(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
            restricted_metric_type=[
                resources.CustomMetric.RestrictedMetricType.COST_DATA
            ],
        )
        response = client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


def test_update_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        client.update_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()


@pytest.mark.asyncio
async def test_update_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
                restricted_metric_type=[
                    resources.CustomMetric.RestrictedMetricType.COST_DATA
                ],
            )
        )
        response = await client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


@pytest.mark.asyncio
async def test_update_custom_metric_async_from_dict():
    await test_update_custom_metric_async(request_type=dict)


def test_update_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomMetricRequest()

    request.custom_metric.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_metric.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomMetricRequest()

    request.custom_metric.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_metric.name=name_value",
    ) in kw["metadata"]


def test_update_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_metric(
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_metric
        mock_val = resources.CustomMetric(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_metric(
            analytics_admin.UpdateCustomMetricRequest(),
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_metric(
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_metric
        mock_val = resources.CustomMetric(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_metric(
            analytics_admin.UpdateCustomMetricRequest(),
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListCustomMetricsRequest,
        dict,
    ],
)
def test_list_custom_metrics(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomMetricsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_metrics_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        client.list_custom_metrics()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()


@pytest.mark.asyncio
async def test_list_custom_metrics_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListCustomMetricsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomMetricsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_metrics_async_from_dict():
    await test_list_custom_metrics_async(request_type=dict)


def test_list_custom_metrics_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomMetricsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListCustomMetricsResponse()
        client.list_custom_metrics(request)

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
async def test_list_custom_metrics_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomMetricsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse()
        )
        await client.list_custom_metrics(request)

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


def test_list_custom_metrics_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_metrics(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_custom_metrics_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_metrics(
            analytics_admin.ListCustomMetricsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_metrics_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_metrics(
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
async def test_list_custom_metrics_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_metrics(
            analytics_admin.ListCustomMetricsRequest(),
            parent="parent_value",
        )


def test_list_custom_metrics_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_metrics(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.CustomMetric) for i in results)


def test_list_custom_metrics_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_metrics(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_metrics_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_metrics(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CustomMetric) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_metrics_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[],
                next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_custom_metrics(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ArchiveCustomMetricRequest,
        dict,
    ],
)
def test_archive_custom_metric(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_archive_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        client.archive_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()


@pytest.mark.asyncio
async def test_archive_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ArchiveCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_archive_custom_metric_async_from_dict():
    await test_archive_custom_metric_async(request_type=dict)


def test_archive_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomMetricRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        call.return_value = None
        client.archive_custom_metric(request)

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
async def test_archive_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomMetricRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.archive_custom_metric(request)

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


def test_archive_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.archive_custom_metric(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_archive_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.archive_custom_metric(
            analytics_admin.ArchiveCustomMetricRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_archive_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.archive_custom_metric(
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
async def test_archive_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.archive_custom_metric(
            analytics_admin.ArchiveCustomMetricRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetCustomMetricRequest,
        dict,
    ],
)
def test_get_custom_metric(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
            restricted_metric_type=[
                resources.CustomMetric.RestrictedMetricType.COST_DATA
            ],
        )
        response = client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


def test_get_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        client.get_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()


@pytest.mark.asyncio
async def test_get_custom_metric_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetCustomMetricRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
                restricted_metric_type=[
                    resources.CustomMetric.RestrictedMetricType.COST_DATA
                ],
            )
        )
        response = await client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT
    assert response.restricted_metric_type == [
        resources.CustomMetric.RestrictedMetricType.COST_DATA
    ]


@pytest.mark.asyncio
async def test_get_custom_metric_async_from_dict():
    await test_get_custom_metric_async(request_type=dict)


def test_get_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomMetricRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.get_custom_metric(request)

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
async def test_get_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomMetricRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.get_custom_metric(request)

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


def test_get_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_metric(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_metric(
            analytics_admin.GetCustomMetricRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_metric(
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
async def test_get_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_metric(
            analytics_admin.GetCustomMetricRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetDataRetentionSettingsRequest,
        dict,
    ],
)
def test_get_data_retention_settings(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings(
            name="name_value",
            event_data_retention=resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS,
            reset_user_data_on_new_activity=True,
        )
        response = client.get_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataRetentionSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataRetentionSettings)
    assert response.name == "name_value"
    assert (
        response.event_data_retention
        == resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS
    )
    assert response.reset_user_data_on_new_activity is True


def test_get_data_retention_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        client.get_data_retention_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataRetentionSettingsRequest()


@pytest.mark.asyncio
async def test_get_data_retention_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetDataRetentionSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings(
                name="name_value",
                event_data_retention=resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS,
                reset_user_data_on_new_activity=True,
            )
        )
        response = await client.get_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataRetentionSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataRetentionSettings)
    assert response.name == "name_value"
    assert (
        response.event_data_retention
        == resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS
    )
    assert response.reset_user_data_on_new_activity is True


@pytest.mark.asyncio
async def test_get_data_retention_settings_async_from_dict():
    await test_get_data_retention_settings_async(request_type=dict)


def test_get_data_retention_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataRetentionSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        call.return_value = resources.DataRetentionSettings()
        client.get_data_retention_settings(request)

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
async def test_get_data_retention_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataRetentionSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings()
        )
        await client.get_data_retention_settings(request)

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


def test_get_data_retention_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_retention_settings(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_data_retention_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_retention_settings(
            analytics_admin.GetDataRetentionSettingsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_retention_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_retention_settings(
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
async def test_get_data_retention_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_retention_settings(
            analytics_admin.GetDataRetentionSettingsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateDataRetentionSettingsRequest,
        dict,
    ],
)
def test_update_data_retention_settings(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings(
            name="name_value",
            event_data_retention=resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS,
            reset_user_data_on_new_activity=True,
        )
        response = client.update_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataRetentionSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataRetentionSettings)
    assert response.name == "name_value"
    assert (
        response.event_data_retention
        == resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS
    )
    assert response.reset_user_data_on_new_activity is True


def test_update_data_retention_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        client.update_data_retention_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataRetentionSettingsRequest()


@pytest.mark.asyncio
async def test_update_data_retention_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateDataRetentionSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings(
                name="name_value",
                event_data_retention=resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS,
                reset_user_data_on_new_activity=True,
            )
        )
        response = await client.update_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataRetentionSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataRetentionSettings)
    assert response.name == "name_value"
    assert (
        response.event_data_retention
        == resources.DataRetentionSettings.RetentionDuration.TWO_MONTHS
    )
    assert response.reset_user_data_on_new_activity is True


@pytest.mark.asyncio
async def test_update_data_retention_settings_async_from_dict():
    await test_update_data_retention_settings_async(request_type=dict)


def test_update_data_retention_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateDataRetentionSettingsRequest()

    request.data_retention_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        call.return_value = resources.DataRetentionSettings()
        client.update_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_retention_settings.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_data_retention_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateDataRetentionSettingsRequest()

    request.data_retention_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings()
        )
        await client.update_data_retention_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_retention_settings.name=name_value",
    ) in kw["metadata"]


def test_update_data_retention_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_data_retention_settings(
            data_retention_settings=resources.DataRetentionSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_retention_settings
        mock_val = resources.DataRetentionSettings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_data_retention_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_data_retention_settings(
            analytics_admin.UpdateDataRetentionSettingsRequest(),
            data_retention_settings=resources.DataRetentionSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_data_retention_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_retention_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataRetentionSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataRetentionSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_data_retention_settings(
            data_retention_settings=resources.DataRetentionSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_retention_settings
        mock_val = resources.DataRetentionSettings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_data_retention_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_data_retention_settings(
            analytics_admin.UpdateDataRetentionSettingsRequest(),
            data_retention_settings=resources.DataRetentionSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.CreateDataStreamRequest,
        dict,
    ],
)
def test_create_data_stream(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream(
            name="name_value",
            type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
            display_name="display_name_value",
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            ),
        )
        response = client.create_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


def test_create_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        client.create_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateDataStreamRequest()


@pytest.mark.asyncio
async def test_create_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream(
                name="name_value",
                type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
                display_name="display_name_value",
            )
        )
        response = await client.create_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_data_stream_async_from_dict():
    await test_create_data_stream_async(request_type=dict)


def test_create_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateDataStreamRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        call.return_value = resources.DataStream()
        client.create_data_stream(request)

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
async def test_create_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateDataStreamRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        await client.create_data_stream(request)

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


def test_create_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_data_stream(
            parent="parent_value",
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
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
        arg = args[0].data_stream
        mock_val = resources.DataStream(
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            )
        )
        assert arg == mock_val


def test_create_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_data_stream(
            analytics_admin.CreateDataStreamRequest(),
            parent="parent_value",
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_data_stream(
            parent="parent_value",
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
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
        arg = args[0].data_stream
        mock_val = resources.DataStream(
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            )
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_data_stream(
            analytics_admin.CreateDataStreamRequest(),
            parent="parent_value",
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.DeleteDataStreamRequest,
        dict,
    ],
)
def test_delete_data_stream(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        client.delete_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteDataStreamRequest()


@pytest.mark.asyncio
async def test_delete_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_data_stream_async_from_dict():
    await test_delete_data_stream_async(request_type=dict)


def test_delete_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteDataStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        call.return_value = None
        client.delete_data_stream(request)

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
async def test_delete_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteDataStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_data_stream(request)

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


def test_delete_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_data_stream(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_data_stream(
            analytics_admin.DeleteDataStreamRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_data_stream(
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
async def test_delete_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_data_stream(
            analytics_admin.DeleteDataStreamRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.UpdateDataStreamRequest,
        dict,
    ],
)
def test_update_data_stream(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream(
            name="name_value",
            type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
            display_name="display_name_value",
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            ),
        )
        response = client.update_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


def test_update_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        client.update_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataStreamRequest()


@pytest.mark.asyncio
async def test_update_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream(
                name="name_value",
                type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
                display_name="display_name_value",
            )
        )
        response = await client.update_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_data_stream_async_from_dict():
    await test_update_data_stream_async(request_type=dict)


def test_update_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateDataStreamRequest()

    request.data_stream.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        call.return_value = resources.DataStream()
        client.update_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_stream.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateDataStreamRequest()

    request.data_stream.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        await client.update_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "data_stream.name=name_value",
    ) in kw["metadata"]


def test_update_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_data_stream(
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_stream
        mock_val = resources.DataStream(
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_data_stream(
            analytics_admin.UpdateDataStreamRequest(),
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_data_stream(
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].data_stream
        mock_val = resources.DataStream(
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_data_stream(
            analytics_admin.UpdateDataStreamRequest(),
            data_stream=resources.DataStream(
                web_stream_data=resources.DataStream.WebStreamData(
                    measurement_id="measurement_id_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.ListDataStreamsRequest,
        dict,
    ],
)
def test_list_data_streams(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListDataStreamsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataStreamsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_data_streams_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        client.list_data_streams()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListDataStreamsRequest()


@pytest.mark.asyncio
async def test_list_data_streams_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListDataStreamsRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDataStreamsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_data_streams_async_from_dict():
    await test_list_data_streams_async(request_type=dict)


def test_list_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListDataStreamsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListDataStreamsResponse()
        client.list_data_streams(request)

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
async def test_list_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListDataStreamsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListDataStreamsResponse()
        )
        await client.list_data_streams(request)

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


def test_list_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListDataStreamsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_data_streams(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_data_streams(
            analytics_admin.ListDataStreamsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_data_streams(
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
async def test_list_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_data_streams(
            analytics_admin.ListDataStreamsRequest(),
            parent="parent_value",
        )


def test_list_data_streams_pager(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                    resources.DataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[],
                next_page_token="def",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_data_streams(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.DataStream) for i in results)


def test_list_data_streams_pages(transport_name: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                    resources.DataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[],
                next_page_token="def",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_data_streams(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                    resources.DataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[],
                next_page_token="def",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_data_streams(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.DataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                    resources.DataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[],
                next_page_token="def",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                ],
                next_page_token="ghi",
            ),
            analytics_admin.ListDataStreamsResponse(
                data_streams=[
                    resources.DataStream(),
                    resources.DataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_data_streams(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        analytics_admin.GetDataStreamRequest,
        dict,
    ],
)
def test_get_data_stream(request_type, transport: str = "grpc"):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream(
            name="name_value",
            type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
            display_name="display_name_value",
            web_stream_data=resources.DataStream.WebStreamData(
                measurement_id="measurement_id_value"
            ),
        )
        response = client.get_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


def test_get_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        client.get_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataStreamRequest()


@pytest.mark.asyncio
async def test_get_data_stream_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetDataStreamRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream(
                name="name_value",
                type_=resources.DataStream.DataStreamType.WEB_DATA_STREAM,
                display_name="display_name_value",
            )
        )
        response = await client.get_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataStream)
    assert response.name == "name_value"
    assert response.type_ == resources.DataStream.DataStreamType.WEB_DATA_STREAM
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_data_stream_async_from_dict():
    await test_get_data_stream_async(request_type=dict)


def test_get_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        call.return_value = resources.DataStream()
        client.get_data_stream(request)

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
async def test_get_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        await client.get_data_stream(request)

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


def test_get_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_stream(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_stream(
            analytics_admin.GetDataStreamRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_data_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_stream(
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
async def test_get_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_stream(
            analytics_admin.GetDataStreamRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AnalyticsAdminServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
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
    transport = AnalyticsAdminServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AnalyticsAdminServiceGrpcTransport,
    )


def test_analytics_admin_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AnalyticsAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_analytics_admin_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.analytics.admin_v1beta.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AnalyticsAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_account",
        "list_accounts",
        "delete_account",
        "update_account",
        "provision_account_ticket",
        "list_account_summaries",
        "get_property",
        "list_properties",
        "create_property",
        "delete_property",
        "update_property",
        "create_firebase_link",
        "delete_firebase_link",
        "list_firebase_links",
        "create_google_ads_link",
        "update_google_ads_link",
        "delete_google_ads_link",
        "list_google_ads_links",
        "get_data_sharing_settings",
        "get_measurement_protocol_secret",
        "list_measurement_protocol_secrets",
        "create_measurement_protocol_secret",
        "delete_measurement_protocol_secret",
        "update_measurement_protocol_secret",
        "acknowledge_user_data_collection",
        "search_change_history_events",
        "create_conversion_event",
        "get_conversion_event",
        "delete_conversion_event",
        "list_conversion_events",
        "create_custom_dimension",
        "update_custom_dimension",
        "list_custom_dimensions",
        "archive_custom_dimension",
        "get_custom_dimension",
        "create_custom_metric",
        "update_custom_metric",
        "list_custom_metrics",
        "archive_custom_metric",
        "get_custom_metric",
        "get_data_retention_settings",
        "update_data_retention_settings",
        "create_data_stream",
        "delete_data_stream",
        "update_data_stream",
        "list_data_streams",
        "get_data_stream",
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


def test_analytics_admin_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.analytics.admin_v1beta.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_analytics_admin_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.analytics.admin_v1beta.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport()
        adc.assert_called_once()


def test_analytics_admin_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnalyticsAdminServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.AnalyticsAdminServiceGrpcTransport, grpc_helpers),
        (transports.AnalyticsAdminServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_analytics_admin_service_transport_create_channel(
    transport_class, grpc_helpers
):
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
            "analyticsadmin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            scopes=["1", "2"],
            default_host="analyticsadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_grpc_transport_client_cert_source_for_mtls(
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
def test_analytics_admin_service_host_no_port(transport_name):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("analyticsadmin.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_analytics_admin_service_host_with_port(transport_name):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("analyticsadmin.googleapis.com:8000")


def test_analytics_admin_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_analytics_admin_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
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
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_channel_mtls_with_client_cert_source(
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
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_channel_mtls_with_adc(transport_class):
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


def test_account_path():
    account = "squid"
    expected = "accounts/{account}".format(
        account=account,
    )
    actual = AnalyticsAdminServiceClient.account_path(account)
    assert expected == actual


def test_parse_account_path():
    expected = {
        "account": "clam",
    }
    path = AnalyticsAdminServiceClient.account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_account_path(path)
    assert expected == actual


def test_account_summary_path():
    account_summary = "whelk"
    expected = "accountSummaries/{account_summary}".format(
        account_summary=account_summary,
    )
    actual = AnalyticsAdminServiceClient.account_summary_path(account_summary)
    assert expected == actual


def test_parse_account_summary_path():
    expected = {
        "account_summary": "octopus",
    }
    path = AnalyticsAdminServiceClient.account_summary_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_account_summary_path(path)
    assert expected == actual


def test_conversion_event_path():
    property = "oyster"
    conversion_event = "nudibranch"
    expected = "properties/{property}/conversionEvents/{conversion_event}".format(
        property=property,
        conversion_event=conversion_event,
    )
    actual = AnalyticsAdminServiceClient.conversion_event_path(
        property, conversion_event
    )
    assert expected == actual


def test_parse_conversion_event_path():
    expected = {
        "property": "cuttlefish",
        "conversion_event": "mussel",
    }
    path = AnalyticsAdminServiceClient.conversion_event_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_conversion_event_path(path)
    assert expected == actual


def test_custom_dimension_path():
    property = "winkle"
    custom_dimension = "nautilus"
    expected = "properties/{property}/customDimensions/{custom_dimension}".format(
        property=property,
        custom_dimension=custom_dimension,
    )
    actual = AnalyticsAdminServiceClient.custom_dimension_path(
        property, custom_dimension
    )
    assert expected == actual


def test_parse_custom_dimension_path():
    expected = {
        "property": "scallop",
        "custom_dimension": "abalone",
    }
    path = AnalyticsAdminServiceClient.custom_dimension_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_custom_dimension_path(path)
    assert expected == actual


def test_custom_metric_path():
    property = "squid"
    custom_metric = "clam"
    expected = "properties/{property}/customMetrics/{custom_metric}".format(
        property=property,
        custom_metric=custom_metric,
    )
    actual = AnalyticsAdminServiceClient.custom_metric_path(property, custom_metric)
    assert expected == actual


def test_parse_custom_metric_path():
    expected = {
        "property": "whelk",
        "custom_metric": "octopus",
    }
    path = AnalyticsAdminServiceClient.custom_metric_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_custom_metric_path(path)
    assert expected == actual


def test_data_retention_settings_path():
    property = "oyster"
    expected = "properties/{property}/dataRetentionSettings".format(
        property=property,
    )
    actual = AnalyticsAdminServiceClient.data_retention_settings_path(property)
    assert expected == actual


def test_parse_data_retention_settings_path():
    expected = {
        "property": "nudibranch",
    }
    path = AnalyticsAdminServiceClient.data_retention_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_data_retention_settings_path(path)
    assert expected == actual


def test_data_sharing_settings_path():
    account = "cuttlefish"
    expected = "accounts/{account}/dataSharingSettings".format(
        account=account,
    )
    actual = AnalyticsAdminServiceClient.data_sharing_settings_path(account)
    assert expected == actual


def test_parse_data_sharing_settings_path():
    expected = {
        "account": "mussel",
    }
    path = AnalyticsAdminServiceClient.data_sharing_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_data_sharing_settings_path(path)
    assert expected == actual


def test_data_stream_path():
    property = "winkle"
    data_stream = "nautilus"
    expected = "properties/{property}/dataStreams/{data_stream}".format(
        property=property,
        data_stream=data_stream,
    )
    actual = AnalyticsAdminServiceClient.data_stream_path(property, data_stream)
    assert expected == actual


def test_parse_data_stream_path():
    expected = {
        "property": "scallop",
        "data_stream": "abalone",
    }
    path = AnalyticsAdminServiceClient.data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_data_stream_path(path)
    assert expected == actual


def test_firebase_link_path():
    property = "squid"
    firebase_link = "clam"
    expected = "properties/{property}/firebaseLinks/{firebase_link}".format(
        property=property,
        firebase_link=firebase_link,
    )
    actual = AnalyticsAdminServiceClient.firebase_link_path(property, firebase_link)
    assert expected == actual


def test_parse_firebase_link_path():
    expected = {
        "property": "whelk",
        "firebase_link": "octopus",
    }
    path = AnalyticsAdminServiceClient.firebase_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_firebase_link_path(path)
    assert expected == actual


def test_google_ads_link_path():
    property = "oyster"
    google_ads_link = "nudibranch"
    expected = "properties/{property}/googleAdsLinks/{google_ads_link}".format(
        property=property,
        google_ads_link=google_ads_link,
    )
    actual = AnalyticsAdminServiceClient.google_ads_link_path(property, google_ads_link)
    assert expected == actual


def test_parse_google_ads_link_path():
    expected = {
        "property": "cuttlefish",
        "google_ads_link": "mussel",
    }
    path = AnalyticsAdminServiceClient.google_ads_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_google_ads_link_path(path)
    assert expected == actual


def test_measurement_protocol_secret_path():
    property = "winkle"
    data_stream = "nautilus"
    measurement_protocol_secret = "scallop"
    expected = "properties/{property}/dataStreams/{data_stream}/measurementProtocolSecrets/{measurement_protocol_secret}".format(
        property=property,
        data_stream=data_stream,
        measurement_protocol_secret=measurement_protocol_secret,
    )
    actual = AnalyticsAdminServiceClient.measurement_protocol_secret_path(
        property, data_stream, measurement_protocol_secret
    )
    assert expected == actual


def test_parse_measurement_protocol_secret_path():
    expected = {
        "property": "abalone",
        "data_stream": "squid",
        "measurement_protocol_secret": "clam",
    }
    path = AnalyticsAdminServiceClient.measurement_protocol_secret_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_measurement_protocol_secret_path(path)
    assert expected == actual


def test_property_path():
    property = "whelk"
    expected = "properties/{property}".format(
        property=property,
    )
    actual = AnalyticsAdminServiceClient.property_path(property)
    assert expected == actual


def test_parse_property_path():
    expected = {
        "property": "octopus",
    }
    path = AnalyticsAdminServiceClient.property_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_property_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AnalyticsAdminServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = AnalyticsAdminServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = AnalyticsAdminServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = AnalyticsAdminServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = AnalyticsAdminServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = AnalyticsAdminServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = AnalyticsAdminServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = AnalyticsAdminServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = AnalyticsAdminServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = AnalyticsAdminServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AnalyticsAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AnalyticsAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AnalyticsAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AnalyticsAdminServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = AnalyticsAdminServiceClient(
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
        client = AnalyticsAdminServiceClient(
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
        (AnalyticsAdminServiceClient, transports.AnalyticsAdminServiceGrpcTransport),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
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
