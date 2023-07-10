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
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.network_management_v1.services.reachability_service import (
    ReachabilityServiceAsyncClient,
    ReachabilityServiceClient,
    pagers,
    transports,
)
from google.cloud.network_management_v1.types import (
    connectivity_test,
    reachability,
    trace,
)


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

    assert ReachabilityServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ReachabilityServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ReachabilityServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ReachabilityServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ReachabilityServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ReachabilityServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ReachabilityServiceClient, "grpc"),
        (ReachabilityServiceAsyncClient, "grpc_asyncio"),
        (ReachabilityServiceClient, "rest"),
    ],
)
def test_reachability_service_client_from_service_account_info(
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

        assert client.transport._host == (
            "networkmanagement.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://networkmanagement.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ReachabilityServiceGrpcTransport, "grpc"),
        (transports.ReachabilityServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.ReachabilityServiceRestTransport, "rest"),
    ],
)
def test_reachability_service_client_service_account_always_use_jwt(
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
        (ReachabilityServiceClient, "grpc"),
        (ReachabilityServiceAsyncClient, "grpc_asyncio"),
        (ReachabilityServiceClient, "rest"),
    ],
)
def test_reachability_service_client_from_service_account_file(
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

        assert client.transport._host == (
            "networkmanagement.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://networkmanagement.googleapis.com"
        )


def test_reachability_service_client_get_transport_class():
    transport = ReachabilityServiceClient.get_transport_class()
    available_transports = [
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceRestTransport,
    ]
    assert transport in available_transports

    transport = ReachabilityServiceClient.get_transport_class("grpc")
    assert transport == transports.ReachabilityServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    ReachabilityServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceClient),
)
@mock.patch.object(
    ReachabilityServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceAsyncClient),
)
def test_reachability_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ReachabilityServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ReachabilityServiceClient, "get_transport_class") as gtc:
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
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceRestTransport,
            "rest",
            "true",
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    ReachabilityServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceClient),
)
@mock.patch.object(
    ReachabilityServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_reachability_service_client_mtls_env_auto(
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
    "client_class", [ReachabilityServiceClient, ReachabilityServiceAsyncClient]
)
@mock.patch.object(
    ReachabilityServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceClient),
)
@mock.patch.object(
    ReachabilityServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ReachabilityServiceAsyncClient),
)
def test_reachability_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceRestTransport,
            "rest",
        ),
    ],
)
def test_reachability_service_client_client_options_scopes(
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
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            ReachabilityServiceClient,
            transports.ReachabilityServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_reachability_service_client_client_options_credentials_file(
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


def test_reachability_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.network_management_v1.services.reachability_service.transports.ReachabilityServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ReachabilityServiceClient(
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
            ReachabilityServiceClient,
            transports.ReachabilityServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_reachability_service_client_create_channel_credentials_file(
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
            "networkmanagement.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="networkmanagement.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.ListConnectivityTestsRequest,
        dict,
    ],
)
def test_list_connectivity_tests(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = reachability.ListConnectivityTestsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_connectivity_tests(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.ListConnectivityTestsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectivityTestsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_connectivity_tests_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        client.list_connectivity_tests()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.ListConnectivityTestsRequest()


@pytest.mark.asyncio
async def test_list_connectivity_tests_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.ListConnectivityTestsRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reachability.ListConnectivityTestsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_connectivity_tests(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.ListConnectivityTestsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectivityTestsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_connectivity_tests_async_from_dict():
    await test_list_connectivity_tests_async(request_type=dict)


def test_list_connectivity_tests_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.ListConnectivityTestsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        call.return_value = reachability.ListConnectivityTestsResponse()
        client.list_connectivity_tests(request)

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
async def test_list_connectivity_tests_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.ListConnectivityTestsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reachability.ListConnectivityTestsResponse()
        )
        await client.list_connectivity_tests(request)

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


def test_list_connectivity_tests_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = reachability.ListConnectivityTestsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_connectivity_tests(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_connectivity_tests_flattened_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_connectivity_tests(
            reachability.ListConnectivityTestsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_connectivity_tests_flattened_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = reachability.ListConnectivityTestsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            reachability.ListConnectivityTestsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_connectivity_tests(
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
async def test_list_connectivity_tests_flattened_error_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_connectivity_tests(
            reachability.ListConnectivityTestsRequest(),
            parent="parent_value",
        )


def test_list_connectivity_tests_pager(transport_name: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="abc",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[],
                next_page_token="def",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="ghi",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_connectivity_tests(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, connectivity_test.ConnectivityTest) for i in results)


def test_list_connectivity_tests_pages(transport_name: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="abc",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[],
                next_page_token="def",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="ghi",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_connectivity_tests(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_connectivity_tests_async_pager():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="abc",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[],
                next_page_token="def",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="ghi",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_connectivity_tests(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, connectivity_test.ConnectivityTest) for i in responses)


@pytest.mark.asyncio
async def test_list_connectivity_tests_async_pages():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connectivity_tests),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="abc",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[],
                next_page_token="def",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="ghi",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_connectivity_tests(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.GetConnectivityTestRequest,
        dict,
    ],
)
def test_get_connectivity_test(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = connectivity_test.ConnectivityTest(
            name="name_value",
            description="description_value",
            protocol="protocol_value",
            related_projects=["related_projects_value"],
            display_name="display_name_value",
        )
        response = client.get_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.GetConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, connectivity_test.ConnectivityTest)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.protocol == "protocol_value"
    assert response.related_projects == ["related_projects_value"]
    assert response.display_name == "display_name_value"


def test_get_connectivity_test_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        client.get_connectivity_test()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.GetConnectivityTestRequest()


@pytest.mark.asyncio
async def test_get_connectivity_test_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.GetConnectivityTestRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            connectivity_test.ConnectivityTest(
                name="name_value",
                description="description_value",
                protocol="protocol_value",
                related_projects=["related_projects_value"],
                display_name="display_name_value",
            )
        )
        response = await client.get_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.GetConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, connectivity_test.ConnectivityTest)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.protocol == "protocol_value"
    assert response.related_projects == ["related_projects_value"]
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_connectivity_test_async_from_dict():
    await test_get_connectivity_test_async(request_type=dict)


def test_get_connectivity_test_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.GetConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        call.return_value = connectivity_test.ConnectivityTest()
        client.get_connectivity_test(request)

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
async def test_get_connectivity_test_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.GetConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            connectivity_test.ConnectivityTest()
        )
        await client.get_connectivity_test(request)

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


def test_get_connectivity_test_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = connectivity_test.ConnectivityTest()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_connectivity_test(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_connectivity_test_flattened_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connectivity_test(
            reachability.GetConnectivityTestRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_connectivity_test_flattened_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = connectivity_test.ConnectivityTest()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            connectivity_test.ConnectivityTest()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_connectivity_test(
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
async def test_get_connectivity_test_flattened_error_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_connectivity_test(
            reachability.GetConnectivityTestRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.CreateConnectivityTestRequest,
        dict,
    ],
)
def test_create_connectivity_test(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.CreateConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_connectivity_test_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        client.create_connectivity_test()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.CreateConnectivityTestRequest()


@pytest.mark.asyncio
async def test_create_connectivity_test_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.CreateConnectivityTestRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.CreateConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_connectivity_test_async_from_dict():
    await test_create_connectivity_test_async(request_type=dict)


def test_create_connectivity_test_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.CreateConnectivityTestRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_connectivity_test(request)

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
async def test_create_connectivity_test_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.CreateConnectivityTestRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_connectivity_test(request)

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


def test_create_connectivity_test_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_connectivity_test(
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].test_id
        mock_val = "test_id_value"
        assert arg == mock_val
        arg = args[0].resource
        mock_val = connectivity_test.ConnectivityTest(name="name_value")
        assert arg == mock_val


def test_create_connectivity_test_flattened_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connectivity_test(
            reachability.CreateConnectivityTestRequest(),
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_connectivity_test_flattened_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_connectivity_test(
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].test_id
        mock_val = "test_id_value"
        assert arg == mock_val
        arg = args[0].resource
        mock_val = connectivity_test.ConnectivityTest(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_connectivity_test_flattened_error_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_connectivity_test(
            reachability.CreateConnectivityTestRequest(),
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.UpdateConnectivityTestRequest,
        dict,
    ],
)
def test_update_connectivity_test(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.UpdateConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_connectivity_test_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        client.update_connectivity_test()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.UpdateConnectivityTestRequest()


@pytest.mark.asyncio
async def test_update_connectivity_test_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.UpdateConnectivityTestRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.UpdateConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_connectivity_test_async_from_dict():
    await test_update_connectivity_test_async(request_type=dict)


def test_update_connectivity_test_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.UpdateConnectivityTestRequest()

    request.resource.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_connectivity_test_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.UpdateConnectivityTestRequest()

    request.resource.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource.name=name_value",
    ) in kw["metadata"]


def test_update_connectivity_test_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_connectivity_test(
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        arg = args[0].resource
        mock_val = connectivity_test.ConnectivityTest(name="name_value")
        assert arg == mock_val


def test_update_connectivity_test_flattened_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connectivity_test(
            reachability.UpdateConnectivityTestRequest(),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_connectivity_test_flattened_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_connectivity_test(
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        arg = args[0].resource
        mock_val = connectivity_test.ConnectivityTest(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_connectivity_test_flattened_error_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_connectivity_test(
            reachability.UpdateConnectivityTestRequest(),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.RerunConnectivityTestRequest,
        dict,
    ],
)
def test_rerun_connectivity_test(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rerun_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.rerun_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.RerunConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_rerun_connectivity_test_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rerun_connectivity_test), "__call__"
    ) as call:
        client.rerun_connectivity_test()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.RerunConnectivityTestRequest()


@pytest.mark.asyncio
async def test_rerun_connectivity_test_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.RerunConnectivityTestRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rerun_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.rerun_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.RerunConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_rerun_connectivity_test_async_from_dict():
    await test_rerun_connectivity_test_async(request_type=dict)


def test_rerun_connectivity_test_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.RerunConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rerun_connectivity_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.rerun_connectivity_test(request)

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
async def test_rerun_connectivity_test_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.RerunConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rerun_connectivity_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.rerun_connectivity_test(request)

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
        reachability.DeleteConnectivityTestRequest,
        dict,
    ],
)
def test_delete_connectivity_test(request_type, transport: str = "grpc"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.DeleteConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_connectivity_test_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        client.delete_connectivity_test()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.DeleteConnectivityTestRequest()


@pytest.mark.asyncio
async def test_delete_connectivity_test_async(
    transport: str = "grpc_asyncio",
    request_type=reachability.DeleteConnectivityTestRequest,
):
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_connectivity_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == reachability.DeleteConnectivityTestRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_connectivity_test_async_from_dict():
    await test_delete_connectivity_test_async(request_type=dict)


def test_delete_connectivity_test_field_headers():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.DeleteConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_connectivity_test(request)

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
async def test_delete_connectivity_test_field_headers_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = reachability.DeleteConnectivityTestRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_connectivity_test(request)

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


def test_delete_connectivity_test_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_connectivity_test(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_connectivity_test_flattened_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connectivity_test(
            reachability.DeleteConnectivityTestRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_connectivity_test_flattened_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connectivity_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_connectivity_test(
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
async def test_delete_connectivity_test_flattened_error_async():
    client = ReachabilityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_connectivity_test(
            reachability.DeleteConnectivityTestRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.ListConnectivityTestsRequest,
        dict,
    ],
)
def test_list_connectivity_tests_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/global"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = reachability.ListConnectivityTestsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = reachability.ListConnectivityTestsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_connectivity_tests(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectivityTestsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_connectivity_tests_rest_required_fields(
    request_type=reachability.ListConnectivityTestsRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

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
    ).list_connectivity_tests._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_connectivity_tests._get_unset_required_fields(jsonified_request)
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

    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = reachability.ListConnectivityTestsResponse()
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

            pb_return_value = reachability.ListConnectivityTestsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_connectivity_tests(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_connectivity_tests_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_connectivity_tests._get_unset_required_fields({})
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
def test_list_connectivity_tests_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_list_connectivity_tests"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_list_connectivity_tests"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.ListConnectivityTestsRequest.pb(
            reachability.ListConnectivityTestsRequest()
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
        req.return_value._content = reachability.ListConnectivityTestsResponse.to_json(
            reachability.ListConnectivityTestsResponse()
        )

        request = reachability.ListConnectivityTestsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = reachability.ListConnectivityTestsResponse()

        client.list_connectivity_tests(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_connectivity_tests_rest_bad_request(
    transport: str = "rest", request_type=reachability.ListConnectivityTestsRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/global"}
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
        client.list_connectivity_tests(request)


def test_list_connectivity_tests_rest_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = reachability.ListConnectivityTestsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/global"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = reachability.ListConnectivityTestsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_connectivity_tests(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/global}/connectivityTests"
            % client.transport._host,
            args[1],
        )


def test_list_connectivity_tests_rest_flattened_error(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_connectivity_tests(
            reachability.ListConnectivityTestsRequest(),
            parent="parent_value",
        )


def test_list_connectivity_tests_rest_pager(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="abc",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[],
                next_page_token="def",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                ],
                next_page_token="ghi",
            ),
            reachability.ListConnectivityTestsResponse(
                resources=[
                    connectivity_test.ConnectivityTest(),
                    connectivity_test.ConnectivityTest(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            reachability.ListConnectivityTestsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/global"}

        pager = client.list_connectivity_tests(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, connectivity_test.ConnectivityTest) for i in results)

        pages = list(client.list_connectivity_tests(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.GetConnectivityTestRequest,
        dict,
    ],
)
def test_get_connectivity_test_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = connectivity_test.ConnectivityTest(
            name="name_value",
            description="description_value",
            protocol="protocol_value",
            related_projects=["related_projects_value"],
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = connectivity_test.ConnectivityTest.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_connectivity_test(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, connectivity_test.ConnectivityTest)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.protocol == "protocol_value"
    assert response.related_projects == ["related_projects_value"]
    assert response.display_name == "display_name_value"


def test_get_connectivity_test_rest_required_fields(
    request_type=reachability.GetConnectivityTestRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

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
    ).get_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = connectivity_test.ConnectivityTest()
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

            pb_return_value = connectivity_test.ConnectivityTest.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_connectivity_test(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_connectivity_test_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_connectivity_test._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_connectivity_test_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_get_connectivity_test"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_get_connectivity_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.GetConnectivityTestRequest.pb(
            reachability.GetConnectivityTestRequest()
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
        req.return_value._content = connectivity_test.ConnectivityTest.to_json(
            connectivity_test.ConnectivityTest()
        )

        request = reachability.GetConnectivityTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = connectivity_test.ConnectivityTest()

        client.get_connectivity_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_connectivity_test_rest_bad_request(
    transport: str = "rest", request_type=reachability.GetConnectivityTestRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
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
        client.get_connectivity_test(request)


def test_get_connectivity_test_rest_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = connectivity_test.ConnectivityTest()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/global/connectivityTests/sample2"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = connectivity_test.ConnectivityTest.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_connectivity_test(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/global/connectivityTests/*}"
            % client.transport._host,
            args[1],
        )


def test_get_connectivity_test_rest_flattened_error(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connectivity_test(
            reachability.GetConnectivityTestRequest(),
            name="name_value",
        )


def test_get_connectivity_test_rest_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.CreateConnectivityTestRequest,
        dict,
    ],
)
def test_create_connectivity_test_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/global"}
    request_init["resource"] = {
        "name": "name_value",
        "description": "description_value",
        "source": {
            "ip_address": "ip_address_value",
            "port": 453,
            "instance": "instance_value",
            "forwarding_rule": "forwarding_rule_value",
            "gke_master_cluster": "gke_master_cluster_value",
            "cloud_sql_instance": "cloud_sql_instance_value",
            "network": "network_value",
            "network_type": 1,
            "project_id": "project_id_value",
        },
        "destination": {},
        "protocol": "protocol_value",
        "related_projects": ["related_projects_value1", "related_projects_value2"],
        "display_name": "display_name_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "reachability_details": {
            "result": 1,
            "verify_time": {},
            "error": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
            "traces": [
                {
                    "endpoint_info": {
                        "source_ip": "source_ip_value",
                        "destination_ip": "destination_ip_value",
                        "protocol": "protocol_value",
                        "source_port": 1205,
                        "destination_port": 1734,
                        "source_network_uri": "source_network_uri_value",
                        "destination_network_uri": "destination_network_uri_value",
                    },
                    "steps": [
                        {
                            "description": "description_value",
                            "state": 1,
                            "causes_drop": True,
                            "project_id": "project_id_value",
                            "instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "interface": "interface_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "network_tags": [
                                    "network_tags_value1",
                                    "network_tags_value2",
                                ],
                                "service_account": "service_account_value",
                            },
                            "firewall": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "direction": "direction_value",
                                "action": "action_value",
                                "priority": 898,
                                "network_uri": "network_uri_value",
                                "target_tags": [
                                    "target_tags_value1",
                                    "target_tags_value2",
                                ],
                                "target_service_accounts": [
                                    "target_service_accounts_value1",
                                    "target_service_accounts_value2",
                                ],
                                "policy": "policy_value",
                                "firewall_rule_type": 1,
                            },
                            "route": {
                                "route_type": 1,
                                "next_hop_type": 1,
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "dest_ip_range": "dest_ip_range_value",
                                "next_hop": "next_hop_value",
                                "network_uri": "network_uri_value",
                                "priority": 898,
                                "instance_tags": [
                                    "instance_tags_value1",
                                    "instance_tags_value2",
                                ],
                            },
                            "endpoint": {},
                            "forwarding_rule": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_protocol": "matched_protocol_value",
                                "matched_port_range": "matched_port_range_value",
                                "vip": "vip_value",
                                "target": "target_value",
                                "network_uri": "network_uri_value",
                            },
                            "vpn_gateway": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "ip_address": "ip_address_value",
                                "vpn_tunnel_uri": "vpn_tunnel_uri_value",
                                "region": "region_value",
                            },
                            "vpn_tunnel": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "source_gateway": "source_gateway_value",
                                "remote_gateway": "remote_gateway_value",
                                "remote_gateway_ip": "remote_gateway_ip_value",
                                "source_gateway_ip": "source_gateway_ip_value",
                                "network_uri": "network_uri_value",
                                "region": "region_value",
                                "routing_type": 1,
                            },
                            "deliver": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "forward": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "abort": {
                                "cause": 1,
                                "resource_uri": "resource_uri_value",
                                "projects_missing_permission": [
                                    "projects_missing_permission_value1",
                                    "projects_missing_permission_value2",
                                ],
                            },
                            "drop": {"cause": 1, "resource_uri": "resource_uri_value"},
                            "load_balancer": {
                                "load_balancer_type": 1,
                                "health_check_uri": "health_check_uri_value",
                                "backends": [
                                    {
                                        "display_name": "display_name_value",
                                        "uri": "uri_value",
                                        "health_check_firewall_state": 1,
                                        "health_check_allowing_firewall_rules": [
                                            "health_check_allowing_firewall_rules_value1",
                                            "health_check_allowing_firewall_rules_value2",
                                        ],
                                        "health_check_blocking_firewall_rules": [
                                            "health_check_blocking_firewall_rules_value1",
                                            "health_check_blocking_firewall_rules_value2",
                                        ],
                                    }
                                ],
                                "backend_type": 1,
                                "backend_uri": "backend_uri_value",
                            },
                            "network": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_ip_range": "matched_ip_range_value",
                            },
                            "gke_master": {
                                "cluster_uri": "cluster_uri_value",
                                "cluster_network_uri": "cluster_network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                            },
                            "cloud_sql_instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "region": "region_value",
                            },
                        }
                    ],
                }
            ],
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
        response = client.create_connectivity_test(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_connectivity_test_rest_required_fields(
    request_type=reachability.CreateConnectivityTestRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["test_id"] = ""
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
    assert "testId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "testId" in jsonified_request
    assert jsonified_request["testId"] == request_init["test_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["testId"] = "test_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_connectivity_test._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("test_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "testId" in jsonified_request
    assert jsonified_request["testId"] == "test_id_value"

    client = ReachabilityServiceClient(
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

            response = client.create_connectivity_test(request)

            expected_params = [
                (
                    "testId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_connectivity_test_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_connectivity_test._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("testId",))
        & set(
            (
                "parent",
                "testId",
                "resource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_connectivity_test_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_create_connectivity_test"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_create_connectivity_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.CreateConnectivityTestRequest.pb(
            reachability.CreateConnectivityTestRequest()
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

        request = reachability.CreateConnectivityTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_connectivity_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_connectivity_test_rest_bad_request(
    transport: str = "rest", request_type=reachability.CreateConnectivityTestRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/global"}
    request_init["resource"] = {
        "name": "name_value",
        "description": "description_value",
        "source": {
            "ip_address": "ip_address_value",
            "port": 453,
            "instance": "instance_value",
            "forwarding_rule": "forwarding_rule_value",
            "gke_master_cluster": "gke_master_cluster_value",
            "cloud_sql_instance": "cloud_sql_instance_value",
            "network": "network_value",
            "network_type": 1,
            "project_id": "project_id_value",
        },
        "destination": {},
        "protocol": "protocol_value",
        "related_projects": ["related_projects_value1", "related_projects_value2"],
        "display_name": "display_name_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "reachability_details": {
            "result": 1,
            "verify_time": {},
            "error": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
            "traces": [
                {
                    "endpoint_info": {
                        "source_ip": "source_ip_value",
                        "destination_ip": "destination_ip_value",
                        "protocol": "protocol_value",
                        "source_port": 1205,
                        "destination_port": 1734,
                        "source_network_uri": "source_network_uri_value",
                        "destination_network_uri": "destination_network_uri_value",
                    },
                    "steps": [
                        {
                            "description": "description_value",
                            "state": 1,
                            "causes_drop": True,
                            "project_id": "project_id_value",
                            "instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "interface": "interface_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "network_tags": [
                                    "network_tags_value1",
                                    "network_tags_value2",
                                ],
                                "service_account": "service_account_value",
                            },
                            "firewall": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "direction": "direction_value",
                                "action": "action_value",
                                "priority": 898,
                                "network_uri": "network_uri_value",
                                "target_tags": [
                                    "target_tags_value1",
                                    "target_tags_value2",
                                ],
                                "target_service_accounts": [
                                    "target_service_accounts_value1",
                                    "target_service_accounts_value2",
                                ],
                                "policy": "policy_value",
                                "firewall_rule_type": 1,
                            },
                            "route": {
                                "route_type": 1,
                                "next_hop_type": 1,
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "dest_ip_range": "dest_ip_range_value",
                                "next_hop": "next_hop_value",
                                "network_uri": "network_uri_value",
                                "priority": 898,
                                "instance_tags": [
                                    "instance_tags_value1",
                                    "instance_tags_value2",
                                ],
                            },
                            "endpoint": {},
                            "forwarding_rule": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_protocol": "matched_protocol_value",
                                "matched_port_range": "matched_port_range_value",
                                "vip": "vip_value",
                                "target": "target_value",
                                "network_uri": "network_uri_value",
                            },
                            "vpn_gateway": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "ip_address": "ip_address_value",
                                "vpn_tunnel_uri": "vpn_tunnel_uri_value",
                                "region": "region_value",
                            },
                            "vpn_tunnel": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "source_gateway": "source_gateway_value",
                                "remote_gateway": "remote_gateway_value",
                                "remote_gateway_ip": "remote_gateway_ip_value",
                                "source_gateway_ip": "source_gateway_ip_value",
                                "network_uri": "network_uri_value",
                                "region": "region_value",
                                "routing_type": 1,
                            },
                            "deliver": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "forward": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "abort": {
                                "cause": 1,
                                "resource_uri": "resource_uri_value",
                                "projects_missing_permission": [
                                    "projects_missing_permission_value1",
                                    "projects_missing_permission_value2",
                                ],
                            },
                            "drop": {"cause": 1, "resource_uri": "resource_uri_value"},
                            "load_balancer": {
                                "load_balancer_type": 1,
                                "health_check_uri": "health_check_uri_value",
                                "backends": [
                                    {
                                        "display_name": "display_name_value",
                                        "uri": "uri_value",
                                        "health_check_firewall_state": 1,
                                        "health_check_allowing_firewall_rules": [
                                            "health_check_allowing_firewall_rules_value1",
                                            "health_check_allowing_firewall_rules_value2",
                                        ],
                                        "health_check_blocking_firewall_rules": [
                                            "health_check_blocking_firewall_rules_value1",
                                            "health_check_blocking_firewall_rules_value2",
                                        ],
                                    }
                                ],
                                "backend_type": 1,
                                "backend_uri": "backend_uri_value",
                            },
                            "network": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_ip_range": "matched_ip_range_value",
                            },
                            "gke_master": {
                                "cluster_uri": "cluster_uri_value",
                                "cluster_network_uri": "cluster_network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                            },
                            "cloud_sql_instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "region": "region_value",
                            },
                        }
                    ],
                }
            ],
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
        client.create_connectivity_test(request)


def test_create_connectivity_test_rest_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/global"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_connectivity_test(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/global}/connectivityTests"
            % client.transport._host,
            args[1],
        )


def test_create_connectivity_test_rest_flattened_error(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connectivity_test(
            reachability.CreateConnectivityTestRequest(),
            parent="parent_value",
            test_id="test_id_value",
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


def test_create_connectivity_test_rest_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.UpdateConnectivityTestRequest,
        dict,
    ],
)
def test_update_connectivity_test_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": {
            "name": "projects/sample1/locations/global/connectivityTests/sample2"
        }
    }
    request_init["resource"] = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2",
        "description": "description_value",
        "source": {
            "ip_address": "ip_address_value",
            "port": 453,
            "instance": "instance_value",
            "forwarding_rule": "forwarding_rule_value",
            "gke_master_cluster": "gke_master_cluster_value",
            "cloud_sql_instance": "cloud_sql_instance_value",
            "network": "network_value",
            "network_type": 1,
            "project_id": "project_id_value",
        },
        "destination": {},
        "protocol": "protocol_value",
        "related_projects": ["related_projects_value1", "related_projects_value2"],
        "display_name": "display_name_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "reachability_details": {
            "result": 1,
            "verify_time": {},
            "error": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
            "traces": [
                {
                    "endpoint_info": {
                        "source_ip": "source_ip_value",
                        "destination_ip": "destination_ip_value",
                        "protocol": "protocol_value",
                        "source_port": 1205,
                        "destination_port": 1734,
                        "source_network_uri": "source_network_uri_value",
                        "destination_network_uri": "destination_network_uri_value",
                    },
                    "steps": [
                        {
                            "description": "description_value",
                            "state": 1,
                            "causes_drop": True,
                            "project_id": "project_id_value",
                            "instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "interface": "interface_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "network_tags": [
                                    "network_tags_value1",
                                    "network_tags_value2",
                                ],
                                "service_account": "service_account_value",
                            },
                            "firewall": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "direction": "direction_value",
                                "action": "action_value",
                                "priority": 898,
                                "network_uri": "network_uri_value",
                                "target_tags": [
                                    "target_tags_value1",
                                    "target_tags_value2",
                                ],
                                "target_service_accounts": [
                                    "target_service_accounts_value1",
                                    "target_service_accounts_value2",
                                ],
                                "policy": "policy_value",
                                "firewall_rule_type": 1,
                            },
                            "route": {
                                "route_type": 1,
                                "next_hop_type": 1,
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "dest_ip_range": "dest_ip_range_value",
                                "next_hop": "next_hop_value",
                                "network_uri": "network_uri_value",
                                "priority": 898,
                                "instance_tags": [
                                    "instance_tags_value1",
                                    "instance_tags_value2",
                                ],
                            },
                            "endpoint": {},
                            "forwarding_rule": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_protocol": "matched_protocol_value",
                                "matched_port_range": "matched_port_range_value",
                                "vip": "vip_value",
                                "target": "target_value",
                                "network_uri": "network_uri_value",
                            },
                            "vpn_gateway": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "ip_address": "ip_address_value",
                                "vpn_tunnel_uri": "vpn_tunnel_uri_value",
                                "region": "region_value",
                            },
                            "vpn_tunnel": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "source_gateway": "source_gateway_value",
                                "remote_gateway": "remote_gateway_value",
                                "remote_gateway_ip": "remote_gateway_ip_value",
                                "source_gateway_ip": "source_gateway_ip_value",
                                "network_uri": "network_uri_value",
                                "region": "region_value",
                                "routing_type": 1,
                            },
                            "deliver": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "forward": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "abort": {
                                "cause": 1,
                                "resource_uri": "resource_uri_value",
                                "projects_missing_permission": [
                                    "projects_missing_permission_value1",
                                    "projects_missing_permission_value2",
                                ],
                            },
                            "drop": {"cause": 1, "resource_uri": "resource_uri_value"},
                            "load_balancer": {
                                "load_balancer_type": 1,
                                "health_check_uri": "health_check_uri_value",
                                "backends": [
                                    {
                                        "display_name": "display_name_value",
                                        "uri": "uri_value",
                                        "health_check_firewall_state": 1,
                                        "health_check_allowing_firewall_rules": [
                                            "health_check_allowing_firewall_rules_value1",
                                            "health_check_allowing_firewall_rules_value2",
                                        ],
                                        "health_check_blocking_firewall_rules": [
                                            "health_check_blocking_firewall_rules_value1",
                                            "health_check_blocking_firewall_rules_value2",
                                        ],
                                    }
                                ],
                                "backend_type": 1,
                                "backend_uri": "backend_uri_value",
                            },
                            "network": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_ip_range": "matched_ip_range_value",
                            },
                            "gke_master": {
                                "cluster_uri": "cluster_uri_value",
                                "cluster_network_uri": "cluster_network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                            },
                            "cloud_sql_instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "region": "region_value",
                            },
                        }
                    ],
                }
            ],
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
        response = client.update_connectivity_test(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_connectivity_test_rest_required_fields(
    request_type=reachability.UpdateConnectivityTestRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

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
    ).update_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_connectivity_test._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ReachabilityServiceClient(
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

            response = client.update_connectivity_test(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_connectivity_test_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_connectivity_test._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "updateMask",
                "resource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_connectivity_test_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_update_connectivity_test"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_update_connectivity_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.UpdateConnectivityTestRequest.pb(
            reachability.UpdateConnectivityTestRequest()
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

        request = reachability.UpdateConnectivityTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_connectivity_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_connectivity_test_rest_bad_request(
    transport: str = "rest", request_type=reachability.UpdateConnectivityTestRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": {
            "name": "projects/sample1/locations/global/connectivityTests/sample2"
        }
    }
    request_init["resource"] = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2",
        "description": "description_value",
        "source": {
            "ip_address": "ip_address_value",
            "port": 453,
            "instance": "instance_value",
            "forwarding_rule": "forwarding_rule_value",
            "gke_master_cluster": "gke_master_cluster_value",
            "cloud_sql_instance": "cloud_sql_instance_value",
            "network": "network_value",
            "network_type": 1,
            "project_id": "project_id_value",
        },
        "destination": {},
        "protocol": "protocol_value",
        "related_projects": ["related_projects_value1", "related_projects_value2"],
        "display_name": "display_name_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "reachability_details": {
            "result": 1,
            "verify_time": {},
            "error": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
            "traces": [
                {
                    "endpoint_info": {
                        "source_ip": "source_ip_value",
                        "destination_ip": "destination_ip_value",
                        "protocol": "protocol_value",
                        "source_port": 1205,
                        "destination_port": 1734,
                        "source_network_uri": "source_network_uri_value",
                        "destination_network_uri": "destination_network_uri_value",
                    },
                    "steps": [
                        {
                            "description": "description_value",
                            "state": 1,
                            "causes_drop": True,
                            "project_id": "project_id_value",
                            "instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "interface": "interface_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "network_tags": [
                                    "network_tags_value1",
                                    "network_tags_value2",
                                ],
                                "service_account": "service_account_value",
                            },
                            "firewall": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "direction": "direction_value",
                                "action": "action_value",
                                "priority": 898,
                                "network_uri": "network_uri_value",
                                "target_tags": [
                                    "target_tags_value1",
                                    "target_tags_value2",
                                ],
                                "target_service_accounts": [
                                    "target_service_accounts_value1",
                                    "target_service_accounts_value2",
                                ],
                                "policy": "policy_value",
                                "firewall_rule_type": 1,
                            },
                            "route": {
                                "route_type": 1,
                                "next_hop_type": 1,
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "dest_ip_range": "dest_ip_range_value",
                                "next_hop": "next_hop_value",
                                "network_uri": "network_uri_value",
                                "priority": 898,
                                "instance_tags": [
                                    "instance_tags_value1",
                                    "instance_tags_value2",
                                ],
                            },
                            "endpoint": {},
                            "forwarding_rule": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_protocol": "matched_protocol_value",
                                "matched_port_range": "matched_port_range_value",
                                "vip": "vip_value",
                                "target": "target_value",
                                "network_uri": "network_uri_value",
                            },
                            "vpn_gateway": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "ip_address": "ip_address_value",
                                "vpn_tunnel_uri": "vpn_tunnel_uri_value",
                                "region": "region_value",
                            },
                            "vpn_tunnel": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "source_gateway": "source_gateway_value",
                                "remote_gateway": "remote_gateway_value",
                                "remote_gateway_ip": "remote_gateway_ip_value",
                                "source_gateway_ip": "source_gateway_ip_value",
                                "network_uri": "network_uri_value",
                                "region": "region_value",
                                "routing_type": 1,
                            },
                            "deliver": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "forward": {
                                "target": 1,
                                "resource_uri": "resource_uri_value",
                            },
                            "abort": {
                                "cause": 1,
                                "resource_uri": "resource_uri_value",
                                "projects_missing_permission": [
                                    "projects_missing_permission_value1",
                                    "projects_missing_permission_value2",
                                ],
                            },
                            "drop": {"cause": 1, "resource_uri": "resource_uri_value"},
                            "load_balancer": {
                                "load_balancer_type": 1,
                                "health_check_uri": "health_check_uri_value",
                                "backends": [
                                    {
                                        "display_name": "display_name_value",
                                        "uri": "uri_value",
                                        "health_check_firewall_state": 1,
                                        "health_check_allowing_firewall_rules": [
                                            "health_check_allowing_firewall_rules_value1",
                                            "health_check_allowing_firewall_rules_value2",
                                        ],
                                        "health_check_blocking_firewall_rules": [
                                            "health_check_blocking_firewall_rules_value1",
                                            "health_check_blocking_firewall_rules_value2",
                                        ],
                                    }
                                ],
                                "backend_type": 1,
                                "backend_uri": "backend_uri_value",
                            },
                            "network": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "matched_ip_range": "matched_ip_range_value",
                            },
                            "gke_master": {
                                "cluster_uri": "cluster_uri_value",
                                "cluster_network_uri": "cluster_network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                            },
                            "cloud_sql_instance": {
                                "display_name": "display_name_value",
                                "uri": "uri_value",
                                "network_uri": "network_uri_value",
                                "internal_ip": "internal_ip_value",
                                "external_ip": "external_ip_value",
                                "region": "region_value",
                            },
                        }
                    ],
                }
            ],
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
        client.update_connectivity_test(request)


def test_update_connectivity_test_rest_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "resource": {
                "name": "projects/sample1/locations/global/connectivityTests/sample2"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_connectivity_test(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{resource.name=projects/*/locations/global/connectivityTests/*}"
            % client.transport._host,
            args[1],
        )


def test_update_connectivity_test_rest_flattened_error(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connectivity_test(
            reachability.UpdateConnectivityTestRequest(),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            resource=connectivity_test.ConnectivityTest(name="name_value"),
        )


def test_update_connectivity_test_rest_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.RerunConnectivityTestRequest,
        dict,
    ],
)
def test_rerun_connectivity_test_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
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
        response = client.rerun_connectivity_test(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_rerun_connectivity_test_rest_required_fields(
    request_type=reachability.RerunConnectivityTestRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

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
    ).rerun_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rerun_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ReachabilityServiceClient(
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

            response = client.rerun_connectivity_test(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rerun_connectivity_test_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rerun_connectivity_test._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rerun_connectivity_test_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_rerun_connectivity_test"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_rerun_connectivity_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.RerunConnectivityTestRequest.pb(
            reachability.RerunConnectivityTestRequest()
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

        request = reachability.RerunConnectivityTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.rerun_connectivity_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rerun_connectivity_test_rest_bad_request(
    transport: str = "rest", request_type=reachability.RerunConnectivityTestRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
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
        client.rerun_connectivity_test(request)


def test_rerun_connectivity_test_rest_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        reachability.DeleteConnectivityTestRequest,
        dict,
    ],
)
def test_delete_connectivity_test_rest(request_type):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
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
        response = client.delete_connectivity_test(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_connectivity_test_rest_required_fields(
    request_type=reachability.DeleteConnectivityTestRequest,
):
    transport_class = transports.ReachabilityServiceRestTransport

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
    ).delete_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_connectivity_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ReachabilityServiceClient(
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

            response = client.delete_connectivity_test(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_connectivity_test_rest_unset_required_fields():
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_connectivity_test._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_connectivity_test_rest_interceptors(null_interceptor):
    transport = transports.ReachabilityServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ReachabilityServiceRestInterceptor(),
    )
    client = ReachabilityServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "post_delete_connectivity_test"
    ) as post, mock.patch.object(
        transports.ReachabilityServiceRestInterceptor, "pre_delete_connectivity_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = reachability.DeleteConnectivityTestRequest.pb(
            reachability.DeleteConnectivityTestRequest()
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

        request = reachability.DeleteConnectivityTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_connectivity_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_connectivity_test_rest_bad_request(
    transport: str = "rest", request_type=reachability.DeleteConnectivityTestRequest
):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/global/connectivityTests/sample2"
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
        client.delete_connectivity_test(request)


def test_delete_connectivity_test_rest_flattened():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/global/connectivityTests/sample2"
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

        client.delete_connectivity_test(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/global/connectivityTests/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_connectivity_test_rest_flattened_error(transport: str = "rest"):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connectivity_test(
            reachability.DeleteConnectivityTestRequest(),
            name="name_value",
        )


def test_delete_connectivity_test_rest_error():
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ReachabilityServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ReachabilityServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ReachabilityServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ReachabilityServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ReachabilityServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ReachabilityServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ReachabilityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ReachabilityServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
        transports.ReachabilityServiceRestTransport,
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
    transport = ReachabilityServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ReachabilityServiceGrpcTransport,
    )


def test_reachability_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ReachabilityServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_reachability_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.network_management_v1.services.reachability_service.transports.ReachabilityServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ReachabilityServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_connectivity_tests",
        "get_connectivity_test",
        "create_connectivity_test",
        "update_connectivity_test",
        "rerun_connectivity_test",
        "delete_connectivity_test",
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


def test_reachability_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.network_management_v1.services.reachability_service.transports.ReachabilityServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ReachabilityServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_reachability_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.network_management_v1.services.reachability_service.transports.ReachabilityServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ReachabilityServiceTransport()
        adc.assert_called_once()


def test_reachability_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ReachabilityServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
    ],
)
def test_reachability_service_transport_auth_adc(transport_class):
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
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
        transports.ReachabilityServiceRestTransport,
    ],
)
def test_reachability_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.ReachabilityServiceGrpcTransport, grpc_helpers),
        (transports.ReachabilityServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_reachability_service_transport_create_channel(transport_class, grpc_helpers):
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
            "networkmanagement.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="networkmanagement.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
    ],
)
def test_reachability_service_grpc_transport_client_cert_source_for_mtls(
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


def test_reachability_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.ReachabilityServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_reachability_service_rest_lro_client():
    client = ReachabilityServiceClient(
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
def test_reachability_service_host_no_port(transport_name):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="networkmanagement.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "networkmanagement.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://networkmanagement.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_reachability_service_host_with_port(transport_name):
    client = ReachabilityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="networkmanagement.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "networkmanagement.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://networkmanagement.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_reachability_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = ReachabilityServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = ReachabilityServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_connectivity_tests._session
    session2 = client2.transport.list_connectivity_tests._session
    assert session1 != session2
    session1 = client1.transport.get_connectivity_test._session
    session2 = client2.transport.get_connectivity_test._session
    assert session1 != session2
    session1 = client1.transport.create_connectivity_test._session
    session2 = client2.transport.create_connectivity_test._session
    assert session1 != session2
    session1 = client1.transport.update_connectivity_test._session
    session2 = client2.transport.update_connectivity_test._session
    assert session1 != session2
    session1 = client1.transport.rerun_connectivity_test._session
    session2 = client2.transport.rerun_connectivity_test._session
    assert session1 != session2
    session1 = client1.transport.delete_connectivity_test._session
    session2 = client2.transport.delete_connectivity_test._session
    assert session1 != session2


def test_reachability_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ReachabilityServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_reachability_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ReachabilityServiceGrpcAsyncIOTransport(
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
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
    ],
)
def test_reachability_service_transport_channel_mtls_with_client_cert_source(
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
        transports.ReachabilityServiceGrpcTransport,
        transports.ReachabilityServiceGrpcAsyncIOTransport,
    ],
)
def test_reachability_service_transport_channel_mtls_with_adc(transport_class):
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


def test_reachability_service_grpc_lro_client():
    client = ReachabilityServiceClient(
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


def test_reachability_service_grpc_lro_async_client():
    client = ReachabilityServiceAsyncClient(
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


def test_connectivity_test_path():
    project = "squid"
    test = "clam"
    expected = "projects/{project}/locations/global/connectivityTests/{test}".format(
        project=project,
        test=test,
    )
    actual = ReachabilityServiceClient.connectivity_test_path(project, test)
    assert expected == actual


def test_parse_connectivity_test_path():
    expected = {
        "project": "whelk",
        "test": "octopus",
    }
    path = ReachabilityServiceClient.connectivity_test_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_connectivity_test_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ReachabilityServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = ReachabilityServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ReachabilityServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = ReachabilityServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ReachabilityServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = ReachabilityServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ReachabilityServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = ReachabilityServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ReachabilityServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = ReachabilityServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ReachabilityServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ReachabilityServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ReachabilityServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ReachabilityServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ReachabilityServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ReachabilityServiceAsyncClient(
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
        client = ReachabilityServiceClient(
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
        client = ReachabilityServiceClient(
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
        (ReachabilityServiceClient, transports.ReachabilityServiceGrpcTransport),
        (
            ReachabilityServiceAsyncClient,
            transports.ReachabilityServiceGrpcAsyncIOTransport,
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
