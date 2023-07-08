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
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.dataform_v1beta1.services.dataform import (
    DataformAsyncClient,
    DataformClient,
    pagers,
    transports,
)
from google.cloud.dataform_v1beta1.types import dataform


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

    assert DataformClient._get_default_mtls_endpoint(None) is None
    assert DataformClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        DataformClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataformClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataformClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DataformClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DataformClient, "grpc"),
        (DataformAsyncClient, "grpc_asyncio"),
        (DataformClient, "rest"),
    ],
)
def test_dataform_client_from_service_account_info(client_class, transport_name):
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
            "dataform.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataform.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataformGrpcTransport, "grpc"),
        (transports.DataformGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DataformRestTransport, "rest"),
    ],
)
def test_dataform_client_service_account_always_use_jwt(
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
        (DataformClient, "grpc"),
        (DataformAsyncClient, "grpc_asyncio"),
        (DataformClient, "rest"),
    ],
)
def test_dataform_client_from_service_account_file(client_class, transport_name):
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
            "dataform.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataform.googleapis.com"
        )


def test_dataform_client_get_transport_class():
    transport = DataformClient.get_transport_class()
    available_transports = [
        transports.DataformGrpcTransport,
        transports.DataformRestTransport,
    ]
    assert transport in available_transports

    transport = DataformClient.get_transport_class("grpc")
    assert transport == transports.DataformGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataformClient, transports.DataformGrpcTransport, "grpc"),
        (DataformAsyncClient, transports.DataformGrpcAsyncIOTransport, "grpc_asyncio"),
        (DataformClient, transports.DataformRestTransport, "rest"),
    ],
)
@mock.patch.object(
    DataformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataformClient)
)
@mock.patch.object(
    DataformAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataformAsyncClient),
)
def test_dataform_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataformClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataformClient, "get_transport_class") as gtc:
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
        (DataformClient, transports.DataformGrpcTransport, "grpc", "true"),
        (
            DataformAsyncClient,
            transports.DataformGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DataformClient, transports.DataformGrpcTransport, "grpc", "false"),
        (
            DataformAsyncClient,
            transports.DataformGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (DataformClient, transports.DataformRestTransport, "rest", "true"),
        (DataformClient, transports.DataformRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    DataformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataformClient)
)
@mock.patch.object(
    DataformAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataformAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_dataform_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [DataformClient, DataformAsyncClient])
@mock.patch.object(
    DataformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataformClient)
)
@mock.patch.object(
    DataformAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataformAsyncClient),
)
def test_dataform_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DataformClient, transports.DataformGrpcTransport, "grpc"),
        (DataformAsyncClient, transports.DataformGrpcAsyncIOTransport, "grpc_asyncio"),
        (DataformClient, transports.DataformRestTransport, "rest"),
    ],
)
def test_dataform_client_client_options_scopes(
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
        (DataformClient, transports.DataformGrpcTransport, "grpc", grpc_helpers),
        (
            DataformAsyncClient,
            transports.DataformGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (DataformClient, transports.DataformRestTransport, "rest", None),
    ],
)
def test_dataform_client_client_options_credentials_file(
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


def test_dataform_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataform_v1beta1.services.dataform.transports.DataformGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataformClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (DataformClient, transports.DataformGrpcTransport, "grpc", grpc_helpers),
        (
            DataformAsyncClient,
            transports.DataformGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_dataform_client_create_channel_credentials_file(
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
            "dataform.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="dataform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListRepositoriesRequest,
        dict,
    ],
)
def test_list_repositories(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListRepositoriesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_repositories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListRepositoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_repositories_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        client.list_repositories()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListRepositoriesRequest()


@pytest.mark.asyncio
async def test_list_repositories_async(
    transport: str = "grpc_asyncio", request_type=dataform.ListRepositoriesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListRepositoriesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_repositories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListRepositoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_repositories_async_from_dict():
    await test_list_repositories_async(request_type=dict)


def test_list_repositories_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListRepositoriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        call.return_value = dataform.ListRepositoriesResponse()
        client.list_repositories(request)

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
async def test_list_repositories_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListRepositoriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListRepositoriesResponse()
        )
        await client.list_repositories(request)

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


def test_list_repositories_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListRepositoriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_repositories(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_repositories_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_repositories(
            dataform.ListRepositoriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_repositories_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListRepositoriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListRepositoriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_repositories(
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
async def test_list_repositories_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_repositories(
            dataform.ListRepositoriesRequest(),
            parent="parent_value",
        )


def test_list_repositories_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                    dataform.Repository(),
                ],
                next_page_token="abc",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_repositories(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.Repository) for i in results)


def test_list_repositories_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                    dataform.Repository(),
                ],
                next_page_token="abc",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_repositories(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_repositories_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                    dataform.Repository(),
                ],
                next_page_token="abc",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_repositories(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.Repository) for i in responses)


@pytest.mark.asyncio
async def test_list_repositories_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                    dataform.Repository(),
                ],
                next_page_token="abc",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_repositories(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetRepositoryRequest,
        dict,
    ],
)
def test_get_repository(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository(
            name="name_value",
        )
        response = client.get_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_get_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        client.get_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetRepositoryRequest()


@pytest.mark.asyncio
async def test_get_repository_async(
    transport: str = "grpc_asyncio", request_type=dataform.GetRepositoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.Repository(
                name="name_value",
            )
        )
        response = await client.get_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_repository_async_from_dict():
    await test_get_repository_async(request_type=dict)


def test_get_repository_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        call.return_value = dataform.Repository()
        client.get_repository(request)

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
async def test_get_repository_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        await client.get_repository(request)

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


def test_get_repository_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_repository(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_repository_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_repository(
            dataform.GetRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_repository_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_repository(
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
async def test_get_repository_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_repository(
            dataform.GetRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateRepositoryRequest,
        dict,
    ],
)
def test_create_repository(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository(
            name="name_value",
        )
        response = client.create_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_create_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        client.create_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateRepositoryRequest()


@pytest.mark.asyncio
async def test_create_repository_async(
    transport: str = "grpc_asyncio", request_type=dataform.CreateRepositoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.Repository(
                name="name_value",
            )
        )
        response = await client.create_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_repository_async_from_dict():
    await test_create_repository_async(request_type=dict)


def test_create_repository_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateRepositoryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        call.return_value = dataform.Repository()
        client.create_repository(request)

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
async def test_create_repository_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateRepositoryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        await client.create_repository(request)

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


def test_create_repository_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_repository(
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].repository
        mock_val = dataform.Repository(name="name_value")
        assert arg == mock_val
        arg = args[0].repository_id
        mock_val = "repository_id_value"
        assert arg == mock_val


def test_create_repository_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_repository(
            dataform.CreateRepositoryRequest(),
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )


@pytest.mark.asyncio
async def test_create_repository_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_repository(
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].repository
        mock_val = dataform.Repository(name="name_value")
        assert arg == mock_val
        arg = args[0].repository_id
        mock_val = "repository_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_repository_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_repository(
            dataform.CreateRepositoryRequest(),
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.UpdateRepositoryRequest,
        dict,
    ],
)
def test_update_repository(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository(
            name="name_value",
        )
        response = client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.UpdateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_update_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        client.update_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.UpdateRepositoryRequest()


@pytest.mark.asyncio
async def test_update_repository_async(
    transport: str = "grpc_asyncio", request_type=dataform.UpdateRepositoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.Repository(
                name="name_value",
            )
        )
        response = await client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.UpdateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_update_repository_async_from_dict():
    await test_update_repository_async(request_type=dict)


def test_update_repository_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.UpdateRepositoryRequest()

    request.repository.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        call.return_value = dataform.Repository()
        client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "repository.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_repository_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.UpdateRepositoryRequest()

    request.repository.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        await client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "repository.name=name_value",
    ) in kw["metadata"]


def test_update_repository_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_repository(
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].repository
        mock_val = dataform.Repository(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_repository_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_repository(
            dataform.UpdateRepositoryRequest(),
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_repository_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Repository()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Repository())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_repository(
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].repository
        mock_val = dataform.Repository(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_repository_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_repository(
            dataform.UpdateRepositoryRequest(),
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteRepositoryRequest,
        dict,
    ],
)
def test_delete_repository(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        client.delete_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteRepositoryRequest()


@pytest.mark.asyncio
async def test_delete_repository_async(
    transport: str = "grpc_asyncio", request_type=dataform.DeleteRepositoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_repository_async_from_dict():
    await test_delete_repository_async(request_type=dict)


def test_delete_repository_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        call.return_value = None
        client.delete_repository(request)

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
async def test_delete_repository_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_repository(request)

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


def test_delete_repository_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_repository(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_repository_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_repository(
            dataform.DeleteRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_repository_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_repository(
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
async def test_delete_repository_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_repository(
            dataform.DeleteRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchRemoteBranchesRequest,
        dict,
    ],
)
def test_fetch_remote_branches(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_remote_branches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.FetchRemoteBranchesResponse(
            branches=["branches_value"],
        )
        response = client.fetch_remote_branches(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchRemoteBranchesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchRemoteBranchesResponse)
    assert response.branches == ["branches_value"]


def test_fetch_remote_branches_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_remote_branches), "__call__"
    ) as call:
        client.fetch_remote_branches()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchRemoteBranchesRequest()


@pytest.mark.asyncio
async def test_fetch_remote_branches_async(
    transport: str = "grpc_asyncio", request_type=dataform.FetchRemoteBranchesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_remote_branches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchRemoteBranchesResponse(
                branches=["branches_value"],
            )
        )
        response = await client.fetch_remote_branches(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchRemoteBranchesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchRemoteBranchesResponse)
    assert response.branches == ["branches_value"]


@pytest.mark.asyncio
async def test_fetch_remote_branches_async_from_dict():
    await test_fetch_remote_branches_async(request_type=dict)


def test_fetch_remote_branches_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchRemoteBranchesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_remote_branches), "__call__"
    ) as call:
        call.return_value = dataform.FetchRemoteBranchesResponse()
        client.fetch_remote_branches(request)

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
async def test_fetch_remote_branches_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchRemoteBranchesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_remote_branches), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchRemoteBranchesResponse()
        )
        await client.fetch_remote_branches(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListWorkspacesRequest,
        dict,
    ],
)
def test_list_workspaces(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkspacesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkspacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkspacesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workspaces_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        client.list_workspaces()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkspacesRequest()


@pytest.mark.asyncio
async def test_list_workspaces_async(
    transport: str = "grpc_asyncio", request_type=dataform.ListWorkspacesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkspacesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkspacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkspacesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_workspaces_async_from_dict():
    await test_list_workspaces_async(request_type=dict)


def test_list_workspaces_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListWorkspacesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        call.return_value = dataform.ListWorkspacesResponse()
        client.list_workspaces(request)

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
async def test_list_workspaces_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListWorkspacesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkspacesResponse()
        )
        await client.list_workspaces(request)

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


def test_list_workspaces_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkspacesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_workspaces(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_workspaces_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workspaces(
            dataform.ListWorkspacesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_workspaces_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkspacesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkspacesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_workspaces(
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
async def test_list_workspaces_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_workspaces(
            dataform.ListWorkspacesRequest(),
            parent="parent_value",
        )


def test_list_workspaces_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[],
                next_page_token="def",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_workspaces(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.Workspace) for i in results)


def test_list_workspaces_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workspaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[],
                next_page_token="def",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_workspaces(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_workspaces_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workspaces), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[],
                next_page_token="def",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_workspaces(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.Workspace) for i in responses)


@pytest.mark.asyncio
async def test_list_workspaces_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workspaces), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[],
                next_page_token="def",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_workspaces(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetWorkspaceRequest,
        dict,
    ],
)
def test_get_workspace(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace(
            name="name_value",
        )
        response = client.get_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


def test_get_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        client.get_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkspaceRequest()


@pytest.mark.asyncio
async def test_get_workspace_async(
    transport: str = "grpc_asyncio", request_type=dataform.GetWorkspaceRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.Workspace(
                name="name_value",
            )
        )
        response = await client.get_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_workspace_async_from_dict():
    await test_get_workspace_async(request_type=dict)


def test_get_workspace_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        call.return_value = dataform.Workspace()
        client.get_workspace(request)

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
async def test_get_workspace_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Workspace())
        await client.get_workspace(request)

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


def test_get_workspace_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_workspace(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_workspace_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workspace(
            dataform.GetWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_workspace_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Workspace())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_workspace(
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
async def test_get_workspace_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_workspace(
            dataform.GetWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateWorkspaceRequest,
        dict,
    ],
)
def test_create_workspace(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace(
            name="name_value",
        )
        response = client.create_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


def test_create_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        client.create_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkspaceRequest()


@pytest.mark.asyncio
async def test_create_workspace_async(
    transport: str = "grpc_asyncio", request_type=dataform.CreateWorkspaceRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.Workspace(
                name="name_value",
            )
        )
        response = await client.create_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_workspace_async_from_dict():
    await test_create_workspace_async(request_type=dict)


def test_create_workspace_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateWorkspaceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        call.return_value = dataform.Workspace()
        client.create_workspace(request)

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
async def test_create_workspace_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateWorkspaceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Workspace())
        await client.create_workspace(request)

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


def test_create_workspace_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_workspace(
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].workspace
        mock_val = dataform.Workspace(name="name_value")
        assert arg == mock_val
        arg = args[0].workspace_id
        mock_val = "workspace_id_value"
        assert arg == mock_val


def test_create_workspace_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workspace(
            dataform.CreateWorkspaceRequest(),
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )


@pytest.mark.asyncio
async def test_create_workspace_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.Workspace()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataform.Workspace())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_workspace(
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].workspace
        mock_val = dataform.Workspace(name="name_value")
        assert arg == mock_val
        arg = args[0].workspace_id
        mock_val = "workspace_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_workspace_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_workspace(
            dataform.CreateWorkspaceRequest(),
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteWorkspaceRequest,
        dict,
    ],
)
def test_delete_workspace(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        client.delete_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkspaceRequest()


@pytest.mark.asyncio
async def test_delete_workspace_async(
    transport: str = "grpc_asyncio", request_type=dataform.DeleteWorkspaceRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_workspace_async_from_dict():
    await test_delete_workspace_async(request_type=dict)


def test_delete_workspace_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        call.return_value = None
        client.delete_workspace(request)

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
async def test_delete_workspace_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_workspace(request)

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


def test_delete_workspace_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_workspace(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_workspace_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workspace(
            dataform.DeleteWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_workspace_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_workspace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_workspace(
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
async def test_delete_workspace_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_workspace(
            dataform.DeleteWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.InstallNpmPackagesRequest,
        dict,
    ],
)
def test_install_npm_packages(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.InstallNpmPackagesResponse()
        response = client.install_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.InstallNpmPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.InstallNpmPackagesResponse)


def test_install_npm_packages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_npm_packages), "__call__"
    ) as call:
        client.install_npm_packages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.InstallNpmPackagesRequest()


@pytest.mark.asyncio
async def test_install_npm_packages_async(
    transport: str = "grpc_asyncio", request_type=dataform.InstallNpmPackagesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.InstallNpmPackagesResponse()
        )
        response = await client.install_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.InstallNpmPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.InstallNpmPackagesResponse)


@pytest.mark.asyncio
async def test_install_npm_packages_async_from_dict():
    await test_install_npm_packages_async(request_type=dict)


def test_install_npm_packages_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.InstallNpmPackagesRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_npm_packages), "__call__"
    ) as call:
        call.return_value = dataform.InstallNpmPackagesResponse()
        client.install_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_install_npm_packages_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.InstallNpmPackagesRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_npm_packages), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.InstallNpmPackagesResponse()
        )
        await client.install_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.PullGitCommitsRequest,
        dict,
    ],
)
def test_pull_git_commits(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull_git_commits), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.pull_git_commits(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PullGitCommitsRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_pull_git_commits_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull_git_commits), "__call__") as call:
        client.pull_git_commits()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PullGitCommitsRequest()


@pytest.mark.asyncio
async def test_pull_git_commits_async(
    transport: str = "grpc_asyncio", request_type=dataform.PullGitCommitsRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull_git_commits), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.pull_git_commits(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PullGitCommitsRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_pull_git_commits_async_from_dict():
    await test_pull_git_commits_async(request_type=dict)


def test_pull_git_commits_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.PullGitCommitsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull_git_commits), "__call__") as call:
        call.return_value = None
        client.pull_git_commits(request)

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
async def test_pull_git_commits_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.PullGitCommitsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull_git_commits), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.pull_git_commits(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.PushGitCommitsRequest,
        dict,
    ],
)
def test_push_git_commits(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.push_git_commits), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.push_git_commits(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PushGitCommitsRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_push_git_commits_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.push_git_commits), "__call__") as call:
        client.push_git_commits()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PushGitCommitsRequest()


@pytest.mark.asyncio
async def test_push_git_commits_async(
    transport: str = "grpc_asyncio", request_type=dataform.PushGitCommitsRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.push_git_commits), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.push_git_commits(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.PushGitCommitsRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_push_git_commits_async_from_dict():
    await test_push_git_commits_async(request_type=dict)


def test_push_git_commits_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.PushGitCommitsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.push_git_commits), "__call__") as call:
        call.return_value = None
        client.push_git_commits(request)

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
async def test_push_git_commits_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.PushGitCommitsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.push_git_commits), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.push_git_commits(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchFileGitStatusesRequest,
        dict,
    ],
)
def test_fetch_file_git_statuses(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_file_git_statuses), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.FetchFileGitStatusesResponse()
        response = client.fetch_file_git_statuses(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileGitStatusesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileGitStatusesResponse)


def test_fetch_file_git_statuses_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_file_git_statuses), "__call__"
    ) as call:
        client.fetch_file_git_statuses()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileGitStatusesRequest()


@pytest.mark.asyncio
async def test_fetch_file_git_statuses_async(
    transport: str = "grpc_asyncio", request_type=dataform.FetchFileGitStatusesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_file_git_statuses), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchFileGitStatusesResponse()
        )
        response = await client.fetch_file_git_statuses(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileGitStatusesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileGitStatusesResponse)


@pytest.mark.asyncio
async def test_fetch_file_git_statuses_async_from_dict():
    await test_fetch_file_git_statuses_async(request_type=dict)


def test_fetch_file_git_statuses_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchFileGitStatusesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_file_git_statuses), "__call__"
    ) as call:
        call.return_value = dataform.FetchFileGitStatusesResponse()
        client.fetch_file_git_statuses(request)

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
async def test_fetch_file_git_statuses_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchFileGitStatusesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_file_git_statuses), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchFileGitStatusesResponse()
        )
        await client.fetch_file_git_statuses(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchGitAheadBehindRequest,
        dict,
    ],
)
def test_fetch_git_ahead_behind(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_git_ahead_behind), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.FetchGitAheadBehindResponse(
            commits_ahead=1358,
            commits_behind=1477,
        )
        response = client.fetch_git_ahead_behind(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchGitAheadBehindRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchGitAheadBehindResponse)
    assert response.commits_ahead == 1358
    assert response.commits_behind == 1477


def test_fetch_git_ahead_behind_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_git_ahead_behind), "__call__"
    ) as call:
        client.fetch_git_ahead_behind()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchGitAheadBehindRequest()


@pytest.mark.asyncio
async def test_fetch_git_ahead_behind_async(
    transport: str = "grpc_asyncio", request_type=dataform.FetchGitAheadBehindRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_git_ahead_behind), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchGitAheadBehindResponse(
                commits_ahead=1358,
                commits_behind=1477,
            )
        )
        response = await client.fetch_git_ahead_behind(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchGitAheadBehindRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchGitAheadBehindResponse)
    assert response.commits_ahead == 1358
    assert response.commits_behind == 1477


@pytest.mark.asyncio
async def test_fetch_git_ahead_behind_async_from_dict():
    await test_fetch_git_ahead_behind_async(request_type=dict)


def test_fetch_git_ahead_behind_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchGitAheadBehindRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_git_ahead_behind), "__call__"
    ) as call:
        call.return_value = dataform.FetchGitAheadBehindResponse()
        client.fetch_git_ahead_behind(request)

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
async def test_fetch_git_ahead_behind_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchGitAheadBehindRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_git_ahead_behind), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchGitAheadBehindResponse()
        )
        await client.fetch_git_ahead_behind(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CommitWorkspaceChangesRequest,
        dict,
    ],
)
def test_commit_workspace_changes(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_workspace_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.commit_workspace_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CommitWorkspaceChangesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_commit_workspace_changes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_workspace_changes), "__call__"
    ) as call:
        client.commit_workspace_changes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CommitWorkspaceChangesRequest()


@pytest.mark.asyncio
async def test_commit_workspace_changes_async(
    transport: str = "grpc_asyncio", request_type=dataform.CommitWorkspaceChangesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_workspace_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.commit_workspace_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CommitWorkspaceChangesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_commit_workspace_changes_async_from_dict():
    await test_commit_workspace_changes_async(request_type=dict)


def test_commit_workspace_changes_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CommitWorkspaceChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_workspace_changes), "__call__"
    ) as call:
        call.return_value = None
        client.commit_workspace_changes(request)

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
async def test_commit_workspace_changes_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CommitWorkspaceChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_workspace_changes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.commit_workspace_changes(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ResetWorkspaceChangesRequest,
        dict,
    ],
)
def test_reset_workspace_changes(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_workspace_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.reset_workspace_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ResetWorkspaceChangesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_reset_workspace_changes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_workspace_changes), "__call__"
    ) as call:
        client.reset_workspace_changes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ResetWorkspaceChangesRequest()


@pytest.mark.asyncio
async def test_reset_workspace_changes_async(
    transport: str = "grpc_asyncio", request_type=dataform.ResetWorkspaceChangesRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_workspace_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.reset_workspace_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ResetWorkspaceChangesRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_reset_workspace_changes_async_from_dict():
    await test_reset_workspace_changes_async(request_type=dict)


def test_reset_workspace_changes_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ResetWorkspaceChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_workspace_changes), "__call__"
    ) as call:
        call.return_value = None
        client.reset_workspace_changes(request)

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
async def test_reset_workspace_changes_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ResetWorkspaceChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_workspace_changes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.reset_workspace_changes(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchFileDiffRequest,
        dict,
    ],
)
def test_fetch_file_diff(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_file_diff), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.FetchFileDiffResponse(
            formatted_diff="formatted_diff_value",
        )
        response = client.fetch_file_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileDiffRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileDiffResponse)
    assert response.formatted_diff == "formatted_diff_value"


def test_fetch_file_diff_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_file_diff), "__call__") as call:
        client.fetch_file_diff()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileDiffRequest()


@pytest.mark.asyncio
async def test_fetch_file_diff_async(
    transport: str = "grpc_asyncio", request_type=dataform.FetchFileDiffRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_file_diff), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchFileDiffResponse(
                formatted_diff="formatted_diff_value",
            )
        )
        response = await client.fetch_file_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.FetchFileDiffRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileDiffResponse)
    assert response.formatted_diff == "formatted_diff_value"


@pytest.mark.asyncio
async def test_fetch_file_diff_async_from_dict():
    await test_fetch_file_diff_async(request_type=dict)


def test_fetch_file_diff_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchFileDiffRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_file_diff), "__call__") as call:
        call.return_value = dataform.FetchFileDiffResponse()
        client.fetch_file_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_file_diff_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.FetchFileDiffRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_file_diff), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.FetchFileDiffResponse()
        )
        await client.fetch_file_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryDirectoryContentsRequest,
        dict,
    ],
)
def test_query_directory_contents(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.QueryDirectoryContentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.query_directory_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryDirectoryContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryDirectoryContentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_directory_contents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        client.query_directory_contents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryDirectoryContentsRequest()


@pytest.mark.asyncio
async def test_query_directory_contents_async(
    transport: str = "grpc_asyncio", request_type=dataform.QueryDirectoryContentsRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryDirectoryContentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.query_directory_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryDirectoryContentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryDirectoryContentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_query_directory_contents_async_from_dict():
    await test_query_directory_contents_async(request_type=dict)


def test_query_directory_contents_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryDirectoryContentsRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        call.return_value = dataform.QueryDirectoryContentsResponse()
        client.query_directory_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_query_directory_contents_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryDirectoryContentsRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryDirectoryContentsResponse()
        )
        await client.query_directory_contents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


def test_query_directory_contents_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[],
                next_page_token="def",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("workspace", ""),)),
        )
        pager = client.query_directory_contents(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, dataform.QueryDirectoryContentsResponse.DirectoryEntry)
            for i in results
        )


def test_query_directory_contents_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[],
                next_page_token="def",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.query_directory_contents(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_query_directory_contents_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[],
                next_page_token="def",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.query_directory_contents(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, dataform.QueryDirectoryContentsResponse.DirectoryEntry)
            for i in responses
        )


@pytest.mark.asyncio
async def test_query_directory_contents_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_directory_contents),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[],
                next_page_token="def",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.query_directory_contents(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MakeDirectoryRequest,
        dict,
    ],
)
def test_make_directory(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.make_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.MakeDirectoryResponse()
        response = client.make_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MakeDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MakeDirectoryResponse)


def test_make_directory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.make_directory), "__call__") as call:
        client.make_directory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MakeDirectoryRequest()


@pytest.mark.asyncio
async def test_make_directory_async(
    transport: str = "grpc_asyncio", request_type=dataform.MakeDirectoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.make_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MakeDirectoryResponse()
        )
        response = await client.make_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MakeDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MakeDirectoryResponse)


@pytest.mark.asyncio
async def test_make_directory_async_from_dict():
    await test_make_directory_async(request_type=dict)


def test_make_directory_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MakeDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.make_directory), "__call__") as call:
        call.return_value = dataform.MakeDirectoryResponse()
        client.make_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_make_directory_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MakeDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.make_directory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MakeDirectoryResponse()
        )
        await client.make_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.RemoveDirectoryRequest,
        dict,
    ],
)
def test_remove_directory(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.remove_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_directory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_directory), "__call__") as call:
        client.remove_directory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveDirectoryRequest()


@pytest.mark.asyncio
async def test_remove_directory_async(
    transport: str = "grpc_asyncio", request_type=dataform.RemoveDirectoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.remove_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_remove_directory_async_from_dict():
    await test_remove_directory_async(request_type=dict)


def test_remove_directory_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.RemoveDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_directory), "__call__") as call:
        call.return_value = None
        client.remove_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_directory_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.RemoveDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_directory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.remove_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MoveDirectoryRequest,
        dict,
    ],
)
def test_move_directory(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.MoveDirectoryResponse()
        response = client.move_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveDirectoryResponse)


def test_move_directory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_directory), "__call__") as call:
        client.move_directory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveDirectoryRequest()


@pytest.mark.asyncio
async def test_move_directory_async(
    transport: str = "grpc_asyncio", request_type=dataform.MoveDirectoryRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_directory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MoveDirectoryResponse()
        )
        response = await client.move_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveDirectoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveDirectoryResponse)


@pytest.mark.asyncio
async def test_move_directory_async_from_dict():
    await test_move_directory_async(request_type=dict)


def test_move_directory_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MoveDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_directory), "__call__") as call:
        call.return_value = dataform.MoveDirectoryResponse()
        client.move_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_move_directory_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MoveDirectoryRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_directory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MoveDirectoryResponse()
        )
        await client.move_directory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ReadFileRequest,
        dict,
    ],
)
def test_read_file(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ReadFileResponse(
            file_contents=b"file_contents_blob",
        )
        response = client.read_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ReadFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.ReadFileResponse)
    assert response.file_contents == b"file_contents_blob"


def test_read_file_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_file), "__call__") as call:
        client.read_file()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ReadFileRequest()


@pytest.mark.asyncio
async def test_read_file_async(
    transport: str = "grpc_asyncio", request_type=dataform.ReadFileRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ReadFileResponse(
                file_contents=b"file_contents_blob",
            )
        )
        response = await client.read_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ReadFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.ReadFileResponse)
    assert response.file_contents == b"file_contents_blob"


@pytest.mark.asyncio
async def test_read_file_async_from_dict():
    await test_read_file_async(request_type=dict)


def test_read_file_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ReadFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_file), "__call__") as call:
        call.return_value = dataform.ReadFileResponse()
        client.read_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_file_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ReadFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_file), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ReadFileResponse()
        )
        await client.read_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.RemoveFileRequest,
        dict,
    ],
)
def test_remove_file(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.remove_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveFileRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_file_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_file), "__call__") as call:
        client.remove_file()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveFileRequest()


@pytest.mark.asyncio
async def test_remove_file_async(
    transport: str = "grpc_asyncio", request_type=dataform.RemoveFileRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.remove_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.RemoveFileRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_remove_file_async_from_dict():
    await test_remove_file_async(request_type=dict)


def test_remove_file_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.RemoveFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_file), "__call__") as call:
        call.return_value = None
        client.remove_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_file_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.RemoveFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.remove_file), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.remove_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MoveFileRequest,
        dict,
    ],
)
def test_move_file(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.MoveFileResponse()
        response = client.move_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveFileResponse)


def test_move_file_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_file), "__call__") as call:
        client.move_file()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveFileRequest()


@pytest.mark.asyncio
async def test_move_file_async(
    transport: str = "grpc_asyncio", request_type=dataform.MoveFileRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MoveFileResponse()
        )
        response = await client.move_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.MoveFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveFileResponse)


@pytest.mark.asyncio
async def test_move_file_async_from_dict():
    await test_move_file_async(request_type=dict)


def test_move_file_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MoveFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_file), "__call__") as call:
        call.return_value = dataform.MoveFileResponse()
        client.move_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_move_file_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.MoveFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.move_file), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.MoveFileResponse()
        )
        await client.move_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.WriteFileRequest,
        dict,
    ],
)
def test_write_file(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WriteFileResponse()
        response = client.write_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.WriteFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WriteFileResponse)


def test_write_file_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_file), "__call__") as call:
        client.write_file()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.WriteFileRequest()


@pytest.mark.asyncio
async def test_write_file_async(
    transport: str = "grpc_asyncio", request_type=dataform.WriteFileRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WriteFileResponse()
        )
        response = await client.write_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.WriteFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WriteFileResponse)


@pytest.mark.asyncio
async def test_write_file_async_from_dict():
    await test_write_file_async(request_type=dict)


def test_write_file_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.WriteFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_file), "__call__") as call:
        call.return_value = dataform.WriteFileResponse()
        client.write_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_write_file_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.WriteFileRequest()

    request.workspace = "workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_file), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WriteFileResponse()
        )
        await client.write_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "workspace=workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListCompilationResultsRequest,
        dict,
    ],
)
def test_list_compilation_results(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListCompilationResultsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_compilation_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListCompilationResultsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCompilationResultsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_compilation_results_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        client.list_compilation_results()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListCompilationResultsRequest()


@pytest.mark.asyncio
async def test_list_compilation_results_async(
    transport: str = "grpc_asyncio", request_type=dataform.ListCompilationResultsRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListCompilationResultsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_compilation_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListCompilationResultsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCompilationResultsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_compilation_results_async_from_dict():
    await test_list_compilation_results_async(request_type=dict)


def test_list_compilation_results_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListCompilationResultsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        call.return_value = dataform.ListCompilationResultsResponse()
        client.list_compilation_results(request)

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
async def test_list_compilation_results_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListCompilationResultsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListCompilationResultsResponse()
        )
        await client.list_compilation_results(request)

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


def test_list_compilation_results_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListCompilationResultsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_compilation_results(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_compilation_results_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_compilation_results(
            dataform.ListCompilationResultsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_compilation_results_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListCompilationResultsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListCompilationResultsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_compilation_results(
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
async def test_list_compilation_results_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_compilation_results(
            dataform.ListCompilationResultsRequest(),
            parent="parent_value",
        )


def test_list_compilation_results_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
                next_page_token="abc",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[],
                next_page_token="def",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_compilation_results(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.CompilationResult) for i in results)


def test_list_compilation_results_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
                next_page_token="abc",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[],
                next_page_token="def",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_compilation_results(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_compilation_results_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
                next_page_token="abc",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[],
                next_page_token="def",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_compilation_results(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.CompilationResult) for i in responses)


@pytest.mark.asyncio
async def test_list_compilation_results_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_compilation_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
                next_page_token="abc",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[],
                next_page_token="def",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_compilation_results(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetCompilationResultRequest,
        dict,
    ],
)
def test_get_compilation_result(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult(
            name="name_value",
            dataform_core_version="dataform_core_version_value",
            git_commitish="git_commitish_value",
        )
        response = client.get_compilation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetCompilationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


def test_get_compilation_result_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        client.get_compilation_result()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetCompilationResultRequest()


@pytest.mark.asyncio
async def test_get_compilation_result_async(
    transport: str = "grpc_asyncio", request_type=dataform.GetCompilationResultRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult(
                name="name_value",
                dataform_core_version="dataform_core_version_value",
            )
        )
        response = await client.get_compilation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetCompilationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


@pytest.mark.asyncio
async def test_get_compilation_result_async_from_dict():
    await test_get_compilation_result_async(request_type=dict)


def test_get_compilation_result_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetCompilationResultRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        call.return_value = dataform.CompilationResult()
        client.get_compilation_result(request)

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
async def test_get_compilation_result_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetCompilationResultRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult()
        )
        await client.get_compilation_result(request)

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


def test_get_compilation_result_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_compilation_result(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_compilation_result_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_compilation_result(
            dataform.GetCompilationResultRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_compilation_result_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_compilation_result(
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
async def test_get_compilation_result_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_compilation_result(
            dataform.GetCompilationResultRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateCompilationResultRequest,
        dict,
    ],
)
def test_create_compilation_result(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult(
            name="name_value",
            dataform_core_version="dataform_core_version_value",
            git_commitish="git_commitish_value",
        )
        response = client.create_compilation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateCompilationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


def test_create_compilation_result_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        client.create_compilation_result()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateCompilationResultRequest()


@pytest.mark.asyncio
async def test_create_compilation_result_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.CreateCompilationResultRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult(
                name="name_value",
                dataform_core_version="dataform_core_version_value",
            )
        )
        response = await client.create_compilation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateCompilationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


@pytest.mark.asyncio
async def test_create_compilation_result_async_from_dict():
    await test_create_compilation_result_async(request_type=dict)


def test_create_compilation_result_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateCompilationResultRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        call.return_value = dataform.CompilationResult()
        client.create_compilation_result(request)

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
async def test_create_compilation_result_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateCompilationResultRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult()
        )
        await client.create_compilation_result(request)

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


def test_create_compilation_result_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_compilation_result(
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].compilation_result
        mock_val = dataform.CompilationResult(name="name_value")
        assert arg == mock_val


def test_create_compilation_result_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_compilation_result(
            dataform.CreateCompilationResultRequest(),
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_compilation_result_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_compilation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.CompilationResult()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.CompilationResult()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_compilation_result(
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].compilation_result
        mock_val = dataform.CompilationResult(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_compilation_result_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_compilation_result(
            dataform.CreateCompilationResultRequest(),
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryCompilationResultActionsRequest,
        dict,
    ],
)
def test_query_compilation_result_actions(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.QueryCompilationResultActionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.query_compilation_result_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryCompilationResultActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryCompilationResultActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_compilation_result_actions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        client.query_compilation_result_actions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryCompilationResultActionsRequest()


@pytest.mark.asyncio
async def test_query_compilation_result_actions_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.QueryCompilationResultActionsRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryCompilationResultActionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.query_compilation_result_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryCompilationResultActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryCompilationResultActionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_query_compilation_result_actions_async_from_dict():
    await test_query_compilation_result_actions_async(request_type=dict)


def test_query_compilation_result_actions_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryCompilationResultActionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        call.return_value = dataform.QueryCompilationResultActionsResponse()
        client.query_compilation_result_actions(request)

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
async def test_query_compilation_result_actions_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryCompilationResultActionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryCompilationResultActionsResponse()
        )
        await client.query_compilation_result_actions(request)

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


def test_query_compilation_result_actions_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[],
                next_page_token="def",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.query_compilation_result_actions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.CompilationResultAction) for i in results)


def test_query_compilation_result_actions_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[],
                next_page_token="def",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.query_compilation_result_actions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_query_compilation_result_actions_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[],
                next_page_token="def",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.query_compilation_result_actions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.CompilationResultAction) for i in responses)


@pytest.mark.asyncio
async def test_query_compilation_result_actions_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_compilation_result_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[],
                next_page_token="def",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.query_compilation_result_actions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListWorkflowInvocationsRequest,
        dict,
    ],
)
def test_list_workflow_invocations(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkflowInvocationsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_workflow_invocations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkflowInvocationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowInvocationsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workflow_invocations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        client.list_workflow_invocations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkflowInvocationsRequest()


@pytest.mark.asyncio
async def test_list_workflow_invocations_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.ListWorkflowInvocationsRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkflowInvocationsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_workflow_invocations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.ListWorkflowInvocationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowInvocationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_workflow_invocations_async_from_dict():
    await test_list_workflow_invocations_async(request_type=dict)


def test_list_workflow_invocations_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListWorkflowInvocationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        call.return_value = dataform.ListWorkflowInvocationsResponse()
        client.list_workflow_invocations(request)

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
async def test_list_workflow_invocations_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.ListWorkflowInvocationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkflowInvocationsResponse()
        )
        await client.list_workflow_invocations(request)

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


def test_list_workflow_invocations_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkflowInvocationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_workflow_invocations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_workflow_invocations_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workflow_invocations(
            dataform.ListWorkflowInvocationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_workflow_invocations_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.ListWorkflowInvocationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.ListWorkflowInvocationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_workflow_invocations(
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
async def test_list_workflow_invocations_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_workflow_invocations(
            dataform.ListWorkflowInvocationsRequest(),
            parent="parent_value",
        )


def test_list_workflow_invocations_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[],
                next_page_token="def",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_workflow_invocations(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.WorkflowInvocation) for i in results)


def test_list_workflow_invocations_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[],
                next_page_token="def",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_workflow_invocations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_workflow_invocations_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[],
                next_page_token="def",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_workflow_invocations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.WorkflowInvocation) for i in responses)


@pytest.mark.asyncio
async def test_list_workflow_invocations_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_invocations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[],
                next_page_token="def",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_workflow_invocations(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetWorkflowInvocationRequest,
        dict,
    ],
)
def test_get_workflow_invocation(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation(
            name="name_value",
            compilation_result="compilation_result_value",
            state=dataform.WorkflowInvocation.State.RUNNING,
        )
        response = client.get_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


def test_get_workflow_invocation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        client.get_workflow_invocation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkflowInvocationRequest()


@pytest.mark.asyncio
async def test_get_workflow_invocation_async(
    transport: str = "grpc_asyncio", request_type=dataform.GetWorkflowInvocationRequest
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation(
                name="name_value",
                compilation_result="compilation_result_value",
                state=dataform.WorkflowInvocation.State.RUNNING,
            )
        )
        response = await client.get_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.GetWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


@pytest.mark.asyncio
async def test_get_workflow_invocation_async_from_dict():
    await test_get_workflow_invocation_async(request_type=dict)


def test_get_workflow_invocation_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        call.return_value = dataform.WorkflowInvocation()
        client.get_workflow_invocation(request)

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
async def test_get_workflow_invocation_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.GetWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation()
        )
        await client.get_workflow_invocation(request)

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


def test_get_workflow_invocation_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_workflow_invocation(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_workflow_invocation_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workflow_invocation(
            dataform.GetWorkflowInvocationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_workflow_invocation_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_workflow_invocation(
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
async def test_get_workflow_invocation_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_workflow_invocation(
            dataform.GetWorkflowInvocationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateWorkflowInvocationRequest,
        dict,
    ],
)
def test_create_workflow_invocation(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation(
            name="name_value",
            compilation_result="compilation_result_value",
            state=dataform.WorkflowInvocation.State.RUNNING,
        )
        response = client.create_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


def test_create_workflow_invocation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        client.create_workflow_invocation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkflowInvocationRequest()


@pytest.mark.asyncio
async def test_create_workflow_invocation_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.CreateWorkflowInvocationRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation(
                name="name_value",
                compilation_result="compilation_result_value",
                state=dataform.WorkflowInvocation.State.RUNNING,
            )
        )
        response = await client.create_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CreateWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


@pytest.mark.asyncio
async def test_create_workflow_invocation_async_from_dict():
    await test_create_workflow_invocation_async(request_type=dict)


def test_create_workflow_invocation_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateWorkflowInvocationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        call.return_value = dataform.WorkflowInvocation()
        client.create_workflow_invocation(request)

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
async def test_create_workflow_invocation_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CreateWorkflowInvocationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation()
        )
        await client.create_workflow_invocation(request)

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


def test_create_workflow_invocation_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_workflow_invocation(
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].workflow_invocation
        mock_val = dataform.WorkflowInvocation(name="name_value")
        assert arg == mock_val


def test_create_workflow_invocation_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workflow_invocation(
            dataform.CreateWorkflowInvocationRequest(),
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_workflow_invocation_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.WorkflowInvocation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.WorkflowInvocation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_workflow_invocation(
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].workflow_invocation
        mock_val = dataform.WorkflowInvocation(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_workflow_invocation_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_workflow_invocation(
            dataform.CreateWorkflowInvocationRequest(),
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteWorkflowInvocationRequest,
        dict,
    ],
)
def test_delete_workflow_invocation(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workflow_invocation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        client.delete_workflow_invocation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkflowInvocationRequest()


@pytest.mark.asyncio
async def test_delete_workflow_invocation_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.DeleteWorkflowInvocationRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.DeleteWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_workflow_invocation_async_from_dict():
    await test_delete_workflow_invocation_async(request_type=dict)


def test_delete_workflow_invocation_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        call.return_value = None
        client.delete_workflow_invocation(request)

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
async def test_delete_workflow_invocation_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.DeleteWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_workflow_invocation(request)

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


def test_delete_workflow_invocation_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_workflow_invocation(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_workflow_invocation_flattened_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workflow_invocation(
            dataform.DeleteWorkflowInvocationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_workflow_invocation_flattened_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_workflow_invocation(
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
async def test_delete_workflow_invocation_flattened_error_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_workflow_invocation(
            dataform.DeleteWorkflowInvocationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CancelWorkflowInvocationRequest,
        dict,
    ],
)
def test_cancel_workflow_invocation(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CancelWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_workflow_invocation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_workflow_invocation), "__call__"
    ) as call:
        client.cancel_workflow_invocation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CancelWorkflowInvocationRequest()


@pytest.mark.asyncio
async def test_cancel_workflow_invocation_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.CancelWorkflowInvocationRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_workflow_invocation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_workflow_invocation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.CancelWorkflowInvocationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_workflow_invocation_async_from_dict():
    await test_cancel_workflow_invocation_async(request_type=dict)


def test_cancel_workflow_invocation_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CancelWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_workflow_invocation), "__call__"
    ) as call:
        call.return_value = None
        client.cancel_workflow_invocation(request)

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
async def test_cancel_workflow_invocation_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.CancelWorkflowInvocationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_workflow_invocation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_workflow_invocation(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryWorkflowInvocationActionsRequest,
        dict,
    ],
)
def test_query_workflow_invocation_actions(request_type, transport: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataform.QueryWorkflowInvocationActionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.query_workflow_invocation_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryWorkflowInvocationActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryWorkflowInvocationActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_workflow_invocation_actions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        client.query_workflow_invocation_actions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryWorkflowInvocationActionsRequest()


@pytest.mark.asyncio
async def test_query_workflow_invocation_actions_async(
    transport: str = "grpc_asyncio",
    request_type=dataform.QueryWorkflowInvocationActionsRequest,
):
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryWorkflowInvocationActionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.query_workflow_invocation_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dataform.QueryWorkflowInvocationActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryWorkflowInvocationActionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_query_workflow_invocation_actions_async_from_dict():
    await test_query_workflow_invocation_actions_async(request_type=dict)


def test_query_workflow_invocation_actions_field_headers():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryWorkflowInvocationActionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        call.return_value = dataform.QueryWorkflowInvocationActionsResponse()
        client.query_workflow_invocation_actions(request)

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
async def test_query_workflow_invocation_actions_field_headers_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dataform.QueryWorkflowInvocationActionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataform.QueryWorkflowInvocationActionsResponse()
        )
        await client.query_workflow_invocation_actions(request)

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


def test_query_workflow_invocation_actions_pager(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[],
                next_page_token="def",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.query_workflow_invocation_actions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.WorkflowInvocationAction) for i in results)


def test_query_workflow_invocation_actions_pages(transport_name: str = "grpc"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[],
                next_page_token="def",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.query_workflow_invocation_actions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_query_workflow_invocation_actions_async_pager():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[],
                next_page_token="def",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.query_workflow_invocation_actions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataform.WorkflowInvocationAction) for i in responses)


@pytest.mark.asyncio
async def test_query_workflow_invocation_actions_async_pages():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_workflow_invocation_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[],
                next_page_token="def",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.query_workflow_invocation_actions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListRepositoriesRequest,
        dict,
    ],
)
def test_list_repositories_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListRepositoriesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListRepositoriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_repositories(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_repositories_rest_required_fields(
    request_type=dataform.ListRepositoriesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).list_repositories._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_repositories._get_unset_required_fields(jsonified_request)
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

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.ListRepositoriesResponse()
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

            pb_return_value = dataform.ListRepositoriesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_repositories(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_repositories_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_repositories._get_unset_required_fields({})
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
def test_list_repositories_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_list_repositories"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_list_repositories"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.ListRepositoriesRequest.pb(
            dataform.ListRepositoriesRequest()
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
        req.return_value._content = dataform.ListRepositoriesResponse.to_json(
            dataform.ListRepositoriesResponse()
        )

        request = dataform.ListRepositoriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.ListRepositoriesResponse()

        client.list_repositories(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_repositories_rest_bad_request(
    transport: str = "rest", request_type=dataform.ListRepositoriesRequest
):
    client = DataformClient(
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
        client.list_repositories(request)


def test_list_repositories_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListRepositoriesResponse()

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
        pb_return_value = dataform.ListRepositoriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_repositories(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*}/repositories"
            % client.transport._host,
            args[1],
        )


def test_list_repositories_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_repositories(
            dataform.ListRepositoriesRequest(),
            parent="parent_value",
        )


def test_list_repositories_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                    dataform.Repository(),
                ],
                next_page_token="abc",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListRepositoriesResponse(
                repositories=[
                    dataform.Repository(),
                    dataform.Repository(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(dataform.ListRepositoriesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_repositories(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.Repository) for i in results)

        pages = list(client.list_repositories(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetRepositoryRequest,
        dict,
    ],
)
def test_get_repository_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_repository(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_get_repository_rest_required_fields(
    request_type=dataform.GetRepositoryRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).get_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.Repository()
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

            pb_return_value = dataform.Repository.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_repository_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_repository_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_get_repository"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_get_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.GetRepositoryRequest.pb(dataform.GetRepositoryRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.Repository.to_json(dataform.Repository())

        request = dataform.GetRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.Repository()

        client.get_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_repository_rest_bad_request(
    transport: str = "rest", request_type=dataform.GetRepositoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.get_repository(request)


def test_get_repository_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_get_repository_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_repository(
            dataform.GetRepositoryRequest(),
            name="name_value",
        )


def test_get_repository_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateRepositoryRequest,
        dict,
    ],
)
def test_create_repository_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["repository"] = {
        "name": "name_value",
        "git_remote_settings": {
            "url": "url_value",
            "default_branch": "default_branch_value",
            "authentication_token_secret_version": "authentication_token_secret_version_value",
            "token_status": 1,
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_repository(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_create_repository_rest_required_fields(
    request_type=dataform.CreateRepositoryRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["repository_id"] = ""
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
    assert "repositoryId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "repositoryId" in jsonified_request
    assert jsonified_request["repositoryId"] == request_init["repository_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["repositoryId"] = "repository_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_repository._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("repository_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "repositoryId" in jsonified_request
    assert jsonified_request["repositoryId"] == "repository_id_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.Repository()
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

            pb_return_value = dataform.Repository.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_repository(request)

            expected_params = [
                (
                    "repositoryId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_repository_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_repository._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("repositoryId",))
        & set(
            (
                "parent",
                "repository",
                "repositoryId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_repository_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_create_repository"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_create_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.CreateRepositoryRequest.pb(
            dataform.CreateRepositoryRequest()
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
        req.return_value._content = dataform.Repository.to_json(dataform.Repository())

        request = dataform.CreateRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.Repository()

        client.create_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_repository_rest_bad_request(
    transport: str = "rest", request_type=dataform.CreateRepositoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["repository"] = {
        "name": "name_value",
        "git_remote_settings": {
            "url": "url_value",
            "default_branch": "default_branch_value",
            "authentication_token_secret_version": "authentication_token_secret_version_value",
            "token_status": 1,
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
        client.create_repository(request)


def test_create_repository_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*}/repositories"
            % client.transport._host,
            args[1],
        )


def test_create_repository_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_repository(
            dataform.CreateRepositoryRequest(),
            parent="parent_value",
            repository=dataform.Repository(name="name_value"),
            repository_id="repository_id_value",
        )


def test_create_repository_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.UpdateRepositoryRequest,
        dict,
    ],
)
def test_update_repository_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "repository": {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }
    }
    request_init["repository"] = {
        "name": "projects/sample1/locations/sample2/repositories/sample3",
        "git_remote_settings": {
            "url": "url_value",
            "default_branch": "default_branch_value",
            "authentication_token_secret_version": "authentication_token_secret_version_value",
            "token_status": 1,
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_repository(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Repository)
    assert response.name == "name_value"


def test_update_repository_rest_required_fields(
    request_type=dataform.UpdateRepositoryRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).update_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_repository._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.Repository()
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

            pb_return_value = dataform.Repository.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_repository_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("repository",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_repository_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_update_repository"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_update_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.UpdateRepositoryRequest.pb(
            dataform.UpdateRepositoryRequest()
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
        req.return_value._content = dataform.Repository.to_json(dataform.Repository())

        request = dataform.UpdateRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.Repository()

        client.update_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_repository_rest_bad_request(
    transport: str = "rest", request_type=dataform.UpdateRepositoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "repository": {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }
    }
    request_init["repository"] = {
        "name": "projects/sample1/locations/sample2/repositories/sample3",
        "git_remote_settings": {
            "url": "url_value",
            "default_branch": "default_branch_value",
            "authentication_token_secret_version": "authentication_token_secret_version_value",
            "token_status": 1,
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
        client.update_repository(request)


def test_update_repository_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Repository()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "repository": {
                "name": "projects/sample1/locations/sample2/repositories/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{repository.name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_update_repository_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_repository(
            dataform.UpdateRepositoryRequest(),
            repository=dataform.Repository(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_repository_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteRepositoryRequest,
        dict,
    ],
)
def test_delete_repository_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_repository(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_repository_rest_required_fields(
    request_type=dataform.DeleteRepositoryRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).delete_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_repository._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_repository_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_repository_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_delete_repository"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.DeleteRepositoryRequest.pb(
            dataform.DeleteRepositoryRequest()
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

        request = dataform.DeleteRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_repository_rest_bad_request(
    transport: str = "rest", request_type=dataform.DeleteRepositoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.delete_repository(request)


def test_delete_repository_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_repository_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_repository(
            dataform.DeleteRepositoryRequest(),
            name="name_value",
        )


def test_delete_repository_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchRemoteBranchesRequest,
        dict,
    ],
)
def test_fetch_remote_branches_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.FetchRemoteBranchesResponse(
            branches=["branches_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.FetchRemoteBranchesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_remote_branches(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchRemoteBranchesResponse)
    assert response.branches == ["branches_value"]


def test_fetch_remote_branches_rest_required_fields(
    request_type=dataform.FetchRemoteBranchesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).fetch_remote_branches._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_remote_branches._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.FetchRemoteBranchesResponse()
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

            pb_return_value = dataform.FetchRemoteBranchesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_remote_branches(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_remote_branches_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_remote_branches._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_remote_branches_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_fetch_remote_branches"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_fetch_remote_branches"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.FetchRemoteBranchesRequest.pb(
            dataform.FetchRemoteBranchesRequest()
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
        req.return_value._content = dataform.FetchRemoteBranchesResponse.to_json(
            dataform.FetchRemoteBranchesResponse()
        )

        request = dataform.FetchRemoteBranchesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.FetchRemoteBranchesResponse()

        client.fetch_remote_branches(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_remote_branches_rest_bad_request(
    transport: str = "rest", request_type=dataform.FetchRemoteBranchesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.fetch_remote_branches(request)


def test_fetch_remote_branches_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListWorkspacesRequest,
        dict,
    ],
)
def test_list_workspaces_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListWorkspacesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListWorkspacesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_workspaces(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkspacesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workspaces_rest_required_fields(
    request_type=dataform.ListWorkspacesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).list_workspaces._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_workspaces._get_unset_required_fields(jsonified_request)
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

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.ListWorkspacesResponse()
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

            pb_return_value = dataform.ListWorkspacesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_workspaces(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_workspaces_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_workspaces._get_unset_required_fields({})
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
def test_list_workspaces_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_list_workspaces"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_list_workspaces"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.ListWorkspacesRequest.pb(dataform.ListWorkspacesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.ListWorkspacesResponse.to_json(
            dataform.ListWorkspacesResponse()
        )

        request = dataform.ListWorkspacesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.ListWorkspacesResponse()

        client.list_workspaces(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_workspaces_rest_bad_request(
    transport: str = "rest", request_type=dataform.ListWorkspacesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_workspaces(request)


def test_list_workspaces_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListWorkspacesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListWorkspacesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_workspaces(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/workspaces"
            % client.transport._host,
            args[1],
        )


def test_list_workspaces_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workspaces(
            dataform.ListWorkspacesRequest(),
            parent="parent_value",
        )


def test_list_workspaces_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[],
                next_page_token="def",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkspacesResponse(
                workspaces=[
                    dataform.Workspace(),
                    dataform.Workspace(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(dataform.ListWorkspacesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_workspaces(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.Workspace) for i in results)

        pages = list(client.list_workspaces(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetWorkspaceRequest,
        dict,
    ],
)
def test_get_workspace_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Workspace(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Workspace.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_workspace(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


def test_get_workspace_rest_required_fields(request_type=dataform.GetWorkspaceRequest):
    transport_class = transports.DataformRestTransport

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
    ).get_workspace._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_workspace._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.Workspace()
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

            pb_return_value = dataform.Workspace.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_workspace(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_workspace_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_workspace._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_workspace_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_get_workspace"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_get_workspace"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.GetWorkspaceRequest.pb(dataform.GetWorkspaceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.Workspace.to_json(dataform.Workspace())

        request = dataform.GetWorkspaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.Workspace()

        client.get_workspace(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_workspace_rest_bad_request(
    transport: str = "rest", request_type=dataform.GetWorkspaceRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.get_workspace(request)


def test_get_workspace_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Workspace()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Workspace.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_workspace(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}"
            % client.transport._host,
            args[1],
        )


def test_get_workspace_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workspace(
            dataform.GetWorkspaceRequest(),
            name="name_value",
        )


def test_get_workspace_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateWorkspaceRequest,
        dict,
    ],
)
def test_create_workspace_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["workspace"] = {"name": "name_value"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Workspace(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Workspace.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_workspace(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.Workspace)
    assert response.name == "name_value"


def test_create_workspace_rest_required_fields(
    request_type=dataform.CreateWorkspaceRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["workspace_id"] = ""
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
    assert "workspaceId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_workspace._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "workspaceId" in jsonified_request
    assert jsonified_request["workspaceId"] == request_init["workspace_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["workspaceId"] = "workspace_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_workspace._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("workspace_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "workspaceId" in jsonified_request
    assert jsonified_request["workspaceId"] == "workspace_id_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.Workspace()
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

            pb_return_value = dataform.Workspace.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_workspace(request)

            expected_params = [
                (
                    "workspaceId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_workspace_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_workspace._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("workspaceId",))
        & set(
            (
                "parent",
                "workspace",
                "workspaceId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_workspace_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_create_workspace"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_create_workspace"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.CreateWorkspaceRequest.pb(
            dataform.CreateWorkspaceRequest()
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
        req.return_value._content = dataform.Workspace.to_json(dataform.Workspace())

        request = dataform.CreateWorkspaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.Workspace()

        client.create_workspace(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_workspace_rest_bad_request(
    transport: str = "rest", request_type=dataform.CreateWorkspaceRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["workspace"] = {"name": "name_value"}
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
        client.create_workspace(request)


def test_create_workspace_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.Workspace()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.Workspace.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_workspace(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/workspaces"
            % client.transport._host,
            args[1],
        )


def test_create_workspace_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workspace(
            dataform.CreateWorkspaceRequest(),
            parent="parent_value",
            workspace=dataform.Workspace(name="name_value"),
            workspace_id="workspace_id_value",
        )


def test_create_workspace_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteWorkspaceRequest,
        dict,
    ],
)
def test_delete_workspace_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_workspace(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workspace_rest_required_fields(
    request_type=dataform.DeleteWorkspaceRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).delete_workspace._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_workspace._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_workspace(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_workspace_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_workspace._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_workspace_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_delete_workspace"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.DeleteWorkspaceRequest.pb(
            dataform.DeleteWorkspaceRequest()
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

        request = dataform.DeleteWorkspaceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_workspace(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_workspace_rest_bad_request(
    transport: str = "rest", request_type=dataform.DeleteWorkspaceRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.delete_workspace(request)


def test_delete_workspace_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_workspace(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*/workspaces/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_workspace_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workspace(
            dataform.DeleteWorkspaceRequest(),
            name="name_value",
        )


def test_delete_workspace_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.InstallNpmPackagesRequest,
        dict,
    ],
)
def test_install_npm_packages_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.InstallNpmPackagesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.InstallNpmPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.install_npm_packages(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.InstallNpmPackagesResponse)


def test_install_npm_packages_rest_required_fields(
    request_type=dataform.InstallNpmPackagesRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
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
    ).install_npm_packages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).install_npm_packages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.InstallNpmPackagesResponse()
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

            pb_return_value = dataform.InstallNpmPackagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.install_npm_packages(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_install_npm_packages_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.install_npm_packages._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("workspace",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_install_npm_packages_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_install_npm_packages"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_install_npm_packages"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.InstallNpmPackagesRequest.pb(
            dataform.InstallNpmPackagesRequest()
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
        req.return_value._content = dataform.InstallNpmPackagesResponse.to_json(
            dataform.InstallNpmPackagesResponse()
        )

        request = dataform.InstallNpmPackagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.InstallNpmPackagesResponse()

        client.install_npm_packages(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_install_npm_packages_rest_bad_request(
    transport: str = "rest", request_type=dataform.InstallNpmPackagesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.install_npm_packages(request)


def test_install_npm_packages_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.PullGitCommitsRequest,
        dict,
    ],
)
def test_pull_git_commits_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.pull_git_commits(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_pull_git_commits_rest_required_fields(
    request_type=dataform.PullGitCommitsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).pull_git_commits._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).pull_git_commits._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.pull_git_commits(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_pull_git_commits_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.pull_git_commits._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "author",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_pull_git_commits_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_pull_git_commits"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.PullGitCommitsRequest.pb(dataform.PullGitCommitsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = dataform.PullGitCommitsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.pull_git_commits(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_pull_git_commits_rest_bad_request(
    transport: str = "rest", request_type=dataform.PullGitCommitsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.pull_git_commits(request)


def test_pull_git_commits_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.PushGitCommitsRequest,
        dict,
    ],
)
def test_push_git_commits_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.push_git_commits(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_push_git_commits_rest_required_fields(
    request_type=dataform.PushGitCommitsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).push_git_commits._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).push_git_commits._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.push_git_commits(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_push_git_commits_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.push_git_commits._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_push_git_commits_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_push_git_commits"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.PushGitCommitsRequest.pb(dataform.PushGitCommitsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = dataform.PushGitCommitsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.push_git_commits(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_push_git_commits_rest_bad_request(
    transport: str = "rest", request_type=dataform.PushGitCommitsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.push_git_commits(request)


def test_push_git_commits_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchFileGitStatusesRequest,
        dict,
    ],
)
def test_fetch_file_git_statuses_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.FetchFileGitStatusesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.FetchFileGitStatusesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_file_git_statuses(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileGitStatusesResponse)


def test_fetch_file_git_statuses_rest_required_fields(
    request_type=dataform.FetchFileGitStatusesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).fetch_file_git_statuses._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_file_git_statuses._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.FetchFileGitStatusesResponse()
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

            pb_return_value = dataform.FetchFileGitStatusesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_file_git_statuses(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_file_git_statuses_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_file_git_statuses._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_file_git_statuses_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_fetch_file_git_statuses"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_fetch_file_git_statuses"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.FetchFileGitStatusesRequest.pb(
            dataform.FetchFileGitStatusesRequest()
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
        req.return_value._content = dataform.FetchFileGitStatusesResponse.to_json(
            dataform.FetchFileGitStatusesResponse()
        )

        request = dataform.FetchFileGitStatusesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.FetchFileGitStatusesResponse()

        client.fetch_file_git_statuses(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_file_git_statuses_rest_bad_request(
    transport: str = "rest", request_type=dataform.FetchFileGitStatusesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.fetch_file_git_statuses(request)


def test_fetch_file_git_statuses_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchGitAheadBehindRequest,
        dict,
    ],
)
def test_fetch_git_ahead_behind_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.FetchGitAheadBehindResponse(
            commits_ahead=1358,
            commits_behind=1477,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.FetchGitAheadBehindResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_git_ahead_behind(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchGitAheadBehindResponse)
    assert response.commits_ahead == 1358
    assert response.commits_behind == 1477


def test_fetch_git_ahead_behind_rest_required_fields(
    request_type=dataform.FetchGitAheadBehindRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).fetch_git_ahead_behind._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_git_ahead_behind._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("remote_branch",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.FetchGitAheadBehindResponse()
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

            pb_return_value = dataform.FetchGitAheadBehindResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_git_ahead_behind(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_git_ahead_behind_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_git_ahead_behind._get_unset_required_fields({})
    assert set(unset_fields) == (set(("remoteBranch",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_git_ahead_behind_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_fetch_git_ahead_behind"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_fetch_git_ahead_behind"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.FetchGitAheadBehindRequest.pb(
            dataform.FetchGitAheadBehindRequest()
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
        req.return_value._content = dataform.FetchGitAheadBehindResponse.to_json(
            dataform.FetchGitAheadBehindResponse()
        )

        request = dataform.FetchGitAheadBehindRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.FetchGitAheadBehindResponse()

        client.fetch_git_ahead_behind(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_git_ahead_behind_rest_bad_request(
    transport: str = "rest", request_type=dataform.FetchGitAheadBehindRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.fetch_git_ahead_behind(request)


def test_fetch_git_ahead_behind_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CommitWorkspaceChangesRequest,
        dict,
    ],
)
def test_commit_workspace_changes_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.commit_workspace_changes(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_commit_workspace_changes_rest_required_fields(
    request_type=dataform.CommitWorkspaceChangesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).commit_workspace_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).commit_workspace_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.commit_workspace_changes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_commit_workspace_changes_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.commit_workspace_changes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "author",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_commit_workspace_changes_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_commit_workspace_changes"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.CommitWorkspaceChangesRequest.pb(
            dataform.CommitWorkspaceChangesRequest()
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

        request = dataform.CommitWorkspaceChangesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.commit_workspace_changes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_commit_workspace_changes_rest_bad_request(
    transport: str = "rest", request_type=dataform.CommitWorkspaceChangesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.commit_workspace_changes(request)


def test_commit_workspace_changes_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ResetWorkspaceChangesRequest,
        dict,
    ],
)
def test_reset_workspace_changes_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.reset_workspace_changes(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_reset_workspace_changes_rest_required_fields(
    request_type=dataform.ResetWorkspaceChangesRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).reset_workspace_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).reset_workspace_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.reset_workspace_changes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_reset_workspace_changes_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.reset_workspace_changes._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_reset_workspace_changes_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_reset_workspace_changes"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.ResetWorkspaceChangesRequest.pb(
            dataform.ResetWorkspaceChangesRequest()
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

        request = dataform.ResetWorkspaceChangesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.reset_workspace_changes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_reset_workspace_changes_rest_bad_request(
    transport: str = "rest", request_type=dataform.ResetWorkspaceChangesRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.reset_workspace_changes(request)


def test_reset_workspace_changes_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.FetchFileDiffRequest,
        dict,
    ],
)
def test_fetch_file_diff_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.FetchFileDiffResponse(
            formatted_diff="formatted_diff_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.FetchFileDiffResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_file_diff(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.FetchFileDiffResponse)
    assert response.formatted_diff == "formatted_diff_value"


def test_fetch_file_diff_rest_required_fields(
    request_type=dataform.FetchFileDiffRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
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
    assert "path" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_file_diff._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "path" in jsonified_request
    assert jsonified_request["path"] == request_init["path"]

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_file_diff._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("path",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.FetchFileDiffResponse()
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

            pb_return_value = dataform.FetchFileDiffResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_file_diff(request)

            expected_params = [
                (
                    "path",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_file_diff_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_file_diff._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("path",))
        & set(
            (
                "workspace",
                "path",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_file_diff_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_fetch_file_diff"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_fetch_file_diff"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.FetchFileDiffRequest.pb(dataform.FetchFileDiffRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.FetchFileDiffResponse.to_json(
            dataform.FetchFileDiffResponse()
        )

        request = dataform.FetchFileDiffRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.FetchFileDiffResponse()

        client.fetch_file_diff(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_file_diff_rest_bad_request(
    transport: str = "rest", request_type=dataform.FetchFileDiffRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.fetch_file_diff(request)


def test_fetch_file_diff_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryDirectoryContentsRequest,
        dict,
    ],
)
def test_query_directory_contents_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.QueryDirectoryContentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.QueryDirectoryContentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.query_directory_contents(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryDirectoryContentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_directory_contents_rest_required_fields(
    request_type=dataform.QueryDirectoryContentsRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
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
    ).query_directory_contents._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query_directory_contents._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "path",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.QueryDirectoryContentsResponse()
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

            pb_return_value = dataform.QueryDirectoryContentsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.query_directory_contents(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_directory_contents_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.query_directory_contents._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "path",
            )
        )
        & set(("workspace",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_query_directory_contents_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_query_directory_contents"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_query_directory_contents"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.QueryDirectoryContentsRequest.pb(
            dataform.QueryDirectoryContentsRequest()
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
        req.return_value._content = dataform.QueryDirectoryContentsResponse.to_json(
            dataform.QueryDirectoryContentsResponse()
        )

        request = dataform.QueryDirectoryContentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.QueryDirectoryContentsResponse()

        client.query_directory_contents(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_query_directory_contents_rest_bad_request(
    transport: str = "rest", request_type=dataform.QueryDirectoryContentsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.query_directory_contents(request)


def test_query_directory_contents_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[],
                next_page_token="def",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryDirectoryContentsResponse(
                directory_entries=[
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                    dataform.QueryDirectoryContentsResponse.DirectoryEntry(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            dataform.QueryDirectoryContentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
        }

        pager = client.query_directory_contents(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, dataform.QueryDirectoryContentsResponse.DirectoryEntry)
            for i in results
        )

        pages = list(client.query_directory_contents(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MakeDirectoryRequest,
        dict,
    ],
)
def test_make_directory_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.MakeDirectoryResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.MakeDirectoryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.make_directory(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MakeDirectoryResponse)


def test_make_directory_rest_required_fields(
    request_type=dataform.MakeDirectoryRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
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
    ).make_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).make_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.MakeDirectoryResponse()
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

            pb_return_value = dataform.MakeDirectoryResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.make_directory(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_make_directory_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.make_directory._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_make_directory_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_make_directory"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_make_directory"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.MakeDirectoryRequest.pb(dataform.MakeDirectoryRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.MakeDirectoryResponse.to_json(
            dataform.MakeDirectoryResponse()
        )

        request = dataform.MakeDirectoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.MakeDirectoryResponse()

        client.make_directory(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_make_directory_rest_bad_request(
    transport: str = "rest", request_type=dataform.MakeDirectoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.make_directory(request)


def test_make_directory_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.RemoveDirectoryRequest,
        dict,
    ],
)
def test_remove_directory_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_directory(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_directory_rest_required_fields(
    request_type=dataform.RemoveDirectoryRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
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
    ).remove_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).remove_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_directory(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_directory_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.remove_directory._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_directory_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_remove_directory"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.RemoveDirectoryRequest.pb(
            dataform.RemoveDirectoryRequest()
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

        request = dataform.RemoveDirectoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.remove_directory(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_remove_directory_rest_bad_request(
    transport: str = "rest", request_type=dataform.RemoveDirectoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.remove_directory(request)


def test_remove_directory_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MoveDirectoryRequest,
        dict,
    ],
)
def test_move_directory_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.MoveDirectoryResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.MoveDirectoryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.move_directory(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveDirectoryResponse)


def test_move_directory_rest_required_fields(
    request_type=dataform.MoveDirectoryRequest,
):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
    request_init["new_path"] = ""
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
    ).move_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"
    jsonified_request["newPath"] = "new_path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).move_directory._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"
    assert "newPath" in jsonified_request
    assert jsonified_request["newPath"] == "new_path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.MoveDirectoryResponse()
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

            pb_return_value = dataform.MoveDirectoryResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.move_directory(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_move_directory_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.move_directory._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
                "newPath",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_move_directory_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_move_directory"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_move_directory"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.MoveDirectoryRequest.pb(dataform.MoveDirectoryRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.MoveDirectoryResponse.to_json(
            dataform.MoveDirectoryResponse()
        )

        request = dataform.MoveDirectoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.MoveDirectoryResponse()

        client.move_directory(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_move_directory_rest_bad_request(
    transport: str = "rest", request_type=dataform.MoveDirectoryRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.move_directory(request)


def test_move_directory_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ReadFileRequest,
        dict,
    ],
)
def test_read_file_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ReadFileResponse(
            file_contents=b"file_contents_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ReadFileResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.read_file(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.ReadFileResponse)
    assert response.file_contents == b"file_contents_blob"


def test_read_file_rest_required_fields(request_type=dataform.ReadFileRequest):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
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
    assert "path" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "path" in jsonified_request
    assert jsonified_request["path"] == request_init["path"]

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).read_file._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("path",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.ReadFileResponse()
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

            pb_return_value = dataform.ReadFileResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.read_file(request)

            expected_params = [
                (
                    "path",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_read_file_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.read_file._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("path",))
        & set(
            (
                "workspace",
                "path",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_read_file_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_read_file"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_read_file"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.ReadFileRequest.pb(dataform.ReadFileRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.ReadFileResponse.to_json(
            dataform.ReadFileResponse()
        )

        request = dataform.ReadFileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.ReadFileResponse()

        client.read_file(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_read_file_rest_bad_request(
    transport: str = "rest", request_type=dataform.ReadFileRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.read_file(request)


def test_read_file_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.RemoveFileRequest,
        dict,
    ],
)
def test_remove_file_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_file(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_file_rest_required_fields(request_type=dataform.RemoveFileRequest):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
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
    ).remove_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).remove_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_file(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_file_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.remove_file._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_file_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_remove_file"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.RemoveFileRequest.pb(dataform.RemoveFileRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = dataform.RemoveFileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.remove_file(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_remove_file_rest_bad_request(
    transport: str = "rest", request_type=dataform.RemoveFileRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.remove_file(request)


def test_remove_file_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.MoveFileRequest,
        dict,
    ],
)
def test_move_file_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.MoveFileResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.MoveFileResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.move_file(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.MoveFileResponse)


def test_move_file_rest_required_fields(request_type=dataform.MoveFileRequest):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
    request_init["new_path"] = ""
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
    ).move_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"
    jsonified_request["newPath"] = "new_path_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).move_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"
    assert "newPath" in jsonified_request
    assert jsonified_request["newPath"] == "new_path_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.MoveFileResponse()
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

            pb_return_value = dataform.MoveFileResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.move_file(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_move_file_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.move_file._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
                "newPath",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_move_file_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_move_file"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_move_file"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.MoveFileRequest.pb(dataform.MoveFileRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.MoveFileResponse.to_json(
            dataform.MoveFileResponse()
        )

        request = dataform.MoveFileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.MoveFileResponse()

        client.move_file(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_move_file_rest_bad_request(
    transport: str = "rest", request_type=dataform.MoveFileRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.move_file(request)


def test_move_file_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.WriteFileRequest,
        dict,
    ],
)
def test_write_file_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.WriteFileResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.WriteFileResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.write_file(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WriteFileResponse)


def test_write_file_rest_required_fields(request_type=dataform.WriteFileRequest):
    transport_class = transports.DataformRestTransport

    request_init = {}
    request_init["workspace"] = ""
    request_init["path"] = ""
    request_init["contents"] = b""
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
    ).write_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["workspace"] = "workspace_value"
    jsonified_request["path"] = "path_value"
    jsonified_request["contents"] = b"contents_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).write_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "workspace" in jsonified_request
    assert jsonified_request["workspace"] == "workspace_value"
    assert "path" in jsonified_request
    assert jsonified_request["path"] == "path_value"
    assert "contents" in jsonified_request
    assert jsonified_request["contents"] == b"contents_blob"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.WriteFileResponse()
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

            pb_return_value = dataform.WriteFileResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.write_file(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_write_file_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.write_file._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "workspace",
                "path",
                "contents",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_write_file_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_write_file"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_write_file"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.WriteFileRequest.pb(dataform.WriteFileRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = dataform.WriteFileResponse.to_json(
            dataform.WriteFileResponse()
        )

        request = dataform.WriteFileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.WriteFileResponse()

        client.write_file(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_write_file_rest_bad_request(
    transport: str = "rest", request_type=dataform.WriteFileRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "workspace": "projects/sample1/locations/sample2/repositories/sample3/workspaces/sample4"
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
        client.write_file(request)


def test_write_file_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListCompilationResultsRequest,
        dict,
    ],
)
def test_list_compilation_results_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListCompilationResultsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListCompilationResultsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_compilation_results(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCompilationResultsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_compilation_results_rest_required_fields(
    request_type=dataform.ListCompilationResultsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).list_compilation_results._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_compilation_results._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.ListCompilationResultsResponse()
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

            pb_return_value = dataform.ListCompilationResultsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_compilation_results(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_compilation_results_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_compilation_results._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_compilation_results_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_list_compilation_results"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_list_compilation_results"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.ListCompilationResultsRequest.pb(
            dataform.ListCompilationResultsRequest()
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
        req.return_value._content = dataform.ListCompilationResultsResponse.to_json(
            dataform.ListCompilationResultsResponse()
        )

        request = dataform.ListCompilationResultsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.ListCompilationResultsResponse()

        client.list_compilation_results(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_compilation_results_rest_bad_request(
    transport: str = "rest", request_type=dataform.ListCompilationResultsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_compilation_results(request)


def test_list_compilation_results_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListCompilationResultsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListCompilationResultsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_compilation_results(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/compilationResults"
            % client.transport._host,
            args[1],
        )


def test_list_compilation_results_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_compilation_results(
            dataform.ListCompilationResultsRequest(),
            parent="parent_value",
        )


def test_list_compilation_results_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
                next_page_token="abc",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[],
                next_page_token="def",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListCompilationResultsResponse(
                compilation_results=[
                    dataform.CompilationResult(),
                    dataform.CompilationResult(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            dataform.ListCompilationResultsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_compilation_results(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.CompilationResult) for i in results)

        pages = list(client.list_compilation_results(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetCompilationResultRequest,
        dict,
    ],
)
def test_get_compilation_result_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.CompilationResult(
            name="name_value",
            dataform_core_version="dataform_core_version_value",
            git_commitish="git_commitish_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.CompilationResult.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_compilation_result(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


def test_get_compilation_result_rest_required_fields(
    request_type=dataform.GetCompilationResultRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).get_compilation_result._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_compilation_result._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.CompilationResult()
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

            pb_return_value = dataform.CompilationResult.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_compilation_result(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_compilation_result_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_compilation_result._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_compilation_result_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_get_compilation_result"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_get_compilation_result"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.GetCompilationResultRequest.pb(
            dataform.GetCompilationResultRequest()
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
        req.return_value._content = dataform.CompilationResult.to_json(
            dataform.CompilationResult()
        )

        request = dataform.GetCompilationResultRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.CompilationResult()

        client.get_compilation_result(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_compilation_result_rest_bad_request(
    transport: str = "rest", request_type=dataform.GetCompilationResultRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
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
        client.get_compilation_result(request)


def test_get_compilation_result_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.CompilationResult()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.CompilationResult.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_compilation_result(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*/compilationResults/*}"
            % client.transport._host,
            args[1],
        )


def test_get_compilation_result_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_compilation_result(
            dataform.GetCompilationResultRequest(),
            name="name_value",
        )


def test_get_compilation_result_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateCompilationResultRequest,
        dict,
    ],
)
def test_create_compilation_result_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["compilation_result"] = {
        "name": "name_value",
        "git_commitish": "git_commitish_value",
        "workspace": "workspace_value",
        "code_compilation_config": {
            "default_database": "default_database_value",
            "default_schema": "default_schema_value",
            "default_location": "default_location_value",
            "assertion_schema": "assertion_schema_value",
            "vars": {},
            "database_suffix": "database_suffix_value",
            "schema_suffix": "schema_suffix_value",
            "table_prefix": "table_prefix_value",
        },
        "dataform_core_version": "dataform_core_version_value",
        "compilation_errors": [
            {
                "message": "message_value",
                "stack": "stack_value",
                "path": "path_value",
                "action_target": {
                    "database": "database_value",
                    "schema": "schema_value",
                    "name": "name_value",
                },
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.CompilationResult(
            name="name_value",
            dataform_core_version="dataform_core_version_value",
            git_commitish="git_commitish_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.CompilationResult.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_compilation_result(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.CompilationResult)
    assert response.name == "name_value"
    assert response.dataform_core_version == "dataform_core_version_value"


def test_create_compilation_result_rest_required_fields(
    request_type=dataform.CreateCompilationResultRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).create_compilation_result._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_compilation_result._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.CompilationResult()
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

            pb_return_value = dataform.CompilationResult.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_compilation_result(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_compilation_result_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_compilation_result._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "compilationResult",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_compilation_result_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_create_compilation_result"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_create_compilation_result"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.CreateCompilationResultRequest.pb(
            dataform.CreateCompilationResultRequest()
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
        req.return_value._content = dataform.CompilationResult.to_json(
            dataform.CompilationResult()
        )

        request = dataform.CreateCompilationResultRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.CompilationResult()

        client.create_compilation_result(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_compilation_result_rest_bad_request(
    transport: str = "rest", request_type=dataform.CreateCompilationResultRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["compilation_result"] = {
        "name": "name_value",
        "git_commitish": "git_commitish_value",
        "workspace": "workspace_value",
        "code_compilation_config": {
            "default_database": "default_database_value",
            "default_schema": "default_schema_value",
            "default_location": "default_location_value",
            "assertion_schema": "assertion_schema_value",
            "vars": {},
            "database_suffix": "database_suffix_value",
            "schema_suffix": "schema_suffix_value",
            "table_prefix": "table_prefix_value",
        },
        "dataform_core_version": "dataform_core_version_value",
        "compilation_errors": [
            {
                "message": "message_value",
                "stack": "stack_value",
                "path": "path_value",
                "action_target": {
                    "database": "database_value",
                    "schema": "schema_value",
                    "name": "name_value",
                },
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
        client.create_compilation_result(request)


def test_create_compilation_result_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.CompilationResult()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.CompilationResult.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_compilation_result(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/compilationResults"
            % client.transport._host,
            args[1],
        )


def test_create_compilation_result_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_compilation_result(
            dataform.CreateCompilationResultRequest(),
            parent="parent_value",
            compilation_result=dataform.CompilationResult(name="name_value"),
        )


def test_create_compilation_result_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryCompilationResultActionsRequest,
        dict,
    ],
)
def test_query_compilation_result_actions_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.QueryCompilationResultActionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.QueryCompilationResultActionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.query_compilation_result_actions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryCompilationResultActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_compilation_result_actions_rest_required_fields(
    request_type=dataform.QueryCompilationResultActionsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).query_compilation_result_actions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query_compilation_result_actions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.QueryCompilationResultActionsResponse()
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

            pb_return_value = dataform.QueryCompilationResultActionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.query_compilation_result_actions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_compilation_result_actions_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.query_compilation_result_actions._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_query_compilation_result_actions_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_query_compilation_result_actions"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_query_compilation_result_actions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.QueryCompilationResultActionsRequest.pb(
            dataform.QueryCompilationResultActionsRequest()
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
            dataform.QueryCompilationResultActionsResponse.to_json(
                dataform.QueryCompilationResultActionsResponse()
            )
        )

        request = dataform.QueryCompilationResultActionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.QueryCompilationResultActionsResponse()

        client.query_compilation_result_actions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_query_compilation_result_actions_rest_bad_request(
    transport: str = "rest", request_type=dataform.QueryCompilationResultActionsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
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
        client.query_compilation_result_actions(request)


def test_query_compilation_result_actions_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[],
                next_page_token="def",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryCompilationResultActionsResponse(
                compilation_result_actions=[
                    dataform.CompilationResultAction(),
                    dataform.CompilationResultAction(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            dataform.QueryCompilationResultActionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/compilationResults/sample4"
        }

        pager = client.query_compilation_result_actions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.CompilationResultAction) for i in results)

        pages = list(
            client.query_compilation_result_actions(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.ListWorkflowInvocationsRequest,
        dict,
    ],
)
def test_list_workflow_invocations_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListWorkflowInvocationsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListWorkflowInvocationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_workflow_invocations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowInvocationsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workflow_invocations_rest_required_fields(
    request_type=dataform.ListWorkflowInvocationsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).list_workflow_invocations._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_workflow_invocations._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.ListWorkflowInvocationsResponse()
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

            pb_return_value = dataform.ListWorkflowInvocationsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_workflow_invocations(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_workflow_invocations_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_workflow_invocations._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_workflow_invocations_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_list_workflow_invocations"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_list_workflow_invocations"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.ListWorkflowInvocationsRequest.pb(
            dataform.ListWorkflowInvocationsRequest()
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
        req.return_value._content = dataform.ListWorkflowInvocationsResponse.to_json(
            dataform.ListWorkflowInvocationsResponse()
        )

        request = dataform.ListWorkflowInvocationsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.ListWorkflowInvocationsResponse()

        client.list_workflow_invocations(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_workflow_invocations_rest_bad_request(
    transport: str = "rest", request_type=dataform.ListWorkflowInvocationsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_workflow_invocations(request)


def test_list_workflow_invocations_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.ListWorkflowInvocationsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.ListWorkflowInvocationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_workflow_invocations(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/workflowInvocations"
            % client.transport._host,
            args[1],
        )


def test_list_workflow_invocations_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workflow_invocations(
            dataform.ListWorkflowInvocationsRequest(),
            parent="parent_value",
        )


def test_list_workflow_invocations_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="abc",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[],
                next_page_token="def",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                ],
                next_page_token="ghi",
            ),
            dataform.ListWorkflowInvocationsResponse(
                workflow_invocations=[
                    dataform.WorkflowInvocation(),
                    dataform.WorkflowInvocation(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            dataform.ListWorkflowInvocationsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_workflow_invocations(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.WorkflowInvocation) for i in results)

        pages = list(client.list_workflow_invocations(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.GetWorkflowInvocationRequest,
        dict,
    ],
)
def test_get_workflow_invocation_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.WorkflowInvocation(
            name="name_value",
            compilation_result="compilation_result_value",
            state=dataform.WorkflowInvocation.State.RUNNING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.WorkflowInvocation.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_workflow_invocation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


def test_get_workflow_invocation_rest_required_fields(
    request_type=dataform.GetWorkflowInvocationRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).get_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.WorkflowInvocation()
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

            pb_return_value = dataform.WorkflowInvocation.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_workflow_invocation(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_workflow_invocation_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_workflow_invocation._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_workflow_invocation_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_get_workflow_invocation"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_get_workflow_invocation"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.GetWorkflowInvocationRequest.pb(
            dataform.GetWorkflowInvocationRequest()
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
        req.return_value._content = dataform.WorkflowInvocation.to_json(
            dataform.WorkflowInvocation()
        )

        request = dataform.GetWorkflowInvocationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.WorkflowInvocation()

        client.get_workflow_invocation(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_workflow_invocation_rest_bad_request(
    transport: str = "rest", request_type=dataform.GetWorkflowInvocationRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
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
        client.get_workflow_invocation(request)


def test_get_workflow_invocation_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.WorkflowInvocation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.WorkflowInvocation.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_workflow_invocation(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}"
            % client.transport._host,
            args[1],
        )


def test_get_workflow_invocation_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workflow_invocation(
            dataform.GetWorkflowInvocationRequest(),
            name="name_value",
        )


def test_get_workflow_invocation_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CreateWorkflowInvocationRequest,
        dict,
    ],
)
def test_create_workflow_invocation_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["workflow_invocation"] = {
        "name": "name_value",
        "compilation_result": "compilation_result_value",
        "invocation_config": {
            "included_targets": [
                {
                    "database": "database_value",
                    "schema": "schema_value",
                    "name": "name_value",
                }
            ],
            "included_tags": ["included_tags_value1", "included_tags_value2"],
            "transitive_dependencies_included": True,
            "transitive_dependents_included": True,
            "fully_refresh_incremental_tables_enabled": True,
        },
        "state": 1,
        "invocation_timing": {
            "start_time": {"seconds": 751, "nanos": 543},
            "end_time": {},
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.WorkflowInvocation(
            name="name_value",
            compilation_result="compilation_result_value",
            state=dataform.WorkflowInvocation.State.RUNNING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.WorkflowInvocation.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_workflow_invocation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataform.WorkflowInvocation)
    assert response.name == "name_value"
    assert response.compilation_result == "compilation_result_value"
    assert response.state == dataform.WorkflowInvocation.State.RUNNING


def test_create_workflow_invocation_rest_required_fields(
    request_type=dataform.CreateWorkflowInvocationRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).create_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.WorkflowInvocation()
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

            pb_return_value = dataform.WorkflowInvocation.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_workflow_invocation(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_workflow_invocation_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_workflow_invocation._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "workflowInvocation",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_workflow_invocation_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_create_workflow_invocation"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_create_workflow_invocation"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.CreateWorkflowInvocationRequest.pb(
            dataform.CreateWorkflowInvocationRequest()
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
        req.return_value._content = dataform.WorkflowInvocation.to_json(
            dataform.WorkflowInvocation()
        )

        request = dataform.CreateWorkflowInvocationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.WorkflowInvocation()

        client.create_workflow_invocation(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_workflow_invocation_rest_bad_request(
    transport: str = "rest", request_type=dataform.CreateWorkflowInvocationRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request_init["workflow_invocation"] = {
        "name": "name_value",
        "compilation_result": "compilation_result_value",
        "invocation_config": {
            "included_targets": [
                {
                    "database": "database_value",
                    "schema": "schema_value",
                    "name": "name_value",
                }
            ],
            "included_tags": ["included_tags_value1", "included_tags_value2"],
            "transitive_dependencies_included": True,
            "transitive_dependents_included": True,
            "fully_refresh_incremental_tables_enabled": True,
        },
        "state": 1,
        "invocation_timing": {
            "start_time": {"seconds": 751, "nanos": 543},
            "end_time": {},
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
        client.create_workflow_invocation(request)


def test_create_workflow_invocation_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.WorkflowInvocation()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.WorkflowInvocation.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_workflow_invocation(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{parent=projects/*/locations/*/repositories/*}/workflowInvocations"
            % client.transport._host,
            args[1],
        )


def test_create_workflow_invocation_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workflow_invocation(
            dataform.CreateWorkflowInvocationRequest(),
            parent="parent_value",
            workflow_invocation=dataform.WorkflowInvocation(name="name_value"),
        )


def test_create_workflow_invocation_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.DeleteWorkflowInvocationRequest,
        dict,
    ],
)
def test_delete_workflow_invocation_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_workflow_invocation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workflow_invocation_rest_required_fields(
    request_type=dataform.DeleteWorkflowInvocationRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).delete_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_workflow_invocation(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_workflow_invocation_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_workflow_invocation._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_workflow_invocation_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_delete_workflow_invocation"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.DeleteWorkflowInvocationRequest.pb(
            dataform.DeleteWorkflowInvocationRequest()
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

        request = dataform.DeleteWorkflowInvocationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_workflow_invocation(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_workflow_invocation_rest_bad_request(
    transport: str = "rest", request_type=dataform.DeleteWorkflowInvocationRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
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
        client.delete_workflow_invocation(request)


def test_delete_workflow_invocation_rest_flattened():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_workflow_invocation(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta1/{name=projects/*/locations/*/repositories/*/workflowInvocations/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_workflow_invocation_rest_flattened_error(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workflow_invocation(
            dataform.DeleteWorkflowInvocationRequest(),
            name="name_value",
        )


def test_delete_workflow_invocation_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.CancelWorkflowInvocationRequest,
        dict,
    ],
)
def test_cancel_workflow_invocation_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.cancel_workflow_invocation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_workflow_invocation_rest_required_fields(
    request_type=dataform.CancelWorkflowInvocationRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).cancel_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).cancel_workflow_invocation._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.cancel_workflow_invocation(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_cancel_workflow_invocation_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.cancel_workflow_invocation._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_cancel_workflow_invocation_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "pre_cancel_workflow_invocation"
    ) as pre:
        pre.assert_not_called()
        pb_message = dataform.CancelWorkflowInvocationRequest.pb(
            dataform.CancelWorkflowInvocationRequest()
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

        request = dataform.CancelWorkflowInvocationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.cancel_workflow_invocation(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_cancel_workflow_invocation_rest_bad_request(
    transport: str = "rest", request_type=dataform.CancelWorkflowInvocationRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
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
        client.cancel_workflow_invocation(request)


def test_cancel_workflow_invocation_rest_error():
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        dataform.QueryWorkflowInvocationActionsRequest,
        dict,
    ],
)
def test_query_workflow_invocation_actions_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataform.QueryWorkflowInvocationActionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataform.QueryWorkflowInvocationActionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.query_workflow_invocation_actions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.QueryWorkflowInvocationActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_query_workflow_invocation_actions_rest_required_fields(
    request_type=dataform.QueryWorkflowInvocationActionsRequest,
):
    transport_class = transports.DataformRestTransport

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
    ).query_workflow_invocation_actions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query_workflow_invocation_actions._get_unset_required_fields(jsonified_request)
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

    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataform.QueryWorkflowInvocationActionsResponse()
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

            pb_return_value = dataform.QueryWorkflowInvocationActionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.query_workflow_invocation_actions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_workflow_invocation_actions_rest_unset_required_fields():
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.query_workflow_invocation_actions._get_unset_required_fields({})
    )
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
def test_query_workflow_invocation_actions_rest_interceptors(null_interceptor):
    transport = transports.DataformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DataformRestInterceptor(),
    )
    client = DataformClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataformRestInterceptor, "post_query_workflow_invocation_actions"
    ) as post, mock.patch.object(
        transports.DataformRestInterceptor, "pre_query_workflow_invocation_actions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = dataform.QueryWorkflowInvocationActionsRequest.pb(
            dataform.QueryWorkflowInvocationActionsRequest()
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
            dataform.QueryWorkflowInvocationActionsResponse.to_json(
                dataform.QueryWorkflowInvocationActionsResponse()
            )
        )

        request = dataform.QueryWorkflowInvocationActionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataform.QueryWorkflowInvocationActionsResponse()

        client.query_workflow_invocation_actions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_query_workflow_invocation_actions_rest_bad_request(
    transport: str = "rest", request_type=dataform.QueryWorkflowInvocationActionsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
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
        client.query_workflow_invocation_actions(request)


def test_query_workflow_invocation_actions_rest_pager(transport: str = "rest"):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="abc",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[],
                next_page_token="def",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                ],
                next_page_token="ghi",
            ),
            dataform.QueryWorkflowInvocationActionsResponse(
                workflow_invocation_actions=[
                    dataform.WorkflowInvocationAction(),
                    dataform.WorkflowInvocationAction(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            dataform.QueryWorkflowInvocationActionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/workflowInvocations/sample4"
        }

        pager = client.query_workflow_invocation_actions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataform.WorkflowInvocationAction) for i in results)

        pages = list(
            client.query_workflow_invocation_actions(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataformClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataformClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataformClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataformClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataformClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataformGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataformGrpcTransport,
        transports.DataformGrpcAsyncIOTransport,
        transports.DataformRestTransport,
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
    transport = DataformClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DataformGrpcTransport,
    )


def test_dataform_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataformTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_dataform_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataform_v1beta1.services.dataform.transports.DataformTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataformTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_repositories",
        "get_repository",
        "create_repository",
        "update_repository",
        "delete_repository",
        "fetch_remote_branches",
        "list_workspaces",
        "get_workspace",
        "create_workspace",
        "delete_workspace",
        "install_npm_packages",
        "pull_git_commits",
        "push_git_commits",
        "fetch_file_git_statuses",
        "fetch_git_ahead_behind",
        "commit_workspace_changes",
        "reset_workspace_changes",
        "fetch_file_diff",
        "query_directory_contents",
        "make_directory",
        "remove_directory",
        "move_directory",
        "read_file",
        "remove_file",
        "move_file",
        "write_file",
        "list_compilation_results",
        "get_compilation_result",
        "create_compilation_result",
        "query_compilation_result_actions",
        "list_workflow_invocations",
        "get_workflow_invocation",
        "create_workflow_invocation",
        "delete_workflow_invocation",
        "cancel_workflow_invocation",
        "query_workflow_invocation_actions",
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


def test_dataform_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dataform_v1beta1.services.dataform.transports.DataformTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataformTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_dataform_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dataform_v1beta1.services.dataform.transports.DataformTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataformTransport()
        adc.assert_called_once()


def test_dataform_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataformClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataformGrpcTransport,
        transports.DataformGrpcAsyncIOTransport,
    ],
)
def test_dataform_transport_auth_adc(transport_class):
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
        transports.DataformGrpcTransport,
        transports.DataformGrpcAsyncIOTransport,
        transports.DataformRestTransport,
    ],
)
def test_dataform_transport_auth_gdch_credentials(transport_class):
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
        (transports.DataformGrpcTransport, grpc_helpers),
        (transports.DataformGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_dataform_transport_create_channel(transport_class, grpc_helpers):
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
            "dataform.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dataform.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DataformGrpcTransport, transports.DataformGrpcAsyncIOTransport],
)
def test_dataform_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_dataform_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DataformRestTransport(
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
def test_dataform_host_no_port(transport_name):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataform.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataform.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataform.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_dataform_host_with_port(transport_name):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataform.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataform.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataform.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_dataform_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DataformClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DataformClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_repositories._session
    session2 = client2.transport.list_repositories._session
    assert session1 != session2
    session1 = client1.transport.get_repository._session
    session2 = client2.transport.get_repository._session
    assert session1 != session2
    session1 = client1.transport.create_repository._session
    session2 = client2.transport.create_repository._session
    assert session1 != session2
    session1 = client1.transport.update_repository._session
    session2 = client2.transport.update_repository._session
    assert session1 != session2
    session1 = client1.transport.delete_repository._session
    session2 = client2.transport.delete_repository._session
    assert session1 != session2
    session1 = client1.transport.fetch_remote_branches._session
    session2 = client2.transport.fetch_remote_branches._session
    assert session1 != session2
    session1 = client1.transport.list_workspaces._session
    session2 = client2.transport.list_workspaces._session
    assert session1 != session2
    session1 = client1.transport.get_workspace._session
    session2 = client2.transport.get_workspace._session
    assert session1 != session2
    session1 = client1.transport.create_workspace._session
    session2 = client2.transport.create_workspace._session
    assert session1 != session2
    session1 = client1.transport.delete_workspace._session
    session2 = client2.transport.delete_workspace._session
    assert session1 != session2
    session1 = client1.transport.install_npm_packages._session
    session2 = client2.transport.install_npm_packages._session
    assert session1 != session2
    session1 = client1.transport.pull_git_commits._session
    session2 = client2.transport.pull_git_commits._session
    assert session1 != session2
    session1 = client1.transport.push_git_commits._session
    session2 = client2.transport.push_git_commits._session
    assert session1 != session2
    session1 = client1.transport.fetch_file_git_statuses._session
    session2 = client2.transport.fetch_file_git_statuses._session
    assert session1 != session2
    session1 = client1.transport.fetch_git_ahead_behind._session
    session2 = client2.transport.fetch_git_ahead_behind._session
    assert session1 != session2
    session1 = client1.transport.commit_workspace_changes._session
    session2 = client2.transport.commit_workspace_changes._session
    assert session1 != session2
    session1 = client1.transport.reset_workspace_changes._session
    session2 = client2.transport.reset_workspace_changes._session
    assert session1 != session2
    session1 = client1.transport.fetch_file_diff._session
    session2 = client2.transport.fetch_file_diff._session
    assert session1 != session2
    session1 = client1.transport.query_directory_contents._session
    session2 = client2.transport.query_directory_contents._session
    assert session1 != session2
    session1 = client1.transport.make_directory._session
    session2 = client2.transport.make_directory._session
    assert session1 != session2
    session1 = client1.transport.remove_directory._session
    session2 = client2.transport.remove_directory._session
    assert session1 != session2
    session1 = client1.transport.move_directory._session
    session2 = client2.transport.move_directory._session
    assert session1 != session2
    session1 = client1.transport.read_file._session
    session2 = client2.transport.read_file._session
    assert session1 != session2
    session1 = client1.transport.remove_file._session
    session2 = client2.transport.remove_file._session
    assert session1 != session2
    session1 = client1.transport.move_file._session
    session2 = client2.transport.move_file._session
    assert session1 != session2
    session1 = client1.transport.write_file._session
    session2 = client2.transport.write_file._session
    assert session1 != session2
    session1 = client1.transport.list_compilation_results._session
    session2 = client2.transport.list_compilation_results._session
    assert session1 != session2
    session1 = client1.transport.get_compilation_result._session
    session2 = client2.transport.get_compilation_result._session
    assert session1 != session2
    session1 = client1.transport.create_compilation_result._session
    session2 = client2.transport.create_compilation_result._session
    assert session1 != session2
    session1 = client1.transport.query_compilation_result_actions._session
    session2 = client2.transport.query_compilation_result_actions._session
    assert session1 != session2
    session1 = client1.transport.list_workflow_invocations._session
    session2 = client2.transport.list_workflow_invocations._session
    assert session1 != session2
    session1 = client1.transport.get_workflow_invocation._session
    session2 = client2.transport.get_workflow_invocation._session
    assert session1 != session2
    session1 = client1.transport.create_workflow_invocation._session
    session2 = client2.transport.create_workflow_invocation._session
    assert session1 != session2
    session1 = client1.transport.delete_workflow_invocation._session
    session2 = client2.transport.delete_workflow_invocation._session
    assert session1 != session2
    session1 = client1.transport.cancel_workflow_invocation._session
    session2 = client2.transport.cancel_workflow_invocation._session
    assert session1 != session2
    session1 = client1.transport.query_workflow_invocation_actions._session
    session2 = client2.transport.query_workflow_invocation_actions._session
    assert session1 != session2


def test_dataform_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataformGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_dataform_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataformGrpcAsyncIOTransport(
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
    [transports.DataformGrpcTransport, transports.DataformGrpcAsyncIOTransport],
)
def test_dataform_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.DataformGrpcTransport, transports.DataformGrpcAsyncIOTransport],
)
def test_dataform_transport_channel_mtls_with_adc(transport_class):
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


def test_compilation_result_path():
    project = "squid"
    location = "clam"
    repository = "whelk"
    compilation_result = "octopus"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/compilationResults/{compilation_result}".format(
        project=project,
        location=location,
        repository=repository,
        compilation_result=compilation_result,
    )
    actual = DataformClient.compilation_result_path(
        project, location, repository, compilation_result
    )
    assert expected == actual


def test_parse_compilation_result_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "repository": "cuttlefish",
        "compilation_result": "mussel",
    }
    path = DataformClient.compilation_result_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_compilation_result_path(path)
    assert expected == actual


def test_repository_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    expected = (
        "projects/{project}/locations/{location}/repositories/{repository}".format(
            project=project,
            location=location,
            repository=repository,
        )
    )
    actual = DataformClient.repository_path(project, location, repository)
    assert expected == actual


def test_parse_repository_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "repository": "clam",
    }
    path = DataformClient.repository_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_repository_path(path)
    assert expected == actual


def test_secret_version_path():
    project = "whelk"
    secret = "octopus"
    version = "oyster"
    expected = "projects/{project}/secrets/{secret}/versions/{version}".format(
        project=project,
        secret=secret,
        version=version,
    )
    actual = DataformClient.secret_version_path(project, secret, version)
    assert expected == actual


def test_parse_secret_version_path():
    expected = {
        "project": "nudibranch",
        "secret": "cuttlefish",
        "version": "mussel",
    }
    path = DataformClient.secret_version_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_secret_version_path(path)
    assert expected == actual


def test_workflow_invocation_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    workflow_invocation = "abalone"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/workflowInvocations/{workflow_invocation}".format(
        project=project,
        location=location,
        repository=repository,
        workflow_invocation=workflow_invocation,
    )
    actual = DataformClient.workflow_invocation_path(
        project, location, repository, workflow_invocation
    )
    assert expected == actual


def test_parse_workflow_invocation_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "repository": "whelk",
        "workflow_invocation": "octopus",
    }
    path = DataformClient.workflow_invocation_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_workflow_invocation_path(path)
    assert expected == actual


def test_workspace_path():
    project = "oyster"
    location = "nudibranch"
    repository = "cuttlefish"
    workspace = "mussel"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/workspaces/{workspace}".format(
        project=project,
        location=location,
        repository=repository,
        workspace=workspace,
    )
    actual = DataformClient.workspace_path(project, location, repository, workspace)
    assert expected == actual


def test_parse_workspace_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "repository": "scallop",
        "workspace": "abalone",
    }
    path = DataformClient.workspace_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_workspace_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataformClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = DataformClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DataformClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = DataformClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DataformClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = DataformClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DataformClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = DataformClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DataformClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = DataformClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataformClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataformTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataformTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataformClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DataformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = DataformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations(transport: str = "grpc"):
    client = DataformClient(
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
    client = DataformAsyncClient(
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
    client = DataformClient(
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
    client = DataformAsyncClient(
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
    client = DataformClient(
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
    client = DataformAsyncClient(
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
    client = DataformClient(
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
    client = DataformAsyncClient(
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
    client = DataformClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = DataformAsyncClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = DataformClient(
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
    client = DataformAsyncClient(
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
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = DataformClient(
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
        client = DataformClient(
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
        (DataformClient, transports.DataformGrpcTransport),
        (DataformAsyncClient, transports.DataformGrpcAsyncIOTransport),
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
