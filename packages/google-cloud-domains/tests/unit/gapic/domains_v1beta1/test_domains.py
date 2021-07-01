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
from google.cloud.domains_v1beta1.services.domains import DomainsAsyncClient
from google.cloud.domains_v1beta1.services.domains import DomainsClient
from google.cloud.domains_v1beta1.services.domains import pagers
from google.cloud.domains_v1beta1.services.domains import transports
from google.cloud.domains_v1beta1.services.domains.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.domains_v1beta1.types import domains
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore
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


@pytest.mark.parametrize("client_class", [DomainsClient, DomainsAsyncClient,])
def test_domains_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "domains.googleapis.com:443"


@pytest.mark.parametrize("client_class", [DomainsClient, DomainsAsyncClient,])
def test_domains_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DomainsGrpcTransport, "grpc"),
        (transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_domains_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize("client_class", [DomainsClient, DomainsAsyncClient,])
def test_domains_client_from_service_account_file(client_class):
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

        assert client.transport._host == "domains.googleapis.com:443"


def test_domains_client_get_transport_class():
    transport = DomainsClient.get_transport_class()
    available_transports = [
        transports.DomainsGrpcTransport,
    ]
    assert transport in available_transports

    transport = DomainsClient.get_transport_class("grpc")
    assert transport == transports.DomainsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DomainsClient, transports.DomainsGrpcTransport, "grpc"),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc"),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_domains_client_client_options_scopes(
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
        (DomainsClient, transports.DomainsGrpcTransport, "grpc"),
        (DomainsAsyncClient, transports.DomainsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_domains_client_client_options_credentials_file(
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


def test_domains_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.domains_v1beta1.services.domains.transports.DomainsGrpcTransport.__init__"
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
        )


def test_search_domains(
    transport: str = "grpc", request_type=domains.SearchDomainsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_search_domains_from_dict():
    test_search_domains(request_type=dict)


def test_search_domains_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.SearchDomainsRequest()

    request.location = "location/value"

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
    assert ("x-goog-request-params", "location=location/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_domains_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.SearchDomainsRequest()

    request.location = "location/value"

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
    assert ("x-goog-request-params", "location=location/value",) in kw["metadata"]


def test_search_domains_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_domains), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.SearchDomainsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_domains(
            location="location_value", query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].location == "location_value"
        assert args[0].query == "query_value"


def test_search_domains_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
            location="location_value", query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].location == "location_value"
        assert args[0].query == "query_value"


@pytest.mark.asyncio
async def test_search_domains_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_domains(
            domains.SearchDomainsRequest(),
            location="location_value",
            query="query_value",
        )


def test_retrieve_register_parameters(
    transport: str = "grpc", request_type=domains.RetrieveRegisterParametersRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_retrieve_register_parameters_from_dict():
    test_retrieve_register_parameters(request_type=dict)


def test_retrieve_register_parameters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveRegisterParametersRequest()

    request.location = "location/value"

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
    assert ("x-goog-request-params", "location=location/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_retrieve_register_parameters_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveRegisterParametersRequest()

    request.location = "location/value"

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
    assert ("x-goog-request-params", "location=location/value",) in kw["metadata"]


def test_retrieve_register_parameters_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_register_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.RetrieveRegisterParametersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retrieve_register_parameters(
            location="location_value", domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].location == "location_value"
        assert args[0].domain_name == "domain_name_value"


def test_retrieve_register_parameters_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
            location="location_value", domain_name="domain_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].location == "location_value"
        assert args[0].domain_name == "domain_name_value"


@pytest.mark.asyncio
async def test_retrieve_register_parameters_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retrieve_register_parameters(
            domains.RetrieveRegisterParametersRequest(),
            location="location_value",
            domain_name="domain_name_value",
        )


def test_register_domain(
    transport: str = "grpc", request_type=domains.RegisterDomainRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_register_domain_from_dict():
    test_register_domain(request_type=dict)


def test_register_domain_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RegisterDomainRequest()

    request.parent = "parent/value"

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
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_register_domain_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RegisterDomainRequest()

    request.parent = "parent/value"

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
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_register_domain_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].parent == "parent_value"
        assert args[0].registration == domains.Registration(name="name_value")
        assert args[0].yearly_price == money_pb2.Money(
            currency_code="currency_code_value"
        )


def test_register_domain_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].parent == "parent_value"
        assert args[0].registration == domains.Registration(name="name_value")
        assert args[0].yearly_price == money_pb2.Money(
            currency_code="currency_code_value"
        )


@pytest.mark.asyncio
async def test_register_domain_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.register_domain(
            domains.RegisterDomainRequest(),
            parent="parent_value",
            registration=domains.Registration(name="name_value"),
            yearly_price=money_pb2.Money(currency_code="currency_code_value"),
        )


def test_list_registrations(
    transport: str = "grpc", request_type=domains.ListRegistrationsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_list_registrations_from_dict():
    test_list_registrations(request_type=dict)


def test_list_registrations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            domains.ListRegistrationsResponse(next_page_token="next_page_token_value",)
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ListRegistrationsRequest()

    request.parent = "parent/value"

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
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_registrations_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ListRegistrationsRequest()

    request.parent = "parent/value"

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
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_registrations_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.ListRegistrationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_registrations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_registrations_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_registrations(
            domains.ListRegistrationsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_registrations_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        response = await client.list_registrations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_registrations_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_registrations(
            domains.ListRegistrationsRequest(), parent="parent_value",
        )


def test_list_registrations_pager():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials,)

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
            domains.ListRegistrationsResponse(registrations=[], next_page_token="def",),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(),], next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(), domains.Registration(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_registrations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, domains.Registration) for i in results)


def test_list_registrations_pages():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials,)

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
            domains.ListRegistrationsResponse(registrations=[], next_page_token="def",),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(),], next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(), domains.Registration(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_registrations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_registrations_async_pager():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

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
            domains.ListRegistrationsResponse(registrations=[], next_page_token="def",),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(),], next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(), domains.Registration(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_registrations(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, domains.Registration) for i in responses)


@pytest.mark.asyncio
async def test_list_registrations_async_pages():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

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
            domains.ListRegistrationsResponse(registrations=[], next_page_token="def",),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(),], next_page_token="ghi",
            ),
            domains.ListRegistrationsResponse(
                registrations=[domains.Registration(), domains.Registration(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_registrations(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_registration(
    transport: str = "grpc", request_type=domains.GetRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_get_registration_from_dict():
    test_get_registration(request_type=dict)


def test_get_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.GetRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_registration_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.GetRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_registration_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.Registration()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_registration_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_registration(
            domains.GetRegistrationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_registration_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_registration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.Registration()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            domains.Registration()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_registration_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_registration(
            domains.GetRegistrationRequest(), name="name_value",
        )


def test_update_registration(
    transport: str = "grpc", request_type=domains.UpdateRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_update_registration_from_dict():
    test_update_registration(request_type=dict)


def test_update_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.UpdateRegistrationRequest()

    request.registration.name = "registration.name/value"

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
        "registration.name=registration.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_registration_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.UpdateRegistrationRequest()

    request.registration.name = "registration.name/value"

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
        "registration.name=registration.name/value",
    ) in kw["metadata"]


def test_update_registration_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == domains.Registration(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_registration_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == domains.Registration(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_registration_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_registration(
            domains.UpdateRegistrationRequest(),
            registration=domains.Registration(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_configure_management_settings(
    transport: str = "grpc", request_type=domains.ConfigureManagementSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_configure_management_settings_from_dict():
    test_configure_management_settings(request_type=dict)


def test_configure_management_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureManagementSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_configure_management_settings_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureManagementSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


def test_configure_management_settings_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].management_settings == domains.ManagementSettings(
            renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_configure_management_settings_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].management_settings == domains.ManagementSettings(
            renewal_method=domains.ManagementSettings.RenewalMethod.AUTOMATIC_RENEWAL
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_configure_management_settings_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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


def test_configure_dns_settings(
    transport: str = "grpc", request_type=domains.ConfigureDnsSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_configure_dns_settings_from_dict():
    test_configure_dns_settings(request_type=dict)


def test_configure_dns_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureDnsSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_configure_dns_settings_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureDnsSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


def test_configure_dns_settings_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].dns_settings == domains.DnsSettings(
            custom_dns=domains.DnsSettings.CustomDns(
                name_servers=["name_servers_value"]
            )
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_configure_dns_settings_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].dns_settings == domains.DnsSettings(
            custom_dns=domains.DnsSettings.CustomDns(
                name_servers=["name_servers_value"]
            )
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_configure_dns_settings_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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


def test_configure_contact_settings(
    transport: str = "grpc", request_type=domains.ConfigureContactSettingsRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_configure_contact_settings_from_dict():
    test_configure_contact_settings(request_type=dict)


def test_configure_contact_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureContactSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_configure_contact_settings_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ConfigureContactSettingsRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


def test_configure_contact_settings_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].contact_settings == domains.ContactSettings(
            privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_configure_contact_settings_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"
        assert args[0].contact_settings == domains.ContactSettings(
            privacy=domains.ContactPrivacy.PUBLIC_CONTACT_DATA
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_configure_contact_settings_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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


def test_export_registration(
    transport: str = "grpc", request_type=domains.ExportRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_export_registration_from_dict():
    test_export_registration(request_type=dict)


def test_export_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ExportRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_registration_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ExportRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_registration_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_export_registration_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_registration(
            domains.ExportRegistrationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_export_registration_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        response = await client.export_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_export_registration_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_registration(
            domains.ExportRegistrationRequest(), name="name_value",
        )


def test_delete_registration(
    transport: str = "grpc", request_type=domains.DeleteRegistrationRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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


def test_delete_registration_from_dict():
    test_delete_registration(request_type=dict)


def test_delete_registration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.DeleteRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_registration_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.DeleteRegistrationRequest()

    request.name = "name/value"

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
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_registration_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_registration_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_registration(
            domains.DeleteRegistrationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_registration_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        response = await client.delete_registration(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_registration_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_registration(
            domains.DeleteRegistrationRequest(), name="name_value",
        )


def test_retrieve_authorization_code(
    transport: str = "grpc", request_type=domains.RetrieveAuthorizationCodeRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode(code="code_value",)
        response = client.retrieve_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.RetrieveAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_retrieve_authorization_code_from_dict():
    test_retrieve_authorization_code(request_type=dict)


def test_retrieve_authorization_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            domains.AuthorizationCode(code="code_value",)
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveAuthorizationCodeRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_retrieve_authorization_code_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.RetrieveAuthorizationCodeRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


def test_retrieve_authorization_code_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.retrieve_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retrieve_authorization_code(registration="registration_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].registration == "registration_value"


def test_retrieve_authorization_code_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retrieve_authorization_code(
            domains.RetrieveAuthorizationCodeRequest(),
            registration="registration_value",
        )


@pytest.mark.asyncio
async def test_retrieve_authorization_code_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"


@pytest.mark.asyncio
async def test_retrieve_authorization_code_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retrieve_authorization_code(
            domains.RetrieveAuthorizationCodeRequest(),
            registration="registration_value",
        )


def test_reset_authorization_code(
    transport: str = "grpc", request_type=domains.ResetAuthorizationCodeRequest
):
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode(code="code_value",)
        response = client.reset_authorization_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == domains.ResetAuthorizationCodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, domains.AuthorizationCode)
    assert response.code == "code_value"


def test_reset_authorization_code_from_dict():
    test_reset_authorization_code(request_type=dict)


def test_reset_authorization_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            domains.AuthorizationCode(code="code_value",)
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
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ResetAuthorizationCodeRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_reset_authorization_code_field_headers_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = domains.ResetAuthorizationCodeRequest()

    request.registration = "registration/value"

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
    assert ("x-goog-request-params", "registration=registration/value",) in kw[
        "metadata"
    ]


def test_reset_authorization_code_flattened():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.reset_authorization_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = domains.AuthorizationCode()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.reset_authorization_code(registration="registration_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].registration == "registration_value"


def test_reset_authorization_code_flattened_error():
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset_authorization_code(
            domains.ResetAuthorizationCodeRequest(), registration="registration_value",
        )


@pytest.mark.asyncio
async def test_reset_authorization_code_flattened_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

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
        assert args[0].registration == "registration_value"


@pytest.mark.asyncio
async def test_reset_authorization_code_flattened_error_async():
    client = DomainsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.reset_authorization_code(
            domains.ResetAuthorizationCodeRequest(), registration="registration_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DomainsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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

    # It is an error to provide scopes and a transport instance.
    transport = transports.DomainsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DomainsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
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
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DomainsClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.DomainsGrpcTransport,)


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
        "google.cloud.domains_v1beta1.services.domains.transports.DomainsTransport.__init__"
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

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_domains_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.domains_v1beta1.services.domains.transports.DomainsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DomainsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_domains_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.domains_v1beta1.services.domains.transports.DomainsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DomainsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_domains_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.domains_v1beta1.services.domains.transports.DomainsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DomainsTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
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


@requires_google_auth_lt_1_25_0
def test_domains_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DomainsClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
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
    [transports.DomainsGrpcTransport, transports.DomainsGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_domains_transport_auth_adc_old_google_auth(transport_class):
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


def test_domains_host_no_port():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="domains.googleapis.com"
        ),
    )
    assert client.transport._host == "domains.googleapis.com:443"


def test_domains_host_with_port():
    client = DomainsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="domains.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "domains.googleapis.com:8000"


def test_domains_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DomainsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_domains_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DomainsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
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
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_domains_grpc_lro_async_client():
    client = DomainsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_registration_path():
    project = "squid"
    location = "clam"
    registration = "whelk"
    expected = "projects/{project}/locations/{location}/registrations/{registration}".format(
        project=project, location=location, registration=registration,
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
    expected = "folders/{folder}".format(folder=folder,)
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
    expected = "organizations/{organization}".format(organization=organization,)
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
    expected = "projects/{project}".format(project=project,)
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
        project=project, location=location,
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


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DomainsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DomainsClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DomainsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DomainsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
