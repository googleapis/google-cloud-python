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
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import (
    PolicyTagManagerAsyncClient,
)
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import (
    PolicyTagManagerClient,
)
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import pagers
from google.cloud.datacatalog_v1beta1.services.policy_tag_manager import transports
from google.cloud.datacatalog_v1beta1.types import policytagmanager
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


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
    "client_class", [PolicyTagManagerClient, PolicyTagManagerAsyncClient]
)
def test_policy_tag_manager_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "datacatalog.googleapis.com:443"


def test_policy_tag_manager_client_get_transport_class():
    transport = PolicyTagManagerClient.get_transport_class()
    assert transport == transports.PolicyTagManagerGrpcTransport

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
        transport = transport_class(credentials=credentials.AnonymousCredentials())
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
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
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
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
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
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_create_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.CreateTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_taxonomy), "__call__") as call:
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


@pytest.mark.asyncio
async def test_create_taxonomy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.CreateTaxonomyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_taxonomy), "__call__"
    ) as call:
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_create_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreateTaxonomyRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_taxonomy), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreateTaxonomyRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_taxonomy), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_taxonomy), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_taxonomy), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_taxonomy), "__call__") as call:
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


@pytest.mark.asyncio
async def test_delete_taxonomy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.DeleteTaxonomyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_taxonomy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_taxonomy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeleteTaxonomyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_taxonomy), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeleteTaxonomyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_taxonomy), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_taxonomy), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_taxonomy(
            policytagmanager.DeleteTaxonomyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_taxonomy), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_taxonomy), "__call__") as call:
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


@pytest.mark.asyncio
async def test_update_taxonomy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.UpdateTaxonomyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_taxonomy), "__call__"
    ) as call:
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_update_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdateTaxonomyRequest()
    request.taxonomy.name = "taxonomy.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_taxonomy), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdateTaxonomyRequest()
    request.taxonomy.name = "taxonomy.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_taxonomy), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_taxonomy), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_taxonomy), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_taxonomies), "__call__") as call:
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


@pytest.mark.asyncio
async def test_list_taxonomies_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.ListTaxonomiesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_taxonomies), "__call__"
    ) as call:
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTaxonomiesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_taxonomies_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListTaxonomiesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_taxonomies), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListTaxonomiesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_taxonomies), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_taxonomies), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_taxonomies(
            policytagmanager.ListTaxonomiesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_taxonomies_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_taxonomies), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_taxonomies(
            policytagmanager.ListTaxonomiesRequest(), parent="parent_value",
        )


def test_list_taxonomies_pager():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_taxonomies), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_taxonomies), "__call__") as call:
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
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_taxonomies_async_pager():
    client = PolicyTagManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_taxonomies),
        "__call__",
        new_callable=mock.AsyncMock,
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
    client = PolicyTagManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_taxonomies),
        "__call__",
        new_callable=mock.AsyncMock,
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
        async for page in (await client.list_taxonomies(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_taxonomy(
    transport: str = "grpc", request_type=policytagmanager.GetTaxonomyRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_taxonomy), "__call__") as call:
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


@pytest.mark.asyncio
async def test_get_taxonomy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.GetTaxonomyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_taxonomy), "__call__"
    ) as call:
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.Taxonomy)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.activated_policy_types == [
        policytagmanager.Taxonomy.PolicyType.FINE_GRAINED_ACCESS_CONTROL
    ]


def test_get_taxonomy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetTaxonomyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_taxonomy), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetTaxonomyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_taxonomy), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_taxonomy), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_taxonomy(
            policytagmanager.GetTaxonomyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_taxonomy_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_taxonomy), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_policy_tag), "__call__"
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


@pytest.mark.asyncio
async def test_create_policy_tag_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.CreatePolicyTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_policy_tag), "__call__"
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.parent_policy_tag == "parent_policy_tag_value"

    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_create_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreatePolicyTagRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.CreatePolicyTagRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_policy_tag), "__call__"
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


@pytest.mark.asyncio
async def test_delete_policy_tag_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.DeletePolicyTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_policy_tag), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeletePolicyTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.DeletePolicyTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_policy_tag(
            policytagmanager.DeletePolicyTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_policy_tag), "__call__"
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


@pytest.mark.asyncio
async def test_update_policy_tag_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.UpdatePolicyTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_policy_tag), "__call__"
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.parent_policy_tag == "parent_policy_tag_value"

    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_update_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdatePolicyTagRequest()
    request.policy_tag.name = "policy_tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.UpdatePolicyTagRequest()
    request.policy_tag.name = "policy_tag.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_policy_tag), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_policy_tag), "__call__"
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
        credentials=credentials.AnonymousCredentials(),
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
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_policy_tags), "__call__"
    ) as call:
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


@pytest.mark.asyncio
async def test_list_policy_tags_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.ListPolicyTagsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_policy_tags), "__call__"
    ) as call:
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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPolicyTagsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_policy_tags_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListPolicyTagsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_policy_tags), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.ListPolicyTagsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_policy_tags), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_policy_tags), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_policy_tags(
            policytagmanager.ListPolicyTagsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_policy_tags_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_policy_tags), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_policy_tags(
            policytagmanager.ListPolicyTagsRequest(), parent="parent_value",
        )


def test_list_policy_tags_pager():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_policy_tags), "__call__"
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_policy_tags), "__call__"
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
        pages = list(client.list_policy_tags(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_policy_tags_async_pager():
    client = PolicyTagManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_policy_tags),
        "__call__",
        new_callable=mock.AsyncMock,
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
    client = PolicyTagManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_policy_tags),
        "__call__",
        new_callable=mock.AsyncMock,
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
        async for page in (await client.list_policy_tags(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_policy_tag(
    transport: str = "grpc", request_type=policytagmanager.GetPolicyTagRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_policy_tag), "__call__") as call:
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


@pytest.mark.asyncio
async def test_get_policy_tag_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = policytagmanager.GetPolicyTagRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_policy_tag), "__call__"
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

        response = await client.get_policy_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policytagmanager.PolicyTag)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.description == "description_value"

    assert response.parent_policy_tag == "parent_policy_tag_value"

    assert response.child_policy_tags == ["child_policy_tags_value"]


def test_get_policy_tag_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetPolicyTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_policy_tag), "__call__") as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = policytagmanager.GetPolicyTagRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_policy_tag), "__call__"
    ) as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_policy_tag), "__call__") as call:
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
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_policy_tag(
            policytagmanager.GetPolicyTagRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_policy_tag_flattened_async():
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_policy_tag), "__call__"
    ) as call:
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
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_policy_tag(
            policytagmanager.GetPolicyTagRequest(), name="name_value",
        )


def test_get_iam_policy(
    transport: str = "grpc", request_type=iam_policy.GetIamPolicyRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_from_dict():
    test_get_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_set_iam_policy(
    transport: str = "grpc", request_type=iam_policy.SetIamPolicyRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    test_set_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


def test_test_iam_permissions(
    transport: str = "grpc", request_type=iam_policy.TestIamPermissionsRequest
):
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    test_test_iam_permissions(request_type=dict)


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = PolicyTagManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse(permissions=["permissions_value"],)
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

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
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

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
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PolicyTagManagerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = PolicyTagManagerClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PolicyTagManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PolicyTagManagerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.PolicyTagManagerGrpcTransport,)


def test_policy_tag_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.PolicyTagManagerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_policy_tag_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PolicyTagManagerTransport(
            credentials=credentials.AnonymousCredentials(),
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


def test_policy_tag_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.datacatalog_v1beta1.services.policy_tag_manager.transports.PolicyTagManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.PolicyTagManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_policy_tag_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        PolicyTagManagerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_policy_tag_manager_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.PolicyTagManagerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_policy_tag_manager_host_no_port():
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com"
        ),
    )
    assert client._transport._host == "datacatalog.googleapis.com:443"


def test_policy_tag_manager_host_with_port():
    client = PolicyTagManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "datacatalog.googleapis.com:8000"


def test_policy_tag_manager_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.PolicyTagManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_policy_tag_manager_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_policy_tag_manager_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.PolicyTagManagerGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_policy_tag_manager_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_policy_tag_manager_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.PolicyTagManagerGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_policy_tag_manager_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.PolicyTagManagerGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_taxonomy_path():
    project = "squid"
    location = "clam"
    taxonomy = "whelk"

    expected = "projects/{project}/locations/{location}/taxonomies/{taxonomy}".format(
        project=project, location=location, taxonomy=taxonomy,
    )
    actual = PolicyTagManagerClient.taxonomy_path(project, location, taxonomy)
    assert expected == actual


def test_parse_taxonomy_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "taxonomy": "nudibranch",
    }
    path = PolicyTagManagerClient.taxonomy_path(**expected)

    # Check that the path construction is reversible.
    actual = PolicyTagManagerClient.parse_taxonomy_path(path)
    assert expected == actual


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
