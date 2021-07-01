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
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import (
    PolicyTagManagerAsyncClient,
)
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import (
    PolicyTagManagerClient,
)
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import pagers
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import transports
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.datacatalog_v1beta1.types import policytagmanager
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
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

    assert PolicyTagManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        PolicyTagManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PolicyTagManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PolicyTagManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PolicyTagManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PolicyTagManagerClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [PolicyTagManagerClient, PolicyTagManagerAsyncClient,]
)
def test_policy_tag_manager_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "datacatalog.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [PolicyTagManagerClient, PolicyTagManagerAsyncClient,]
)
def test_policy_tag_manager_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.PolicyTagManagerGrpcTransport, "grpc"),
        (transports.PolicyTagManagerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_policy_tag_manager_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [PolicyTagManagerClient, PolicyTagManagerAsyncClient,]
)
def test_policy_tag_manager_client_from_service_account_file(client_class):
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

        assert client.transport._host == "datacatalog.googleapis.com:443"


def test_policy_tag_manager_client_get_transport_class():
    transport = PolicyTagManagerClient.get_transport_class()
    available_transports = [
        transports.PolicyTagManagerGrpcTransport,
    ]
    assert transport in available_transports

    transport = PolicyTagManagerClient.get_transport_class("grpc")
    assert transport == transports.PolicyTagManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PolicyTagManagerClient, transports.PolicyTagManagerGrpcTransport, "grpc"),
        (
            PolicyTagManagerAsyncClient,
            transports.PolicyTagManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    PolicyTagManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PolicyTagManagerClient),
)
@mock.patch.object(
    PolicyTagManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PolicyTagManagerAsyncClient),
)
def test_policy_tag_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(PolicyTagManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(PolicyTagManagerClient, "get_transport_class") as gtc:
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
            PolicyTagManagerClient,
            transports.PolicyTagManagerGrpcTransport,
            "grpc",
            "true",
        ),
        (
            PolicyTagManagerAsyncClient,
            transports.PolicyTagManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            PolicyTagManagerClient,
            transports.PolicyTagManagerGrpcTransport,
            "grpc",
            "false",
        ),
        (
            PolicyTagManagerAsyncClient,
            transports.PolicyTagManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    PolicyTagManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PolicyTagManagerClient),
)
@mock.patch.object(
    PolicyTagManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PolicyTagManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_policy_tag_manager_client_mtls_env_auto(
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
        (PolicyTagManagerClient, transports.PolicyTagManagerGrpcTransport, "grpc"),
        (
            PolicyTagManagerAsyncClient,
            transports.PolicyTagManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_policy_tag_manager_client_client_options_scopes(
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
        (PolicyTagManagerClient, transports.PolicyTagManagerGrpcTransport, "grpc"),
        (
            PolicyTagManagerAsyncClient,
            transports.PolicyTagManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_policy_tag_manager_client_client_options_credentials_file(
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


def test_policy_tag_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = PolicyTagManagerClient(
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


def test_create_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.CreateTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            activated_policy_types=[
                policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
            ],
        )
        response = client.create_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreateTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_create_taxonomy_from_dict():
    test_create_taxonomy(request_type=dict)


def test_create_taxonomy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        client.create_taxonomy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreateTaxonomyRequest()


@pytest.mark.asyncio
async def test_create_taxonomy_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.CreateTaxonomyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                activated_policy_types=[
                    policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
                ],
            )
        )
        response = await client.create_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreateTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


@pytest.mark.asyncio
async def test_create_taxonomy_async_from_dict():
    await test_create_taxonomy_async(request_type=dict)


def test_create_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreateTaxonomyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        call.return_value = policytagmanager.Taxonomy()
        client.create_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_taxonomy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreateTaxonomyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        await client.create_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_taxonomy_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_taxonomy(
            parent="parent_value",
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].taxonomy == policytagmanager.Taxonomy(name="name_value")


def test_create_taxonomy_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_taxonomy(
            policytagmanager.CreateTaxonomyRequest(),
            parent="parent_value",
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_taxonomy(
            parent="parent_value",
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].taxonomy == policytagmanager.Taxonomy(name="name_value")


@pytest.mark.asyncio
async def test_create_taxonomy_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_taxonomy(
            policytagmanager.CreateTaxonomyRequest(),
            parent="parent_value",
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )


def test_delete_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.DeleteTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeleteTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_taxonomy_from_dict():
    test_delete_taxonomy(request_type=dict)


def test_delete_taxonomy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        client.delete_taxonomy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeleteTaxonomyRequest()


@pytest.mark.asyncio
async def test_delete_taxonomy_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.DeleteTaxonomyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeleteTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_taxonomy_async_from_dict():
    await test_delete_taxonomy_async(request_type=dict)


def test_delete_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeleteTaxonomyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        call.return_value = None
        client.delete_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_taxonomy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeleteTaxonomyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_taxonomy_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_taxonomy(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_taxonomy_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_taxonomy(
            policytagmanager.DeleteTaxonomyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_taxonomy(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_taxonomy_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_taxonomy(
            policytagmanager.DeleteTaxonomyRequest(), name="name_value",
        )


def test_update_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.UpdateTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            activated_policy_types=[
                policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
            ],
        )
        response = client.update_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdateTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_update_taxonomy_from_dict():
    test_update_taxonomy(request_type=dict)


def test_update_taxonomy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        client.update_taxonomy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdateTaxonomyRequest()


@pytest.mark.asyncio
async def test_update_taxonomy_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.UpdateTaxonomyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                activated_policy_types=[
                    policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
                ],
            )
        )
        response = await client.update_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdateTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


@pytest.mark.asyncio
async def test_update_taxonomy_async_from_dict():
    await test_update_taxonomy_async(request_type=dict)


def test_update_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdateTaxonomyRequest()

    request.taxonomy.name = "taxonomy.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        call.return_value = policytagmanager.Taxonomy()
        client.update_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "taxonomy.name=taxonomy.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_taxonomy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdateTaxonomyRequest()

    request.taxonomy.name = "taxonomy.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        await client.update_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "taxonomy.name=taxonomy.name/value",) in kw[
        "metadata"
    ]


def test_update_taxonomy_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_taxonomy(taxonomy=policytagmanager.Taxonomy(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].taxonomy == policytagmanager.Taxonomy(name="name_value")


def test_update_taxonomy_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_taxonomy(
            policytagmanager.UpdateTaxonomyRequest(),
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_taxonomy(
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].taxonomy == policytagmanager.Taxonomy(name="name_value")


@pytest.mark.asyncio
async def test_update_taxonomy_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_taxonomy(
            policytagmanager.UpdateTaxonomyRequest(),
            taxonomy=policytagmanager.Taxonomy(name="name_value"),
        )


def test_list_taxonomies(
    transport: str = "grpc", request_type=policytagmanager.ListTaxonomiesRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListTaxonomiesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_taxonomies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListTaxonomiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTaxonomiesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_taxonomies_from_dict():
    test_list_taxonomies(request_type=dict)


def test_list_taxonomies_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        client.list_taxonomies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListTaxonomiesRequest()


@pytest.mark.asyncio
async def test_list_taxonomies_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.ListTaxonomiesRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListTaxonomiesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_taxonomies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListTaxonomiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTaxonomiesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_taxonomies_async_from_dict():
    await test_list_taxonomies_async(request_type=dict)


def test_list_taxonomies_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListTaxonomiesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        call.return_value = policytagmanager.ListTaxonomiesResponse()
        client.list_taxonomies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_taxonomies_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListTaxonomiesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListTaxonomiesResponse()
        )
        await client.list_taxonomies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_taxonomies_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListTaxonomiesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_taxonomies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_taxonomies_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_taxonomies(
            policytagmanager.ListTaxonomiesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_taxonomies_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListTaxonomiesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListTaxonomiesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_taxonomies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_taxonomies_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_taxonomies(
            policytagmanager.ListTaxonomiesRequest(), parent="parent_value",
        )


def test_list_taxonomies_pager():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[], next_page_token="def",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(),], next_page_token="ghi",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(), policytagmanager.Taxonomy(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_taxonomies(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, policytagmanager.Taxonomy) for i in results)


def test_list_taxonomies_pages():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_taxonomies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[], next_page_token="def",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(),], next_page_token="ghi",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(), policytagmanager.Taxonomy(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_taxonomies(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_taxonomies_async_pager():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_taxonomies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[], next_page_token="def",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(),], next_page_token="ghi",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(), policytagmanager.Taxonomy(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_taxonomies(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, policytagmanager.Taxonomy) for i in responses)


@pytest.mark.asyncio
async def test_list_taxonomies_async_pages():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_taxonomies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                    policytagmanager.Taxonomy(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[], next_page_token="def",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(),], next_page_token="ghi",
            ),
            policytagmanager.ListTaxonomiesResponse(
                taxonomies=[policytagmanager.Taxonomy(), policytagmanager.Taxonomy(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_taxonomies(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.GetTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            activated_policy_types=[
                policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
            ],
        )
        response = client.get_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_get_taxonomy_from_dict():
    test_get_taxonomy(request_type=dict)


def test_get_taxonomy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        client.get_taxonomy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetTaxonomyRequest()


@pytest.mark.asyncio
async def test_get_taxonomy_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.GetTaxonomyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                activated_policy_types=[
                    policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
                ],
            )
        )
        response = await client.get_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetTaxonomyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


@pytest.mark.asyncio
async def test_get_taxonomy_async_from_dict():
    await test_get_taxonomy_async(request_type=dict)


def test_get_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetTaxonomyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        call.return_value = policytagmanager.Taxonomy()
        client.get_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_taxonomy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetTaxonomyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        await client.get_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_taxonomy_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_taxonomy(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_taxonomy_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_taxonomy(
            policytagmanager.GetTaxonomyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_taxonomy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.Taxonomy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.Taxonomy()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_taxonomy(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_taxonomy_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_taxonomy(
            policytagmanager.GetTaxonomyRequest(), name="name_value",
        )


def test_create_policy_tag(
    transport: str = "grpc", request_type=policytagmanager.CreatePolicyTagRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            parent_policy_tag="parent_policy_tag_value",
            child_policy_tags=["child_policy_tags_value"],
        )
        response = client.create_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreatePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_create_policy_tag_from_dict():
    test_create_policy_tag(request_type=dict)


def test_create_policy_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        client.create_policy_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreatePolicyTagRequest()


@pytest.mark.asyncio
async def test_create_policy_tag_async(
    transport: str = "grpc_asyncio",
    request_type=policytagmanager.CreatePolicyTagRequest,
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                parent_policy_tag="parent_policy_tag_value",
                child_policy_tags=["child_policy_tags_value"],
            )
        )
        response = await client.create_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.CreatePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


@pytest.mark.asyncio
async def test_create_policy_tag_async_from_dict():
    await test_create_policy_tag_async(request_type=dict)


def test_create_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreatePolicyTagRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        call.return_value = policytagmanager.PolicyTag()
        client.create_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_policy_tag_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreatePolicyTagRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        await client.create_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_policy_tag_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_policy_tag(
            parent="parent_value",
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].policy_tag == policytagmanager.PolicyTag(name="name_value")


def test_create_policy_tag_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_policy_tag(
            policytagmanager.CreatePolicyTagRequest(),
            parent="parent_value",
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_policy_tag(
            parent="parent_value",
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].policy_tag == policytagmanager.PolicyTag(name="name_value")


@pytest.mark.asyncio
async def test_create_policy_tag_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_policy_tag(
            policytagmanager.CreatePolicyTagRequest(),
            parent="parent_value",
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )


def test_delete_policy_tag(
    transport: str = "grpc", request_type=policytagmanager.DeletePolicyTagRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeletePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_policy_tag_from_dict():
    test_delete_policy_tag(request_type=dict)


def test_delete_policy_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        client.delete_policy_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeletePolicyTagRequest()


@pytest.mark.asyncio
async def test_delete_policy_tag_async(
    transport: str = "grpc_asyncio",
    request_type=policytagmanager.DeletePolicyTagRequest,
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.DeletePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_policy_tag_async_from_dict():
    await test_delete_policy_tag_async(request_type=dict)


def test_delete_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeletePolicyTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        call.return_value = None
        client.delete_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_policy_tag_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeletePolicyTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_policy_tag_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_policy_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_policy_tag_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_policy_tag(
            policytagmanager.DeletePolicyTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_policy_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_policy_tag_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_policy_tag(
            policytagmanager.DeletePolicyTagRequest(), name="name_value",
        )


def test_update_policy_tag(
    transport: str = "grpc", request_type=policytagmanager.UpdatePolicyTagRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            parent_policy_tag="parent_policy_tag_value",
            child_policy_tags=["child_policy_tags_value"],
        )
        response = client.update_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdatePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_update_policy_tag_from_dict():
    test_update_policy_tag(request_type=dict)


def test_update_policy_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        client.update_policy_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdatePolicyTagRequest()


@pytest.mark.asyncio
async def test_update_policy_tag_async(
    transport: str = "grpc_asyncio",
    request_type=policytagmanager.UpdatePolicyTagRequest,
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                parent_policy_tag="parent_policy_tag_value",
                child_policy_tags=["child_policy_tags_value"],
            )
        )
        response = await client.update_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.UpdatePolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


@pytest.mark.asyncio
async def test_update_policy_tag_async_from_dict():
    await test_update_policy_tag_async(request_type=dict)


def test_update_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdatePolicyTagRequest()

    request.policy_tag.name = "policy_tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        call.return_value = policytagmanager.PolicyTag()
        client.update_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "policy_tag.name=policy_tag.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_policy_tag_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdatePolicyTagRequest()

    request.policy_tag.name = "policy_tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        await client.update_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "policy_tag.name=policy_tag.name/value",) in kw[
        "metadata"
    ]


def test_update_policy_tag_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_policy_tag(
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].policy_tag == policytagmanager.PolicyTag(name="name_value")


def test_update_policy_tag_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_policy_tag(
            policytagmanager.UpdatePolicyTagRequest(),
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_policy_tag(
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].policy_tag == policytagmanager.PolicyTag(name="name_value")


@pytest.mark.asyncio
async def test_update_policy_tag_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_policy_tag(
            policytagmanager.UpdatePolicyTagRequest(),
            policy_tag=policytagmanager.PolicyTag(name="name_value"),
        )


def test_list_policy_tags(
    transport: str = "grpc", request_type=policytagmanager.ListPolicyTagsRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListPolicyTagsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_policy_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListPolicyTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPolicyTagsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_policy_tags_from_dict():
    test_list_policy_tags(request_type=dict)


def test_list_policy_tags_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        client.list_policy_tags()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListPolicyTagsRequest()


@pytest.mark.asyncio
async def test_list_policy_tags_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.ListPolicyTagsRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListPolicyTagsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_policy_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.ListPolicyTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPolicyTagsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_policy_tags_async_from_dict():
    await test_list_policy_tags_async(request_type=dict)


def test_list_policy_tags_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListPolicyTagsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        call.return_value = policytagmanager.ListPolicyTagsResponse()
        client.list_policy_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_policy_tags_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListPolicyTagsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListPolicyTagsResponse()
        )
        await client.list_policy_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_policy_tags_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListPolicyTagsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_policy_tags(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_policy_tags_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_policy_tags(
            policytagmanager.ListPolicyTagsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_policy_tags_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.ListPolicyTagsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.ListPolicyTagsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_policy_tags(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_policy_tags_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_policy_tags(
            policytagmanager.ListPolicyTagsRequest(), parent="parent_value",
        )


def test_list_policy_tags_pager():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[], next_page_token="def",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[policytagmanager.PolicyTag(),], next_page_token="ghi",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_policy_tags(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, policytagmanager.PolicyTag) for i in results)


def test_list_policy_tags_pages():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policy_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[], next_page_token="def",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[policytagmanager.PolicyTag(),], next_page_token="ghi",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_policy_tags(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_policy_tags_async_pager():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_policy_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[], next_page_token="def",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[policytagmanager.PolicyTag(),], next_page_token="ghi",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_policy_tags(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, policytagmanager.PolicyTag) for i in responses)


@pytest.mark.asyncio
async def test_list_policy_tags_async_pages():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_policy_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
                next_page_token="abc",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[], next_page_token="def",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[policytagmanager.PolicyTag(),], next_page_token="ghi",
            ),
            policytagmanager.ListPolicyTagsResponse(
                policy_tags=[
                    policytagmanager.PolicyTag(),
                    policytagmanager.PolicyTag(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_policy_tags(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_policy_tag(
    transport: str = "grpc", request_type=policytagmanager.GetPolicyTagRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            parent_policy_tag="parent_policy_tag_value",
            child_policy_tags=["child_policy_tags_value"],
        )
        response = client.get_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetPolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_get_policy_tag_from_dict():
    test_get_policy_tag(request_type=dict)


def test_get_policy_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        client.get_policy_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetPolicyTagRequest()


@pytest.mark.asyncio
async def test_get_policy_tag_async(
    transport: str = "grpc_asyncio", request_type=policytagmanager.GetPolicyTagRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                parent_policy_tag="parent_policy_tag_value",
                child_policy_tags=["child_policy_tags_value"],
            )
        )
        response = await client.get_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == policytagmanager.GetPolicyTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.parent_policy_tag == "parent_policy_tag_value"
    assert response.child_policy_tags == ["child_policy_tags_value"]


@pytest.mark.asyncio
async def test_get_policy_tag_async_from_dict():
    await test_get_policy_tag_async(request_type=dict)


def test_get_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetPolicyTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        call.return_value = policytagmanager.PolicyTag()
        client.get_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_policy_tag_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetPolicyTagRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        await client.get_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_policy_tag_flattened():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_policy_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_policy_tag_flattened_error():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_policy_tag(
            policytagmanager.GetPolicyTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policytagmanager.PolicyTag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policytagmanager.PolicyTag()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_policy_tag(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_policy_tag_flattened_error_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_policy_tag(
            policytagmanager.GetPolicyTagRequest(), name="name_value",
        )


def test_get_iam_policy(
    transport: str = "grpc", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(version=774, etag=b"etag_blob",)
        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_from_dict():
    test_get_iam_policy(request_type=dict)


def test_get_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        client.get_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()


@pytest.mark.asyncio
async def test_get_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(version=774, etag=b"etag_blob",)
        )
        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async_from_dict():
    await test_get_iam_policy_async(request_type=dict)


def test_get_iam_policy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_set_iam_policy(
    transport: str = "grpc", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(version=774, etag=b"etag_blob",)
        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    test_set_iam_policy(request_type=dict)


def test_set_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        client.set_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()


@pytest.mark.asyncio
async def test_set_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(version=774, etag=b"etag_blob",)
        )
        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async_from_dict():
    await test_set_iam_policy_async(request_type=dict)


def test_set_iam_policy_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_test_iam_permissions(
    transport: str = "grpc", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )
        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    test_test_iam_permissions(request_type=dict)


def test_test_iam_permissions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        client.test_iam_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()


@pytest.mark.asyncio
async def test_test_iam_permissions_async(
    transport: str = "grpc_asyncio",
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )
        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async_from_dict():
    await test_test_iam_permissions_async(request_type=dict)


def test_test_iam_permissions_field_headers():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = PolicyTagManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )
        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = PolicyTagManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
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
    client = PolicyTagManagerClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.PolicyTagManagerGrpcTransport,)


def test_policy_tag_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.PolicyTagManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_policy_tag_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PolicyTagManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_taxonomy",
        "delete_taxonomy",
        "update_taxonomy",
        "list_taxonomies",
        "get_taxonomy",
        "create_policy_tag",
        "delete_policy_tag",
        "update_policy_tag",
        "list_policy_tags",
        "get_policy_tag",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_policy_tag_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PolicyTagManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_policy_tag_manager_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PolicyTagManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_policy_tag_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PolicyTagManagerTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_policy_tag_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        PolicyTagManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_policy_tag_manager_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        PolicyTagManagerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_policy_tag_manager_transport_auth_adc(transport_class):
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
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_policy_tag_manager_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.PolicyTagManagerGrpcTransport, grpc_helpers),
        (transports.PolicyTagManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_policy_tag_manager_transport_create_channel(transport_class, grpc_helpers):
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
            "datacatalog.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="datacatalog.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
    ],
)
def test_policy_tag_manager_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_policy_tag_manager_host_no_port():
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com"
        ),
    )
    assert client.transport._host == "datacatalog.googleapis.com:443"


def test_policy_tag_manager_host_with_port():
    client = PolicyTagManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "datacatalog.googleapis.com:8000"


def test_policy_tag_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PolicyTagManagerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_policy_tag_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
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
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
    ],
)
def test_policy_tag_manager_transport_channel_mtls_with_client_cert_source(
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
        transports.PolicyTagManagerGrpcTransport,
        transports.PolicyTagManagerGrpcAsyncIOTransport,
    ],
)
def test_policy_tag_manager_transport_channel_mtls_with_adc(transport_class):
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


def test_policy_tag_path():
    project = "squid"
    location = "clam"
    taxonomy = "whelk"
    policy_tag = "octopus"
    expected = "projects/{project}/locations/{location}/taxonomies/{taxonomy}/policyTags/{policy_tag}".format(
        project=project, location=location, taxonomy=taxonomy, policy_tag=policy_tag,
    )
    actual = PolicyTagManagerClient.policy_tag_path(
        project, location, taxonomy, policy_tag
    )
    assert expected == actual


def test_parse_policy_tag_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "taxonomy": "cuttlefish",
        "policy_tag": "mussel",
    }
    path = PolicyTagManagerClient.policy_tag_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_policy_tag_path(path)
    assert expected == actual


def test_taxonomy_path():
    project = "winkle"
    location = "nautilus"
    taxonomy = "scallop"
    expected = "projects/{project}/locations/{location}/taxonomies/{taxonomy}".format(
        project=project, location=location, taxonomy=taxonomy,
    )
    actual = PolicyTagManagerClient.taxonomy_path(project, location, taxonomy)
    assert expected == actual


def test_parse_taxonomy_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "taxonomy": "clam",
    }
    path = PolicyTagManagerClient.taxonomy_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_taxonomy_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = PolicyTagManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = PolicyTagManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = PolicyTagManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = PolicyTagManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = PolicyTagManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = PolicyTagManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = PolicyTagManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = PolicyTagManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = PolicyTagManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = PolicyTagManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.PolicyTagManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = PolicyTagManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.PolicyTagManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = PolicyTagManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
