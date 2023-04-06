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
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.cloud.speech_v2.services.speech import SpeechAsyncClient
from google.cloud.speech_v2.services.speech import SpeechClient
from google.cloud.speech_v2.services.speech import pagers
from google.cloud.speech_v2.services.speech import transports
from google.cloud.speech_v2.types import cloud_speech
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


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

    assert SpeechClient._get_default_mtls_endpoint(None) is None
    assert SpeechClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        SpeechClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        SpeechClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SpeechClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert SpeechClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (SpeechClient, "grpc"),
        (SpeechAsyncClient, "grpc_asyncio"),
        (SpeechClient, "rest"),
    ],
)
def test_speech_client_from_service_account_info(client_class, transport_name):
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
            "speech.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://speech.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.SpeechGrpcTransport, "grpc"),
        (transports.SpeechGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.SpeechRestTransport, "rest"),
    ],
)
def test_speech_client_service_account_always_use_jwt(transport_class, transport_name):
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
        (SpeechClient, "grpc"),
        (SpeechAsyncClient, "grpc_asyncio"),
        (SpeechClient, "rest"),
    ],
)
def test_speech_client_from_service_account_file(client_class, transport_name):
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
            "speech.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://speech.googleapis.com"
        )


def test_speech_client_get_transport_class():
    transport = SpeechClient.get_transport_class()
    available_transports = [
        transports.SpeechGrpcTransport,
        transports.SpeechRestTransport,
    ]
    assert transport in available_transports

    transport = SpeechClient.get_transport_class("grpc")
    assert transport == transports.SpeechGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SpeechClient, transports.SpeechGrpcTransport, "grpc"),
        (SpeechAsyncClient, transports.SpeechGrpcAsyncIOTransport, "grpc_asyncio"),
        (SpeechClient, transports.SpeechRestTransport, "rest"),
    ],
)
@mock.patch.object(
    SpeechClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechClient)
)
@mock.patch.object(
    SpeechAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechAsyncClient)
)
def test_speech_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SpeechClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SpeechClient, "get_transport_class") as gtc:
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
        (SpeechClient, transports.SpeechGrpcTransport, "grpc", "true"),
        (
            SpeechAsyncClient,
            transports.SpeechGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SpeechClient, transports.SpeechGrpcTransport, "grpc", "false"),
        (
            SpeechAsyncClient,
            transports.SpeechGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (SpeechClient, transports.SpeechRestTransport, "rest", "true"),
        (SpeechClient, transports.SpeechRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    SpeechClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechClient)
)
@mock.patch.object(
    SpeechAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_speech_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [SpeechClient, SpeechAsyncClient])
@mock.patch.object(
    SpeechClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechClient)
)
@mock.patch.object(
    SpeechAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SpeechAsyncClient)
)
def test_speech_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (SpeechClient, transports.SpeechGrpcTransport, "grpc"),
        (SpeechAsyncClient, transports.SpeechGrpcAsyncIOTransport, "grpc_asyncio"),
        (SpeechClient, transports.SpeechRestTransport, "rest"),
    ],
)
def test_speech_client_client_options_scopes(
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
        (SpeechClient, transports.SpeechGrpcTransport, "grpc", grpc_helpers),
        (
            SpeechAsyncClient,
            transports.SpeechGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (SpeechClient, transports.SpeechRestTransport, "rest", None),
    ],
)
def test_speech_client_client_options_credentials_file(
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


def test_speech_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.speech_v2.services.speech.transports.SpeechGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SpeechClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (SpeechClient, transports.SpeechGrpcTransport, "grpc", grpc_helpers),
        (
            SpeechAsyncClient,
            transports.SpeechGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_speech_client_create_channel_credentials_file(
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
            "speech.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="speech.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreateRecognizerRequest,
        dict,
    ],
)
def test_create_recognizer(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_recognizer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        client.create_recognizer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateRecognizerRequest()


@pytest.mark.asyncio
async def test_create_recognizer_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.CreateRecognizerRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_recognizer_async_from_dict():
    await test_create_recognizer_async(request_type=dict)


def test_create_recognizer_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreateRecognizerRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_recognizer(request)

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
async def test_create_recognizer_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreateRecognizerRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_recognizer(request)

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


def test_create_recognizer_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_recognizer(
            parent="parent_value",
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].recognizer
        mock_val = cloud_speech.Recognizer(name="name_value")
        assert arg == mock_val
        arg = args[0].recognizer_id
        mock_val = "recognizer_id_value"
        assert arg == mock_val


def test_create_recognizer_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_recognizer(
            cloud_speech.CreateRecognizerRequest(),
            parent="parent_value",
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )


@pytest.mark.asyncio
async def test_create_recognizer_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_recognizer(
            parent="parent_value",
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].recognizer
        mock_val = cloud_speech.Recognizer(name="name_value")
        assert arg == mock_val
        arg = args[0].recognizer_id
        mock_val = "recognizer_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_recognizer_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_recognizer(
            cloud_speech.CreateRecognizerRequest(),
            parent="parent_value",
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListRecognizersRequest,
        dict,
    ],
)
def test_list_recognizers(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListRecognizersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_recognizers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListRecognizersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecognizersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_recognizers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        client.list_recognizers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListRecognizersRequest()


@pytest.mark.asyncio
async def test_list_recognizers_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.ListRecognizersRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListRecognizersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_recognizers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListRecognizersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecognizersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_recognizers_async_from_dict():
    await test_list_recognizers_async(request_type=dict)


def test_list_recognizers_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListRecognizersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        call.return_value = cloud_speech.ListRecognizersResponse()
        client.list_recognizers(request)

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
async def test_list_recognizers_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListRecognizersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListRecognizersResponse()
        )
        await client.list_recognizers(request)

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


def test_list_recognizers_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListRecognizersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_recognizers(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_recognizers_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_recognizers(
            cloud_speech.ListRecognizersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_recognizers_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListRecognizersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListRecognizersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_recognizers(
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
async def test_list_recognizers_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_recognizers(
            cloud_speech.ListRecognizersRequest(),
            parent="parent_value",
        )


def test_list_recognizers_pager(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[],
                next_page_token="def",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_recognizers(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.Recognizer) for i in results)


def test_list_recognizers_pages(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_recognizers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[],
                next_page_token="def",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_recognizers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_recognizers_async_pager():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recognizers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[],
                next_page_token="def",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_recognizers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_speech.Recognizer) for i in responses)


@pytest.mark.asyncio
async def test_list_recognizers_async_pages():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recognizers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[],
                next_page_token="def",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_recognizers(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetRecognizerRequest,
        dict,
    ],
)
def test_get_recognizer(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Recognizer(
            name="name_value",
            uid="uid_value",
            display_name="display_name_value",
            model="model_value",
            language_codes=["language_codes_value"],
            state=cloud_speech.Recognizer.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )
        response = client.get_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Recognizer)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.model == "model_value"
    assert response.language_codes == ["language_codes_value"]
    assert response.state == cloud_speech.Recognizer.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_recognizer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        client.get_recognizer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetRecognizerRequest()


@pytest.mark.asyncio
async def test_get_recognizer_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.GetRecognizerRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.Recognizer(
                name="name_value",
                uid="uid_value",
                display_name="display_name_value",
                model="model_value",
                language_codes=["language_codes_value"],
                state=cloud_speech.Recognizer.State.ACTIVE,
                etag="etag_value",
                reconciling=True,
                kms_key_name="kms_key_name_value",
                kms_key_version_name="kms_key_version_name_value",
            )
        )
        response = await client.get_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Recognizer)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.model == "model_value"
    assert response.language_codes == ["language_codes_value"]
    assert response.state == cloud_speech.Recognizer.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


@pytest.mark.asyncio
async def test_get_recognizer_async_from_dict():
    await test_get_recognizer_async(request_type=dict)


def test_get_recognizer_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        call.return_value = cloud_speech.Recognizer()
        client.get_recognizer(request)

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
async def test_get_recognizer_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.Recognizer()
        )
        await client.get_recognizer(request)

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


def test_get_recognizer_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Recognizer()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_recognizer(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_recognizer_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_recognizer(
            cloud_speech.GetRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_recognizer_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_recognizer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Recognizer()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.Recognizer()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_recognizer(
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
async def test_get_recognizer_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_recognizer(
            cloud_speech.GetRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateRecognizerRequest,
        dict,
    ],
)
def test_update_recognizer(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_recognizer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        client.update_recognizer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateRecognizerRequest()


@pytest.mark.asyncio
async def test_update_recognizer_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UpdateRecognizerRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_recognizer_async_from_dict():
    await test_update_recognizer_async(request_type=dict)


def test_update_recognizer_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateRecognizerRequest()

    request.recognizer.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_recognizer_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateRecognizerRequest()

    request.recognizer.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer.name=name_value",
    ) in kw["metadata"]


def test_update_recognizer_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_recognizer(
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = cloud_speech.Recognizer(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_recognizer_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_recognizer(
            cloud_speech.UpdateRecognizerRequest(),
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_recognizer_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_recognizer(
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = cloud_speech.Recognizer(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_recognizer_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_recognizer(
            cloud_speech.UpdateRecognizerRequest(),
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeleteRecognizerRequest,
        dict,
    ],
)
def test_delete_recognizer(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_recognizer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        client.delete_recognizer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteRecognizerRequest()


@pytest.mark.asyncio
async def test_delete_recognizer_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.DeleteRecognizerRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_recognizer_async_from_dict():
    await test_delete_recognizer_async(request_type=dict)


def test_delete_recognizer_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeleteRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_recognizer(request)

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
async def test_delete_recognizer_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeleteRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_recognizer(request)

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


def test_delete_recognizer_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_recognizer(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_recognizer_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_recognizer(
            cloud_speech.DeleteRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_recognizer_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_recognizer(
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
async def test_delete_recognizer_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_recognizer(
            cloud_speech.DeleteRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeleteRecognizerRequest,
        dict,
    ],
)
def test_undelete_recognizer(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undelete_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undelete_recognizer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        client.undelete_recognizer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteRecognizerRequest()


@pytest.mark.asyncio
async def test_undelete_recognizer_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UndeleteRecognizerRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undelete_recognizer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteRecognizerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undelete_recognizer_async_from_dict():
    await test_undelete_recognizer_async(request_type=dict)


def test_undelete_recognizer_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeleteRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undelete_recognizer(request)

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
async def test_undelete_recognizer_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeleteRecognizerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undelete_recognizer(request)

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


def test_undelete_recognizer_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undelete_recognizer(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_undelete_recognizer_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_recognizer(
            cloud_speech.UndeleteRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_undelete_recognizer_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_recognizer), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undelete_recognizer(
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
async def test_undelete_recognizer_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undelete_recognizer(
            cloud_speech.UndeleteRecognizerRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.RecognizeRequest,
        dict,
    ],
)
def test_recognize(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.RecognizeResponse()
        response = client.recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.RecognizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.RecognizeResponse)


def test_recognize_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        client.recognize()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.RecognizeRequest()


@pytest.mark.asyncio
async def test_recognize_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.RecognizeRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.RecognizeResponse()
        )
        response = await client.recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.RecognizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.RecognizeResponse)


@pytest.mark.asyncio
async def test_recognize_async_from_dict():
    await test_recognize_async(request_type=dict)


def test_recognize_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.RecognizeRequest()

    request.recognizer = "recognizer_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        call.return_value = cloud_speech.RecognizeResponse()
        client.recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer=recognizer_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_recognize_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.RecognizeRequest()

    request.recognizer = "recognizer_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.RecognizeResponse()
        )
        await client.recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer=recognizer_value",
    ) in kw["metadata"]


def test_recognize_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.RecognizeResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.recognize(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            content=b"content_blob",
            uri="uri_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = "recognizer_value"
        assert arg == mock_val
        arg = args[0].config
        mock_val = cloud_speech.RecognitionConfig(auto_decoding_config=None)
        assert arg == mock_val
        arg = args[0].config_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        assert args[0].uri == "uri_value"


def test_recognize_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.recognize(
            cloud_speech.RecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            content=b"content_blob",
            uri="uri_value",
        )


@pytest.mark.asyncio
async def test_recognize_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.RecognizeResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.RecognizeResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.recognize(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            content=b"content_blob",
            uri="uri_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = "recognizer_value"
        assert arg == mock_val
        arg = args[0].config
        mock_val = cloud_speech.RecognitionConfig(auto_decoding_config=None)
        assert arg == mock_val
        arg = args[0].config_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        assert args[0].uri == "uri_value"


@pytest.mark.asyncio
async def test_recognize_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.recognize(
            cloud_speech.RecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            content=b"content_blob",
            uri="uri_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.StreamingRecognizeRequest,
        dict,
    ],
)
def test_streaming_recognize(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.streaming_recognize), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([cloud_speech.StreamingRecognizeResponse()])
        response = client.streaming_recognize(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, cloud_speech.StreamingRecognizeResponse)


@pytest.mark.asyncio
async def test_streaming_recognize_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.StreamingRecognizeRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.streaming_recognize), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[cloud_speech.StreamingRecognizeResponse()]
        )
        response = await client.streaming_recognize(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, cloud_speech.StreamingRecognizeResponse)


@pytest.mark.asyncio
async def test_streaming_recognize_async_from_dict():
    await test_streaming_recognize_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.BatchRecognizeRequest,
        dict,
    ],
)
def test_batch_recognize(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.batch_recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.BatchRecognizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_batch_recognize_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        client.batch_recognize()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.BatchRecognizeRequest()


@pytest.mark.asyncio
async def test_batch_recognize_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.BatchRecognizeRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.batch_recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.BatchRecognizeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_batch_recognize_async_from_dict():
    await test_batch_recognize_async(request_type=dict)


def test_batch_recognize_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.BatchRecognizeRequest()

    request.recognizer = "recognizer_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.batch_recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer=recognizer_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_recognize_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.BatchRecognizeRequest()

    request.recognizer = "recognizer_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.batch_recognize(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "recognizer=recognizer_value",
    ) in kw["metadata"]


def test_batch_recognize_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_recognize(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = "recognizer_value"
        assert arg == mock_val
        arg = args[0].config
        mock_val = cloud_speech.RecognitionConfig(auto_decoding_config=None)
        assert arg == mock_val
        arg = args[0].config_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        arg = args[0].files
        mock_val = [cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")]
        assert arg == mock_val


def test_batch_recognize_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_recognize(
            cloud_speech.BatchRecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )


@pytest.mark.asyncio
async def test_batch_recognize_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.batch_recognize), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_recognize(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].recognizer
        mock_val = "recognizer_value"
        assert arg == mock_val
        arg = args[0].config
        mock_val = cloud_speech.RecognitionConfig(auto_decoding_config=None)
        assert arg == mock_val
        arg = args[0].config_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val
        arg = args[0].files
        mock_val = [cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_batch_recognize_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_recognize(
            cloud_speech.BatchRecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetConfigRequest,
        dict,
    ],
)
def test_get_config(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config(
            name="name_value",
            kms_key_name="kms_key_name_value",
        )
        response = client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_get_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        client.get_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetConfigRequest()


@pytest.mark.asyncio
async def test_get_config_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.GetConfigRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.Config(
                name="name_value",
                kms_key_name="kms_key_name_value",
            )
        )
        response = await client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


@pytest.mark.asyncio
async def test_get_config_async_from_dict():
    await test_get_config_async(request_type=dict)


def test_get_config_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        call.return_value = cloud_speech.Config()
        client.get_config(request)

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
async def test_get_config_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_speech.Config())
        await client.get_config(request)

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


def test_get_config_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_config_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_config(
            cloud_speech.GetConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_config_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_speech.Config())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_config(
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
async def test_get_config_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_config(
            cloud_speech.GetConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateConfigRequest,
        dict,
    ],
)
def test_update_config(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config(
            name="name_value",
            kms_key_name="kms_key_name_value",
        )
        response = client.update_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_update_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        client.update_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateConfigRequest()


@pytest.mark.asyncio
async def test_update_config_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UpdateConfigRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.Config(
                name="name_value",
                kms_key_name="kms_key_name_value",
            )
        )
        response = await client.update_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


@pytest.mark.asyncio
async def test_update_config_async_from_dict():
    await test_update_config_async(request_type=dict)


def test_update_config_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateConfigRequest()

    request.config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        call.return_value = cloud_speech.Config()
        client.update_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_config_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateConfigRequest()

    request.config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_speech.Config())
        await client.update_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "config.name=name_value",
    ) in kw["metadata"]


def test_update_config_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_config(
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].config
        mock_val = cloud_speech.Config(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_config_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_config(
            cloud_speech.UpdateConfigRequest(),
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_config_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.Config()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_speech.Config())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_config(
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].config
        mock_val = cloud_speech.Config(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_config_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_config(
            cloud_speech.UpdateConfigRequest(),
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreateCustomClassRequest,
        dict,
    ],
)
def test_create_custom_class(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        client.create_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateCustomClassRequest()


@pytest.mark.asyncio
async def test_create_custom_class_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.CreateCustomClassRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_custom_class_async_from_dict():
    await test_create_custom_class_async(request_type=dict)


def test_create_custom_class_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreateCustomClassRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_custom_class(request)

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
async def test_create_custom_class_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreateCustomClassRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_custom_class(request)

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


def test_create_custom_class_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_class(
            parent="parent_value",
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_class
        mock_val = cloud_speech.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].custom_class_id
        mock_val = "custom_class_id_value"
        assert arg == mock_val


def test_create_custom_class_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_class(
            cloud_speech.CreateCustomClassRequest(),
            parent="parent_value",
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )


@pytest.mark.asyncio
async def test_create_custom_class_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_class(
            parent="parent_value",
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_class
        mock_val = cloud_speech.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].custom_class_id
        mock_val = "custom_class_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_custom_class_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_class(
            cloud_speech.CreateCustomClassRequest(),
            parent="parent_value",
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListCustomClassesRequest,
        dict,
    ],
)
def test_list_custom_classes(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListCustomClassesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListCustomClassesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomClassesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_classes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        client.list_custom_classes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListCustomClassesRequest()


@pytest.mark.asyncio
async def test_list_custom_classes_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.ListCustomClassesRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListCustomClassesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListCustomClassesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomClassesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_classes_async_from_dict():
    await test_list_custom_classes_async(request_type=dict)


def test_list_custom_classes_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListCustomClassesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        call.return_value = cloud_speech.ListCustomClassesResponse()
        client.list_custom_classes(request)

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
async def test_list_custom_classes_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListCustomClassesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListCustomClassesResponse()
        )
        await client.list_custom_classes(request)

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


def test_list_custom_classes_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListCustomClassesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_classes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_custom_classes_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_classes(
            cloud_speech.ListCustomClassesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_classes_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListCustomClassesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListCustomClassesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_classes(
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
async def test_list_custom_classes_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_classes(
            cloud_speech.ListCustomClassesRequest(),
            parent="parent_value",
        )


def test_list_custom_classes_pager(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[],
                next_page_token="def",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_classes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.CustomClass) for i in results)


def test_list_custom_classes_pages(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[],
                next_page_token="def",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_classes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_classes_async_pager():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[],
                next_page_token="def",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_classes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_speech.CustomClass) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_classes_async_pages():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[],
                next_page_token="def",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_custom_classes(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetCustomClassRequest,
        dict,
    ],
)
def test_get_custom_class(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.CustomClass(
            name="name_value",
            uid="uid_value",
            display_name="display_name_value",
            state=cloud_speech.CustomClass.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )
        response = client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.CustomClass)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.CustomClass.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        client.get_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetCustomClassRequest()


@pytest.mark.asyncio
async def test_get_custom_class_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.GetCustomClassRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.CustomClass(
                name="name_value",
                uid="uid_value",
                display_name="display_name_value",
                state=cloud_speech.CustomClass.State.ACTIVE,
                etag="etag_value",
                reconciling=True,
                kms_key_name="kms_key_name_value",
                kms_key_version_name="kms_key_version_name_value",
            )
        )
        response = await client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.CustomClass)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.CustomClass.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


@pytest.mark.asyncio
async def test_get_custom_class_async_from_dict():
    await test_get_custom_class_async(request_type=dict)


def test_get_custom_class_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        call.return_value = cloud_speech.CustomClass()
        client.get_custom_class(request)

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
async def test_get_custom_class_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.CustomClass()
        )
        await client.get_custom_class(request)

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


def test_get_custom_class_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.CustomClass()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_class(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_custom_class_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_class(
            cloud_speech.GetCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_class_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.CustomClass()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.CustomClass()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_class(
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
async def test_get_custom_class_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_class(
            cloud_speech.GetCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateCustomClassRequest,
        dict,
    ],
)
def test_update_custom_class(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        client.update_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateCustomClassRequest()


@pytest.mark.asyncio
async def test_update_custom_class_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UpdateCustomClassRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_custom_class_async_from_dict():
    await test_update_custom_class_async(request_type=dict)


def test_update_custom_class_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateCustomClassRequest()

    request.custom_class.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_class.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_class_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdateCustomClassRequest()

    request.custom_class.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_class.name=name_value",
    ) in kw["metadata"]


def test_update_custom_class_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_class(
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_class
        mock_val = cloud_speech.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_custom_class_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_class(
            cloud_speech.UpdateCustomClassRequest(),
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_class_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_class(
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_class
        mock_val = cloud_speech.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_custom_class_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_class(
            cloud_speech.UpdateCustomClassRequest(),
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeleteCustomClassRequest,
        dict,
    ],
)
def test_delete_custom_class(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        client.delete_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteCustomClassRequest()


@pytest.mark.asyncio
async def test_delete_custom_class_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.DeleteCustomClassRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_custom_class_async_from_dict():
    await test_delete_custom_class_async(request_type=dict)


def test_delete_custom_class_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeleteCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_custom_class(request)

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
async def test_delete_custom_class_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeleteCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_custom_class(request)

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


def test_delete_custom_class_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_custom_class(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_custom_class_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_custom_class(
            cloud_speech.DeleteCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_custom_class_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_custom_class(
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
async def test_delete_custom_class_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_custom_class(
            cloud_speech.DeleteCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeleteCustomClassRequest,
        dict,
    ],
)
def test_undelete_custom_class(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undelete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undelete_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        client.undelete_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteCustomClassRequest()


@pytest.mark.asyncio
async def test_undelete_custom_class_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech.UndeleteCustomClassRequest,
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undelete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undelete_custom_class_async_from_dict():
    await test_undelete_custom_class_async(request_type=dict)


def test_undelete_custom_class_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeleteCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undelete_custom_class(request)

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
async def test_undelete_custom_class_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeleteCustomClassRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undelete_custom_class(request)

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


def test_undelete_custom_class_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undelete_custom_class(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_undelete_custom_class_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_custom_class(
            cloud_speech.UndeleteCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_undelete_custom_class_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undelete_custom_class(
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
async def test_undelete_custom_class_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undelete_custom_class(
            cloud_speech.UndeleteCustomClassRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreatePhraseSetRequest,
        dict,
    ],
)
def test_create_phrase_set(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        client.create_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreatePhraseSetRequest()


@pytest.mark.asyncio
async def test_create_phrase_set_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.CreatePhraseSetRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.CreatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_phrase_set_async_from_dict():
    await test_create_phrase_set_async(request_type=dict)


def test_create_phrase_set_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreatePhraseSetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_phrase_set(request)

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
async def test_create_phrase_set_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.CreatePhraseSetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_phrase_set(request)

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


def test_create_phrase_set_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_phrase_set(
            parent="parent_value",
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_set
        mock_val = cloud_speech.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].phrase_set_id
        mock_val = "phrase_set_id_value"
        assert arg == mock_val


def test_create_phrase_set_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_phrase_set(
            cloud_speech.CreatePhraseSetRequest(),
            parent="parent_value",
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )


@pytest.mark.asyncio
async def test_create_phrase_set_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_phrase_set(
            parent="parent_value",
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_set
        mock_val = cloud_speech.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].phrase_set_id
        mock_val = "phrase_set_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_phrase_set_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_phrase_set(
            cloud_speech.CreatePhraseSetRequest(),
            parent="parent_value",
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListPhraseSetsRequest,
        dict,
    ],
)
def test_list_phrase_sets(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListPhraseSetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_phrase_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListPhraseSetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_phrase_sets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        client.list_phrase_sets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListPhraseSetsRequest()


@pytest.mark.asyncio
async def test_list_phrase_sets_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.ListPhraseSetsRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListPhraseSetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_phrase_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.ListPhraseSetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseSetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_phrase_sets_async_from_dict():
    await test_list_phrase_sets_async(request_type=dict)


def test_list_phrase_sets_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListPhraseSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        call.return_value = cloud_speech.ListPhraseSetsResponse()
        client.list_phrase_sets(request)

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
async def test_list_phrase_sets_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.ListPhraseSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListPhraseSetsResponse()
        )
        await client.list_phrase_sets(request)

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


def test_list_phrase_sets_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListPhraseSetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_phrase_sets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_phrase_sets_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_phrase_sets(
            cloud_speech.ListPhraseSetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_phrase_sets_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.ListPhraseSetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.ListPhraseSetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_phrase_sets(
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
async def test_list_phrase_sets_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_phrase_sets(
            cloud_speech.ListPhraseSetsRequest(),
            parent="parent_value",
        )


def test_list_phrase_sets_pager(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[],
                next_page_token="def",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_phrase_sets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.PhraseSet) for i in results)


def test_list_phrase_sets_pages(transport_name: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_sets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[],
                next_page_token="def",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_phrase_sets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_phrase_sets_async_pager():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_sets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[],
                next_page_token="def",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_phrase_sets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_speech.PhraseSet) for i in responses)


@pytest.mark.asyncio
async def test_list_phrase_sets_async_pages():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_sets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[],
                next_page_token="def",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_phrase_sets(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetPhraseSetRequest,
        dict,
    ],
)
def test_get_phrase_set(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.PhraseSet(
            name="name_value",
            uid="uid_value",
            boost=0.551,
            display_name="display_name_value",
            state=cloud_speech.PhraseSet.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )
        response = client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.PhraseSet)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.PhraseSet.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        client.get_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetPhraseSetRequest()


@pytest.mark.asyncio
async def test_get_phrase_set_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.GetPhraseSetRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.PhraseSet(
                name="name_value",
                uid="uid_value",
                boost=0.551,
                display_name="display_name_value",
                state=cloud_speech.PhraseSet.State.ACTIVE,
                etag="etag_value",
                reconciling=True,
                kms_key_name="kms_key_name_value",
                kms_key_version_name="kms_key_version_name_value",
            )
        )
        response = await client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.GetPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.PhraseSet)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.PhraseSet.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


@pytest.mark.asyncio
async def test_get_phrase_set_async_from_dict():
    await test_get_phrase_set_async(request_type=dict)


def test_get_phrase_set_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetPhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        call.return_value = cloud_speech.PhraseSet()
        client.get_phrase_set(request)

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
async def test_get_phrase_set_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.GetPhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.PhraseSet()
        )
        await client.get_phrase_set(request)

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


def test_get_phrase_set_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.PhraseSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_phrase_set(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_phrase_set_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_phrase_set(
            cloud_speech.GetPhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_phrase_set_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech.PhraseSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech.PhraseSet()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_phrase_set(
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
async def test_get_phrase_set_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_phrase_set(
            cloud_speech.GetPhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdatePhraseSetRequest,
        dict,
    ],
)
def test_update_phrase_set(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        client.update_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdatePhraseSetRequest()


@pytest.mark.asyncio
async def test_update_phrase_set_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UpdatePhraseSetRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UpdatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_phrase_set_async_from_dict():
    await test_update_phrase_set_async(request_type=dict)


def test_update_phrase_set_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdatePhraseSetRequest()

    request.phrase_set.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "phrase_set.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_phrase_set_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UpdatePhraseSetRequest()

    request.phrase_set.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "phrase_set.name=name_value",
    ) in kw["metadata"]


def test_update_phrase_set_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_phrase_set(
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_set
        mock_val = cloud_speech.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_phrase_set_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_phrase_set(
            cloud_speech.UpdatePhraseSetRequest(),
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_phrase_set_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_phrase_set(
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_set
        mock_val = cloud_speech.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_phrase_set_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_phrase_set(
            cloud_speech.UpdatePhraseSetRequest(),
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeletePhraseSetRequest,
        dict,
    ],
)
def test_delete_phrase_set(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        client.delete_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeletePhraseSetRequest()


@pytest.mark.asyncio
async def test_delete_phrase_set_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.DeletePhraseSetRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.DeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_phrase_set_async_from_dict():
    await test_delete_phrase_set_async(request_type=dict)


def test_delete_phrase_set_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeletePhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_phrase_set(request)

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
async def test_delete_phrase_set_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.DeletePhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_phrase_set(request)

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


def test_delete_phrase_set_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_phrase_set(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_phrase_set_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_phrase_set(
            cloud_speech.DeletePhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_phrase_set_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_phrase_set(
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
async def test_delete_phrase_set_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_phrase_set(
            cloud_speech.DeletePhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeletePhraseSetRequest,
        dict,
    ],
)
def test_undelete_phrase_set(request_type, transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undelete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undelete_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        client.undelete_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeletePhraseSetRequest()


@pytest.mark.asyncio
async def test_undelete_phrase_set_async(
    transport: str = "grpc_asyncio", request_type=cloud_speech.UndeletePhraseSetRequest
):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undelete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech.UndeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undelete_phrase_set_async_from_dict():
    await test_undelete_phrase_set_async(request_type=dict)


def test_undelete_phrase_set_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeletePhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undelete_phrase_set(request)

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
async def test_undelete_phrase_set_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech.UndeletePhraseSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undelete_phrase_set(request)

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


def test_undelete_phrase_set_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undelete_phrase_set(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_undelete_phrase_set_flattened_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_phrase_set(
            cloud_speech.UndeletePhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_undelete_phrase_set_flattened_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undelete_phrase_set(
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
async def test_undelete_phrase_set_flattened_error_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undelete_phrase_set(
            cloud_speech.UndeletePhraseSetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreateRecognizerRequest,
        dict,
    ],
)
def test_create_recognizer_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["recognizer"] = {
        "name": "name_value",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "model": "model_value",
        "language_codes": ["language_codes_value1", "language_codes_value2"],
        "default_recognition_config": {
            "auto_decoding_config": {},
            "explicit_decoding_config": {
                "encoding": 1,
                "sample_rate_hertz": 1817,
                "audio_channel_count": 2002,
            },
            "features": {
                "profanity_filter": True,
                "enable_word_time_offsets": True,
                "enable_word_confidence": True,
                "enable_automatic_punctuation": True,
                "enable_spoken_punctuation": True,
                "enable_spoken_emojis": True,
                "multi_channel_mode": 1,
                "diarization_config": {
                    "min_speaker_count": 1814,
                    "max_speaker_count": 1816,
                },
                "max_alternatives": 1719,
            },
            "adaptation": {
                "phrase_sets": [
                    {
                        "phrase_set": "phrase_set_value",
                        "inline_phrase_set": {
                            "name": "name_value",
                            "uid": "uid_value",
                            "phrases": [{"value": "value_value", "boost": 0.551}],
                            "boost": 0.551,
                            "display_name": "display_name_value",
                            "state": 2,
                            "create_time": {"seconds": 751, "nanos": 543},
                            "update_time": {},
                            "delete_time": {},
                            "expire_time": {},
                            "annotations": {},
                            "etag": "etag_value",
                            "reconciling": True,
                            "kms_key_name": "kms_key_name_value",
                            "kms_key_version_name": "kms_key_version_name_value",
                        },
                    }
                ],
                "custom_classes": [
                    {
                        "name": "name_value",
                        "uid": "uid_value",
                        "display_name": "display_name_value",
                        "items": [{"value": "value_value"}],
                        "state": 2,
                        "create_time": {},
                        "update_time": {},
                        "delete_time": {},
                        "expire_time": {},
                        "annotations": {},
                        "etag": "etag_value",
                        "reconciling": True,
                        "kms_key_name": "kms_key_name_value",
                        "kms_key_version_name": "kms_key_version_name_value",
                    }
                ],
            },
        },
        "annotations": {},
        "state": 2,
        "create_time": {},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.create_recognizer(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_recognizer_rest_required_fields(
    request_type=cloud_speech.CreateRecognizerRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).create_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_recognizer._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "recognizer_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
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

            response = client.create_recognizer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_recognizer_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_recognizer._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "recognizerId",
                "validateOnly",
            )
        )
        & set(
            (
                "recognizer",
                "parent",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_recognizer_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_create_recognizer"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_create_recognizer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.CreateRecognizerRequest.pb(
            cloud_speech.CreateRecognizerRequest()
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

        request = cloud_speech.CreateRecognizerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_recognizer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_recognizer_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.CreateRecognizerRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["recognizer"] = {
        "name": "name_value",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "model": "model_value",
        "language_codes": ["language_codes_value1", "language_codes_value2"],
        "default_recognition_config": {
            "auto_decoding_config": {},
            "explicit_decoding_config": {
                "encoding": 1,
                "sample_rate_hertz": 1817,
                "audio_channel_count": 2002,
            },
            "features": {
                "profanity_filter": True,
                "enable_word_time_offsets": True,
                "enable_word_confidence": True,
                "enable_automatic_punctuation": True,
                "enable_spoken_punctuation": True,
                "enable_spoken_emojis": True,
                "multi_channel_mode": 1,
                "diarization_config": {
                    "min_speaker_count": 1814,
                    "max_speaker_count": 1816,
                },
                "max_alternatives": 1719,
            },
            "adaptation": {
                "phrase_sets": [
                    {
                        "phrase_set": "phrase_set_value",
                        "inline_phrase_set": {
                            "name": "name_value",
                            "uid": "uid_value",
                            "phrases": [{"value": "value_value", "boost": 0.551}],
                            "boost": 0.551,
                            "display_name": "display_name_value",
                            "state": 2,
                            "create_time": {"seconds": 751, "nanos": 543},
                            "update_time": {},
                            "delete_time": {},
                            "expire_time": {},
                            "annotations": {},
                            "etag": "etag_value",
                            "reconciling": True,
                            "kms_key_name": "kms_key_name_value",
                            "kms_key_version_name": "kms_key_version_name_value",
                        },
                    }
                ],
                "custom_classes": [
                    {
                        "name": "name_value",
                        "uid": "uid_value",
                        "display_name": "display_name_value",
                        "items": [{"value": "value_value"}],
                        "state": 2,
                        "create_time": {},
                        "update_time": {},
                        "delete_time": {},
                        "expire_time": {},
                        "annotations": {},
                        "etag": "etag_value",
                        "reconciling": True,
                        "kms_key_name": "kms_key_name_value",
                        "kms_key_version_name": "kms_key_version_name_value",
                    }
                ],
            },
        },
        "annotations": {},
        "state": 2,
        "create_time": {},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.create_recognizer(request)


def test_create_recognizer_rest_flattened():
    client = SpeechClient(
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
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_recognizer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/recognizers"
            % client.transport._host,
            args[1],
        )


def test_create_recognizer_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_recognizer(
            cloud_speech.CreateRecognizerRequest(),
            parent="parent_value",
            recognizer=cloud_speech.Recognizer(name="name_value"),
            recognizer_id="recognizer_id_value",
        )


def test_create_recognizer_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListRecognizersRequest,
        dict,
    ],
)
def test_list_recognizers_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListRecognizersResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.ListRecognizersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_recognizers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecognizersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_recognizers_rest_required_fields(
    request_type=cloud_speech.ListRecognizersRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).list_recognizers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_recognizers._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "show_deleted",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.ListRecognizersResponse()
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

            pb_return_value = cloud_speech.ListRecognizersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_recognizers(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_recognizers_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_recognizers._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "showDeleted",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_recognizers_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_list_recognizers"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_list_recognizers"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.ListRecognizersRequest.pb(
            cloud_speech.ListRecognizersRequest()
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
        req.return_value._content = cloud_speech.ListRecognizersResponse.to_json(
            cloud_speech.ListRecognizersResponse()
        )

        request = cloud_speech.ListRecognizersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.ListRecognizersResponse()

        client.list_recognizers(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_recognizers_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.ListRecognizersRequest
):
    client = SpeechClient(
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
        client.list_recognizers(request)


def test_list_recognizers_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListRecognizersResponse()

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
        pb_return_value = cloud_speech.ListRecognizersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_recognizers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/recognizers"
            % client.transport._host,
            args[1],
        )


def test_list_recognizers_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_recognizers(
            cloud_speech.ListRecognizersRequest(),
            parent="parent_value",
        )


def test_list_recognizers_rest_pager(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[],
                next_page_token="def",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListRecognizersResponse(
                recognizers=[
                    cloud_speech.Recognizer(),
                    cloud_speech.Recognizer(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloud_speech.ListRecognizersResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_recognizers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.Recognizer) for i in results)

        pages = list(client.list_recognizers(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetRecognizerRequest,
        dict,
    ],
)
def test_get_recognizer_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Recognizer(
            name="name_value",
            uid="uid_value",
            display_name="display_name_value",
            model="model_value",
            language_codes=["language_codes_value"],
            state=cloud_speech.Recognizer.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Recognizer.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_recognizer(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Recognizer)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.model == "model_value"
    assert response.language_codes == ["language_codes_value"]
    assert response.state == cloud_speech.Recognizer.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_recognizer_rest_required_fields(
    request_type=cloud_speech.GetRecognizerRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).get_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.Recognizer()
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

            pb_return_value = cloud_speech.Recognizer.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_recognizer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_recognizer_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_recognizer._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_recognizer_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_get_recognizer"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_get_recognizer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.GetRecognizerRequest.pb(
            cloud_speech.GetRecognizerRequest()
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
        req.return_value._content = cloud_speech.Recognizer.to_json(
            cloud_speech.Recognizer()
        )

        request = cloud_speech.GetRecognizerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.Recognizer()

        client.get_recognizer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_recognizer_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.GetRecognizerRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
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
        client.get_recognizer(request)


def test_get_recognizer_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Recognizer()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/recognizers/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Recognizer.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_recognizer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/recognizers/*}"
            % client.transport._host,
            args[1],
        )


def test_get_recognizer_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_recognizer(
            cloud_speech.GetRecognizerRequest(),
            name="name_value",
        )


def test_get_recognizer_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateRecognizerRequest,
        dict,
    ],
)
def test_update_recognizer_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
    }
    request_init["recognizer"] = {
        "name": "projects/sample1/locations/sample2/recognizers/sample3",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "model": "model_value",
        "language_codes": ["language_codes_value1", "language_codes_value2"],
        "default_recognition_config": {
            "auto_decoding_config": {},
            "explicit_decoding_config": {
                "encoding": 1,
                "sample_rate_hertz": 1817,
                "audio_channel_count": 2002,
            },
            "features": {
                "profanity_filter": True,
                "enable_word_time_offsets": True,
                "enable_word_confidence": True,
                "enable_automatic_punctuation": True,
                "enable_spoken_punctuation": True,
                "enable_spoken_emojis": True,
                "multi_channel_mode": 1,
                "diarization_config": {
                    "min_speaker_count": 1814,
                    "max_speaker_count": 1816,
                },
                "max_alternatives": 1719,
            },
            "adaptation": {
                "phrase_sets": [
                    {
                        "phrase_set": "phrase_set_value",
                        "inline_phrase_set": {
                            "name": "name_value",
                            "uid": "uid_value",
                            "phrases": [{"value": "value_value", "boost": 0.551}],
                            "boost": 0.551,
                            "display_name": "display_name_value",
                            "state": 2,
                            "create_time": {"seconds": 751, "nanos": 543},
                            "update_time": {},
                            "delete_time": {},
                            "expire_time": {},
                            "annotations": {},
                            "etag": "etag_value",
                            "reconciling": True,
                            "kms_key_name": "kms_key_name_value",
                            "kms_key_version_name": "kms_key_version_name_value",
                        },
                    }
                ],
                "custom_classes": [
                    {
                        "name": "name_value",
                        "uid": "uid_value",
                        "display_name": "display_name_value",
                        "items": [{"value": "value_value"}],
                        "state": 2,
                        "create_time": {},
                        "update_time": {},
                        "delete_time": {},
                        "expire_time": {},
                        "annotations": {},
                        "etag": "etag_value",
                        "reconciling": True,
                        "kms_key_name": "kms_key_name_value",
                        "kms_key_version_name": "kms_key_version_name_value",
                    }
                ],
            },
        },
        "annotations": {},
        "state": 2,
        "create_time": {},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.update_recognizer(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_recognizer_rest_required_fields(
    request_type=cloud_speech.UpdateRecognizerRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).update_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_recognizer._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SpeechClient(
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

            response = client.update_recognizer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_recognizer_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_recognizer._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(("recognizer",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_recognizer_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_update_recognizer"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_update_recognizer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UpdateRecognizerRequest.pb(
            cloud_speech.UpdateRecognizerRequest()
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

        request = cloud_speech.UpdateRecognizerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_recognizer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_recognizer_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UpdateRecognizerRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
    }
    request_init["recognizer"] = {
        "name": "projects/sample1/locations/sample2/recognizers/sample3",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "model": "model_value",
        "language_codes": ["language_codes_value1", "language_codes_value2"],
        "default_recognition_config": {
            "auto_decoding_config": {},
            "explicit_decoding_config": {
                "encoding": 1,
                "sample_rate_hertz": 1817,
                "audio_channel_count": 2002,
            },
            "features": {
                "profanity_filter": True,
                "enable_word_time_offsets": True,
                "enable_word_confidence": True,
                "enable_automatic_punctuation": True,
                "enable_spoken_punctuation": True,
                "enable_spoken_emojis": True,
                "multi_channel_mode": 1,
                "diarization_config": {
                    "min_speaker_count": 1814,
                    "max_speaker_count": 1816,
                },
                "max_alternatives": 1719,
            },
            "adaptation": {
                "phrase_sets": [
                    {
                        "phrase_set": "phrase_set_value",
                        "inline_phrase_set": {
                            "name": "name_value",
                            "uid": "uid_value",
                            "phrases": [{"value": "value_value", "boost": 0.551}],
                            "boost": 0.551,
                            "display_name": "display_name_value",
                            "state": 2,
                            "create_time": {"seconds": 751, "nanos": 543},
                            "update_time": {},
                            "delete_time": {},
                            "expire_time": {},
                            "annotations": {},
                            "etag": "etag_value",
                            "reconciling": True,
                            "kms_key_name": "kms_key_name_value",
                            "kms_key_version_name": "kms_key_version_name_value",
                        },
                    }
                ],
                "custom_classes": [
                    {
                        "name": "name_value",
                        "uid": "uid_value",
                        "display_name": "display_name_value",
                        "items": [{"value": "value_value"}],
                        "state": 2,
                        "create_time": {},
                        "update_time": {},
                        "delete_time": {},
                        "expire_time": {},
                        "annotations": {},
                        "etag": "etag_value",
                        "reconciling": True,
                        "kms_key_name": "kms_key_name_value",
                        "kms_key_version_name": "kms_key_version_name_value",
                    }
                ],
            },
        },
        "annotations": {},
        "state": 2,
        "create_time": {},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.update_recognizer(request)


def test_update_recognizer_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "recognizer": {
                "name": "projects/sample1/locations/sample2/recognizers/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_recognizer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{recognizer.name=projects/*/locations/*/recognizers/*}"
            % client.transport._host,
            args[1],
        )


def test_update_recognizer_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_recognizer(
            cloud_speech.UpdateRecognizerRequest(),
            recognizer=cloud_speech.Recognizer(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_recognizer_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeleteRecognizerRequest,
        dict,
    ],
)
def test_delete_recognizer_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
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
        response = client.delete_recognizer(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_recognizer_rest_required_fields(
    request_type=cloud_speech.DeleteRecognizerRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).delete_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_recognizer._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "etag",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.delete_recognizer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_recognizer_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_recognizer._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "etag",
                "validateOnly",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_recognizer_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_delete_recognizer"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_delete_recognizer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.DeleteRecognizerRequest.pb(
            cloud_speech.DeleteRecognizerRequest()
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

        request = cloud_speech.DeleteRecognizerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_recognizer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_recognizer_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.DeleteRecognizerRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
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
        client.delete_recognizer(request)


def test_delete_recognizer_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/recognizers/sample3"
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

        client.delete_recognizer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/recognizers/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_recognizer_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_recognizer(
            cloud_speech.DeleteRecognizerRequest(),
            name="name_value",
        )


def test_delete_recognizer_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeleteRecognizerRequest,
        dict,
    ],
)
def test_undelete_recognizer_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
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
        response = client.undelete_recognizer(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_undelete_recognizer_rest_required_fields(
    request_type=cloud_speech.UndeleteRecognizerRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).undelete_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).undelete_recognizer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.undelete_recognizer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_undelete_recognizer_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.undelete_recognizer._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_undelete_recognizer_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_undelete_recognizer"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_undelete_recognizer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UndeleteRecognizerRequest.pb(
            cloud_speech.UndeleteRecognizerRequest()
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

        request = cloud_speech.UndeleteRecognizerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.undelete_recognizer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_undelete_recognizer_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UndeleteRecognizerRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/recognizers/sample3"}
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
        client.undelete_recognizer(request)


def test_undelete_recognizer_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/recognizers/sample3"
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

        client.undelete_recognizer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/recognizers/*}:undelete"
            % client.transport._host,
            args[1],
        )


def test_undelete_recognizer_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_recognizer(
            cloud_speech.UndeleteRecognizerRequest(),
            name="name_value",
        )


def test_undelete_recognizer_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.RecognizeRequest,
        dict,
    ],
)
def test_recognize_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.RecognizeResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.RecognizeResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.recognize(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.RecognizeResponse)


def test_recognize_rest_required_fields(request_type=cloud_speech.RecognizeRequest):
    transport_class = transports.SpeechRestTransport

    request_init = {}
    request_init["recognizer"] = ""
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
    ).recognize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["recognizer"] = "recognizer_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recognize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "recognizer" in jsonified_request
    assert jsonified_request["recognizer"] == "recognizer_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.RecognizeResponse()
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

            pb_return_value = cloud_speech.RecognizeResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.recognize(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_recognize_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.recognize._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("recognizer",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_recognize_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_recognize"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_recognize"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.RecognizeRequest.pb(cloud_speech.RecognizeRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloud_speech.RecognizeResponse.to_json(
            cloud_speech.RecognizeResponse()
        )

        request = cloud_speech.RecognizeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.RecognizeResponse()

        client.recognize(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_recognize_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.RecognizeRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
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
        client.recognize(request)


def test_recognize_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.RecognizeResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.RecognizeResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.recognize(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{recognizer=projects/*/locations/*/recognizers/*}:recognize"
            % client.transport._host,
            args[1],
        )


def test_recognize_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.recognize(
            cloud_speech.RecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            content=b"content_blob",
            uri="uri_value",
        )


def test_recognize_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_streaming_recognize_rest_no_http_options():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = cloud_speech.StreamingRecognizeRequest()
    requests = [request]
    with pytest.raises(RuntimeError):
        client.streaming_recognize(requests)


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.BatchRecognizeRequest,
        dict,
    ],
)
def test_batch_recognize_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
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
        response = client.batch_recognize(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_batch_recognize_rest_required_fields(
    request_type=cloud_speech.BatchRecognizeRequest,
):
    transport_class = transports.SpeechRestTransport

    request_init = {}
    request_init["recognizer"] = ""
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
    ).batch_recognize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["recognizer"] = "recognizer_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).batch_recognize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "recognizer" in jsonified_request
    assert jsonified_request["recognizer"] == "recognizer_value"

    client = SpeechClient(
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

            response = client.batch_recognize(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_batch_recognize_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.batch_recognize._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("recognizer",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_recognize_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_batch_recognize"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_batch_recognize"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.BatchRecognizeRequest.pb(
            cloud_speech.BatchRecognizeRequest()
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

        request = cloud_speech.BatchRecognizeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.batch_recognize(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_recognize_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.BatchRecognizeRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
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
        client.batch_recognize(request)


def test_batch_recognize_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "recognizer": "projects/sample1/locations/sample2/recognizers/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.batch_recognize(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{recognizer=projects/*/locations/*/recognizers/*}:batchRecognize"
            % client.transport._host,
            args[1],
        )


def test_batch_recognize_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_recognize(
            cloud_speech.BatchRecognizeRequest(),
            recognizer="recognizer_value",
            config=cloud_speech.RecognitionConfig(auto_decoding_config=None),
            config_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            files=[cloud_speech.BatchRecognizeFileMetadata(uri="uri_value")],
        )


def test_batch_recognize_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetConfigRequest,
        dict,
    ],
)
def test_get_config_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/config"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Config(
            name="name_value",
            kms_key_name="kms_key_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Config.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_get_config_rest_required_fields(request_type=cloud_speech.GetConfigRequest):
    transport_class = transports.SpeechRestTransport

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
    ).get_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.Config()
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

            pb_return_value = cloud_speech.Config.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_config_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_config_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_get_config"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_get_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.GetConfigRequest.pb(cloud_speech.GetConfigRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloud_speech.Config.to_json(cloud_speech.Config())

        request = cloud_speech.GetConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.Config()

        client.get_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_config_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.GetConfigRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/config"}
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
        client.get_config(request)


def test_get_config_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Config()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/config"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Config.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/config}" % client.transport._host,
            args[1],
        )


def test_get_config_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_config(
            cloud_speech.GetConfigRequest(),
            name="name_value",
        )


def test_get_config_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateConfigRequest,
        dict,
    ],
)
def test_update_config_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"config": {"name": "projects/sample1/locations/sample2/config"}}
    request_init["config"] = {
        "name": "projects/sample1/locations/sample2/config",
        "kms_key_name": "kms_key_name_value",
        "update_time": {"seconds": 751, "nanos": 543},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Config(
            name="name_value",
            kms_key_name="kms_key_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Config.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.Config)
    assert response.name == "name_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_update_config_rest_required_fields(
    request_type=cloud_speech.UpdateConfigRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).update_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.Config()
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

            pb_return_value = cloud_speech.Config.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_config_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("config",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_config_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_update_config"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_update_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UpdateConfigRequest.pb(
            cloud_speech.UpdateConfigRequest()
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
        req.return_value._content = cloud_speech.Config.to_json(cloud_speech.Config())

        request = cloud_speech.UpdateConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.Config()

        client.update_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_config_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UpdateConfigRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"config": {"name": "projects/sample1/locations/sample2/config"}}
    request_init["config"] = {
        "name": "projects/sample1/locations/sample2/config",
        "kms_key_name": "kms_key_name_value",
        "update_time": {"seconds": 751, "nanos": 543},
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
        client.update_config(request)


def test_update_config_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.Config()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "config": {"name": "projects/sample1/locations/sample2/config"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.Config.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{config.name=projects/*/locations/*/config}"
            % client.transport._host,
            args[1],
        )


def test_update_config_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_config(
            cloud_speech.UpdateConfigRequest(),
            config=cloud_speech.Config(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_config_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreateCustomClassRequest,
        dict,
    ],
)
def test_create_custom_class_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["custom_class"] = {
        "name": "name_value",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "items": [{"value": "value_value"}],
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.create_custom_class(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_custom_class_rest_required_fields(
    request_type=cloud_speech.CreateCustomClassRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).create_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_custom_class._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "custom_class_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
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

            response = client.create_custom_class(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_custom_class_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_custom_class._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "customClassId",
                "validateOnly",
            )
        )
        & set(
            (
                "customClass",
                "parent",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_custom_class_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_create_custom_class"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_create_custom_class"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.CreateCustomClassRequest.pb(
            cloud_speech.CreateCustomClassRequest()
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

        request = cloud_speech.CreateCustomClassRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_custom_class(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_custom_class_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.CreateCustomClassRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["custom_class"] = {
        "name": "name_value",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "items": [{"value": "value_value"}],
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.create_custom_class(request)


def test_create_custom_class_rest_flattened():
    client = SpeechClient(
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
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_custom_class(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/customClasses"
            % client.transport._host,
            args[1],
        )


def test_create_custom_class_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_class(
            cloud_speech.CreateCustomClassRequest(),
            parent="parent_value",
            custom_class=cloud_speech.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )


def test_create_custom_class_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListCustomClassesRequest,
        dict,
    ],
)
def test_list_custom_classes_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListCustomClassesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.ListCustomClassesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_custom_classes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomClassesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_classes_rest_required_fields(
    request_type=cloud_speech.ListCustomClassesRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).list_custom_classes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_custom_classes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "show_deleted",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.ListCustomClassesResponse()
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

            pb_return_value = cloud_speech.ListCustomClassesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_custom_classes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_custom_classes_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_custom_classes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "showDeleted",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_custom_classes_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_list_custom_classes"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_list_custom_classes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.ListCustomClassesRequest.pb(
            cloud_speech.ListCustomClassesRequest()
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
        req.return_value._content = cloud_speech.ListCustomClassesResponse.to_json(
            cloud_speech.ListCustomClassesResponse()
        )

        request = cloud_speech.ListCustomClassesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.ListCustomClassesResponse()

        client.list_custom_classes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_custom_classes_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.ListCustomClassesRequest
):
    client = SpeechClient(
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
        client.list_custom_classes(request)


def test_list_custom_classes_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListCustomClassesResponse()

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
        pb_return_value = cloud_speech.ListCustomClassesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_custom_classes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/customClasses"
            % client.transport._host,
            args[1],
        )


def test_list_custom_classes_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_classes(
            cloud_speech.ListCustomClassesRequest(),
            parent="parent_value",
        )


def test_list_custom_classes_rest_pager(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[],
                next_page_token="def",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListCustomClassesResponse(
                custom_classes=[
                    cloud_speech.CustomClass(),
                    cloud_speech.CustomClass(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloud_speech.ListCustomClassesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_custom_classes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.CustomClass) for i in results)

        pages = list(client.list_custom_classes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetCustomClassRequest,
        dict,
    ],
)
def test_get_custom_class_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.CustomClass(
            name="name_value",
            uid="uid_value",
            display_name="display_name_value",
            state=cloud_speech.CustomClass.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.CustomClass.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_custom_class(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.CustomClass)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.CustomClass.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_custom_class_rest_required_fields(
    request_type=cloud_speech.GetCustomClassRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).get_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.CustomClass()
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

            pb_return_value = cloud_speech.CustomClass.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_custom_class(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_custom_class_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_custom_class._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_custom_class_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_get_custom_class"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_get_custom_class"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.GetCustomClassRequest.pb(
            cloud_speech.GetCustomClassRequest()
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
        req.return_value._content = cloud_speech.CustomClass.to_json(
            cloud_speech.CustomClass()
        )

        request = cloud_speech.GetCustomClassRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.CustomClass()

        client.get_custom_class(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_custom_class_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.GetCustomClassRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
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
        client.get_custom_class(request)


def test_get_custom_class_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.CustomClass()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/customClasses/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.CustomClass.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_custom_class(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/customClasses/*}"
            % client.transport._host,
            args[1],
        )


def test_get_custom_class_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_class(
            cloud_speech.GetCustomClassRequest(),
            name="name_value",
        )


def test_get_custom_class_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdateCustomClassRequest,
        dict,
    ],
)
def test_update_custom_class_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "custom_class": {
            "name": "projects/sample1/locations/sample2/customClasses/sample3"
        }
    }
    request_init["custom_class"] = {
        "name": "projects/sample1/locations/sample2/customClasses/sample3",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "items": [{"value": "value_value"}],
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.update_custom_class(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_custom_class_rest_required_fields(
    request_type=cloud_speech.UpdateCustomClassRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).update_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_custom_class._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SpeechClient(
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

            response = client.update_custom_class(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_custom_class_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_custom_class._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(("customClass",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_custom_class_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_update_custom_class"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_update_custom_class"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UpdateCustomClassRequest.pb(
            cloud_speech.UpdateCustomClassRequest()
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

        request = cloud_speech.UpdateCustomClassRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_custom_class(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_custom_class_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UpdateCustomClassRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "custom_class": {
            "name": "projects/sample1/locations/sample2/customClasses/sample3"
        }
    }
    request_init["custom_class"] = {
        "name": "projects/sample1/locations/sample2/customClasses/sample3",
        "uid": "uid_value",
        "display_name": "display_name_value",
        "items": [{"value": "value_value"}],
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.update_custom_class(request)


def test_update_custom_class_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "custom_class": {
                "name": "projects/sample1/locations/sample2/customClasses/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_custom_class(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{custom_class.name=projects/*/locations/*/customClasses/*}"
            % client.transport._host,
            args[1],
        )


def test_update_custom_class_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_class(
            cloud_speech.UpdateCustomClassRequest(),
            custom_class=cloud_speech.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_custom_class_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeleteCustomClassRequest,
        dict,
    ],
)
def test_delete_custom_class_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
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
        response = client.delete_custom_class(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_custom_class_rest_required_fields(
    request_type=cloud_speech.DeleteCustomClassRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).delete_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_custom_class._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "etag",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.delete_custom_class(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_custom_class_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_custom_class._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "etag",
                "validateOnly",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_custom_class_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_delete_custom_class"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_delete_custom_class"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.DeleteCustomClassRequest.pb(
            cloud_speech.DeleteCustomClassRequest()
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

        request = cloud_speech.DeleteCustomClassRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_custom_class(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_custom_class_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.DeleteCustomClassRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
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
        client.delete_custom_class(request)


def test_delete_custom_class_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/customClasses/sample3"
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

        client.delete_custom_class(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/customClasses/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_custom_class_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_custom_class(
            cloud_speech.DeleteCustomClassRequest(),
            name="name_value",
        )


def test_delete_custom_class_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeleteCustomClassRequest,
        dict,
    ],
)
def test_undelete_custom_class_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
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
        response = client.undelete_custom_class(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_undelete_custom_class_rest_required_fields(
    request_type=cloud_speech.UndeleteCustomClassRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).undelete_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).undelete_custom_class._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.undelete_custom_class(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_undelete_custom_class_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.undelete_custom_class._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_undelete_custom_class_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_undelete_custom_class"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_undelete_custom_class"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UndeleteCustomClassRequest.pb(
            cloud_speech.UndeleteCustomClassRequest()
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

        request = cloud_speech.UndeleteCustomClassRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.undelete_custom_class(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_undelete_custom_class_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UndeleteCustomClassRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/customClasses/sample3"}
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
        client.undelete_custom_class(request)


def test_undelete_custom_class_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/customClasses/sample3"
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

        client.undelete_custom_class(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/customClasses/*}:undelete"
            % client.transport._host,
            args[1],
        )


def test_undelete_custom_class_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_custom_class(
            cloud_speech.UndeleteCustomClassRequest(),
            name="name_value",
        )


def test_undelete_custom_class_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.CreatePhraseSetRequest,
        dict,
    ],
)
def test_create_phrase_set_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["phrase_set"] = {
        "name": "name_value",
        "uid": "uid_value",
        "phrases": [{"value": "value_value", "boost": 0.551}],
        "boost": 0.551,
        "display_name": "display_name_value",
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.create_phrase_set(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_phrase_set_rest_required_fields(
    request_type=cloud_speech.CreatePhraseSetRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).create_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_phrase_set._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "phrase_set_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
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

            response = client.create_phrase_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_phrase_set_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_phrase_set._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "phraseSetId",
                "validateOnly",
            )
        )
        & set(
            (
                "phraseSet",
                "parent",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_phrase_set_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_create_phrase_set"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_create_phrase_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.CreatePhraseSetRequest.pb(
            cloud_speech.CreatePhraseSetRequest()
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

        request = cloud_speech.CreatePhraseSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_phrase_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_phrase_set_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.CreatePhraseSetRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["phrase_set"] = {
        "name": "name_value",
        "uid": "uid_value",
        "phrases": [{"value": "value_value", "boost": 0.551}],
        "boost": 0.551,
        "display_name": "display_name_value",
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.create_phrase_set(request)


def test_create_phrase_set_rest_flattened():
    client = SpeechClient(
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
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_phrase_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/phraseSets" % client.transport._host,
            args[1],
        )


def test_create_phrase_set_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_phrase_set(
            cloud_speech.CreatePhraseSetRequest(),
            parent="parent_value",
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )


def test_create_phrase_set_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.ListPhraseSetsRequest,
        dict,
    ],
)
def test_list_phrase_sets_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListPhraseSetsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.ListPhraseSetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_phrase_sets(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_phrase_sets_rest_required_fields(
    request_type=cloud_speech.ListPhraseSetsRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).list_phrase_sets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_phrase_sets._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "show_deleted",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.ListPhraseSetsResponse()
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

            pb_return_value = cloud_speech.ListPhraseSetsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_phrase_sets(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_phrase_sets_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_phrase_sets._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "showDeleted",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_phrase_sets_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_list_phrase_sets"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_list_phrase_sets"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.ListPhraseSetsRequest.pb(
            cloud_speech.ListPhraseSetsRequest()
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
        req.return_value._content = cloud_speech.ListPhraseSetsResponse.to_json(
            cloud_speech.ListPhraseSetsResponse()
        )

        request = cloud_speech.ListPhraseSetsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.ListPhraseSetsResponse()

        client.list_phrase_sets(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_phrase_sets_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.ListPhraseSetsRequest
):
    client = SpeechClient(
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
        client.list_phrase_sets(request)


def test_list_phrase_sets_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.ListPhraseSetsResponse()

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
        pb_return_value = cloud_speech.ListPhraseSetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_phrase_sets(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/phraseSets" % client.transport._host,
            args[1],
        )


def test_list_phrase_sets_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_phrase_sets(
            cloud_speech.ListPhraseSetsRequest(),
            parent="parent_value",
        )


def test_list_phrase_sets_rest_pager(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[],
                next_page_token="def",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                ],
                next_page_token="ghi",
            ),
            cloud_speech.ListPhraseSetsResponse(
                phrase_sets=[
                    cloud_speech.PhraseSet(),
                    cloud_speech.PhraseSet(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloud_speech.ListPhraseSetsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_phrase_sets(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_speech.PhraseSet) for i in results)

        pages = list(client.list_phrase_sets(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.GetPhraseSetRequest,
        dict,
    ],
)
def test_get_phrase_set_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.PhraseSet(
            name="name_value",
            uid="uid_value",
            boost=0.551,
            display_name="display_name_value",
            state=cloud_speech.PhraseSet.State.ACTIVE,
            etag="etag_value",
            reconciling=True,
            kms_key_name="kms_key_name_value",
            kms_key_version_name="kms_key_version_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.PhraseSet.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_phrase_set(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_speech.PhraseSet)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)
    assert response.display_name == "display_name_value"
    assert response.state == cloud_speech.PhraseSet.State.ACTIVE
    assert response.etag == "etag_value"
    assert response.reconciling is True
    assert response.kms_key_name == "kms_key_name_value"
    assert response.kms_key_version_name == "kms_key_version_name_value"


def test_get_phrase_set_rest_required_fields(
    request_type=cloud_speech.GetPhraseSetRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).get_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloud_speech.PhraseSet()
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

            pb_return_value = cloud_speech.PhraseSet.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_phrase_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_phrase_set_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_phrase_set._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_phrase_set_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SpeechRestInterceptor, "post_get_phrase_set"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_get_phrase_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.GetPhraseSetRequest.pb(
            cloud_speech.GetPhraseSetRequest()
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
        req.return_value._content = cloud_speech.PhraseSet.to_json(
            cloud_speech.PhraseSet()
        )

        request = cloud_speech.GetPhraseSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloud_speech.PhraseSet()

        client.get_phrase_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_phrase_set_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.GetPhraseSetRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
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
        client.get_phrase_set(request)


def test_get_phrase_set_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloud_speech.PhraseSet()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/phraseSets/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cloud_speech.PhraseSet.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_phrase_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/phraseSets/*}" % client.transport._host,
            args[1],
        )


def test_get_phrase_set_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_phrase_set(
            cloud_speech.GetPhraseSetRequest(),
            name="name_value",
        )


def test_get_phrase_set_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UpdatePhraseSetRequest,
        dict,
    ],
)
def test_update_phrase_set_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "phrase_set": {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
    }
    request_init["phrase_set"] = {
        "name": "projects/sample1/locations/sample2/phraseSets/sample3",
        "uid": "uid_value",
        "phrases": [{"value": "value_value", "boost": 0.551}],
        "boost": 0.551,
        "display_name": "display_name_value",
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        response = client.update_phrase_set(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_phrase_set_rest_required_fields(
    request_type=cloud_speech.UpdatePhraseSetRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).update_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_phrase_set._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = SpeechClient(
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

            response = client.update_phrase_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_phrase_set_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_phrase_set._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(("phraseSet",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_phrase_set_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_update_phrase_set"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_update_phrase_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UpdatePhraseSetRequest.pb(
            cloud_speech.UpdatePhraseSetRequest()
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

        request = cloud_speech.UpdatePhraseSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_phrase_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_phrase_set_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UpdatePhraseSetRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "phrase_set": {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
    }
    request_init["phrase_set"] = {
        "name": "projects/sample1/locations/sample2/phraseSets/sample3",
        "uid": "uid_value",
        "phrases": [{"value": "value_value", "boost": 0.551}],
        "boost": 0.551,
        "display_name": "display_name_value",
        "state": 2,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "annotations": {},
        "etag": "etag_value",
        "reconciling": True,
        "kms_key_name": "kms_key_name_value",
        "kms_key_version_name": "kms_key_version_name_value",
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
        client.update_phrase_set(request)


def test_update_phrase_set_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "phrase_set": {
                "name": "projects/sample1/locations/sample2/phraseSets/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_phrase_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{phrase_set.name=projects/*/locations/*/phraseSets/*}"
            % client.transport._host,
            args[1],
        )


def test_update_phrase_set_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_phrase_set(
            cloud_speech.UpdatePhraseSetRequest(),
            phrase_set=cloud_speech.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_phrase_set_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.DeletePhraseSetRequest,
        dict,
    ],
)
def test_delete_phrase_set_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
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
        response = client.delete_phrase_set(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_phrase_set_rest_required_fields(
    request_type=cloud_speech.DeletePhraseSetRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).delete_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_phrase_set._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "etag",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.delete_phrase_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_phrase_set_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_phrase_set._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "etag",
                "validateOnly",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_phrase_set_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_delete_phrase_set"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_delete_phrase_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.DeletePhraseSetRequest.pb(
            cloud_speech.DeletePhraseSetRequest()
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

        request = cloud_speech.DeletePhraseSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_phrase_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_phrase_set_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.DeletePhraseSetRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
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
        client.delete_phrase_set(request)


def test_delete_phrase_set_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/phraseSets/sample3"
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

        client.delete_phrase_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/phraseSets/*}" % client.transport._host,
            args[1],
        )


def test_delete_phrase_set_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_phrase_set(
            cloud_speech.DeletePhraseSetRequest(),
            name="name_value",
        )


def test_delete_phrase_set_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_speech.UndeletePhraseSetRequest,
        dict,
    ],
)
def test_undelete_phrase_set_rest(request_type):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
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
        response = client.undelete_phrase_set(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_undelete_phrase_set_rest_required_fields(
    request_type=cloud_speech.UndeletePhraseSetRequest,
):
    transport_class = transports.SpeechRestTransport

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
    ).undelete_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).undelete_phrase_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SpeechClient(
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

            response = client.undelete_phrase_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_undelete_phrase_set_rest_unset_required_fields():
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.undelete_phrase_set._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_undelete_phrase_set_rest_interceptors(null_interceptor):
    transport = transports.SpeechRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.SpeechRestInterceptor(),
    )
    client = SpeechClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.SpeechRestInterceptor, "post_undelete_phrase_set"
    ) as post, mock.patch.object(
        transports.SpeechRestInterceptor, "pre_undelete_phrase_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloud_speech.UndeletePhraseSetRequest.pb(
            cloud_speech.UndeletePhraseSetRequest()
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

        request = cloud_speech.UndeletePhraseSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.undelete_phrase_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_undelete_phrase_set_rest_bad_request(
    transport: str = "rest", request_type=cloud_speech.UndeletePhraseSetRequest
):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/phraseSets/sample3"}
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
        client.undelete_phrase_set(request)


def test_undelete_phrase_set_rest_flattened():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/phraseSets/sample3"
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

        client.undelete_phrase_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/phraseSets/*}:undelete"
            % client.transport._host,
            args[1],
        )


def test_undelete_phrase_set_rest_flattened_error(transport: str = "rest"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_phrase_set(
            cloud_speech.UndeletePhraseSetRequest(),
            name="name_value",
        )


def test_undelete_phrase_set_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_streaming_recognize_rest_error():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # Since a `google.api.http` annotation is required for using a rest transport
    # method, this should error.
    with pytest.raises(NotImplementedError) as not_implemented_error:
        client.streaming_recognize({})
    assert "Method StreamingRecognize is not available over REST transport" in str(
        not_implemented_error.value
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpeechClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpeechClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SpeechClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SpeechClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SpeechClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = SpeechClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SpeechGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SpeechGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SpeechGrpcTransport,
        transports.SpeechGrpcAsyncIOTransport,
        transports.SpeechRestTransport,
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
    transport = SpeechClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.SpeechGrpcTransport,
    )


def test_speech_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.SpeechTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_speech_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.speech_v2.services.speech.transports.SpeechTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SpeechTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_recognizer",
        "list_recognizers",
        "get_recognizer",
        "update_recognizer",
        "delete_recognizer",
        "undelete_recognizer",
        "recognize",
        "streaming_recognize",
        "batch_recognize",
        "get_config",
        "update_config",
        "create_custom_class",
        "list_custom_classes",
        "get_custom_class",
        "update_custom_class",
        "delete_custom_class",
        "undelete_custom_class",
        "create_phrase_set",
        "list_phrase_sets",
        "get_phrase_set",
        "update_phrase_set",
        "delete_phrase_set",
        "undelete_phrase_set",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
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


def test_speech_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.speech_v2.services.speech.transports.SpeechTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SpeechTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_speech_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.speech_v2.services.speech.transports.SpeechTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SpeechTransport()
        adc.assert_called_once()


def test_speech_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SpeechClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SpeechGrpcTransport,
        transports.SpeechGrpcAsyncIOTransport,
    ],
)
def test_speech_transport_auth_adc(transport_class):
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
        transports.SpeechGrpcTransport,
        transports.SpeechGrpcAsyncIOTransport,
        transports.SpeechRestTransport,
    ],
)
def test_speech_transport_auth_gdch_credentials(transport_class):
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
        (transports.SpeechGrpcTransport, grpc_helpers),
        (transports.SpeechGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_speech_transport_create_channel(transport_class, grpc_helpers):
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
            "speech.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="speech.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.SpeechGrpcTransport, transports.SpeechGrpcAsyncIOTransport],
)
def test_speech_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_speech_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.SpeechRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_speech_rest_lro_client():
    client = SpeechClient(
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
def test_speech_host_no_port(transport_name):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="speech.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "speech.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://speech.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_speech_host_with_port(transport_name):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="speech.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "speech.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://speech.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_speech_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = SpeechClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = SpeechClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_recognizer._session
    session2 = client2.transport.create_recognizer._session
    assert session1 != session2
    session1 = client1.transport.list_recognizers._session
    session2 = client2.transport.list_recognizers._session
    assert session1 != session2
    session1 = client1.transport.get_recognizer._session
    session2 = client2.transport.get_recognizer._session
    assert session1 != session2
    session1 = client1.transport.update_recognizer._session
    session2 = client2.transport.update_recognizer._session
    assert session1 != session2
    session1 = client1.transport.delete_recognizer._session
    session2 = client2.transport.delete_recognizer._session
    assert session1 != session2
    session1 = client1.transport.undelete_recognizer._session
    session2 = client2.transport.undelete_recognizer._session
    assert session1 != session2
    session1 = client1.transport.recognize._session
    session2 = client2.transport.recognize._session
    assert session1 != session2
    session1 = client1.transport.streaming_recognize._session
    session2 = client2.transport.streaming_recognize._session
    assert session1 != session2
    session1 = client1.transport.batch_recognize._session
    session2 = client2.transport.batch_recognize._session
    assert session1 != session2
    session1 = client1.transport.get_config._session
    session2 = client2.transport.get_config._session
    assert session1 != session2
    session1 = client1.transport.update_config._session
    session2 = client2.transport.update_config._session
    assert session1 != session2
    session1 = client1.transport.create_custom_class._session
    session2 = client2.transport.create_custom_class._session
    assert session1 != session2
    session1 = client1.transport.list_custom_classes._session
    session2 = client2.transport.list_custom_classes._session
    assert session1 != session2
    session1 = client1.transport.get_custom_class._session
    session2 = client2.transport.get_custom_class._session
    assert session1 != session2
    session1 = client1.transport.update_custom_class._session
    session2 = client2.transport.update_custom_class._session
    assert session1 != session2
    session1 = client1.transport.delete_custom_class._session
    session2 = client2.transport.delete_custom_class._session
    assert session1 != session2
    session1 = client1.transport.undelete_custom_class._session
    session2 = client2.transport.undelete_custom_class._session
    assert session1 != session2
    session1 = client1.transport.create_phrase_set._session
    session2 = client2.transport.create_phrase_set._session
    assert session1 != session2
    session1 = client1.transport.list_phrase_sets._session
    session2 = client2.transport.list_phrase_sets._session
    assert session1 != session2
    session1 = client1.transport.get_phrase_set._session
    session2 = client2.transport.get_phrase_set._session
    assert session1 != session2
    session1 = client1.transport.update_phrase_set._session
    session2 = client2.transport.update_phrase_set._session
    assert session1 != session2
    session1 = client1.transport.delete_phrase_set._session
    session2 = client2.transport.delete_phrase_set._session
    assert session1 != session2
    session1 = client1.transport.undelete_phrase_set._session
    session2 = client2.transport.undelete_phrase_set._session
    assert session1 != session2


def test_speech_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SpeechGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_speech_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SpeechGrpcAsyncIOTransport(
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
    [transports.SpeechGrpcTransport, transports.SpeechGrpcAsyncIOTransport],
)
def test_speech_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.SpeechGrpcTransport, transports.SpeechGrpcAsyncIOTransport],
)
def test_speech_transport_channel_mtls_with_adc(transport_class):
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


def test_speech_grpc_lro_client():
    client = SpeechClient(
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


def test_speech_grpc_lro_async_client():
    client = SpeechAsyncClient(
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


def test_config_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}/config".format(
        project=project,
        location=location,
    )
    actual = SpeechClient.config_path(project, location)
    assert expected == actual


def test_parse_config_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = SpeechClient.config_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_config_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "oyster"
    location = "nudibranch"
    key_ring = "cuttlefish"
    crypto_key = "mussel"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
    )
    actual = SpeechClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "key_ring": "scallop",
        "crypto_key": "abalone",
    }
    path = SpeechClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_crypto_key_path(path)
    assert expected == actual


def test_crypto_key_version_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    crypto_key = "octopus"
    crypto_key_version = "oyster"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
    )
    actual = SpeechClient.crypto_key_version_path(
        project, location, key_ring, crypto_key, crypto_key_version
    )
    assert expected == actual


def test_parse_crypto_key_version_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "key_ring": "mussel",
        "crypto_key": "winkle",
        "crypto_key_version": "nautilus",
    }
    path = SpeechClient.crypto_key_version_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_crypto_key_version_path(path)
    assert expected == actual


def test_custom_class_path():
    project = "scallop"
    location = "abalone"
    custom_class = "squid"
    expected = (
        "projects/{project}/locations/{location}/customClasses/{custom_class}".format(
            project=project,
            location=location,
            custom_class=custom_class,
        )
    )
    actual = SpeechClient.custom_class_path(project, location, custom_class)
    assert expected == actual


def test_parse_custom_class_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "custom_class": "octopus",
    }
    path = SpeechClient.custom_class_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_custom_class_path(path)
    assert expected == actual


def test_phrase_set_path():
    project = "oyster"
    location = "nudibranch"
    phrase_set = "cuttlefish"
    expected = "projects/{project}/locations/{location}/phraseSets/{phrase_set}".format(
        project=project,
        location=location,
        phrase_set=phrase_set,
    )
    actual = SpeechClient.phrase_set_path(project, location, phrase_set)
    assert expected == actual


def test_parse_phrase_set_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "phrase_set": "nautilus",
    }
    path = SpeechClient.phrase_set_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_phrase_set_path(path)
    assert expected == actual


def test_recognizer_path():
    project = "scallop"
    location = "abalone"
    recognizer = "squid"
    expected = (
        "projects/{project}/locations/{location}/recognizers/{recognizer}".format(
            project=project,
            location=location,
            recognizer=recognizer,
        )
    )
    actual = SpeechClient.recognizer_path(project, location, recognizer)
    assert expected == actual


def test_parse_recognizer_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "recognizer": "octopus",
    }
    path = SpeechClient.recognizer_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_recognizer_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SpeechClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = SpeechClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = SpeechClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = SpeechClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = SpeechClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = SpeechClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = SpeechClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = SpeechClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = SpeechClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = SpeechClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SpeechClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SpeechTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SpeechClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SpeechTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SpeechClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = SpeechClient(
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
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = SpeechClient(
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

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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


def test_cancel_operation(transport: str = "grpc"):
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
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
async def test_cancel_operation_field_headers_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
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


def test_cancel_operation_from_dict():
    client = SpeechClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = SpeechAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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


def test_list_locations(transport: str = "grpc"):
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
    client = SpeechClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = SpeechAsyncClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = SpeechClient(
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
    client = SpeechAsyncClient(
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
        client = SpeechClient(
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
        client = SpeechClient(
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
        (SpeechClient, transports.SpeechGrpcTransport),
        (SpeechAsyncClient, transports.SpeechGrpcAsyncIOTransport),
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
