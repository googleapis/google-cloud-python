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
from google.cloud.dialogflow_v2beta1.services.conversations import (
    ConversationsAsyncClient,
)
from google.cloud.dialogflow_v2beta1.services.conversations import ConversationsClient
from google.cloud.dialogflow_v2beta1.services.conversations import pagers
from google.cloud.dialogflow_v2beta1.services.conversations import transports
from google.cloud.dialogflow_v2beta1.services.conversations.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.dialogflow_v2beta1.types import conversation
from google.cloud.dialogflow_v2beta1.types import conversation as gcd_conversation
from google.cloud.dialogflow_v2beta1.types import participant
from google.cloud.dialogflow_v2beta1.types import session
from google.oauth2 import service_account
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

    assert ConversationsClient._get_default_mtls_endpoint(None) is None
    assert (
        ConversationsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConversationsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConversationsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConversationsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConversationsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ConversationsClient, ConversationsAsyncClient,]
)
def test_conversations_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "dialogflow.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ConversationsGrpcTransport, "grpc"),
        (transports.ConversationsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_conversations_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class", [ConversationsClient, ConversationsAsyncClient,]
)
def test_conversations_client_from_service_account_file(client_class):
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

        assert client.transport._host == "dialogflow.googleapis.com:443"


def test_conversations_client_get_transport_class():
    transport = ConversationsClient.get_transport_class()
    available_transports = [
        transports.ConversationsGrpcTransport,
    ]
    assert transport in available_transports

    transport = ConversationsClient.get_transport_class("grpc")
    assert transport == transports.ConversationsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ConversationsClient, transports.ConversationsGrpcTransport, "grpc"),
        (
            ConversationsAsyncClient,
            transports.ConversationsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ConversationsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversationsClient),
)
@mock.patch.object(
    ConversationsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversationsAsyncClient),
)
def test_conversations_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ConversationsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ConversationsClient, "get_transport_class") as gtc:
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
            always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (ConversationsClient, transports.ConversationsGrpcTransport, "grpc", "true"),
        (
            ConversationsAsyncClient,
            transports.ConversationsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ConversationsClient, transports.ConversationsGrpcTransport, "grpc", "false"),
        (
            ConversationsAsyncClient,
            transports.ConversationsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ConversationsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversationsClient),
)
@mock.patch.object(
    ConversationsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversationsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_conversations_client_mtls_env_auto(
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
                always_use_jwt_access=True,
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
                        always_use_jwt_access=True,
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
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ConversationsClient, transports.ConversationsGrpcTransport, "grpc"),
        (
            ConversationsAsyncClient,
            transports.ConversationsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_conversations_client_client_options_scopes(
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ConversationsClient, transports.ConversationsGrpcTransport, "grpc"),
        (
            ConversationsAsyncClient,
            transports.ConversationsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_conversations_client_client_options_credentials_file(
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
            always_use_jwt_access=True,
        )


def test_conversations_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.conversations.transports.ConversationsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConversationsClient(
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
            always_use_jwt_access=True,
        )


def test_create_conversation(
    transport: str = "grpc", request_type=gcd_conversation.CreateConversationRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_conversation.Conversation(
            name="name_value",
            lifecycle_state=gcd_conversation.Conversation.LifecycleState.IN_PROGRESS,
            conversation_profile="conversation_profile_value",
            conversation_stage=gcd_conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
        )
        response = client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_conversation.CreateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state
        == gcd_conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == gcd_conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


def test_create_conversation_from_dict():
    test_create_conversation(request_type=dict)


def test_create_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        client.create_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_conversation.CreateConversationRequest()


@pytest.mark.asyncio
async def test_create_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_conversation.CreateConversationRequest,
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_conversation.Conversation(
                name="name_value",
                lifecycle_state=gcd_conversation.Conversation.LifecycleState.IN_PROGRESS,
                conversation_profile="conversation_profile_value",
                conversation_stage=gcd_conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
            )
        )
        response = await client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_conversation.CreateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state
        == gcd_conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == gcd_conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


@pytest.mark.asyncio
async def test_create_conversation_async_from_dict():
    await test_create_conversation_async(request_type=dict)


def test_create_conversation_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_conversation.CreateConversationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        call.return_value = gcd_conversation.Conversation()
        client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_conversation_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_conversation.CreateConversationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_conversation.Conversation()
        )
        await client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_conversation_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_conversation.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversation(
            parent="parent_value",
            conversation=gcd_conversation.Conversation(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].conversation == gcd_conversation.Conversation(name="name_value")


def test_create_conversation_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversation(
            gcd_conversation.CreateConversationRequest(),
            parent="parent_value",
            conversation=gcd_conversation.Conversation(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_conversation_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_conversation.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_conversation.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversation(
            parent="parent_value",
            conversation=gcd_conversation.Conversation(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].conversation == gcd_conversation.Conversation(name="name_value")


@pytest.mark.asyncio
async def test_create_conversation_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversation(
            gcd_conversation.CreateConversationRequest(),
            parent="parent_value",
            conversation=gcd_conversation.Conversation(name="name_value"),
        )


def test_list_conversations(
    transport: str = "grpc", request_type=conversation.ListConversationsRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListConversationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListConversationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversations_from_dict():
    test_list_conversations(request_type=dict)


def test_list_conversations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        client.list_conversations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListConversationsRequest()


@pytest.mark.asyncio
async def test_list_conversations_async(
    transport: str = "grpc_asyncio", request_type=conversation.ListConversationsRequest
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListConversationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListConversationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_conversations_async_from_dict():
    await test_list_conversations_async(request_type=dict)


def test_list_conversations_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.ListConversationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        call.return_value = conversation.ListConversationsResponse()
        client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_conversations_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.ListConversationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListConversationsResponse()
        )
        await client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_conversations_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListConversationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_conversations_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversations(
            conversation.ListConversationsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversations_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListConversationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListConversationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_conversations_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversations(
            conversation.ListConversationsRequest(), parent="parent_value",
        )


def test_list_conversations_pager():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
                next_page_token="abc",
            ),
            conversation.ListConversationsResponse(
                conversations=[], next_page_token="def",
            ),
            conversation.ListConversationsResponse(
                conversations=[conversation.Conversation(),], next_page_token="ghi",
            ),
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, conversation.Conversation) for i in results)


def test_list_conversations_pages():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
                next_page_token="abc",
            ),
            conversation.ListConversationsResponse(
                conversations=[], next_page_token="def",
            ),
            conversation.ListConversationsResponse(
                conversations=[conversation.Conversation(),], next_page_token="ghi",
            ),
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversations_async_pager():
    client = ConversationsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
                next_page_token="abc",
            ),
            conversation.ListConversationsResponse(
                conversations=[], next_page_token="def",
            ),
            conversation.ListConversationsResponse(
                conversations=[conversation.Conversation(),], next_page_token="ghi",
            ),
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversations(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, conversation.Conversation) for i in responses)


@pytest.mark.asyncio
async def test_list_conversations_async_pages():
    client = ConversationsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
                next_page_token="abc",
            ),
            conversation.ListConversationsResponse(
                conversations=[], next_page_token="def",
            ),
            conversation.ListConversationsResponse(
                conversations=[conversation.Conversation(),], next_page_token="ghi",
            ),
            conversation.ListConversationsResponse(
                conversations=[
                    conversation.Conversation(),
                    conversation.Conversation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_conversations(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_conversation(
    transport: str = "grpc", request_type=conversation.GetConversationRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation(
            name="name_value",
            lifecycle_state=conversation.Conversation.LifecycleState.IN_PROGRESS,
            conversation_profile="conversation_profile_value",
            conversation_stage=conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
        )
        response = client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.GetConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state == conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


def test_get_conversation_from_dict():
    test_get_conversation(request_type=dict)


def test_get_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        client.get_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.GetConversationRequest()


@pytest.mark.asyncio
async def test_get_conversation_async(
    transport: str = "grpc_asyncio", request_type=conversation.GetConversationRequest
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation(
                name="name_value",
                lifecycle_state=conversation.Conversation.LifecycleState.IN_PROGRESS,
                conversation_profile="conversation_profile_value",
                conversation_stage=conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
            )
        )
        response = await client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.GetConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state == conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


@pytest.mark.asyncio
async def test_get_conversation_async_from_dict():
    await test_get_conversation_async(request_type=dict)


def test_get_conversation_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.GetConversationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        call.return_value = conversation.Conversation()
        client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_conversation_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.GetConversationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation()
        )
        await client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_conversation_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_conversation_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversation(
            conversation.GetConversationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversation_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_conversation_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversation(
            conversation.GetConversationRequest(), name="name_value",
        )


def test_complete_conversation(
    transport: str = "grpc", request_type=conversation.CompleteConversationRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation(
            name="name_value",
            lifecycle_state=conversation.Conversation.LifecycleState.IN_PROGRESS,
            conversation_profile="conversation_profile_value",
            conversation_stage=conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
        )
        response = client.complete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.CompleteConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state == conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


def test_complete_conversation_from_dict():
    test_complete_conversation(request_type=dict)


def test_complete_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        client.complete_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.CompleteConversationRequest()


@pytest.mark.asyncio
async def test_complete_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=conversation.CompleteConversationRequest,
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation(
                name="name_value",
                lifecycle_state=conversation.Conversation.LifecycleState.IN_PROGRESS,
                conversation_profile="conversation_profile_value",
                conversation_stage=conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE,
            )
        )
        response = await client.complete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.CompleteConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.Conversation)
    assert response.name == "name_value"
    assert (
        response.lifecycle_state == conversation.Conversation.LifecycleState.IN_PROGRESS
    )
    assert response.conversation_profile == "conversation_profile_value"
    assert (
        response.conversation_stage
        == conversation.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE
    )


@pytest.mark.asyncio
async def test_complete_conversation_async_from_dict():
    await test_complete_conversation_async(request_type=dict)


def test_complete_conversation_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.CompleteConversationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        call.return_value = conversation.Conversation()
        client.complete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_complete_conversation_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.CompleteConversationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation()
        )
        await client.complete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_complete_conversation_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.complete_conversation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_complete_conversation_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.complete_conversation(
            conversation.CompleteConversationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_complete_conversation_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.complete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.complete_conversation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_complete_conversation_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.complete_conversation(
            conversation.CompleteConversationRequest(), name="name_value",
        )


def test_batch_create_messages(
    transport: str = "grpc", request_type=conversation.BatchCreateMessagesRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.BatchCreateMessagesResponse()
        response = client.batch_create_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.BatchCreateMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.BatchCreateMessagesResponse)


def test_batch_create_messages_from_dict():
    test_batch_create_messages(request_type=dict)


def test_batch_create_messages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        client.batch_create_messages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.BatchCreateMessagesRequest()


@pytest.mark.asyncio
async def test_batch_create_messages_async(
    transport: str = "grpc_asyncio",
    request_type=conversation.BatchCreateMessagesRequest,
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.BatchCreateMessagesResponse()
        )
        response = await client.batch_create_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.BatchCreateMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversation.BatchCreateMessagesResponse)


@pytest.mark.asyncio
async def test_batch_create_messages_async_from_dict():
    await test_batch_create_messages_async(request_type=dict)


def test_batch_create_messages_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.BatchCreateMessagesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        call.return_value = conversation.BatchCreateMessagesResponse()
        client.batch_create_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_messages_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.BatchCreateMessagesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.BatchCreateMessagesResponse()
        )
        await client.batch_create_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_create_messages_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.BatchCreateMessagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_messages(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_batch_create_messages_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_messages(
            conversation.BatchCreateMessagesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_batch_create_messages_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_messages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.BatchCreateMessagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.BatchCreateMessagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_messages(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_batch_create_messages_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_messages(
            conversation.BatchCreateMessagesRequest(), parent="parent_value",
        )


def test_list_messages(
    transport: str = "grpc", request_type=conversation.ListMessagesRequest
):
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListMessagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMessagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_messages_from_dict():
    test_list_messages(request_type=dict)


def test_list_messages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        client.list_messages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListMessagesRequest()


@pytest.mark.asyncio
async def test_list_messages_async(
    transport: str = "grpc_asyncio", request_type=conversation.ListMessagesRequest
):
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListMessagesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversation.ListMessagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMessagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_messages_async_from_dict():
    await test_list_messages_async(request_type=dict)


def test_list_messages_field_headers():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.ListMessagesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        call.return_value = conversation.ListMessagesResponse()
        client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_messages_field_headers_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversation.ListMessagesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListMessagesResponse()
        )
        await client.list_messages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_messages_flattened():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListMessagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_messages(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_messages_flattened_error():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_messages(
            conversation.ListMessagesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_messages_flattened_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversation.ListMessagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversation.ListMessagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_messages(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_messages_flattened_error_async():
    client = ConversationsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_messages(
            conversation.ListMessagesRequest(), parent="parent_value",
        )


def test_list_messages_pager():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListMessagesResponse(
                messages=[
                    participant.Message(),
                    participant.Message(),
                    participant.Message(),
                ],
                next_page_token="abc",
            ),
            conversation.ListMessagesResponse(messages=[], next_page_token="def",),
            conversation.ListMessagesResponse(
                messages=[participant.Message(),], next_page_token="ghi",
            ),
            conversation.ListMessagesResponse(
                messages=[participant.Message(), participant.Message(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_messages(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, participant.Message) for i in results)


def test_list_messages_pages():
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_messages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListMessagesResponse(
                messages=[
                    participant.Message(),
                    participant.Message(),
                    participant.Message(),
                ],
                next_page_token="abc",
            ),
            conversation.ListMessagesResponse(messages=[], next_page_token="def",),
            conversation.ListMessagesResponse(
                messages=[participant.Message(),], next_page_token="ghi",
            ),
            conversation.ListMessagesResponse(
                messages=[participant.Message(), participant.Message(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_messages(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_messages_async_pager():
    client = ConversationsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_messages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListMessagesResponse(
                messages=[
                    participant.Message(),
                    participant.Message(),
                    participant.Message(),
                ],
                next_page_token="abc",
            ),
            conversation.ListMessagesResponse(messages=[], next_page_token="def",),
            conversation.ListMessagesResponse(
                messages=[participant.Message(),], next_page_token="ghi",
            ),
            conversation.ListMessagesResponse(
                messages=[participant.Message(), participant.Message(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_messages(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, participant.Message) for i in responses)


@pytest.mark.asyncio
async def test_list_messages_async_pages():
    client = ConversationsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_messages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversation.ListMessagesResponse(
                messages=[
                    participant.Message(),
                    participant.Message(),
                    participant.Message(),
                ],
                next_page_token="abc",
            ),
            conversation.ListMessagesResponse(messages=[], next_page_token="def",),
            conversation.ListMessagesResponse(
                messages=[participant.Message(),], next_page_token="ghi",
            ),
            conversation.ListMessagesResponse(
                messages=[participant.Message(), participant.Message(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_messages(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ConversationsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversationsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ConversationsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversationsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ConversationsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversationsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConversationsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ConversationsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConversationsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ConversationsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
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
    client = ConversationsClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.ConversationsGrpcTransport,)


def test_conversations_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ConversationsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_conversations_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.conversations.transports.ConversationsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ConversationsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_conversation",
        "list_conversations",
        "get_conversation",
        "complete_conversation",
        "batch_create_messages",
        "list_messages",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_conversations_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.conversations.transports.ConversationsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConversationsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_conversations_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.conversations.transports.ConversationsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConversationsTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_conversations_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.conversations.transports.ConversationsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConversationsTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_conversations_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ConversationsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_conversations_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ConversationsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_conversations_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_conversations_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ConversationsGrpcTransport, grpc_helpers),
        (transports.ConversationsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_conversations_transport_create_channel(transport_class, grpc_helpers):
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
            "dialogflow.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=["1", "2"],
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
    ],
)
def test_conversations_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_conversations_host_no_port():
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_conversations_host_with_port():
    client = ConversationsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_conversations_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConversationsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_conversations_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConversationsGrpcAsyncIOTransport(
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
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
    ],
)
def test_conversations_transport_channel_mtls_with_client_cert_source(transport_class):
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
        transports.ConversationsGrpcTransport,
        transports.ConversationsGrpcAsyncIOTransport,
    ],
)
def test_conversations_transport_channel_mtls_with_adc(transport_class):
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


def test_conversation_path():
    project = "squid"
    conversation = "clam"
    expected = "projects/{project}/conversations/{conversation}".format(
        project=project, conversation=conversation,
    )
    actual = ConversationsClient.conversation_path(project, conversation)
    assert expected == actual


def test_parse_conversation_path():
    expected = {
        "project": "whelk",
        "conversation": "octopus",
    }
    path = ConversationsClient.conversation_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_conversation_path(path)
    assert expected == actual


def test_conversation_profile_path():
    project = "oyster"
    conversation_profile = "nudibranch"
    expected = "projects/{project}/conversationProfiles/{conversation_profile}".format(
        project=project, conversation_profile=conversation_profile,
    )
    actual = ConversationsClient.conversation_profile_path(
        project, conversation_profile
    )
    assert expected == actual


def test_parse_conversation_profile_path():
    expected = {
        "project": "cuttlefish",
        "conversation_profile": "mussel",
    }
    path = ConversationsClient.conversation_profile_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_conversation_profile_path(path)
    assert expected == actual


def test_message_path():
    project = "winkle"
    conversation = "nautilus"
    message = "scallop"
    expected = "projects/{project}/conversations/{conversation}/messages/{message}".format(
        project=project, conversation=conversation, message=message,
    )
    actual = ConversationsClient.message_path(project, conversation, message)
    assert expected == actual


def test_parse_message_path():
    expected = {
        "project": "abalone",
        "conversation": "squid",
        "message": "clam",
    }
    path = ConversationsClient.message_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_message_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ConversationsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = ConversationsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = ConversationsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = ConversationsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = ConversationsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = ConversationsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = ConversationsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = ConversationsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ConversationsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = ConversationsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversationsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ConversationsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ConversationsClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ConversationsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ConversationsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
