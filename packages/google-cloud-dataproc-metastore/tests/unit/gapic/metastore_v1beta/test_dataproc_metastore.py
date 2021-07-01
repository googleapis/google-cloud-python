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
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.metastore_v1beta.services.dataproc_metastore import (
    DataprocMetastoreAsyncClient,
)
from google.cloud.metastore_v1beta.services.dataproc_metastore import (
    DataprocMetastoreClient,
)
from google.cloud.metastore_v1beta.services.dataproc_metastore import pagers
from google.cloud.metastore_v1beta.services.dataproc_metastore import transports
from google.cloud.metastore_v1beta.services.dataproc_metastore.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.metastore_v1beta.types import metastore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
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

    assert DataprocMetastoreClient._get_default_mtls_endpoint(None) is None
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [DataprocMetastoreClient, DataprocMetastoreAsyncClient,]
)
def test_dataproc_metastore_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "metastore.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [DataprocMetastoreClient, DataprocMetastoreAsyncClient,]
)
def test_dataproc_metastore_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataprocMetastoreGrpcTransport, "grpc"),
        (transports.DataprocMetastoreGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_dataproc_metastore_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [DataprocMetastoreClient, DataprocMetastoreAsyncClient,]
)
def test_dataproc_metastore_client_from_service_account_file(client_class):
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

        assert client.transport._host == "metastore.googleapis.com:443"


def test_dataproc_metastore_client_get_transport_class():
    transport = DataprocMetastoreClient.get_transport_class()
    available_transports = [
        transports.DataprocMetastoreGrpcTransport,
    ]
    assert transport in available_transports

    transport = DataprocMetastoreClient.get_transport_class("grpc")
    assert transport == transports.DataprocMetastoreGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport, "grpc"),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataprocMetastoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreClient),
)
@mock.patch.object(
    DataprocMetastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreAsyncClient),
)
def test_dataproc_metastore_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataprocMetastoreClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataprocMetastoreClient, "get_transport_class") as gtc:
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
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            "true",
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            "false",
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataprocMetastoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreClient),
)
@mock.patch.object(
    DataprocMetastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_dataproc_metastore_client_mtls_env_auto(
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
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport, "grpc"),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_dataproc_metastore_client_client_options_scopes(
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
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport, "grpc"),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_dataproc_metastore_client_client_options_credentials_file(
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


def test_dataproc_metastore_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.metastore_v1beta.services.dataproc_metastore.transports.DataprocMetastoreGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataprocMetastoreClient(
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
    transport: str = "grpc", request_type=metastore.ListServicesRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_services_from_dict():
    test_list_services(request_type=dict)


def test_list_services_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        client.list_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()


@pytest.mark.asyncio
async def test_list_services_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListServicesRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_services_async_from_dict():
    await test_list_services_async(request_type=dict)


def test_list_services_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListServicesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        call.return_value = metastore.ListServicesResponse()
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListServicesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse()
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
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_services(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_services_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            metastore.ListServicesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_services_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse()
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_services(
            metastore.ListServicesRequest(), parent="parent_value",
        )


def test_list_services_pager():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(services=[], next_page_token="def",),
            metastore.ListServicesResponse(
                services=[metastore.Service(),], next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[metastore.Service(), metastore.Service(),],
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
        assert all(isinstance(i, metastore.Service) for i in results)


def test_list_services_pages():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(services=[], next_page_token="def",),
            metastore.ListServicesResponse(
                services=[metastore.Service(),], next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[metastore.Service(), metastore.Service(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_services_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(services=[], next_page_token="def",),
            metastore.ListServicesResponse(
                services=[metastore.Service(),], next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[metastore.Service(), metastore.Service(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_services(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Service) for i in responses)


@pytest.mark.asyncio
async def test_list_services_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(services=[], next_page_token="def",),
            metastore.ListServicesResponse(
                services=[metastore.Service(),], next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[metastore.Service(), metastore.Service(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_services(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_service(transport: str = "grpc", request_type=metastore.GetServiceRequest):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service(
            name="name_value",
            network="network_value",
            endpoint_uri="endpoint_uri_value",
            port=453,
            state=metastore.Service.State.CREATING,
            state_message="state_message_value",
            artifact_gcs_uri="artifact_gcs_uri_value",
            tier=metastore.Service.Tier.DEVELOPER,
            uid="uid_value",
            release_channel=metastore.Service.ReleaseChannel.CANARY,
            hive_metastore_config=metastore.HiveMetastoreConfig(
                version="version_value"
            ),
        )
        response = client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Service)
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.port == 453
    assert response.state == metastore.Service.State.CREATING
    assert response.state_message == "state_message_value"
    assert response.artifact_gcs_uri == "artifact_gcs_uri_value"
    assert response.tier == metastore.Service.Tier.DEVELOPER
    assert response.uid == "uid_value"
    assert response.release_channel == metastore.Service.ReleaseChannel.CANARY


def test_get_service_from_dict():
    test_get_service(request_type=dict)


def test_get_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        client.get_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()


@pytest.mark.asyncio
async def test_get_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Service(
                name="name_value",
                network="network_value",
                endpoint_uri="endpoint_uri_value",
                port=453,
                state=metastore.Service.State.CREATING,
                state_message="state_message_value",
                artifact_gcs_uri="artifact_gcs_uri_value",
                tier=metastore.Service.Tier.DEVELOPER,
                uid="uid_value",
                release_channel=metastore.Service.ReleaseChannel.CANARY,
            )
        )
        response = await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Service)
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.port == 453
    assert response.state == metastore.Service.State.CREATING
    assert response.state_message == "state_message_value"
    assert response.artifact_gcs_uri == "artifact_gcs_uri_value"
    assert response.tier == metastore.Service.Tier.DEVELOPER
    assert response.uid == "uid_value"
    assert response.release_channel == metastore.Service.ReleaseChannel.CANARY


@pytest.mark.asyncio
async def test_get_service_async_from_dict():
    await test_get_service_async(request_type=dict)


def test_get_service_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        call.return_value = metastore.Service()
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Service())
        await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_service_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_service_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(
            metastore.GetServiceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Service())
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service(
            metastore.GetServiceRequest(), name="name_value",
        )


def test_create_service(
    transport: str = "grpc", request_type=metastore.CreateServiceRequest
):
    client = DataprocMetastoreClient(
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
        assert args[0] == metastore.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_service_from_dict():
    test_create_service(request_type=dict)


def test_create_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        client.create_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateServiceRequest()


@pytest.mark.asyncio
async def test_create_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateServiceRequest
):
    client = DataprocMetastoreAsyncClient(
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
        assert args[0] == metastore.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_service_async_from_dict():
    await test_create_service_async(request_type=dict)


def test_create_service_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateServiceRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateServiceRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_service_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service(
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].service == metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert args[0].service_id == "service_id_value"


def test_create_service_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            metastore.CreateServiceRequest(),
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )


@pytest.mark.asyncio
async def test_create_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
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
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].service == metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert args[0].service_id == "service_id_value"


@pytest.mark.asyncio
async def test_create_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service(
            metastore.CreateServiceRequest(),
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )


def test_update_service(
    transport: str = "grpc", request_type=metastore.UpdateServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_service_from_dict():
    test_update_service(request_type=dict)


def test_update_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        client.update_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()


@pytest.mark.asyncio
async def test_update_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_service_async_from_dict():
    await test_update_service_async(request_type=dict)


def test_update_service_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateServiceRequest()

    request.service.name = "service.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateServiceRequest()

    request.service.name = "service.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
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
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_service(
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service == metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_service_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service(
            metastore.UpdateServiceRequest(),
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_service(
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service == metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_service(
            metastore.UpdateServiceRequest(),
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_service(
    transport: str = "grpc", request_type=metastore.DeleteServiceRequest
):
    client = DataprocMetastoreClient(
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
        assert args[0] == metastore.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_service_from_dict():
    test_delete_service(request_type=dict)


def test_delete_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        client.delete_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteServiceRequest()


@pytest.mark.asyncio
async def test_delete_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteServiceRequest
):
    client = DataprocMetastoreAsyncClient(
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
        assert args[0] == metastore.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_service_async_from_dict():
    await test_delete_service_async(request_type=dict)


def test_delete_service_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteServiceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_service_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_service_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            metastore.DeleteServiceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
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
        response = await client.delete_service(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service(
            metastore.DeleteServiceRequest(), name="name_value",
        )


def test_list_metadata_imports(
    transport: str = "grpc", request_type=metastore.ListMetadataImportsRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMetadataImportsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_metadata_imports_from_dict():
    test_list_metadata_imports(request_type=dict)


def test_list_metadata_imports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        client.list_metadata_imports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()


@pytest.mark.asyncio
async def test_list_metadata_imports_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListMetadataImportsRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMetadataImportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_metadata_imports_async_from_dict():
    await test_list_metadata_imports_async(request_type=dict)


def test_list_metadata_imports_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListMetadataImportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        call.return_value = metastore.ListMetadataImportsResponse()
        client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_metadata_imports_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListMetadataImportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse()
        )
        await client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_metadata_imports_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_metadata_imports(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_metadata_imports_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_metadata_imports(
            metastore.ListMetadataImportsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_metadata_imports_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_metadata_imports(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_metadata_imports_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_metadata_imports(
            metastore.ListMetadataImportsRequest(), parent="parent_value",
        )


def test_list_metadata_imports_pager():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[], next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[metastore.MetadataImport(),], next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_metadata_imports(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, metastore.MetadataImport) for i in results)


def test_list_metadata_imports_pages():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[], next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[metastore.MetadataImport(),], next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_metadata_imports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_metadata_imports_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[], next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[metastore.MetadataImport(),], next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_metadata_imports(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.MetadataImport) for i in responses)


@pytest.mark.asyncio
async def test_list_metadata_imports_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[], next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[metastore.MetadataImport(),], next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_metadata_imports(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_metadata_import(
    transport: str = "grpc", request_type=metastore.GetMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport(
            name="name_value",
            description="description_value",
            state=metastore.MetadataImport.State.RUNNING,
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            ),
        )
        response = client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.MetadataImport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.state == metastore.MetadataImport.State.RUNNING


def test_get_metadata_import_from_dict():
    test_get_metadata_import(request_type=dict)


def test_get_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        client.get_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()


@pytest.mark.asyncio
async def test_get_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport(
                name="name_value",
                description="description_value",
                state=metastore.MetadataImport.State.RUNNING,
            )
        )
        response = await client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.MetadataImport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.state == metastore.MetadataImport.State.RUNNING


@pytest.mark.asyncio
async def test_get_metadata_import_async_from_dict():
    await test_get_metadata_import_async(request_type=dict)


def test_get_metadata_import_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetMetadataImportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        call.return_value = metastore.MetadataImport()
        client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetMetadataImportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport()
        )
        await client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_metadata_import_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_metadata_import(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_metadata_import_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata_import(
            metastore.GetMetadataImportRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_metadata_import(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_metadata_import(
            metastore.GetMetadataImportRequest(), name="name_value",
        )


def test_create_metadata_import(
    transport: str = "grpc", request_type=metastore.CreateMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_metadata_import_from_dict():
    test_create_metadata_import(request_type=dict)


def test_create_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        client.create_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()


@pytest.mark.asyncio
async def test_create_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_metadata_import_async_from_dict():
    await test_create_metadata_import_async(request_type=dict)


def test_create_metadata_import_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateMetadataImportRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateMetadataImportRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_metadata_import_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_metadata_import(
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].metadata_import == metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert args[0].metadata_import_id == "metadata_import_id_value"


def test_create_metadata_import_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_metadata_import(
            metastore.CreateMetadataImportRequest(),
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )


@pytest.mark.asyncio
async def test_create_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_metadata_import(
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].metadata_import == metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert args[0].metadata_import_id == "metadata_import_id_value"


@pytest.mark.asyncio
async def test_create_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_metadata_import(
            metastore.CreateMetadataImportRequest(),
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )


def test_update_metadata_import(
    transport: str = "grpc", request_type=metastore.UpdateMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_metadata_import_from_dict():
    test_update_metadata_import(request_type=dict)


def test_update_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        client.update_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()


@pytest.mark.asyncio
async def test_update_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_metadata_import_async_from_dict():
    await test_update_metadata_import_async(request_type=dict)


def test_update_metadata_import_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateMetadataImportRequest()

    request.metadata_import.name = "metadata_import.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "metadata_import.name=metadata_import.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateMetadataImportRequest()

    request.metadata_import.name = "metadata_import.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "metadata_import.name=metadata_import.name/value",
    ) in kw["metadata"]


def test_update_metadata_import_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_metadata_import(
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].metadata_import == metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_metadata_import_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_metadata_import(
            metastore.UpdateMetadataImportRequest(),
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_metadata_import(
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].metadata_import == metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_metadata_import(
            metastore.UpdateMetadataImportRequest(),
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_export_metadata(
    transport: str = "grpc", request_type=metastore.ExportMetadataRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_metadata_from_dict():
    test_export_metadata(request_type=dict)


def test_export_metadata_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        client.export_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()


@pytest.mark.asyncio
async def test_export_metadata_async(
    transport: str = "grpc_asyncio", request_type=metastore.ExportMetadataRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_metadata_async_from_dict():
    await test_export_metadata_async(request_type=dict)


def test_export_metadata_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ExportMetadataRequest()

    request.service = "service/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service=service/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_metadata_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ExportMetadataRequest()

    request.service = "service/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service=service/value",) in kw["metadata"]


def test_restore_service(
    transport: str = "grpc", request_type=metastore.RestoreServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restore_service_from_dict():
    test_restore_service(request_type=dict)


def test_restore_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        client.restore_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()


@pytest.mark.asyncio
async def test_restore_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.RestoreServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restore_service_async_from_dict():
    await test_restore_service_async(request_type=dict)


def test_restore_service_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RestoreServiceRequest()

    request.service = "service/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service=service/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_restore_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RestoreServiceRequest()

    request.service = "service/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service=service/value",) in kw["metadata"]


def test_restore_service_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restore_service(
            service="service_value", backup="backup_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service == "service_value"
        assert args[0].backup == "backup_value"


def test_restore_service_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_service(
            metastore.RestoreServiceRequest(),
            service="service_value",
            backup="backup_value",
        )


@pytest.mark.asyncio
async def test_restore_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restore_service(
            service="service_value", backup="backup_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].service == "service_value"
        assert args[0].backup == "backup_value"


@pytest.mark.asyncio
async def test_restore_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restore_service(
            metastore.RestoreServiceRequest(),
            service="service_value",
            backup="backup_value",
        )


def test_list_backups(
    transport: str = "grpc", request_type=metastore.ListBackupsRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_backups_from_dict():
    test_list_backups(request_type=dict)


def test_list_backups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        client.list_backups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()


@pytest.mark.asyncio
async def test_list_backups_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListBackupsRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListBackupsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_backups_async_from_dict():
    await test_list_backups_async(request_type=dict)


def test_list_backups_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListBackupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = metastore.ListBackupsResponse()
        client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_backups_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListBackupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListBackupsResponse()
        )
        await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_backups_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_backups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_backups_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            metastore.ListBackupsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_backups_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListBackupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_backups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_backups_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_backups(
            metastore.ListBackupsRequest(), parent="parent_value",
        )


def test_list_backups_pager():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(), metastore.Backup(),],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(backups=[], next_page_token="def",),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(),], next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_backups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, metastore.Backup) for i in results)


def test_list_backups_pages():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(), metastore.Backup(),],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(backups=[], next_page_token="def",),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(),], next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_backups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_backups_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(), metastore.Backup(),],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(backups=[], next_page_token="def",),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(),], next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_backups(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Backup) for i in responses)


@pytest.mark.asyncio
async def test_list_backups_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(), metastore.Backup(),],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(backups=[], next_page_token="def",),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(),], next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[metastore.Backup(), metastore.Backup(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_backups(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_backup(transport: str = "grpc", request_type=metastore.GetBackupRequest):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup(
            name="name_value",
            state=metastore.Backup.State.CREATING,
            description="description_value",
        )
        response = client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Backup)
    assert response.name == "name_value"
    assert response.state == metastore.Backup.State.CREATING
    assert response.description == "description_value"


def test_get_backup_from_dict():
    test_get_backup(request_type=dict)


def test_get_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        client.get_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()


@pytest.mark.asyncio
async def test_get_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetBackupRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Backup(
                name="name_value",
                state=metastore.Backup.State.CREATING,
                description="description_value",
            )
        )
        response = await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Backup)
    assert response.name == "name_value"
    assert response.state == metastore.Backup.State.CREATING
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_backup_async_from_dict():
    await test_get_backup_async(request_type=dict)


def test_get_backup_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = metastore.Backup()
        client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Backup())
        await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_backup_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_backup(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_backup_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            metastore.GetBackupRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Backup())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_backup(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_backup_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_backup(
            metastore.GetBackupRequest(), name="name_value",
        )


def test_create_backup(
    transport: str = "grpc", request_type=metastore.CreateBackupRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_backup_from_dict():
    test_create_backup(request_type=dict)


def test_create_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        client.create_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateBackupRequest()


@pytest.mark.asyncio
async def test_create_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateBackupRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_backup_async_from_dict():
    await test_create_backup_async(request_type=dict)


def test_create_backup_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateBackupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateBackupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_backup_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_backup(
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].backup == metastore.Backup(name="name_value")
        assert args[0].backup_id == "backup_id_value"


def test_create_backup_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            metastore.CreateBackupRequest(),
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )


@pytest.mark.asyncio
async def test_create_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_backup(
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].backup == metastore.Backup(name="name_value")
        assert args[0].backup_id == "backup_id_value"


@pytest.mark.asyncio
async def test_create_backup_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_backup(
            metastore.CreateBackupRequest(),
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )


def test_delete_backup(
    transport: str = "grpc", request_type=metastore.DeleteBackupRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_backup_from_dict():
    test_delete_backup(request_type=dict)


def test_delete_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        client.delete_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()


@pytest.mark.asyncio
async def test_delete_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteBackupRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_backup_async_from_dict():
    await test_delete_backup_async(request_type=dict)


def test_delete_backup_field_headers():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_backup_flattened():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_backup(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_backup_flattened_error():
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            metastore.DeleteBackupRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_backup(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_backup_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_backup(
            metastore.DeleteBackupRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataprocMetastoreClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataprocMetastoreGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
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
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.DataprocMetastoreGrpcTransport,)


def test_dataproc_metastore_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataprocMetastoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_dataproc_metastore_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.metastore_v1beta.services.dataproc_metastore.transports.DataprocMetastoreTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataprocMetastoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_services",
        "get_service",
        "create_service",
        "update_service",
        "delete_service",
        "list_metadata_imports",
        "get_metadata_import",
        "create_metadata_import",
        "update_metadata_import",
        "export_metadata",
        "restore_service",
        "list_backups",
        "get_backup",
        "create_backup",
        "delete_backup",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_dataproc_metastore_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.metastore_v1beta.services.dataproc_metastore.transports.DataprocMetastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataprocMetastoreTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_dataproc_metastore_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.metastore_v1beta.services.dataproc_metastore.transports.DataprocMetastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataprocMetastoreTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_dataproc_metastore_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.metastore_v1beta.services.dataproc_metastore.transports.DataprocMetastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataprocMetastoreTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_dataproc_metastore_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataprocMetastoreClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_dataproc_metastore_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataprocMetastoreClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_dataproc_metastore_transport_auth_adc(transport_class):
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_dataproc_metastore_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.DataprocMetastoreGrpcTransport, grpc_helpers),
        (transports.DataprocMetastoreGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_dataproc_metastore_transport_create_channel(transport_class, grpc_helpers):
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
            "metastore.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="metastore.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_dataproc_metastore_host_no_port():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="metastore.googleapis.com"
        ),
    )
    assert client.transport._host == "metastore.googleapis.com:443"


def test_dataproc_metastore_host_with_port():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="metastore.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "metastore.googleapis.com:8000"


def test_dataproc_metastore_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataprocMetastoreGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_dataproc_metastore_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataprocMetastoreGrpcAsyncIOTransport(
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_transport_channel_mtls_with_client_cert_source(
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_transport_channel_mtls_with_adc(transport_class):
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


def test_dataproc_metastore_grpc_lro_client():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_dataproc_metastore_grpc_lro_async_client():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_backup_path():
    project = "squid"
    location = "clam"
    service = "whelk"
    backup = "octopus"
    expected = "projects/{project}/locations/{location}/services/{service}/backups/{backup}".format(
        project=project, location=location, service=service, backup=backup,
    )
    actual = DataprocMetastoreClient.backup_path(project, location, service, backup)
    assert expected == actual


def test_parse_backup_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "service": "cuttlefish",
        "backup": "mussel",
    }
    path = DataprocMetastoreClient.backup_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_backup_path(path)
    assert expected == actual


def test_metadata_import_path():
    project = "winkle"
    location = "nautilus"
    service = "scallop"
    metadata_import = "abalone"
    expected = "projects/{project}/locations/{location}/services/{service}/metadataImports/{metadata_import}".format(
        project=project,
        location=location,
        service=service,
        metadata_import=metadata_import,
    )
    actual = DataprocMetastoreClient.metadata_import_path(
        project, location, service, metadata_import
    )
    assert expected == actual


def test_parse_metadata_import_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "service": "whelk",
        "metadata_import": "octopus",
    }
    path = DataprocMetastoreClient.metadata_import_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_metadata_import_path(path)
    assert expected == actual


def test_network_path():
    project = "oyster"
    network = "nudibranch"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project, network=network,
    )
    actual = DataprocMetastoreClient.network_path(project, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "cuttlefish",
        "network": "mussel",
    }
    path = DataprocMetastoreClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_network_path(path)
    assert expected == actual


def test_service_path():
    project = "winkle"
    location = "nautilus"
    service = "scallop"
    expected = "projects/{project}/locations/{location}/services/{service}".format(
        project=project, location=location, service=service,
    )
    actual = DataprocMetastoreClient.service_path(project, location, service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "service": "clam",
    }
    path = DataprocMetastoreClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_service_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataprocMetastoreClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = DataprocMetastoreClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = DataprocMetastoreClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = DataprocMetastoreClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = DataprocMetastoreClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = DataprocMetastoreClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = DataprocMetastoreClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = DataprocMetastoreClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = DataprocMetastoreClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = DataprocMetastoreClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataprocMetastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataprocMetastoreClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataprocMetastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataprocMetastoreClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
