# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api import monitored_resource_pb2 as monitored_resource  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.logging_v2.services.logging_service_v2 import (
    LoggingServiceV2AsyncClient,
)
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.services.logging_service_v2 import pagers
from google.cloud.logging_v2.services.logging_service_v2 import transports
from google.cloud.logging_v2.types import log_entry
from google.cloud.logging_v2.types import logging
from google.logging.type import http_request_pb2 as http_request  # type: ignore
from google.logging.type import log_severity_pb2 as log_severity  # type: ignore
from google.oauth2 import service_account
from google.protobuf import any_pb2 as gp_any  # type: ignore
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


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

    assert LoggingServiceV2Client._get_default_mtls_endpoint(None) is None
    assert (
        LoggingServiceV2Client._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        LoggingServiceV2Client._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        LoggingServiceV2Client._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        LoggingServiceV2Client._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        LoggingServiceV2Client._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [LoggingServiceV2Client, LoggingServiceV2AsyncClient]
)
def test_logging_service_v2_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "logging.googleapis.com:443"


def test_logging_service_v2_client_get_transport_class():
    transport = LoggingServiceV2Client.get_transport_class()
    assert transport == transports.LoggingServiceV2GrpcTransport

    transport = LoggingServiceV2Client.get_transport_class("grpc")
    assert transport == transports.LoggingServiceV2GrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc"),
        (
            LoggingServiceV2AsyncClient,
            transports.LoggingServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    LoggingServiceV2Client,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LoggingServiceV2Client),
)
@mock.patch.object(
    LoggingServiceV2AsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LoggingServiceV2AsyncClient),
)
def test_logging_service_v2_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(LoggingServiceV2Client, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(LoggingServiceV2Client, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            LoggingServiceV2Client,
            transports.LoggingServiceV2GrpcTransport,
            "grpc",
            "true",
        ),
        (
            LoggingServiceV2AsyncClient,
            transports.LoggingServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            LoggingServiceV2Client,
            transports.LoggingServiceV2GrpcTransport,
            "grpc",
            "false",
        ),
        (
            LoggingServiceV2AsyncClient,
            transports.LoggingServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    LoggingServiceV2Client,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LoggingServiceV2Client),
)
@mock.patch.object(
    LoggingServiceV2AsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LoggingServiceV2AsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_logging_service_v2_client_mtls_env_auto(
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
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc"),
        (
            LoggingServiceV2AsyncClient,
            transports.LoggingServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_logging_service_v2_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LoggingServiceV2Client, transports.LoggingServiceV2GrpcTransport, "grpc"),
        (
            LoggingServiceV2AsyncClient,
            transports.LoggingServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_logging_service_v2_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_logging_service_v2_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2GrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = LoggingServiceV2Client(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_delete_log(transport: str = "grpc", request_type=logging.DeleteLogRequest):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.DeleteLogRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_log_from_dict():
    test_delete_log(request_type=dict)


@pytest.mark.asyncio
async def test_delete_log_async(
    transport: str = "grpc_asyncio", request_type=logging.DeleteLogRequest
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.DeleteLogRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_log_async_from_dict():
    await test_delete_log_async(request_type=dict)


def test_delete_log_field_headers():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.DeleteLogRequest()
    request.log_name = "log_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        call.return_value = None

        client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "log_name=log_name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_log_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.DeleteLogRequest()
    request.log_name = "log_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_log(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "log_name=log_name/value",) in kw["metadata"]


def test_delete_log_flattened():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_log(log_name="log_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].log_name == "log_name_value"


def test_delete_log_flattened_error():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_log(
            logging.DeleteLogRequest(), log_name="log_name_value",
        )


@pytest.mark.asyncio
async def test_delete_log_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_log), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_log(log_name="log_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].log_name == "log_name_value"


@pytest.mark.asyncio
async def test_delete_log_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_log(
            logging.DeleteLogRequest(), log_name="log_name_value",
        )


def test_write_log_entries(
    transport: str = "grpc", request_type=logging.WriteLogEntriesRequest
):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_log_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse()

        response = client.write_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.WriteLogEntriesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, logging.WriteLogEntriesResponse)


def test_write_log_entries_from_dict():
    test_write_log_entries(request_type=dict)


@pytest.mark.asyncio
async def test_write_log_entries_async(
    transport: str = "grpc_asyncio", request_type=logging.WriteLogEntriesRequest
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_log_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.WriteLogEntriesResponse()
        )

        response = await client.write_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.WriteLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging.WriteLogEntriesResponse)


@pytest.mark.asyncio
async def test_write_log_entries_async_from_dict():
    await test_write_log_entries_async(request_type=dict)


def test_write_log_entries_flattened():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_log_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.write_log_entries(
            log_name="log_name_value",
            resource=monitored_resource.MonitoredResource(type="type__value"),
            labels={"key_value": "value_value"},
            entries=[log_entry.LogEntry(log_name="log_name_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].log_name == "log_name_value"

        assert args[0].resource == monitored_resource.MonitoredResource(
            type="type__value"
        )

        assert args[0].labels == {"key_value": "value_value"}

        assert args[0].entries == [log_entry.LogEntry(log_name="log_name_value")]


def test_write_log_entries_flattened_error():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.write_log_entries(
            logging.WriteLogEntriesRequest(),
            log_name="log_name_value",
            resource=monitored_resource.MonitoredResource(type="type__value"),
            labels={"key_value": "value_value"},
            entries=[log_entry.LogEntry(log_name="log_name_value")],
        )


@pytest.mark.asyncio
async def test_write_log_entries_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.write_log_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.WriteLogEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.WriteLogEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.write_log_entries(
            log_name="log_name_value",
            resource=monitored_resource.MonitoredResource(type="type__value"),
            labels={"key_value": "value_value"},
            entries=[log_entry.LogEntry(log_name="log_name_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].log_name == "log_name_value"

        assert args[0].resource == monitored_resource.MonitoredResource(
            type="type__value"
        )

        assert args[0].labels == {"key_value": "value_value"}

        assert args[0].entries == [log_entry.LogEntry(log_name="log_name_value")]


@pytest.mark.asyncio
async def test_write_log_entries_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.write_log_entries(
            logging.WriteLogEntriesRequest(),
            log_name="log_name_value",
            resource=monitored_resource.MonitoredResource(type="type__value"),
            labels={"key_value": "value_value"},
            entries=[log_entry.LogEntry(log_name="log_name_value")],
        )


def test_list_log_entries(
    transport: str = "grpc", request_type=logging.ListLogEntriesRequest
):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListLogEntriesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListLogEntriesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_log_entries_from_dict():
    test_list_log_entries(request_type=dict)


@pytest.mark.asyncio
async def test_list_log_entries_async(
    transport: str = "grpc_asyncio", request_type=logging.ListLogEntriesRequest
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListLogEntriesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_log_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListLogEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogEntriesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_log_entries_async_from_dict():
    await test_list_log_entries_async(request_type=dict)


def test_list_log_entries_flattened():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_log_entries(
            resource_names=["resource_names_value"],
            filter="filter_value",
            order_by="order_by_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource_names == ["resource_names_value"]

        assert args[0].filter == "filter_value"

        assert args[0].order_by == "order_by_value"


def test_list_log_entries_flattened_error():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_log_entries(
            logging.ListLogEntriesRequest(),
            resource_names=["resource_names_value"],
            filter="filter_value",
            order_by="order_by_value",
        )


@pytest.mark.asyncio
async def test_list_log_entries_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListLogEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_log_entries(
            resource_names=["resource_names_value"],
            filter="filter_value",
            order_by="order_by_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource_names == ["resource_names_value"]

        assert args[0].filter == "filter_value"

        assert args[0].order_by == "order_by_value"


@pytest.mark.asyncio
async def test_list_log_entries_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_log_entries(
            logging.ListLogEntriesRequest(),
            resource_names=["resource_names_value"],
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_log_entries_pager():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token="abc",
            ),
            logging.ListLogEntriesResponse(entries=[], next_page_token="def",),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(),], next_page_token="ghi",
            ),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(), log_entry.LogEntry(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_log_entries(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, log_entry.LogEntry) for i in results)


def test_list_log_entries_pages():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token="abc",
            ),
            logging.ListLogEntriesResponse(entries=[], next_page_token="def",),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(),], next_page_token="ghi",
            ),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(), log_entry.LogEntry(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_log_entries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_log_entries_async_pager():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_log_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token="abc",
            ),
            logging.ListLogEntriesResponse(entries=[], next_page_token="def",),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(),], next_page_token="ghi",
            ),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(), log_entry.LogEntry(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_log_entries(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, log_entry.LogEntry) for i in responses)


@pytest.mark.asyncio
async def test_list_log_entries_async_pages():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_log_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogEntriesResponse(
                entries=[
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                    log_entry.LogEntry(),
                ],
                next_page_token="abc",
            ),
            logging.ListLogEntriesResponse(entries=[], next_page_token="def",),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(),], next_page_token="ghi",
            ),
            logging.ListLogEntriesResponse(
                entries=[log_entry.LogEntry(), log_entry.LogEntry(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_log_entries(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_monitored_resource_descriptors(
    transport: str = "grpc",
    request_type=logging.ListMonitoredResourceDescriptorsRequest,
):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListMonitoredResourceDescriptorsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_monitored_resource_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListMonitoredResourceDescriptorsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListMonitoredResourceDescriptorsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_monitored_resource_descriptors_from_dict():
    test_list_monitored_resource_descriptors(request_type=dict)


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async(
    transport: str = "grpc_asyncio",
    request_type=logging.ListMonitoredResourceDescriptorsRequest,
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListMonitoredResourceDescriptorsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_monitored_resource_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListMonitoredResourceDescriptorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMonitoredResourceDescriptorsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_from_dict():
    await test_list_monitored_resource_descriptors_async(request_type=dict)


def test_list_monitored_resource_descriptors_pager():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="abc",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[], next_page_token="def",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="ghi",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_monitored_resource_descriptors(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, monitored_resource.MonitoredResourceDescriptor)
            for i in results
        )


def test_list_monitored_resource_descriptors_pages():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="abc",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[], next_page_token="def",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="ghi",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_monitored_resource_descriptors(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_pager():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="abc",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[], next_page_token="def",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="ghi",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_monitored_resource_descriptors(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, monitored_resource.MonitoredResourceDescriptor)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_monitored_resource_descriptors_async_pages():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_monitored_resource_descriptors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="abc",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[], next_page_token="def",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
                next_page_token="ghi",
            ),
            logging.ListMonitoredResourceDescriptorsResponse(
                resource_descriptors=[
                    monitored_resource.MonitoredResourceDescriptor(),
                    monitored_resource.MonitoredResourceDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_monitored_resource_descriptors(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_logs(transport: str = "grpc", request_type=logging.ListLogsRequest):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse(
            log_names=["log_names_value"], next_page_token="next_page_token_value",
        )

        response = client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListLogsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListLogsPager)

    assert response.log_names == ["log_names_value"]

    assert response.next_page_token == "next_page_token_value"


def test_list_logs_from_dict():
    test_list_logs(request_type=dict)


@pytest.mark.asyncio
async def test_list_logs_async(
    transport: str = "grpc_asyncio", request_type=logging.ListLogsRequest
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListLogsResponse(
                log_names=["log_names_value"], next_page_token="next_page_token_value",
            )
        )

        response = await client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging.ListLogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogsAsyncPager)

    assert response.log_names == ["log_names_value"]

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_logs_async_from_dict():
    await test_list_logs_async(request_type=dict)


def test_list_logs_field_headers():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.ListLogsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        call.return_value = logging.ListLogsResponse()

        client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_logs_field_headers_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging.ListLogsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListLogsResponse()
        )

        await client.list_logs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_logs_flattened():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_logs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_logs_flattened_error():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_logs(
            logging.ListLogsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_logs_flattened_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging.ListLogsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging.ListLogsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_logs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_logs_flattened_error_async():
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_logs(
            logging.ListLogsRequest(), parent="parent_value",
        )


def test_list_logs_pager():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[str(), str(), str(),], next_page_token="abc",
            ),
            logging.ListLogsResponse(log_names=[], next_page_token="def",),
            logging.ListLogsResponse(log_names=[str(),], next_page_token="ghi",),
            logging.ListLogsResponse(log_names=[str(), str(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_logs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_list_logs_pages():
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_logs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[str(), str(), str(),], next_page_token="abc",
            ),
            logging.ListLogsResponse(log_names=[], next_page_token="def",),
            logging.ListLogsResponse(log_names=[str(),], next_page_token="ghi",),
            logging.ListLogsResponse(log_names=[str(), str(),],),
            RuntimeError,
        )
        pages = list(client.list_logs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_logs_async_pager():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_logs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[str(), str(), str(),], next_page_token="abc",
            ),
            logging.ListLogsResponse(log_names=[], next_page_token="def",),
            logging.ListLogsResponse(log_names=[str(),], next_page_token="ghi",),
            logging.ListLogsResponse(log_names=[str(), str(),],),
            RuntimeError,
        )
        async_pager = await client.list_logs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_list_logs_async_pages():
    client = LoggingServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_logs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging.ListLogsResponse(
                log_names=[str(), str(), str(),], next_page_token="abc",
            ),
            logging.ListLogsResponse(log_names=[], next_page_token="def",),
            logging.ListLogsResponse(log_names=[str(),], next_page_token="ghi",),
            logging.ListLogsResponse(log_names=[str(), str(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_logs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_tail_log_entries(
    transport: str = "grpc", request_type=logging.TailLogEntriesRequest
):
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tail_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([logging.TailLogEntriesResponse()])

        response = client.tail_log_entries(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, logging.TailLogEntriesResponse)


def test_tail_log_entries_from_dict():
    test_tail_log_entries(request_type=dict)


@pytest.mark.asyncio
async def test_tail_log_entries_async(
    transport: str = "grpc_asyncio", request_type=logging.TailLogEntriesRequest
):
    client = LoggingServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tail_log_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[logging.TailLogEntriesResponse()]
        )

        response = await client.tail_log_entries(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, logging.TailLogEntriesResponse)


@pytest.mark.asyncio
async def test_tail_log_entries_async_from_dict():
    await test_tail_log_entries_async(request_type=dict)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LoggingServiceV2Client(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = LoggingServiceV2Client(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LoggingServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.LoggingServiceV2GrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LoggingServiceV2GrpcTransport,
        transports.LoggingServiceV2GrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = LoggingServiceV2Client(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.LoggingServiceV2GrpcTransport,)


def test_logging_service_v2_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.LoggingServiceV2Transport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_logging_service_v2_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.LoggingServiceV2Transport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "delete_log",
        "write_log_entries",
        "list_log_entries",
        "list_monitored_resource_descriptors",
        "list_logs",
        "tail_log_entries",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_logging_service_v2_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.LoggingServiceV2Transport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id="octopus",
        )


def test_logging_service_v2_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.logging_v2.services.logging_service_v2.transports.LoggingServiceV2Transport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.LoggingServiceV2Transport()
        adc.assert_called_once()


def test_logging_service_v2_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        LoggingServiceV2Client()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id=None,
        )


def test_logging_service_v2_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.LoggingServiceV2GrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id="octopus",
        )


def test_logging_service_v2_host_no_port():
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="logging.googleapis.com"
        ),
    )
    assert client.transport._host == "logging.googleapis.com:443"


def test_logging_service_v2_host_with_port():
    client = LoggingServiceV2Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="logging.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "logging.googleapis.com:8000"


def test_logging_service_v2_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.LoggingServiceV2GrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_logging_service_v2_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.LoggingServiceV2GrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LoggingServiceV2GrpcTransport,
        transports.LoggingServiceV2GrpcAsyncIOTransport,
    ],
)
def test_logging_service_v2_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                    "https://www.googleapis.com/auth/logging.admin",
                    "https://www.googleapis.com/auth/logging.read",
                    "https://www.googleapis.com/auth/logging.write",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LoggingServiceV2GrpcTransport,
        transports.LoggingServiceV2GrpcAsyncIOTransport,
    ],
)
def test_logging_service_v2_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                    "https://www.googleapis.com/auth/logging.admin",
                    "https://www.googleapis.com/auth/logging.read",
                    "https://www.googleapis.com/auth/logging.write",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_log_path():
    project = "squid"
    log = "clam"

    expected = "projects/{project}/logs/{log}".format(project=project, log=log,)
    actual = LoggingServiceV2Client.log_path(project, log)
    assert expected == actual


def test_parse_log_path():
    expected = {
        "project": "whelk",
        "log": "octopus",
    }
    path = LoggingServiceV2Client.log_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_log_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = LoggingServiceV2Client.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = LoggingServiceV2Client.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"

    expected = "folders/{folder}".format(folder=folder,)
    actual = LoggingServiceV2Client.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = LoggingServiceV2Client.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = LoggingServiceV2Client.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = LoggingServiceV2Client.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"

    expected = "projects/{project}".format(project=project,)
    actual = LoggingServiceV2Client.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = LoggingServiceV2Client.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = LoggingServiceV2Client.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = LoggingServiceV2Client.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = LoggingServiceV2Client.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.LoggingServiceV2Transport, "_prep_wrapped_messages"
    ) as prep:
        client = LoggingServiceV2Client(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.LoggingServiceV2Transport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = LoggingServiceV2Client.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
