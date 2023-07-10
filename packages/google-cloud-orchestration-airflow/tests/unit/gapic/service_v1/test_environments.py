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
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.orchestration.airflow.service_v1.services.environments import (
    EnvironmentsAsyncClient,
    EnvironmentsClient,
    pagers,
    transports,
)
from google.cloud.orchestration.airflow.service_v1.types import environments, operations


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

    assert EnvironmentsClient._get_default_mtls_endpoint(None) is None
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert EnvironmentsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (EnvironmentsClient, "grpc"),
        (EnvironmentsAsyncClient, "grpc_asyncio"),
        (EnvironmentsClient, "rest"),
    ],
)
def test_environments_client_from_service_account_info(client_class, transport_name):
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
            "composer.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://composer.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.EnvironmentsGrpcTransport, "grpc"),
        (transports.EnvironmentsGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.EnvironmentsRestTransport, "rest"),
    ],
)
def test_environments_client_service_account_always_use_jwt(
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
        (EnvironmentsClient, "grpc"),
        (EnvironmentsAsyncClient, "grpc_asyncio"),
        (EnvironmentsClient, "rest"),
    ],
)
def test_environments_client_from_service_account_file(client_class, transport_name):
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
            "composer.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://composer.googleapis.com"
        )


def test_environments_client_get_transport_class():
    transport = EnvironmentsClient.get_transport_class()
    available_transports = [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsRestTransport,
    ]
    assert transport in available_transports

    transport = EnvironmentsClient.get_transport_class("grpc")
    assert transport == transports.EnvironmentsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest"),
    ],
)
@mock.patch.object(
    EnvironmentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EnvironmentsClient)
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EnvironmentsAsyncClient),
)
def test_environments_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(EnvironmentsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(EnvironmentsClient, "get_transport_class") as gtc:
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
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc", "true"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc", "false"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", "true"),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    EnvironmentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EnvironmentsClient)
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EnvironmentsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_environments_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [EnvironmentsClient, EnvironmentsAsyncClient])
@mock.patch.object(
    EnvironmentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EnvironmentsClient)
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EnvironmentsAsyncClient),
)
def test_environments_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest"),
    ],
)
def test_environments_client_client_options_scopes(
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
            EnvironmentsClient,
            transports.EnvironmentsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", None),
    ],
)
def test_environments_client_client_options_credentials_file(
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


def test_environments_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.orchestration.airflow.service_v1.services.environments.transports.EnvironmentsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = EnvironmentsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
            EnvironmentsClient,
            transports.EnvironmentsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_environments_client_create_channel_credentials_file(
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
            "composer.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="composer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.CreateEnvironmentRequest,
        dict,
    ],
)
def test_create_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.CreateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        client.create_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.CreateEnvironmentRequest()


@pytest.mark.asyncio
async def test_create_environment_async(
    transport: str = "grpc_asyncio", request_type=environments.CreateEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.CreateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_environment_async_from_dict():
    await test_create_environment_async(request_type=dict)


def test_create_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_environment(request)

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
async def test_create_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_environment(request)

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


def test_create_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_environment(
            parent="parent_value",
            environment=environments.Environment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = environments.Environment(name="name_value")
        assert arg == mock_val


def test_create_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_environment(
            environments.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=environments.Environment(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_environment(
            parent="parent_value",
            environment=environments.Environment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = environments.Environment(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_environment(
            environments.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=environments.Environment(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.GetEnvironmentRequest,
        dict,
    ],
)
def test_get_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.Environment(
            name="name_value",
            uuid="uuid_value",
            state=environments.Environment.State.CREATING,
        )
        response = client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.GetEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.Environment)
    assert response.name == "name_value"
    assert response.uuid == "uuid_value"
    assert response.state == environments.Environment.State.CREATING


def test_get_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        client.get_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.GetEnvironmentRequest()


@pytest.mark.asyncio
async def test_get_environment_async(
    transport: str = "grpc_asyncio", request_type=environments.GetEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.Environment(
                name="name_value",
                uuid="uuid_value",
                state=environments.Environment.State.CREATING,
            )
        )
        response = await client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.GetEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.Environment)
    assert response.name == "name_value"
    assert response.uuid == "uuid_value"
    assert response.state == environments.Environment.State.CREATING


@pytest.mark.asyncio
async def test_get_environment_async_from_dict():
    await test_get_environment_async(request_type=dict)


def test_get_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = environments.Environment()
        client.get_environment(request)

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
async def test_get_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.Environment()
        )
        await client.get_environment(request)

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


def test_get_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.Environment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_environment(
            environments.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.Environment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.Environment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_environment(
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
async def test_get_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_environment(
            environments.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.ListEnvironmentsRequest,
        dict,
    ],
)
def test_list_environments(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.ListEnvironmentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ListEnvironmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_environments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        client.list_environments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ListEnvironmentsRequest()


@pytest.mark.asyncio
async def test_list_environments_async(
    transport: str = "grpc_asyncio", request_type=environments.ListEnvironmentsRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.ListEnvironmentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ListEnvironmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_environments_async_from_dict():
    await test_list_environments_async(request_type=dict)


def test_list_environments_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = environments.ListEnvironmentsResponse()
        client.list_environments(request)

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
async def test_list_environments_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.ListEnvironmentsResponse()
        )
        await client.list_environments(request)

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


def test_list_environments_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.ListEnvironmentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_environments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_environments_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_environments(
            environments.ListEnvironmentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_environments_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.ListEnvironmentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.ListEnvironmentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_environments(
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
async def test_list_environments_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_environments(
            environments.ListEnvironmentsRequest(),
            parent="parent_value",
        )


def test_list_environments_pager(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                    environments.Environment(),
                ],
                next_page_token="abc",
            ),
            environments.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                ],
                next_page_token="ghi",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_environments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environments.Environment) for i in results)


def test_list_environments_pages(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                    environments.Environment(),
                ],
                next_page_token="abc",
            ),
            environments.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                ],
                next_page_token="ghi",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_environments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_environments_async_pager():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                    environments.Environment(),
                ],
                next_page_token="abc",
            ),
            environments.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                ],
                next_page_token="ghi",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_environments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, environments.Environment) for i in responses)


@pytest.mark.asyncio
async def test_list_environments_async_pages():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                    environments.Environment(),
                ],
                next_page_token="abc",
            ),
            environments.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                ],
                next_page_token="ghi",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_environments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        environments.UpdateEnvironmentRequest,
        dict,
    ],
)
def test_update_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.UpdateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        client.update_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.UpdateEnvironmentRequest()


@pytest.mark.asyncio
async def test_update_environment_async(
    transport: str = "grpc_asyncio", request_type=environments.UpdateEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.UpdateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_environment_async_from_dict():
    await test_update_environment_async(request_type=dict)


def test_update_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.UpdateEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_environment(request)

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
async def test_update_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.UpdateEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_environment(request)

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


def test_update_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_environment(
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = environments.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_environment(
            environments.UpdateEnvironmentRequest(),
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_environment(
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = environments.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_environment(
            environments.UpdateEnvironmentRequest(),
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.DeleteEnvironmentRequest,
        dict,
    ],
)
def test_delete_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DeleteEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        client.delete_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DeleteEnvironmentRequest()


@pytest.mark.asyncio
async def test_delete_environment_async(
    transport: str = "grpc_asyncio", request_type=environments.DeleteEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DeleteEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_environment_async_from_dict():
    await test_delete_environment_async(request_type=dict)


def test_delete_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_environment(request)

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
async def test_delete_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_environment(request)

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


def test_delete_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_environment(
            environments.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_environment(
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
async def test_delete_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_environment(
            environments.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.ExecuteAirflowCommandRequest,
        dict,
    ],
)
def test_execute_airflow_command(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.ExecuteAirflowCommandResponse(
            execution_id="execution_id_value",
            pod="pod_value",
            pod_namespace="pod_namespace_value",
            error="error_value",
        )
        response = client.execute_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ExecuteAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.ExecuteAirflowCommandResponse)
    assert response.execution_id == "execution_id_value"
    assert response.pod == "pod_value"
    assert response.pod_namespace == "pod_namespace_value"
    assert response.error == "error_value"


def test_execute_airflow_command_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_airflow_command), "__call__"
    ) as call:
        client.execute_airflow_command()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ExecuteAirflowCommandRequest()


@pytest.mark.asyncio
async def test_execute_airflow_command_async(
    transport: str = "grpc_asyncio",
    request_type=environments.ExecuteAirflowCommandRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.ExecuteAirflowCommandResponse(
                execution_id="execution_id_value",
                pod="pod_value",
                pod_namespace="pod_namespace_value",
                error="error_value",
            )
        )
        response = await client.execute_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.ExecuteAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.ExecuteAirflowCommandResponse)
    assert response.execution_id == "execution_id_value"
    assert response.pod == "pod_value"
    assert response.pod_namespace == "pod_namespace_value"
    assert response.error == "error_value"


@pytest.mark.asyncio
async def test_execute_airflow_command_async_from_dict():
    await test_execute_airflow_command_async(request_type=dict)


def test_execute_airflow_command_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.ExecuteAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_airflow_command), "__call__"
    ) as call:
        call.return_value = environments.ExecuteAirflowCommandResponse()
        client.execute_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_execute_airflow_command_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.ExecuteAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.execute_airflow_command), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.ExecuteAirflowCommandResponse()
        )
        await client.execute_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.StopAirflowCommandRequest,
        dict,
    ],
)
def test_stop_airflow_command(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.StopAirflowCommandResponse(
            is_done=True,
            output=["output_value"],
        )
        response = client.stop_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.StopAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.StopAirflowCommandResponse)
    assert response.is_done is True
    assert response.output == ["output_value"]


def test_stop_airflow_command_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_airflow_command), "__call__"
    ) as call:
        client.stop_airflow_command()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.StopAirflowCommandRequest()


@pytest.mark.asyncio
async def test_stop_airflow_command_async(
    transport: str = "grpc_asyncio", request_type=environments.StopAirflowCommandRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.StopAirflowCommandResponse(
                is_done=True,
                output=["output_value"],
            )
        )
        response = await client.stop_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.StopAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.StopAirflowCommandResponse)
    assert response.is_done is True
    assert response.output == ["output_value"]


@pytest.mark.asyncio
async def test_stop_airflow_command_async_from_dict():
    await test_stop_airflow_command_async(request_type=dict)


def test_stop_airflow_command_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.StopAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_airflow_command), "__call__"
    ) as call:
        call.return_value = environments.StopAirflowCommandResponse()
        client.stop_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_stop_airflow_command_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.StopAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_airflow_command), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.StopAirflowCommandResponse()
        )
        await client.stop_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.PollAirflowCommandRequest,
        dict,
    ],
)
def test_poll_airflow_command(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.poll_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.PollAirflowCommandResponse(
            output_end=True,
        )
        response = client.poll_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.PollAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.PollAirflowCommandResponse)
    assert response.output_end is True


def test_poll_airflow_command_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.poll_airflow_command), "__call__"
    ) as call:
        client.poll_airflow_command()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.PollAirflowCommandRequest()


@pytest.mark.asyncio
async def test_poll_airflow_command_async(
    transport: str = "grpc_asyncio", request_type=environments.PollAirflowCommandRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.poll_airflow_command), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.PollAirflowCommandResponse(
                output_end=True,
            )
        )
        response = await client.poll_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.PollAirflowCommandRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.PollAirflowCommandResponse)
    assert response.output_end is True


@pytest.mark.asyncio
async def test_poll_airflow_command_async_from_dict():
    await test_poll_airflow_command_async(request_type=dict)


def test_poll_airflow_command_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.PollAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.poll_airflow_command), "__call__"
    ) as call:
        call.return_value = environments.PollAirflowCommandResponse()
        client.poll_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_poll_airflow_command_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.PollAirflowCommandRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.poll_airflow_command), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.PollAirflowCommandResponse()
        )
        await client.poll_airflow_command(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.SaveSnapshotRequest,
        dict,
    ],
)
def test_save_snapshot(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.save_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.save_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.SaveSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_save_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.save_snapshot), "__call__") as call:
        client.save_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.SaveSnapshotRequest()


@pytest.mark.asyncio
async def test_save_snapshot_async(
    transport: str = "grpc_asyncio", request_type=environments.SaveSnapshotRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.save_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.save_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.SaveSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_save_snapshot_async_from_dict():
    await test_save_snapshot_async(request_type=dict)


def test_save_snapshot_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.SaveSnapshotRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.save_snapshot), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.save_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_save_snapshot_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.SaveSnapshotRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.save_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.save_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.LoadSnapshotRequest,
        dict,
    ],
)
def test_load_snapshot(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.load_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.load_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.LoadSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_load_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.load_snapshot), "__call__") as call:
        client.load_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.LoadSnapshotRequest()


@pytest.mark.asyncio
async def test_load_snapshot_async(
    transport: str = "grpc_asyncio", request_type=environments.LoadSnapshotRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.load_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.load_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.LoadSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_load_snapshot_async_from_dict():
    await test_load_snapshot_async(request_type=dict)


def test_load_snapshot_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.LoadSnapshotRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.load_snapshot), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.load_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_load_snapshot_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.LoadSnapshotRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.load_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.load_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.DatabaseFailoverRequest,
        dict,
    ],
)
def test_database_failover(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.database_failover), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.database_failover(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DatabaseFailoverRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_database_failover_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.database_failover), "__call__"
    ) as call:
        client.database_failover()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DatabaseFailoverRequest()


@pytest.mark.asyncio
async def test_database_failover_async(
    transport: str = "grpc_asyncio", request_type=environments.DatabaseFailoverRequest
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.database_failover), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.database_failover(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.DatabaseFailoverRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_database_failover_async_from_dict():
    await test_database_failover_async(request_type=dict)


def test_database_failover_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.DatabaseFailoverRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.database_failover), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.database_failover(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_database_failover_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.DatabaseFailoverRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.database_failover), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.database_failover(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.FetchDatabasePropertiesRequest,
        dict,
    ],
)
def test_fetch_database_properties(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_database_properties), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environments.FetchDatabasePropertiesResponse(
            primary_gce_zone="primary_gce_zone_value",
            secondary_gce_zone="secondary_gce_zone_value",
            is_failover_replica_available=True,
        )
        response = client.fetch_database_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.FetchDatabasePropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.FetchDatabasePropertiesResponse)
    assert response.primary_gce_zone == "primary_gce_zone_value"
    assert response.secondary_gce_zone == "secondary_gce_zone_value"
    assert response.is_failover_replica_available is True


def test_fetch_database_properties_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_database_properties), "__call__"
    ) as call:
        client.fetch_database_properties()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.FetchDatabasePropertiesRequest()


@pytest.mark.asyncio
async def test_fetch_database_properties_async(
    transport: str = "grpc_asyncio",
    request_type=environments.FetchDatabasePropertiesRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_database_properties), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.FetchDatabasePropertiesResponse(
                primary_gce_zone="primary_gce_zone_value",
                secondary_gce_zone="secondary_gce_zone_value",
                is_failover_replica_available=True,
            )
        )
        response = await client.fetch_database_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == environments.FetchDatabasePropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.FetchDatabasePropertiesResponse)
    assert response.primary_gce_zone == "primary_gce_zone_value"
    assert response.secondary_gce_zone == "secondary_gce_zone_value"
    assert response.is_failover_replica_available is True


@pytest.mark.asyncio
async def test_fetch_database_properties_async_from_dict():
    await test_fetch_database_properties_async(request_type=dict)


def test_fetch_database_properties_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.FetchDatabasePropertiesRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_database_properties), "__call__"
    ) as call:
        call.return_value = environments.FetchDatabasePropertiesResponse()
        client.fetch_database_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_database_properties_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environments.FetchDatabasePropertiesRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_database_properties), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environments.FetchDatabasePropertiesResponse()
        )
        await client.fetch_database_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environments.CreateEnvironmentRequest,
        dict,
    ],
)
def test_create_environment_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["environment"] = {
        "name": "name_value",
        "config": {
            "gke_cluster": "gke_cluster_value",
            "dag_gcs_prefix": "dag_gcs_prefix_value",
            "node_count": 1070,
            "software_config": {
                "image_version": "image_version_value",
                "airflow_config_overrides": {},
                "pypi_packages": {},
                "env_variables": {},
                "python_version": "python_version_value",
                "scheduler_count": 1607,
            },
            "node_config": {
                "location": "location_value",
                "machine_type": "machine_type_value",
                "network": "network_value",
                "subnetwork": "subnetwork_value",
                "disk_size_gb": 1261,
                "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
                "service_account": "service_account_value",
                "tags": ["tags_value1", "tags_value2"],
                "ip_allocation_policy": {
                    "use_ip_aliases": True,
                    "cluster_secondary_range_name": "cluster_secondary_range_name_value",
                    "cluster_ipv4_cidr_block": "cluster_ipv4_cidr_block_value",
                    "services_secondary_range_name": "services_secondary_range_name_value",
                    "services_ipv4_cidr_block": "services_ipv4_cidr_block_value",
                },
                "enable_ip_masq_agent": True,
            },
            "private_environment_config": {
                "enable_private_environment": True,
                "private_cluster_config": {
                    "enable_private_endpoint": True,
                    "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                    "master_ipv4_reserved_range": "master_ipv4_reserved_range_value",
                },
                "web_server_ipv4_cidr_block": "web_server_ipv4_cidr_block_value",
                "cloud_sql_ipv4_cidr_block": "cloud_sql_ipv4_cidr_block_value",
                "web_server_ipv4_reserved_range": "web_server_ipv4_reserved_range_value",
                "cloud_composer_network_ipv4_cidr_block": "cloud_composer_network_ipv4_cidr_block_value",
                "cloud_composer_network_ipv4_reserved_range": "cloud_composer_network_ipv4_reserved_range_value",
                "enable_privately_used_public_ips": True,
                "cloud_composer_connection_subnetwork": "cloud_composer_connection_subnetwork_value",
                "networking_config": {"connection_type": 1},
            },
            "web_server_network_access_control": {
                "allowed_ip_ranges": [
                    {"value": "value_value", "description": "description_value"}
                ]
            },
            "database_config": {"machine_type": "machine_type_value"},
            "web_server_config": {"machine_type": "machine_type_value"},
            "encryption_config": {"kms_key_name": "kms_key_name_value"},
            "maintenance_window": {
                "start_time": {"seconds": 751, "nanos": 543},
                "end_time": {},
                "recurrence": "recurrence_value",
            },
            "workloads_config": {
                "scheduler": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "count": 553,
                },
                "web_server": {"cpu": 0.328, "memory_gb": 0.961, "storage_gb": 0.1053},
                "worker": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "min_count": 972,
                    "max_count": 974,
                },
            },
            "environment_size": 1,
            "airflow_uri": "airflow_uri_value",
            "airflow_byoid_uri": "airflow_byoid_uri_value",
            "master_authorized_networks_config": {
                "enabled": True,
                "cidr_blocks": [
                    {
                        "display_name": "display_name_value",
                        "cidr_block": "cidr_block_value",
                    }
                ],
            },
            "recovery_config": {
                "scheduled_snapshots_config": {
                    "enabled": True,
                    "snapshot_location": "snapshot_location_value",
                    "snapshot_creation_schedule": "snapshot_creation_schedule_value",
                    "time_zone": "time_zone_value",
                }
            },
            "resilience_mode": 1,
        },
        "uuid": "uuid_value",
        "state": 1,
        "create_time": {},
        "update_time": {},
        "labels": {},
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
        response = client.create_environment(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_create_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_create_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.CreateEnvironmentRequest.pb(
            environments.CreateEnvironmentRequest()
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

        request = environments.CreateEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_environment_rest_bad_request(
    transport: str = "rest", request_type=environments.CreateEnvironmentRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["environment"] = {
        "name": "name_value",
        "config": {
            "gke_cluster": "gke_cluster_value",
            "dag_gcs_prefix": "dag_gcs_prefix_value",
            "node_count": 1070,
            "software_config": {
                "image_version": "image_version_value",
                "airflow_config_overrides": {},
                "pypi_packages": {},
                "env_variables": {},
                "python_version": "python_version_value",
                "scheduler_count": 1607,
            },
            "node_config": {
                "location": "location_value",
                "machine_type": "machine_type_value",
                "network": "network_value",
                "subnetwork": "subnetwork_value",
                "disk_size_gb": 1261,
                "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
                "service_account": "service_account_value",
                "tags": ["tags_value1", "tags_value2"],
                "ip_allocation_policy": {
                    "use_ip_aliases": True,
                    "cluster_secondary_range_name": "cluster_secondary_range_name_value",
                    "cluster_ipv4_cidr_block": "cluster_ipv4_cidr_block_value",
                    "services_secondary_range_name": "services_secondary_range_name_value",
                    "services_ipv4_cidr_block": "services_ipv4_cidr_block_value",
                },
                "enable_ip_masq_agent": True,
            },
            "private_environment_config": {
                "enable_private_environment": True,
                "private_cluster_config": {
                    "enable_private_endpoint": True,
                    "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                    "master_ipv4_reserved_range": "master_ipv4_reserved_range_value",
                },
                "web_server_ipv4_cidr_block": "web_server_ipv4_cidr_block_value",
                "cloud_sql_ipv4_cidr_block": "cloud_sql_ipv4_cidr_block_value",
                "web_server_ipv4_reserved_range": "web_server_ipv4_reserved_range_value",
                "cloud_composer_network_ipv4_cidr_block": "cloud_composer_network_ipv4_cidr_block_value",
                "cloud_composer_network_ipv4_reserved_range": "cloud_composer_network_ipv4_reserved_range_value",
                "enable_privately_used_public_ips": True,
                "cloud_composer_connection_subnetwork": "cloud_composer_connection_subnetwork_value",
                "networking_config": {"connection_type": 1},
            },
            "web_server_network_access_control": {
                "allowed_ip_ranges": [
                    {"value": "value_value", "description": "description_value"}
                ]
            },
            "database_config": {"machine_type": "machine_type_value"},
            "web_server_config": {"machine_type": "machine_type_value"},
            "encryption_config": {"kms_key_name": "kms_key_name_value"},
            "maintenance_window": {
                "start_time": {"seconds": 751, "nanos": 543},
                "end_time": {},
                "recurrence": "recurrence_value",
            },
            "workloads_config": {
                "scheduler": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "count": 553,
                },
                "web_server": {"cpu": 0.328, "memory_gb": 0.961, "storage_gb": 0.1053},
                "worker": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "min_count": 972,
                    "max_count": 974,
                },
            },
            "environment_size": 1,
            "airflow_uri": "airflow_uri_value",
            "airflow_byoid_uri": "airflow_byoid_uri_value",
            "master_authorized_networks_config": {
                "enabled": True,
                "cidr_blocks": [
                    {
                        "display_name": "display_name_value",
                        "cidr_block": "cidr_block_value",
                    }
                ],
            },
            "recovery_config": {
                "scheduled_snapshots_config": {
                    "enabled": True,
                    "snapshot_location": "snapshot_location_value",
                    "snapshot_creation_schedule": "snapshot_creation_schedule_value",
                    "time_zone": "time_zone_value",
                }
            },
            "resilience_mode": 1,
        },
        "uuid": "uuid_value",
        "state": 1,
        "create_time": {},
        "update_time": {},
        "labels": {},
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
        client.create_environment(request)


def test_create_environment_rest_flattened():
    client = EnvironmentsClient(
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
            environment=environments.Environment(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/environments"
            % client.transport._host,
            args[1],
        )


def test_create_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_environment(
            environments.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=environments.Environment(name="name_value"),
        )


def test_create_environment_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.GetEnvironmentRequest,
        dict,
    ],
)
def test_get_environment_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.Environment(
            name="name_value",
            uuid="uuid_value",
            state=environments.Environment.State.CREATING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.Environment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_environment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.Environment)
    assert response.name == "name_value"
    assert response.uuid == "uuid_value"
    assert response.state == environments.Environment.State.CREATING


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_get_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_get_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.GetEnvironmentRequest.pb(
            environments.GetEnvironmentRequest()
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
        req.return_value._content = environments.Environment.to_json(
            environments.Environment()
        )

        request = environments.GetEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.Environment()

        client.get_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_environment_rest_bad_request(
    transport: str = "rest", request_type=environments.GetEnvironmentRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
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
        client.get_environment(request)


def test_get_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.Environment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/environments/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.Environment.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_environment(
            environments.GetEnvironmentRequest(),
            name="name_value",
        )


def test_get_environment_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.ListEnvironmentsRequest,
        dict,
    ],
)
def test_list_environments_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.ListEnvironmentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.ListEnvironmentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_environments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_environments_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_list_environments"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_list_environments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.ListEnvironmentsRequest.pb(
            environments.ListEnvironmentsRequest()
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
        req.return_value._content = environments.ListEnvironmentsResponse.to_json(
            environments.ListEnvironmentsResponse()
        )

        request = environments.ListEnvironmentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.ListEnvironmentsResponse()

        client.list_environments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_environments_rest_bad_request(
    transport: str = "rest", request_type=environments.ListEnvironmentsRequest
):
    client = EnvironmentsClient(
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
        client.list_environments(request)


def test_list_environments_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.ListEnvironmentsResponse()

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
        pb_return_value = environments.ListEnvironmentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_environments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/environments"
            % client.transport._host,
            args[1],
        )


def test_list_environments_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_environments(
            environments.ListEnvironmentsRequest(),
            parent="parent_value",
        )


def test_list_environments_rest_pager(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                    environments.Environment(),
                ],
                next_page_token="abc",
            ),
            environments.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                ],
                next_page_token="ghi",
            ),
            environments.ListEnvironmentsResponse(
                environments=[
                    environments.Environment(),
                    environments.Environment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            environments.ListEnvironmentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_environments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environments.Environment) for i in results)

        pages = list(client.list_environments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        environments.UpdateEnvironmentRequest,
        dict,
    ],
)
def test_update_environment_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
    request_init["environment"] = {
        "name": "name_value",
        "config": {
            "gke_cluster": "gke_cluster_value",
            "dag_gcs_prefix": "dag_gcs_prefix_value",
            "node_count": 1070,
            "software_config": {
                "image_version": "image_version_value",
                "airflow_config_overrides": {},
                "pypi_packages": {},
                "env_variables": {},
                "python_version": "python_version_value",
                "scheduler_count": 1607,
            },
            "node_config": {
                "location": "location_value",
                "machine_type": "machine_type_value",
                "network": "network_value",
                "subnetwork": "subnetwork_value",
                "disk_size_gb": 1261,
                "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
                "service_account": "service_account_value",
                "tags": ["tags_value1", "tags_value2"],
                "ip_allocation_policy": {
                    "use_ip_aliases": True,
                    "cluster_secondary_range_name": "cluster_secondary_range_name_value",
                    "cluster_ipv4_cidr_block": "cluster_ipv4_cidr_block_value",
                    "services_secondary_range_name": "services_secondary_range_name_value",
                    "services_ipv4_cidr_block": "services_ipv4_cidr_block_value",
                },
                "enable_ip_masq_agent": True,
            },
            "private_environment_config": {
                "enable_private_environment": True,
                "private_cluster_config": {
                    "enable_private_endpoint": True,
                    "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                    "master_ipv4_reserved_range": "master_ipv4_reserved_range_value",
                },
                "web_server_ipv4_cidr_block": "web_server_ipv4_cidr_block_value",
                "cloud_sql_ipv4_cidr_block": "cloud_sql_ipv4_cidr_block_value",
                "web_server_ipv4_reserved_range": "web_server_ipv4_reserved_range_value",
                "cloud_composer_network_ipv4_cidr_block": "cloud_composer_network_ipv4_cidr_block_value",
                "cloud_composer_network_ipv4_reserved_range": "cloud_composer_network_ipv4_reserved_range_value",
                "enable_privately_used_public_ips": True,
                "cloud_composer_connection_subnetwork": "cloud_composer_connection_subnetwork_value",
                "networking_config": {"connection_type": 1},
            },
            "web_server_network_access_control": {
                "allowed_ip_ranges": [
                    {"value": "value_value", "description": "description_value"}
                ]
            },
            "database_config": {"machine_type": "machine_type_value"},
            "web_server_config": {"machine_type": "machine_type_value"},
            "encryption_config": {"kms_key_name": "kms_key_name_value"},
            "maintenance_window": {
                "start_time": {"seconds": 751, "nanos": 543},
                "end_time": {},
                "recurrence": "recurrence_value",
            },
            "workloads_config": {
                "scheduler": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "count": 553,
                },
                "web_server": {"cpu": 0.328, "memory_gb": 0.961, "storage_gb": 0.1053},
                "worker": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "min_count": 972,
                    "max_count": 974,
                },
            },
            "environment_size": 1,
            "airflow_uri": "airflow_uri_value",
            "airflow_byoid_uri": "airflow_byoid_uri_value",
            "master_authorized_networks_config": {
                "enabled": True,
                "cidr_blocks": [
                    {
                        "display_name": "display_name_value",
                        "cidr_block": "cidr_block_value",
                    }
                ],
            },
            "recovery_config": {
                "scheduled_snapshots_config": {
                    "enabled": True,
                    "snapshot_location": "snapshot_location_value",
                    "snapshot_creation_schedule": "snapshot_creation_schedule_value",
                    "time_zone": "time_zone_value",
                }
            },
            "resilience_mode": 1,
        },
        "uuid": "uuid_value",
        "state": 1,
        "create_time": {},
        "update_time": {},
        "labels": {},
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
        response = client.update_environment(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_update_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_update_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.UpdateEnvironmentRequest.pb(
            environments.UpdateEnvironmentRequest()
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

        request = environments.UpdateEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_environment_rest_bad_request(
    transport: str = "rest", request_type=environments.UpdateEnvironmentRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
    request_init["environment"] = {
        "name": "name_value",
        "config": {
            "gke_cluster": "gke_cluster_value",
            "dag_gcs_prefix": "dag_gcs_prefix_value",
            "node_count": 1070,
            "software_config": {
                "image_version": "image_version_value",
                "airflow_config_overrides": {},
                "pypi_packages": {},
                "env_variables": {},
                "python_version": "python_version_value",
                "scheduler_count": 1607,
            },
            "node_config": {
                "location": "location_value",
                "machine_type": "machine_type_value",
                "network": "network_value",
                "subnetwork": "subnetwork_value",
                "disk_size_gb": 1261,
                "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
                "service_account": "service_account_value",
                "tags": ["tags_value1", "tags_value2"],
                "ip_allocation_policy": {
                    "use_ip_aliases": True,
                    "cluster_secondary_range_name": "cluster_secondary_range_name_value",
                    "cluster_ipv4_cidr_block": "cluster_ipv4_cidr_block_value",
                    "services_secondary_range_name": "services_secondary_range_name_value",
                    "services_ipv4_cidr_block": "services_ipv4_cidr_block_value",
                },
                "enable_ip_masq_agent": True,
            },
            "private_environment_config": {
                "enable_private_environment": True,
                "private_cluster_config": {
                    "enable_private_endpoint": True,
                    "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                    "master_ipv4_reserved_range": "master_ipv4_reserved_range_value",
                },
                "web_server_ipv4_cidr_block": "web_server_ipv4_cidr_block_value",
                "cloud_sql_ipv4_cidr_block": "cloud_sql_ipv4_cidr_block_value",
                "web_server_ipv4_reserved_range": "web_server_ipv4_reserved_range_value",
                "cloud_composer_network_ipv4_cidr_block": "cloud_composer_network_ipv4_cidr_block_value",
                "cloud_composer_network_ipv4_reserved_range": "cloud_composer_network_ipv4_reserved_range_value",
                "enable_privately_used_public_ips": True,
                "cloud_composer_connection_subnetwork": "cloud_composer_connection_subnetwork_value",
                "networking_config": {"connection_type": 1},
            },
            "web_server_network_access_control": {
                "allowed_ip_ranges": [
                    {"value": "value_value", "description": "description_value"}
                ]
            },
            "database_config": {"machine_type": "machine_type_value"},
            "web_server_config": {"machine_type": "machine_type_value"},
            "encryption_config": {"kms_key_name": "kms_key_name_value"},
            "maintenance_window": {
                "start_time": {"seconds": 751, "nanos": 543},
                "end_time": {},
                "recurrence": "recurrence_value",
            },
            "workloads_config": {
                "scheduler": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "count": 553,
                },
                "web_server": {"cpu": 0.328, "memory_gb": 0.961, "storage_gb": 0.1053},
                "worker": {
                    "cpu": 0.328,
                    "memory_gb": 0.961,
                    "storage_gb": 0.1053,
                    "min_count": 972,
                    "max_count": 974,
                },
            },
            "environment_size": 1,
            "airflow_uri": "airflow_uri_value",
            "airflow_byoid_uri": "airflow_byoid_uri_value",
            "master_authorized_networks_config": {
                "enabled": True,
                "cidr_blocks": [
                    {
                        "display_name": "display_name_value",
                        "cidr_block": "cidr_block_value",
                    }
                ],
            },
            "recovery_config": {
                "scheduled_snapshots_config": {
                    "enabled": True,
                    "snapshot_location": "snapshot_location_value",
                    "snapshot_creation_schedule": "snapshot_creation_schedule_value",
                    "time_zone": "time_zone_value",
                }
            },
            "resilience_mode": 1,
        },
        "uuid": "uuid_value",
        "state": 1,
        "create_time": {},
        "update_time": {},
        "labels": {},
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
        client.update_environment(request)


def test_update_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/environments/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_environment(
            environments.UpdateEnvironmentRequest(),
            name="name_value",
            environment=environments.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_environment_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.DeleteEnvironmentRequest,
        dict,
    ],
)
def test_delete_environment_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
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
        response = client.delete_environment(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_delete_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_delete_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.DeleteEnvironmentRequest.pb(
            environments.DeleteEnvironmentRequest()
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

        request = environments.DeleteEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_environment_rest_bad_request(
    transport: str = "rest", request_type=environments.DeleteEnvironmentRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/environments/sample3"}
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
        client.delete_environment(request)


def test_delete_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/environments/sample3"
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

        client.delete_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_environment(
            environments.DeleteEnvironmentRequest(),
            name="name_value",
        )


def test_delete_environment_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.ExecuteAirflowCommandRequest,
        dict,
    ],
)
def test_execute_airflow_command_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.ExecuteAirflowCommandResponse(
            execution_id="execution_id_value",
            pod="pod_value",
            pod_namespace="pod_namespace_value",
            error="error_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.ExecuteAirflowCommandResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.execute_airflow_command(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.ExecuteAirflowCommandResponse)
    assert response.execution_id == "execution_id_value"
    assert response.pod == "pod_value"
    assert response.pod_namespace == "pod_namespace_value"
    assert response.error == "error_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_execute_airflow_command_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_execute_airflow_command"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_execute_airflow_command"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.ExecuteAirflowCommandRequest.pb(
            environments.ExecuteAirflowCommandRequest()
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
        req.return_value._content = environments.ExecuteAirflowCommandResponse.to_json(
            environments.ExecuteAirflowCommandResponse()
        )

        request = environments.ExecuteAirflowCommandRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.ExecuteAirflowCommandResponse()

        client.execute_airflow_command(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_execute_airflow_command_rest_bad_request(
    transport: str = "rest", request_type=environments.ExecuteAirflowCommandRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.execute_airflow_command(request)


def test_execute_airflow_command_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.StopAirflowCommandRequest,
        dict,
    ],
)
def test_stop_airflow_command_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.StopAirflowCommandResponse(
            is_done=True,
            output=["output_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.StopAirflowCommandResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.stop_airflow_command(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.StopAirflowCommandResponse)
    assert response.is_done is True
    assert response.output == ["output_value"]


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_stop_airflow_command_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_stop_airflow_command"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_stop_airflow_command"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.StopAirflowCommandRequest.pb(
            environments.StopAirflowCommandRequest()
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
        req.return_value._content = environments.StopAirflowCommandResponse.to_json(
            environments.StopAirflowCommandResponse()
        )

        request = environments.StopAirflowCommandRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.StopAirflowCommandResponse()

        client.stop_airflow_command(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_stop_airflow_command_rest_bad_request(
    transport: str = "rest", request_type=environments.StopAirflowCommandRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.stop_airflow_command(request)


def test_stop_airflow_command_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.PollAirflowCommandRequest,
        dict,
    ],
)
def test_poll_airflow_command_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.PollAirflowCommandResponse(
            output_end=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.PollAirflowCommandResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.poll_airflow_command(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.PollAirflowCommandResponse)
    assert response.output_end is True


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_poll_airflow_command_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_poll_airflow_command"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_poll_airflow_command"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.PollAirflowCommandRequest.pb(
            environments.PollAirflowCommandRequest()
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
        req.return_value._content = environments.PollAirflowCommandResponse.to_json(
            environments.PollAirflowCommandResponse()
        )

        request = environments.PollAirflowCommandRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.PollAirflowCommandResponse()

        client.poll_airflow_command(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_poll_airflow_command_rest_bad_request(
    transport: str = "rest", request_type=environments.PollAirflowCommandRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.poll_airflow_command(request)


def test_poll_airflow_command_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.SaveSnapshotRequest,
        dict,
    ],
)
def test_save_snapshot_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        response = client.save_snapshot(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_save_snapshot_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_save_snapshot"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_save_snapshot"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.SaveSnapshotRequest.pb(
            environments.SaveSnapshotRequest()
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

        request = environments.SaveSnapshotRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.save_snapshot(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_save_snapshot_rest_bad_request(
    transport: str = "rest", request_type=environments.SaveSnapshotRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.save_snapshot(request)


def test_save_snapshot_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.LoadSnapshotRequest,
        dict,
    ],
)
def test_load_snapshot_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        response = client.load_snapshot(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_load_snapshot_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_load_snapshot"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_load_snapshot"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.LoadSnapshotRequest.pb(
            environments.LoadSnapshotRequest()
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

        request = environments.LoadSnapshotRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.load_snapshot(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_load_snapshot_rest_bad_request(
    transport: str = "rest", request_type=environments.LoadSnapshotRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.load_snapshot(request)


def test_load_snapshot_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.DatabaseFailoverRequest,
        dict,
    ],
)
def test_database_failover_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        response = client.database_failover(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_database_failover_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_database_failover"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_database_failover"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.DatabaseFailoverRequest.pb(
            environments.DatabaseFailoverRequest()
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

        request = environments.DatabaseFailoverRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.database_failover(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_database_failover_rest_bad_request(
    transport: str = "rest", request_type=environments.DatabaseFailoverRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.database_failover(request)


def test_database_failover_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        environments.FetchDatabasePropertiesRequest,
        dict,
    ],
)
def test_fetch_database_properties_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environments.FetchDatabasePropertiesResponse(
            primary_gce_zone="primary_gce_zone_value",
            secondary_gce_zone="secondary_gce_zone_value",
            is_failover_replica_available=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = environments.FetchDatabasePropertiesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.fetch_database_properties(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environments.FetchDatabasePropertiesResponse)
    assert response.primary_gce_zone == "primary_gce_zone_value"
    assert response.secondary_gce_zone == "secondary_gce_zone_value"
    assert response.is_failover_replica_available is True


def test_fetch_database_properties_rest_required_fields(
    request_type=environments.FetchDatabasePropertiesRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["environment"] = ""
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
    ).fetch_database_properties._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["environment"] = "environment_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).fetch_database_properties._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "environment" in jsonified_request
    assert jsonified_request["environment"] == "environment_value"

    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = environments.FetchDatabasePropertiesResponse()
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

            pb_return_value = environments.FetchDatabasePropertiesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.fetch_database_properties(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_fetch_database_properties_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.fetch_database_properties._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("environment",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_fetch_database_properties_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_fetch_database_properties"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_fetch_database_properties"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environments.FetchDatabasePropertiesRequest.pb(
            environments.FetchDatabasePropertiesRequest()
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
            environments.FetchDatabasePropertiesResponse.to_json(
                environments.FetchDatabasePropertiesResponse()
            )
        )

        request = environments.FetchDatabasePropertiesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environments.FetchDatabasePropertiesResponse()

        client.fetch_database_properties(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_fetch_database_properties_rest_bad_request(
    transport: str = "rest", request_type=environments.FetchDatabasePropertiesRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/environments/sample3"
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
        client.fetch_database_properties(request)


def test_fetch_database_properties_rest_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = EnvironmentsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.EnvironmentsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
        transports.EnvironmentsRestTransport,
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
    transport = EnvironmentsClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.EnvironmentsGrpcTransport,
    )


def test_environments_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.EnvironmentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_environments_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.orchestration.airflow.service_v1.services.environments.transports.EnvironmentsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.EnvironmentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_environment",
        "get_environment",
        "list_environments",
        "update_environment",
        "delete_environment",
        "execute_airflow_command",
        "stop_airflow_command",
        "poll_airflow_command",
        "save_snapshot",
        "load_snapshot",
        "database_failover",
        "fetch_database_properties",
        "get_operation",
        "delete_operation",
        "list_operations",
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


def test_environments_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.orchestration.airflow.service_v1.services.environments.transports.EnvironmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EnvironmentsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_environments_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.orchestration.airflow.service_v1.services.environments.transports.EnvironmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EnvironmentsTransport()
        adc.assert_called_once()


def test_environments_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        EnvironmentsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
    ],
)
def test_environments_transport_auth_adc(transport_class):
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
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
        transports.EnvironmentsRestTransport,
    ],
)
def test_environments_transport_auth_gdch_credentials(transport_class):
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
        (transports.EnvironmentsGrpcTransport, grpc_helpers),
        (transports.EnvironmentsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_environments_transport_create_channel(transport_class, grpc_helpers):
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
            "composer.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="composer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_environments_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.EnvironmentsRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_environments_rest_lro_client():
    client = EnvironmentsClient(
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
def test_environments_host_no_port(transport_name):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="composer.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "composer.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://composer.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_environments_host_with_port(transport_name):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="composer.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "composer.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://composer.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_environments_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = EnvironmentsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = EnvironmentsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_environment._session
    session2 = client2.transport.create_environment._session
    assert session1 != session2
    session1 = client1.transport.get_environment._session
    session2 = client2.transport.get_environment._session
    assert session1 != session2
    session1 = client1.transport.list_environments._session
    session2 = client2.transport.list_environments._session
    assert session1 != session2
    session1 = client1.transport.update_environment._session
    session2 = client2.transport.update_environment._session
    assert session1 != session2
    session1 = client1.transport.delete_environment._session
    session2 = client2.transport.delete_environment._session
    assert session1 != session2
    session1 = client1.transport.execute_airflow_command._session
    session2 = client2.transport.execute_airflow_command._session
    assert session1 != session2
    session1 = client1.transport.stop_airflow_command._session
    session2 = client2.transport.stop_airflow_command._session
    assert session1 != session2
    session1 = client1.transport.poll_airflow_command._session
    session2 = client2.transport.poll_airflow_command._session
    assert session1 != session2
    session1 = client1.transport.save_snapshot._session
    session2 = client2.transport.save_snapshot._session
    assert session1 != session2
    session1 = client1.transport.load_snapshot._session
    session2 = client2.transport.load_snapshot._session
    assert session1 != session2
    session1 = client1.transport.database_failover._session
    session2 = client2.transport.database_failover._session
    assert session1 != session2
    session1 = client1.transport.fetch_database_properties._session
    session2 = client2.transport.fetch_database_properties._session
    assert session1 != session2


def test_environments_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EnvironmentsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_environments_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EnvironmentsGrpcAsyncIOTransport(
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
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_transport_channel_mtls_with_adc(transport_class):
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


def test_environments_grpc_lro_client():
    client = EnvironmentsClient(
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


def test_environments_grpc_lro_async_client():
    client = EnvironmentsAsyncClient(
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


def test_environment_path():
    project = "squid"
    location = "clam"
    environment = "whelk"
    expected = (
        "projects/{project}/locations/{location}/environments/{environment}".format(
            project=project,
            location=location,
            environment=environment,
        )
    )
    actual = EnvironmentsClient.environment_path(project, location, environment)
    assert expected == actual


def test_parse_environment_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "environment": "nudibranch",
    }
    path = EnvironmentsClient.environment_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_environment_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = EnvironmentsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = EnvironmentsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = EnvironmentsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = EnvironmentsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = EnvironmentsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = EnvironmentsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = EnvironmentsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = EnvironmentsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = EnvironmentsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = EnvironmentsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.EnvironmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.EnvironmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = EnvironmentsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
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
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
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
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = EnvironmentsClient(
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
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
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
async def test_delete_operation_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
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


def test_delete_operation_from_dict():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
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
async def test_get_operation_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
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


def test_get_operation_from_dict():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
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
async def test_list_operations_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
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


def test_list_operations_from_dict():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = EnvironmentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
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
        client = EnvironmentsClient(
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
        client = EnvironmentsClient(
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
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport),
        (EnvironmentsAsyncClient, transports.EnvironmentsGrpcAsyncIOTransport),
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
