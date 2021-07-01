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
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dlp_v2.services.dlp_service import DlpServiceAsyncClient
from google.cloud.dlp_v2.services.dlp_service import DlpServiceClient
from google.cloud.dlp_v2.services.dlp_service import pagers
from google.cloud.dlp_v2.services.dlp_service import transports
from google.cloud.dlp_v2.services.dlp_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.dlp_v2.types import dlp
from google.cloud.dlp_v2.types import storage
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-auth >= 1.25.0 is required transitively
# through google-api-core:
# - Delete the auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
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

    assert DlpServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        DlpServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        DlpServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DlpServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DlpServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DlpServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [DlpServiceClient, DlpServiceAsyncClient,])
def test_dlp_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "dlp.googleapis.com:443"


@pytest.mark.parametrize("client_class", [DlpServiceClient, DlpServiceAsyncClient,])
def test_dlp_service_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DlpServiceGrpcTransport, "grpc"),
        (transports.DlpServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_dlp_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize("client_class", [DlpServiceClient, DlpServiceAsyncClient,])
def test_dlp_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "dlp.googleapis.com:443"


def test_dlp_service_client_get_transport_class():
    transport = DlpServiceClient.get_transport_class()
    available_transports = [
        transports.DlpServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = DlpServiceClient.get_transport_class("grpc")
    assert transport == transports.DlpServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DlpServiceClient, transports.DlpServiceGrpcTransport, "grpc"),
        (
            DlpServiceAsyncClient,
            transports.DlpServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DlpServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DlpServiceClient)
)
@mock.patch.object(
    DlpServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DlpServiceAsyncClient),
)
def test_dlp_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DlpServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DlpServiceClient, "get_transport_class") as gtc:
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
            client_cert_source_for_mtls=None,
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
                client_cert_source_for_mtls=None,
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
                client_cert_source_for_mtls=None,
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
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (DlpServiceClient, transports.DlpServiceGrpcTransport, "grpc", "true"),
        (
            DlpServiceAsyncClient,
            transports.DlpServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DlpServiceClient, transports.DlpServiceGrpcTransport, "grpc", "false"),
        (
            DlpServiceAsyncClient,
            transports.DlpServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DlpServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DlpServiceClient)
)
@mock.patch.object(
    DlpServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DlpServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_dlp_service_client_mtls_env_auto(
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
            client = client_class(client_options=options)

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
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DlpServiceClient, transports.DlpServiceGrpcTransport, "grpc"),
        (
            DlpServiceAsyncClient,
            transports.DlpServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_dlp_service_client_client_options_scopes(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DlpServiceClient, transports.DlpServiceGrpcTransport, "grpc"),
        (
            DlpServiceAsyncClient,
            transports.DlpServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_dlp_service_client_client_options_credentials_file(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_dlp_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dlp_v2.services.dlp_service.transports.DlpServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DlpServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_inspect_content(
    transport: str = "grpc", request_type=dlp.InspectContentRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.inspect_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectContentResponse()
        response = client.inspect_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.InspectContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectContentResponse)


def test_inspect_content_from_dict():
    test_inspect_content(request_type=dict)


def test_inspect_content_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.inspect_content), "__call__") as call:
        client.inspect_content()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.InspectContentRequest()


@pytest.mark.asyncio
async def test_inspect_content_async(
    transport: str = "grpc_asyncio", request_type=dlp.InspectContentRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.inspect_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.InspectContentResponse()
        )
        response = await client.inspect_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.InspectContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectContentResponse)


@pytest.mark.asyncio
async def test_inspect_content_async_from_dict():
    await test_inspect_content_async(request_type=dict)


def test_inspect_content_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.InspectContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.inspect_content), "__call__") as call:
        call.return_value = dlp.InspectContentResponse()
        client.inspect_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_inspect_content_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.InspectContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.inspect_content), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.InspectContentResponse()
        )
        await client.inspect_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_redact_image(transport: str = "grpc", request_type=dlp.RedactImageRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.redact_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.RedactImageResponse(
            redacted_image=b"redacted_image_blob",
            extracted_text="extracted_text_value",
        )
        response = client.redact_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.RedactImageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.RedactImageResponse)
    assert response.redacted_image == b"redacted_image_blob"
    assert response.extracted_text == "extracted_text_value"


def test_redact_image_from_dict():
    test_redact_image(request_type=dict)


def test_redact_image_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.redact_image), "__call__") as call:
        client.redact_image()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.RedactImageRequest()


@pytest.mark.asyncio
async def test_redact_image_async(
    transport: str = "grpc_asyncio", request_type=dlp.RedactImageRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.redact_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.RedactImageResponse(
                redacted_image=b"redacted_image_blob",
                extracted_text="extracted_text_value",
            )
        )
        response = await client.redact_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.RedactImageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.RedactImageResponse)
    assert response.redacted_image == b"redacted_image_blob"
    assert response.extracted_text == "extracted_text_value"


@pytest.mark.asyncio
async def test_redact_image_async_from_dict():
    await test_redact_image_async(request_type=dict)


def test_redact_image_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.RedactImageRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.redact_image), "__call__") as call:
        call.return_value = dlp.RedactImageResponse()
        client.redact_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_redact_image_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.RedactImageRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.redact_image), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.RedactImageResponse()
        )
        await client.redact_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_deidentify_content(
    transport: str = "grpc", request_type=dlp.DeidentifyContentRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deidentify_content), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyContentResponse()
        response = client.deidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeidentifyContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyContentResponse)


def test_deidentify_content_from_dict():
    test_deidentify_content(request_type=dict)


def test_deidentify_content_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deidentify_content), "__call__"
    ) as call:
        client.deidentify_content()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeidentifyContentRequest()


@pytest.mark.asyncio
async def test_deidentify_content_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeidentifyContentRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deidentify_content), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyContentResponse()
        )
        response = await client.deidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeidentifyContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyContentResponse)


@pytest.mark.asyncio
async def test_deidentify_content_async_from_dict():
    await test_deidentify_content_async(request_type=dict)


def test_deidentify_content_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeidentifyContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deidentify_content), "__call__"
    ) as call:
        call.return_value = dlp.DeidentifyContentResponse()
        client.deidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_deidentify_content_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeidentifyContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deidentify_content), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyContentResponse()
        )
        await client.deidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_reidentify_content(
    transport: str = "grpc", request_type=dlp.ReidentifyContentRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reidentify_content), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ReidentifyContentResponse()
        response = client.reidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ReidentifyContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.ReidentifyContentResponse)


def test_reidentify_content_from_dict():
    test_reidentify_content(request_type=dict)


def test_reidentify_content_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reidentify_content), "__call__"
    ) as call:
        client.reidentify_content()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ReidentifyContentRequest()


@pytest.mark.asyncio
async def test_reidentify_content_async(
    transport: str = "grpc_asyncio", request_type=dlp.ReidentifyContentRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reidentify_content), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ReidentifyContentResponse()
        )
        response = await client.reidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ReidentifyContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.ReidentifyContentResponse)


@pytest.mark.asyncio
async def test_reidentify_content_async_from_dict():
    await test_reidentify_content_async(request_type=dict)


def test_reidentify_content_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ReidentifyContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reidentify_content), "__call__"
    ) as call:
        call.return_value = dlp.ReidentifyContentResponse()
        client.reidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_reidentify_content_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ReidentifyContentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reidentify_content), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ReidentifyContentResponse()
        )
        await client.reidentify_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_info_types(
    transport: str = "grpc", request_type=dlp.ListInfoTypesRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_info_types), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInfoTypesResponse()
        response = client.list_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInfoTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.ListInfoTypesResponse)


def test_list_info_types_from_dict():
    test_list_info_types(request_type=dict)


def test_list_info_types_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_info_types), "__call__") as call:
        client.list_info_types()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInfoTypesRequest()


@pytest.mark.asyncio
async def test_list_info_types_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListInfoTypesRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_info_types), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListInfoTypesResponse()
        )
        response = await client.list_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInfoTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.ListInfoTypesResponse)


@pytest.mark.asyncio
async def test_list_info_types_async_from_dict():
    await test_list_info_types_async(request_type=dict)


def test_list_info_types_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_info_types), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInfoTypesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_info_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_info_types_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_info_types(
            dlp.ListInfoTypesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_info_types_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_info_types), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInfoTypesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListInfoTypesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_info_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_info_types_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_info_types(
            dlp.ListInfoTypesRequest(), parent="parent_value",
        )


def test_create_inspect_template(
    transport: str = "grpc", request_type=dlp.CreateInspectTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.create_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_inspect_template_from_dict():
    test_create_inspect_template(request_type=dict)


def test_create_inspect_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        client.create_inspect_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateInspectTemplateRequest()


@pytest.mark.asyncio
async def test_create_inspect_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.CreateInspectTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.InspectTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.create_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_inspect_template_async_from_dict():
    await test_create_inspect_template_async(request_type=dict)


def test_create_inspect_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateInspectTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        call.return_value = dlp.InspectTemplate()
        client.create_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_inspect_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateInspectTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        await client.create_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_inspect_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_inspect_template(
            parent="parent_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].inspect_template == dlp.InspectTemplate(name="name_value")


def test_create_inspect_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_inspect_template(
            dlp.CreateInspectTemplateRequest(),
            parent="parent_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_inspect_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_inspect_template(
            parent="parent_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].inspect_template == dlp.InspectTemplate(name="name_value")


@pytest.mark.asyncio
async def test_create_inspect_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_inspect_template(
            dlp.CreateInspectTemplateRequest(),
            parent="parent_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
        )


def test_update_inspect_template(
    transport: str = "grpc", request_type=dlp.UpdateInspectTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.update_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_inspect_template_from_dict():
    test_update_inspect_template(request_type=dict)


def test_update_inspect_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        client.update_inspect_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateInspectTemplateRequest()


@pytest.mark.asyncio
async def test_update_inspect_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.UpdateInspectTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.InspectTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.update_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_inspect_template_async_from_dict():
    await test_update_inspect_template_async(request_type=dict)


def test_update_inspect_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        call.return_value = dlp.InspectTemplate()
        client.update_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_inspect_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        await client.update_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_inspect_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_inspect_template(
            name="name_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].inspect_template == dlp.InspectTemplate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_inspect_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_inspect_template(
            dlp.UpdateInspectTemplateRequest(),
            name="name_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_inspect_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_inspect_template(
            name="name_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].inspect_template == dlp.InspectTemplate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_inspect_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_inspect_template(
            dlp.UpdateInspectTemplateRequest(),
            name="name_value",
            inspect_template=dlp.InspectTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_inspect_template(
    transport: str = "grpc", request_type=dlp.GetInspectTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_inspect_template_from_dict():
    test_get_inspect_template(request_type=dict)


def test_get_inspect_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        client.get_inspect_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetInspectTemplateRequest()


@pytest.mark.asyncio
async def test_get_inspect_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.GetInspectTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.InspectTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.InspectTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_inspect_template_async_from_dict():
    await test_get_inspect_template_async(request_type=dict)


def test_get_inspect_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        call.return_value = dlp.InspectTemplate()
        client.get_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_inspect_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        await client.get_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_inspect_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_inspect_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_inspect_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_inspect_template(
            dlp.GetInspectTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_inspect_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.InspectTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.InspectTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_inspect_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_inspect_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_inspect_template(
            dlp.GetInspectTemplateRequest(), name="name_value",
        )


def test_list_inspect_templates(
    transport: str = "grpc", request_type=dlp.ListInspectTemplatesRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInspectTemplatesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_inspect_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInspectTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInspectTemplatesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_inspect_templates_from_dict():
    test_list_inspect_templates(request_type=dict)


def test_list_inspect_templates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        client.list_inspect_templates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInspectTemplatesRequest()


@pytest.mark.asyncio
async def test_list_inspect_templates_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListInspectTemplatesRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListInspectTemplatesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_inspect_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListInspectTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInspectTemplatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_inspect_templates_async_from_dict():
    await test_list_inspect_templates_async(request_type=dict)


def test_list_inspect_templates_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListInspectTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        call.return_value = dlp.ListInspectTemplatesResponse()
        client.list_inspect_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_inspect_templates_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListInspectTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListInspectTemplatesResponse()
        )
        await client.list_inspect_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_inspect_templates_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInspectTemplatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_inspect_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_inspect_templates_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_inspect_templates(
            dlp.ListInspectTemplatesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_inspect_templates_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListInspectTemplatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListInspectTemplatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_inspect_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_inspect_templates_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_inspect_templates(
            dlp.ListInspectTemplatesRequest(), parent="parent_value",
        )


def test_list_inspect_templates_pager():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[], next_page_token="def",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(),], next_page_token="ghi",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(), dlp.InspectTemplate(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_inspect_templates(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dlp.InspectTemplate) for i in results)


def test_list_inspect_templates_pages():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[], next_page_token="def",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(),], next_page_token="ghi",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(), dlp.InspectTemplate(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_inspect_templates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_inspect_templates_async_pager():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[], next_page_token="def",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(),], next_page_token="ghi",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(), dlp.InspectTemplate(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_inspect_templates(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dlp.InspectTemplate) for i in responses)


@pytest.mark.asyncio
async def test_list_inspect_templates_async_pages():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inspect_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                    dlp.InspectTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[], next_page_token="def",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(),], next_page_token="ghi",
            ),
            dlp.ListInspectTemplatesResponse(
                inspect_templates=[dlp.InspectTemplate(), dlp.InspectTemplate(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_inspect_templates(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_inspect_template(
    transport: str = "grpc", request_type=dlp.DeleteInspectTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_inspect_template_from_dict():
    test_delete_inspect_template(request_type=dict)


def test_delete_inspect_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        client.delete_inspect_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteInspectTemplateRequest()


@pytest.mark.asyncio
async def test_delete_inspect_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeleteInspectTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteInspectTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_inspect_template_async_from_dict():
    await test_delete_inspect_template_async(request_type=dict)


def test_delete_inspect_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        call.return_value = None
        client.delete_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_inspect_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteInspectTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_inspect_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_inspect_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_inspect_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_inspect_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_inspect_template(
            dlp.DeleteInspectTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_inspect_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_inspect_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_inspect_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_inspect_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_inspect_template(
            dlp.DeleteInspectTemplateRequest(), name="name_value",
        )


def test_create_deidentify_template(
    transport: str = "grpc", request_type=dlp.CreateDeidentifyTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.create_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_deidentify_template_from_dict():
    test_create_deidentify_template(request_type=dict)


def test_create_deidentify_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        client.create_deidentify_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDeidentifyTemplateRequest()


@pytest.mark.asyncio
async def test_create_deidentify_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.CreateDeidentifyTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.create_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_deidentify_template_async_from_dict():
    await test_create_deidentify_template_async(request_type=dict)


def test_create_deidentify_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateDeidentifyTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        call.return_value = dlp.DeidentifyTemplate()
        client.create_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_deidentify_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateDeidentifyTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        await client.create_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_deidentify_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_deidentify_template(
            parent="parent_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].deidentify_template == dlp.DeidentifyTemplate(name="name_value")


def test_create_deidentify_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_deidentify_template(
            dlp.CreateDeidentifyTemplateRequest(),
            parent="parent_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_deidentify_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_deidentify_template(
            parent="parent_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].deidentify_template == dlp.DeidentifyTemplate(name="name_value")


@pytest.mark.asyncio
async def test_create_deidentify_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_deidentify_template(
            dlp.CreateDeidentifyTemplateRequest(),
            parent="parent_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
        )


def test_update_deidentify_template(
    transport: str = "grpc", request_type=dlp.UpdateDeidentifyTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.update_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_deidentify_template_from_dict():
    test_update_deidentify_template(request_type=dict)


def test_update_deidentify_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        client.update_deidentify_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateDeidentifyTemplateRequest()


@pytest.mark.asyncio
async def test_update_deidentify_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.UpdateDeidentifyTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.update_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_deidentify_template_async_from_dict():
    await test_update_deidentify_template_async(request_type=dict)


def test_update_deidentify_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        call.return_value = dlp.DeidentifyTemplate()
        client.update_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_deidentify_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        await client.update_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_deidentify_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_deidentify_template(
            name="name_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].deidentify_template == dlp.DeidentifyTemplate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_deidentify_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_deidentify_template(
            dlp.UpdateDeidentifyTemplateRequest(),
            name="name_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_deidentify_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_deidentify_template(
            name="name_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].deidentify_template == dlp.DeidentifyTemplate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_deidentify_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_deidentify_template(
            dlp.UpdateDeidentifyTemplateRequest(),
            name="name_value",
            deidentify_template=dlp.DeidentifyTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_deidentify_template(
    transport: str = "grpc", request_type=dlp.GetDeidentifyTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_deidentify_template_from_dict():
    test_get_deidentify_template(request_type=dict)


def test_get_deidentify_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        client.get_deidentify_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDeidentifyTemplateRequest()


@pytest.mark.asyncio
async def test_get_deidentify_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.GetDeidentifyTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DeidentifyTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_deidentify_template_async_from_dict():
    await test_get_deidentify_template_async(request_type=dict)


def test_get_deidentify_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        call.return_value = dlp.DeidentifyTemplate()
        client.get_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_deidentify_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        await client.get_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_deidentify_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_deidentify_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_deidentify_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_deidentify_template(
            dlp.GetDeidentifyTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_deidentify_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DeidentifyTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DeidentifyTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_deidentify_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_deidentify_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_deidentify_template(
            dlp.GetDeidentifyTemplateRequest(), name="name_value",
        )


def test_list_deidentify_templates(
    transport: str = "grpc", request_type=dlp.ListDeidentifyTemplatesRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDeidentifyTemplatesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_deidentify_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDeidentifyTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeidentifyTemplatesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deidentify_templates_from_dict():
    test_list_deidentify_templates(request_type=dict)


def test_list_deidentify_templates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        client.list_deidentify_templates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDeidentifyTemplatesRequest()


@pytest.mark.asyncio
async def test_list_deidentify_templates_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListDeidentifyTemplatesRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDeidentifyTemplatesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_deidentify_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDeidentifyTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeidentifyTemplatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_deidentify_templates_async_from_dict():
    await test_list_deidentify_templates_async(request_type=dict)


def test_list_deidentify_templates_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListDeidentifyTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        call.return_value = dlp.ListDeidentifyTemplatesResponse()
        client.list_deidentify_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_deidentify_templates_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListDeidentifyTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDeidentifyTemplatesResponse()
        )
        await client.list_deidentify_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_deidentify_templates_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDeidentifyTemplatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_deidentify_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_deidentify_templates_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deidentify_templates(
            dlp.ListDeidentifyTemplatesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_deidentify_templates_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDeidentifyTemplatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDeidentifyTemplatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_deidentify_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_deidentify_templates_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_deidentify_templates(
            dlp.ListDeidentifyTemplatesRequest(), parent="parent_value",
        )


def test_list_deidentify_templates_pager():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[], next_page_token="def",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[dlp.DeidentifyTemplate(),], next_page_token="ghi",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_deidentify_templates(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dlp.DeidentifyTemplate) for i in results)


def test_list_deidentify_templates_pages():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[], next_page_token="def",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[dlp.DeidentifyTemplate(),], next_page_token="ghi",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_deidentify_templates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_deidentify_templates_async_pager():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[], next_page_token="def",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[dlp.DeidentifyTemplate(),], next_page_token="ghi",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_deidentify_templates(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dlp.DeidentifyTemplate) for i in responses)


@pytest.mark.asyncio
async def test_list_deidentify_templates_async_pages():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deidentify_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
                next_page_token="abc",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[], next_page_token="def",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[dlp.DeidentifyTemplate(),], next_page_token="ghi",
            ),
            dlp.ListDeidentifyTemplatesResponse(
                deidentify_templates=[
                    dlp.DeidentifyTemplate(),
                    dlp.DeidentifyTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_deidentify_templates(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_deidentify_template(
    transport: str = "grpc", request_type=dlp.DeleteDeidentifyTemplateRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_deidentify_template_from_dict():
    test_delete_deidentify_template(request_type=dict)


def test_delete_deidentify_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        client.delete_deidentify_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDeidentifyTemplateRequest()


@pytest.mark.asyncio
async def test_delete_deidentify_template_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeleteDeidentifyTemplateRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDeidentifyTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_deidentify_template_async_from_dict():
    await test_delete_deidentify_template_async(request_type=dict)


def test_delete_deidentify_template_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        call.return_value = None
        client.delete_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_deidentify_template_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteDeidentifyTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_deidentify_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_deidentify_template_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_deidentify_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_deidentify_template_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_deidentify_template(
            dlp.DeleteDeidentifyTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_deidentify_template_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deidentify_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_deidentify_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_deidentify_template_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_deidentify_template(
            dlp.DeleteDeidentifyTemplateRequest(), name="name_value",
        )


def test_create_job_trigger(
    transport: str = "grpc", request_type=dlp.CreateJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            status=dlp.JobTrigger.Status.HEALTHY,
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
        )
        response = client.create_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


def test_create_job_trigger_from_dict():
    test_create_job_trigger(request_type=dict)


def test_create_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        client.create_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateJobTriggerRequest()


@pytest.mark.asyncio
async def test_create_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.CreateJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.JobTrigger(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                status=dlp.JobTrigger.Status.HEALTHY,
            )
        )
        response = await client.create_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


@pytest.mark.asyncio
async def test_create_job_trigger_async_from_dict():
    await test_create_job_trigger_async(request_type=dict)


def test_create_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateJobTriggerRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        call.return_value = dlp.JobTrigger()
        client.create_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateJobTriggerRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        await client.create_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_job_trigger_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_job_trigger(
            parent="parent_value", job_trigger=dlp.JobTrigger(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].job_trigger == dlp.JobTrigger(name="name_value")


def test_create_job_trigger_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_job_trigger(
            dlp.CreateJobTriggerRequest(),
            parent="parent_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_job_trigger_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_job_trigger(
            parent="parent_value", job_trigger=dlp.JobTrigger(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].job_trigger == dlp.JobTrigger(name="name_value")


@pytest.mark.asyncio
async def test_create_job_trigger_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_job_trigger(
            dlp.CreateJobTriggerRequest(),
            parent="parent_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
        )


def test_update_job_trigger(
    transport: str = "grpc", request_type=dlp.UpdateJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            status=dlp.JobTrigger.Status.HEALTHY,
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
        )
        response = client.update_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


def test_update_job_trigger_from_dict():
    test_update_job_trigger(request_type=dict)


def test_update_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        client.update_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateJobTriggerRequest()


@pytest.mark.asyncio
async def test_update_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.UpdateJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.JobTrigger(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                status=dlp.JobTrigger.Status.HEALTHY,
            )
        )
        response = await client.update_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


@pytest.mark.asyncio
async def test_update_job_trigger_async_from_dict():
    await test_update_job_trigger_async(request_type=dict)


def test_update_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        call.return_value = dlp.JobTrigger()
        client.update_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        await client.update_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_job_trigger_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_job_trigger(
            name="name_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].job_trigger == dlp.JobTrigger(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_job_trigger_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_job_trigger(
            dlp.UpdateJobTriggerRequest(),
            name="name_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_job_trigger_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_job_trigger(
            name="name_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].job_trigger == dlp.JobTrigger(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_job_trigger_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_job_trigger(
            dlp.UpdateJobTriggerRequest(),
            name="name_value",
            job_trigger=dlp.JobTrigger(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_hybrid_inspect_job_trigger(
    transport: str = "grpc", request_type=dlp.HybridInspectJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()
        response = client.hybrid_inspect_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.HybridInspectResponse)


def test_hybrid_inspect_job_trigger_from_dict():
    test_hybrid_inspect_job_trigger(request_type=dict)


def test_hybrid_inspect_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        client.hybrid_inspect_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectJobTriggerRequest()


@pytest.mark.asyncio
async def test_hybrid_inspect_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.HybridInspectJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        response = await client.hybrid_inspect_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.HybridInspectResponse)


@pytest.mark.asyncio
async def test_hybrid_inspect_job_trigger_async_from_dict():
    await test_hybrid_inspect_job_trigger_async(request_type=dict)


def test_hybrid_inspect_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.HybridInspectJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        call.return_value = dlp.HybridInspectResponse()
        client.hybrid_inspect_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_hybrid_inspect_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.HybridInspectJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        await client.hybrid_inspect_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_hybrid_inspect_job_trigger_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.hybrid_inspect_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_hybrid_inspect_job_trigger_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.hybrid_inspect_job_trigger(
            dlp.HybridInspectJobTriggerRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_hybrid_inspect_job_trigger_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.hybrid_inspect_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_hybrid_inspect_job_trigger_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.hybrid_inspect_job_trigger(
            dlp.HybridInspectJobTriggerRequest(), name="name_value",
        )


def test_get_job_trigger(
    transport: str = "grpc", request_type=dlp.GetJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            status=dlp.JobTrigger.Status.HEALTHY,
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
        )
        response = client.get_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


def test_get_job_trigger_from_dict():
    test_get_job_trigger(request_type=dict)


def test_get_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        client.get_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetJobTriggerRequest()


@pytest.mark.asyncio
async def test_get_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.GetJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.JobTrigger(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                status=dlp.JobTrigger.Status.HEALTHY,
            )
        )
        response = await client.get_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.JobTrigger)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.status == dlp.JobTrigger.Status.HEALTHY


@pytest.mark.asyncio
async def test_get_job_trigger_async_from_dict():
    await test_get_job_trigger_async(request_type=dict)


def test_get_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        call.return_value = dlp.JobTrigger()
        client.get_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        await client.get_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_job_trigger_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_job_trigger_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_job_trigger(
            dlp.GetJobTriggerRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_job_trigger_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job_trigger), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.JobTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.JobTrigger())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_job_trigger_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_job_trigger(
            dlp.GetJobTriggerRequest(), name="name_value",
        )


def test_list_job_triggers(
    transport: str = "grpc", request_type=dlp.ListJobTriggersRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListJobTriggersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_job_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListJobTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobTriggersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_job_triggers_from_dict():
    test_list_job_triggers(request_type=dict)


def test_list_job_triggers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        client.list_job_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListJobTriggersRequest()


@pytest.mark.asyncio
async def test_list_job_triggers_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListJobTriggersRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListJobTriggersResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_job_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListJobTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobTriggersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_job_triggers_async_from_dict():
    await test_list_job_triggers_async(request_type=dict)


def test_list_job_triggers_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListJobTriggersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        call.return_value = dlp.ListJobTriggersResponse()
        client.list_job_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_job_triggers_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListJobTriggersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListJobTriggersResponse()
        )
        await client.list_job_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_job_triggers_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListJobTriggersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_job_triggers(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_job_triggers_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_job_triggers(
            dlp.ListJobTriggersRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_job_triggers_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListJobTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListJobTriggersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_job_triggers(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_job_triggers_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_job_triggers(
            dlp.ListJobTriggersRequest(), parent="parent_value",
        )


def test_list_job_triggers_pager():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(), dlp.JobTrigger(),],
                next_page_token="abc",
            ),
            dlp.ListJobTriggersResponse(job_triggers=[], next_page_token="def",),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(),], next_page_token="ghi",
            ),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_job_triggers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dlp.JobTrigger) for i in results)


def test_list_job_triggers_pages():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(), dlp.JobTrigger(),],
                next_page_token="abc",
            ),
            dlp.ListJobTriggersResponse(job_triggers=[], next_page_token="def",),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(),], next_page_token="ghi",
            ),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_job_triggers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_job_triggers_async_pager():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(), dlp.JobTrigger(),],
                next_page_token="abc",
            ),
            dlp.ListJobTriggersResponse(job_triggers=[], next_page_token="def",),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(),], next_page_token="ghi",
            ),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_job_triggers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dlp.JobTrigger) for i in responses)


@pytest.mark.asyncio
async def test_list_job_triggers_async_pages():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_job_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(), dlp.JobTrigger(),],
                next_page_token="abc",
            ),
            dlp.ListJobTriggersResponse(job_triggers=[], next_page_token="def",),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(),], next_page_token="ghi",
            ),
            dlp.ListJobTriggersResponse(
                job_triggers=[dlp.JobTrigger(), dlp.JobTrigger(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_job_triggers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_job_trigger(
    transport: str = "grpc", request_type=dlp.DeleteJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_job_trigger_from_dict():
    test_delete_job_trigger(request_type=dict)


def test_delete_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        client.delete_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteJobTriggerRequest()


@pytest.mark.asyncio
async def test_delete_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeleteJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_job_trigger_async_from_dict():
    await test_delete_job_trigger_async(request_type=dict)


def test_delete_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        call.return_value = None
        client.delete_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_job_trigger_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_job_trigger_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_job_trigger(
            dlp.DeleteJobTriggerRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_job_trigger_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_job_trigger(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_job_trigger_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_job_trigger(
            dlp.DeleteJobTriggerRequest(), name="name_value",
        )


def test_activate_job_trigger(
    transport: str = "grpc", request_type=dlp.ActivateJobTriggerRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob(
            name="name_value",
            type_=dlp.DlpJobType.INSPECT_JOB,
            state=dlp.DlpJob.JobState.PENDING,
            job_trigger_name="job_trigger_name_value",
            risk_details=dlp.AnalyzeDataSourceRiskDetails(
                requested_privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )
        response = client.activate_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ActivateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


def test_activate_job_trigger_from_dict():
    test_activate_job_trigger(request_type=dict)


def test_activate_job_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_job_trigger), "__call__"
    ) as call:
        client.activate_job_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ActivateJobTriggerRequest()


@pytest.mark.asyncio
async def test_activate_job_trigger_async(
    transport: str = "grpc_asyncio", request_type=dlp.ActivateJobTriggerRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_job_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DlpJob(
                name="name_value",
                type_=dlp.DlpJobType.INSPECT_JOB,
                state=dlp.DlpJob.JobState.PENDING,
                job_trigger_name="job_trigger_name_value",
            )
        )
        response = await client.activate_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ActivateJobTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


@pytest.mark.asyncio
async def test_activate_job_trigger_async_from_dict():
    await test_activate_job_trigger_async(request_type=dict)


def test_activate_job_trigger_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ActivateJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_job_trigger), "__call__"
    ) as call:
        call.return_value = dlp.DlpJob()
        client.activate_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_activate_job_trigger_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ActivateJobTriggerRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_job_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.DlpJob())
        await client.activate_job_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_dlp_job(transport: str = "grpc", request_type=dlp.CreateDlpJobRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob(
            name="name_value",
            type_=dlp.DlpJobType.INSPECT_JOB,
            state=dlp.DlpJob.JobState.PENDING,
            job_trigger_name="job_trigger_name_value",
            risk_details=dlp.AnalyzeDataSourceRiskDetails(
                requested_privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )
        response = client.create_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


def test_create_dlp_job_from_dict():
    test_create_dlp_job(request_type=dict)


def test_create_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        client.create_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDlpJobRequest()


@pytest.mark.asyncio
async def test_create_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.CreateDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DlpJob(
                name="name_value",
                type_=dlp.DlpJobType.INSPECT_JOB,
                state=dlp.DlpJob.JobState.PENDING,
                job_trigger_name="job_trigger_name_value",
            )
        )
        response = await client.create_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


@pytest.mark.asyncio
async def test_create_dlp_job_async_from_dict():
    await test_create_dlp_job_async(request_type=dict)


def test_create_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateDlpJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        call.return_value = dlp.DlpJob()
        client.create_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateDlpJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.DlpJob())
        await client.create_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_dlp_job_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dlp_job(
            parent="parent_value",
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
            risk_job=dlp.RiskAnalysisJobConfig(
                privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].risk_job == dlp.RiskAnalysisJobConfig(
            privacy_metric=dlp.PrivacyMetric(
                numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                    field=storage.FieldId(name="name_value")
                )
            )
        )


def test_create_dlp_job_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dlp_job(
            dlp.CreateDlpJobRequest(),
            parent="parent_value",
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
            risk_job=dlp.RiskAnalysisJobConfig(
                privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_dlp_job_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.DlpJob())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dlp_job(
            parent="parent_value",
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
            risk_job=dlp.RiskAnalysisJobConfig(
                privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].risk_job == dlp.RiskAnalysisJobConfig(
            privacy_metric=dlp.PrivacyMetric(
                numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                    field=storage.FieldId(name="name_value")
                )
            )
        )


@pytest.mark.asyncio
async def test_create_dlp_job_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dlp_job(
            dlp.CreateDlpJobRequest(),
            parent="parent_value",
            inspect_job=dlp.InspectJobConfig(
                storage_config=storage.StorageConfig(
                    datastore_options=storage.DatastoreOptions(
                        partition_id=storage.PartitionId(project_id="project_id_value")
                    )
                )
            ),
            risk_job=dlp.RiskAnalysisJobConfig(
                privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )


def test_list_dlp_jobs(transport: str = "grpc", request_type=dlp.ListDlpJobsRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDlpJobsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_dlp_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDlpJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDlpJobsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_dlp_jobs_from_dict():
    test_list_dlp_jobs(request_type=dict)


def test_list_dlp_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        client.list_dlp_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDlpJobsRequest()


@pytest.mark.asyncio
async def test_list_dlp_jobs_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListDlpJobsRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDlpJobsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_dlp_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListDlpJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDlpJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_dlp_jobs_async_from_dict():
    await test_list_dlp_jobs_async(request_type=dict)


def test_list_dlp_jobs_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListDlpJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        call.return_value = dlp.ListDlpJobsResponse()
        client.list_dlp_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_dlp_jobs_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListDlpJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDlpJobsResponse()
        )
        await client.list_dlp_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_dlp_jobs_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDlpJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_dlp_jobs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_dlp_jobs_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dlp_jobs(
            dlp.ListDlpJobsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_dlp_jobs_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListDlpJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListDlpJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_dlp_jobs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_dlp_jobs_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_dlp_jobs(
            dlp.ListDlpJobsRequest(), parent="parent_value",
        )


def test_list_dlp_jobs_pager():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDlpJobsResponse(
                jobs=[dlp.DlpJob(), dlp.DlpJob(), dlp.DlpJob(),], next_page_token="abc",
            ),
            dlp.ListDlpJobsResponse(jobs=[], next_page_token="def",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(),], next_page_token="ghi",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(), dlp.DlpJob(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_dlp_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dlp.DlpJob) for i in results)


def test_list_dlp_jobs_pages():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_dlp_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDlpJobsResponse(
                jobs=[dlp.DlpJob(), dlp.DlpJob(), dlp.DlpJob(),], next_page_token="abc",
            ),
            dlp.ListDlpJobsResponse(jobs=[], next_page_token="def",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(),], next_page_token="ghi",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(), dlp.DlpJob(),],),
            RuntimeError,
        )
        pages = list(client.list_dlp_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_dlp_jobs_async_pager():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dlp_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDlpJobsResponse(
                jobs=[dlp.DlpJob(), dlp.DlpJob(), dlp.DlpJob(),], next_page_token="abc",
            ),
            dlp.ListDlpJobsResponse(jobs=[], next_page_token="def",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(),], next_page_token="ghi",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(), dlp.DlpJob(),],),
            RuntimeError,
        )
        async_pager = await client.list_dlp_jobs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dlp.DlpJob) for i in responses)


@pytest.mark.asyncio
async def test_list_dlp_jobs_async_pages():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dlp_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListDlpJobsResponse(
                jobs=[dlp.DlpJob(), dlp.DlpJob(), dlp.DlpJob(),], next_page_token="abc",
            ),
            dlp.ListDlpJobsResponse(jobs=[], next_page_token="def",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(),], next_page_token="ghi",),
            dlp.ListDlpJobsResponse(jobs=[dlp.DlpJob(), dlp.DlpJob(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_dlp_jobs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_dlp_job(transport: str = "grpc", request_type=dlp.GetDlpJobRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob(
            name="name_value",
            type_=dlp.DlpJobType.INSPECT_JOB,
            state=dlp.DlpJob.JobState.PENDING,
            job_trigger_name="job_trigger_name_value",
            risk_details=dlp.AnalyzeDataSourceRiskDetails(
                requested_privacy_metric=dlp.PrivacyMetric(
                    numerical_stats_config=dlp.PrivacyMetric.NumericalStatsConfig(
                        field=storage.FieldId(name="name_value")
                    )
                )
            ),
        )
        response = client.get_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


def test_get_dlp_job_from_dict():
    test_get_dlp_job(request_type=dict)


def test_get_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        client.get_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDlpJobRequest()


@pytest.mark.asyncio
async def test_get_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.GetDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.DlpJob(
                name="name_value",
                type_=dlp.DlpJobType.INSPECT_JOB,
                state=dlp.DlpJob.JobState.PENDING,
                job_trigger_name="job_trigger_name_value",
            )
        )
        response = await client.get_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.DlpJob)
    assert response.name == "name_value"
    assert response.type_ == dlp.DlpJobType.INSPECT_JOB
    assert response.state == dlp.DlpJob.JobState.PENDING
    assert response.job_trigger_name == "job_trigger_name_value"


@pytest.mark.asyncio
async def test_get_dlp_job_async_from_dict():
    await test_get_dlp_job_async(request_type=dict)


def test_get_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        call.return_value = dlp.DlpJob()
        client.get_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.DlpJob())
        await client.get_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_dlp_job_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_dlp_job_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dlp_job(
            dlp.GetDlpJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dlp_job_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.DlpJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.DlpJob())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_dlp_job_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dlp_job(
            dlp.GetDlpJobRequest(), name="name_value",
        )


def test_delete_dlp_job(transport: str = "grpc", request_type=dlp.DeleteDlpJobRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dlp_job_from_dict():
    test_delete_dlp_job(request_type=dict)


def test_delete_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        client.delete_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDlpJobRequest()


@pytest.mark.asyncio
async def test_delete_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeleteDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_dlp_job_async_from_dict():
    await test_delete_dlp_job_async(request_type=dict)


def test_delete_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        call.return_value = None
        client.delete_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_dlp_job_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_dlp_job_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dlp_job(
            dlp.DeleteDlpJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dlp_job_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_dlp_job_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dlp_job(
            dlp.DeleteDlpJobRequest(), name="name_value",
        )


def test_cancel_dlp_job(transport: str = "grpc", request_type=dlp.CancelDlpJobRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CancelDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_dlp_job_from_dict():
    test_cancel_dlp_job(request_type=dict)


def test_cancel_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_dlp_job), "__call__") as call:
        client.cancel_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CancelDlpJobRequest()


@pytest.mark.asyncio
async def test_cancel_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.CancelDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CancelDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_dlp_job_async_from_dict():
    await test_cancel_dlp_job_async(request_type=dict)


def test_cancel_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CancelDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_dlp_job), "__call__") as call:
        call.return_value = None
        client.cancel_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CancelDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_dlp_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_stored_info_type(
    transport: str = "grpc", request_type=dlp.CreateStoredInfoTypeRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType(name="name_value",)
        response = client.create_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


def test_create_stored_info_type_from_dict():
    test_create_stored_info_type(request_type=dict)


def test_create_stored_info_type_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        client.create_stored_info_type()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateStoredInfoTypeRequest()


@pytest.mark.asyncio
async def test_create_stored_info_type_async(
    transport: str = "grpc_asyncio", request_type=dlp.CreateStoredInfoTypeRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.StoredInfoType(name="name_value",)
        )
        response = await client.create_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.CreateStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_stored_info_type_async_from_dict():
    await test_create_stored_info_type_async(request_type=dict)


def test_create_stored_info_type_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateStoredInfoTypeRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        call.return_value = dlp.StoredInfoType()
        client.create_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_stored_info_type_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.CreateStoredInfoTypeRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        await client.create_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_stored_info_type_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_stored_info_type(
            parent="parent_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].config == dlp.StoredInfoTypeConfig(
            display_name="display_name_value"
        )


def test_create_stored_info_type_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_stored_info_type(
            dlp.CreateStoredInfoTypeRequest(),
            parent="parent_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
        )


@pytest.mark.asyncio
async def test_create_stored_info_type_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_stored_info_type(
            parent="parent_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].config == dlp.StoredInfoTypeConfig(
            display_name="display_name_value"
        )


@pytest.mark.asyncio
async def test_create_stored_info_type_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_stored_info_type(
            dlp.CreateStoredInfoTypeRequest(),
            parent="parent_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
        )


def test_update_stored_info_type(
    transport: str = "grpc", request_type=dlp.UpdateStoredInfoTypeRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType(name="name_value",)
        response = client.update_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


def test_update_stored_info_type_from_dict():
    test_update_stored_info_type(request_type=dict)


def test_update_stored_info_type_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        client.update_stored_info_type()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateStoredInfoTypeRequest()


@pytest.mark.asyncio
async def test_update_stored_info_type_async(
    transport: str = "grpc_asyncio", request_type=dlp.UpdateStoredInfoTypeRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.StoredInfoType(name="name_value",)
        )
        response = await client.update_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.UpdateStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_update_stored_info_type_async_from_dict():
    await test_update_stored_info_type_async(request_type=dict)


def test_update_stored_info_type_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        call.return_value = dlp.StoredInfoType()
        client.update_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_stored_info_type_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.UpdateStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        await client.update_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_stored_info_type_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_stored_info_type(
            name="name_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].config == dlp.StoredInfoTypeConfig(
            display_name="display_name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_stored_info_type_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_stored_info_type(
            dlp.UpdateStoredInfoTypeRequest(),
            name="name_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_stored_info_type_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_stored_info_type(
            name="name_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].config == dlp.StoredInfoTypeConfig(
            display_name="display_name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_stored_info_type_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_stored_info_type(
            dlp.UpdateStoredInfoTypeRequest(),
            name="name_value",
            config=dlp.StoredInfoTypeConfig(display_name="display_name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_stored_info_type(
    transport: str = "grpc", request_type=dlp.GetStoredInfoTypeRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType(name="name_value",)
        response = client.get_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


def test_get_stored_info_type_from_dict():
    test_get_stored_info_type(request_type=dict)


def test_get_stored_info_type_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        client.get_stored_info_type()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetStoredInfoTypeRequest()


@pytest.mark.asyncio
async def test_get_stored_info_type_async(
    transport: str = "grpc_asyncio", request_type=dlp.GetStoredInfoTypeRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.StoredInfoType(name="name_value",)
        )
        response = await client.get_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.GetStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.StoredInfoType)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_stored_info_type_async_from_dict():
    await test_get_stored_info_type_async(request_type=dict)


def test_get_stored_info_type_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        call.return_value = dlp.StoredInfoType()
        client.get_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_stored_info_type_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.GetStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        await client.get_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_stored_info_type_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_stored_info_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_stored_info_type_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_stored_info_type(
            dlp.GetStoredInfoTypeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_stored_info_type_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.StoredInfoType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dlp.StoredInfoType())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_stored_info_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_stored_info_type_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_stored_info_type(
            dlp.GetStoredInfoTypeRequest(), name="name_value",
        )


def test_list_stored_info_types(
    transport: str = "grpc", request_type=dlp.ListStoredInfoTypesRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListStoredInfoTypesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_stored_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListStoredInfoTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListStoredInfoTypesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_stored_info_types_from_dict():
    test_list_stored_info_types(request_type=dict)


def test_list_stored_info_types_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        client.list_stored_info_types()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListStoredInfoTypesRequest()


@pytest.mark.asyncio
async def test_list_stored_info_types_async(
    transport: str = "grpc_asyncio", request_type=dlp.ListStoredInfoTypesRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListStoredInfoTypesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_stored_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.ListStoredInfoTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListStoredInfoTypesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_stored_info_types_async_from_dict():
    await test_list_stored_info_types_async(request_type=dict)


def test_list_stored_info_types_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListStoredInfoTypesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        call.return_value = dlp.ListStoredInfoTypesResponse()
        client.list_stored_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_stored_info_types_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.ListStoredInfoTypesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListStoredInfoTypesResponse()
        )
        await client.list_stored_info_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_stored_info_types_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListStoredInfoTypesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_stored_info_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_stored_info_types_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_stored_info_types(
            dlp.ListStoredInfoTypesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_stored_info_types_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.ListStoredInfoTypesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.ListStoredInfoTypesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_stored_info_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_stored_info_types_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_stored_info_types(
            dlp.ListStoredInfoTypesRequest(), parent="parent_value",
        )


def test_list_stored_info_types_pager():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                ],
                next_page_token="abc",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[], next_page_token="def",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(),], next_page_token="ghi",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(), dlp.StoredInfoType(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_stored_info_types(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dlp.StoredInfoType) for i in results)


def test_list_stored_info_types_pages():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                ],
                next_page_token="abc",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[], next_page_token="def",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(),], next_page_token="ghi",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(), dlp.StoredInfoType(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_stored_info_types(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_stored_info_types_async_pager():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                ],
                next_page_token="abc",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[], next_page_token="def",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(),], next_page_token="ghi",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(), dlp.StoredInfoType(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_stored_info_types(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dlp.StoredInfoType) for i in responses)


@pytest.mark.asyncio
async def test_list_stored_info_types_async_pages():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_stored_info_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                    dlp.StoredInfoType(),
                ],
                next_page_token="abc",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[], next_page_token="def",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(),], next_page_token="ghi",
            ),
            dlp.ListStoredInfoTypesResponse(
                stored_info_types=[dlp.StoredInfoType(), dlp.StoredInfoType(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_stored_info_types(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_stored_info_type(
    transport: str = "grpc", request_type=dlp.DeleteStoredInfoTypeRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_stored_info_type_from_dict():
    test_delete_stored_info_type(request_type=dict)


def test_delete_stored_info_type_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        client.delete_stored_info_type()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteStoredInfoTypeRequest()


@pytest.mark.asyncio
async def test_delete_stored_info_type_async(
    transport: str = "grpc_asyncio", request_type=dlp.DeleteStoredInfoTypeRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.DeleteStoredInfoTypeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_stored_info_type_async_from_dict():
    await test_delete_stored_info_type_async(request_type=dict)


def test_delete_stored_info_type_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        call.return_value = None
        client.delete_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_stored_info_type_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.DeleteStoredInfoTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_stored_info_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_stored_info_type_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_stored_info_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_stored_info_type_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_stored_info_type(
            dlp.DeleteStoredInfoTypeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_stored_info_type_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_stored_info_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_stored_info_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_stored_info_type_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_stored_info_type(
            dlp.DeleteStoredInfoTypeRequest(), name="name_value",
        )


def test_hybrid_inspect_dlp_job(
    transport: str = "grpc", request_type=dlp.HybridInspectDlpJobRequest
):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()
        response = client.hybrid_inspect_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.HybridInspectResponse)


def test_hybrid_inspect_dlp_job_from_dict():
    test_hybrid_inspect_dlp_job(request_type=dict)


def test_hybrid_inspect_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        client.hybrid_inspect_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectDlpJobRequest()


@pytest.mark.asyncio
async def test_hybrid_inspect_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.HybridInspectDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        response = await client.hybrid_inspect_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.HybridInspectDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dlp.HybridInspectResponse)


@pytest.mark.asyncio
async def test_hybrid_inspect_dlp_job_async_from_dict():
    await test_hybrid_inspect_dlp_job_async(request_type=dict)


def test_hybrid_inspect_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.HybridInspectDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        call.return_value = dlp.HybridInspectResponse()
        client.hybrid_inspect_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_hybrid_inspect_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.HybridInspectDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        await client.hybrid_inspect_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_hybrid_inspect_dlp_job_flattened():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.hybrid_inspect_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_hybrid_inspect_dlp_job_flattened_error():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.hybrid_inspect_dlp_job(
            dlp.HybridInspectDlpJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_hybrid_inspect_dlp_job_flattened_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.hybrid_inspect_dlp_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = dlp.HybridInspectResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dlp.HybridInspectResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.hybrid_inspect_dlp_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_hybrid_inspect_dlp_job_flattened_error_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.hybrid_inspect_dlp_job(
            dlp.HybridInspectDlpJobRequest(), name="name_value",
        )


def test_finish_dlp_job(transport: str = "grpc", request_type=dlp.FinishDlpJobRequest):
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.finish_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.finish_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.FinishDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_finish_dlp_job_from_dict():
    test_finish_dlp_job(request_type=dict)


def test_finish_dlp_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.finish_dlp_job), "__call__") as call:
        client.finish_dlp_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.FinishDlpJobRequest()


@pytest.mark.asyncio
async def test_finish_dlp_job_async(
    transport: str = "grpc_asyncio", request_type=dlp.FinishDlpJobRequest
):
    client = DlpServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.finish_dlp_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.finish_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == dlp.FinishDlpJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_finish_dlp_job_async_from_dict():
    await test_finish_dlp_job_async(request_type=dict)


def test_finish_dlp_job_field_headers():
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.FinishDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.finish_dlp_job), "__call__") as call:
        call.return_value = None
        client.finish_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_finish_dlp_job_field_headers_async():
    client = DlpServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = dlp.FinishDlpJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.finish_dlp_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.finish_dlp_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DlpServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DlpServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DlpServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DlpServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DlpServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DlpServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DlpServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DlpServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DlpServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DlpServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DlpServiceClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.DlpServiceGrpcTransport,)


def test_dlp_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DlpServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_dlp_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dlp_v2.services.dlp_service.transports.DlpServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DlpServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "inspect_content",
        "redact_image",
        "deidentify_content",
        "reidentify_content",
        "list_info_types",
        "create_inspect_template",
        "update_inspect_template",
        "get_inspect_template",
        "list_inspect_templates",
        "delete_inspect_template",
        "create_deidentify_template",
        "update_deidentify_template",
        "get_deidentify_template",
        "list_deidentify_templates",
        "delete_deidentify_template",
        "create_job_trigger",
        "update_job_trigger",
        "hybrid_inspect_job_trigger",
        "get_job_trigger",
        "list_job_triggers",
        "delete_job_trigger",
        "activate_job_trigger",
        "create_dlp_job",
        "list_dlp_jobs",
        "get_dlp_job",
        "delete_dlp_job",
        "cancel_dlp_job",
        "create_stored_info_type",
        "update_stored_info_type",
        "get_stored_info_type",
        "list_stored_info_types",
        "delete_stored_info_type",
        "hybrid_inspect_dlp_job",
        "finish_dlp_job",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_dlp_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dlp_v2.services.dlp_service.transports.DlpServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DlpServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_dlp_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dlp_v2.services.dlp_service.transports.DlpServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DlpServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_dlp_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dlp_v2.services.dlp_service.transports.DlpServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DlpServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_dlp_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DlpServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_dlp_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DlpServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
def test_dlp_service_transport_auth_adc(transport_class):
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
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_dlp_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.DlpServiceGrpcTransport, grpc_helpers),
        (transports.DlpServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_dlp_service_transport_create_channel(transport_class, grpc_helpers):
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
            "dlp.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dlp.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport],
)
def test_dlp_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_dlp_service_host_no_port():
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint="dlp.googleapis.com"),
    )
    assert client.transport._host == "dlp.googleapis.com:443"


def test_dlp_service_host_with_port():
    client = DlpServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dlp.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dlp.googleapis.com:8000"


def test_dlp_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DlpServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_dlp_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DlpServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport],
)
def test_dlp_service_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.DlpServiceGrpcTransport, transports.DlpServiceGrpcAsyncIOTransport],
)
def test_dlp_service_transport_channel_mtls_with_adc(transport_class):
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


def test_deidentify_template_path():
    organization = "squid"
    deidentify_template = "clam"
    expected = "organizations/{organization}/deidentifyTemplates/{deidentify_template}".format(
        organization=organization, deidentify_template=deidentify_template,
    )
    actual = DlpServiceClient.deidentify_template_path(
        organization, deidentify_template
    )
    assert expected == actual


def test_parse_deidentify_template_path():
    expected = {
        "organization": "whelk",
        "deidentify_template": "octopus",
    }
    path = DlpServiceClient.deidentify_template_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_deidentify_template_path(path)
    assert expected == actual


def test_dlp_content_path():
    project = "oyster"
    expected = "projects/{project}/dlpContent".format(project=project,)
    actual = DlpServiceClient.dlp_content_path(project)
    assert expected == actual


def test_parse_dlp_content_path():
    expected = {
        "project": "nudibranch",
    }
    path = DlpServiceClient.dlp_content_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_dlp_content_path(path)
    assert expected == actual


def test_dlp_job_path():
    project = "cuttlefish"
    dlp_job = "mussel"
    expected = "projects/{project}/dlpJobs/{dlp_job}".format(
        project=project, dlp_job=dlp_job,
    )
    actual = DlpServiceClient.dlp_job_path(project, dlp_job)
    assert expected == actual


def test_parse_dlp_job_path():
    expected = {
        "project": "winkle",
        "dlp_job": "nautilus",
    }
    path = DlpServiceClient.dlp_job_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_dlp_job_path(path)
    assert expected == actual


def test_finding_path():
    project = "scallop"
    location = "abalone"
    finding = "squid"
    expected = "projects/{project}/locations/{location}/findings/{finding}".format(
        project=project, location=location, finding=finding,
    )
    actual = DlpServiceClient.finding_path(project, location, finding)
    assert expected == actual


def test_parse_finding_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "finding": "octopus",
    }
    path = DlpServiceClient.finding_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_finding_path(path)
    assert expected == actual


def test_inspect_template_path():
    organization = "oyster"
    inspect_template = "nudibranch"
    expected = "organizations/{organization}/inspectTemplates/{inspect_template}".format(
        organization=organization, inspect_template=inspect_template,
    )
    actual = DlpServiceClient.inspect_template_path(organization, inspect_template)
    assert expected == actual


def test_parse_inspect_template_path():
    expected = {
        "organization": "cuttlefish",
        "inspect_template": "mussel",
    }
    path = DlpServiceClient.inspect_template_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_inspect_template_path(path)
    assert expected == actual


def test_job_trigger_path():
    project = "winkle"
    job_trigger = "nautilus"
    expected = "projects/{project}/jobTriggers/{job_trigger}".format(
        project=project, job_trigger=job_trigger,
    )
    actual = DlpServiceClient.job_trigger_path(project, job_trigger)
    assert expected == actual


def test_parse_job_trigger_path():
    expected = {
        "project": "scallop",
        "job_trigger": "abalone",
    }
    path = DlpServiceClient.job_trigger_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_job_trigger_path(path)
    assert expected == actual


def test_stored_info_type_path():
    organization = "squid"
    stored_info_type = "clam"
    expected = "organizations/{organization}/storedInfoTypes/{stored_info_type}".format(
        organization=organization, stored_info_type=stored_info_type,
    )
    actual = DlpServiceClient.stored_info_type_path(organization, stored_info_type)
    assert expected == actual


def test_parse_stored_info_type_path():
    expected = {
        "organization": "whelk",
        "stored_info_type": "octopus",
    }
    path = DlpServiceClient.stored_info_type_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_stored_info_type_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DlpServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = DlpServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder,)
    actual = DlpServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = DlpServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = DlpServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = DlpServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project,)
    actual = DlpServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = DlpServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = DlpServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = DlpServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DlpServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DlpServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DlpServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DlpServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DlpServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
