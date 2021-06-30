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


from google.analytics.admin_v1alpha.services.analytics_admin_service import (
    AnalyticsAdminServiceAsyncClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service import (
    AnalyticsAdminServiceClient,
)
from google.analytics.admin_v1alpha.services.analytics_admin_service import pagers
from google.analytics.admin_v1alpha.services.analytics_admin_service import transports
from google.analytics.admin_v1alpha.services.analytics_admin_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import resources
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert AnalyticsAdminServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AnalyticsAdminServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [AnalyticsAdminServiceClient, AnalyticsAdminServiceAsyncClient,]
)
def test_analytics_admin_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "analyticsadmin.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [AnalyticsAdminServiceClient, AnalyticsAdminServiceAsyncClient,]
)
def test_analytics_admin_service_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AnalyticsAdminServiceGrpcTransport, "grpc"),
        (transports.AnalyticsAdminServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_analytics_admin_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [AnalyticsAdminServiceClient, AnalyticsAdminServiceAsyncClient,]
)
def test_analytics_admin_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "analyticsadmin.googleapis.com:443"


def test_analytics_admin_service_client_get_transport_class():
    transport = AnalyticsAdminServiceClient.get_transport_class()
    available_transports = [
        transports.AnalyticsAdminServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = AnalyticsAdminServiceClient.get_transport_class("grpc")
    assert transport == transports.AnalyticsAdminServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AnalyticsAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceClient),
)
@mock.patch.object(
    AnalyticsAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceAsyncClient),
)
def test_analytics_admin_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AnalyticsAdminServiceClient, "get_transport_class") as gtc:
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
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AnalyticsAdminServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceClient),
)
@mock.patch.object(
    AnalyticsAdminServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AnalyticsAdminServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_analytics_admin_service_client_mtls_env_auto(
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
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options_scopes(
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
        (
            AnalyticsAdminServiceClient,
            transports.AnalyticsAdminServiceGrpcTransport,
            "grpc",
        ),
        (
            AnalyticsAdminServiceAsyncClient,
            transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_analytics_admin_service_client_client_options_credentials_file(
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


def test_analytics_admin_service_client_client_options_from_dict():
    with mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AnalyticsAdminServiceClient(
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


def test_get_account(
    transport: str = "grpc", request_type=analytics_admin.GetAccountRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            region_code="region_code_value",
            deleted=True,
        )
        response = client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


def test_get_account_from_dict():
    test_get_account(request_type=dict)


def test_get_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        client.get_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()


@pytest.mark.asyncio
async def test_get_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                region_code="region_code_value",
                deleted=True,
            )
        )
        response = await client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


@pytest.mark.asyncio
async def test_get_account_async_from_dict():
    await test_get_account_async(request_type=dict)


def test_get_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        call.return_value = resources.Account()
        client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        await client.get_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_account(
            analytics_admin.GetAccountRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_account(
            analytics_admin.GetAccountRequest(), name="name_value",
        )


def test_list_accounts(
    transport: str = "grpc", request_type=analytics_admin.ListAccountsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAccountsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_accounts_from_dict():
    test_list_accounts(request_type=dict)


def test_list_accounts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        client.list_accounts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()


@pytest.mark.asyncio
async def test_list_accounts_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListAccountsRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAccountsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_accounts_async_from_dict():
    await test_list_accounts_async(request_type=dict)


def test_list_accounts_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_accounts(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Account) for i in results)


def test_list_accounts_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_accounts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_accounts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_accounts_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accounts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_accounts(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Account) for i in responses)


@pytest.mark.asyncio
async def test_list_accounts_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accounts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountsResponse(
                accounts=[
                    resources.Account(),
                    resources.Account(),
                    resources.Account(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountsResponse(accounts=[], next_page_token="def",),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountsResponse(
                accounts=[resources.Account(), resources.Account(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_accounts(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_account(
    transport: str = "grpc", request_type=analytics_admin.DeleteAccountRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_account_from_dict():
    test_delete_account(request_type=dict)


def test_delete_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        client.delete_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()


@pytest.mark.asyncio
async def test_delete_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.DeleteAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_account_async_from_dict():
    await test_delete_account_async(request_type=dict)


def test_delete_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        call.return_value = None
        client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_account(
            analytics_admin.DeleteAccountRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_account(
            analytics_admin.DeleteAccountRequest(), name="name_value",
        )


def test_update_account(
    transport: str = "grpc", request_type=analytics_admin.UpdateAccountRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account(
            name="name_value",
            display_name="display_name_value",
            region_code="region_code_value",
            deleted=True,
        )
        response = client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


def test_update_account_from_dict():
    test_update_account(request_type=dict)


def test_update_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        client.update_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()


@pytest.mark.asyncio
async def test_update_account_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.UpdateAccountRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Account(
                name="name_value",
                display_name="display_name_value",
                region_code="region_code_value",
                deleted=True,
            )
        )
        response = await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Account)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.region_code == "region_code_value"
    assert response.deleted is True


@pytest.mark.asyncio
async def test_update_account_async_from_dict():
    await test_update_account_async(request_type=dict)


def test_update_account_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()

    request.account.name = "account.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        call.return_value = resources.Account()
        client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account.name=account.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_account_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAccountRequest()

    request.account.name = "account.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        await client.update_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account.name=account.name/value",) in kw[
        "metadata"
    ]


def test_update_account_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].account == resources.Account(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_account_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_account_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_account), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Account()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Account())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_account(
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].account == resources.Account(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_account_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_account(
            analytics_admin.UpdateAccountRequest(),
            account=resources.Account(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_provision_account_ticket(
    transport: str = "grpc", request_type=analytics_admin.ProvisionAccountTicketRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ProvisionAccountTicketResponse(
            account_ticket_id="account_ticket_id_value",
        )
        response = client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)
    assert response.account_ticket_id == "account_ticket_id_value"


def test_provision_account_ticket_from_dict():
    test_provision_account_ticket(request_type=dict)


def test_provision_account_ticket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        client.provision_account_ticket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()


@pytest.mark.asyncio
async def test_provision_account_ticket_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ProvisionAccountTicketRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.provision_account_ticket), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ProvisionAccountTicketResponse(
                account_ticket_id="account_ticket_id_value",
            )
        )
        response = await client.provision_account_ticket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ProvisionAccountTicketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.ProvisionAccountTicketResponse)
    assert response.account_ticket_id == "account_ticket_id_value"


@pytest.mark.asyncio
async def test_provision_account_ticket_async_from_dict():
    await test_provision_account_ticket_async(request_type=dict)


def test_list_account_summaries(
    transport: str = "grpc", request_type=analytics_admin.ListAccountSummariesRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAccountSummariesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_account_summaries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountSummariesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_account_summaries_from_dict():
    test_list_account_summaries(request_type=dict)


def test_list_account_summaries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        client.list_account_summaries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()


@pytest.mark.asyncio
async def test_list_account_summaries_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListAccountSummariesRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAccountSummariesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_account_summaries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAccountSummariesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccountSummariesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_account_summaries_async_from_dict():
    await test_list_account_summaries_async(request_type=dict)


def test_list_account_summaries_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[], next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[resources.AccountSummary(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_account_summaries(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.AccountSummary) for i in results)


def test_list_account_summaries_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[], next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[resources.AccountSummary(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_account_summaries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_account_summaries_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[], next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[resources.AccountSummary(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_account_summaries(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AccountSummary) for i in responses)


@pytest.mark.asyncio
async def test_list_account_summaries_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_account_summaries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[], next_page_token="def",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[resources.AccountSummary(),], next_page_token="ghi",
            ),
            analytics_admin.ListAccountSummariesResponse(
                account_summaries=[
                    resources.AccountSummary(),
                    resources.AccountSummary(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_account_summaries(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_property(
    transport: str = "grpc", request_type=analytics_admin.GetPropertyRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
        )
        response = client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


def test_get_property_from_dict():
    test_get_property(request_type=dict)


def test_get_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        client.get_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()


@pytest.mark.asyncio
async def test_get_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetPropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
            )
        )
        response = await client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetPropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


@pytest.mark.asyncio
async def test_get_property_async_from_dict():
    await test_get_property_async(request_type=dict)


def test_get_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        call.return_value = resources.Property()
        client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetPropertyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.get_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_property(
            analytics_admin.GetPropertyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_property(
            analytics_admin.GetPropertyRequest(), name="name_value",
        )


def test_list_properties(
    transport: str = "grpc", request_type=analytics_admin.ListPropertiesRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListPropertiesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_properties_from_dict():
    test_list_properties(request_type=dict)


def test_list_properties_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        client.list_properties()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()


@pytest.mark.asyncio
async def test_list_properties_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListPropertiesRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListPropertiesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_properties(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListPropertiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPropertiesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_properties_async_from_dict():
    await test_list_properties_async(request_type=dict)


def test_list_properties_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_properties(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Property) for i in results)


def test_list_properties_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_properties), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_properties(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_properties_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_properties), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_properties(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Property) for i in responses)


@pytest.mark.asyncio
async def test_list_properties_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_properties), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListPropertiesResponse(
                properties=[
                    resources.Property(),
                    resources.Property(),
                    resources.Property(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[], next_page_token="def",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(),], next_page_token="ghi",
            ),
            analytics_admin.ListPropertiesResponse(
                properties=[resources.Property(), resources.Property(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_properties(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_property(
    transport: str = "grpc", request_type=analytics_admin.CreatePropertyRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
        )
        response = client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


def test_create_property_from_dict():
    test_create_property(request_type=dict)


def test_create_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        client.create_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()


@pytest.mark.asyncio
async def test_create_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.CreatePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
            )
        )
        response = await client.create_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


@pytest.mark.asyncio
async def test_create_property_async_from_dict():
    await test_create_property_async(request_type=dict)


def test_create_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_property(property=resources.Property(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].property == resources.Property(name="name_value")


def test_create_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_property(
            property=resources.Property(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].property == resources.Property(name="name_value")


@pytest.mark.asyncio
async def test_create_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_property(
            analytics_admin.CreatePropertyRequest(),
            property=resources.Property(name="name_value"),
        )


def test_delete_property(
    transport: str = "grpc", request_type=analytics_admin.DeletePropertyRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
        )
        response = client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


def test_delete_property_from_dict():
    test_delete_property(request_type=dict)


def test_delete_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        client.delete_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()


@pytest.mark.asyncio
async def test_delete_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.DeletePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
            )
        )
        response = await client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeletePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


@pytest.mark.asyncio
async def test_delete_property_async_from_dict():
    await test_delete_property_async(request_type=dict)


def test_delete_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        call.return_value = resources.Property()
        client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeletePropertyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.delete_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_property(
            analytics_admin.DeletePropertyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_property(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_property(
            analytics_admin.DeletePropertyRequest(), name="name_value",
        )


def test_update_property(
    transport: str = "grpc", request_type=analytics_admin.UpdatePropertyRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property(
            name="name_value",
            parent="parent_value",
            display_name="display_name_value",
            industry_category=resources.IndustryCategory.AUTOMOTIVE,
            time_zone="time_zone_value",
            currency_code="currency_code_value",
        )
        response = client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


def test_update_property_from_dict():
    test_update_property(request_type=dict)


def test_update_property_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        client.update_property()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()


@pytest.mark.asyncio
async def test_update_property_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.UpdatePropertyRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Property(
                name="name_value",
                parent="parent_value",
                display_name="display_name_value",
                industry_category=resources.IndustryCategory.AUTOMOTIVE,
                time_zone="time_zone_value",
                currency_code="currency_code_value",
            )
        )
        response = await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdatePropertyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Property)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.industry_category == resources.IndustryCategory.AUTOMOTIVE
    assert response.time_zone == "time_zone_value"
    assert response.currency_code == "currency_code_value"


@pytest.mark.asyncio
async def test_update_property_async_from_dict():
    await test_update_property_async(request_type=dict)


def test_update_property_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()

    request.property.name = "property.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        call.return_value = resources.Property()
        client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property.name=property.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_property_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdatePropertyRequest()

    request.property.name = "property.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        await client.update_property(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property.name=property.name/value",) in kw[
        "metadata"
    ]


def test_update_property_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].property == resources.Property(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_property_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_property_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_property), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Property()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Property())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_property(
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].property == resources.Property(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_property_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_property(
            analytics_admin.UpdatePropertyRequest(),
            property=resources.Property(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_user_link(
    transport: str = "grpc", request_type=analytics_admin.GetUserLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )
        response = client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


def test_get_user_link_from_dict():
    test_get_user_link(request_type=dict)


def test_get_user_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        client.get_user_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetUserLinkRequest()


@pytest.mark.asyncio
async def test_get_user_link_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetUserLinkRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )
        response = await client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_get_user_link_async_from_dict():
    await test_get_user_link_async(request_type=dict)


def test_get_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetUserLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        call.return_value = resources.UserLink()
        client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetUserLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        await client.get_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_user_link(
            analytics_admin.GetUserLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_user_link(
            analytics_admin.GetUserLinkRequest(), name="name_value",
        )


def test_batch_get_user_links(
    transport: str = "grpc", request_type=analytics_admin.BatchGetUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchGetUserLinksResponse()
        response = client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchGetUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchGetUserLinksResponse)


def test_batch_get_user_links_from_dict():
    test_batch_get_user_links(request_type=dict)


def test_batch_get_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_user_links), "__call__"
    ) as call:
        client.batch_get_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchGetUserLinksRequest()


@pytest.mark.asyncio
async def test_batch_get_user_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.BatchGetUserLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchGetUserLinksResponse()
        )
        response = await client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchGetUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchGetUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_get_user_links_async_from_dict():
    await test_batch_get_user_links_async(request_type=dict)


def test_batch_get_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchGetUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchGetUserLinksResponse()
        client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_get_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchGetUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_get_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchGetUserLinksResponse()
        )
        await client.batch_get_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_user_links(
    transport: str = "grpc", request_type=analytics_admin.ListUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUserLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_user_links_from_dict():
    test_list_user_links(request_type=dict)


def test_list_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        client.list_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListUserLinksRequest()


@pytest.mark.asyncio
async def test_list_user_links_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.ListUserLinksRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUserLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_user_links_async_from_dict():
    await test_list_user_links_async(request_type=dict)


def test_list_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        call.return_value = analytics_admin.ListUserLinksResponse()
        client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse()
        )
        await client.list_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_user_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_user_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_user_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_user_links(
            analytics_admin.ListUserLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_user_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListUserLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListUserLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_user_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_user_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_user_links(
            analytics_admin.ListUserLinksRequest(), parent="parent_value",
        )


def test_list_user_links_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_user_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.UserLink) for i in results)


def test_list_user_links_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_user_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_user_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_user_links), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_user_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.UserLink) for i in responses)


@pytest.mark.asyncio
async def test_list_user_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_user_links), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListUserLinksResponse(
                user_links=[
                    resources.UserLink(),
                    resources.UserLink(),
                    resources.UserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListUserLinksResponse(
                user_links=[resources.UserLink(), resources.UserLink(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_user_links(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_audit_user_links(
    transport: str = "grpc", request_type=analytics_admin.AuditUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.AuditUserLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AuditUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AuditUserLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_audit_user_links_from_dict():
    test_audit_user_links(request_type=dict)


def test_audit_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        client.audit_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AuditUserLinksRequest()


@pytest.mark.asyncio
async def test_audit_user_links_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.AuditUserLinksRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AuditUserLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.AuditUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AuditUserLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_audit_user_links_async_from_dict():
    await test_audit_user_links_async(request_type=dict)


def test_audit_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AuditUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        call.return_value = analytics_admin.AuditUserLinksResponse()
        client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_audit_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.AuditUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.AuditUserLinksResponse()
        )
        await client.audit_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_audit_user_links_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.audit_user_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.AuditUserLink) for i in results)


def test_audit_user_links_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.audit_user_links), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        pages = list(client.audit_user_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_audit_user_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.audit_user_links), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        async_pager = await client.audit_user_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AuditUserLink) for i in responses)


@pytest.mark.asyncio
async def test_audit_user_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.audit_user_links), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.AuditUserLinksResponse(
                user_links=[
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                    resources.AuditUserLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[], next_page_token="def",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(),], next_page_token="ghi",
            ),
            analytics_admin.AuditUserLinksResponse(
                user_links=[resources.AuditUserLink(), resources.AuditUserLink(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.audit_user_links(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_user_link(
    transport: str = "grpc", request_type=analytics_admin.CreateUserLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )
        response = client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


def test_create_user_link_from_dict():
    test_create_user_link(request_type=dict)


def test_create_user_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        client.create_user_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateUserLinkRequest()


@pytest.mark.asyncio
async def test_create_user_link_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.CreateUserLinkRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )
        response = await client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_create_user_link_async_from_dict():
    await test_create_user_link_async(request_type=dict)


def test_create_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateUserLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        call.return_value = resources.UserLink()
        client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateUserLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        await client.create_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_user_link(
            parent="parent_value", user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].user_link == resources.UserLink(name="name_value")


def test_create_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_user_link(
            analytics_admin.CreateUserLinkRequest(),
            parent="parent_value",
            user_link=resources.UserLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_user_link(
            parent="parent_value", user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].user_link == resources.UserLink(name="name_value")


@pytest.mark.asyncio
async def test_create_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_user_link(
            analytics_admin.CreateUserLinkRequest(),
            parent="parent_value",
            user_link=resources.UserLink(name="name_value"),
        )


def test_batch_create_user_links(
    transport: str = "grpc", request_type=analytics_admin.BatchCreateUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchCreateUserLinksResponse()
        response = client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchCreateUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchCreateUserLinksResponse)


def test_batch_create_user_links_from_dict():
    test_batch_create_user_links(request_type=dict)


def test_batch_create_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_user_links), "__call__"
    ) as call:
        client.batch_create_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchCreateUserLinksRequest()


@pytest.mark.asyncio
async def test_batch_create_user_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.BatchCreateUserLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchCreateUserLinksResponse()
        )
        response = await client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchCreateUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchCreateUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_create_user_links_async_from_dict():
    await test_batch_create_user_links_async(request_type=dict)


def test_batch_create_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchCreateUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchCreateUserLinksResponse()
        client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchCreateUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchCreateUserLinksResponse()
        )
        await client.batch_create_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_update_user_link(
    transport: str = "grpc", request_type=analytics_admin.UpdateUserLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink(
            name="name_value",
            email_address="email_address_value",
            direct_roles=["direct_roles_value"],
        )
        response = client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


def test_update_user_link_from_dict():
    test_update_user_link(request_type=dict)


def test_update_user_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        client.update_user_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateUserLinkRequest()


@pytest.mark.asyncio
async def test_update_user_link_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.UpdateUserLinkRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.UserLink(
                name="name_value",
                email_address="email_address_value",
                direct_roles=["direct_roles_value"],
            )
        )
        response = await client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.UserLink)
    assert response.name == "name_value"
    assert response.email_address == "email_address_value"
    assert response.direct_roles == ["direct_roles_value"]


@pytest.mark.asyncio
async def test_update_user_link_async_from_dict():
    await test_update_user_link_async(request_type=dict)


def test_update_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateUserLinkRequest()

    request.user_link.name = "user_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        call.return_value = resources.UserLink()
        client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "user_link.name=user_link.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateUserLinkRequest()

    request.user_link.name = "user_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        await client.update_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "user_link.name=user_link.name/value",) in kw[
        "metadata"
    ]


def test_update_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_user_link(user_link=resources.UserLink(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].user_link == resources.UserLink(name="name_value")


def test_update_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_user_link(
            analytics_admin.UpdateUserLinkRequest(),
            user_link=resources.UserLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.UserLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.UserLink())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_user_link(
            user_link=resources.UserLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].user_link == resources.UserLink(name="name_value")


@pytest.mark.asyncio
async def test_update_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_user_link(
            analytics_admin.UpdateUserLinkRequest(),
            user_link=resources.UserLink(name="name_value"),
        )


def test_batch_update_user_links(
    transport: str = "grpc", request_type=analytics_admin.BatchUpdateUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.BatchUpdateUserLinksResponse()
        response = client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchUpdateUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchUpdateUserLinksResponse)


def test_batch_update_user_links_from_dict():
    test_batch_update_user_links(request_type=dict)


def test_batch_update_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_user_links), "__call__"
    ) as call:
        client.batch_update_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchUpdateUserLinksRequest()


@pytest.mark.asyncio
async def test_batch_update_user_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.BatchUpdateUserLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchUpdateUserLinksResponse()
        )
        response = await client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchUpdateUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_admin.BatchUpdateUserLinksResponse)


@pytest.mark.asyncio
async def test_batch_update_user_links_async_from_dict():
    await test_batch_update_user_links_async(request_type=dict)


def test_batch_update_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchUpdateUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_user_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.BatchUpdateUserLinksResponse()
        client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_update_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchUpdateUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_update_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.BatchUpdateUserLinksResponse()
        )
        await client.batch_update_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_delete_user_link(
    transport: str = "grpc", request_type=analytics_admin.DeleteUserLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_user_link_from_dict():
    test_delete_user_link(request_type=dict)


def test_delete_user_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        client.delete_user_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteUserLinkRequest()


@pytest.mark.asyncio
async def test_delete_user_link_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.DeleteUserLinkRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteUserLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_user_link_async_from_dict():
    await test_delete_user_link_async(request_type=dict)


def test_delete_user_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteUserLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        call.return_value = None
        client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_user_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteUserLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_user_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_user_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_user_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_user_link(
            analytics_admin.DeleteUserLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_user_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_user_link), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_user_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_user_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_user_link(
            analytics_admin.DeleteUserLinkRequest(), name="name_value",
        )


def test_batch_delete_user_links(
    transport: str = "grpc", request_type=analytics_admin.BatchDeleteUserLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchDeleteUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_batch_delete_user_links_from_dict():
    test_batch_delete_user_links(request_type=dict)


def test_batch_delete_user_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_user_links), "__call__"
    ) as call:
        client.batch_delete_user_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchDeleteUserLinksRequest()


@pytest.mark.asyncio
async def test_batch_delete_user_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.BatchDeleteUserLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_user_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.BatchDeleteUserLinksRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_batch_delete_user_links_async_from_dict():
    await test_batch_delete_user_links_async(request_type=dict)


def test_batch_delete_user_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchDeleteUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_user_links), "__call__"
    ) as call:
        call.return_value = None
        client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_delete_user_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.BatchDeleteUserLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_delete_user_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.batch_delete_user_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_get_web_data_stream(
    transport: str = "grpc", request_type=analytics_admin.GetWebDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )
        response = client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


def test_get_web_data_stream_from_dict():
    test_get_web_data_stream(request_type=dict)


def test_get_web_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        client.get_web_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetWebDataStreamRequest()


@pytest.mark.asyncio
async def test_get_web_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetWebDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_web_data_stream_async_from_dict():
    await test_get_web_data_stream_async(request_type=dict)


def test_get_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetWebDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()
        client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetWebDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        await client.get_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_web_data_stream(
            analytics_admin.GetWebDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_web_data_stream(
            analytics_admin.GetWebDataStreamRequest(), name="name_value",
        )


def test_delete_web_data_stream(
    transport: str = "grpc", request_type=analytics_admin.DeleteWebDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_web_data_stream_from_dict():
    test_delete_web_data_stream(request_type=dict)


def test_delete_web_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        client.delete_web_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteWebDataStreamRequest()


@pytest.mark.asyncio
async def test_delete_web_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteWebDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_web_data_stream_async_from_dict():
    await test_delete_web_data_stream_async(request_type=dict)


def test_delete_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteWebDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        call.return_value = None
        client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteWebDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_web_data_stream(
            analytics_admin.DeleteWebDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_web_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_web_data_stream(
            analytics_admin.DeleteWebDataStreamRequest(), name="name_value",
        )


def test_update_web_data_stream(
    transport: str = "grpc", request_type=analytics_admin.UpdateWebDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )
        response = client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


def test_update_web_data_stream_from_dict():
    test_update_web_data_stream(request_type=dict)


def test_update_web_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        client.update_web_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateWebDataStreamRequest()


@pytest.mark.asyncio
async def test_update_web_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateWebDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )
        response = await client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_web_data_stream_async_from_dict():
    await test_update_web_data_stream_async(request_type=dict)


def test_update_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateWebDataStreamRequest()

    request.web_data_stream.name = "web_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()
        client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "web_data_stream.name=web_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateWebDataStreamRequest()

    request.web_data_stream.name = "web_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        await client.update_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "web_data_stream.name=web_data_stream.name/value",
    ) in kw["metadata"]


def test_update_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_web_data_stream(
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_web_data_stream(
            analytics_admin.UpdateWebDataStreamRequest(),
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_web_data_stream(
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_web_data_stream(
            analytics_admin.UpdateWebDataStreamRequest(),
            web_data_stream=resources.WebDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_web_data_stream(
    transport: str = "grpc", request_type=analytics_admin.CreateWebDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream(
            name="name_value",
            measurement_id="measurement_id_value",
            firebase_app_id="firebase_app_id_value",
            default_uri="default_uri_value",
            display_name="display_name_value",
        )
        response = client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


def test_create_web_data_stream_from_dict():
    test_create_web_data_stream(request_type=dict)


def test_create_web_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        client.create_web_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateWebDataStreamRequest()


@pytest.mark.asyncio
async def test_create_web_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateWebDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream(
                name="name_value",
                measurement_id="measurement_id_value",
                firebase_app_id="firebase_app_id_value",
                default_uri="default_uri_value",
                display_name="display_name_value",
            )
        )
        response = await client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateWebDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.WebDataStream)
    assert response.name == "name_value"
    assert response.measurement_id == "measurement_id_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.default_uri == "default_uri_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_web_data_stream_async_from_dict():
    await test_create_web_data_stream_async(request_type=dict)


def test_create_web_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateWebDataStreamRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        call.return_value = resources.WebDataStream()
        client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_web_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateWebDataStreamRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        await client.create_web_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_web_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_web_data_stream(
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")


def test_create_web_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_web_data_stream(
            analytics_admin.CreateWebDataStreamRequest(),
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_web_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_web_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.WebDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.WebDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_web_data_stream(
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].web_data_stream == resources.WebDataStream(name="name_value")


@pytest.mark.asyncio
async def test_create_web_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_web_data_stream(
            analytics_admin.CreateWebDataStreamRequest(),
            parent="parent_value",
            web_data_stream=resources.WebDataStream(name="name_value"),
        )


def test_list_web_data_streams(
    transport: str = "grpc", request_type=analytics_admin.ListWebDataStreamsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListWebDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWebDataStreamsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_web_data_streams_from_dict():
    test_list_web_data_streams(request_type=dict)


def test_list_web_data_streams_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        client.list_web_data_streams()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListWebDataStreamsRequest()


@pytest.mark.asyncio
async def test_list_web_data_streams_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListWebDataStreamsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListWebDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWebDataStreamsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_web_data_streams_async_from_dict():
    await test_list_web_data_streams_async(request_type=dict)


def test_list_web_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListWebDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListWebDataStreamsResponse()
        client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_web_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListWebDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse()
        )
        await client.list_web_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_web_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_web_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_web_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_web_data_streams(
            analytics_admin.ListWebDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_web_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListWebDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListWebDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_web_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_web_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_web_data_streams(
            analytics_admin.ListWebDataStreamsRequest(), parent="parent_value",
        )


def test_list_web_data_streams_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_web_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.WebDataStream) for i in results)


def test_list_web_data_streams_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_web_data_streams(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_web_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_web_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.WebDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_web_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_web_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[resources.WebDataStream(),], next_page_token="ghi",
            ),
            analytics_admin.ListWebDataStreamsResponse(
                web_data_streams=[
                    resources.WebDataStream(),
                    resources.WebDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_web_data_streams(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_ios_app_data_stream(
    transport: str = "grpc", request_type=analytics_admin.GetIosAppDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            bundle_id="bundle_id_value",
            display_name="display_name_value",
        )
        response = client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.bundle_id == "bundle_id_value"
    assert response.display_name == "display_name_value"


def test_get_ios_app_data_stream_from_dict():
    test_get_ios_app_data_stream(request_type=dict)


def test_get_ios_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        client.get_ios_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetIosAppDataStreamRequest()


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetIosAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                bundle_id="bundle_id_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.bundle_id == "bundle_id_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_async_from_dict():
    await test_get_ios_app_data_stream_async(request_type=dict)


def test_get_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetIosAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.IosAppDataStream()
        client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetIosAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        await client.get_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ios_app_data_stream(
            analytics_admin.GetIosAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_ios_app_data_stream(
            analytics_admin.GetIosAppDataStreamRequest(), name="name_value",
        )


def test_delete_ios_app_data_stream(
    transport: str = "grpc", request_type=analytics_admin.DeleteIosAppDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_ios_app_data_stream_from_dict():
    test_delete_ios_app_data_stream(request_type=dict)


def test_delete_ios_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        client.delete_ios_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteIosAppDataStreamRequest()


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteIosAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_async_from_dict():
    await test_delete_ios_app_data_stream_async(request_type=dict)


def test_delete_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteIosAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = None
        client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteIosAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_ios_app_data_stream(
            analytics_admin.DeleteIosAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_ios_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_ios_app_data_stream(
            analytics_admin.DeleteIosAppDataStreamRequest(), name="name_value",
        )


def test_update_ios_app_data_stream(
    transport: str = "grpc", request_type=analytics_admin.UpdateIosAppDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            bundle_id="bundle_id_value",
            display_name="display_name_value",
        )
        response = client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.bundle_id == "bundle_id_value"
    assert response.display_name == "display_name_value"


def test_update_ios_app_data_stream_from_dict():
    test_update_ios_app_data_stream(request_type=dict)


def test_update_ios_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        client.update_ios_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateIosAppDataStreamRequest()


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateIosAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                bundle_id="bundle_id_value",
                display_name="display_name_value",
            )
        )
        response = await client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateIosAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IosAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.bundle_id == "bundle_id_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_async_from_dict():
    await test_update_ios_app_data_stream_async(request_type=dict)


def test_update_ios_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateIosAppDataStreamRequest()

    request.ios_app_data_stream.name = "ios_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.IosAppDataStream()
        client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "ios_app_data_stream.name=ios_app_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateIosAppDataStreamRequest()

    request.ios_app_data_stream.name = "ios_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        await client.update_ios_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "ios_app_data_stream.name=ios_app_data_stream.name/value",
    ) in kw["metadata"]


def test_update_ios_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_ios_app_data_stream(
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_ios_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_ios_app_data_stream(
            analytics_admin.UpdateIosAppDataStreamRequest(),
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ios_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IosAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IosAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_ios_app_data_stream(
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].ios_app_data_stream == resources.IosAppDataStream(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_ios_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_ios_app_data_stream(
            analytics_admin.UpdateIosAppDataStreamRequest(),
            ios_app_data_stream=resources.IosAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_list_ios_app_data_streams(
    transport: str = "grpc", request_type=analytics_admin.ListIosAppDataStreamsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListIosAppDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIosAppDataStreamsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_ios_app_data_streams_from_dict():
    test_list_ios_app_data_streams(request_type=dict)


def test_list_ios_app_data_streams_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        client.list_ios_app_data_streams()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListIosAppDataStreamsRequest()


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListIosAppDataStreamsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListIosAppDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListIosAppDataStreamsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async_from_dict():
    await test_list_ios_app_data_streams_async(request_type=dict)


def test_list_ios_app_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListIosAppDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()
        client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListIosAppDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse()
        )
        await client.list_ios_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_ios_app_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_ios_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_ios_app_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_ios_app_data_streams(
            analytics_admin.ListIosAppDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListIosAppDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListIosAppDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_ios_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_ios_app_data_streams(
            analytics_admin.ListIosAppDataStreamsRequest(), parent="parent_value",
        )


def test_list_ios_app_data_streams_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_ios_app_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.IosAppDataStream) for i in results)


def test_list_ios_app_data_streams_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_ios_app_data_streams(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_ios_app_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.IosAppDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_ios_app_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ios_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[resources.IosAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListIosAppDataStreamsResponse(
                ios_app_data_streams=[
                    resources.IosAppDataStream(),
                    resources.IosAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_ios_app_data_streams(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_android_app_data_stream(
    transport: str = "grpc", request_type=analytics_admin.GetAndroidAppDataStreamRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            package_name="package_name_value",
            display_name="display_name_value",
        )
        response = client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.package_name == "package_name_value"
    assert response.display_name == "display_name_value"


def test_get_android_app_data_stream_from_dict():
    test_get_android_app_data_stream(request_type=dict)


def test_get_android_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        client.get_android_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAndroidAppDataStreamRequest()


@pytest.mark.asyncio
async def test_get_android_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetAndroidAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                package_name="package_name_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.package_name == "package_name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_android_app_data_stream_async_from_dict():
    await test_get_android_app_data_stream_async(request_type=dict)


def test_get_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAndroidAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.AndroidAppDataStream()
        client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetAndroidAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        await client.get_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_android_app_data_stream(
            analytics_admin.GetAndroidAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_android_app_data_stream(
            analytics_admin.GetAndroidAppDataStreamRequest(), name="name_value",
        )


def test_delete_android_app_data_stream(
    transport: str = "grpc",
    request_type=analytics_admin.DeleteAndroidAppDataStreamRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_android_app_data_stream_from_dict():
    test_delete_android_app_data_stream(request_type=dict)


def test_delete_android_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        client.delete_android_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAndroidAppDataStreamRequest()


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteAndroidAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_async_from_dict():
    await test_delete_android_app_data_stream_async(request_type=dict)


def test_delete_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = None
        client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteAndroidAppDataStreamRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_android_app_data_stream(
            analytics_admin.DeleteAndroidAppDataStreamRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_android_app_data_stream(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_android_app_data_stream(
            analytics_admin.DeleteAndroidAppDataStreamRequest(), name="name_value",
        )


def test_update_android_app_data_stream(
    transport: str = "grpc",
    request_type=analytics_admin.UpdateAndroidAppDataStreamRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream(
            name="name_value",
            firebase_app_id="firebase_app_id_value",
            package_name="package_name_value",
            display_name="display_name_value",
        )
        response = client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.package_name == "package_name_value"
    assert response.display_name == "display_name_value"


def test_update_android_app_data_stream_from_dict():
    test_update_android_app_data_stream(request_type=dict)


def test_update_android_app_data_stream_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        client.update_android_app_data_stream()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAndroidAppDataStreamRequest()


@pytest.mark.asyncio
async def test_update_android_app_data_stream_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateAndroidAppDataStreamRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream(
                name="name_value",
                firebase_app_id="firebase_app_id_value",
                package_name="package_name_value",
                display_name="display_name_value",
            )
        )
        response = await client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateAndroidAppDataStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.AndroidAppDataStream)
    assert response.name == "name_value"
    assert response.firebase_app_id == "firebase_app_id_value"
    assert response.package_name == "package_name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_android_app_data_stream_async_from_dict():
    await test_update_android_app_data_stream_async(request_type=dict)


def test_update_android_app_data_stream_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()

    request.android_app_data_stream.name = "android_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = resources.AndroidAppDataStream()
        client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "android_app_data_stream.name=android_app_data_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_android_app_data_stream_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateAndroidAppDataStreamRequest()

    request.android_app_data_stream.name = "android_app_data_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        await client.update_android_app_data_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "android_app_data_stream.name=android_app_data_stream.name/value",
    ) in kw["metadata"]


def test_update_android_app_data_stream_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_android_app_data_stream(
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_android_app_data_stream_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_android_app_data_stream(
            analytics_admin.UpdateAndroidAppDataStreamRequest(),
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_android_app_data_stream_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_android_app_data_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.AndroidAppDataStream()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.AndroidAppDataStream()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_android_app_data_stream(
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].android_app_data_stream == resources.AndroidAppDataStream(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_android_app_data_stream_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_android_app_data_stream(
            analytics_admin.UpdateAndroidAppDataStreamRequest(),
            android_app_data_stream=resources.AndroidAppDataStream(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_list_android_app_data_streams(
    transport: str = "grpc",
    request_type=analytics_admin.ListAndroidAppDataStreamsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAndroidAppDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAndroidAppDataStreamsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_android_app_data_streams_from_dict():
    test_list_android_app_data_streams(request_type=dict)


def test_list_android_app_data_streams_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        client.list_android_app_data_streams()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAndroidAppDataStreamsRequest()


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListAndroidAppDataStreamsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListAndroidAppDataStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAndroidAppDataStreamsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async_from_dict():
    await test_list_android_app_data_streams_async(request_type=dict)


def test_list_android_app_data_streams_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()
        client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_android_app_data_streams_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListAndroidAppDataStreamsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse()
        )
        await client.list_android_app_data_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_android_app_data_streams_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_android_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_android_app_data_streams_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_android_app_data_streams(
            analytics_admin.ListAndroidAppDataStreamsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_android_app_data_streams_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListAndroidAppDataStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListAndroidAppDataStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_android_app_data_streams(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_android_app_data_streams_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_android_app_data_streams(
            analytics_admin.ListAndroidAppDataStreamsRequest(), parent="parent_value",
        )


def test_list_android_app_data_streams_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_android_app_data_streams(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.AndroidAppDataStream) for i in results)


def test_list_android_app_data_streams_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_android_app_data_streams(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_android_app_data_streams(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.AndroidAppDataStream) for i in responses)


@pytest.mark.asyncio
async def test_list_android_app_data_streams_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_android_app_data_streams),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[], next_page_token="def",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[resources.AndroidAppDataStream(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListAndroidAppDataStreamsResponse(
                android_app_data_streams=[
                    resources.AndroidAppDataStream(),
                    resources.AndroidAppDataStream(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_android_app_data_streams(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_enhanced_measurement_settings(
    transport: str = "grpc",
    request_type=analytics_admin.GetEnhancedMeasurementSettingsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings(
            name="name_value",
            stream_enabled=True,
            page_views_enabled=True,
            scrolls_enabled=True,
            outbound_clicks_enabled=True,
            site_search_enabled=True,
            video_engagement_enabled=True,
            file_downloads_enabled=True,
            page_loads_enabled=True,
            page_changes_enabled=True,
            search_query_parameter="search_query_parameter_value",
            uri_query_parameter="uri_query_parameter_value",
        )
        response = client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetEnhancedMeasurementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)
    assert response.name == "name_value"
    assert response.stream_enabled is True
    assert response.page_views_enabled is True
    assert response.scrolls_enabled is True
    assert response.outbound_clicks_enabled is True
    assert response.site_search_enabled is True
    assert response.video_engagement_enabled is True
    assert response.file_downloads_enabled is True
    assert response.page_loads_enabled is True
    assert response.page_changes_enabled is True
    assert response.search_query_parameter == "search_query_parameter_value"
    assert response.uri_query_parameter == "uri_query_parameter_value"


def test_get_enhanced_measurement_settings_from_dict():
    test_get_enhanced_measurement_settings(request_type=dict)


def test_get_enhanced_measurement_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        client.get_enhanced_measurement_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetEnhancedMeasurementSettingsRequest()


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetEnhancedMeasurementSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings(
                name="name_value",
                stream_enabled=True,
                page_views_enabled=True,
                scrolls_enabled=True,
                outbound_clicks_enabled=True,
                site_search_enabled=True,
                video_engagement_enabled=True,
                file_downloads_enabled=True,
                page_loads_enabled=True,
                page_changes_enabled=True,
                search_query_parameter="search_query_parameter_value",
                uri_query_parameter="uri_query_parameter_value",
            )
        )
        response = await client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetEnhancedMeasurementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)
    assert response.name == "name_value"
    assert response.stream_enabled is True
    assert response.page_views_enabled is True
    assert response.scrolls_enabled is True
    assert response.outbound_clicks_enabled is True
    assert response.site_search_enabled is True
    assert response.video_engagement_enabled is True
    assert response.file_downloads_enabled is True
    assert response.page_loads_enabled is True
    assert response.page_changes_enabled is True
    assert response.search_query_parameter == "search_query_parameter_value"
    assert response.uri_query_parameter == "uri_query_parameter_value"


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_async_from_dict():
    await test_get_enhanced_measurement_settings_async(request_type=dict)


def test_get_enhanced_measurement_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = resources.EnhancedMeasurementSettings()
        client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetEnhancedMeasurementSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        await client.get_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_enhanced_measurement_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_enhanced_measurement_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_enhanced_measurement_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_enhanced_measurement_settings(
            analytics_admin.GetEnhancedMeasurementSettingsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_enhanced_measurement_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_enhanced_measurement_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_enhanced_measurement_settings(
            analytics_admin.GetEnhancedMeasurementSettingsRequest(), name="name_value",
        )


def test_update_enhanced_measurement_settings(
    transport: str = "grpc",
    request_type=analytics_admin.UpdateEnhancedMeasurementSettingsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings(
            name="name_value",
            stream_enabled=True,
            page_views_enabled=True,
            scrolls_enabled=True,
            outbound_clicks_enabled=True,
            site_search_enabled=True,
            video_engagement_enabled=True,
            file_downloads_enabled=True,
            page_loads_enabled=True,
            page_changes_enabled=True,
            search_query_parameter="search_query_parameter_value",
            uri_query_parameter="uri_query_parameter_value",
        )
        response = client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)
    assert response.name == "name_value"
    assert response.stream_enabled is True
    assert response.page_views_enabled is True
    assert response.scrolls_enabled is True
    assert response.outbound_clicks_enabled is True
    assert response.site_search_enabled is True
    assert response.video_engagement_enabled is True
    assert response.file_downloads_enabled is True
    assert response.page_loads_enabled is True
    assert response.page_changes_enabled is True
    assert response.search_query_parameter == "search_query_parameter_value"
    assert response.uri_query_parameter == "uri_query_parameter_value"


def test_update_enhanced_measurement_settings_from_dict():
    test_update_enhanced_measurement_settings(request_type=dict)


def test_update_enhanced_measurement_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        client.update_enhanced_measurement_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateEnhancedMeasurementSettingsRequest()


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateEnhancedMeasurementSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings(
                name="name_value",
                stream_enabled=True,
                page_views_enabled=True,
                scrolls_enabled=True,
                outbound_clicks_enabled=True,
                site_search_enabled=True,
                video_engagement_enabled=True,
                file_downloads_enabled=True,
                page_loads_enabled=True,
                page_changes_enabled=True,
                search_query_parameter="search_query_parameter_value",
                uri_query_parameter="uri_query_parameter_value",
            )
        )
        response = await client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.EnhancedMeasurementSettings)
    assert response.name == "name_value"
    assert response.stream_enabled is True
    assert response.page_views_enabled is True
    assert response.scrolls_enabled is True
    assert response.outbound_clicks_enabled is True
    assert response.site_search_enabled is True
    assert response.video_engagement_enabled is True
    assert response.file_downloads_enabled is True
    assert response.page_loads_enabled is True
    assert response.page_changes_enabled is True
    assert response.search_query_parameter == "search_query_parameter_value"
    assert response.uri_query_parameter == "uri_query_parameter_value"


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_async_from_dict():
    await test_update_enhanced_measurement_settings_async(request_type=dict)


def test_update_enhanced_measurement_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    request.enhanced_measurement_settings.name = (
        "enhanced_measurement_settings.name/value"
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = resources.EnhancedMeasurementSettings()
        client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "enhanced_measurement_settings.name=enhanced_measurement_settings.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest()

    request.enhanced_measurement_settings.name = (
        "enhanced_measurement_settings.name/value"
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        await client.update_enhanced_measurement_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "enhanced_measurement_settings.name=enhanced_measurement_settings.name/value",
    ) in kw["metadata"]


def test_update_enhanced_measurement_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_enhanced_measurement_settings(
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].enhanced_measurement_settings == resources.EnhancedMeasurementSettings(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_enhanced_measurement_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_enhanced_measurement_settings(
            analytics_admin.UpdateEnhancedMeasurementSettingsRequest(),
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_enhanced_measurement_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.EnhancedMeasurementSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.EnhancedMeasurementSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_enhanced_measurement_settings(
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].enhanced_measurement_settings == resources.EnhancedMeasurementSettings(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_enhanced_measurement_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_enhanced_measurement_settings(
            analytics_admin.UpdateEnhancedMeasurementSettingsRequest(),
            enhanced_measurement_settings=resources.EnhancedMeasurementSettings(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_firebase_link(
    transport: str = "grpc", request_type=analytics_admin.CreateFirebaseLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink(
            name="name_value",
            project="project_value",
            maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
        )
        response = client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


def test_create_firebase_link_from_dict():
    test_create_firebase_link(request_type=dict)


def test_create_firebase_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        client.create_firebase_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()


@pytest.mark.asyncio
async def test_create_firebase_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateFirebaseLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink(
                name="name_value",
                project="project_value",
                maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
            )
        )
        response = await client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


@pytest.mark.asyncio
async def test_create_firebase_link_async_from_dict():
    await test_create_firebase_link_async(request_type=dict)


def test_create_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = resources.FirebaseLink()
        client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateFirebaseLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        await client.create_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")


def test_create_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_firebase_link(
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")


@pytest.mark.asyncio
async def test_create_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_firebase_link(
            analytics_admin.CreateFirebaseLinkRequest(),
            parent="parent_value",
            firebase_link=resources.FirebaseLink(name="name_value"),
        )


def test_update_firebase_link(
    transport: str = "grpc", request_type=analytics_admin.UpdateFirebaseLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink(
            name="name_value",
            project="project_value",
            maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
        )
        response = client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


def test_update_firebase_link_from_dict():
    test_update_firebase_link(request_type=dict)


def test_update_firebase_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        client.update_firebase_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateFirebaseLinkRequest()


@pytest.mark.asyncio
async def test_update_firebase_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateFirebaseLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink(
                name="name_value",
                project="project_value",
                maximum_user_access=resources.MaximumUserAccess.NO_ACCESS,
            )
        )
        response = await client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.FirebaseLink)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.maximum_user_access == resources.MaximumUserAccess.NO_ACCESS


@pytest.mark.asyncio
async def test_update_firebase_link_async_from_dict():
    await test_update_firebase_link_async(request_type=dict)


def test_update_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateFirebaseLinkRequest()

    request.firebase_link.name = "firebase_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        call.return_value = resources.FirebaseLink()
        client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "firebase_link.name=firebase_link.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateFirebaseLinkRequest()

    request.firebase_link.name = "firebase_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        await client.update_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "firebase_link.name=firebase_link.name/value",
    ) in kw["metadata"]


def test_update_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_firebase_link(
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_firebase_link(
            analytics_admin.UpdateFirebaseLinkRequest(),
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.FirebaseLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.FirebaseLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_firebase_link(
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].firebase_link == resources.FirebaseLink(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_firebase_link(
            analytics_admin.UpdateFirebaseLinkRequest(),
            firebase_link=resources.FirebaseLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_firebase_link(
    transport: str = "grpc", request_type=analytics_admin.DeleteFirebaseLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_firebase_link_from_dict():
    test_delete_firebase_link(request_type=dict)


def test_delete_firebase_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        client.delete_firebase_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()


@pytest.mark.asyncio
async def test_delete_firebase_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteFirebaseLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteFirebaseLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_firebase_link_async_from_dict():
    await test_delete_firebase_link_async(request_type=dict)


def test_delete_firebase_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_firebase_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteFirebaseLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_firebase_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_firebase_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_firebase_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_firebase_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_firebase_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_firebase_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_firebase_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_firebase_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_firebase_link(
            analytics_admin.DeleteFirebaseLinkRequest(), name="name_value",
        )


def test_list_firebase_links(
    transport: str = "grpc", request_type=analytics_admin.ListFirebaseLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFirebaseLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_firebase_links_from_dict():
    test_list_firebase_links(request_type=dict)


def test_list_firebase_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        client.list_firebase_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()


@pytest.mark.asyncio
async def test_list_firebase_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListFirebaseLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListFirebaseLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFirebaseLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_firebase_links_async_from_dict():
    await test_list_firebase_links_async(request_type=dict)


def test_list_firebase_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListFirebaseLinksResponse()
        client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_firebase_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListFirebaseLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )
        await client.list_firebase_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_firebase_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_firebase_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_firebase_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_firebase_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListFirebaseLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListFirebaseLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_firebase_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_firebase_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_firebase_links(
            analytics_admin.ListFirebaseLinksRequest(), parent="parent_value",
        )


def test_list_firebase_links_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[], next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(), resources.FirebaseLink(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_firebase_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.FirebaseLink) for i in results)


def test_list_firebase_links_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[], next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(), resources.FirebaseLink(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_firebase_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_firebase_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[], next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(), resources.FirebaseLink(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_firebase_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.FirebaseLink) for i in responses)


@pytest.mark.asyncio
async def test_list_firebase_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_firebase_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                    resources.FirebaseLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[], next_page_token="def",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListFirebaseLinksResponse(
                firebase_links=[resources.FirebaseLink(), resources.FirebaseLink(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_firebase_links(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_global_site_tag(
    transport: str = "grpc", request_type=analytics_admin.GetGlobalSiteTagRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag(
            name="name_value", snippet="snippet_value",
        )
        response = client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGlobalSiteTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GlobalSiteTag)
    assert response.name == "name_value"
    assert response.snippet == "snippet_value"


def test_get_global_site_tag_from_dict():
    test_get_global_site_tag(request_type=dict)


def test_get_global_site_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        client.get_global_site_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGlobalSiteTagRequest()


@pytest.mark.asyncio
async def test_get_global_site_tag_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetGlobalSiteTagRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag(name="name_value", snippet="snippet_value",)
        )
        response = await client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGlobalSiteTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GlobalSiteTag)
    assert response.name == "name_value"
    assert response.snippet == "snippet_value"


@pytest.mark.asyncio
async def test_get_global_site_tag_async_from_dict():
    await test_get_global_site_tag_async(request_type=dict)


def test_get_global_site_tag_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGlobalSiteTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        call.return_value = resources.GlobalSiteTag()
        client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_global_site_tag_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGlobalSiteTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag()
        )
        await client.get_global_site_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_global_site_tag_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_global_site_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_global_site_tag_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_global_site_tag(
            analytics_admin.GetGlobalSiteTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_global_site_tag_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_global_site_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GlobalSiteTag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GlobalSiteTag()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_global_site_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_global_site_tag_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_global_site_tag(
            analytics_admin.GetGlobalSiteTagRequest(), name="name_value",
        )


def test_create_google_ads_link(
    transport: str = "grpc", request_type=analytics_admin.CreateGoogleAdsLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            email_address="email_address_value",
        )
        response = client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.email_address == "email_address_value"


def test_create_google_ads_link_from_dict():
    test_create_google_ads_link(request_type=dict)


def test_create_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        client.create_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_create_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                email_address="email_address_value",
            )
        )
        response = await client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.email_address == "email_address_value"


@pytest.mark.asyncio
async def test_create_google_ads_link_async_from_dict():
    await test_create_google_ads_link_async(request_type=dict)


def test_create_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()
        client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateGoogleAdsLinkRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        await client.create_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")


def test_create_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_google_ads_link(
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")


@pytest.mark.asyncio
async def test_create_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_google_ads_link(
            analytics_admin.CreateGoogleAdsLinkRequest(),
            parent="parent_value",
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
        )


def test_update_google_ads_link(
    transport: str = "grpc", request_type=analytics_admin.UpdateGoogleAdsLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink(
            name="name_value",
            customer_id="customer_id_value",
            can_manage_clients=True,
            email_address="email_address_value",
        )
        response = client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.email_address == "email_address_value"


def test_update_google_ads_link_from_dict():
    test_update_google_ads_link(request_type=dict)


def test_update_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        client.update_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_update_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink(
                name="name_value",
                customer_id="customer_id_value",
                can_manage_clients=True,
                email_address="email_address_value",
            )
        )
        response = await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleAdsLink)
    assert response.name == "name_value"
    assert response.customer_id == "customer_id_value"
    assert response.can_manage_clients is True
    assert response.email_address == "email_address_value"


@pytest.mark.asyncio
async def test_update_google_ads_link_async_from_dict():
    await test_update_google_ads_link_async(request_type=dict)


def test_update_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    request.google_ads_link.name = "google_ads_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = resources.GoogleAdsLink()
        client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=google_ads_link.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleAdsLinkRequest()

    request.google_ads_link.name = "google_ads_link.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        await client.update_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_ads_link.name=google_ads_link.name/value",
    ) in kw["metadata"]


def test_update_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleAdsLink()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleAdsLink()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_google_ads_link(
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].google_ads_link == resources.GoogleAdsLink(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_google_ads_link(
            analytics_admin.UpdateGoogleAdsLinkRequest(),
            google_ads_link=resources.GoogleAdsLink(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_google_ads_link(
    transport: str = "grpc", request_type=analytics_admin.DeleteGoogleAdsLinkRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_google_ads_link_from_dict():
    test_delete_google_ads_link(request_type=dict)


def test_delete_google_ads_link_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        client.delete_google_ads_link()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()


@pytest.mark.asyncio
async def test_delete_google_ads_link_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteGoogleAdsLinkRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteGoogleAdsLinkRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_google_ads_link_async_from_dict():
    await test_delete_google_ads_link_async(request_type=dict)


def test_delete_google_ads_link_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = None
        client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_google_ads_link_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteGoogleAdsLinkRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_google_ads_link(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_google_ads_link_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_google_ads_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_google_ads_link_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_google_ads_link_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_google_ads_link), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_google_ads_link(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_google_ads_link_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_google_ads_link(
            analytics_admin.DeleteGoogleAdsLinkRequest(), name="name_value",
        )


def test_list_google_ads_links(
    transport: str = "grpc", request_type=analytics_admin.ListGoogleAdsLinksRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_google_ads_links_from_dict():
    test_list_google_ads_links(request_type=dict)


def test_list_google_ads_links_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        client.list_google_ads_links()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()


@pytest.mark.asyncio
async def test_list_google_ads_links_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListGoogleAdsLinksRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListGoogleAdsLinksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGoogleAdsLinksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_google_ads_links_async_from_dict():
    await test_list_google_ads_links_async(request_type=dict)


def test_list_google_ads_links_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()
        client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_google_ads_links_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListGoogleAdsLinksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )
        await client.list_google_ads_links(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_google_ads_links_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_google_ads_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_google_ads_links_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_google_ads_links_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListGoogleAdsLinksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListGoogleAdsLinksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_google_ads_links(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_google_ads_links_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_google_ads_links(
            analytics_admin.ListGoogleAdsLinksRequest(), parent="parent_value",
        )


def test_list_google_ads_links_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_google_ads_links(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in results)


def test_list_google_ads_links_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_google_ads_links(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_google_ads_links(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.GoogleAdsLink) for i in responses)


@pytest.mark.asyncio
async def test_list_google_ads_links_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_google_ads_links),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[], next_page_token="def",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[resources.GoogleAdsLink(),], next_page_token="ghi",
            ),
            analytics_admin.ListGoogleAdsLinksResponse(
                google_ads_links=[
                    resources.GoogleAdsLink(),
                    resources.GoogleAdsLink(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_google_ads_links(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_data_sharing_settings(
    transport: str = "grpc", request_type=analytics_admin.GetDataSharingSettingsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings(
            name="name_value",
            sharing_with_google_support_enabled=True,
            sharing_with_google_assigned_sales_enabled=True,
            sharing_with_google_any_sales_enabled=True,
            sharing_with_google_products_enabled=True,
            sharing_with_others_enabled=True,
        )
        response = client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)
    assert response.name == "name_value"
    assert response.sharing_with_google_support_enabled is True
    assert response.sharing_with_google_assigned_sales_enabled is True
    assert response.sharing_with_google_any_sales_enabled is True
    assert response.sharing_with_google_products_enabled is True
    assert response.sharing_with_others_enabled is True


def test_get_data_sharing_settings_from_dict():
    test_get_data_sharing_settings(request_type=dict)


def test_get_data_sharing_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        client.get_data_sharing_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()


@pytest.mark.asyncio
async def test_get_data_sharing_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetDataSharingSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings(
                name="name_value",
                sharing_with_google_support_enabled=True,
                sharing_with_google_assigned_sales_enabled=True,
                sharing_with_google_any_sales_enabled=True,
                sharing_with_google_products_enabled=True,
                sharing_with_others_enabled=True,
            )
        )
        response = await client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetDataSharingSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DataSharingSettings)
    assert response.name == "name_value"
    assert response.sharing_with_google_support_enabled is True
    assert response.sharing_with_google_assigned_sales_enabled is True
    assert response.sharing_with_google_any_sales_enabled is True
    assert response.sharing_with_google_products_enabled is True
    assert response.sharing_with_others_enabled is True


@pytest.mark.asyncio
async def test_get_data_sharing_settings_async_from_dict():
    await test_get_data_sharing_settings_async(request_type=dict)


def test_get_data_sharing_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = resources.DataSharingSettings()
        client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_data_sharing_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetDataSharingSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )
        await client.get_data_sharing_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_data_sharing_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_data_sharing_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_data_sharing_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_data_sharing_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_data_sharing_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DataSharingSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DataSharingSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_data_sharing_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_data_sharing_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_data_sharing_settings(
            analytics_admin.GetDataSharingSettingsRequest(), name="name_value",
        )


def test_get_measurement_protocol_secret(
    transport: str = "grpc",
    request_type=analytics_admin.GetMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_get_measurement_protocol_secret_from_dict():
    test_get_measurement_protocol_secret(request_type=dict)


def test_get_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        client.get_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_async_from_dict():
    await test_get_measurement_protocol_secret_async(request_type=dict)


def test_get_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetMeasurementProtocolSecretRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetMeasurementProtocolSecretRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.get_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_measurement_protocol_secret(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_measurement_protocol_secret(
            analytics_admin.GetMeasurementProtocolSecretRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_measurement_protocol_secret(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_measurement_protocol_secret(
            analytics_admin.GetMeasurementProtocolSecretRequest(), name="name_value",
        )


def test_list_measurement_protocol_secrets(
    transport: str = "grpc",
    request_type=analytics_admin.ListMeasurementProtocolSecretsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeasurementProtocolSecretsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_measurement_protocol_secrets_from_dict():
    test_list_measurement_protocol_secrets(request_type=dict)


def test_list_measurement_protocol_secrets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        client.list_measurement_protocol_secrets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListMeasurementProtocolSecretsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListMeasurementProtocolSecretsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMeasurementProtocolSecretsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_from_dict():
    await test_list_measurement_protocol_secrets_async(request_type=dict)


def test_list_measurement_protocol_secrets_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListMeasurementProtocolSecretsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()
        client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListMeasurementProtocolSecretsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse()
        )
        await client.list_measurement_protocol_secrets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_measurement_protocol_secrets_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_measurement_protocol_secrets(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_measurement_protocol_secrets_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_measurement_protocol_secrets(
            analytics_admin.ListMeasurementProtocolSecretsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListMeasurementProtocolSecretsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListMeasurementProtocolSecretsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_measurement_protocol_secrets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_measurement_protocol_secrets(
            analytics_admin.ListMeasurementProtocolSecretsRequest(),
            parent="parent_value",
        )


def test_list_measurement_protocol_secrets_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[], next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[resources.MeasurementProtocolSecret(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_measurement_protocol_secrets(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.MeasurementProtocolSecret) for i in results)


def test_list_measurement_protocol_secrets_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[], next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[resources.MeasurementProtocolSecret(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_measurement_protocol_secrets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[], next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[resources.MeasurementProtocolSecret(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_measurement_protocol_secrets(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, resources.MeasurementProtocolSecret) for i in responses
        )


@pytest.mark.asyncio
async def test_list_measurement_protocol_secrets_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_measurement_protocol_secrets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[], next_page_token="def",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[resources.MeasurementProtocolSecret(),],
                next_page_token="ghi",
            ),
            analytics_admin.ListMeasurementProtocolSecretsResponse(
                measurement_protocol_secrets=[
                    resources.MeasurementProtocolSecret(),
                    resources.MeasurementProtocolSecret(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_measurement_protocol_secrets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_measurement_protocol_secret(
    transport: str = "grpc",
    request_type=analytics_admin.CreateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_create_measurement_protocol_secret_from_dict():
    test_create_measurement_protocol_secret(request_type=dict)


def test_create_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        client.create_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_async_from_dict():
    await test_create_measurement_protocol_secret_async(request_type=dict)


def test_create_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateMeasurementProtocolSecretRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateMeasurementProtocolSecretRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.create_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_measurement_protocol_secret(
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[
            0
        ].measurement_protocol_secret == resources.MeasurementProtocolSecret(
            name="name_value"
        )


def test_create_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_measurement_protocol_secret(
            analytics_admin.CreateMeasurementProtocolSecretRequest(),
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_measurement_protocol_secret(
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[
            0
        ].measurement_protocol_secret == resources.MeasurementProtocolSecret(
            name="name_value"
        )


@pytest.mark.asyncio
async def test_create_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_measurement_protocol_secret(
            analytics_admin.CreateMeasurementProtocolSecretRequest(),
            parent="parent_value",
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
        )


def test_delete_measurement_protocol_secret(
    transport: str = "grpc",
    request_type=analytics_admin.DeleteMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_measurement_protocol_secret_from_dict():
    test_delete_measurement_protocol_secret(request_type=dict)


def test_delete_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        client.delete_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_async_from_dict():
    await test_delete_measurement_protocol_secret_async(request_type=dict)


def test_delete_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteMeasurementProtocolSecretRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = None
        client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteMeasurementProtocolSecretRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_measurement_protocol_secret(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_measurement_protocol_secret(
            analytics_admin.DeleteMeasurementProtocolSecretRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_measurement_protocol_secret(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_measurement_protocol_secret(
            analytics_admin.DeleteMeasurementProtocolSecretRequest(), name="name_value",
        )


def test_update_measurement_protocol_secret(
    transport: str = "grpc",
    request_type=analytics_admin.UpdateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret(
            name="name_value",
            display_name="display_name_value",
            secret_value="secret_value_value",
        )
        response = client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


def test_update_measurement_protocol_secret_from_dict():
    test_update_measurement_protocol_secret(request_type=dict)


def test_update_measurement_protocol_secret_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        client.update_measurement_protocol_secret()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateMeasurementProtocolSecretRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret(
                name="name_value",
                display_name="display_name_value",
                secret_value="secret_value_value",
            )
        )
        response = await client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateMeasurementProtocolSecretRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.MeasurementProtocolSecret)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.secret_value == "secret_value_value"


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_async_from_dict():
    await test_update_measurement_protocol_secret_async(request_type=dict)


def test_update_measurement_protocol_secret_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateMeasurementProtocolSecretRequest()

    request.measurement_protocol_secret.name = "measurement_protocol_secret.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = resources.MeasurementProtocolSecret()
        client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "measurement_protocol_secret.name=measurement_protocol_secret.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateMeasurementProtocolSecretRequest()

    request.measurement_protocol_secret.name = "measurement_protocol_secret.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        await client.update_measurement_protocol_secret(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "measurement_protocol_secret.name=measurement_protocol_secret.name/value",
    ) in kw["metadata"]


def test_update_measurement_protocol_secret_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_measurement_protocol_secret(
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].measurement_protocol_secret == resources.MeasurementProtocolSecret(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_measurement_protocol_secret_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_measurement_protocol_secret(
            analytics_admin.UpdateMeasurementProtocolSecretRequest(),
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_measurement_protocol_secret), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.MeasurementProtocolSecret()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.MeasurementProtocolSecret()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_measurement_protocol_secret(
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].measurement_protocol_secret == resources.MeasurementProtocolSecret(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_measurement_protocol_secret_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_measurement_protocol_secret(
            analytics_admin.UpdateMeasurementProtocolSecretRequest(),
            measurement_protocol_secret=resources.MeasurementProtocolSecret(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_search_change_history_events(
    transport: str = "grpc",
    request_type=analytics_admin.SearchChangeHistoryEventsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.SearchChangeHistoryEventsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchChangeHistoryEventsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_change_history_events_from_dict():
    test_search_change_history_events(request_type=dict)


def test_search_change_history_events_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        client.search_change_history_events()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()


@pytest.mark.asyncio
async def test_search_change_history_events_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.SearchChangeHistoryEventsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.SearchChangeHistoryEventsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.SearchChangeHistoryEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchChangeHistoryEventsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_change_history_events_async_from_dict():
    await test_search_change_history_events_async(request_type=dict)


def test_search_change_history_events_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.SearchChangeHistoryEventsRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        call.return_value = analytics_admin.SearchChangeHistoryEventsResponse()
        client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_change_history_events_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.SearchChangeHistoryEventsRequest()

    request.account = "account/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.SearchChangeHistoryEventsResponse()
        )
        await client.search_change_history_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "account=account/value",) in kw["metadata"]


def test_search_change_history_events_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[], next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[resources.ChangeHistoryEvent(),],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", ""),)),
        )
        pager = client.search_change_history_events(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.ChangeHistoryEvent) for i in results)


def test_search_change_history_events_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[], next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[resources.ChangeHistoryEvent(),],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_change_history_events(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_change_history_events_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[], next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[resources.ChangeHistoryEvent(),],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_change_history_events(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ChangeHistoryEvent) for i in responses)


@pytest.mark.asyncio
async def test_search_change_history_events_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_change_history_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[], next_page_token="def",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[resources.ChangeHistoryEvent(),],
                next_page_token="ghi",
            ),
            analytics_admin.SearchChangeHistoryEventsResponse(
                change_history_events=[
                    resources.ChangeHistoryEvent(),
                    resources.ChangeHistoryEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.search_change_history_events(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_google_signals_settings(
    transport: str = "grpc",
    request_type=analytics_admin.GetGoogleSignalsSettingsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings(
            name="name_value",
            state=resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED,
            consent=resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED,
        )
        response = client.get_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGoogleSignalsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleSignalsSettings)
    assert response.name == "name_value"
    assert response.state == resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED
    assert (
        response.consent
        == resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED
    )


def test_get_google_signals_settings_from_dict():
    test_get_google_signals_settings(request_type=dict)


def test_get_google_signals_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        client.get_google_signals_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGoogleSignalsSettingsRequest()


@pytest.mark.asyncio
async def test_get_google_signals_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetGoogleSignalsSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings(
                name="name_value",
                state=resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED,
                consent=resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED,
            )
        )
        response = await client.get_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetGoogleSignalsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleSignalsSettings)
    assert response.name == "name_value"
    assert response.state == resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED
    assert (
        response.consent
        == resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED
    )


@pytest.mark.asyncio
async def test_get_google_signals_settings_async_from_dict():
    await test_get_google_signals_settings_async(request_type=dict)


def test_get_google_signals_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGoogleSignalsSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        call.return_value = resources.GoogleSignalsSettings()
        client.get_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_google_signals_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetGoogleSignalsSettingsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings()
        )
        await client.get_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_google_signals_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_google_signals_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_google_signals_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_google_signals_settings(
            analytics_admin.GetGoogleSignalsSettingsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_google_signals_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_google_signals_settings(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_google_signals_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_google_signals_settings(
            analytics_admin.GetGoogleSignalsSettingsRequest(), name="name_value",
        )


def test_update_google_signals_settings(
    transport: str = "grpc",
    request_type=analytics_admin.UpdateGoogleSignalsSettingsRequest,
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings(
            name="name_value",
            state=resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED,
            consent=resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED,
        )
        response = client.update_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleSignalsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleSignalsSettings)
    assert response.name == "name_value"
    assert response.state == resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED
    assert (
        response.consent
        == resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED
    )


def test_update_google_signals_settings_from_dict():
    test_update_google_signals_settings(request_type=dict)


def test_update_google_signals_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        client.update_google_signals_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleSignalsSettingsRequest()


@pytest.mark.asyncio
async def test_update_google_signals_settings_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateGoogleSignalsSettingsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings(
                name="name_value",
                state=resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED,
                consent=resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED,
            )
        )
        response = await client.update_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateGoogleSignalsSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.GoogleSignalsSettings)
    assert response.name == "name_value"
    assert response.state == resources.GoogleSignalsState.GOOGLE_SIGNALS_ENABLED
    assert (
        response.consent
        == resources.GoogleSignalsConsent.GOOGLE_SIGNALS_CONSENT_CONSENTED
    )


@pytest.mark.asyncio
async def test_update_google_signals_settings_async_from_dict():
    await test_update_google_signals_settings_async(request_type=dict)


def test_update_google_signals_settings_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleSignalsSettingsRequest()

    request.google_signals_settings.name = "google_signals_settings.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        call.return_value = resources.GoogleSignalsSettings()
        client.update_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_signals_settings.name=google_signals_settings.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_google_signals_settings_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateGoogleSignalsSettingsRequest()

    request.google_signals_settings.name = "google_signals_settings.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings()
        )
        await client.update_google_signals_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "google_signals_settings.name=google_signals_settings.name/value",
    ) in kw["metadata"]


def test_update_google_signals_settings_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_google_signals_settings(
            google_signals_settings=resources.GoogleSignalsSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].google_signals_settings == resources.GoogleSignalsSettings(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_google_signals_settings_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_signals_settings(
            analytics_admin.UpdateGoogleSignalsSettingsRequest(),
            google_signals_settings=resources.GoogleSignalsSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_google_signals_settings_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_google_signals_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.GoogleSignalsSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.GoogleSignalsSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_google_signals_settings(
            google_signals_settings=resources.GoogleSignalsSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].google_signals_settings == resources.GoogleSignalsSettings(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_google_signals_settings_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_google_signals_settings(
            analytics_admin.UpdateGoogleSignalsSettingsRequest(),
            google_signals_settings=resources.GoogleSignalsSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_conversion_event(
    transport: str = "grpc", request_type=analytics_admin.CreateConversionEventRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent(
            name="name_value", event_name="event_name_value", is_deletable=True,
        )
        response = client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.is_deletable is True


def test_create_conversion_event_from_dict():
    test_create_conversion_event(request_type=dict)


def test_create_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        client.create_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()


@pytest.mark.asyncio
async def test_create_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent(
                name="name_value", event_name="event_name_value", is_deletable=True,
            )
        )
        response = await client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.is_deletable is True


@pytest.mark.asyncio
async def test_create_conversion_event_async_from_dict():
    await test_create_conversion_event_async(request_type=dict)


def test_create_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateConversionEventRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        call.return_value = resources.ConversionEvent()
        client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateConversionEventRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        await client.create_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversion_event(
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].conversion_event == resources.ConversionEvent(name="name_value")


def test_create_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversion_event(
            analytics_admin.CreateConversionEventRequest(),
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversion_event(
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].conversion_event == resources.ConversionEvent(name="name_value")


@pytest.mark.asyncio
async def test_create_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversion_event(
            analytics_admin.CreateConversionEventRequest(),
            parent="parent_value",
            conversion_event=resources.ConversionEvent(name="name_value"),
        )


def test_get_conversion_event(
    transport: str = "grpc", request_type=analytics_admin.GetConversionEventRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent(
            name="name_value", event_name="event_name_value", is_deletable=True,
        )
        response = client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.is_deletable is True


def test_get_conversion_event_from_dict():
    test_get_conversion_event(request_type=dict)


def test_get_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        client.get_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()


@pytest.mark.asyncio
async def test_get_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent(
                name="name_value", event_name="event_name_value", is_deletable=True,
            )
        )
        response = await client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ConversionEvent)
    assert response.name == "name_value"
    assert response.event_name == "event_name_value"
    assert response.is_deletable is True


@pytest.mark.asyncio
async def test_get_conversion_event_async_from_dict():
    await test_get_conversion_event_async(request_type=dict)


def test_get_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetConversionEventRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        call.return_value = resources.ConversionEvent()
        client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetConversionEventRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        await client.get_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversion_event(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversion_event(
            analytics_admin.GetConversionEventRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ConversionEvent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ConversionEvent()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversion_event(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversion_event(
            analytics_admin.GetConversionEventRequest(), name="name_value",
        )


def test_delete_conversion_event(
    transport: str = "grpc", request_type=analytics_admin.DeleteConversionEventRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_conversion_event_from_dict():
    test_delete_conversion_event(request_type=dict)


def test_delete_conversion_event_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        client.delete_conversion_event()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()


@pytest.mark.asyncio
async def test_delete_conversion_event_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.DeleteConversionEventRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.DeleteConversionEventRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_conversion_event_async_from_dict():
    await test_delete_conversion_event_async(request_type=dict)


def test_delete_conversion_event_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteConversionEventRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        call.return_value = None
        client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_conversion_event_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.DeleteConversionEventRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_conversion_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_conversion_event_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_conversion_event(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_conversion_event_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversion_event(
            analytics_admin.DeleteConversionEventRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_conversion_event_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_conversion_event(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_conversion_event_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_conversion_event(
            analytics_admin.DeleteConversionEventRequest(), name="name_value",
        )


def test_list_conversion_events(
    transport: str = "grpc", request_type=analytics_admin.ListConversionEventsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionEventsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversion_events_from_dict():
    test_list_conversion_events(request_type=dict)


def test_list_conversion_events_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        client.list_conversion_events()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()


@pytest.mark.asyncio
async def test_list_conversion_events_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListConversionEventsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListConversionEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionEventsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_conversion_events_async_from_dict():
    await test_list_conversion_events_async(request_type=dict)


def test_list_conversion_events_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListConversionEventsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListConversionEventsResponse()
        client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_conversion_events_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListConversionEventsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse()
        )
        await client.list_conversion_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_conversion_events_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversion_events(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_conversion_events_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversion_events(
            analytics_admin.ListConversionEventsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversion_events_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListConversionEventsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListConversionEventsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversion_events(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_conversion_events_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversion_events(
            analytics_admin.ListConversionEventsRequest(), parent="parent_value",
        )


def test_list_conversion_events_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[], next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[resources.ConversionEvent(),], next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversion_events(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.ConversionEvent) for i in results)


def test_list_conversion_events_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[], next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[resources.ConversionEvent(),], next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversion_events(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversion_events_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[], next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[resources.ConversionEvent(),], next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversion_events(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.ConversionEvent) for i in responses)


@pytest.mark.asyncio
async def test_list_conversion_events_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[], next_page_token="def",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[resources.ConversionEvent(),], next_page_token="ghi",
            ),
            analytics_admin.ListConversionEventsResponse(
                conversion_events=[
                    resources.ConversionEvent(),
                    resources.ConversionEvent(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_conversion_events(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_custom_dimension(
    transport: str = "grpc", request_type=analytics_admin.CreateCustomDimensionRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_create_custom_dimension_from_dict():
    test_create_custom_dimension(request_type=dict)


def test_create_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        client.create_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()


@pytest.mark.asyncio
async def test_create_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_create_custom_dimension_async_from_dict():
    await test_create_custom_dimension_async(request_type=dict)


def test_create_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomDimensionRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomDimensionRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.create_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_dimension(
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].custom_dimension == resources.CustomDimension(name="name_value")


def test_create_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_dimension(
            analytics_admin.CreateCustomDimensionRequest(),
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_dimension(
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].custom_dimension == resources.CustomDimension(name="name_value")


@pytest.mark.asyncio
async def test_create_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_dimension(
            analytics_admin.CreateCustomDimensionRequest(),
            parent="parent_value",
            custom_dimension=resources.CustomDimension(name="name_value"),
        )


def test_update_custom_dimension(
    transport: str = "grpc", request_type=analytics_admin.UpdateCustomDimensionRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_update_custom_dimension_from_dict():
    test_update_custom_dimension(request_type=dict)


def test_update_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        client.update_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()


@pytest.mark.asyncio
async def test_update_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_update_custom_dimension_async_from_dict():
    await test_update_custom_dimension_async(request_type=dict)


def test_update_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomDimensionRequest()

    request.custom_dimension.name = "custom_dimension.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_dimension.name=custom_dimension.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomDimensionRequest()

    request.custom_dimension.name = "custom_dimension.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.update_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_dimension.name=custom_dimension.name/value",
    ) in kw["metadata"]


def test_update_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_dimension(
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].custom_dimension == resources.CustomDimension(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_dimension(
            analytics_admin.UpdateCustomDimensionRequest(),
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_dimension(
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].custom_dimension == resources.CustomDimension(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_dimension(
            analytics_admin.UpdateCustomDimensionRequest(),
            custom_dimension=resources.CustomDimension(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_list_custom_dimensions(
    transport: str = "grpc", request_type=analytics_admin.ListCustomDimensionsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomDimensionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_dimensions_from_dict():
    test_list_custom_dimensions(request_type=dict)


def test_list_custom_dimensions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        client.list_custom_dimensions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()


@pytest.mark.asyncio
async def test_list_custom_dimensions_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListCustomDimensionsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomDimensionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomDimensionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_from_dict():
    await test_list_custom_dimensions_async(request_type=dict)


def test_list_custom_dimensions_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomDimensionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListCustomDimensionsResponse()
        client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_custom_dimensions_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomDimensionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse()
        )
        await client.list_custom_dimensions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_custom_dimensions_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_dimensions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_custom_dimensions_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_dimensions(
            analytics_admin.ListCustomDimensionsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_dimensions_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomDimensionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomDimensionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_dimensions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_custom_dimensions_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_dimensions(
            analytics_admin.ListCustomDimensionsRequest(), parent="parent_value",
        )


def test_list_custom_dimensions_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[], next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[resources.CustomDimension(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_dimensions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CustomDimension) for i in results)


def test_list_custom_dimensions_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[], next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[resources.CustomDimension(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_dimensions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[], next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[resources.CustomDimension(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_dimensions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CustomDimension) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_dimensions_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_dimensions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[], next_page_token="def",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[resources.CustomDimension(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomDimensionsResponse(
                custom_dimensions=[
                    resources.CustomDimension(),
                    resources.CustomDimension(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_custom_dimensions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_archive_custom_dimension(
    transport: str = "grpc", request_type=analytics_admin.ArchiveCustomDimensionRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_archive_custom_dimension_from_dict():
    test_archive_custom_dimension(request_type=dict)


def test_archive_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        client.archive_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()


@pytest.mark.asyncio
async def test_archive_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ArchiveCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_archive_custom_dimension_async_from_dict():
    await test_archive_custom_dimension_async(request_type=dict)


def test_archive_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomDimensionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        call.return_value = None
        client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_archive_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomDimensionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.archive_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_archive_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.archive_custom_dimension(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_archive_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.archive_custom_dimension(
            analytics_admin.ArchiveCustomDimensionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_archive_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.archive_custom_dimension(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_archive_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.archive_custom_dimension(
            analytics_admin.ArchiveCustomDimensionRequest(), name="name_value",
        )


def test_get_custom_dimension(
    transport: str = "grpc", request_type=analytics_admin.GetCustomDimensionRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            scope=resources.CustomDimension.DimensionScope.EVENT,
            disallow_ads_personalization=True,
        )
        response = client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


def test_get_custom_dimension_from_dict():
    test_get_custom_dimension(request_type=dict)


def test_get_custom_dimension_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        client.get_custom_dimension()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()


@pytest.mark.asyncio
async def test_get_custom_dimension_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.GetCustomDimensionRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                scope=resources.CustomDimension.DimensionScope.EVENT,
                disallow_ads_personalization=True,
            )
        )
        response = await client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomDimensionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomDimension)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.scope == resources.CustomDimension.DimensionScope.EVENT
    assert response.disallow_ads_personalization is True


@pytest.mark.asyncio
async def test_get_custom_dimension_async_from_dict():
    await test_get_custom_dimension_async(request_type=dict)


def test_get_custom_dimension_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomDimensionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        call.return_value = resources.CustomDimension()
        client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_custom_dimension_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomDimensionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        await client.get_custom_dimension(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_custom_dimension_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_dimension(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_custom_dimension_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_dimension(
            analytics_admin.GetCustomDimensionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_dimension_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_dimension), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomDimension()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomDimension()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_dimension(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_custom_dimension_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_dimension(
            analytics_admin.GetCustomDimensionRequest(), name="name_value",
        )


def test_create_custom_metric(
    transport: str = "grpc", request_type=analytics_admin.CreateCustomMetricRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
        )
        response = client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


def test_create_custom_metric_from_dict():
    test_create_custom_metric(request_type=dict)


def test_create_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        client.create_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()


@pytest.mark.asyncio
async def test_create_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.CreateCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
            )
        )
        response = await client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.CreateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


@pytest.mark.asyncio
async def test_create_custom_metric_async_from_dict():
    await test_create_custom_metric_async(request_type=dict)


def test_create_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomMetricRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.CreateCustomMetricRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.create_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_metric(
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].custom_metric == resources.CustomMetric(name="name_value")


def test_create_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_metric(
            analytics_admin.CreateCustomMetricRequest(),
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_metric(
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].custom_metric == resources.CustomMetric(name="name_value")


@pytest.mark.asyncio
async def test_create_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_metric(
            analytics_admin.CreateCustomMetricRequest(),
            parent="parent_value",
            custom_metric=resources.CustomMetric(name="name_value"),
        )


def test_update_custom_metric(
    transport: str = "grpc", request_type=analytics_admin.UpdateCustomMetricRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
        )
        response = client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


def test_update_custom_metric_from_dict():
    test_update_custom_metric(request_type=dict)


def test_update_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        client.update_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()


@pytest.mark.asyncio
async def test_update_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.UpdateCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
            )
        )
        response = await client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.UpdateCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


@pytest.mark.asyncio
async def test_update_custom_metric_async_from_dict():
    await test_update_custom_metric_async(request_type=dict)


def test_update_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomMetricRequest()

    request.custom_metric.name = "custom_metric.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_metric.name=custom_metric.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.UpdateCustomMetricRequest()

    request.custom_metric.name = "custom_metric.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.update_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_metric.name=custom_metric.name/value",
    ) in kw["metadata"]


def test_update_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_metric(
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].custom_metric == resources.CustomMetric(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_metric(
            analytics_admin.UpdateCustomMetricRequest(),
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_metric(
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].custom_metric == resources.CustomMetric(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_metric(
            analytics_admin.UpdateCustomMetricRequest(),
            custom_metric=resources.CustomMetric(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_list_custom_metrics(
    transport: str = "grpc", request_type=analytics_admin.ListCustomMetricsRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomMetricsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_metrics_from_dict():
    test_list_custom_metrics(request_type=dict)


def test_list_custom_metrics_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        client.list_custom_metrics()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()


@pytest.mark.asyncio
async def test_list_custom_metrics_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ListCustomMetricsRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ListCustomMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomMetricsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_metrics_async_from_dict():
    await test_list_custom_metrics_async(request_type=dict)


def test_list_custom_metrics_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomMetricsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        call.return_value = analytics_admin.ListCustomMetricsResponse()
        client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_custom_metrics_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ListCustomMetricsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse()
        )
        await client.list_custom_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_custom_metrics_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_metrics(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_custom_metrics_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_metrics(
            analytics_admin.ListCustomMetricsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_metrics_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_admin.ListCustomMetricsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_admin.ListCustomMetricsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_metrics(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_custom_metrics_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_metrics(
            analytics_admin.ListCustomMetricsRequest(), parent="parent_value",
        )


def test_list_custom_metrics_pager():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[], next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(), resources.CustomMetric(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_metrics(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CustomMetric) for i in results)


def test_list_custom_metrics_pages():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[], next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(), resources.CustomMetric(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_metrics(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_metrics_async_pager():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[], next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(), resources.CustomMetric(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_metrics(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CustomMetric) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_metrics_async_pages():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_metrics),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                    resources.CustomMetric(),
                ],
                next_page_token="abc",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[], next_page_token="def",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(),], next_page_token="ghi",
            ),
            analytics_admin.ListCustomMetricsResponse(
                custom_metrics=[resources.CustomMetric(), resources.CustomMetric(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_custom_metrics(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_archive_custom_metric(
    transport: str = "grpc", request_type=analytics_admin.ArchiveCustomMetricRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_archive_custom_metric_from_dict():
    test_archive_custom_metric(request_type=dict)


def test_archive_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        client.archive_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()


@pytest.mark.asyncio
async def test_archive_custom_metric_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_admin.ArchiveCustomMetricRequest,
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.ArchiveCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_archive_custom_metric_async_from_dict():
    await test_archive_custom_metric_async(request_type=dict)


def test_archive_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomMetricRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        call.return_value = None
        client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_archive_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.ArchiveCustomMetricRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.archive_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_archive_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.archive_custom_metric(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_archive_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.archive_custom_metric(
            analytics_admin.ArchiveCustomMetricRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_archive_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.archive_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.archive_custom_metric(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_archive_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.archive_custom_metric(
            analytics_admin.ArchiveCustomMetricRequest(), name="name_value",
        )


def test_get_custom_metric(
    transport: str = "grpc", request_type=analytics_admin.GetCustomMetricRequest
):
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric(
            name="name_value",
            parameter_name="parameter_name_value",
            display_name="display_name_value",
            description="description_value",
            measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
            scope=resources.CustomMetric.MetricScope.EVENT,
        )
        response = client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


def test_get_custom_metric_from_dict():
    test_get_custom_metric(request_type=dict)


def test_get_custom_metric_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        client.get_custom_metric()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()


@pytest.mark.asyncio
async def test_get_custom_metric_async(
    transport: str = "grpc_asyncio", request_type=analytics_admin.GetCustomMetricRequest
):
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric(
                name="name_value",
                parameter_name="parameter_name_value",
                display_name="display_name_value",
                description="description_value",
                measurement_unit=resources.CustomMetric.MeasurementUnit.STANDARD,
                scope=resources.CustomMetric.MetricScope.EVENT,
            )
        )
        response = await client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == analytics_admin.GetCustomMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CustomMetric)
    assert response.name == "name_value"
    assert response.parameter_name == "parameter_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.measurement_unit == resources.CustomMetric.MeasurementUnit.STANDARD
    assert response.scope == resources.CustomMetric.MetricScope.EVENT


@pytest.mark.asyncio
async def test_get_custom_metric_async_from_dict():
    await test_get_custom_metric_async(request_type=dict)


def test_get_custom_metric_field_headers():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomMetricRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        call.return_value = resources.CustomMetric()
        client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_custom_metric_field_headers_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_admin.GetCustomMetricRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        await client.get_custom_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_custom_metric_flattened():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_metric(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_custom_metric_flattened_error():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_metric(
            analytics_admin.GetCustomMetricRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_metric_flattened_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CustomMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CustomMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_metric(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_custom_metric_flattened_error_async():
    client = AnalyticsAdminServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_metric(
            analytics_admin.GetCustomMetricRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AnalyticsAdminServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AnalyticsAdminServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
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
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(client.transport, transports.AnalyticsAdminServiceGrpcTransport,)


def test_analytics_admin_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AnalyticsAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_analytics_admin_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AnalyticsAdminServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_account",
        "list_accounts",
        "delete_account",
        "update_account",
        "provision_account_ticket",
        "list_account_summaries",
        "get_property",
        "list_properties",
        "create_property",
        "delete_property",
        "update_property",
        "get_user_link",
        "batch_get_user_links",
        "list_user_links",
        "audit_user_links",
        "create_user_link",
        "batch_create_user_links",
        "update_user_link",
        "batch_update_user_links",
        "delete_user_link",
        "batch_delete_user_links",
        "get_web_data_stream",
        "delete_web_data_stream",
        "update_web_data_stream",
        "create_web_data_stream",
        "list_web_data_streams",
        "get_ios_app_data_stream",
        "delete_ios_app_data_stream",
        "update_ios_app_data_stream",
        "list_ios_app_data_streams",
        "get_android_app_data_stream",
        "delete_android_app_data_stream",
        "update_android_app_data_stream",
        "list_android_app_data_streams",
        "get_enhanced_measurement_settings",
        "update_enhanced_measurement_settings",
        "create_firebase_link",
        "update_firebase_link",
        "delete_firebase_link",
        "list_firebase_links",
        "get_global_site_tag",
        "create_google_ads_link",
        "update_google_ads_link",
        "delete_google_ads_link",
        "list_google_ads_links",
        "get_data_sharing_settings",
        "get_measurement_protocol_secret",
        "list_measurement_protocol_secrets",
        "create_measurement_protocol_secret",
        "delete_measurement_protocol_secret",
        "update_measurement_protocol_secret",
        "search_change_history_events",
        "get_google_signals_settings",
        "update_google_signals_settings",
        "create_conversion_event",
        "get_conversion_event",
        "delete_conversion_event",
        "list_conversion_events",
        "create_custom_dimension",
        "update_custom_dimension",
        "list_custom_dimensions",
        "archive_custom_dimension",
        "get_custom_dimension",
        "create_custom_metric",
        "update_custom_metric",
        "list_custom_metrics",
        "archive_custom_metric",
        "get_custom_metric",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_analytics_admin_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_analytics_admin_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_analytics_admin_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.analytics.admin_v1alpha.services.analytics_admin_service.transports.AnalyticsAdminServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AnalyticsAdminServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_analytics_admin_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnalyticsAdminServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_analytics_admin_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AnalyticsAdminServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_analytics_admin_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_analytics_admin_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.AnalyticsAdminServiceGrpcTransport, grpc_helpers),
        (transports.AnalyticsAdminServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_analytics_admin_service_transport_create_channel(
    transport_class, grpc_helpers
):
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
            "analyticsadmin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/analytics.edit",
                "https://www.googleapis.com/auth/analytics.manage.users",
                "https://www.googleapis.com/auth/analytics.manage.users.readonly",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            scopes=["1", "2"],
            default_host="analyticsadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_grpc_transport_client_cert_source_for_mtls(
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


def test_analytics_admin_service_host_no_port():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com"
        ),
    )
    assert client.transport._host == "analyticsadmin.googleapis.com:443"


def test_analytics_admin_service_host_with_port():
    client = AnalyticsAdminServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsadmin.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "analyticsadmin.googleapis.com:8000"


def test_analytics_admin_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsAdminServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_analytics_admin_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AnalyticsAdminServiceGrpcAsyncIOTransport(
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
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_channel_mtls_with_client_cert_source(
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
        transports.AnalyticsAdminServiceGrpcTransport,
        transports.AnalyticsAdminServiceGrpcAsyncIOTransport,
    ],
)
def test_analytics_admin_service_transport_channel_mtls_with_adc(transport_class):
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


def test_account_path():
    account = "squid"
    expected = "accounts/{account}".format(account=account,)
    actual = AnalyticsAdminServiceClient.account_path(account)
    assert expected == actual


def test_parse_account_path():
    expected = {
        "account": "clam",
    }
    path = AnalyticsAdminServiceClient.account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_account_path(path)
    assert expected == actual


def test_account_summary_path():
    account_summary = "whelk"
    expected = "accountSummaries/{account_summary}".format(
        account_summary=account_summary,
    )
    actual = AnalyticsAdminServiceClient.account_summary_path(account_summary)
    assert expected == actual


def test_parse_account_summary_path():
    expected = {
        "account_summary": "octopus",
    }
    path = AnalyticsAdminServiceClient.account_summary_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_account_summary_path(path)
    assert expected == actual


def test_android_app_data_stream_path():
    property = "oyster"
    android_app_data_stream = "nudibranch"
    expected = "properties/{property}/androidAppDataStreams/{android_app_data_stream}".format(
        property=property, android_app_data_stream=android_app_data_stream,
    )
    actual = AnalyticsAdminServiceClient.android_app_data_stream_path(
        property, android_app_data_stream
    )
    assert expected == actual


def test_parse_android_app_data_stream_path():
    expected = {
        "property": "cuttlefish",
        "android_app_data_stream": "mussel",
    }
    path = AnalyticsAdminServiceClient.android_app_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_android_app_data_stream_path(path)
    assert expected == actual


def test_conversion_event_path():
    property = "winkle"
    conversion_event = "nautilus"
    expected = "properties/{property}/conversionEvents/{conversion_event}".format(
        property=property, conversion_event=conversion_event,
    )
    actual = AnalyticsAdminServiceClient.conversion_event_path(
        property, conversion_event
    )
    assert expected == actual


def test_parse_conversion_event_path():
    expected = {
        "property": "scallop",
        "conversion_event": "abalone",
    }
    path = AnalyticsAdminServiceClient.conversion_event_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_conversion_event_path(path)
    assert expected == actual


def test_custom_dimension_path():
    property = "squid"
    expected = "properties/{property}/customDimensions".format(property=property,)
    actual = AnalyticsAdminServiceClient.custom_dimension_path(property)
    assert expected == actual


def test_parse_custom_dimension_path():
    expected = {
        "property": "clam",
    }
    path = AnalyticsAdminServiceClient.custom_dimension_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_custom_dimension_path(path)
    assert expected == actual


def test_custom_metric_path():
    property = "whelk"
    expected = "properties/{property}/customMetrics".format(property=property,)
    actual = AnalyticsAdminServiceClient.custom_metric_path(property)
    assert expected == actual


def test_parse_custom_metric_path():
    expected = {
        "property": "octopus",
    }
    path = AnalyticsAdminServiceClient.custom_metric_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_custom_metric_path(path)
    assert expected == actual


def test_data_sharing_settings_path():
    account = "oyster"
    expected = "accounts/{account}/dataSharingSettings".format(account=account,)
    actual = AnalyticsAdminServiceClient.data_sharing_settings_path(account)
    assert expected == actual


def test_parse_data_sharing_settings_path():
    expected = {
        "account": "nudibranch",
    }
    path = AnalyticsAdminServiceClient.data_sharing_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_data_sharing_settings_path(path)
    assert expected == actual


def test_enhanced_measurement_settings_path():
    property = "cuttlefish"
    web_data_stream = "mussel"
    expected = "properties/{property}/webDataStreams/{web_data_stream}/enhancedMeasurementSettings".format(
        property=property, web_data_stream=web_data_stream,
    )
    actual = AnalyticsAdminServiceClient.enhanced_measurement_settings_path(
        property, web_data_stream
    )
    assert expected == actual


def test_parse_enhanced_measurement_settings_path():
    expected = {
        "property": "winkle",
        "web_data_stream": "nautilus",
    }
    path = AnalyticsAdminServiceClient.enhanced_measurement_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_enhanced_measurement_settings_path(path)
    assert expected == actual


def test_firebase_link_path():
    property = "scallop"
    firebase_link = "abalone"
    expected = "properties/{property}/firebaseLinks/{firebase_link}".format(
        property=property, firebase_link=firebase_link,
    )
    actual = AnalyticsAdminServiceClient.firebase_link_path(property, firebase_link)
    assert expected == actual


def test_parse_firebase_link_path():
    expected = {
        "property": "squid",
        "firebase_link": "clam",
    }
    path = AnalyticsAdminServiceClient.firebase_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_firebase_link_path(path)
    assert expected == actual


def test_global_site_tag_path():
    property = "whelk"
    expected = "properties/{property}/globalSiteTag".format(property=property,)
    actual = AnalyticsAdminServiceClient.global_site_tag_path(property)
    assert expected == actual


def test_parse_global_site_tag_path():
    expected = {
        "property": "octopus",
    }
    path = AnalyticsAdminServiceClient.global_site_tag_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_global_site_tag_path(path)
    assert expected == actual


def test_google_ads_link_path():
    property = "oyster"
    google_ads_link = "nudibranch"
    expected = "properties/{property}/googleAdsLinks/{google_ads_link}".format(
        property=property, google_ads_link=google_ads_link,
    )
    actual = AnalyticsAdminServiceClient.google_ads_link_path(property, google_ads_link)
    assert expected == actual


def test_parse_google_ads_link_path():
    expected = {
        "property": "cuttlefish",
        "google_ads_link": "mussel",
    }
    path = AnalyticsAdminServiceClient.google_ads_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_google_ads_link_path(path)
    assert expected == actual


def test_google_signals_settings_path():
    property = "winkle"
    expected = "properties/{property}/googleSignalsSettings".format(property=property,)
    actual = AnalyticsAdminServiceClient.google_signals_settings_path(property)
    assert expected == actual


def test_parse_google_signals_settings_path():
    expected = {
        "property": "nautilus",
    }
    path = AnalyticsAdminServiceClient.google_signals_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_google_signals_settings_path(path)
    assert expected == actual


def test_ios_app_data_stream_path():
    property = "scallop"
    ios_app_data_stream = "abalone"
    expected = "properties/{property}/iosAppDataStreams/{ios_app_data_stream}".format(
        property=property, ios_app_data_stream=ios_app_data_stream,
    )
    actual = AnalyticsAdminServiceClient.ios_app_data_stream_path(
        property, ios_app_data_stream
    )
    assert expected == actual


def test_parse_ios_app_data_stream_path():
    expected = {
        "property": "squid",
        "ios_app_data_stream": "clam",
    }
    path = AnalyticsAdminServiceClient.ios_app_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_ios_app_data_stream_path(path)
    assert expected == actual


def test_measurement_protocol_secret_path():
    property = "whelk"
    web_data_stream = "octopus"
    measurement_protocol_secret = "oyster"
    expected = "properties/{property}/webDataStreams/{web_data_stream}/measurementProtocolSecrets/{measurement_protocol_secret}".format(
        property=property,
        web_data_stream=web_data_stream,
        measurement_protocol_secret=measurement_protocol_secret,
    )
    actual = AnalyticsAdminServiceClient.measurement_protocol_secret_path(
        property, web_data_stream, measurement_protocol_secret
    )
    assert expected == actual


def test_parse_measurement_protocol_secret_path():
    expected = {
        "property": "nudibranch",
        "web_data_stream": "cuttlefish",
        "measurement_protocol_secret": "mussel",
    }
    path = AnalyticsAdminServiceClient.measurement_protocol_secret_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_measurement_protocol_secret_path(path)
    assert expected == actual


def test_property_path():
    property = "winkle"
    expected = "properties/{property}".format(property=property,)
    actual = AnalyticsAdminServiceClient.property_path(property)
    assert expected == actual


def test_parse_property_path():
    expected = {
        "property": "nautilus",
    }
    path = AnalyticsAdminServiceClient.property_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_property_path(path)
    assert expected == actual


def test_user_link_path():
    account = "scallop"
    user_link = "abalone"
    expected = "accounts/{account}/userLinks/{user_link}".format(
        account=account, user_link=user_link,
    )
    actual = AnalyticsAdminServiceClient.user_link_path(account, user_link)
    assert expected == actual


def test_parse_user_link_path():
    expected = {
        "account": "squid",
        "user_link": "clam",
    }
    path = AnalyticsAdminServiceClient.user_link_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_user_link_path(path)
    assert expected == actual


def test_web_data_stream_path():
    property = "whelk"
    web_data_stream = "octopus"
    expected = "properties/{property}/webDataStreams/{web_data_stream}".format(
        property=property, web_data_stream=web_data_stream,
    )
    actual = AnalyticsAdminServiceClient.web_data_stream_path(property, web_data_stream)
    assert expected == actual


def test_parse_web_data_stream_path():
    expected = {
        "property": "oyster",
        "web_data_stream": "nudibranch",
    }
    path = AnalyticsAdminServiceClient.web_data_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_web_data_stream_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AnalyticsAdminServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = AnalyticsAdminServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(folder=folder,)
    actual = AnalyticsAdminServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = AnalyticsAdminServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = AnalyticsAdminServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = AnalyticsAdminServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(project=project,)
    actual = AnalyticsAdminServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = AnalyticsAdminServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AnalyticsAdminServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = AnalyticsAdminServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AnalyticsAdminServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AnalyticsAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AnalyticsAdminServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AnalyticsAdminServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AnalyticsAdminServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
