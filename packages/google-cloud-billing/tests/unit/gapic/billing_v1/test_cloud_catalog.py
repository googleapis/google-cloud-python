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

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.billing_v1.services.cloud_catalog import (
    CloudCatalogAsyncClient,
    CloudCatalogClient,
    pagers,
    transports,
)
from google.cloud.billing_v1.types import cloud_catalog


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

    assert CloudCatalogClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudCatalogClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudCatalogClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudCatalogClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudCatalogClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudCatalogClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudCatalogClient, "grpc"),
        (CloudCatalogAsyncClient, "grpc_asyncio"),
        (CloudCatalogClient, "rest"),
    ],
)
def test_cloud_catalog_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "cloudbilling.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudbilling.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudCatalogGrpcTransport, "grpc"),
        (transports.CloudCatalogGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CloudCatalogRestTransport, "rest"),
    ],
)
def test_cloud_catalog_client_service_account_always_use_jwt(
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
        (CloudCatalogClient, "grpc"),
        (CloudCatalogAsyncClient, "grpc_asyncio"),
        (CloudCatalogClient, "rest"),
    ],
)
def test_cloud_catalog_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == (
            "cloudbilling.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudbilling.googleapis.com"
        )


def test_cloud_catalog_client_get_transport_class():
    transport = CloudCatalogClient.get_transport_class()
    available_transports = [
        transports.CloudCatalogGrpcTransport,
        transports.CloudCatalogRestTransport,
    ]
    assert transport in available_transports

    transport = CloudCatalogClient.get_transport_class("grpc")
    assert transport == transports.CloudCatalogGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudCatalogClient, transports.CloudCatalogGrpcTransport, "grpc"),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudCatalogClient, transports.CloudCatalogRestTransport, "rest"),
    ],
)
@mock.patch.object(
    CloudCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudCatalogClient)
)
@mock.patch.object(
    CloudCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudCatalogAsyncClient),
)
def test_cloud_catalog_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudCatalogClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudCatalogClient, "get_transport_class") as gtc:
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
        (CloudCatalogClient, transports.CloudCatalogGrpcTransport, "grpc", "true"),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudCatalogClient, transports.CloudCatalogGrpcTransport, "grpc", "false"),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (CloudCatalogClient, transports.CloudCatalogRestTransport, "rest", "true"),
        (CloudCatalogClient, transports.CloudCatalogRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    CloudCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudCatalogClient)
)
@mock.patch.object(
    CloudCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudCatalogAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_catalog_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [CloudCatalogClient, CloudCatalogAsyncClient])
@mock.patch.object(
    CloudCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudCatalogClient)
)
@mock.patch.object(
    CloudCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudCatalogAsyncClient),
)
def test_cloud_catalog_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (CloudCatalogClient, transports.CloudCatalogGrpcTransport, "grpc"),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudCatalogClient, transports.CloudCatalogRestTransport, "rest"),
    ],
)
def test_cloud_catalog_client_client_options_scopes(
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
            CloudCatalogClient,
            transports.CloudCatalogGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (CloudCatalogClient, transports.CloudCatalogRestTransport, "rest", None),
    ],
)
def test_cloud_catalog_client_client_options_credentials_file(
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


def test_cloud_catalog_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_catalog.transports.CloudCatalogGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudCatalogClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
            CloudCatalogClient,
            transports.CloudCatalogGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CloudCatalogAsyncClient,
            transports.CloudCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_catalog_client_create_channel_credentials_file(
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
            "cloudbilling.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-billing",
                "https://www.googleapis.com/auth/cloud-billing.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=None,
            default_host="cloudbilling.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_catalog.ListServicesRequest,
        dict,
    ],
)
def test_list_services(request_type, transport: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_catalog.ListServicesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_services_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        client.list_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListServicesRequest()


@pytest.mark.asyncio
async def test_list_services_async(
    transport: str = "grpc_asyncio", request_type=cloud_catalog.ListServicesRequest
):
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_catalog.ListServicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_services_async_from_dict():
    await test_list_services_async(request_type=dict)


def test_list_services_pager(transport_name: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_services(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_catalog.Service) for i in results)


def test_list_services_pages(transport_name: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_services_async_pager():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_services(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_catalog.Service) for i in responses)


@pytest.mark.asyncio
async def test_list_services_async_pages():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_services(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_catalog.ListSkusRequest,
        dict,
    ],
)
def test_list_skus(request_type, transport: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_catalog.ListSkusResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSkusPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_skus_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        client.list_skus()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListSkusRequest()


@pytest.mark.asyncio
async def test_list_skus_async(
    transport: str = "grpc_asyncio", request_type=cloud_catalog.ListSkusRequest
):
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_catalog.ListSkusResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_skus(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_catalog.ListSkusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSkusAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_skus_async_from_dict():
    await test_list_skus_async(request_type=dict)


def test_list_skus_field_headers():
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_catalog.ListSkusRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        call.return_value = cloud_catalog.ListSkusResponse()
        client.list_skus(request)

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
async def test_list_skus_field_headers_async():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_catalog.ListSkusRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_catalog.ListSkusResponse()
        )
        await client.list_skus(request)

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


def test_list_skus_flattened():
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_catalog.ListSkusResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_skus(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_skus_flattened_error():
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_skus(
            cloud_catalog.ListSkusRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_skus_flattened_async():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_catalog.ListSkusResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_catalog.ListSkusResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_skus(
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
async def test_list_skus_flattened_error_async():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_skus(
            cloud_catalog.ListSkusRequest(),
            parent="parent_value",
        )


def test_list_skus_pager(transport_name: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[],
                next_page_token="def",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_skus(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_catalog.Sku) for i in results)


def test_list_skus_pages(transport_name: str = "grpc"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_skus), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[],
                next_page_token="def",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_skus(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_skus_async_pager():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_skus), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[],
                next_page_token="def",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_skus(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_catalog.Sku) for i in responses)


@pytest.mark.asyncio
async def test_list_skus_async_pages():
    client = CloudCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_skus), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[],
                next_page_token="def",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_skus(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_catalog.ListServicesRequest,
        dict,
    ],
)
def test_list_services_rest(request_type):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_catalog.ListServicesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_catalog.ListServicesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_services(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_services_rest_interceptors(null_interceptor):
    transport = transports.CloudCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudCatalogRestInterceptor(),
    )
    client = CloudCatalogClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudCatalogRestInterceptor, "post_list_services"
    ) as post, mock.patch.object(
        transports.CloudCatalogRestInterceptor, "pre_list_services"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_catalog.ListServicesRequest.pb(
            cloud_catalog.ListServicesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloud_catalog.ListServicesResponse.to_json(
            cloud_catalog.ListServicesResponse()
        )

        request = cloud_catalog.ListServicesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_catalog.ListServicesResponse()

        client.list_services(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_services_rest_bad_request(
    transport: str = "rest", request_type=cloud_catalog.ListServicesRequest
):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_services(request)


def test_list_services_rest_pager(transport: str = "rest"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListServicesResponse(
                services=[
                    cloud_catalog.Service(),
                    cloud_catalog.Service(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloud_catalog.ListServicesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {}

        pager = client.list_services(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_catalog.Service) for i in results)

        pages = list(client.list_services(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_catalog.ListSkusRequest,
        dict,
    ],
)
def test_list_skus_rest(request_type):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "services/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_catalog.ListSkusResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_catalog.ListSkusResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_skus(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSkusPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_skus_rest_required_fields(request_type=cloud_catalog.ListSkusRequest):
    transport_class = transports.CloudCatalogRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_skus._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_skus._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "currency_code",
            "end_time",
            "page_size",
            "page_token",
            "start_time",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_catalog.ListSkusResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = cloud_catalog.ListSkusResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_skus(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_skus_rest_unset_required_fields():
    transport = transports.CloudCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_skus._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "currencyCode",
                "endTime",
                "pageSize",
                "pageToken",
                "startTime",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_skus_rest_interceptors(null_interceptor):
    transport = transports.CloudCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudCatalogRestInterceptor(),
    )
    client = CloudCatalogClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudCatalogRestInterceptor, "post_list_skus"
    ) as post, mock.patch.object(
        transports.CloudCatalogRestInterceptor, "pre_list_skus"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_catalog.ListSkusRequest.pb(cloud_catalog.ListSkusRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloud_catalog.ListSkusResponse.to_json(
            cloud_catalog.ListSkusResponse()
        )

        request = cloud_catalog.ListSkusRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_catalog.ListSkusResponse()

        client.list_skus(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_skus_rest_bad_request(
    transport: str = "rest", request_type=cloud_catalog.ListSkusRequest
):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "services/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_skus(request)


def test_list_skus_rest_flattened():
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_catalog.ListSkusResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "services/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_catalog.ListSkusResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_skus(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=services/*}/skus" % client.transport._host, args[1]
        )


def test_list_skus_rest_flattened_error(transport: str = "rest"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_skus(
            cloud_catalog.ListSkusRequest(),
            parent="parent_value",
        )


def test_list_skus_rest_pager(transport: str = "rest"):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
                next_page_token="abc",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[],
                next_page_token="def",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                ],
                next_page_token="ghi",
            ),
            cloud_catalog.ListSkusResponse(
                skus=[
                    cloud_catalog.Sku(),
                    cloud_catalog.Sku(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(cloud_catalog.ListSkusResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "services/sample1"}

        pager = client.list_skus(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_catalog.Sku) for i in results)

        pages = list(client.list_skus(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudCatalogClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudCatalogClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudCatalogClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudCatalogClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudCatalogClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudCatalogGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudCatalogGrpcTransport,
        transports.CloudCatalogGrpcAsyncIOTransport,
        transports.CloudCatalogRestTransport,
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
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = CloudCatalogClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudCatalogGrpcTransport,
    )


def test_cloud_catalog_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_catalog_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_catalog.transports.CloudCatalogTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_services",
        "list_skus",
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


def test_cloud_catalog_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.billing_v1.services.cloud_catalog.transports.CloudCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudCatalogTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-billing",
                "https://www.googleapis.com/auth/cloud-billing.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_cloud_catalog_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.billing_v1.services.cloud_catalog.transports.CloudCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudCatalogTransport()
        adc.assert_called_once()


def test_cloud_catalog_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudCatalogClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-billing",
                "https://www.googleapis.com/auth/cloud-billing.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudCatalogGrpcTransport,
        transports.CloudCatalogGrpcAsyncIOTransport,
    ],
)
def test_cloud_catalog_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-billing",
                "https://www.googleapis.com/auth/cloud-billing.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudCatalogGrpcTransport,
        transports.CloudCatalogGrpcAsyncIOTransport,
        transports.CloudCatalogRestTransport,
    ],
)
def test_cloud_catalog_transport_auth_gdch_credentials(transport_class):
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
        (transports.CloudCatalogGrpcTransport, grpc_helpers),
        (transports.CloudCatalogGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_catalog_transport_create_channel(transport_class, grpc_helpers):
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
            "cloudbilling.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-billing",
                "https://www.googleapis.com/auth/cloud-billing.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=["1", "2"],
            default_host="cloudbilling.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudCatalogGrpcTransport, transports.CloudCatalogGrpcAsyncIOTransport],
)
def test_cloud_catalog_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_cloud_catalog_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CloudCatalogRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_catalog_host_no_port(transport_name):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudbilling.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudbilling.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_catalog_host_with_port(transport_name):
    client = CloudCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudbilling.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudbilling.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_cloud_catalog_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = CloudCatalogClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CloudCatalogClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_services._session
    session2 = client2.transport.list_services._session
    assert session1 != session2
    session1 = client1.transport.list_skus._session
    session2 = client2.transport.list_skus._session
    assert session1 != session2


def test_cloud_catalog_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudCatalogGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_catalog_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudCatalogGrpcAsyncIOTransport(
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
    [transports.CloudCatalogGrpcTransport, transports.CloudCatalogGrpcAsyncIOTransport],
)
def test_cloud_catalog_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.CloudCatalogGrpcTransport, transports.CloudCatalogGrpcAsyncIOTransport],
)
def test_cloud_catalog_transport_channel_mtls_with_adc(transport_class):
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


def test_service_path():
    service = "squid"
    expected = "services/{service}".format(
        service=service,
    )
    actual = CloudCatalogClient.service_path(service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "service": "clam",
    }
    path = CloudCatalogClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_service_path(path)
    assert expected == actual


def test_sku_path():
    service = "whelk"
    sku = "octopus"
    expected = "services/{service}/skus/{sku}".format(
        service=service,
        sku=sku,
    )
    actual = CloudCatalogClient.sku_path(service, sku)
    assert expected == actual


def test_parse_sku_path():
    expected = {
        "service": "oyster",
        "sku": "nudibranch",
    }
    path = CloudCatalogClient.sku_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_sku_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudCatalogClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = CloudCatalogClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudCatalogClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = CloudCatalogClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudCatalogClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = CloudCatalogClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudCatalogClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = CloudCatalogClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudCatalogClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = CloudCatalogClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudCatalogClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudCatalogClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudCatalogAsyncClient(
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
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CloudCatalogClient(
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
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = CloudCatalogClient(
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
        (CloudCatalogClient, transports.CloudCatalogGrpcTransport),
        (CloudCatalogAsyncClient, transports.CloudCatalogGrpcAsyncIOTransport),
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
