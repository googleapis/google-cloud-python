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

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.datastream_v1alpha1.services.datastream import (
    DatastreamAsyncClient,
    DatastreamClient,
    pagers,
    transports,
)
from google.cloud.datastream_v1alpha1.types import datastream, datastream_resources


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

    assert DatastreamClient._get_default_mtls_endpoint(None) is None
    assert (
        DatastreamClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        DatastreamClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DatastreamClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DatastreamClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DatastreamClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DatastreamClient, "grpc"),
        (DatastreamAsyncClient, "grpc_asyncio"),
        (DatastreamClient, "rest"),
    ],
)
def test_datastream_client_from_service_account_info(client_class, transport_name):
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
            "datastream.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://datastream.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DatastreamGrpcTransport, "grpc"),
        (transports.DatastreamGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DatastreamRestTransport, "rest"),
    ],
)
def test_datastream_client_service_account_always_use_jwt(
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
        (DatastreamClient, "grpc"),
        (DatastreamAsyncClient, "grpc_asyncio"),
        (DatastreamClient, "rest"),
    ],
)
def test_datastream_client_from_service_account_file(client_class, transport_name):
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
            "datastream.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://datastream.googleapis.com"
        )


def test_datastream_client_get_transport_class():
    transport = DatastreamClient.get_transport_class()
    available_transports = [
        transports.DatastreamGrpcTransport,
        transports.DatastreamRestTransport,
    ]
    assert transport in available_transports

    transport = DatastreamClient.get_transport_class("grpc")
    assert transport == transports.DatastreamGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc"),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DatastreamClient, transports.DatastreamRestTransport, "rest"),
    ],
)
@mock.patch.object(
    DatastreamClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DatastreamClient)
)
@mock.patch.object(
    DatastreamAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DatastreamAsyncClient),
)
def test_datastream_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DatastreamClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DatastreamClient, "get_transport_class") as gtc:
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
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc", "true"),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc", "false"),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (DatastreamClient, transports.DatastreamRestTransport, "rest", "true"),
        (DatastreamClient, transports.DatastreamRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    DatastreamClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DatastreamClient)
)
@mock.patch.object(
    DatastreamAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DatastreamAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_datastream_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [DatastreamClient, DatastreamAsyncClient])
@mock.patch.object(
    DatastreamClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DatastreamClient)
)
@mock.patch.object(
    DatastreamAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DatastreamAsyncClient),
)
def test_datastream_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc"),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DatastreamClient, transports.DatastreamRestTransport, "rest"),
    ],
)
def test_datastream_client_client_options_scopes(
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
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc", grpc_helpers),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (DatastreamClient, transports.DatastreamRestTransport, "rest", None),
    ],
)
def test_datastream_client_client_options_credentials_file(
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


def test_datastream_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datastream_v1alpha1.services.datastream.transports.DatastreamGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DatastreamClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (DatastreamClient, transports.DatastreamGrpcTransport, "grpc", grpc_helpers),
        (
            DatastreamAsyncClient,
            transports.DatastreamGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_datastream_client_create_channel_credentials_file(
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
            "datastream.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="datastream.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListConnectionProfilesRequest,
        dict,
    ],
)
def test_list_connection_profiles(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListConnectionProfilesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListConnectionProfilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionProfilesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_connection_profiles_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        client.list_connection_profiles()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListConnectionProfilesRequest()


@pytest.mark.asyncio
async def test_list_connection_profiles_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.ListConnectionProfilesRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListConnectionProfilesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListConnectionProfilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionProfilesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_connection_profiles_async_from_dict():
    await test_list_connection_profiles_async(request_type=dict)


def test_list_connection_profiles_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListConnectionProfilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        call.return_value = datastream.ListConnectionProfilesResponse()
        client.list_connection_profiles(request)

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
async def test_list_connection_profiles_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListConnectionProfilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListConnectionProfilesResponse()
        )
        await client.list_connection_profiles(request)

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


def test_list_connection_profiles_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListConnectionProfilesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_connection_profiles(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_connection_profiles_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_connection_profiles(
            datastream.ListConnectionProfilesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_connection_profiles_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListConnectionProfilesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListConnectionProfilesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_connection_profiles(
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
async def test_list_connection_profiles_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_connection_profiles(
            datastream.ListConnectionProfilesRequest(),
            parent="parent_value",
        )


def test_list_connection_profiles_pager(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_connection_profiles(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, datastream_resources.ConnectionProfile) for i in results
        )


def test_list_connection_profiles_pages(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_connection_profiles(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_connection_profiles_async_pager():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_connection_profiles(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, datastream_resources.ConnectionProfile) for i in responses
        )


@pytest.mark.asyncio
async def test_list_connection_profiles_async_pages():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_connection_profiles(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetConnectionProfileRequest,
        dict,
    ],
)
def test_get_connection_profile(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.ConnectionProfile(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.ConnectionProfile)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        client.get_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetConnectionProfileRequest()


@pytest.mark.asyncio
async def test_get_connection_profile_async(
    transport: str = "grpc_asyncio", request_type=datastream.GetConnectionProfileRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.ConnectionProfile(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.ConnectionProfile)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_connection_profile_async_from_dict():
    await test_get_connection_profile_async(request_type=dict)


def test_get_connection_profile_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        call.return_value = datastream_resources.ConnectionProfile()
        client.get_connection_profile(request)

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
async def test_get_connection_profile_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.ConnectionProfile()
        )
        await client.get_connection_profile(request)

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


def test_get_connection_profile_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.ConnectionProfile()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_connection_profile(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_connection_profile_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connection_profile(
            datastream.GetConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_connection_profile_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.ConnectionProfile()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.ConnectionProfile()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_connection_profile(
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
async def test_get_connection_profile_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_connection_profile(
            datastream.GetConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateConnectionProfileRequest,
        dict,
    ],
)
def test_create_connection_profile(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        client.create_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateConnectionProfileRequest()


@pytest.mark.asyncio
async def test_create_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.CreateConnectionProfileRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_connection_profile_async_from_dict():
    await test_create_connection_profile_async(request_type=dict)


def test_create_connection_profile_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_connection_profile(request)

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
async def test_create_connection_profile_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_connection_profile(request)

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


def test_create_connection_profile_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_connection_profile(
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].connection_profile
        mock_val = datastream_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].connection_profile_id
        mock_val = "connection_profile_id_value"
        assert arg == mock_val


def test_create_connection_profile_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connection_profile(
            datastream.CreateConnectionProfileRequest(),
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )


@pytest.mark.asyncio
async def test_create_connection_profile_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_connection_profile(
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].connection_profile
        mock_val = datastream_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].connection_profile_id
        mock_val = "connection_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_connection_profile_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_connection_profile(
            datastream.CreateConnectionProfileRequest(),
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.UpdateConnectionProfileRequest,
        dict,
    ],
)
def test_update_connection_profile(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        client.update_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateConnectionProfileRequest()


@pytest.mark.asyncio
async def test_update_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.UpdateConnectionProfileRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_connection_profile_async_from_dict():
    await test_update_connection_profile_async(request_type=dict)


def test_update_connection_profile_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.UpdateConnectionProfileRequest()

    request.connection_profile.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "connection_profile.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_connection_profile_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.UpdateConnectionProfileRequest()

    request.connection_profile.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "connection_profile.name=name_value",
    ) in kw["metadata"]


def test_update_connection_profile_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_connection_profile(
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].connection_profile
        mock_val = datastream_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_connection_profile_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connection_profile(
            datastream.UpdateConnectionProfileRequest(),
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_connection_profile_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_connection_profile(
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].connection_profile
        mock_val = datastream_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_connection_profile_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_connection_profile(
            datastream.UpdateConnectionProfileRequest(),
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteConnectionProfileRequest,
        dict,
    ],
)
def test_delete_connection_profile(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        client.delete_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteConnectionProfileRequest()


@pytest.mark.asyncio
async def test_delete_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.DeleteConnectionProfileRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_connection_profile_async_from_dict():
    await test_delete_connection_profile_async(request_type=dict)


def test_delete_connection_profile_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_connection_profile(request)

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
async def test_delete_connection_profile_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_connection_profile(request)

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


def test_delete_connection_profile_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_connection_profile(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_connection_profile_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connection_profile(
            datastream.DeleteConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_connection_profile_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_connection_profile(
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
async def test_delete_connection_profile_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_connection_profile(
            datastream.DeleteConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DiscoverConnectionProfileRequest,
        dict,
    ],
)
def test_discover_connection_profile(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discover_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.DiscoverConnectionProfileResponse()
        response = client.discover_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DiscoverConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream.DiscoverConnectionProfileResponse)


def test_discover_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discover_connection_profile), "__call__"
    ) as call:
        client.discover_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DiscoverConnectionProfileRequest()


@pytest.mark.asyncio
async def test_discover_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.DiscoverConnectionProfileRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discover_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.DiscoverConnectionProfileResponse()
        )
        response = await client.discover_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DiscoverConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream.DiscoverConnectionProfileResponse)


@pytest.mark.asyncio
async def test_discover_connection_profile_async_from_dict():
    await test_discover_connection_profile_async(request_type=dict)


def test_discover_connection_profile_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DiscoverConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discover_connection_profile), "__call__"
    ) as call:
        call.return_value = datastream.DiscoverConnectionProfileResponse()
        client.discover_connection_profile(request)

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
async def test_discover_connection_profile_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DiscoverConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discover_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.DiscoverConnectionProfileResponse()
        )
        await client.discover_connection_profile(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListStreamsRequest,
        dict,
    ],
)
def test_list_streams(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListStreamsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListStreamsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_streams_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        client.list_streams()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListStreamsRequest()


@pytest.mark.asyncio
async def test_list_streams_async(
    transport: str = "grpc_asyncio", request_type=datastream.ListStreamsRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListStreamsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListStreamsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_streams_async_from_dict():
    await test_list_streams_async(request_type=dict)


def test_list_streams_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListStreamsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        call.return_value = datastream.ListStreamsResponse()
        client.list_streams(request)

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
async def test_list_streams_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListStreamsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListStreamsResponse()
        )
        await client.list_streams(request)

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


def test_list_streams_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListStreamsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_streams(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_streams_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_streams(
            datastream.ListStreamsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_streams_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_streams(
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
async def test_list_streams_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_streams(
            datastream.ListStreamsRequest(),
            parent="parent_value",
        )


def test_list_streams_pager(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
                next_page_token="abc",
            ),
            datastream.ListStreamsResponse(
                streams=[],
                next_page_token="def",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_streams(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datastream_resources.Stream) for i in results)


def test_list_streams_pages(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_streams), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
                next_page_token="abc",
            ),
            datastream.ListStreamsResponse(
                streams=[],
                next_page_token="def",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_streams(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_streams_async_pager():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_streams), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
                next_page_token="abc",
            ),
            datastream.ListStreamsResponse(
                streams=[],
                next_page_token="def",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_streams(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datastream_resources.Stream) for i in responses)


@pytest.mark.asyncio
async def test_list_streams_async_pages():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_streams), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
                next_page_token="abc",
            ),
            datastream.ListStreamsResponse(
                streams=[],
                next_page_token="def",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_streams(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetStreamRequest,
        dict,
    ],
)
def test_get_stream(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Stream(
            name="name_value",
            display_name="display_name_value",
            state=datastream_resources.Stream.State.CREATED,
        )
        response = client.get_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Stream)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.Stream.State.CREATED


def test_get_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        client.get_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetStreamRequest()


@pytest.mark.asyncio
async def test_get_stream_async(
    transport: str = "grpc_asyncio", request_type=datastream.GetStreamRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Stream(
                name="name_value",
                display_name="display_name_value",
                state=datastream_resources.Stream.State.CREATED,
            )
        )
        response = await client.get_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Stream)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.Stream.State.CREATED


@pytest.mark.asyncio
async def test_get_stream_async_from_dict():
    await test_get_stream_async(request_type=dict)


def test_get_stream_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        call.return_value = datastream_resources.Stream()
        client.get_stream(request)

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
async def test_get_stream_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Stream()
        )
        await client.get_stream(request)

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


def test_get_stream_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Stream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_stream(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_stream_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_stream(
            datastream.GetStreamRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_stream_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Stream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Stream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_stream(
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
async def test_get_stream_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_stream(
            datastream.GetStreamRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateStreamRequest,
        dict,
    ],
)
def test_create_stream(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        client.create_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateStreamRequest()


@pytest.mark.asyncio
async def test_create_stream_async(
    transport: str = "grpc_asyncio", request_type=datastream.CreateStreamRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_stream_async_from_dict():
    await test_create_stream_async(request_type=dict)


def test_create_stream_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateStreamRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_stream(request)

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
async def test_create_stream_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateStreamRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_stream(request)

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


def test_create_stream_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_stream(
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].stream
        mock_val = datastream_resources.Stream(name="name_value")
        assert arg == mock_val
        arg = args[0].stream_id
        mock_val = "stream_id_value"
        assert arg == mock_val


def test_create_stream_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_stream(
            datastream.CreateStreamRequest(),
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )


@pytest.mark.asyncio
async def test_create_stream_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_stream(
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].stream
        mock_val = datastream_resources.Stream(name="name_value")
        assert arg == mock_val
        arg = args[0].stream_id
        mock_val = "stream_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_stream_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_stream(
            datastream.CreateStreamRequest(),
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.UpdateStreamRequest,
        dict,
    ],
)
def test_update_stream(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        client.update_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateStreamRequest()


@pytest.mark.asyncio
async def test_update_stream_async(
    transport: str = "grpc_asyncio", request_type=datastream.UpdateStreamRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.UpdateStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_stream_async_from_dict():
    await test_update_stream_async(request_type=dict)


def test_update_stream_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.UpdateStreamRequest()

    request.stream.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "stream.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_stream_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.UpdateStreamRequest()

    request.stream.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "stream.name=name_value",
    ) in kw["metadata"]


def test_update_stream_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_stream(
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].stream
        mock_val = datastream_resources.Stream(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_stream_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_stream(
            datastream.UpdateStreamRequest(),
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_stream_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_stream(
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].stream
        mock_val = datastream_resources.Stream(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_stream_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_stream(
            datastream.UpdateStreamRequest(),
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteStreamRequest,
        dict,
    ],
)
def test_delete_stream(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        client.delete_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteStreamRequest()


@pytest.mark.asyncio
async def test_delete_stream_async(
    transport: str = "grpc_asyncio", request_type=datastream.DeleteStreamRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_stream_async_from_dict():
    await test_delete_stream_async(request_type=dict)


def test_delete_stream_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_stream(request)

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
async def test_delete_stream_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteStreamRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_stream(request)

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


def test_delete_stream_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_stream(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_stream_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_stream(
            datastream.DeleteStreamRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_stream_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_stream(
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
async def test_delete_stream_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_stream(
            datastream.DeleteStreamRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.FetchErrorsRequest,
        dict,
    ],
)
def test_fetch_errors(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_errors), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.fetch_errors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchErrorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_fetch_errors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_errors), "__call__") as call:
        client.fetch_errors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchErrorsRequest()


@pytest.mark.asyncio
async def test_fetch_errors_async(
    transport: str = "grpc_asyncio", request_type=datastream.FetchErrorsRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_errors), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.fetch_errors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchErrorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_fetch_errors_async_from_dict():
    await test_fetch_errors_async(request_type=dict)


def test_fetch_errors_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.FetchErrorsRequest()

    request.stream = "stream_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_errors), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.fetch_errors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "stream=stream_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_errors_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.FetchErrorsRequest()

    request.stream = "stream_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_errors), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.fetch_errors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "stream=stream_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.FetchStaticIpsRequest,
        dict,
    ],
)
def test_fetch_static_ips(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.FetchStaticIpsResponse(
            static_ips=["static_ips_value"],
            next_page_token="next_page_token_value",
        )
        response = client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchStaticIpsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.FetchStaticIpsPager)
    assert response.static_ips == ["static_ips_value"]
    assert response.next_page_token == "next_page_token_value"


def test_fetch_static_ips_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        client.fetch_static_ips()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchStaticIpsRequest()


@pytest.mark.asyncio
async def test_fetch_static_ips_async(
    transport: str = "grpc_asyncio", request_type=datastream.FetchStaticIpsRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.FetchStaticIpsResponse(
                static_ips=["static_ips_value"],
                next_page_token="next_page_token_value",
            )
        )
        response = await client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.FetchStaticIpsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.FetchStaticIpsAsyncPager)
    assert response.static_ips == ["static_ips_value"]
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_fetch_static_ips_async_from_dict():
    await test_fetch_static_ips_async(request_type=dict)


def test_fetch_static_ips_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.FetchStaticIpsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        call.return_value = datastream.FetchStaticIpsResponse()
        client.fetch_static_ips(request)

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
async def test_fetch_static_ips_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.FetchStaticIpsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.FetchStaticIpsResponse()
        )
        await client.fetch_static_ips(request)

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


def test_fetch_static_ips_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.FetchStaticIpsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.fetch_static_ips(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_fetch_static_ips_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_static_ips(
            datastream.FetchStaticIpsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_fetch_static_ips_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.FetchStaticIpsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.FetchStaticIpsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.fetch_static_ips(
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
async def test_fetch_static_ips_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.fetch_static_ips(
            datastream.FetchStaticIpsRequest(),
            name="name_value",
        )


def test_fetch_static_ips_pager(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.fetch_static_ips(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_fetch_static_ips_pages(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.fetch_static_ips(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_fetch_static_ips_async_pager():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_static_ips), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.fetch_static_ips(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_fetch_static_ips_async_pages():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_static_ips), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.fetch_static_ips(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreatePrivateConnectionRequest,
        dict,
    ],
)
def test_create_private_connection(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreatePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        client.create_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreatePrivateConnectionRequest()


@pytest.mark.asyncio
async def test_create_private_connection_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.CreatePrivateConnectionRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreatePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_private_connection_async_from_dict():
    await test_create_private_connection_async(request_type=dict)


def test_create_private_connection_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreatePrivateConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_private_connection(request)

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
async def test_create_private_connection_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreatePrivateConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_private_connection(request)

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


def test_create_private_connection_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_private_connection(
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].private_connection
        mock_val = datastream_resources.PrivateConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].private_connection_id
        mock_val = "private_connection_id_value"
        assert arg == mock_val


def test_create_private_connection_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_private_connection(
            datastream.CreatePrivateConnectionRequest(),
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )


@pytest.mark.asyncio
async def test_create_private_connection_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_private_connection(
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].private_connection
        mock_val = datastream_resources.PrivateConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].private_connection_id
        mock_val = "private_connection_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_private_connection_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_private_connection(
            datastream.CreatePrivateConnectionRequest(),
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetPrivateConnectionRequest,
        dict,
    ],
)
def test_get_private_connection(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.PrivateConnection(
            name="name_value",
            display_name="display_name_value",
            state=datastream_resources.PrivateConnection.State.CREATING,
        )
        response = client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetPrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.PrivateConnection)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.PrivateConnection.State.CREATING


def test_get_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        client.get_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetPrivateConnectionRequest()


@pytest.mark.asyncio
async def test_get_private_connection_async(
    transport: str = "grpc_asyncio", request_type=datastream.GetPrivateConnectionRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.PrivateConnection(
                name="name_value",
                display_name="display_name_value",
                state=datastream_resources.PrivateConnection.State.CREATING,
            )
        )
        response = await client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetPrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.PrivateConnection)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.PrivateConnection.State.CREATING


@pytest.mark.asyncio
async def test_get_private_connection_async_from_dict():
    await test_get_private_connection_async(request_type=dict)


def test_get_private_connection_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetPrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        call.return_value = datastream_resources.PrivateConnection()
        client.get_private_connection(request)

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
async def test_get_private_connection_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetPrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.PrivateConnection()
        )
        await client.get_private_connection(request)

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


def test_get_private_connection_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.PrivateConnection()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_private_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_private_connection_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_private_connection(
            datastream.GetPrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_private_connection_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.PrivateConnection()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.PrivateConnection()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_private_connection(
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
async def test_get_private_connection_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_private_connection(
            datastream.GetPrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListPrivateConnectionsRequest,
        dict,
    ],
)
def test_list_private_connections(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListPrivateConnectionsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListPrivateConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateConnectionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_private_connections_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        client.list_private_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListPrivateConnectionsRequest()


@pytest.mark.asyncio
async def test_list_private_connections_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.ListPrivateConnectionsRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListPrivateConnectionsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListPrivateConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateConnectionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_private_connections_async_from_dict():
    await test_list_private_connections_async(request_type=dict)


def test_list_private_connections_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListPrivateConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        call.return_value = datastream.ListPrivateConnectionsResponse()
        client.list_private_connections(request)

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
async def test_list_private_connections_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListPrivateConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListPrivateConnectionsResponse()
        )
        await client.list_private_connections(request)

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


def test_list_private_connections_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListPrivateConnectionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_private_connections(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_private_connections_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_private_connections(
            datastream.ListPrivateConnectionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_private_connections_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListPrivateConnectionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListPrivateConnectionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_private_connections(
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
async def test_list_private_connections_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_private_connections(
            datastream.ListPrivateConnectionsRequest(),
            parent="parent_value",
        )


def test_list_private_connections_pager(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_private_connections(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, datastream_resources.PrivateConnection) for i in results
        )


def test_list_private_connections_pages(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_private_connections(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_private_connections_async_pager():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_private_connections(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, datastream_resources.PrivateConnection) for i in responses
        )


@pytest.mark.asyncio
async def test_list_private_connections_async_pages():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_private_connections(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeletePrivateConnectionRequest,
        dict,
    ],
)
def test_delete_private_connection(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeletePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        client.delete_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeletePrivateConnectionRequest()


@pytest.mark.asyncio
async def test_delete_private_connection_async(
    transport: str = "grpc_asyncio",
    request_type=datastream.DeletePrivateConnectionRequest,
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeletePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_private_connection_async_from_dict():
    await test_delete_private_connection_async(request_type=dict)


def test_delete_private_connection_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeletePrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_private_connection(request)

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
async def test_delete_private_connection_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeletePrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_private_connection(request)

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


def test_delete_private_connection_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_private_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_private_connection_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_private_connection(
            datastream.DeletePrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_private_connection_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_private_connection(
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
async def test_delete_private_connection_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_private_connection(
            datastream.DeletePrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateRouteRequest,
        dict,
    ],
)
def test_create_route(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        client.create_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateRouteRequest()


@pytest.mark.asyncio
async def test_create_route_async(
    transport: str = "grpc_asyncio", request_type=datastream.CreateRouteRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.CreateRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_route_async_from_dict():
    await test_create_route_async(request_type=dict)


def test_create_route_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_route(request)

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
async def test_create_route_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.CreateRouteRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_route(request)

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


def test_create_route_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_route(
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].route
        mock_val = datastream_resources.Route(name="name_value")
        assert arg == mock_val
        arg = args[0].route_id
        mock_val = "route_id_value"
        assert arg == mock_val


def test_create_route_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_route(
            datastream.CreateRouteRequest(),
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )


@pytest.mark.asyncio
async def test_create_route_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_route(
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].route
        mock_val = datastream_resources.Route(name="name_value")
        assert arg == mock_val
        arg = args[0].route_id
        mock_val = "route_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_route_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_route(
            datastream.CreateRouteRequest(),
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetRouteRequest,
        dict,
    ],
)
def test_get_route(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Route(
            name="name_value",
            display_name="display_name_value",
            destination_address="destination_address_value",
            destination_port=1734,
        )
        response = client.get_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Route)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.destination_address == "destination_address_value"
    assert response.destination_port == 1734


def test_get_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        client.get_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetRouteRequest()


@pytest.mark.asyncio
async def test_get_route_async(
    transport: str = "grpc_asyncio", request_type=datastream.GetRouteRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Route(
                name="name_value",
                display_name="display_name_value",
                destination_address="destination_address_value",
                destination_port=1734,
            )
        )
        response = await client.get_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.GetRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Route)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.destination_address == "destination_address_value"
    assert response.destination_port == 1734


@pytest.mark.asyncio
async def test_get_route_async_from_dict():
    await test_get_route_async(request_type=dict)


def test_get_route_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        call.return_value = datastream_resources.Route()
        client.get_route(request)

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
async def test_get_route_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.GetRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Route()
        )
        await client.get_route(request)

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


def test_get_route_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Route()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_route_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_route(
            datastream.GetRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_route_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream_resources.Route()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream_resources.Route()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_route(
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
async def test_get_route_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_route(
            datastream.GetRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListRoutesRequest,
        dict,
    ],
)
def test_list_routes(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListRoutesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRoutesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_routes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        client.list_routes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListRoutesRequest()


@pytest.mark.asyncio
async def test_list_routes_async(
    transport: str = "grpc_asyncio", request_type=datastream.ListRoutesRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListRoutesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_routes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.ListRoutesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRoutesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_routes_async_from_dict():
    await test_list_routes_async(request_type=dict)


def test_list_routes_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        call.return_value = datastream.ListRoutesResponse()
        client.list_routes(request)

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
async def test_list_routes_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.ListRoutesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListRoutesResponse()
        )
        await client.list_routes(request)

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


def test_list_routes_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListRoutesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_routes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_routes_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_routes(
            datastream.ListRoutesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_routes_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datastream.ListRoutesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datastream.ListRoutesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_routes(
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
async def test_list_routes_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_routes(
            datastream.ListRoutesRequest(),
            parent="parent_value",
        )


def test_list_routes_pager(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
                next_page_token="abc",
            ),
            datastream.ListRoutesResponse(
                routes=[],
                next_page_token="def",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_routes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datastream_resources.Route) for i in results)


def test_list_routes_pages(transport_name: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_routes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
                next_page_token="abc",
            ),
            datastream.ListRoutesResponse(
                routes=[],
                next_page_token="def",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_routes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_routes_async_pager():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
                next_page_token="abc",
            ),
            datastream.ListRoutesResponse(
                routes=[],
                next_page_token="def",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_routes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datastream_resources.Route) for i in responses)


@pytest.mark.asyncio
async def test_list_routes_async_pages():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_routes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
                next_page_token="abc",
            ),
            datastream.ListRoutesResponse(
                routes=[],
                next_page_token="def",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_routes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteRouteRequest,
        dict,
    ],
)
def test_delete_route(request_type, transport: str = "grpc"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_route_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        client.delete_route()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteRouteRequest()


@pytest.mark.asyncio
async def test_delete_route_async(
    transport: str = "grpc_asyncio", request_type=datastream.DeleteRouteRequest
):
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_route(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datastream.DeleteRouteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_route_async_from_dict():
    await test_delete_route_async(request_type=dict)


def test_delete_route_field_headers():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_route(request)

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
async def test_delete_route_field_headers_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datastream.DeleteRouteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_route(request)

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


def test_delete_route_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_route(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_route_flattened_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_route(
            datastream.DeleteRouteRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_route_flattened_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_route), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_route(
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
async def test_delete_route_flattened_error_async():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_route(
            datastream.DeleteRouteRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListConnectionProfilesRequest,
        dict,
    ],
)
def test_list_connection_profiles_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListConnectionProfilesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListConnectionProfilesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_connection_profiles(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionProfilesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_connection_profiles_rest_required_fields(
    request_type=datastream.ListConnectionProfilesRequest,
):
    transport_class = transports.DatastreamRestTransport

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
    ).list_connection_profiles._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_connection_profiles._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.ListConnectionProfilesResponse()
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

            pb_return_value = datastream.ListConnectionProfilesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_connection_profiles(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_connection_profiles_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_connection_profiles._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_connection_profiles_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_list_connection_profiles"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_list_connection_profiles"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.ListConnectionProfilesRequest.pb(
            datastream.ListConnectionProfilesRequest()
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
        req.return_value._content = datastream.ListConnectionProfilesResponse.to_json(
            datastream.ListConnectionProfilesResponse()
        )

        request = datastream.ListConnectionProfilesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.ListConnectionProfilesResponse()

        client.list_connection_profiles(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_connection_profiles_rest_bad_request(
    transport: str = "rest", request_type=datastream.ListConnectionProfilesRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_connection_profiles(request)


def test_list_connection_profiles_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListConnectionProfilesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListConnectionProfilesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_connection_profiles(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/connectionProfiles"
            % client.transport._host,
            args[1],
        )


def test_list_connection_profiles_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_connection_profiles(
            datastream.ListConnectionProfilesRequest(),
            parent="parent_value",
        )


def test_list_connection_profiles_rest_pager(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListConnectionProfilesResponse(
                connection_profiles=[
                    datastream_resources.ConnectionProfile(),
                    datastream_resources.ConnectionProfile(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            datastream.ListConnectionProfilesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_connection_profiles(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, datastream_resources.ConnectionProfile) for i in results
        )

        pages = list(client.list_connection_profiles(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetConnectionProfileRequest,
        dict,
    ],
)
def test_get_connection_profile_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.ConnectionProfile(
            name="name_value",
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.ConnectionProfile.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_connection_profile(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.ConnectionProfile)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_connection_profile_rest_required_fields(
    request_type=datastream.GetConnectionProfileRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).get_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream_resources.ConnectionProfile()
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

            pb_return_value = datastream_resources.ConnectionProfile.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_connection_profile(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_connection_profile_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_connection_profile._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_connection_profile_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_get_connection_profile"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_get_connection_profile"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.GetConnectionProfileRequest.pb(
            datastream.GetConnectionProfileRequest()
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
        req.return_value._content = datastream_resources.ConnectionProfile.to_json(
            datastream_resources.ConnectionProfile()
        )

        request = datastream.GetConnectionProfileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream_resources.ConnectionProfile()

        client.get_connection_profile(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_connection_profile_rest_bad_request(
    transport: str = "rest", request_type=datastream.GetConnectionProfileRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
    }
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
        client.get_connection_profile(request)


def test_get_connection_profile_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.ConnectionProfile()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.ConnectionProfile.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_connection_profile(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/connectionProfiles/*}"
            % client.transport._host,
            args[1],
        )


def test_get_connection_profile_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connection_profile(
            datastream.GetConnectionProfileRequest(),
            name="name_value",
        )


def test_get_connection_profile_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateConnectionProfileRequest,
        dict,
    ],
)
def test_create_connection_profile_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["connection_profile"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "oracle_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "database_service": "database_service_value",
            "connection_attributes": {},
        },
        "gcs_profile": {
            "bucket_name": "bucket_name_value",
            "root_path": "root_path_value",
        },
        "mysql_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "ssl_config": {
                "client_key": "client_key_value",
                "client_key_set": True,
                "client_certificate": "client_certificate_value",
                "client_certificate_set": True,
                "ca_certificate": "ca_certificate_value",
                "ca_certificate_set": True,
            },
        },
        "no_connectivity": {},
        "static_service_ip_connectivity": {},
        "forward_ssh_connectivity": {
            "hostname": "hostname_value",
            "username": "username_value",
            "port": 453,
            "password": "password_value",
            "private_key": "private_key_value",
        },
        "private_connectivity": {
            "private_connection_name": "private_connection_name_value"
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_connection_profile(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_connection_profile_rest_required_fields(
    request_type=datastream.CreateConnectionProfileRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["connection_profile_id"] = ""
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
    assert "connectionProfileId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "connectionProfileId" in jsonified_request
    assert (
        jsonified_request["connectionProfileId"]
        == request_init["connection_profile_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["connectionProfileId"] = "connection_profile_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_connection_profile._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "connection_profile_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "connectionProfileId" in jsonified_request
    assert jsonified_request["connectionProfileId"] == "connection_profile_id_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_connection_profile(request)

            expected_params = [
                (
                    "connectionProfileId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_connection_profile_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_connection_profile._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "connectionProfileId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "connectionProfileId",
                "connectionProfile",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_connection_profile_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_create_connection_profile"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_create_connection_profile"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.CreateConnectionProfileRequest.pb(
            datastream.CreateConnectionProfileRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.CreateConnectionProfileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_connection_profile(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_connection_profile_rest_bad_request(
    transport: str = "rest", request_type=datastream.CreateConnectionProfileRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["connection_profile"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "oracle_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "database_service": "database_service_value",
            "connection_attributes": {},
        },
        "gcs_profile": {
            "bucket_name": "bucket_name_value",
            "root_path": "root_path_value",
        },
        "mysql_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "ssl_config": {
                "client_key": "client_key_value",
                "client_key_set": True,
                "client_certificate": "client_certificate_value",
                "client_certificate_set": True,
                "ca_certificate": "ca_certificate_value",
                "ca_certificate_set": True,
            },
        },
        "no_connectivity": {},
        "static_service_ip_connectivity": {},
        "forward_ssh_connectivity": {
            "hostname": "hostname_value",
            "username": "username_value",
            "port": 453,
            "password": "password_value",
            "private_key": "private_key_value",
        },
        "private_connectivity": {
            "private_connection_name": "private_connection_name_value"
        },
    }
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
        client.create_connection_profile(request)


def test_create_connection_profile_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_connection_profile(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/connectionProfiles"
            % client.transport._host,
            args[1],
        )


def test_create_connection_profile_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connection_profile(
            datastream.CreateConnectionProfileRequest(),
            parent="parent_value",
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            connection_profile_id="connection_profile_id_value",
        )


def test_create_connection_profile_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.UpdateConnectionProfileRequest,
        dict,
    ],
)
def test_update_connection_profile_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "connection_profile": {
            "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
        }
    }
    request_init["connection_profile"] = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "oracle_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "database_service": "database_service_value",
            "connection_attributes": {},
        },
        "gcs_profile": {
            "bucket_name": "bucket_name_value",
            "root_path": "root_path_value",
        },
        "mysql_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "ssl_config": {
                "client_key": "client_key_value",
                "client_key_set": True,
                "client_certificate": "client_certificate_value",
                "client_certificate_set": True,
                "ca_certificate": "ca_certificate_value",
                "ca_certificate_set": True,
            },
        },
        "no_connectivity": {},
        "static_service_ip_connectivity": {},
        "forward_ssh_connectivity": {
            "hostname": "hostname_value",
            "username": "username_value",
            "port": 453,
            "password": "password_value",
            "private_key": "private_key_value",
        },
        "private_connectivity": {
            "private_connection_name": "private_connection_name_value"
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_connection_profile(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_connection_profile_rest_required_fields(
    request_type=datastream.UpdateConnectionProfileRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
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
    ).update_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_connection_profile._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_connection_profile(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_connection_profile_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_connection_profile._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "updateMask",
            )
        )
        & set(("connectionProfile",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_connection_profile_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_update_connection_profile"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_update_connection_profile"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.UpdateConnectionProfileRequest.pb(
            datastream.UpdateConnectionProfileRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.UpdateConnectionProfileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_connection_profile(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_connection_profile_rest_bad_request(
    transport: str = "rest", request_type=datastream.UpdateConnectionProfileRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "connection_profile": {
            "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
        }
    }
    request_init["connection_profile"] = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "oracle_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "database_service": "database_service_value",
            "connection_attributes": {},
        },
        "gcs_profile": {
            "bucket_name": "bucket_name_value",
            "root_path": "root_path_value",
        },
        "mysql_profile": {
            "hostname": "hostname_value",
            "port": 453,
            "username": "username_value",
            "password": "password_value",
            "ssl_config": {
                "client_key": "client_key_value",
                "client_key_set": True,
                "client_certificate": "client_certificate_value",
                "client_certificate_set": True,
                "ca_certificate": "ca_certificate_value",
                "ca_certificate_set": True,
            },
        },
        "no_connectivity": {},
        "static_service_ip_connectivity": {},
        "forward_ssh_connectivity": {
            "hostname": "hostname_value",
            "username": "username_value",
            "port": 453,
            "password": "password_value",
            "private_key": "private_key_value",
        },
        "private_connectivity": {
            "private_connection_name": "private_connection_name_value"
        },
    }
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
        client.update_connection_profile(request)


def test_update_connection_profile_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "connection_profile": {
                "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_connection_profile(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{connection_profile.name=projects/*/locations/*/connectionProfiles/*}"
            % client.transport._host,
            args[1],
        )


def test_update_connection_profile_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connection_profile(
            datastream.UpdateConnectionProfileRequest(),
            connection_profile=datastream_resources.ConnectionProfile(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_connection_profile_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteConnectionProfileRequest,
        dict,
    ],
)
def test_delete_connection_profile_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_connection_profile(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_connection_profile_rest_required_fields(
    request_type=datastream.DeleteConnectionProfileRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).delete_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_connection_profile._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_connection_profile(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_connection_profile_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_connection_profile._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_connection_profile_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_delete_connection_profile"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_delete_connection_profile"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.DeleteConnectionProfileRequest.pb(
            datastream.DeleteConnectionProfileRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.DeleteConnectionProfileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_connection_profile(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_connection_profile_rest_bad_request(
    transport: str = "rest", request_type=datastream.DeleteConnectionProfileRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
    }
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
        client.delete_connection_profile(request)


def test_delete_connection_profile_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/connectionProfiles/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_connection_profile(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/connectionProfiles/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_connection_profile_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connection_profile(
            datastream.DeleteConnectionProfileRequest(),
            name="name_value",
        )


def test_delete_connection_profile_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DiscoverConnectionProfileRequest,
        dict,
    ],
)
def test_discover_connection_profile_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.DiscoverConnectionProfileResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.DiscoverConnectionProfileResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.discover_connection_profile(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream.DiscoverConnectionProfileResponse)


def test_discover_connection_profile_rest_required_fields(
    request_type=datastream.DiscoverConnectionProfileRequest,
):
    transport_class = transports.DatastreamRestTransport

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
    ).discover_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).discover_connection_profile._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.DiscoverConnectionProfileResponse()
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = datastream.DiscoverConnectionProfileResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.discover_connection_profile(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_discover_connection_profile_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.discover_connection_profile._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_discover_connection_profile_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_discover_connection_profile"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_discover_connection_profile"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.DiscoverConnectionProfileRequest.pb(
            datastream.DiscoverConnectionProfileRequest()
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
        req.return_value._content = (
            datastream.DiscoverConnectionProfileResponse.to_json(
                datastream.DiscoverConnectionProfileResponse()
            )
        )

        request = datastream.DiscoverConnectionProfileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.DiscoverConnectionProfileResponse()

        client.discover_connection_profile(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_discover_connection_profile_rest_bad_request(
    transport: str = "rest", request_type=datastream.DiscoverConnectionProfileRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.discover_connection_profile(request)


def test_discover_connection_profile_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListStreamsRequest,
        dict,
    ],
)
def test_list_streams_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListStreamsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListStreamsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_streams(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListStreamsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_streams_rest_required_fields(request_type=datastream.ListStreamsRequest):
    transport_class = transports.DatastreamRestTransport

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
    ).list_streams._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_streams._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.ListStreamsResponse()
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

            pb_return_value = datastream.ListStreamsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_streams(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_streams_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_streams._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_streams_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_list_streams"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_list_streams"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.ListStreamsRequest.pb(datastream.ListStreamsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = datastream.ListStreamsResponse.to_json(
            datastream.ListStreamsResponse()
        )

        request = datastream.ListStreamsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.ListStreamsResponse()

        client.list_streams(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_streams_rest_bad_request(
    transport: str = "rest", request_type=datastream.ListStreamsRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_streams(request)


def test_list_streams_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListStreamsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListStreamsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_streams(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/streams"
            % client.transport._host,
            args[1],
        )


def test_list_streams_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_streams(
            datastream.ListStreamsRequest(),
            parent="parent_value",
        )


def test_list_streams_rest_pager(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
                next_page_token="abc",
            ),
            datastream.ListStreamsResponse(
                streams=[],
                next_page_token="def",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListStreamsResponse(
                streams=[
                    datastream_resources.Stream(),
                    datastream_resources.Stream(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(datastream.ListStreamsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_streams(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datastream_resources.Stream) for i in results)

        pages = list(client.list_streams(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetStreamRequest,
        dict,
    ],
)
def test_get_stream_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/streams/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.Stream(
            name="name_value",
            display_name="display_name_value",
            state=datastream_resources.Stream.State.CREATED,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.Stream.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_stream(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Stream)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.Stream.State.CREATED


def test_get_stream_rest_required_fields(request_type=datastream.GetStreamRequest):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).get_stream._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_stream._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream_resources.Stream()
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

            pb_return_value = datastream_resources.Stream.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_stream(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_stream_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_stream._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_stream_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_get_stream"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_get_stream"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.GetStreamRequest.pb(datastream.GetStreamRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = datastream_resources.Stream.to_json(
            datastream_resources.Stream()
        )

        request = datastream.GetStreamRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream_resources.Stream()

        client.get_stream(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_stream_rest_bad_request(
    transport: str = "rest", request_type=datastream.GetStreamRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/streams/sample3"}
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
        client.get_stream(request)


def test_get_stream_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.Stream()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/streams/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.Stream.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_stream(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/streams/*}"
            % client.transport._host,
            args[1],
        )


def test_get_stream_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_stream(
            datastream.GetStreamRequest(),
            name="name_value",
        )


def test_get_stream_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateStreamRequest,
        dict,
    ],
)
def test_create_stream_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["stream"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "source_config": {
            "source_connection_profile_name": "source_connection_profile_name_value",
            "oracle_source_config": {
                "allowlist": {
                    "oracle_schemas": [
                        {
                            "schema_name": "schema_name_value",
                            "oracle_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "oracle_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "precision": 972,
                                            "scale": 520,
                                            "encoding": "encoding_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
            "mysql_source_config": {
                "allowlist": {
                    "mysql_databases": [
                        {
                            "database_name": "database_name_value",
                            "mysql_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "mysql_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "collation": "collation_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
        },
        "destination_config": {
            "destination_connection_profile_name": "destination_connection_profile_name_value",
            "gcs_destination_config": {
                "path": "path_value",
                "gcs_file_format": 1,
                "file_rotation_mb": 1693,
                "file_rotation_interval": {"seconds": 751, "nanos": 543},
                "avro_file_format": {},
                "json_file_format": {"schema_file_format": 1, "compression": 1},
            },
        },
        "state": 1,
        "backfill_all": {"oracle_excluded_objects": {}, "mysql_excluded_objects": {}},
        "backfill_none": {},
        "errors": [
            {
                "reason": "reason_value",
                "error_uuid": "error_uuid_value",
                "message": "message_value",
                "error_time": {},
                "details": {},
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_stream(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_stream_rest_required_fields(
    request_type=datastream.CreateStreamRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["stream_id"] = ""
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
    assert "streamId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_stream._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "streamId" in jsonified_request
    assert jsonified_request["streamId"] == request_init["stream_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["streamId"] = "stream_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_stream._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "force",
            "request_id",
            "stream_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "streamId" in jsonified_request
    assert jsonified_request["streamId"] == "stream_id_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_stream(request)

            expected_params = [
                (
                    "streamId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_stream_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_stream._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "force",
                "requestId",
                "streamId",
                "validateOnly",
            )
        )
        & set(
            (
                "parent",
                "streamId",
                "stream",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_stream_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_create_stream"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_create_stream"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.CreateStreamRequest.pb(datastream.CreateStreamRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.CreateStreamRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_stream(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_stream_rest_bad_request(
    transport: str = "rest", request_type=datastream.CreateStreamRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["stream"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "source_config": {
            "source_connection_profile_name": "source_connection_profile_name_value",
            "oracle_source_config": {
                "allowlist": {
                    "oracle_schemas": [
                        {
                            "schema_name": "schema_name_value",
                            "oracle_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "oracle_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "precision": 972,
                                            "scale": 520,
                                            "encoding": "encoding_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
            "mysql_source_config": {
                "allowlist": {
                    "mysql_databases": [
                        {
                            "database_name": "database_name_value",
                            "mysql_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "mysql_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "collation": "collation_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
        },
        "destination_config": {
            "destination_connection_profile_name": "destination_connection_profile_name_value",
            "gcs_destination_config": {
                "path": "path_value",
                "gcs_file_format": 1,
                "file_rotation_mb": 1693,
                "file_rotation_interval": {"seconds": 751, "nanos": 543},
                "avro_file_format": {},
                "json_file_format": {"schema_file_format": 1, "compression": 1},
            },
        },
        "state": 1,
        "backfill_all": {"oracle_excluded_objects": {}, "mysql_excluded_objects": {}},
        "backfill_none": {},
        "errors": [
            {
                "reason": "reason_value",
                "error_uuid": "error_uuid_value",
                "message": "message_value",
                "error_time": {},
                "details": {},
            }
        ],
    }
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
        client.create_stream(request)


def test_create_stream_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_stream(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/streams"
            % client.transport._host,
            args[1],
        )


def test_create_stream_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_stream(
            datastream.CreateStreamRequest(),
            parent="parent_value",
            stream=datastream_resources.Stream(name="name_value"),
            stream_id="stream_id_value",
        )


def test_create_stream_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.UpdateStreamRequest,
        dict,
    ],
)
def test_update_stream_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "stream": {"name": "projects/sample1/locations/sample2/streams/sample3"}
    }
    request_init["stream"] = {
        "name": "projects/sample1/locations/sample2/streams/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "source_config": {
            "source_connection_profile_name": "source_connection_profile_name_value",
            "oracle_source_config": {
                "allowlist": {
                    "oracle_schemas": [
                        {
                            "schema_name": "schema_name_value",
                            "oracle_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "oracle_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "precision": 972,
                                            "scale": 520,
                                            "encoding": "encoding_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
            "mysql_source_config": {
                "allowlist": {
                    "mysql_databases": [
                        {
                            "database_name": "database_name_value",
                            "mysql_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "mysql_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "collation": "collation_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
        },
        "destination_config": {
            "destination_connection_profile_name": "destination_connection_profile_name_value",
            "gcs_destination_config": {
                "path": "path_value",
                "gcs_file_format": 1,
                "file_rotation_mb": 1693,
                "file_rotation_interval": {"seconds": 751, "nanos": 543},
                "avro_file_format": {},
                "json_file_format": {"schema_file_format": 1, "compression": 1},
            },
        },
        "state": 1,
        "backfill_all": {"oracle_excluded_objects": {}, "mysql_excluded_objects": {}},
        "backfill_none": {},
        "errors": [
            {
                "reason": "reason_value",
                "error_uuid": "error_uuid_value",
                "message": "message_value",
                "error_time": {},
                "details": {},
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_stream(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_stream_rest_required_fields(
    request_type=datastream.UpdateStreamRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
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
    ).update_stream._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_stream._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "force",
            "request_id",
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_stream(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_stream_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_stream._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "force",
                "requestId",
                "updateMask",
                "validateOnly",
            )
        )
        & set(("stream",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_stream_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_update_stream"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_update_stream"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.UpdateStreamRequest.pb(datastream.UpdateStreamRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.UpdateStreamRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_stream(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_stream_rest_bad_request(
    transport: str = "rest", request_type=datastream.UpdateStreamRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "stream": {"name": "projects/sample1/locations/sample2/streams/sample3"}
    }
    request_init["stream"] = {
        "name": "projects/sample1/locations/sample2/streams/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "source_config": {
            "source_connection_profile_name": "source_connection_profile_name_value",
            "oracle_source_config": {
                "allowlist": {
                    "oracle_schemas": [
                        {
                            "schema_name": "schema_name_value",
                            "oracle_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "oracle_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "precision": 972,
                                            "scale": 520,
                                            "encoding": "encoding_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
            "mysql_source_config": {
                "allowlist": {
                    "mysql_databases": [
                        {
                            "database_name": "database_name_value",
                            "mysql_tables": [
                                {
                                    "table_name": "table_name_value",
                                    "mysql_columns": [
                                        {
                                            "column_name": "column_name_value",
                                            "data_type": "data_type_value",
                                            "length": 642,
                                            "collation": "collation_value",
                                            "primary_key": True,
                                            "nullable": True,
                                            "ordinal_position": 1725,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "rejectlist": {},
            },
        },
        "destination_config": {
            "destination_connection_profile_name": "destination_connection_profile_name_value",
            "gcs_destination_config": {
                "path": "path_value",
                "gcs_file_format": 1,
                "file_rotation_mb": 1693,
                "file_rotation_interval": {"seconds": 751, "nanos": 543},
                "avro_file_format": {},
                "json_file_format": {"schema_file_format": 1, "compression": 1},
            },
        },
        "state": 1,
        "backfill_all": {"oracle_excluded_objects": {}, "mysql_excluded_objects": {}},
        "backfill_none": {},
        "errors": [
            {
                "reason": "reason_value",
                "error_uuid": "error_uuid_value",
                "message": "message_value",
                "error_time": {},
                "details": {},
            }
        ],
    }
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
        client.update_stream(request)


def test_update_stream_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "stream": {"name": "projects/sample1/locations/sample2/streams/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_stream(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{stream.name=projects/*/locations/*/streams/*}"
            % client.transport._host,
            args[1],
        )


def test_update_stream_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_stream(
            datastream.UpdateStreamRequest(),
            stream=datastream_resources.Stream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_stream_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteStreamRequest,
        dict,
    ],
)
def test_delete_stream_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/streams/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_stream(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_stream_rest_required_fields(
    request_type=datastream.DeleteStreamRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).delete_stream._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_stream._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_stream(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_stream_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_stream._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_stream_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_delete_stream"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_delete_stream"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.DeleteStreamRequest.pb(datastream.DeleteStreamRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.DeleteStreamRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_stream(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_stream_rest_bad_request(
    transport: str = "rest", request_type=datastream.DeleteStreamRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/streams/sample3"}
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
        client.delete_stream(request)


def test_delete_stream_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/streams/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_stream(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/streams/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_stream_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_stream(
            datastream.DeleteStreamRequest(),
            name="name_value",
        )


def test_delete_stream_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.FetchErrorsRequest,
        dict,
    ],
)
def test_fetch_errors_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"stream": "projects/sample1/locations/sample2/streams/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_errors(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_errors_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_fetch_errors"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_fetch_errors"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.FetchErrorsRequest.pb(datastream.FetchErrorsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.FetchErrorsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.fetch_errors(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_errors_rest_bad_request(
    transport: str = "rest", request_type=datastream.FetchErrorsRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"stream": "projects/sample1/locations/sample2/streams/sample3"}
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
        client.fetch_errors(request)


def test_fetch_errors_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.FetchStaticIpsRequest,
        dict,
    ],
)
def test_fetch_static_ips_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.FetchStaticIpsResponse(
            static_ips=["static_ips_value"],
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.FetchStaticIpsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_static_ips(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.FetchStaticIpsPager)
    assert response.static_ips == ["static_ips_value"]
    assert response.next_page_token == "next_page_token_value"


def test_fetch_static_ips_rest_required_fields(
    request_type=datastream.FetchStaticIpsRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).fetch_static_ips._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_static_ips._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.FetchStaticIpsResponse()
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

            pb_return_value = datastream.FetchStaticIpsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_static_ips(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_static_ips_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_static_ips._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_static_ips_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_fetch_static_ips"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_fetch_static_ips"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.FetchStaticIpsRequest.pb(
            datastream.FetchStaticIpsRequest()
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
        req.return_value._content = datastream.FetchStaticIpsResponse.to_json(
            datastream.FetchStaticIpsResponse()
        )

        request = datastream.FetchStaticIpsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.FetchStaticIpsResponse()

        client.fetch_static_ips(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_static_ips_rest_bad_request(
    transport: str = "rest", request_type=datastream.FetchStaticIpsRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2"}
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
        client.fetch_static_ips(request)


def test_fetch_static_ips_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.FetchStaticIpsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.FetchStaticIpsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.fetch_static_ips(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*}:fetchStaticIps"
            % client.transport._host,
            args[1],
        )


def test_fetch_static_ips_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_static_ips(
            datastream.FetchStaticIpsRequest(),
            name="name_value",
        )


def test_fetch_static_ips_rest_pager(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            datastream.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(datastream.FetchStaticIpsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"name": "projects/sample1/locations/sample2"}

        pager = client.fetch_static_ips(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)

        pages = list(client.fetch_static_ips(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreatePrivateConnectionRequest,
        dict,
    ],
)
def test_create_private_connection_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["private_connection"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "state": 1,
        "error": {
            "reason": "reason_value",
            "error_uuid": "error_uuid_value",
            "message": "message_value",
            "error_time": {},
            "details": {},
        },
        "vpc_peering_config": {"vpc_name": "vpc_name_value", "subnet": "subnet_value"},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_private_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_private_connection_rest_required_fields(
    request_type=datastream.CreatePrivateConnectionRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["private_connection_id"] = ""
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
    assert "privateConnectionId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_private_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "privateConnectionId" in jsonified_request
    assert (
        jsonified_request["privateConnectionId"]
        == request_init["private_connection_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["privateConnectionId"] = "private_connection_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_private_connection._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "private_connection_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "privateConnectionId" in jsonified_request
    assert jsonified_request["privateConnectionId"] == "private_connection_id_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_private_connection(request)

            expected_params = [
                (
                    "privateConnectionId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_private_connection_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_private_connection._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "privateConnectionId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "privateConnectionId",
                "privateConnection",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_private_connection_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_create_private_connection"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_create_private_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.CreatePrivateConnectionRequest.pb(
            datastream.CreatePrivateConnectionRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.CreatePrivateConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_private_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_private_connection_rest_bad_request(
    transport: str = "rest", request_type=datastream.CreatePrivateConnectionRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["private_connection"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "state": 1,
        "error": {
            "reason": "reason_value",
            "error_uuid": "error_uuid_value",
            "message": "message_value",
            "error_time": {},
            "details": {},
        },
        "vpc_peering_config": {"vpc_name": "vpc_name_value", "subnet": "subnet_value"},
    }
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
        client.create_private_connection(request)


def test_create_private_connection_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_private_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/privateConnections"
            % client.transport._host,
            args[1],
        )


def test_create_private_connection_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_private_connection(
            datastream.CreatePrivateConnectionRequest(),
            parent="parent_value",
            private_connection=datastream_resources.PrivateConnection(
                name="name_value"
            ),
            private_connection_id="private_connection_id_value",
        )


def test_create_private_connection_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetPrivateConnectionRequest,
        dict,
    ],
)
def test_get_private_connection_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.PrivateConnection(
            name="name_value",
            display_name="display_name_value",
            state=datastream_resources.PrivateConnection.State.CREATING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.PrivateConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_private_connection(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.PrivateConnection)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == datastream_resources.PrivateConnection.State.CREATING


def test_get_private_connection_rest_required_fields(
    request_type=datastream.GetPrivateConnectionRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).get_private_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_private_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream_resources.PrivateConnection()
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

            pb_return_value = datastream_resources.PrivateConnection.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_private_connection(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_private_connection_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_private_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_private_connection_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_get_private_connection"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_get_private_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.GetPrivateConnectionRequest.pb(
            datastream.GetPrivateConnectionRequest()
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
        req.return_value._content = datastream_resources.PrivateConnection.to_json(
            datastream_resources.PrivateConnection()
        )

        request = datastream.GetPrivateConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream_resources.PrivateConnection()

        client.get_private_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_private_connection_rest_bad_request(
    transport: str = "rest", request_type=datastream.GetPrivateConnectionRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
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
        client.get_private_connection(request)


def test_get_private_connection_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.PrivateConnection()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/privateConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.PrivateConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_private_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/privateConnections/*}"
            % client.transport._host,
            args[1],
        )


def test_get_private_connection_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_private_connection(
            datastream.GetPrivateConnectionRequest(),
            name="name_value",
        )


def test_get_private_connection_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListPrivateConnectionsRequest,
        dict,
    ],
)
def test_list_private_connections_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListPrivateConnectionsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListPrivateConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_private_connections(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateConnectionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_private_connections_rest_required_fields(
    request_type=datastream.ListPrivateConnectionsRequest,
):
    transport_class = transports.DatastreamRestTransport

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
    ).list_private_connections._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_private_connections._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.ListPrivateConnectionsResponse()
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

            pb_return_value = datastream.ListPrivateConnectionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_private_connections(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_private_connections_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_private_connections._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_private_connections_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_list_private_connections"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_list_private_connections"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.ListPrivateConnectionsRequest.pb(
            datastream.ListPrivateConnectionsRequest()
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
        req.return_value._content = datastream.ListPrivateConnectionsResponse.to_json(
            datastream.ListPrivateConnectionsResponse()
        )

        request = datastream.ListPrivateConnectionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.ListPrivateConnectionsResponse()

        client.list_private_connections(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_private_connections_rest_bad_request(
    transport: str = "rest", request_type=datastream.ListPrivateConnectionsRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_private_connections(request)


def test_list_private_connections_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListPrivateConnectionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListPrivateConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_private_connections(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/privateConnections"
            % client.transport._host,
            args[1],
        )


def test_list_private_connections_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_private_connections(
            datastream.ListPrivateConnectionsRequest(),
            parent="parent_value",
        )


def test_list_private_connections_rest_pager(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListPrivateConnectionsResponse(
                private_connections=[
                    datastream_resources.PrivateConnection(),
                    datastream_resources.PrivateConnection(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            datastream.ListPrivateConnectionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_private_connections(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, datastream_resources.PrivateConnection) for i in results
        )

        pages = list(client.list_private_connections(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeletePrivateConnectionRequest,
        dict,
    ],
)
def test_delete_private_connection_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_private_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_private_connection_rest_required_fields(
    request_type=datastream.DeletePrivateConnectionRequest,
):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).delete_private_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_private_connection._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "force",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_private_connection(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_private_connection_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_private_connection._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "force",
                "requestId",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_private_connection_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_delete_private_connection"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_delete_private_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.DeletePrivateConnectionRequest.pb(
            datastream.DeletePrivateConnectionRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.DeletePrivateConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_private_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_private_connection_rest_bad_request(
    transport: str = "rest", request_type=datastream.DeletePrivateConnectionRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
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
        client.delete_private_connection(request)


def test_delete_private_connection_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/privateConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_private_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/privateConnections/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_private_connection_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_private_connection(
            datastream.DeletePrivateConnectionRequest(),
            name="name_value",
        )


def test_delete_private_connection_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.CreateRouteRequest,
        dict,
    ],
)
def test_create_route_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
    request_init["route"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "destination_address": "destination_address_value",
        "destination_port": 1734,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_route_rest_required_fields(request_type=datastream.CreateRouteRequest):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["route_id"] = ""
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
    assert "routeId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "routeId" in jsonified_request
    assert jsonified_request["routeId"] == request_init["route_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["routeId"] = "route_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "route_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "routeId" in jsonified_request
    assert jsonified_request["routeId"] == "route_id_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_route(request)

            expected_params = [
                (
                    "routeId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_route_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_route._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "routeId",
            )
        )
        & set(
            (
                "parent",
                "routeId",
                "route",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_route_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_create_route"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_create_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.CreateRouteRequest.pb(datastream.CreateRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.CreateRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_route_rest_bad_request(
    transport: str = "rest", request_type=datastream.CreateRouteRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
    request_init["route"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "display_name": "display_name_value",
        "destination_address": "destination_address_value",
        "destination_port": 1734,
    }
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
        client.create_route(request)


def test_create_route_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/privateConnections/*}/routes"
            % client.transport._host,
            args[1],
        )


def test_create_route_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_route(
            datastream.CreateRouteRequest(),
            parent="parent_value",
            route=datastream_resources.Route(name="name_value"),
            route_id="route_id_value",
        )


def test_create_route_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.GetRouteRequest,
        dict,
    ],
)
def test_get_route_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.Route(
            name="name_value",
            display_name="display_name_value",
            destination_address="destination_address_value",
            destination_port=1734,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.Route.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_route(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, datastream_resources.Route)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.destination_address == "destination_address_value"
    assert response.destination_port == 1734


def test_get_route_rest_required_fields(request_type=datastream.GetRouteRequest):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).get_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream_resources.Route()
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

            pb_return_value = datastream_resources.Route.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_route_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_route_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_get_route"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_get_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.GetRouteRequest.pb(datastream.GetRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = datastream_resources.Route.to_json(
            datastream_resources.Route()
        )

        request = datastream.GetRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream_resources.Route()

        client.get_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_route_rest_bad_request(
    transport: str = "rest", request_type=datastream.GetRouteRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
    }
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
        client.get_route(request)


def test_get_route_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream_resources.Route()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream_resources.Route.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/privateConnections/*/routes/*}"
            % client.transport._host,
            args[1],
        )


def test_get_route_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_route(
            datastream.GetRouteRequest(),
            name="name_value",
        )


def test_get_route_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.ListRoutesRequest,
        dict,
    ],
)
def test_list_routes_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListRoutesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_routes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRoutesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_routes_rest_required_fields(request_type=datastream.ListRoutesRequest):
    transport_class = transports.DatastreamRestTransport

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
    ).list_routes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_routes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = datastream.ListRoutesResponse()
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

            pb_return_value = datastream.ListRoutesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_routes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_routes_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_routes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_routes_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DatastreamRestInterceptor, "post_list_routes"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_list_routes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.ListRoutesRequest.pb(datastream.ListRoutesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = datastream.ListRoutesResponse.to_json(
            datastream.ListRoutesResponse()
        )

        request = datastream.ListRoutesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = datastream.ListRoutesResponse()

        client.list_routes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_routes_rest_bad_request(
    transport: str = "rest", request_type=datastream.ListRoutesRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
    }
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
        client.list_routes(request)


def test_list_routes_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = datastream.ListRoutesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = datastream.ListRoutesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_routes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/privateConnections/*}/routes"
            % client.transport._host,
            args[1],
        )


def test_list_routes_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_routes(
            datastream.ListRoutesRequest(),
            parent="parent_value",
        )


def test_list_routes_rest_pager(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
                next_page_token="abc",
            ),
            datastream.ListRoutesResponse(
                routes=[],
                next_page_token="def",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                ],
                next_page_token="ghi",
            ),
            datastream.ListRoutesResponse(
                routes=[
                    datastream_resources.Route(),
                    datastream_resources.Route(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(datastream.ListRoutesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/privateConnections/sample3"
        }

        pager = client.list_routes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datastream_resources.Route) for i in results)

        pages = list(client.list_routes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datastream.DeleteRouteRequest,
        dict,
    ],
)
def test_delete_route_rest(request_type):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_route(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_route_rest_required_fields(request_type=datastream.DeleteRouteRequest):
    transport_class = transports.DatastreamRestTransport

    request_init = {}
    request_init["name"] = ""
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
    ).delete_route._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_route._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_route(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_route_rest_unset_required_fields():
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_route._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_route_rest_interceptors(null_interceptor):
    transport = transports.DatastreamRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DatastreamRestInterceptor(),
    )
    client = DatastreamClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DatastreamRestInterceptor, "post_delete_route"
    ) as post, mock.patch.object(
        transports.DatastreamRestInterceptor, "pre_delete_route"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = datastream.DeleteRouteRequest.pb(datastream.DeleteRouteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = datastream.DeleteRouteRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_route(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_route_rest_bad_request(
    transport: str = "rest", request_type=datastream.DeleteRouteRequest
):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
    }
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
        client.delete_route(request)


def test_delete_route_rest_flattened():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/privateConnections/sample3/routes/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_route(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/privateConnections/*/routes/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_route_rest_flattened_error(transport: str = "rest"):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_route(
            datastream.DeleteRouteRequest(),
            name="name_value",
        )


def test_delete_route_rest_error():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastreamClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastreamClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DatastreamClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DatastreamClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DatastreamClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DatastreamClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DatastreamGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DatastreamGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DatastreamGrpcTransport,
        transports.DatastreamGrpcAsyncIOTransport,
        transports.DatastreamRestTransport,
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
    transport = DatastreamClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DatastreamGrpcTransport,
    )


def test_datastream_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DatastreamTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_datastream_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datastream_v1alpha1.services.datastream.transports.DatastreamTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DatastreamTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_connection_profiles",
        "get_connection_profile",
        "create_connection_profile",
        "update_connection_profile",
        "delete_connection_profile",
        "discover_connection_profile",
        "list_streams",
        "get_stream",
        "create_stream",
        "update_stream",
        "delete_stream",
        "fetch_errors",
        "fetch_static_ips",
        "create_private_connection",
        "get_private_connection",
        "list_private_connections",
        "delete_private_connection",
        "create_route",
        "get_route",
        "list_routes",
        "delete_route",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_datastream_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.datastream_v1alpha1.services.datastream.transports.DatastreamTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DatastreamTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_datastream_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.datastream_v1alpha1.services.datastream.transports.DatastreamTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DatastreamTransport()
        adc.assert_called_once()


def test_datastream_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DatastreamClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DatastreamGrpcTransport,
        transports.DatastreamGrpcAsyncIOTransport,
    ],
)
def test_datastream_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DatastreamGrpcTransport,
        transports.DatastreamGrpcAsyncIOTransport,
        transports.DatastreamRestTransport,
    ],
)
def test_datastream_transport_auth_gdch_credentials(transport_class):
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
        (transports.DatastreamGrpcTransport, grpc_helpers),
        (transports.DatastreamGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_datastream_transport_create_channel(transport_class, grpc_helpers):
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
            "datastream.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="datastream.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DatastreamGrpcTransport, transports.DatastreamGrpcAsyncIOTransport],
)
def test_datastream_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_datastream_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DatastreamRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_datastream_rest_lro_client():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_datastream_host_no_port(transport_name):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datastream.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "datastream.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://datastream.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_datastream_host_with_port(transport_name):
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datastream.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "datastream.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://datastream.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_datastream_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DatastreamClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DatastreamClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_connection_profiles._session
    session2 = client2.transport.list_connection_profiles._session
    assert session1 != session2
    session1 = client1.transport.get_connection_profile._session
    session2 = client2.transport.get_connection_profile._session
    assert session1 != session2
    session1 = client1.transport.create_connection_profile._session
    session2 = client2.transport.create_connection_profile._session
    assert session1 != session2
    session1 = client1.transport.update_connection_profile._session
    session2 = client2.transport.update_connection_profile._session
    assert session1 != session2
    session1 = client1.transport.delete_connection_profile._session
    session2 = client2.transport.delete_connection_profile._session
    assert session1 != session2
    session1 = client1.transport.discover_connection_profile._session
    session2 = client2.transport.discover_connection_profile._session
    assert session1 != session2
    session1 = client1.transport.list_streams._session
    session2 = client2.transport.list_streams._session
    assert session1 != session2
    session1 = client1.transport.get_stream._session
    session2 = client2.transport.get_stream._session
    assert session1 != session2
    session1 = client1.transport.create_stream._session
    session2 = client2.transport.create_stream._session
    assert session1 != session2
    session1 = client1.transport.update_stream._session
    session2 = client2.transport.update_stream._session
    assert session1 != session2
    session1 = client1.transport.delete_stream._session
    session2 = client2.transport.delete_stream._session
    assert session1 != session2
    session1 = client1.transport.fetch_errors._session
    session2 = client2.transport.fetch_errors._session
    assert session1 != session2
    session1 = client1.transport.fetch_static_ips._session
    session2 = client2.transport.fetch_static_ips._session
    assert session1 != session2
    session1 = client1.transport.create_private_connection._session
    session2 = client2.transport.create_private_connection._session
    assert session1 != session2
    session1 = client1.transport.get_private_connection._session
    session2 = client2.transport.get_private_connection._session
    assert session1 != session2
    session1 = client1.transport.list_private_connections._session
    session2 = client2.transport.list_private_connections._session
    assert session1 != session2
    session1 = client1.transport.delete_private_connection._session
    session2 = client2.transport.delete_private_connection._session
    assert session1 != session2
    session1 = client1.transport.create_route._session
    session2 = client2.transport.create_route._session
    assert session1 != session2
    session1 = client1.transport.get_route._session
    session2 = client2.transport.get_route._session
    assert session1 != session2
    session1 = client1.transport.list_routes._session
    session2 = client2.transport.list_routes._session
    assert session1 != session2
    session1 = client1.transport.delete_route._session
    session2 = client2.transport.delete_route._session
    assert session1 != session2


def test_datastream_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DatastreamGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_datastream_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DatastreamGrpcAsyncIOTransport(
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
    [transports.DatastreamGrpcTransport, transports.DatastreamGrpcAsyncIOTransport],
)
def test_datastream_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.DatastreamGrpcTransport, transports.DatastreamGrpcAsyncIOTransport],
)
def test_datastream_transport_channel_mtls_with_adc(transport_class):
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


def test_datastream_grpc_lro_client():
    client = DatastreamClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_datastream_grpc_lro_async_client():
    client = DatastreamAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_connection_profile_path():
    project = "squid"
    location = "clam"
    connection_profile = "whelk"
    expected = "projects/{project}/locations/{location}/connectionProfiles/{connection_profile}".format(
        project=project,
        location=location,
        connection_profile=connection_profile,
    )
    actual = DatastreamClient.connection_profile_path(
        project, location, connection_profile
    )
    assert expected == actual


def test_parse_connection_profile_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "connection_profile": "nudibranch",
    }
    path = DatastreamClient.connection_profile_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_connection_profile_path(path)
    assert expected == actual


def test_private_connection_path():
    project = "cuttlefish"
    location = "mussel"
    private_connection = "winkle"
    expected = "projects/{project}/locations/{location}/privateConnections/{private_connection}".format(
        project=project,
        location=location,
        private_connection=private_connection,
    )
    actual = DatastreamClient.private_connection_path(
        project, location, private_connection
    )
    assert expected == actual


def test_parse_private_connection_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "private_connection": "abalone",
    }
    path = DatastreamClient.private_connection_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_private_connection_path(path)
    assert expected == actual


def test_route_path():
    project = "squid"
    location = "clam"
    private_connection = "whelk"
    route = "octopus"
    expected = "projects/{project}/locations/{location}/privateConnections/{private_connection}/routes/{route}".format(
        project=project,
        location=location,
        private_connection=private_connection,
        route=route,
    )
    actual = DatastreamClient.route_path(project, location, private_connection, route)
    assert expected == actual


def test_parse_route_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "private_connection": "cuttlefish",
        "route": "mussel",
    }
    path = DatastreamClient.route_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_route_path(path)
    assert expected == actual


def test_stream_path():
    project = "winkle"
    location = "nautilus"
    stream = "scallop"
    expected = "projects/{project}/locations/{location}/streams/{stream}".format(
        project=project,
        location=location,
        stream=stream,
    )
    actual = DatastreamClient.stream_path(project, location, stream)
    assert expected == actual


def test_parse_stream_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "stream": "clam",
    }
    path = DatastreamClient.stream_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_stream_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DatastreamClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = DatastreamClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DatastreamClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = DatastreamClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DatastreamClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = DatastreamClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DatastreamClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = DatastreamClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DatastreamClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = DatastreamClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DatastreamClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DatastreamTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DatastreamClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DatastreamTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DatastreamClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DatastreamAsyncClient(
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
        client = DatastreamClient(
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
        client = DatastreamClient(
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
        (DatastreamClient, transports.DatastreamGrpcTransport),
        (DatastreamAsyncClient, transports.DatastreamGrpcAsyncIOTransport),
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
