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
from google.cloud.recommender_v1.services.recommender import RecommenderAsyncClient
from google.cloud.recommender_v1.services.recommender import RecommenderClient
from google.cloud.recommender_v1.services.recommender import pagers
from google.cloud.recommender_v1.services.recommender import transports
from google.cloud.recommender_v1.services.recommender.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.recommender_v1.types import insight
from google.cloud.recommender_v1.types import recommendation
from google.cloud.recommender_v1.types import recommender_service
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert RecommenderClient._get_default_mtls_endpoint(None) is None
    assert (
        RecommenderClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        RecommenderClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RecommenderClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RecommenderClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert RecommenderClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [RecommenderClient, RecommenderAsyncClient,])
def test_recommender_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "recommender.googleapis.com:443"


@pytest.mark.parametrize("client_class", [RecommenderClient, RecommenderAsyncClient,])
def test_recommender_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RecommenderGrpcTransport, "grpc"),
        (transports.RecommenderGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_recommender_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize("client_class", [RecommenderClient, RecommenderAsyncClient,])
def test_recommender_client_from_service_account_file(client_class):
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

        assert client.transport._host == "recommender.googleapis.com:443"


def test_recommender_client_get_transport_class():
    transport = RecommenderClient.get_transport_class()
    available_transports = [
        transports.RecommenderGrpcTransport,
    ]
    assert transport in available_transports

    transport = RecommenderClient.get_transport_class("grpc")
    assert transport == transports.RecommenderGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RecommenderClient, transports.RecommenderGrpcTransport, "grpc"),
        (
            RecommenderAsyncClient,
            transports.RecommenderGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    RecommenderClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RecommenderClient)
)
@mock.patch.object(
    RecommenderAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecommenderAsyncClient),
)
def test_recommender_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(RecommenderClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(RecommenderClient, "get_transport_class") as gtc:
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
        (RecommenderClient, transports.RecommenderGrpcTransport, "grpc", "true"),
        (
            RecommenderAsyncClient,
            transports.RecommenderGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (RecommenderClient, transports.RecommenderGrpcTransport, "grpc", "false"),
        (
            RecommenderAsyncClient,
            transports.RecommenderGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    RecommenderClient, "DEFAULT_ENDPOINT", modify_default_endpoint(RecommenderClient)
)
@mock.patch.object(
    RecommenderAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecommenderAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_recommender_client_mtls_env_auto(
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
        (RecommenderClient, transports.RecommenderGrpcTransport, "grpc"),
        (
            RecommenderAsyncClient,
            transports.RecommenderGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_recommender_client_client_options_scopes(
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
        (RecommenderClient, transports.RecommenderGrpcTransport, "grpc"),
        (
            RecommenderAsyncClient,
            transports.RecommenderGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_recommender_client_client_options_credentials_file(
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


def test_recommender_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recommender_v1.services.recommender.transports.RecommenderGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecommenderClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_insights(
    transport: str = "grpc", request_type=recommender_service.ListInsightsRequest
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListInsightsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_insights(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListInsightsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInsightsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_insights_from_dict():
    test_list_insights(request_type=dict)


def test_list_insights_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        client.list_insights()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListInsightsRequest()


@pytest.mark.asyncio
async def test_list_insights_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.ListInsightsRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListInsightsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_insights(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListInsightsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInsightsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_insights_async_from_dict():
    await test_list_insights_async(request_type=dict)


def test_list_insights_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.ListInsightsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        call.return_value = recommender_service.ListInsightsResponse()
        client.list_insights(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_insights_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.ListInsightsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListInsightsResponse()
        )
        await client.list_insights(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_insights_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListInsightsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_insights(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_insights_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_insights(
            recommender_service.ListInsightsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_insights_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListInsightsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListInsightsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_insights(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_insights_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_insights(
            recommender_service.ListInsightsRequest(), parent="parent_value",
        )


def test_list_insights_pager():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(), insight.Insight(),],
                next_page_token="abc",
            ),
            recommender_service.ListInsightsResponse(
                insights=[], next_page_token="def",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(),], next_page_token="ghi",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_insights(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, insight.Insight) for i in results)


def test_list_insights_pages():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_insights), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(), insight.Insight(),],
                next_page_token="abc",
            ),
            recommender_service.ListInsightsResponse(
                insights=[], next_page_token="def",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(),], next_page_token="ghi",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_insights(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_insights_async_pager():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_insights), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(), insight.Insight(),],
                next_page_token="abc",
            ),
            recommender_service.ListInsightsResponse(
                insights=[], next_page_token="def",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(),], next_page_token="ghi",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_insights(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, insight.Insight) for i in responses)


@pytest.mark.asyncio
async def test_list_insights_async_pages():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_insights), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(), insight.Insight(),],
                next_page_token="abc",
            ),
            recommender_service.ListInsightsResponse(
                insights=[], next_page_token="def",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(),], next_page_token="ghi",
            ),
            recommender_service.ListInsightsResponse(
                insights=[insight.Insight(), insight.Insight(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_insights(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_insight(
    transport: str = "grpc", request_type=recommender_service.GetInsightRequest
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight(
            name="name_value",
            description="description_value",
            target_resources=["target_resources_value"],
            insight_subtype="insight_subtype_value",
            category=insight.Insight.Category.COST,
            etag="etag_value",
        )
        response = client.get_insight(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetInsightRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, insight.Insight)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.target_resources == ["target_resources_value"]
    assert response.insight_subtype == "insight_subtype_value"
    assert response.category == insight.Insight.Category.COST
    assert response.etag == "etag_value"


def test_get_insight_from_dict():
    test_get_insight(request_type=dict)


def test_get_insight_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        client.get_insight()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetInsightRequest()


@pytest.mark.asyncio
async def test_get_insight_async(
    transport: str = "grpc_asyncio", request_type=recommender_service.GetInsightRequest
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            insight.Insight(
                name="name_value",
                description="description_value",
                target_resources=["target_resources_value"],
                insight_subtype="insight_subtype_value",
                category=insight.Insight.Category.COST,
                etag="etag_value",
            )
        )
        response = await client.get_insight(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetInsightRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, insight.Insight)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.target_resources == ["target_resources_value"]
    assert response.insight_subtype == "insight_subtype_value"
    assert response.category == insight.Insight.Category.COST
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_insight_async_from_dict():
    await test_get_insight_async(request_type=dict)


def test_get_insight_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.GetInsightRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        call.return_value = insight.Insight()
        client.get_insight(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_insight_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.GetInsightRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(insight.Insight())
        await client.get_insight(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_insight_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_insight(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_insight_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_insight(
            recommender_service.GetInsightRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_insight_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_insight), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(insight.Insight())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_insight(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_insight_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_insight(
            recommender_service.GetInsightRequest(), name="name_value",
        )


def test_mark_insight_accepted(
    transport: str = "grpc", request_type=recommender_service.MarkInsightAcceptedRequest
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight(
            name="name_value",
            description="description_value",
            target_resources=["target_resources_value"],
            insight_subtype="insight_subtype_value",
            category=insight.Insight.Category.COST,
            etag="etag_value",
        )
        response = client.mark_insight_accepted(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkInsightAcceptedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, insight.Insight)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.target_resources == ["target_resources_value"]
    assert response.insight_subtype == "insight_subtype_value"
    assert response.category == insight.Insight.Category.COST
    assert response.etag == "etag_value"


def test_mark_insight_accepted_from_dict():
    test_mark_insight_accepted(request_type=dict)


def test_mark_insight_accepted_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        client.mark_insight_accepted()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkInsightAcceptedRequest()


@pytest.mark.asyncio
async def test_mark_insight_accepted_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.MarkInsightAcceptedRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            insight.Insight(
                name="name_value",
                description="description_value",
                target_resources=["target_resources_value"],
                insight_subtype="insight_subtype_value",
                category=insight.Insight.Category.COST,
                etag="etag_value",
            )
        )
        response = await client.mark_insight_accepted(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkInsightAcceptedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, insight.Insight)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.target_resources == ["target_resources_value"]
    assert response.insight_subtype == "insight_subtype_value"
    assert response.category == insight.Insight.Category.COST
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_insight_accepted_async_from_dict():
    await test_mark_insight_accepted_async(request_type=dict)


def test_mark_insight_accepted_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkInsightAcceptedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        call.return_value = insight.Insight()
        client.mark_insight_accepted(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_mark_insight_accepted_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkInsightAcceptedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(insight.Insight())
        await client.mark_insight_accepted(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_mark_insight_accepted_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mark_insight_accepted(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


def test_mark_insight_accepted_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mark_insight_accepted(
            recommender_service.MarkInsightAcceptedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


@pytest.mark.asyncio
async def test_mark_insight_accepted_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_insight_accepted), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = insight.Insight()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(insight.Insight())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mark_insight_accepted(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_insight_accepted_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mark_insight_accepted(
            recommender_service.MarkInsightAcceptedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


def test_list_recommendations(
    transport: str = "grpc", request_type=recommender_service.ListRecommendationsRequest
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListRecommendationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListRecommendationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecommendationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_recommendations_from_dict():
    test_list_recommendations(request_type=dict)


def test_list_recommendations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        client.list_recommendations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListRecommendationsRequest()


@pytest.mark.asyncio
async def test_list_recommendations_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.ListRecommendationsRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListRecommendationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.ListRecommendationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRecommendationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_recommendations_async_from_dict():
    await test_list_recommendations_async(request_type=dict)


def test_list_recommendations_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.ListRecommendationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        call.return_value = recommender_service.ListRecommendationsResponse()
        client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_recommendations_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.ListRecommendationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListRecommendationsResponse()
        )
        await client.list_recommendations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_recommendations_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListRecommendationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_recommendations(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


def test_list_recommendations_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_recommendations(
            recommender_service.ListRecommendationsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_recommendations_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommender_service.ListRecommendationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommender_service.ListRecommendationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_recommendations(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_recommendations_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_recommendations(
            recommender_service.ListRecommendationsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_recommendations_pager():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
                next_page_token="abc",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[], next_page_token="def",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[recommendation.Recommendation(),],
                next_page_token="ghi",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_recommendations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, recommendation.Recommendation) for i in results)


def test_list_recommendations_pages():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
                next_page_token="abc",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[], next_page_token="def",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[recommendation.Recommendation(),],
                next_page_token="ghi",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_recommendations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_recommendations_async_pager():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
                next_page_token="abc",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[], next_page_token="def",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[recommendation.Recommendation(),],
                next_page_token="ghi",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_recommendations(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, recommendation.Recommendation) for i in responses)


@pytest.mark.asyncio
async def test_list_recommendations_async_pages():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_recommendations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
                next_page_token="abc",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[], next_page_token="def",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[recommendation.Recommendation(),],
                next_page_token="ghi",
            ),
            recommender_service.ListRecommendationsResponse(
                recommendations=[
                    recommendation.Recommendation(),
                    recommendation.Recommendation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_recommendations(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_recommendation(
    transport: str = "grpc", request_type=recommender_service.GetRecommendationRequest
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.get_recommendation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetRecommendationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_get_recommendation_from_dict():
    test_get_recommendation(request_type=dict)


def test_get_recommendation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        client.get_recommendation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetRecommendationRequest()


@pytest.mark.asyncio
async def test_get_recommendation_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.GetRecommendationRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation(
                name="name_value",
                description="description_value",
                recommender_subtype="recommender_subtype_value",
                etag="etag_value",
            )
        )
        response = await client.get_recommendation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.GetRecommendationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_recommendation_async_from_dict():
    await test_get_recommendation_async(request_type=dict)


def test_get_recommendation_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.GetRecommendationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        call.return_value = recommendation.Recommendation()
        client.get_recommendation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_recommendation_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.GetRecommendationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        await client.get_recommendation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_recommendation_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_recommendation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_recommendation_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_recommendation(
            recommender_service.GetRecommendationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_recommendation_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_recommendation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_recommendation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_recommendation_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_recommendation(
            recommender_service.GetRecommendationRequest(), name="name_value",
        )


def test_mark_recommendation_claimed(
    transport: str = "grpc",
    request_type=recommender_service.MarkRecommendationClaimedRequest,
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_claimed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationClaimedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_mark_recommendation_claimed_from_dict():
    test_mark_recommendation_claimed(request_type=dict)


def test_mark_recommendation_claimed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        client.mark_recommendation_claimed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationClaimedRequest()


@pytest.mark.asyncio
async def test_mark_recommendation_claimed_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.MarkRecommendationClaimedRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation(
                name="name_value",
                description="description_value",
                recommender_subtype="recommender_subtype_value",
                etag="etag_value",
            )
        )
        response = await client.mark_recommendation_claimed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationClaimedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_claimed_async_from_dict():
    await test_mark_recommendation_claimed_async(request_type=dict)


def test_mark_recommendation_claimed_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationClaimedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        call.return_value = recommendation.Recommendation()
        client.mark_recommendation_claimed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_mark_recommendation_claimed_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationClaimedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        await client.mark_recommendation_claimed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_mark_recommendation_claimed_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mark_recommendation_claimed(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


def test_mark_recommendation_claimed_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mark_recommendation_claimed(
            recommender_service.MarkRecommendationClaimedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


@pytest.mark.asyncio
async def test_mark_recommendation_claimed_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_claimed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mark_recommendation_claimed(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_claimed_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mark_recommendation_claimed(
            recommender_service.MarkRecommendationClaimedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


def test_mark_recommendation_succeeded(
    transport: str = "grpc",
    request_type=recommender_service.MarkRecommendationSucceededRequest,
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_succeeded(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationSucceededRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_mark_recommendation_succeeded_from_dict():
    test_mark_recommendation_succeeded(request_type=dict)


def test_mark_recommendation_succeeded_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        client.mark_recommendation_succeeded()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationSucceededRequest()


@pytest.mark.asyncio
async def test_mark_recommendation_succeeded_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.MarkRecommendationSucceededRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation(
                name="name_value",
                description="description_value",
                recommender_subtype="recommender_subtype_value",
                etag="etag_value",
            )
        )
        response = await client.mark_recommendation_succeeded(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationSucceededRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_succeeded_async_from_dict():
    await test_mark_recommendation_succeeded_async(request_type=dict)


def test_mark_recommendation_succeeded_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationSucceededRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        call.return_value = recommendation.Recommendation()
        client.mark_recommendation_succeeded(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_mark_recommendation_succeeded_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationSucceededRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        await client.mark_recommendation_succeeded(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_mark_recommendation_succeeded_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mark_recommendation_succeeded(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


def test_mark_recommendation_succeeded_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mark_recommendation_succeeded(
            recommender_service.MarkRecommendationSucceededRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


@pytest.mark.asyncio
async def test_mark_recommendation_succeeded_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_succeeded), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mark_recommendation_succeeded(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_succeeded_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mark_recommendation_succeeded(
            recommender_service.MarkRecommendationSucceededRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


def test_mark_recommendation_failed(
    transport: str = "grpc",
    request_type=recommender_service.MarkRecommendationFailedRequest,
):
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation(
            name="name_value",
            description="description_value",
            recommender_subtype="recommender_subtype_value",
            etag="etag_value",
        )
        response = client.mark_recommendation_failed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationFailedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


def test_mark_recommendation_failed_from_dict():
    test_mark_recommendation_failed(request_type=dict)


def test_mark_recommendation_failed_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        client.mark_recommendation_failed()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationFailedRequest()


@pytest.mark.asyncio
async def test_mark_recommendation_failed_async(
    transport: str = "grpc_asyncio",
    request_type=recommender_service.MarkRecommendationFailedRequest,
):
    client = RecommenderAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation(
                name="name_value",
                description="description_value",
                recommender_subtype="recommender_subtype_value",
                etag="etag_value",
            )
        )
        response = await client.mark_recommendation_failed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recommender_service.MarkRecommendationFailedRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recommendation.Recommendation)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.recommender_subtype == "recommender_subtype_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_failed_async_from_dict():
    await test_mark_recommendation_failed_async(request_type=dict)


def test_mark_recommendation_failed_field_headers():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationFailedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        call.return_value = recommendation.Recommendation()
        client.mark_recommendation_failed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_mark_recommendation_failed_field_headers_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recommender_service.MarkRecommendationFailedRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        await client.mark_recommendation_failed(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_mark_recommendation_failed_flattened():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.mark_recommendation_failed(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


def test_mark_recommendation_failed_flattened_error():
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.mark_recommendation_failed(
            recommender_service.MarkRecommendationFailedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


@pytest.mark.asyncio
async def test_mark_recommendation_failed_flattened_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.mark_recommendation_failed), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recommendation.Recommendation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recommendation.Recommendation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.mark_recommendation_failed(
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].state_metadata == {"key_value": "value_value"}
        assert args[0].etag == "etag_value"


@pytest.mark.asyncio
async def test_mark_recommendation_failed_flattened_error_async():
    client = RecommenderAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.mark_recommendation_failed(
            recommender_service.MarkRecommendationFailedRequest(),
            name="name_value",
            state_metadata={"key_value": "value_value"},
            etag="etag_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecommenderClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecommenderClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecommenderClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RecommenderClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecommenderGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.RecommenderGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RecommenderClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.RecommenderGrpcTransport,)


def test_recommender_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RecommenderTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_recommender_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.recommender_v1.services.recommender.transports.RecommenderTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RecommenderTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_insights",
        "get_insight",
        "mark_insight_accepted",
        "list_recommendations",
        "get_recommendation",
        "mark_recommendation_claimed",
        "mark_recommendation_succeeded",
        "mark_recommendation_failed",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_recommender_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.recommender_v1.services.recommender.transports.RecommenderTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RecommenderTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_recommender_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.recommender_v1.services.recommender.transports.RecommenderTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RecommenderTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_recommender_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.recommender_v1.services.recommender.transports.RecommenderTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RecommenderTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_recommender_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RecommenderClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_recommender_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RecommenderClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
def test_recommender_transport_auth_adc(transport_class):
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
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_recommender_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.RecommenderGrpcTransport, grpc_helpers),
        (transports.RecommenderGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_recommender_transport_create_channel(transport_class, grpc_helpers):
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
            "recommender.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="recommender.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport],
)
def test_recommender_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_recommender_host_no_port():
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommender.googleapis.com"
        ),
    )
    assert client.transport._host == "recommender.googleapis.com:443"


def test_recommender_host_with_port():
    client = RecommenderClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommender.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "recommender.googleapis.com:8000"


def test_recommender_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RecommenderGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_recommender_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RecommenderGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport],
)
def test_recommender_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.RecommenderGrpcTransport, transports.RecommenderGrpcAsyncIOTransport],
)
def test_recommender_transport_channel_mtls_with_adc(transport_class):
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


def test_insight_path():
    project = "squid"
    location = "clam"
    insight_type = "whelk"
    insight = "octopus"
    expected = "projects/{project}/locations/{location}/insightTypes/{insight_type}/insights/{insight}".format(
        project=project, location=location, insight_type=insight_type, insight=insight,
    )
    actual = RecommenderClient.insight_path(project, location, insight_type, insight)
    assert expected == actual


def test_parse_insight_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "insight_type": "cuttlefish",
        "insight": "mussel",
    }
    path = RecommenderClient.insight_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_insight_path(path)
    assert expected == actual


def test_insight_type_path():
    project = "winkle"
    location = "nautilus"
    insight_type = "scallop"
    expected = "projects/{project}/locations/{location}/insightTypes/{insight_type}".format(
        project=project, location=location, insight_type=insight_type,
    )
    actual = RecommenderClient.insight_type_path(project, location, insight_type)
    assert expected == actual


def test_parse_insight_type_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "insight_type": "clam",
    }
    path = RecommenderClient.insight_type_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_insight_type_path(path)
    assert expected == actual


def test_recommendation_path():
    project = "whelk"
    location = "octopus"
    recommender = "oyster"
    recommendation = "nudibranch"
    expected = "projects/{project}/locations/{location}/recommenders/{recommender}/recommendations/{recommendation}".format(
        project=project,
        location=location,
        recommender=recommender,
        recommendation=recommendation,
    )
    actual = RecommenderClient.recommendation_path(
        project, location, recommender, recommendation
    )
    assert expected == actual


def test_parse_recommendation_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "recommender": "winkle",
        "recommendation": "nautilus",
    }
    path = RecommenderClient.recommendation_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_recommendation_path(path)
    assert expected == actual


def test_recommender_path():
    project = "scallop"
    location = "abalone"
    recommender = "squid"
    expected = "projects/{project}/locations/{location}/recommenders/{recommender}".format(
        project=project, location=location, recommender=recommender,
    )
    actual = RecommenderClient.recommender_path(project, location, recommender)
    assert expected == actual


def test_parse_recommender_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "recommender": "octopus",
    }
    path = RecommenderClient.recommender_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_recommender_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RecommenderClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = RecommenderClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder,)
    actual = RecommenderClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = RecommenderClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = RecommenderClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = RecommenderClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project,)
    actual = RecommenderClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = RecommenderClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = RecommenderClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = RecommenderClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RecommenderClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RecommenderTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RecommenderClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RecommenderTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RecommenderClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
