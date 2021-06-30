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


from google.api import auth_pb2  # type: ignore
from google.api import backend_pb2  # type: ignore
from google.api import billing_pb2  # type: ignore
from google.api import context_pb2  # type: ignore
from google.api import control_pb2  # type: ignore
from google.api import documentation_pb2  # type: ignore
from google.api import endpoint_pb2  # type: ignore
from google.api import http_pb2  # type: ignore
from google.api import label_pb2  # type: ignore
from google.api import launch_stage_pb2  # type: ignore
from google.api import log_pb2  # type: ignore
from google.api import logging_pb2  # type: ignore
from google.api import metric_pb2  # type: ignore
from google.api import monitored_resource_pb2  # type: ignore
from google.api import monitoring_pb2  # type: ignore
from google.api import quota_pb2  # type: ignore
from google.api import service_pb2  # type: ignore
from google.api import source_info_pb2  # type: ignore
from google.api import system_parameter_pb2  # type: ignore
from google.api import usage_pb2  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.servicemanagement_v1.services.service_manager import (
    ServiceManagerAsyncClient,
)
from google.cloud.servicemanagement_v1.services.service_manager import (
    ServiceManagerClient,
)
from google.cloud.servicemanagement_v1.services.service_manager import pagers
from google.cloud.servicemanagement_v1.services.service_manager import transports
from google.cloud.servicemanagement_v1.services.service_manager.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.servicemanagement_v1.types import resources
from google.cloud.servicemanagement_v1.types import servicemanager
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import api_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import source_context_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import type_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
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

    assert ServiceManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        ServiceManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ServiceManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ServiceManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ServiceManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ServiceManagerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ServiceManagerClient, ServiceManagerAsyncClient,]
)
def test_service_manager_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "servicemanagement.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [ServiceManagerClient, ServiceManagerAsyncClient,]
)
def test_service_manager_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ServiceManagerGrpcTransport, "grpc"),
        (transports.ServiceManagerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_service_manager_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [ServiceManagerClient, ServiceManagerAsyncClient,]
)
def test_service_manager_client_from_service_account_file(client_class):
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

        assert client.transport._host == "servicemanagement.googleapis.com:443"


def test_service_manager_client_get_transport_class():
    transport = ServiceManagerClient.get_transport_class()
    available_transports = [
        transports.ServiceManagerGrpcTransport,
    ]
    assert transport in available_transports

    transport = ServiceManagerClient.get_transport_class("grpc")
    assert transport == transports.ServiceManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ServiceManagerClient, transports.ServiceManagerGrpcTransport, "grpc"),
        (
            ServiceManagerAsyncClient,
            transports.ServiceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ServiceManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceManagerClient),
)
@mock.patch.object(
    ServiceManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceManagerAsyncClient),
)
def test_service_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ServiceManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ServiceManagerClient, "get_transport_class") as gtc:
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
        (ServiceManagerClient, transports.ServiceManagerGrpcTransport, "grpc", "true"),
        (
            ServiceManagerAsyncClient,
            transports.ServiceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ServiceManagerClient, transports.ServiceManagerGrpcTransport, "grpc", "false"),
        (
            ServiceManagerAsyncClient,
            transports.ServiceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ServiceManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceManagerClient),
)
@mock.patch.object(
    ServiceManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ServiceManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_service_manager_client_mtls_env_auto(
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
        (ServiceManagerClient, transports.ServiceManagerGrpcTransport, "grpc"),
        (
            ServiceManagerAsyncClient,
            transports.ServiceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_service_manager_client_client_options_scopes(
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
        (ServiceManagerClient, transports.ServiceManagerGrpcTransport, "grpc"),
        (
            ServiceManagerAsyncClient,
            transports.ServiceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_service_manager_client_client_options_credentials_file(
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


def test_service_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.servicemanagement_v1.services.service_manager.transports.ServiceManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ServiceManagerClient(
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
        )


def test_list_services(
    transport: str = "grpc", request_type=servicemanager.ListServicesRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServicesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_services_from_dict():
    test_list_services(request_type=dict)


def test_list_services_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        client.list_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServicesRequest()


@pytest.mark.asyncio
async def test_list_services_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.ListServicesRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_services_async_from_dict():
    await test_list_services_async(request_type=dict)


def test_list_services_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServicesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_services(
            producer_project_id="producer_project_id_value",
            consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].producer_project_id == "producer_project_id_value"
        assert args[0].consumer_id == "consumer_id_value"


def test_list_services_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            servicemanager.ListServicesRequest(),
            producer_project_id="producer_project_id_value",
            consumer_id="consumer_id_value",
        )


@pytest.mark.asyncio
async def test_list_services_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_services(
            producer_project_id="producer_project_id_value",
            consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].producer_project_id == "producer_project_id_value"
        assert args[0].consumer_id == "consumer_id_value"


@pytest.mark.asyncio
async def test_list_services_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_services(
            servicemanager.ListServicesRequest(),
            producer_project_id="producer_project_id_value",
            consumer_id="consumer_id_value",
        )


def test_list_services_pager():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServicesResponse(
                services=[
                    resources.ManagedService(),
                    resources.ManagedService(),
                    resources.ManagedService(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServicesResponse(services=[], next_page_token="def",),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(),], next_page_token="ghi",
            ),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(), resources.ManagedService(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_services(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.ManagedService) for i in results)


def test_list_services_pages():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServicesResponse(
                services=[
                    resources.ManagedService(),
                    resources.ManagedService(),
                    resources.ManagedService(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServicesResponse(services=[], next_page_token="def",),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(),], next_page_token="ghi",
            ),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(), resources.ManagedService(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_services_async_pager():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServicesResponse(
                services=[
                    resources.ManagedService(),
                    resources.ManagedService(),
                    resources.ManagedService(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServicesResponse(services=[], next_page_token="def",),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(),], next_page_token="ghi",
            ),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(), resources.ManagedService(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_services(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ManagedService) for i in responses)


@pytest.mark.asyncio
async def test_list_services_async_pages():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServicesResponse(
                services=[
                    resources.ManagedService(),
                    resources.ManagedService(),
                    resources.ManagedService(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServicesResponse(services=[], next_page_token="def",),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(),], next_page_token="ghi",
            ),
            servicemanager.ListServicesResponse(
                services=[resources.ManagedService(), resources.ManagedService(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_services(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_service(
    transport: str = "grpc", request_type=servicemanager.GetServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ManagedService(
            service_name="service_name_value",
            producer_project_id="producer_project_id_value",
        )
        response = client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ManagedService)
    assert response.service_name == "service_name_value"
    assert response.producer_project_id == "producer_project_id_value"


def test_get_service_from_dict():
    test_get_service(request_type=dict)


def test_get_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        client.get_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRequest()


@pytest.mark.asyncio
async def test_get_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.GetServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ManagedService(
                service_name="service_name_value",
                producer_project_id="producer_project_id_value",
            )
        )
        response = await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ManagedService)
    assert response.service_name == "service_name_value"
    assert response.producer_project_id == "producer_project_id_value"


@pytest.mark.asyncio
async def test_get_service_async_from_dict():
    await test_get_service_async(request_type=dict)


def test_get_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ManagedService()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


def test_get_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(
            servicemanager.GetServiceRequest(), service_name="service_name_value",
        )


@pytest.mark.asyncio
async def test_get_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ManagedService()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ManagedService()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


@pytest.mark.asyncio
async def test_get_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service(
            servicemanager.GetServiceRequest(), service_name="service_name_value",
        )


def test_create_service(
    transport: str = "grpc", request_type=servicemanager.CreateServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_service_from_dict():
    test_create_service(request_type=dict)


def test_create_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        client.create_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRequest()


@pytest.mark.asyncio
async def test_create_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.CreateServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_service_async_from_dict():
    await test_create_service_async(request_type=dict)


def test_create_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service(
            service=resources.ManagedService(service_name="service_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service == resources.ManagedService(
            service_name="service_name_value"
        )


def test_create_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            servicemanager.CreateServiceRequest(),
            service=resources.ManagedService(service_name="service_name_value"),
        )


@pytest.mark.asyncio
async def test_create_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service(
            service=resources.ManagedService(service_name="service_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service == resources.ManagedService(
            service_name="service_name_value"
        )


@pytest.mark.asyncio
async def test_create_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service(
            servicemanager.CreateServiceRequest(),
            service=resources.ManagedService(service_name="service_name_value"),
        )


def test_delete_service(
    transport: str = "grpc", request_type=servicemanager.DeleteServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_service_from_dict():
    test_delete_service(request_type=dict)


def test_delete_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        client.delete_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DeleteServiceRequest()


@pytest.mark.asyncio
async def test_delete_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.DeleteServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_service_async_from_dict():
    await test_delete_service_async(request_type=dict)


def test_delete_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


def test_delete_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            servicemanager.DeleteServiceRequest(), service_name="service_name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


@pytest.mark.asyncio
async def test_delete_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service(
            servicemanager.DeleteServiceRequest(), service_name="service_name_value",
        )


def test_undelete_service(
    transport: str = "grpc", request_type=servicemanager.UndeleteServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undelete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undelete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.UndeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undelete_service_from_dict():
    test_undelete_service(request_type=dict)


def test_undelete_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undelete_service), "__call__") as call:
        client.undelete_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.UndeleteServiceRequest()


@pytest.mark.asyncio
async def test_undelete_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.UndeleteServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undelete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undelete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.UndeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undelete_service_async_from_dict():
    await test_undelete_service_async(request_type=dict)


def test_undelete_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undelete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undelete_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


def test_undelete_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_service(
            servicemanager.UndeleteServiceRequest(), service_name="service_name_value",
        )


@pytest.mark.asyncio
async def test_undelete_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undelete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undelete_service(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


@pytest.mark.asyncio
async def test_undelete_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undelete_service(
            servicemanager.UndeleteServiceRequest(), service_name="service_name_value",
        )


def test_list_service_configs(
    transport: str = "grpc", request_type=servicemanager.ListServiceConfigsRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceConfigsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_service_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_service_configs_from_dict():
    test_list_service_configs(request_type=dict)


def test_list_service_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        client.list_service_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceConfigsRequest()


@pytest.mark.asyncio
async def test_list_service_configs_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.ListServiceConfigsRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServiceConfigsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_service_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_service_configs_async_from_dict():
    await test_list_service_configs_async(request_type=dict)


def test_list_service_configs_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_service_configs(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


def test_list_service_configs_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_service_configs(
            servicemanager.ListServiceConfigsRequest(),
            service_name="service_name_value",
        )


@pytest.mark.asyncio
async def test_list_service_configs_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServiceConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_service_configs(service_name="service_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"


@pytest.mark.asyncio
async def test_list_service_configs_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_service_configs(
            servicemanager.ListServiceConfigsRequest(),
            service_name="service_name_value",
        )


def test_list_service_configs_pager():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceConfigsResponse(
                service_configs=[
                    service_pb2.Service(),
                    service_pb2.Service(),
                    service_pb2.Service(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[], next_page_token="def",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(), service_pb2.Service(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_service_configs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, service_pb2.Service) for i in results)


def test_list_service_configs_pages():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceConfigsResponse(
                service_configs=[
                    service_pb2.Service(),
                    service_pb2.Service(),
                    service_pb2.Service(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[], next_page_token="def",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(), service_pb2.Service(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_service_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_service_configs_async_pager():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceConfigsResponse(
                service_configs=[
                    service_pb2.Service(),
                    service_pb2.Service(),
                    service_pb2.Service(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[], next_page_token="def",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(), service_pb2.Service(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_service_configs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, service_pb2.Service) for i in responses)


@pytest.mark.asyncio
async def test_list_service_configs_async_pages():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceConfigsResponse(
                service_configs=[
                    service_pb2.Service(),
                    service_pb2.Service(),
                    service_pb2.Service(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[], next_page_token="def",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceConfigsResponse(
                service_configs=[service_pb2.Service(), service_pb2.Service(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_service_configs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_service_config(
    transport: str = "grpc", request_type=servicemanager.GetServiceConfigRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service(
            name="name_value",
            title="title_value",
            producer_project_id="producer_project_id_value",
            id="id_value",
        )
        response = client.get_service_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_pb2.Service)
    assert response.name == "name_value"
    assert response.title == "title_value"
    assert response.producer_project_id == "producer_project_id_value"
    assert response.id == "id_value"


def test_get_service_config_from_dict():
    test_get_service_config(request_type=dict)


def test_get_service_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_config), "__call__"
    ) as call:
        client.get_service_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceConfigRequest()


@pytest.mark.asyncio
async def test_get_service_config_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.GetServiceConfigRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_pb2.Service(
                name="name_value",
                title="title_value",
                producer_project_id="producer_project_id_value",
                id="id_value",
            )
        )
        response = await client.get_service_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_pb2.Service)
    assert response.name == "name_value"
    assert response.title == "title_value"
    assert response.producer_project_id == "producer_project_id_value"
    assert response.id == "id_value"


@pytest.mark.asyncio
async def test_get_service_config_async_from_dict():
    await test_get_service_config_async(request_type=dict)


def test_get_service_config_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service_config(
            service_name="service_name_value",
            config_id="config_id_value",
            view=servicemanager.GetServiceConfigRequest.ConfigView.FULL,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].config_id == "config_id_value"
        assert args[0].view == servicemanager.GetServiceConfigRequest.ConfigView.FULL


def test_get_service_config_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_config(
            servicemanager.GetServiceConfigRequest(),
            service_name="service_name_value",
            config_id="config_id_value",
            view=servicemanager.GetServiceConfigRequest.ConfigView.FULL,
        )


@pytest.mark.asyncio
async def test_get_service_config_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(service_pb2.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service_config(
            service_name="service_name_value",
            config_id="config_id_value",
            view=servicemanager.GetServiceConfigRequest.ConfigView.FULL,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].config_id == "config_id_value"
        assert args[0].view == servicemanager.GetServiceConfigRequest.ConfigView.FULL


@pytest.mark.asyncio
async def test_get_service_config_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service_config(
            servicemanager.GetServiceConfigRequest(),
            service_name="service_name_value",
            config_id="config_id_value",
            view=servicemanager.GetServiceConfigRequest.ConfigView.FULL,
        )


def test_create_service_config(
    transport: str = "grpc", request_type=servicemanager.CreateServiceConfigRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service(
            name="name_value",
            title="title_value",
            producer_project_id="producer_project_id_value",
            id="id_value",
        )
        response = client.create_service_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_pb2.Service)
    assert response.name == "name_value"
    assert response.title == "title_value"
    assert response.producer_project_id == "producer_project_id_value"
    assert response.id == "id_value"


def test_create_service_config_from_dict():
    test_create_service_config(request_type=dict)


def test_create_service_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_config), "__call__"
    ) as call:
        client.create_service_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceConfigRequest()


@pytest.mark.asyncio
async def test_create_service_config_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.CreateServiceConfigRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service_pb2.Service(
                name="name_value",
                title="title_value",
                producer_project_id="producer_project_id_value",
                id="id_value",
            )
        )
        response = await client.create_service_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service_pb2.Service)
    assert response.name == "name_value"
    assert response.title == "title_value"
    assert response.producer_project_id == "producer_project_id_value"
    assert response.id == "id_value"


@pytest.mark.asyncio
async def test_create_service_config_async_from_dict():
    await test_create_service_config_async(request_type=dict)


def test_create_service_config_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service_config(
            service_name="service_name_value",
            service_config=service_pb2.Service(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].service_config == service_pb2.Service(name="name_value")


def test_create_service_config_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service_config(
            servicemanager.CreateServiceConfigRequest(),
            service_name="service_name_value",
            service_config=service_pb2.Service(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_service_config_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service_pb2.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(service_pb2.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service_config(
            service_name="service_name_value",
            service_config=service_pb2.Service(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].service_config == service_pb2.Service(name="name_value")


@pytest.mark.asyncio
async def test_create_service_config_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service_config(
            servicemanager.CreateServiceConfigRequest(),
            service_name="service_name_value",
            service_config=service_pb2.Service(name="name_value"),
        )


def test_submit_config_source(
    transport: str = "grpc", request_type=servicemanager.SubmitConfigSourceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_config_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.submit_config_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.SubmitConfigSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_submit_config_source_from_dict():
    test_submit_config_source(request_type=dict)


def test_submit_config_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_config_source), "__call__"
    ) as call:
        client.submit_config_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.SubmitConfigSourceRequest()


@pytest.mark.asyncio
async def test_submit_config_source_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.SubmitConfigSourceRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_config_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.submit_config_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.SubmitConfigSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_submit_config_source_async_from_dict():
    await test_submit_config_source_async(request_type=dict)


def test_submit_config_source_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_config_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.submit_config_source(
            service_name="service_name_value",
            config_source=resources.ConfigSource(id="id_value"),
            validate_only=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].config_source == resources.ConfigSource(id="id_value")
        assert args[0].validate_only == True


def test_submit_config_source_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.submit_config_source(
            servicemanager.SubmitConfigSourceRequest(),
            service_name="service_name_value",
            config_source=resources.ConfigSource(id="id_value"),
            validate_only=True,
        )


@pytest.mark.asyncio
async def test_submit_config_source_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_config_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.submit_config_source(
            service_name="service_name_value",
            config_source=resources.ConfigSource(id="id_value"),
            validate_only=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].config_source == resources.ConfigSource(id="id_value")
        assert args[0].validate_only == True


@pytest.mark.asyncio
async def test_submit_config_source_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.submit_config_source(
            servicemanager.SubmitConfigSourceRequest(),
            service_name="service_name_value",
            config_source=resources.ConfigSource(id="id_value"),
            validate_only=True,
        )


def test_list_service_rollouts(
    transport: str = "grpc", request_type=servicemanager.ListServiceRolloutsRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceRolloutsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_service_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceRolloutsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceRolloutsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_service_rollouts_from_dict():
    test_list_service_rollouts(request_type=dict)


def test_list_service_rollouts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        client.list_service_rollouts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceRolloutsRequest()


@pytest.mark.asyncio
async def test_list_service_rollouts_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.ListServiceRolloutsRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServiceRolloutsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_service_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.ListServiceRolloutsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServiceRolloutsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_service_rollouts_async_from_dict():
    await test_list_service_rollouts_async(request_type=dict)


def test_list_service_rollouts_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceRolloutsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_service_rollouts(
            service_name="service_name_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].filter == "filter_value"


def test_list_service_rollouts_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_service_rollouts(
            servicemanager.ListServiceRolloutsRequest(),
            service_name="service_name_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_service_rollouts_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.ListServiceRolloutsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.ListServiceRolloutsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_service_rollouts(
            service_name="service_name_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_service_rollouts_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_service_rollouts(
            servicemanager.ListServiceRolloutsRequest(),
            service_name="service_name_value",
            filter="filter_value",
        )


def test_list_service_rollouts_pager():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[
                    resources.Rollout(),
                    resources.Rollout(),
                    resources.Rollout(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[], next_page_token="def",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(), resources.Rollout(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_service_rollouts(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Rollout) for i in results)


def test_list_service_rollouts_pages():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[
                    resources.Rollout(),
                    resources.Rollout(),
                    resources.Rollout(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[], next_page_token="def",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(), resources.Rollout(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_service_rollouts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_service_rollouts_async_pager():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[
                    resources.Rollout(),
                    resources.Rollout(),
                    resources.Rollout(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[], next_page_token="def",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(), resources.Rollout(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_service_rollouts(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Rollout) for i in responses)


@pytest.mark.asyncio
async def test_list_service_rollouts_async_pages():
    client = ServiceManagerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_service_rollouts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[
                    resources.Rollout(),
                    resources.Rollout(),
                    resources.Rollout(),
                ],
                next_page_token="abc",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[], next_page_token="def",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(),], next_page_token="ghi",
            ),
            servicemanager.ListServiceRolloutsResponse(
                rollouts=[resources.Rollout(), resources.Rollout(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_service_rollouts(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_service_rollout(
    transport: str = "grpc", request_type=servicemanager.GetServiceRolloutRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Rollout(
            rollout_id="rollout_id_value",
            created_by="created_by_value",
            status=resources.Rollout.RolloutStatus.IN_PROGRESS,
            service_name="service_name_value",
            traffic_percent_strategy=resources.Rollout.TrafficPercentStrategy(
                percentages={"key_value": 0.541}
            ),
        )
        response = client.get_service_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Rollout)
    assert response.rollout_id == "rollout_id_value"
    assert response.created_by == "created_by_value"
    assert response.status == resources.Rollout.RolloutStatus.IN_PROGRESS
    assert response.service_name == "service_name_value"


def test_get_service_rollout_from_dict():
    test_get_service_rollout(request_type=dict)


def test_get_service_rollout_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_rollout), "__call__"
    ) as call:
        client.get_service_rollout()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRolloutRequest()


@pytest.mark.asyncio
async def test_get_service_rollout_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.GetServiceRolloutRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Rollout(
                rollout_id="rollout_id_value",
                created_by="created_by_value",
                status=resources.Rollout.RolloutStatus.IN_PROGRESS,
                service_name="service_name_value",
            )
        )
        response = await client.get_service_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GetServiceRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Rollout)
    assert response.rollout_id == "rollout_id_value"
    assert response.created_by == "created_by_value"
    assert response.status == resources.Rollout.RolloutStatus.IN_PROGRESS
    assert response.service_name == "service_name_value"


@pytest.mark.asyncio
async def test_get_service_rollout_async_from_dict():
    await test_get_service_rollout_async(request_type=dict)


def test_get_service_rollout_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Rollout()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service_rollout(
            service_name="service_name_value", rollout_id="rollout_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].rollout_id == "rollout_id_value"


def test_get_service_rollout_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_rollout(
            servicemanager.GetServiceRolloutRequest(),
            service_name="service_name_value",
            rollout_id="rollout_id_value",
        )


@pytest.mark.asyncio
async def test_get_service_rollout_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Rollout()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Rollout())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service_rollout(
            service_name="service_name_value", rollout_id="rollout_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].rollout_id == "rollout_id_value"


@pytest.mark.asyncio
async def test_get_service_rollout_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service_rollout(
            servicemanager.GetServiceRolloutRequest(),
            service_name="service_name_value",
            rollout_id="rollout_id_value",
        )


def test_create_service_rollout(
    transport: str = "grpc", request_type=servicemanager.CreateServiceRolloutRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_service_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_service_rollout_from_dict():
    test_create_service_rollout(request_type=dict)


def test_create_service_rollout_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_rollout), "__call__"
    ) as call:
        client.create_service_rollout()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRolloutRequest()


@pytest.mark.asyncio
async def test_create_service_rollout_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.CreateServiceRolloutRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_service_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.CreateServiceRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_service_rollout_async_from_dict():
    await test_create_service_rollout_async(request_type=dict)


def test_create_service_rollout_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service_rollout(
            service_name="service_name_value",
            rollout=resources.Rollout(rollout_id="rollout_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].rollout == resources.Rollout(rollout_id="rollout_id_value")


def test_create_service_rollout_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service_rollout(
            servicemanager.CreateServiceRolloutRequest(),
            service_name="service_name_value",
            rollout=resources.Rollout(rollout_id="rollout_id_value"),
        )


@pytest.mark.asyncio
async def test_create_service_rollout_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_service_rollout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service_rollout(
            service_name="service_name_value",
            rollout=resources.Rollout(rollout_id="rollout_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].rollout == resources.Rollout(rollout_id="rollout_id_value")


@pytest.mark.asyncio
async def test_create_service_rollout_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service_rollout(
            servicemanager.CreateServiceRolloutRequest(),
            service_name="service_name_value",
            rollout=resources.Rollout(rollout_id="rollout_id_value"),
        )


def test_generate_config_report(
    transport: str = "grpc", request_type=servicemanager.GenerateConfigReportRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_config_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.GenerateConfigReportResponse(
            service_name="service_name_value", id="id_value",
        )
        response = client.generate_config_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GenerateConfigReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, servicemanager.GenerateConfigReportResponse)
    assert response.service_name == "service_name_value"
    assert response.id == "id_value"


def test_generate_config_report_from_dict():
    test_generate_config_report(request_type=dict)


def test_generate_config_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_config_report), "__call__"
    ) as call:
        client.generate_config_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GenerateConfigReportRequest()


@pytest.mark.asyncio
async def test_generate_config_report_async(
    transport: str = "grpc_asyncio",
    request_type=servicemanager.GenerateConfigReportRequest,
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_config_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.GenerateConfigReportResponse(
                service_name="service_name_value", id="id_value",
            )
        )
        response = await client.generate_config_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.GenerateConfigReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, servicemanager.GenerateConfigReportResponse)
    assert response.service_name == "service_name_value"
    assert response.id == "id_value"


@pytest.mark.asyncio
async def test_generate_config_report_async_from_dict():
    await test_generate_config_report_async(request_type=dict)


def test_generate_config_report_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_config_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.GenerateConfigReportResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_config_report(
            new_config=any_pb2.Any(type_url="type_url_value"),
            old_config=any_pb2.Any(type_url="type_url_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].new_config == any_pb2.Any(type_url="type_url_value")
        assert args[0].old_config == any_pb2.Any(type_url="type_url_value")


def test_generate_config_report_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_config_report(
            servicemanager.GenerateConfigReportRequest(),
            new_config=any_pb2.Any(type_url="type_url_value"),
            old_config=any_pb2.Any(type_url="type_url_value"),
        )


@pytest.mark.asyncio
async def test_generate_config_report_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_config_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = servicemanager.GenerateConfigReportResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            servicemanager.GenerateConfigReportResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_config_report(
            new_config=any_pb2.Any(type_url="type_url_value"),
            old_config=any_pb2.Any(type_url="type_url_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].new_config == any_pb2.Any(type_url="type_url_value")
        assert args[0].old_config == any_pb2.Any(type_url="type_url_value")


@pytest.mark.asyncio
async def test_generate_config_report_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_config_report(
            servicemanager.GenerateConfigReportRequest(),
            new_config=any_pb2.Any(type_url="type_url_value"),
            old_config=any_pb2.Any(type_url="type_url_value"),
        )


def test_enable_service(
    transport: str = "grpc", request_type=servicemanager.EnableServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.enable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.enable_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.EnableServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_enable_service_from_dict():
    test_enable_service(request_type=dict)


def test_enable_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.enable_service), "__call__") as call:
        client.enable_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.EnableServiceRequest()


@pytest.mark.asyncio
async def test_enable_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.EnableServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.enable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.enable_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.EnableServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_enable_service_async_from_dict():
    await test_enable_service_async(request_type=dict)


def test_enable_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.enable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.enable_service(
            service_name="service_name_value", consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].consumer_id == "consumer_id_value"


def test_enable_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.enable_service(
            servicemanager.EnableServiceRequest(),
            service_name="service_name_value",
            consumer_id="consumer_id_value",
        )


@pytest.mark.asyncio
async def test_enable_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.enable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.enable_service(
            service_name="service_name_value", consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].consumer_id == "consumer_id_value"


@pytest.mark.asyncio
async def test_enable_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.enable_service(
            servicemanager.EnableServiceRequest(),
            service_name="service_name_value",
            consumer_id="consumer_id_value",
        )


def test_disable_service(
    transport: str = "grpc", request_type=servicemanager.DisableServiceRequest
):
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.disable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.disable_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DisableServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_disable_service_from_dict():
    test_disable_service(request_type=dict)


def test_disable_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.disable_service), "__call__") as call:
        client.disable_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DisableServiceRequest()


@pytest.mark.asyncio
async def test_disable_service_async(
    transport: str = "grpc_asyncio", request_type=servicemanager.DisableServiceRequest
):
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.disable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.disable_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == servicemanager.DisableServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_disable_service_async_from_dict():
    await test_disable_service_async(request_type=dict)


def test_disable_service_flattened():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.disable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.disable_service(
            service_name="service_name_value", consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].consumer_id == "consumer_id_value"


def test_disable_service_flattened_error():
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.disable_service(
            servicemanager.DisableServiceRequest(),
            service_name="service_name_value",
            consumer_id="consumer_id_value",
        )


@pytest.mark.asyncio
async def test_disable_service_flattened_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.disable_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.disable_service(
            service_name="service_name_value", consumer_id="consumer_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service_name == "service_name_value"
        assert args[0].consumer_id == "consumer_id_value"


@pytest.mark.asyncio
async def test_disable_service_flattened_error_async():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.disable_service(
            servicemanager.DisableServiceRequest(),
            service_name="service_name_value",
            consumer_id="consumer_id_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ServiceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ServiceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ServiceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ServiceManagerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ServiceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ServiceManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ServiceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ServiceManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ServiceManagerClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.ServiceManagerGrpcTransport,)


def test_service_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ServiceManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_service_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.servicemanagement_v1.services.service_manager.transports.ServiceManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ServiceManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_services",
        "get_service",
        "create_service",
        "delete_service",
        "undelete_service",
        "list_service_configs",
        "get_service_config",
        "create_service_config",
        "submit_config_source",
        "list_service_rollouts",
        "get_service_rollout",
        "create_service_rollout",
        "generate_config_report",
        "enable_service",
        "disable_service",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_service_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.servicemanagement_v1.services.service_manager.transports.ServiceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ServiceManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_service_manager_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.servicemanagement_v1.services.service_manager.transports.ServiceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ServiceManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id="octopus",
        )


def test_service_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.servicemanagement_v1.services.service_manager.transports.ServiceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ServiceManagerTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_service_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ServiceManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_service_manager_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ServiceManagerClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_service_manager_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_service_manager_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ServiceManagerGrpcTransport, grpc_helpers),
        (transports.ServiceManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_service_manager_transport_create_channel(transport_class, grpc_helpers):
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
            "servicemanagement.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/service.management",
                "https://www.googleapis.com/auth/service.management.readonly",
            ),
            scopes=["1", "2"],
            default_host="servicemanagement.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
def test_service_manager_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_service_manager_host_no_port():
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicemanagement.googleapis.com"
        ),
    )
    assert client.transport._host == "servicemanagement.googleapis.com:443"


def test_service_manager_host_with_port():
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicemanagement.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "servicemanagement.googleapis.com:8000"


def test_service_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ServiceManagerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_service_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ServiceManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
def test_service_manager_transport_channel_mtls_with_client_cert_source(
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
        transports.ServiceManagerGrpcTransport,
        transports.ServiceManagerGrpcAsyncIOTransport,
    ],
)
def test_service_manager_transport_channel_mtls_with_adc(transport_class):
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


def test_service_manager_grpc_lro_client():
    client = ServiceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_service_manager_grpc_lro_async_client():
    client = ServiceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ServiceManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = ServiceManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = ServiceManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = ServiceManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = ServiceManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = ServiceManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = ServiceManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = ServiceManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ServiceManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = ServiceManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ServiceManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ServiceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ServiceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ServiceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ServiceManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
