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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.domains_v1.services.domains import (
    DomainsAsyncClient,
    DomainsClient,
    pagers,
    transports,
)
from google.cloud.domains_v1.types import domains


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

    assert DomainsClient._get_default_mtls_endpoint(None) is None
    assert DomainsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        DomainsClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        DomainsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DomainsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DomainsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DomainsClient, "grpc"),
        (DomainsAsyncClient, "grpc_asyncio"),
        (DomainsClient, "rest"),
    ],
)
def test_domains_client_from_service_account_info(client_class, transport_name):
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
            "domains.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://domains.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DomainsGrpcTransport, "grpc"),
        (transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DomainsRestTransport, "rest"),
    ],
)
def test_domains_client_service_account_always_use_jwt(transport_class, transport_name):
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
        (DomainsClient, "grpc"),
        (DomainsAsyncClient, "grpc_asyncio"),
        (DomainsClient, "rest"),
    ],
)
def test_domains_client_from_service_account_file(client_class, transport_name):
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
            "domains.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://domains.googleapis.com"
        )


def test_domains_client_get_transport_class():
    transport = DomainsClient.get_transport_class()
    available_transports = [
        transports.DomainsGrpcTransport,
        transports.DomainsRestTransport,
    ]
    assert transport in available_transports

    transport = DomainsClient.get_transport_class("grpc")
    assert transport == transports.DomainsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DomainsClient, transports.DomainsGrpcTransport, "grpc"),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
        (DomainsClient, transports.DomainsRestTransport, "rest"),
    ],
)
@mock.patch.object(
    DomainsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsClient)
)
@mock.patch.object(
    DomainsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsAsyncClient)
)
def test_domains_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DomainsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DomainsClient, "get_transport_class") as gtc:
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc", "true"),
        (
            DomainsAsyncClient,
            transports.DomainsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DomainsClient, transports.DomainsGrpcTransport, "grpc", "false"),
        (
            DomainsAsyncClient,
            transports.DomainsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (DomainsClient, transports.DomainsRestTransport, "rest", "true"),
        (DomainsClient, transports.DomainsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    DomainsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsClient)
)
@mock.patch.object(
    DomainsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_domains_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [DomainsClient, DomainsAsyncClient])
@mock.patch.object(
    DomainsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsClient)
)
@mock.patch.object(
    DomainsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DomainsAsyncClient)
)
def test_domains_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc"),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
        (DomainsClient, transports.DomainsRestTransport, "rest"),
    ],
)
def test_domains_client_client_options_scopes(
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc", grpc_helpers),
        (
            DomainsAsyncClient,
            transports.DomainsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (DomainsClient, transports.DomainsRestTransport, "rest", None),
    ],
)
def test_domains_client_client_options_credentials_file(
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


def test_domains_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.domains_v1.services.domains.transports.DomainsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DomainsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc", grpc_helpers),
        (
            DomainsAsyncClient,
            transports.DomainsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_domains_client_create_channel_credentials_file(
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
            "domains.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="domains.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.SearchDomainsRequest,
        dict,
    ],
)
def test_search_domains(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.SearchDomainsResponse()
        response = client.search_domains(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.SearchDomainsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.SearchDomainsResponse)


def test_search_domains_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        client.search_domains()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.SearchDomainsRequest()


@pytest.mark.asyncio
async def test_search_domains_async(
    transport: str = "grpc_asyncio", request_type=domains.SearchDomainsRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.SearchDomainsResponse()
        )
        response = await client.search_domains(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.SearchDomainsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.SearchDomainsResponse)


@pytest.mark.asyncio
async def test_search_domains_async_from_dict():
    await test_search_domains_async(request_type=dict)


def test_search_domains_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.SearchDomainsRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        call.return_value = domains.SearchDomainsResponse()
        client.search_domains(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_domains_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.SearchDomainsRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.SearchDomainsResponse()
        )
        await client.search_domains(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_search_domains_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.SearchDomainsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_domains(
            location="location_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


def test_search_domains_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_domains(
            domains.SearchDomainsRequest(),
            location="location_value",
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_domains_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.SearchDomainsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.SearchDomainsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_domains(
            location="location_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_search_domains_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_domains(
            domains.SearchDomainsRequest(),
            location="location_value",
            query="query_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveRegisterParametersRequest,
        dict,
    ],
)
def test_retrieve_register_parameters(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveRegisterParametersResponse()
        response = client.retrieve_register_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveRegisterParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveRegisterParametersResponse)


def test_retrieve_register_parameters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        client.retrieve_register_parameters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveRegisterParametersRequest()


@pytest.mark.asyncio
async def test_retrieve_register_parameters_async(
    transport: str = "grpc_asyncio",
    request_type=domains.RetrieveRegisterParametersRequest,
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveRegisterParametersResponse()
        )
        response = await client.retrieve_register_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveRegisterParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveRegisterParametersResponse)


@pytest.mark.asyncio
async def test_retrieve_register_parameters_async_from_dict():
    await test_retrieve_register_parameters_async(request_type=dict)


def test_retrieve_register_parameters_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveRegisterParametersRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        call.return_value = domains.RetrieveRegisterParametersResponse()
        client.retrieve_register_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_retrieve_register_parameters_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveRegisterParametersRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveRegisterParametersResponse()
        )
        await client.retrieve_register_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_retrieve_register_parameters_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveRegisterParametersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retrieve_register_parameters(
            location="location_value",
            domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].domain_name
        mock_val = "domain_name_value"
        assert arg == mock_val


def test_retrieve_register_parameters_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_register_parameters(
            domains.RetrieveRegisterParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


@pytest.mark.asyncio
async def test_retrieve_register_parameters_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveRegisterParametersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveRegisterParametersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retrieve_register_parameters(
            location="location_value",
            domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].domain_name
        mock_val = "domain_name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_retrieve_register_parameters_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retrieve_register_parameters(
            domains.RetrieveRegisterParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RegisterDomainRequest,
        dict,
    ],
)
def test_register_domain(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.register_domain(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RegisterDomainRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_register_domain_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        client.register_domain()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RegisterDomainRequest()


@pytest.mark.asyncio
async def test_register_domain_async(
    transport: str = "grpc_asyncio", request_type=domains.RegisterDomainRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.register_domain(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RegisterDomainRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_register_domain_async_from_dict():
    await test_register_domain_async(request_type=dict)


def test_register_domain_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RegisterDomainRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.register_domain(request)

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
async def test_register_domain_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RegisterDomainRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.register_domain(request)

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


def test_register_domain_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.register_domain(
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].yearly_price
        mock_val = money_pb2.Money(currency_code="currency_code_value")
        assert arg == mock_val


def test_register_domain_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.register_domain(
            domains.RegisterDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )


@pytest.mark.asyncio
async def test_register_domain_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.register_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.register_domain(
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].yearly_price
        mock_val = money_pb2.Money(currency_code="currency_code_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_register_domain_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.register_domain(
            domains.RegisterDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveTransferParametersRequest,
        dict,
    ],
)
def test_retrieve_transfer_parameters(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveTransferParametersResponse()
        response = client.retrieve_transfer_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveTransferParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveTransferParametersResponse)


def test_retrieve_transfer_parameters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        client.retrieve_transfer_parameters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveTransferParametersRequest()


@pytest.mark.asyncio
async def test_retrieve_transfer_parameters_async(
    transport: str = "grpc_asyncio",
    request_type=domains.RetrieveTransferParametersRequest,
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveTransferParametersResponse()
        )
        response = await client.retrieve_transfer_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveTransferParametersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveTransferParametersResponse)


@pytest.mark.asyncio
async def test_retrieve_transfer_parameters_async_from_dict():
    await test_retrieve_transfer_parameters_async(request_type=dict)


def test_retrieve_transfer_parameters_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveTransferParametersRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        call.return_value = domains.RetrieveTransferParametersResponse()
        client.retrieve_transfer_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_retrieve_transfer_parameters_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveTransferParametersRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveTransferParametersResponse()
        )
        await client.retrieve_transfer_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_retrieve_transfer_parameters_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveTransferParametersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retrieve_transfer_parameters(
            location="location_value",
            domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].domain_name
        mock_val = "domain_name_value"
        assert arg == mock_val


def test_retrieve_transfer_parameters_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_transfer_parameters(
            domains.RetrieveTransferParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


@pytest.mark.asyncio
async def test_retrieve_transfer_parameters_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_transfer_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveTransferParametersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.RetrieveTransferParametersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retrieve_transfer_parameters(
            location="location_value",
            domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val
        arg = args[0].domain_name
        mock_val = "domain_name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_retrieve_transfer_parameters_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retrieve_transfer_parameters(
            domains.RetrieveTransferParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.TransferDomainRequest,
        dict,
    ],
)
def test_transfer_domain(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.transfer_domain(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.TransferDomainRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_transfer_domain_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        client.transfer_domain()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.TransferDomainRequest()


@pytest.mark.asyncio
async def test_transfer_domain_async(
    transport: str = "grpc_asyncio", request_type=domains.TransferDomainRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.transfer_domain(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.TransferDomainRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_transfer_domain_async_from_dict():
    await test_transfer_domain_async(request_type=dict)


def test_transfer_domain_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.TransferDomainRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.transfer_domain(request)

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
async def test_transfer_domain_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.TransferDomainRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.transfer_domain(request)

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


def test_transfer_domain_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.transfer_domain(
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].yearly_price
        mock_val = money_pb2.Money(currency_code="currency_code_value")
        assert arg == mock_val
        arg = args[0].authorization_code
        mock_val = domains.AuthorizationCode(code="code_value")
        assert arg == mock_val


def test_transfer_domain_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.transfer_domain(
            domains.TransferDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )


@pytest.mark.asyncio
async def test_transfer_domain_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.transfer_domain), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.transfer_domain(
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].yearly_price
        mock_val = money_pb2.Money(currency_code="currency_code_value")
        assert arg == mock_val
        arg = args[0].authorization_code
        mock_val = domains.AuthorizationCode(code="code_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_transfer_domain_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.transfer_domain(
            domains.TransferDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ListRegistrationsRequest,
        dict,
    ],
)
def test_list_registrations(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.ListRegistrationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_registrations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ListRegistrationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRegistrationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_registrations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        client.list_registrations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ListRegistrationsRequest()


@pytest.mark.asyncio
async def test_list_registrations_async(
    transport: str = "grpc_asyncio", request_type=domains.ListRegistrationsRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.ListRegistrationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_registrations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ListRegistrationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRegistrationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_registrations_async_from_dict():
    await test_list_registrations_async(request_type=dict)


def test_list_registrations_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ListRegistrationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        call.return_value = domains.ListRegistrationsResponse()
        client.list_registrations(request)

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
async def test_list_registrations_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ListRegistrationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.ListRegistrationsResponse()
        )
        await client.list_registrations(request)

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


def test_list_registrations_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.ListRegistrationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_registrations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_registrations_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_registrations(
            domains.ListRegistrationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_registrations_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.ListRegistrationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.ListRegistrationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_registrations(
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
async def test_list_registrations_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_registrations(
            domains.ListRegistrationsRequest(),
            parent="parent_value",
        )


def test_list_registrations_pager(transport_name: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                    domains.Registration(),
                ],
                next_page_token="abc",
            ),
            domains.ListRegistrationsResponse(
                registrations=[],
                next_page_token="def",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                ],
                next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_registrations(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, domains.Registration) for i in results)


def test_list_registrations_pages(transport_name: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                    domains.Registration(),
                ],
                next_page_token="abc",
            ),
            domains.ListRegistrationsResponse(
                registrations=[],
                next_page_token="def",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                ],
                next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_registrations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_registrations_async_pager():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                    domains.Registration(),
                ],
                next_page_token="abc",
            ),
            domains.ListRegistrationsResponse(
                registrations=[],
                next_page_token="def",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                ],
                next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_registrations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, domains.Registration) for i in responses)


@pytest.mark.asyncio
async def test_list_registrations_async_pages():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                    domains.Registration(),
                ],
                next_page_token="abc",
            ),
            domains.ListRegistrationsResponse(
                registrations=[],
                next_page_token="def",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                ],
                next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_registrations(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        domains.GetRegistrationRequest,
        dict,
    ],
)
def test_get_registration(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.Registration(
            name="name_value",
            domain_name="domain_name_value",
            state=domains.Registration.State.REGISTRATION_PENDING,
            issues=[domains.Registration.Issue.CONTACT_SUPPORT],
            supported_privacy=[domains.ContactPrivacy.PUBLIC_CONTACT_DATA],
        )
        response = client.get_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.GetRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.Registration)
    assert response.name == "name_value"
    assert response.domain_name == "domain_name_value"
    assert response.state == domains.Registration.State.REGISTRATION_PENDING
    assert response.issues == [domains.Registration.Issue.CONTACT_SUPPORT]
    assert response.supported_privacy == [domains.ContactPrivacy.PUBLIC_CONTACT_DATA]


def test_get_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        client.get_registration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.GetRegistrationRequest()


@pytest.mark.asyncio
async def test_get_registration_async(
    transport: str = "grpc_asyncio", request_type=domains.GetRegistrationRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.Registration(
                name="name_value",
                domain_name="domain_name_value",
                state=domains.Registration.State.REGISTRATION_PENDING,
                issues=[domains.Registration.Issue.CONTACT_SUPPORT],
                supported_privacy=[domains.ContactPrivacy.PUBLIC_CONTACT_DATA],
            )
        )
        response = await client.get_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.GetRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.Registration)
    assert response.name == "name_value"
    assert response.domain_name == "domain_name_value"
    assert response.state == domains.Registration.State.REGISTRATION_PENDING
    assert response.issues == [domains.Registration.Issue.CONTACT_SUPPORT]
    assert response.supported_privacy == [domains.ContactPrivacy.PUBLIC_CONTACT_DATA]


@pytest.mark.asyncio
async def test_get_registration_async_from_dict():
    await test_get_registration_async(request_type=dict)


def test_get_registration_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.GetRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        call.return_value = domains.Registration()
        client.get_registration(request)

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
async def test_get_registration_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.GetRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.Registration()
        )
        await client.get_registration(request)

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


def test_get_registration_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.Registration()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_registration(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_registration_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_registration(
            domains.GetRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_registration_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.Registration()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.Registration()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_registration(
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
async def test_get_registration_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_registration(
            domains.GetRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.UpdateRegistrationRequest,
        dict,
    ],
)
def test_update_registration(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.UpdateRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        client.update_registration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.UpdateRegistrationRequest()


@pytest.mark.asyncio
async def test_update_registration_async(
    transport: str = "grpc_asyncio", request_type=domains.UpdateRegistrationRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.UpdateRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_registration_async_from_dict():
    await test_update_registration_async(request_type=dict)


def test_update_registration_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.UpdateRegistrationRequest()

    request.registration.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_registration_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.UpdateRegistrationRequest()

    request.registration.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration.name=name_value",
    ) in kw["metadata"]


def test_update_registration_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_registration(
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_registration_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_registration(
            domains.UpdateRegistrationRequest(),
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_registration_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_registration(
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = domains.Registration(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_registration_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_registration(
            domains.UpdateRegistrationRequest(),
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureManagementSettingsRequest,
        dict,
    ],
)
def test_configure_management_settings(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.configure_management_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureManagementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_configure_management_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        client.configure_management_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureManagementSettingsRequest()


@pytest.mark.asyncio
async def test_configure_management_settings_async(
    transport: str = "grpc_asyncio",
    request_type=domains.ConfigureManagementSettingsRequest,
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.configure_management_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureManagementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_configure_management_settings_async_from_dict():
    await test_configure_management_settings_async(request_type=dict)


def test_configure_management_settings_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureManagementSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.configure_management_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_configure_management_settings_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureManagementSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.configure_management_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


def test_configure_management_settings_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.configure_management_settings(
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].management_settings
        mock_val = domains.ManagementSettings(
            renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_configure_management_settings_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_management_settings(
            domains.ConfigureManagementSettingsRequest(),
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_configure_management_settings_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_management_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.configure_management_settings(
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].management_settings
        mock_val = domains.ManagementSettings(
            renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_configure_management_settings_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.configure_management_settings(
            domains.ConfigureManagementSettingsRequest(),
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureDnsSettingsRequest,
        dict,
    ],
)
def test_configure_dns_settings(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.configure_dns_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureDnsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_configure_dns_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        client.configure_dns_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureDnsSettingsRequest()


@pytest.mark.asyncio
async def test_configure_dns_settings_async(
    transport: str = "grpc_asyncio", request_type=domains.ConfigureDnsSettingsRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.configure_dns_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureDnsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_configure_dns_settings_async_from_dict():
    await test_configure_dns_settings_async(request_type=dict)


def test_configure_dns_settings_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureDnsSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.configure_dns_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_configure_dns_settings_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureDnsSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.configure_dns_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


def test_configure_dns_settings_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.configure_dns_settings(
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].dns_settings
        mock_val = domains.DnsSettings(
            custom_dns=domains.DnsSettings.CustomDns(
                name_servers=["name_servers_value"]
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_configure_dns_settings_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_dns_settings(
            domains.ConfigureDnsSettingsRequest(),
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_configure_dns_settings_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_dns_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.configure_dns_settings(
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].dns_settings
        mock_val = domains.DnsSettings(
            custom_dns=domains.DnsSettings.CustomDns(
                name_servers=["name_servers_value"]
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_configure_dns_settings_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.configure_dns_settings(
            domains.ConfigureDnsSettingsRequest(),
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureContactSettingsRequest,
        dict,
    ],
)
def test_configure_contact_settings(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.configure_contact_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureContactSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_configure_contact_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        client.configure_contact_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureContactSettingsRequest()


@pytest.mark.asyncio
async def test_configure_contact_settings_async(
    transport: str = "grpc_asyncio",
    request_type=domains.ConfigureContactSettingsRequest,
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.configure_contact_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ConfigureContactSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_configure_contact_settings_async_from_dict():
    await test_configure_contact_settings_async(request_type=dict)


def test_configure_contact_settings_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureContactSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.configure_contact_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_configure_contact_settings_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureContactSettingsRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.configure_contact_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


def test_configure_contact_settings_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.configure_contact_settings(
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].contact_settings
        mock_val = domains.ContactSettings(
            privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_configure_contact_settings_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_contact_settings(
            domains.ConfigureContactSettingsRequest(),
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_configure_contact_settings_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.configure_contact_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.configure_contact_settings(
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val
        arg = args[0].contact_settings
        mock_val = domains.ContactSettings(
            privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_configure_contact_settings_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.configure_contact_settings(
            domains.ConfigureContactSettingsRequest(),
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ExportRegistrationRequest,
        dict,
    ],
)
def test_export_registration(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ExportRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        client.export_registration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ExportRegistrationRequest()


@pytest.mark.asyncio
async def test_export_registration_async(
    transport: str = "grpc_asyncio", request_type=domains.ExportRegistrationRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ExportRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_registration_async_from_dict():
    await test_export_registration_async(request_type=dict)


def test_export_registration_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ExportRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_registration(request)

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
async def test_export_registration_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ExportRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_registration(request)

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


def test_export_registration_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_registration(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_export_registration_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_registration(
            domains.ExportRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_export_registration_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_registration(
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
async def test_export_registration_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_registration(
            domains.ExportRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.DeleteRegistrationRequest,
        dict,
    ],
)
def test_delete_registration(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.DeleteRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        client.delete_registration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.DeleteRegistrationRequest()


@pytest.mark.asyncio
async def test_delete_registration_async(
    transport: str = "grpc_asyncio", request_type=domains.DeleteRegistrationRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.DeleteRegistrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_registration_async_from_dict():
    await test_delete_registration_async(request_type=dict)


def test_delete_registration_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.DeleteRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_registration(request)

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
async def test_delete_registration_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.DeleteRegistrationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_registration(request)

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


def test_delete_registration_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_registration(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_registration_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_registration(
            domains.DeleteRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_registration_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_registration(
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
async def test_delete_registration_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_registration(
            domains.DeleteRegistrationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveAuthorizationCodeRequest,
        dict,
    ],
)
def test_retrieve_authorization_code(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode(
            code="code_value",
        )
        response = client.retrieve_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_retrieve_authorization_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        client.retrieve_authorization_code()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveAuthorizationCodeRequest()


@pytest.mark.asyncio
async def test_retrieve_authorization_code_async(
    transport: str = "grpc_asyncio",
    request_type=domains.RetrieveAuthorizationCodeRequest,
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode(
                code="code_value",
            )
        )
        response = await client.retrieve_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


@pytest.mark.asyncio
async def test_retrieve_authorization_code_async_from_dict():
    await test_retrieve_authorization_code_async(request_type=dict)


def test_retrieve_authorization_code_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveAuthorizationCodeRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        call.return_value = domains.AuthorizationCode()
        client.retrieve_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_retrieve_authorization_code_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveAuthorizationCodeRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode()
        )
        await client.retrieve_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


def test_retrieve_authorization_code_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retrieve_authorization_code(
            registration="registration_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val


def test_retrieve_authorization_code_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_authorization_code(
            domains.RetrieveAuthorizationCodeRequest(),
            registration="registration_value",
        )


@pytest.mark.asyncio
async def test_retrieve_authorization_code_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retrieve_authorization_code(
            registration="registration_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_retrieve_authorization_code_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retrieve_authorization_code(
            domains.RetrieveAuthorizationCodeRequest(),
            registration="registration_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ResetAuthorizationCodeRequest,
        dict,
    ],
)
def test_reset_authorization_code(request_type, transport: str = "grpc"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode(
            code="code_value",
        )
        response = client.reset_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ResetAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_reset_authorization_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        client.reset_authorization_code()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ResetAuthorizationCodeRequest()


@pytest.mark.asyncio
async def test_reset_authorization_code_async(
    transport: str = "grpc_asyncio", request_type=domains.ResetAuthorizationCodeRequest
):
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode(
                code="code_value",
            )
        )
        response = await client.reset_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ResetAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


@pytest.mark.asyncio
async def test_reset_authorization_code_async_from_dict():
    await test_reset_authorization_code_async(request_type=dict)


def test_reset_authorization_code_field_headers():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ResetAuthorizationCodeRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        call.return_value = domains.AuthorizationCode()
        client.reset_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_reset_authorization_code_field_headers_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ResetAuthorizationCodeRequest()

    request.registration = "registration_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode()
        )
        await client.reset_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "registration=registration_value",
    ) in kw["metadata"]


def test_reset_authorization_code_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.reset_authorization_code(
            registration="registration_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val


def test_reset_authorization_code_flattened_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset_authorization_code(
            domains.ResetAuthorizationCodeRequest(),
            registration="registration_value",
        )


@pytest.mark.asyncio
async def test_reset_authorization_code_flattened_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.AuthorizationCode()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.reset_authorization_code(
            registration="registration_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].registration
        mock_val = "registration_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_reset_authorization_code_flattened_error_async():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.reset_authorization_code(
            domains.ResetAuthorizationCodeRequest(),
            registration="registration_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.SearchDomainsRequest,
        dict,
    ],
)
def test_search_domains_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.SearchDomainsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.SearchDomainsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_domains(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.SearchDomainsResponse)


def test_search_domains_rest_required_fields(request_type=domains.SearchDomainsRequest):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["query"] = ""
    request_init["location"] = ""
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
    assert "query" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_domains._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "query" in jsonified_request
    assert jsonified_request["query"] == request_init["query"]

    jsonified_request["query"] = "query_value"
    jsonified_request["location"] = "location_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_domains._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("query",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "query" in jsonified_request
    assert jsonified_request["query"] == "query_value"
    assert "location" in jsonified_request
    assert jsonified_request["location"] == "location_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.SearchDomainsResponse()
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

            pb_return_value = domains.SearchDomainsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_domains(request)

            expected_params = [
                (
                    "query",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_domains_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_domains._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("query",))
        & set(
            (
                "query",
                "location",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_domains_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_search_domains"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_search_domains"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.SearchDomainsRequest.pb(domains.SearchDomainsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = domains.SearchDomainsResponse.to_json(
            domains.SearchDomainsResponse()
        )

        request = domains.SearchDomainsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.SearchDomainsResponse()

        client.search_domains(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_domains_rest_bad_request(
    transport: str = "rest", request_type=domains.SearchDomainsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
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
        client.search_domains(request)


def test_search_domains_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.SearchDomainsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"location": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            location="location_value",
            query="query_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.SearchDomainsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.search_domains(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{location=projects/*/locations/*}/registrations:searchDomains"
            % client.transport._host,
            args[1],
        )


def test_search_domains_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_domains(
            domains.SearchDomainsRequest(),
            location="location_value",
            query="query_value",
        )


def test_search_domains_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveRegisterParametersRequest,
        dict,
    ],
)
def test_retrieve_register_parameters_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.RetrieveRegisterParametersResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.RetrieveRegisterParametersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.retrieve_register_parameters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveRegisterParametersResponse)


def test_retrieve_register_parameters_rest_required_fields(
    request_type=domains.RetrieveRegisterParametersRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["domain_name"] = ""
    request_init["location"] = ""
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
    assert "domainName" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retrieve_register_parameters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "domainName" in jsonified_request
    assert jsonified_request["domainName"] == request_init["domain_name"]

    jsonified_request["domainName"] = "domain_name_value"
    jsonified_request["location"] = "location_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retrieve_register_parameters._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("domain_name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "domainName" in jsonified_request
    assert jsonified_request["domainName"] == "domain_name_value"
    assert "location" in jsonified_request
    assert jsonified_request["location"] == "location_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.RetrieveRegisterParametersResponse()
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

            pb_return_value = domains.RetrieveRegisterParametersResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.retrieve_register_parameters(request)

            expected_params = [
                (
                    "domainName",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_retrieve_register_parameters_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.retrieve_register_parameters._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("domainName",))
        & set(
            (
                "domainName",
                "location",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_retrieve_register_parameters_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_retrieve_register_parameters"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_retrieve_register_parameters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.RetrieveRegisterParametersRequest.pb(
            domains.RetrieveRegisterParametersRequest()
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
        req.return_value._content = domains.RetrieveRegisterParametersResponse.to_json(
            domains.RetrieveRegisterParametersResponse()
        )

        request = domains.RetrieveRegisterParametersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.RetrieveRegisterParametersResponse()

        client.retrieve_register_parameters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_retrieve_register_parameters_rest_bad_request(
    transport: str = "rest", request_type=domains.RetrieveRegisterParametersRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
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
        client.retrieve_register_parameters(request)


def test_retrieve_register_parameters_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.RetrieveRegisterParametersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"location": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            location="location_value",
            domain_name="domain_name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.RetrieveRegisterParametersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.retrieve_register_parameters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{location=projects/*/locations/*}/registrations:retrieveRegisterParameters"
            % client.transport._host,
            args[1],
        )


def test_retrieve_register_parameters_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_register_parameters(
            domains.RetrieveRegisterParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


def test_retrieve_register_parameters_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RegisterDomainRequest,
        dict,
    ],
)
def test_register_domain_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        response = client.register_domain(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_register_domain_rest_required_fields(
    request_type=domains.RegisterDomainRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).register_domain._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).register_domain._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DomainsClient(
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

            response = client.register_domain(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_register_domain_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.register_domain._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "registration",
                "yearlyPrice",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_register_domain_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_register_domain"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_register_domain"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.RegisterDomainRequest.pb(domains.RegisterDomainRequest())
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

        request = domains.RegisterDomainRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.register_domain(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_register_domain_rest_bad_request(
    transport: str = "rest", request_type=domains.RegisterDomainRequest
):
    client = DomainsClient(
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
        client.register_domain(request)


def test_register_domain_rest_flattened():
    client = DomainsClient(
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
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.register_domain(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/registrations:register"
            % client.transport._host,
            args[1],
        )


def test_register_domain_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.register_domain(
            domains.RegisterDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )


def test_register_domain_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveTransferParametersRequest,
        dict,
    ],
)
def test_retrieve_transfer_parameters_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.RetrieveTransferParametersResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.RetrieveTransferParametersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.retrieve_transfer_parameters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.RetrieveTransferParametersResponse)


def test_retrieve_transfer_parameters_rest_required_fields(
    request_type=domains.RetrieveTransferParametersRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["domain_name"] = ""
    request_init["location"] = ""
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
    assert "domainName" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retrieve_transfer_parameters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "domainName" in jsonified_request
    assert jsonified_request["domainName"] == request_init["domain_name"]

    jsonified_request["domainName"] = "domain_name_value"
    jsonified_request["location"] = "location_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retrieve_transfer_parameters._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("domain_name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "domainName" in jsonified_request
    assert jsonified_request["domainName"] == "domain_name_value"
    assert "location" in jsonified_request
    assert jsonified_request["location"] == "location_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.RetrieveTransferParametersResponse()
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

            pb_return_value = domains.RetrieveTransferParametersResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.retrieve_transfer_parameters(request)

            expected_params = [
                (
                    "domainName",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_retrieve_transfer_parameters_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.retrieve_transfer_parameters._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("domainName",))
        & set(
            (
                "domainName",
                "location",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_retrieve_transfer_parameters_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_retrieve_transfer_parameters"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_retrieve_transfer_parameters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.RetrieveTransferParametersRequest.pb(
            domains.RetrieveTransferParametersRequest()
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
        req.return_value._content = domains.RetrieveTransferParametersResponse.to_json(
            domains.RetrieveTransferParametersResponse()
        )

        request = domains.RetrieveTransferParametersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.RetrieveTransferParametersResponse()

        client.retrieve_transfer_parameters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_retrieve_transfer_parameters_rest_bad_request(
    transport: str = "rest", request_type=domains.RetrieveTransferParametersRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
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
        client.retrieve_transfer_parameters(request)


def test_retrieve_transfer_parameters_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.RetrieveTransferParametersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"location": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            location="location_value",
            domain_name="domain_name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.RetrieveTransferParametersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.retrieve_transfer_parameters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{location=projects/*/locations/*}/registrations:retrieveTransferParameters"
            % client.transport._host,
            args[1],
        )


def test_retrieve_transfer_parameters_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_transfer_parameters(
            domains.RetrieveTransferParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


def test_retrieve_transfer_parameters_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.TransferDomainRequest,
        dict,
    ],
)
def test_transfer_domain_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        response = client.transfer_domain(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_transfer_domain_rest_required_fields(
    request_type=domains.TransferDomainRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).transfer_domain._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).transfer_domain._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DomainsClient(
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

            response = client.transfer_domain(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_transfer_domain_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.transfer_domain._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "registration",
                "yearlyPrice",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_transfer_domain_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_transfer_domain"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_transfer_domain"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.TransferDomainRequest.pb(domains.TransferDomainRequest())
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

        request = domains.TransferDomainRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.transfer_domain(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_transfer_domain_rest_bad_request(
    transport: str = "rest", request_type=domains.TransferDomainRequest
):
    client = DomainsClient(
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
        client.transfer_domain(request)


def test_transfer_domain_rest_flattened():
    client = DomainsClient(
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
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.transfer_domain(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/registrations:transfer"
            % client.transport._host,
            args[1],
        )


def test_transfer_domain_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.transfer_domain(
            domains.TransferDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
            authorization_code=domains.AuthorizationCode(code="code_value"),
        )


def test_transfer_domain_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ListRegistrationsRequest,
        dict,
    ],
)
def test_list_registrations_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.ListRegistrationsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.ListRegistrationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_registrations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRegistrationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_registrations_rest_required_fields(
    request_type=domains.ListRegistrationsRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).list_registrations._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_registrations._get_unset_required_fields(jsonified_request)
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
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.ListRegistrationsResponse()
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

            pb_return_value = domains.ListRegistrationsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_registrations(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_registrations_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_registrations._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_registrations_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_list_registrations"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_list_registrations"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ListRegistrationsRequest.pb(
            domains.ListRegistrationsRequest()
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
        req.return_value._content = domains.ListRegistrationsResponse.to_json(
            domains.ListRegistrationsResponse()
        )

        request = domains.ListRegistrationsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.ListRegistrationsResponse()

        client.list_registrations(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_registrations_rest_bad_request(
    transport: str = "rest", request_type=domains.ListRegistrationsRequest
):
    client = DomainsClient(
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
        client.list_registrations(request)


def test_list_registrations_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.ListRegistrationsResponse()

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
        pb_return_value = domains.ListRegistrationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_registrations(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/registrations"
            % client.transport._host,
            args[1],
        )


def test_list_registrations_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_registrations(
            domains.ListRegistrationsRequest(),
            parent="parent_value",
        )


def test_list_registrations_rest_pager(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                    domains.Registration(),
                ],
                next_page_token="abc",
            ),
            domains.ListRegistrationsResponse(
                registrations=[],
                next_page_token="def",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                ],
                next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[
                    domains.Registration(),
                    domains.Registration(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(domains.ListRegistrationsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_registrations(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, domains.Registration) for i in results)

        pages = list(client.list_registrations(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        domains.GetRegistrationRequest,
        dict,
    ],
)
def test_get_registration_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.Registration(
            name="name_value",
            domain_name="domain_name_value",
            state=domains.Registration.State.REGISTRATION_PENDING,
            issues=[domains.Registration.Issue.CONTACT_SUPPORT],
            supported_privacy=[domains.ContactPrivacy.PUBLIC_CONTACT_DATA],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.Registration.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_registration(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.Registration)
    assert response.name == "name_value"
    assert response.domain_name == "domain_name_value"
    assert response.state == domains.Registration.State.REGISTRATION_PENDING
    assert response.issues == [domains.Registration.Issue.CONTACT_SUPPORT]
    assert response.supported_privacy == [domains.ContactPrivacy.PUBLIC_CONTACT_DATA]


def test_get_registration_rest_required_fields(
    request_type=domains.GetRegistrationRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).get_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.Registration()
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

            pb_return_value = domains.Registration.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_registration(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_registration_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_registration._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_registration_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_get_registration"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_get_registration"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.GetRegistrationRequest.pb(domains.GetRegistrationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = domains.Registration.to_json(domains.Registration())

        request = domains.GetRegistrationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.Registration()

        client.get_registration(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_registration_rest_bad_request(
    transport: str = "rest", request_type=domains.GetRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
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
        client.get_registration(request)


def test_get_registration_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.Registration()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.Registration.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_registration(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registrations/*}"
            % client.transport._host,
            args[1],
        )


def test_get_registration_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_registration(
            domains.GetRegistrationRequest(),
            name="name_value",
        )


def test_get_registration_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.UpdateRegistrationRequest,
        dict,
    ],
)
def test_update_registration_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": {
            "name": "projects/sample1/locations/sample2/registrations/sample3"
        }
    }
    request_init["registration"] = {
        "name": "projects/sample1/locations/sample2/registrations/sample3",
        "domain_name": "domain_name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "expire_time": {},
        "state": 1,
        "issues": [1],
        "labels": {},
        "management_settings": {"renewal_method": 1, "transfer_lock_state": 1},
        "dns_settings": {
            "custom_dns": {
                "name_servers": ["name_servers_value1", "name_servers_value2"],
                "ds_records": [
                    {
                        "key_tag": 740,
                        "algorithm": 1,
                        "digest_type": 1,
                        "digest": "digest_value",
                    }
                ],
            },
            "google_domains_dns": {
                "name_servers": ["name_servers_value1", "name_servers_value2"],
                "ds_state": 1,
                "ds_records": {},
            },
            "glue_records": [
                {
                    "host_name": "host_name_value",
                    "ipv4_addresses": [
                        "ipv4_addresses_value1",
                        "ipv4_addresses_value2",
                    ],
                    "ipv6_addresses": [
                        "ipv6_addresses_value1",
                        "ipv6_addresses_value2",
                    ],
                }
            ],
        },
        "contact_settings": {
            "privacy": 1,
            "registrant_contact": {
                "postal_address": {
                    "revision": 879,
                    "region_code": "region_code_value",
                    "language_code": "language_code_value",
                    "postal_code": "postal_code_value",
                    "sorting_code": "sorting_code_value",
                    "administrative_area": "administrative_area_value",
                    "locality": "locality_value",
                    "sublocality": "sublocality_value",
                    "address_lines": ["address_lines_value1", "address_lines_value2"],
                    "recipients": ["recipients_value1", "recipients_value2"],
                    "organization": "organization_value",
                },
                "email": "email_value",
                "phone_number": "phone_number_value",
                "fax_number": "fax_number_value",
            },
            "admin_contact": {},
            "technical_contact": {},
        },
        "pending_contact_settings": {},
        "supported_privacy": [1],
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
        response = client.update_registration(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_registration_rest_required_fields(
    request_type=domains.UpdateRegistrationRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).update_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_registration._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DomainsClient(
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

            response = client.update_registration(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_registration_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_registration._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("updateMask",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_registration_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_update_registration"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_update_registration"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.UpdateRegistrationRequest.pb(
            domains.UpdateRegistrationRequest()
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

        request = domains.UpdateRegistrationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_registration(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_registration_rest_bad_request(
    transport: str = "rest", request_type=domains.UpdateRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": {
            "name": "projects/sample1/locations/sample2/registrations/sample3"
        }
    }
    request_init["registration"] = {
        "name": "projects/sample1/locations/sample2/registrations/sample3",
        "domain_name": "domain_name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "expire_time": {},
        "state": 1,
        "issues": [1],
        "labels": {},
        "management_settings": {"renewal_method": 1, "transfer_lock_state": 1},
        "dns_settings": {
            "custom_dns": {
                "name_servers": ["name_servers_value1", "name_servers_value2"],
                "ds_records": [
                    {
                        "key_tag": 740,
                        "algorithm": 1,
                        "digest_type": 1,
                        "digest": "digest_value",
                    }
                ],
            },
            "google_domains_dns": {
                "name_servers": ["name_servers_value1", "name_servers_value2"],
                "ds_state": 1,
                "ds_records": {},
            },
            "glue_records": [
                {
                    "host_name": "host_name_value",
                    "ipv4_addresses": [
                        "ipv4_addresses_value1",
                        "ipv4_addresses_value2",
                    ],
                    "ipv6_addresses": [
                        "ipv6_addresses_value1",
                        "ipv6_addresses_value2",
                    ],
                }
            ],
        },
        "contact_settings": {
            "privacy": 1,
            "registrant_contact": {
                "postal_address": {
                    "revision": 879,
                    "region_code": "region_code_value",
                    "language_code": "language_code_value",
                    "postal_code": "postal_code_value",
                    "sorting_code": "sorting_code_value",
                    "administrative_area": "administrative_area_value",
                    "locality": "locality_value",
                    "sublocality": "sublocality_value",
                    "address_lines": ["address_lines_value1", "address_lines_value2"],
                    "recipients": ["recipients_value1", "recipients_value2"],
                    "organization": "organization_value",
                },
                "email": "email_value",
                "phone_number": "phone_number_value",
                "fax_number": "fax_number_value",
            },
            "admin_contact": {},
            "technical_contact": {},
        },
        "pending_contact_settings": {},
        "supported_privacy": [1],
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
        client.update_registration(request)


def test_update_registration_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": {
                "name": "projects/sample1/locations/sample2/registrations/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_registration(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration.name=projects/*/locations/*/registrations/*}"
            % client.transport._host,
            args[1],
        )


def test_update_registration_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_registration(
            domains.UpdateRegistrationRequest(),
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_registration_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureManagementSettingsRequest,
        dict,
    ],
)
def test_configure_management_settings_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        response = client.configure_management_settings(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_configure_management_settings_rest_required_fields(
    request_type=domains.ConfigureManagementSettingsRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["registration"] = ""
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
    ).configure_management_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["registration"] = "registration_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).configure_management_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "registration" in jsonified_request
    assert jsonified_request["registration"] == "registration_value"

    client = DomainsClient(
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

            response = client.configure_management_settings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_configure_management_settings_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.configure_management_settings._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "registration",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_configure_management_settings_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_configure_management_settings"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_configure_management_settings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ConfigureManagementSettingsRequest.pb(
            domains.ConfigureManagementSettingsRequest()
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

        request = domains.ConfigureManagementSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.configure_management_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_configure_management_settings_rest_bad_request(
    transport: str = "rest", request_type=domains.ConfigureManagementSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        client.configure_management_settings(request)


def test_configure_management_settings_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
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

        client.configure_management_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration=projects/*/locations/*/registrations/*}:configureManagementSettings"
            % client.transport._host,
            args[1],
        )


def test_configure_management_settings_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_management_settings(
            domains.ConfigureManagementSettingsRequest(),
            registration="registration_value",
            management_settings=domains.ManagementSettings(
                renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_configure_management_settings_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureDnsSettingsRequest,
        dict,
    ],
)
def test_configure_dns_settings_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        response = client.configure_dns_settings(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_configure_dns_settings_rest_required_fields(
    request_type=domains.ConfigureDnsSettingsRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["registration"] = ""
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
    ).configure_dns_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["registration"] = "registration_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).configure_dns_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "registration" in jsonified_request
    assert jsonified_request["registration"] == "registration_value"

    client = DomainsClient(
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

            response = client.configure_dns_settings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_configure_dns_settings_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.configure_dns_settings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "registration",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_configure_dns_settings_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_configure_dns_settings"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_configure_dns_settings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ConfigureDnsSettingsRequest.pb(
            domains.ConfigureDnsSettingsRequest()
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

        request = domains.ConfigureDnsSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.configure_dns_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_configure_dns_settings_rest_bad_request(
    transport: str = "rest", request_type=domains.ConfigureDnsSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        client.configure_dns_settings(request)


def test_configure_dns_settings_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
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

        client.configure_dns_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration=projects/*/locations/*/registrations/*}:configureDnsSettings"
            % client.transport._host,
            args[1],
        )


def test_configure_dns_settings_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_dns_settings(
            domains.ConfigureDnsSettingsRequest(),
            registration="registration_value",
            dns_settings=domains.DnsSettings(
                custom_dns=domains.DnsSettings.CustomDns(
                    name_servers=["name_servers_value"]
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_configure_dns_settings_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ConfigureContactSettingsRequest,
        dict,
    ],
)
def test_configure_contact_settings_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        response = client.configure_contact_settings(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_configure_contact_settings_rest_required_fields(
    request_type=domains.ConfigureContactSettingsRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["registration"] = ""
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
    ).configure_contact_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["registration"] = "registration_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).configure_contact_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "registration" in jsonified_request
    assert jsonified_request["registration"] == "registration_value"

    client = DomainsClient(
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

            response = client.configure_contact_settings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_configure_contact_settings_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.configure_contact_settings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "registration",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_configure_contact_settings_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_configure_contact_settings"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_configure_contact_settings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ConfigureContactSettingsRequest.pb(
            domains.ConfigureContactSettingsRequest()
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

        request = domains.ConfigureContactSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.configure_contact_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_configure_contact_settings_rest_bad_request(
    transport: str = "rest", request_type=domains.ConfigureContactSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        client.configure_contact_settings(request)


def test_configure_contact_settings_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
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

        client.configure_contact_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration=projects/*/locations/*/registrations/*}:configureContactSettings"
            % client.transport._host,
            args[1],
        )


def test_configure_contact_settings_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.configure_contact_settings(
            domains.ConfigureContactSettingsRequest(),
            registration="registration_value",
            contact_settings=domains.ContactSettings(
                privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_configure_contact_settings_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ExportRegistrationRequest,
        dict,
    ],
)
def test_export_registration_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
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
        response = client.export_registration(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_export_registration_rest_required_fields(
    request_type=domains.ExportRegistrationRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).export_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).export_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DomainsClient(
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

            response = client.export_registration(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_export_registration_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.export_registration._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_export_registration_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_export_registration"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_export_registration"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ExportRegistrationRequest.pb(
            domains.ExportRegistrationRequest()
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

        request = domains.ExportRegistrationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.export_registration(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_export_registration_rest_bad_request(
    transport: str = "rest", request_type=domains.ExportRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
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
        client.export_registration(request)


def test_export_registration_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registrations/sample3"
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

        client.export_registration(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registrations/*}:export"
            % client.transport._host,
            args[1],
        )


def test_export_registration_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_registration(
            domains.ExportRegistrationRequest(),
            name="name_value",
        )


def test_export_registration_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.DeleteRegistrationRequest,
        dict,
    ],
)
def test_delete_registration_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
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
        response = client.delete_registration(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_registration_rest_required_fields(
    request_type=domains.DeleteRegistrationRequest,
):
    transport_class = transports.DomainsRestTransport

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
    ).delete_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_registration._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DomainsClient(
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

            response = client.delete_registration(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_registration_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_registration._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_registration_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DomainsRestInterceptor, "post_delete_registration"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_delete_registration"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.DeleteRegistrationRequest.pb(
            domains.DeleteRegistrationRequest()
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

        request = domains.DeleteRegistrationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_registration(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_registration_rest_bad_request(
    transport: str = "rest", request_type=domains.DeleteRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registrations/sample3"}
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
        client.delete_registration(request)


def test_delete_registration_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registrations/sample3"
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

        client.delete_registration(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registrations/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_registration_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_registration(
            domains.DeleteRegistrationRequest(),
            name="name_value",
        )


def test_delete_registration_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.RetrieveAuthorizationCodeRequest,
        dict,
    ],
)
def test_retrieve_authorization_code_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.AuthorizationCode(
            code="code_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.AuthorizationCode.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.retrieve_authorization_code(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_retrieve_authorization_code_rest_required_fields(
    request_type=domains.RetrieveAuthorizationCodeRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["registration"] = ""
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
    ).retrieve_authorization_code._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["registration"] = "registration_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retrieve_authorization_code._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "registration" in jsonified_request
    assert jsonified_request["registration"] == "registration_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.AuthorizationCode()
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

            pb_return_value = domains.AuthorizationCode.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.retrieve_authorization_code(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_retrieve_authorization_code_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.retrieve_authorization_code._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("registration",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_retrieve_authorization_code_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_retrieve_authorization_code"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_retrieve_authorization_code"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.RetrieveAuthorizationCodeRequest.pb(
            domains.RetrieveAuthorizationCodeRequest()
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
        req.return_value._content = domains.AuthorizationCode.to_json(
            domains.AuthorizationCode()
        )

        request = domains.RetrieveAuthorizationCodeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.AuthorizationCode()

        client.retrieve_authorization_code(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_retrieve_authorization_code_rest_bad_request(
    transport: str = "rest", request_type=domains.RetrieveAuthorizationCodeRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        client.retrieve_authorization_code(request)


def test_retrieve_authorization_code_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.AuthorizationCode()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration="registration_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.AuthorizationCode.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.retrieve_authorization_code(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration=projects/*/locations/*/registrations/*}:retrieveAuthorizationCode"
            % client.transport._host,
            args[1],
        )


def test_retrieve_authorization_code_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_authorization_code(
            domains.RetrieveAuthorizationCodeRequest(),
            registration="registration_value",
        )


def test_retrieve_authorization_code_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        domains.ResetAuthorizationCodeRequest,
        dict,
    ],
)
def test_reset_authorization_code_rest(request_type):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.AuthorizationCode(
            code="code_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.AuthorizationCode.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.reset_authorization_code(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_reset_authorization_code_rest_required_fields(
    request_type=domains.ResetAuthorizationCodeRequest,
):
    transport_class = transports.DomainsRestTransport

    request_init = {}
    request_init["registration"] = ""
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
    ).reset_authorization_code._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["registration"] = "registration_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).reset_authorization_code._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "registration" in jsonified_request
    assert jsonified_request["registration"] == "registration_value"

    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = domains.AuthorizationCode()
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

            pb_return_value = domains.AuthorizationCode.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.reset_authorization_code(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_reset_authorization_code_rest_unset_required_fields():
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.reset_authorization_code._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("registration",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_reset_authorization_code_rest_interceptors(null_interceptor):
    transport = transports.DomainsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.DomainsRestInterceptor(),
    )
    client = DomainsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DomainsRestInterceptor, "post_reset_authorization_code"
    ) as post, mock.patch.object(
        transports.DomainsRestInterceptor, "pre_reset_authorization_code"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = domains.ResetAuthorizationCodeRequest.pb(
            domains.ResetAuthorizationCodeRequest()
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
        req.return_value._content = domains.AuthorizationCode.to_json(
            domains.AuthorizationCode()
        )

        request = domains.ResetAuthorizationCodeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = domains.AuthorizationCode()

        client.reset_authorization_code(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_reset_authorization_code_rest_bad_request(
    transport: str = "rest", request_type=domains.ResetAuthorizationCodeRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "registration": "projects/sample1/locations/sample2/registrations/sample3"
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
        client.reset_authorization_code(request)


def test_reset_authorization_code_rest_flattened():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = domains.AuthorizationCode()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "registration": "projects/sample1/locations/sample2/registrations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            registration="registration_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = domains.AuthorizationCode.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.reset_authorization_code(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{registration=projects/*/locations/*/registrations/*}:resetAuthorizationCode"
            % client.transport._host,
            args[1],
        )


def test_reset_authorization_code_rest_flattened_error(transport: str = "rest"):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset_authorization_code(
            domains.ResetAuthorizationCodeRequest(),
            registration="registration_value",
        )


def test_reset_authorization_code_rest_error():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DomainsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DomainsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DomainsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DomainsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DomainsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DomainsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DomainsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DomainsGrpcTransport,
        transports.DomainsGrpcAsyncIOTransport,
        transports.DomainsRestTransport,
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
    transport = DomainsClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DomainsGrpcTransport,
    )


def test_domains_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DomainsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_domains_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.domains_v1.services.domains.transports.DomainsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DomainsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "search_domains",
        "retrieve_register_parameters",
        "register_domain",
        "retrieve_transfer_parameters",
        "transfer_domain",
        "list_registrations",
        "get_registration",
        "update_registration",
        "configure_management_settings",
        "configure_dns_settings",
        "configure_contact_settings",
        "export_registration",
        "delete_registration",
        "retrieve_authorization_code",
        "reset_authorization_code",
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


def test_domains_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.domains_v1.services.domains.transports.DomainsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DomainsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_domains_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.domains_v1.services.domains.transports.DomainsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DomainsTransport()
        adc.assert_called_once()


def test_domains_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DomainsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DomainsGrpcTransport,
        transports.DomainsGrpcAsyncIOTransport,
    ],
)
def test_domains_transport_auth_adc(transport_class):
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
        transports.DomainsGrpcTransport,
        transports.DomainsGrpcAsyncIOTransport,
        transports.DomainsRestTransport,
    ],
)
def test_domains_transport_auth_gdch_credentials(transport_class):
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
        (transports.DomainsGrpcTransport, grpc_helpers),
        (transports.DomainsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_domains_transport_create_channel(transport_class, grpc_helpers):
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
            "domains.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="domains.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport],
)
def test_domains_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_domains_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DomainsRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_domains_rest_lro_client():
    client = DomainsClient(
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
def test_domains_host_no_port(transport_name):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="domains.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "domains.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://domains.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_domains_host_with_port(transport_name):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="domains.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "domains.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://domains.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_domains_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DomainsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DomainsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.search_domains._session
    session2 = client2.transport.search_domains._session
    assert session1 != session2
    session1 = client1.transport.retrieve_register_parameters._session
    session2 = client2.transport.retrieve_register_parameters._session
    assert session1 != session2
    session1 = client1.transport.register_domain._session
    session2 = client2.transport.register_domain._session
    assert session1 != session2
    session1 = client1.transport.retrieve_transfer_parameters._session
    session2 = client2.transport.retrieve_transfer_parameters._session
    assert session1 != session2
    session1 = client1.transport.transfer_domain._session
    session2 = client2.transport.transfer_domain._session
    assert session1 != session2
    session1 = client1.transport.list_registrations._session
    session2 = client2.transport.list_registrations._session
    assert session1 != session2
    session1 = client1.transport.get_registration._session
    session2 = client2.transport.get_registration._session
    assert session1 != session2
    session1 = client1.transport.update_registration._session
    session2 = client2.transport.update_registration._session
    assert session1 != session2
    session1 = client1.transport.configure_management_settings._session
    session2 = client2.transport.configure_management_settings._session
    assert session1 != session2
    session1 = client1.transport.configure_dns_settings._session
    session2 = client2.transport.configure_dns_settings._session
    assert session1 != session2
    session1 = client1.transport.configure_contact_settings._session
    session2 = client2.transport.configure_contact_settings._session
    assert session1 != session2
    session1 = client1.transport.export_registration._session
    session2 = client2.transport.export_registration._session
    assert session1 != session2
    session1 = client1.transport.delete_registration._session
    session2 = client2.transport.delete_registration._session
    assert session1 != session2
    session1 = client1.transport.retrieve_authorization_code._session
    session2 = client2.transport.retrieve_authorization_code._session
    assert session1 != session2
    session1 = client1.transport.reset_authorization_code._session
    session2 = client2.transport.reset_authorization_code._session
    assert session1 != session2


def test_domains_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DomainsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_domains_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DomainsGrpcAsyncIOTransport(
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
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport],
)
def test_domains_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport],
)
def test_domains_transport_channel_mtls_with_adc(transport_class):
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


def test_domains_grpc_lro_client():
    client = DomainsClient(
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


def test_domains_grpc_lro_async_client():
    client = DomainsAsyncClient(
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


def test_registration_path():
    project = "squid"
    location = "clam"
    registration = "whelk"
    expected = (
        "projects/{project}/locations/{location}/registrations/{registration}".format(
            project=project,
            location=location,
            registration=registration,
        )
    )
    actual = DomainsClient.registration_path(project, location, registration)
    assert expected == actual


def test_parse_registration_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "registration": "nudibranch",
    }
    path = DomainsClient.registration_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_registration_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DomainsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = DomainsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DomainsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = DomainsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DomainsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = DomainsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DomainsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = DomainsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DomainsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = DomainsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DomainsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DomainsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DomainsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DomainsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DomainsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DomainsAsyncClient(
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
        client = DomainsClient(
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
        client = DomainsClient(
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
        (DomainsClient, transports.DomainsGrpcTransport),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport),
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
