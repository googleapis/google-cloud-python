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
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.monitoring_v3.services.service_monitoring_service import (
    ServiceMonitoringServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.service_monitoring_service import (
    ServiceMonitoringServiceClient,
)
from google.cloud.monitoring_v3.services.service_monitoring_service import pagers
from google.cloud.monitoring_v3.services.service_monitoring_service import transports
from google.cloud.monitoring_v3.types import service
from google.cloud.monitoring_v3.types import service as gm_service
from google.cloud.monitoring_v3.types import service_service
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import calendar_period_pb2 as calendar_period  # type: ignore
from google.type import calendar_period_pb2 as gt_calendar_period  # type: ignore


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

    assert ServiceMonitoringServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ServiceMonitoringServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ServiceMonitoringServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ServiceMonitoringServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ServiceMonitoringServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ServiceMonitoringServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [ServiceMonitoringServiceClient, ServiceMonitoringServiceAsyncClient],
)
def test_service_monitoring_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "monitoring.googleapis.com:443"


def test_service_monitoring_service_client_get_transport_class():
    transport = ServiceMonitoringServiceClient.get_transport_class()
    assert transport == transports.ServiceMonitoringServiceGrpcTransport

    transport = ServiceMonitoringServiceClient.get_transport_class("grpc")
    assert transport == transports.ServiceMonitoringServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ServiceMonitoringServiceClient,
            transports.ServiceMonitoringServiceGrpcTransport,
            "grpc",
        ),
        (
            ServiceMonitoringServiceAsyncClient,
            transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ServiceMonitoringServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceMonitoringServiceClient),
)
@mock.patch.object(
    ServiceMonitoringServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceMonitoringServiceAsyncClient),
)
def test_service_monitoring_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        ServiceMonitoringServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        ServiceMonitoringServiceClient, "get_transport_class"
    ) as gtc:
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
            ServiceMonitoringServiceClient,
            transports.ServiceMonitoringServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ServiceMonitoringServiceAsyncClient,
            transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ServiceMonitoringServiceClient,
            transports.ServiceMonitoringServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ServiceMonitoringServiceAsyncClient,
            transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ServiceMonitoringServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceMonitoringServiceClient),
)
@mock.patch.object(
    ServiceMonitoringServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceMonitoringServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_service_monitoring_service_client_mtls_env_auto(
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
        (
            ServiceMonitoringServiceClient,
            transports.ServiceMonitoringServiceGrpcTransport,
            "grpc",
        ),
        (
            ServiceMonitoringServiceAsyncClient,
            transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_service_monitoring_service_client_client_options_scopes(
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
        (
            ServiceMonitoringServiceClient,
            transports.ServiceMonitoringServiceGrpcTransport,
            "grpc",
        ),
        (
            ServiceMonitoringServiceAsyncClient,
            transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_service_monitoring_service_client_client_options_credentials_file(
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


def test_service_monitoring_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.monitoring_v3.services.service_monitoring_service.transports.ServiceMonitoringServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ServiceMonitoringServiceClient(
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


def test_create_service(
    transport: str = "grpc", request_type=service_service.CreateServiceRequest
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service(
            name="name_value", display_name="display_name_value", custom=None,
        )

        response = client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gm_service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_create_service_from_dict():
    test_create_service(request_type=dict)


@pytest.mark.asyncio
async def test_create_service_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.CreateServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gm_service.Service(name="name_value", display_name="display_name_value",)
        )

        response = await client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gm_service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_create_service_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.CreateServiceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        call.return_value = gm_service.Service()

        client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_service_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.CreateServiceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gm_service.Service())

        await client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_service_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service(
            parent="parent_value", service=gm_service.Service(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].service == gm_service.Service(name="name_value")


def test_create_service_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            service_service.CreateServiceRequest(),
            parent="parent_value",
            service=gm_service.Service(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_service_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gm_service.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service(
            parent="parent_value", service=gm_service.Service(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].service == gm_service.Service(name="name_value")


@pytest.mark.asyncio
async def test_create_service_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service(
            service_service.CreateServiceRequest(),
            parent="parent_value",
            service=gm_service.Service(name="name_value"),
        )


def test_get_service(
    transport: str = "grpc", request_type=service_service.GetServiceRequest
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.Service(
            name="name_value", display_name="display_name_value", custom=None,
        )

        response = client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_get_service_from_dict():
    test_get_service(request_type=dict)


@pytest.mark.asyncio
async def test_get_service_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.GetServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.Service(name="name_value", display_name="display_name_value",)
        )

        response = await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_get_service_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.GetServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        call.return_value = service.Service()

        client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_service_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.GetServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(service.Service())

        await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_service_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_service_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(
            service_service.GetServiceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_service_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(service.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_service_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service(
            service_service.GetServiceRequest(), name="name_value",
        )


def test_list_services(
    transport: str = "grpc", request_type=service_service.ListServicesRequest
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServicesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_services_from_dict():
    test_list_services(request_type=dict)


@pytest.mark.asyncio
async def test_list_services_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.ListServicesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServicesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_services_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.ListServicesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        call.return_value = service_service.ListServicesResponse()

        client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_services_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.ListServicesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_services), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServicesResponse()
        )

        await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_services_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServicesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_services(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_services_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            service_service.ListServicesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_services_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_services), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_services(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_services_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_services(
            service_service.ListServicesRequest(), parent="parent_value",
        )


def test_list_services_pager():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service(),],
                next_page_token="abc",
            ),
            service_service.ListServicesResponse(services=[], next_page_token="def",),
            service_service.ListServicesResponse(
                services=[service.Service(),], next_page_token="ghi",
            ),
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_services(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service.Service) for i in results)


def test_list_services_pages():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service(),],
                next_page_token="abc",
            ),
            service_service.ListServicesResponse(services=[], next_page_token="def",),
            service_service.ListServicesResponse(
                services=[service.Service(),], next_page_token="ghi",
            ),
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_services_async_pager():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_services),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service(),],
                next_page_token="abc",
            ),
            service_service.ListServicesResponse(services=[], next_page_token="def",),
            service_service.ListServicesResponse(
                services=[service.Service(),], next_page_token="ghi",
            ),
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_services(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service.Service) for i in responses)


@pytest.mark.asyncio
async def test_list_services_async_pages():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_services),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service(),],
                next_page_token="abc",
            ),
            service_service.ListServicesResponse(services=[], next_page_token="def",),
            service_service.ListServicesResponse(
                services=[service.Service(),], next_page_token="ghi",
            ),
            service_service.ListServicesResponse(
                services=[service.Service(), service.Service(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_services(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_service(
    transport: str = "grpc", request_type=service_service.UpdateServiceRequest
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service(
            name="name_value", display_name="display_name_value", custom=None,
        )

        response = client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.UpdateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gm_service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_update_service_from_dict():
    test_update_service(request_type=dict)


@pytest.mark.asyncio
async def test_update_service_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.UpdateServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gm_service.Service(name="name_value", display_name="display_name_value",)
        )

        response = await client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gm_service.Service)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"


def test_update_service_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.UpdateServiceRequest()
    request.service.name = "service.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        call.return_value = gm_service.Service()

        client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service.name=service.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_service_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.UpdateServiceRequest()
    request.service.name = "service.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gm_service.Service())

        await client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service.name=service.name/value",) in kw[
        "metadata"
    ]


def test_update_service_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_service(service=gm_service.Service(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].service == gm_service.Service(name="name_value")


def test_update_service_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service(
            service_service.UpdateServiceRequest(),
            service=gm_service.Service(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_service_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gm_service.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gm_service.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_service(
            service=gm_service.Service(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].service == gm_service.Service(name="name_value")


@pytest.mark.asyncio
async def test_update_service_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_service(
            service_service.UpdateServiceRequest(),
            service=gm_service.Service(name="name_value"),
        )


def test_delete_service(
    transport: str = "grpc", request_type=service_service.DeleteServiceRequest
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_service_from_dict():
    test_delete_service(request_type=dict)


@pytest.mark.asyncio
async def test_delete_service_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.DeleteServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_service_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.DeleteServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        call.return_value = None

        client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_service_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.DeleteServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_service_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_service_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            service_service.DeleteServiceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_service_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service(
            service_service.DeleteServiceRequest(), name="name_value",
        )


def test_create_service_level_objective(
    transport: str = "grpc",
    request_type=service_service.CreateServiceLevelObjectiveRequest,
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective(
            name="name_value",
            display_name="display_name_value",
            goal=0.419,
            rolling_period=duration.Duration(seconds=751),
        )

        response = client.create_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.CreateServiceLevelObjectiveRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_create_service_level_objective_from_dict():
    test_create_service_level_objective(request_type=dict)


@pytest.mark.asyncio
async def test_create_service_level_objective_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.CreateServiceLevelObjectiveRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective(
                name="name_value", display_name="display_name_value", goal=0.419,
            )
        )

        response = await client.create_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_create_service_level_objective_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.CreateServiceLevelObjectiveRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_service_level_objective), "__call__"
    ) as call:
        call.return_value = service.ServiceLevelObjective()

        client.create_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_service_level_objective_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.CreateServiceLevelObjectiveRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service_level_objective), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )

        await client.create_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_service_level_objective_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service_level_objective(
            parent="parent_value",
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].service_level_objective == service.ServiceLevelObjective(
            name="name_value"
        )


def test_create_service_level_objective_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service_level_objective(
            service_service.CreateServiceLevelObjectiveRequest(),
            parent="parent_value",
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_service_level_objective_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service_level_objective(
            parent="parent_value",
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].service_level_objective == service.ServiceLevelObjective(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_service_level_objective_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service_level_objective(
            service_service.CreateServiceLevelObjectiveRequest(),
            parent="parent_value",
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )


def test_get_service_level_objective(
    transport: str = "grpc",
    request_type=service_service.GetServiceLevelObjectiveRequest,
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective(
            name="name_value",
            display_name="display_name_value",
            goal=0.419,
            rolling_period=duration.Duration(seconds=751),
        )

        response = client.get_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.GetServiceLevelObjectiveRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_get_service_level_objective_from_dict():
    test_get_service_level_objective(request_type=dict)


@pytest.mark.asyncio
async def test_get_service_level_objective_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.GetServiceLevelObjectiveRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective(
                name="name_value", display_name="display_name_value", goal=0.419,
            )
        )

        response = await client.get_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_get_service_level_objective_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.GetServiceLevelObjectiveRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_service_level_objective), "__call__"
    ) as call:
        call.return_value = service.ServiceLevelObjective()

        client.get_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_service_level_objective_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.GetServiceLevelObjectiveRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service_level_objective), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )

        await client.get_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_service_level_objective_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service_level_objective(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_service_level_objective_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_level_objective(
            service_service.GetServiceLevelObjectiveRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_service_level_objective_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service_level_objective(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_service_level_objective_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service_level_objective(
            service_service.GetServiceLevelObjectiveRequest(), name="name_value",
        )


def test_list_service_level_objectives(
    transport: str = "grpc",
    request_type=service_service.ListServiceLevelObjectivesRequest,
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServiceLevelObjectivesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_service_level_objectives(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.ListServiceLevelObjectivesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceLevelObjectivesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_service_level_objectives_from_dict():
    test_list_service_level_objectives(request_type=dict)


@pytest.mark.asyncio
async def test_list_service_level_objectives_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.ListServiceLevelObjectivesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServiceLevelObjectivesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_service_level_objectives(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceLevelObjectivesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_service_level_objectives_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.ListServiceLevelObjectivesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_service_level_objectives), "__call__"
    ) as call:
        call.return_value = service_service.ListServiceLevelObjectivesResponse()

        client.list_service_level_objectives(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_service_level_objectives_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.ListServiceLevelObjectivesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_service_level_objectives), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServiceLevelObjectivesResponse()
        )

        await client.list_service_level_objectives(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_service_level_objectives_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServiceLevelObjectivesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_service_level_objectives(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_service_level_objectives_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_service_level_objectives(
            service_service.ListServiceLevelObjectivesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_service_level_objectives_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_service.ListServiceLevelObjectivesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_service.ListServiceLevelObjectivesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_service_level_objectives(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_service_level_objectives_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_service_level_objectives(
            service_service.ListServiceLevelObjectivesRequest(), parent="parent_value",
        )


def test_list_service_level_objectives_pager():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
                next_page_token="abc",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[], next_page_token="def",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[service.ServiceLevelObjective(),],
                next_page_token="ghi",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_service_level_objectives(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service.ServiceLevelObjective) for i in results)


def test_list_service_level_objectives_pages():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_service_level_objectives), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
                next_page_token="abc",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[], next_page_token="def",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[service.ServiceLevelObjective(),],
                next_page_token="ghi",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_service_level_objectives(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_service_level_objectives_async_pager():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_service_level_objectives),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
                next_page_token="abc",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[], next_page_token="def",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[service.ServiceLevelObjective(),],
                next_page_token="ghi",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_service_level_objectives(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service.ServiceLevelObjective) for i in responses)


@pytest.mark.asyncio
async def test_list_service_level_objectives_async_pages():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_service_level_objectives),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
                next_page_token="abc",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[], next_page_token="def",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[service.ServiceLevelObjective(),],
                next_page_token="ghi",
            ),
            service_service.ListServiceLevelObjectivesResponse(
                service_level_objectives=[
                    service.ServiceLevelObjective(),
                    service.ServiceLevelObjective(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_service_level_objectives(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_service_level_objective(
    transport: str = "grpc",
    request_type=service_service.UpdateServiceLevelObjectiveRequest,
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective(
            name="name_value",
            display_name="display_name_value",
            goal=0.419,
            rolling_period=duration.Duration(seconds=751),
        )

        response = client.update_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.UpdateServiceLevelObjectiveRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_update_service_level_objective_from_dict():
    test_update_service_level_objective(request_type=dict)


@pytest.mark.asyncio
async def test_update_service_level_objective_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.UpdateServiceLevelObjectiveRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective(
                name="name_value", display_name="display_name_value", goal=0.419,
            )
        )

        response = await client.update_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.ServiceLevelObjective)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert math.isclose(response.goal, 0.419, rel_tol=1e-6)


def test_update_service_level_objective_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.UpdateServiceLevelObjectiveRequest()
    request.service_level_objective.name = "service_level_objective.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_service_level_objective), "__call__"
    ) as call:
        call.return_value = service.ServiceLevelObjective()

        client.update_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service_level_objective.name=service_level_objective.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_service_level_objective_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.UpdateServiceLevelObjectiveRequest()
    request.service_level_objective.name = "service_level_objective.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service_level_objective), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )

        await client.update_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service_level_objective.name=service_level_objective.name/value",
    ) in kw["metadata"]


def test_update_service_level_objective_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_service_level_objective(
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].service_level_objective == service.ServiceLevelObjective(
            name="name_value"
        )


def test_update_service_level_objective_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service_level_objective(
            service_service.UpdateServiceLevelObjectiveRequest(),
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_service_level_objective_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ServiceLevelObjective()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ServiceLevelObjective()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_service_level_objective(
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].service_level_objective == service.ServiceLevelObjective(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_update_service_level_objective_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_service_level_objective(
            service_service.UpdateServiceLevelObjectiveRequest(),
            service_level_objective=service.ServiceLevelObjective(name="name_value"),
        )


def test_delete_service_level_objective(
    transport: str = "grpc",
    request_type=service_service.DeleteServiceLevelObjectiveRequest,
):
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == service_service.DeleteServiceLevelObjectiveRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_service_level_objective_from_dict():
    test_delete_service_level_objective(request_type=dict)


@pytest.mark.asyncio
async def test_delete_service_level_objective_async(transport: str = "grpc_asyncio"):
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service_service.DeleteServiceLevelObjectiveRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_service_level_objective_field_headers():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.DeleteServiceLevelObjectiveRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_service_level_objective), "__call__"
    ) as call:
        call.return_value = None

        client.delete_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_service_level_objective_field_headers_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service_service.DeleteServiceLevelObjectiveRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service_level_objective), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_service_level_objective(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_service_level_objective_flattened():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service_level_objective(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_service_level_objective_flattened_error():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service_level_objective(
            service_service.DeleteServiceLevelObjectiveRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_level_objective_flattened_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_service_level_objective), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_service_level_objective(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_service_level_objective_flattened_error_async():
    client = ServiceMonitoringServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service_level_objective(
            service_service.DeleteServiceLevelObjectiveRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceMonitoringServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceMonitoringServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceMonitoringServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ServiceMonitoringServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ServiceMonitoringServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceMonitoringServiceGrpcTransport,
        transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
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
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport, transports.ServiceMonitoringServiceGrpcTransport,
    )


def test_service_monitoring_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ServiceMonitoringServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_service_monitoring_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.monitoring_v3.services.service_monitoring_service.transports.ServiceMonitoringServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ServiceMonitoringServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_service",
        "get_service",
        "list_services",
        "update_service",
        "delete_service",
        "create_service_level_objective",
        "get_service_level_objective",
        "list_service_level_objectives",
        "update_service_level_objective",
        "delete_service_level_objective",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_service_monitoring_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.monitoring_v3.services.service_monitoring_service.transports.ServiceMonitoringServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ServiceMonitoringServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_service_monitoring_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.monitoring_v3.services.service_monitoring_service.transports.ServiceMonitoringServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ServiceMonitoringServiceTransport()
        adc.assert_called_once()


def test_service_monitoring_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ServiceMonitoringServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id=None,
        )


def test_service_monitoring_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ServiceMonitoringServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_service_monitoring_service_host_no_port():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com"
        ),
    )
    assert client._transport._host == "monitoring.googleapis.com:443"


def test_service_monitoring_service_host_with_port():
    client = ServiceMonitoringServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "monitoring.googleapis.com:8000"


def test_service_monitoring_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ServiceMonitoringServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_service_monitoring_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.ServiceMonitoringServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceMonitoringServiceGrpcTransport,
        transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
    ],
)
def test_service_monitoring_service_transport_channel_mtls_with_client_cert_source(
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
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/monitoring.read",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceMonitoringServiceGrpcTransport,
        transports.ServiceMonitoringServiceGrpcAsyncIOTransport,
    ],
)
def test_service_monitoring_service_transport_channel_mtls_with_adc(transport_class):
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
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/monitoring.read",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_service_path():
    project = "squid"
    service = "clam"

    expected = "projects/{project}/services/{service}".format(
        project=project, service=service,
    )
    actual = ServiceMonitoringServiceClient.service_path(project, service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "whelk",
        "service": "octopus",
    }
    path = ServiceMonitoringServiceClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_service_path(path)
    assert expected == actual


def test_service_level_objective_path():
    project = "oyster"
    service = "nudibranch"
    service_level_objective = "cuttlefish"

    expected = "projects/{project}/services/{service}/serviceLevelObjectives/{service_level_objective}".format(
        project=project,
        service=service,
        service_level_objective=service_level_objective,
    )
    actual = ServiceMonitoringServiceClient.service_level_objective_path(
        project, service, service_level_objective
    )
    assert expected == actual


def test_parse_service_level_objective_path():
    expected = {
        "project": "mussel",
        "service": "winkle",
        "service_level_objective": "nautilus",
    }
    path = ServiceMonitoringServiceClient.service_level_objective_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_service_level_objective_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"

    expected = "projects/{project}".format(project=project,)
    actual = ServiceMonitoringServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = ServiceMonitoringServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = ServiceMonitoringServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = ServiceMonitoringServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = ServiceMonitoringServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = ServiceMonitoringServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ServiceMonitoringServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = ServiceMonitoringServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ServiceMonitoringServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = ServiceMonitoringServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceMonitoringServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ServiceMonitoringServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ServiceMonitoringServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ServiceMonitoringServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ServiceMonitoringServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
