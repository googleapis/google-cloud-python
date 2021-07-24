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
from google.cloud.dialogflow_v2beta1.services.participants import (
    ParticipantsAsyncClient,
)
from google.cloud.dialogflow_v2beta1.services.participants import ParticipantsClient
from google.cloud.dialogflow_v2beta1.services.participants import pagers
from google.cloud.dialogflow_v2beta1.services.participants import transports
from google.cloud.dialogflow_v2beta1.services.participants.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.dialogflow_v2beta1.types import agent
from google.cloud.dialogflow_v2beta1.types import audio_config
from google.cloud.dialogflow_v2beta1.types import context
from google.cloud.dialogflow_v2beta1.types import entity_type
from google.cloud.dialogflow_v2beta1.types import participant
from google.cloud.dialogflow_v2beta1.types import participant as gcd_participant
from google.cloud.dialogflow_v2beta1.types import session
from google.cloud.dialogflow_v2beta1.types import session_entity_type
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
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

    assert ParticipantsClient._get_default_mtls_endpoint(None) is None
    assert (
        ParticipantsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ParticipantsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [ParticipantsClient, ParticipantsAsyncClient,])
def test_participants_client_from_service_account_info(client_class):
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
        (transports.ParticipantsGrpcTransport, "grpc"),
        (transports.ParticipantsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_participants_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize("client_class", [ParticipantsClient, ParticipantsAsyncClient,])
def test_participants_client_from_service_account_file(client_class):
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


def test_participants_client_get_transport_class():
    transport = ParticipantsClient.get_transport_class()
    available_transports = [
        transports.ParticipantsGrpcTransport,
    ]
    assert transport in available_transports

    transport = ParticipantsClient.get_transport_class("grpc")
    assert transport == transports.ParticipantsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ParticipantsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ParticipantsClient)
)
@mock.patch.object(
    ParticipantsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ParticipantsAsyncClient),
)
def test_participants_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ParticipantsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ParticipantsClient, "get_transport_class") as gtc:
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
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc", "true"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc", "false"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ParticipantsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ParticipantsClient)
)
@mock.patch.object(
    ParticipantsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ParticipantsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_participants_client_mtls_env_auto(
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
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_participants_client_client_options_scopes(
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
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_participants_client_client_options_credentials_file(
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


def test_participants_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.participants.transports.ParticipantsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ParticipantsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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


def test_create_participant(
    transport: str = "grpc", request_type=gcd_participant.CreateParticipantRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant(
            name="name_value",
            role=gcd_participant.Participant.Role.HUMAN_AGENT,
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.create_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_create_participant_from_dict():
    test_create_participant(request_type=dict)


def test_create_participant_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        client.create_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()


@pytest.mark.asyncio
async def test_create_participant_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_participant.CreateParticipantRequest,
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant(
                name="name_value",
                role=gcd_participant.Participant.Role.HUMAN_AGENT,
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.create_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_create_participant_async_from_dict():
    await test_create_participant_async(request_type=dict)


def test_create_participant_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.CreateParticipantRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        call.return_value = gcd_participant.Participant()
        client.create_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_participant_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.CreateParticipantRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        await client.create_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_participant_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_participant(
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].participant == gcd_participant.Participant(name="name_value")


def test_create_participant_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_participant(
            gcd_participant.CreateParticipantRequest(),
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_participant_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_participant(
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].participant == gcd_participant.Participant(name="name_value")


@pytest.mark.asyncio
async def test_create_participant_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_participant(
            gcd_participant.CreateParticipantRequest(),
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )


def test_get_participant(
    transport: str = "grpc", request_type=participant.GetParticipantRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.Participant(
            name="name_value",
            role=participant.Participant.Role.HUMAN_AGENT,
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.get_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.Participant)
    assert response.name == "name_value"
    assert response.role == participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_get_participant_from_dict():
    test_get_participant(request_type=dict)


def test_get_participant_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        client.get_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()


@pytest.mark.asyncio
async def test_get_participant_async(
    transport: str = "grpc_asyncio", request_type=participant.GetParticipantRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant(
                name="name_value",
                role=participant.Participant.Role.HUMAN_AGENT,
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.get_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.Participant)
    assert response.name == "name_value"
    assert response.role == participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_get_participant_async_from_dict():
    await test_get_participant_async(request_type=dict)


def test_get_participant_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.GetParticipantRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        call.return_value = participant.Participant()
        client.get_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_participant_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.GetParticipantRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant()
        )
        await client.get_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_participant_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.Participant()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_participant(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_participant_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_participant(
            participant.GetParticipantRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_participant_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_participant(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_participant_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_participant(
            participant.GetParticipantRequest(), name="name_value",
        )


def test_list_participants(
    transport: str = "grpc", request_type=participant.ListParticipantsRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.ListParticipantsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_participants(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListParticipantsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_participants_from_dict():
    test_list_participants(request_type=dict)


def test_list_participants_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        client.list_participants()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()


@pytest.mark.asyncio
async def test_list_participants_async(
    transport: str = "grpc_asyncio", request_type=participant.ListParticipantsRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_participants(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListParticipantsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_participants_async_from_dict():
    await test_list_participants_async(request_type=dict)


def test_list_participants_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.ListParticipantsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        call.return_value = participant.ListParticipantsResponse()
        client.list_participants(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_participants_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.ListParticipantsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse()
        )
        await client.list_participants(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_participants_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.ListParticipantsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_participants(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_participants_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_participants(
            participant.ListParticipantsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_participants_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.ListParticipantsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_participants(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_participants_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_participants(
            participant.ListParticipantsRequest(), parent="parent_value",
        )


def test_list_participants_pager():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[], next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(),], next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(), participant.Participant(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_participants(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, participant.Participant) for i in results)


def test_list_participants_pages():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[], next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(),], next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(), participant.Participant(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_participants(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_participants_async_pager():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[], next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(),], next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(), participant.Participant(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_participants(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, participant.Participant) for i in responses)


@pytest.mark.asyncio
async def test_list_participants_async_pages():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_participants),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[], next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(),], next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[participant.Participant(), participant.Participant(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_participants(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_participant(
    transport: str = "grpc", request_type=gcd_participant.UpdateParticipantRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant(
            name="name_value",
            role=gcd_participant.Participant.Role.HUMAN_AGENT,
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.update_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_update_participant_from_dict():
    test_update_participant(request_type=dict)


def test_update_participant_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        client.update_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()


@pytest.mark.asyncio
async def test_update_participant_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_participant.UpdateParticipantRequest,
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant(
                name="name_value",
                role=gcd_participant.Participant.Role.HUMAN_AGENT,
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.update_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_update_participant_async_from_dict():
    await test_update_participant_async(request_type=dict)


def test_update_participant_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.UpdateParticipantRequest()

    request.participant.name = "participant.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        call.return_value = gcd_participant.Participant()
        client.update_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "participant.name=participant.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_participant_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.UpdateParticipantRequest()

    request.participant.name = "participant.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        await client.update_participant(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "participant.name=participant.name/value",) in kw[
        "metadata"
    ]


def test_update_participant_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_participant(
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].participant == gcd_participant.Participant(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_participant_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_participant(
            gcd_participant.UpdateParticipantRequest(),
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_participant_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_participant(
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].participant == gcd_participant.Participant(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_participant_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_participant(
            gcd_participant.UpdateParticipantRequest(),
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_analyze_content(
    transport: str = "grpc", request_type=gcd_participant.AnalyzeContentRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.AnalyzeContentResponse(
            reply_text="reply_text_value",
        )
        response = client.analyze_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.AnalyzeContentResponse)
    assert response.reply_text == "reply_text_value"


def test_analyze_content_from_dict():
    test_analyze_content(request_type=dict)


def test_analyze_content_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        client.analyze_content()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()


@pytest.mark.asyncio
async def test_analyze_content_async(
    transport: str = "grpc_asyncio", request_type=gcd_participant.AnalyzeContentRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse(reply_text="reply_text_value",)
        )
        response = await client.analyze_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_participant.AnalyzeContentResponse)
    assert response.reply_text == "reply_text_value"


@pytest.mark.asyncio
async def test_analyze_content_async_from_dict():
    await test_analyze_content_async(request_type=dict)


def test_analyze_content_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.AnalyzeContentRequest()

    request.participant = "participant/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        call.return_value = gcd_participant.AnalyzeContentResponse()
        client.analyze_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "participant=participant/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_analyze_content_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_participant.AnalyzeContentRequest()

    request.participant = "participant/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse()
        )
        await client.analyze_content(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "participant=participant/value",) in kw["metadata"]


def test_analyze_content_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.AnalyzeContentResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.analyze_content(
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].participant == "participant_value"
        assert args[0].event_input == session.EventInput(name="name_value")


def test_analyze_content_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.analyze_content(
            gcd_participant.AnalyzeContentRequest(),
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )


@pytest.mark.asyncio
async def test_analyze_content_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_participant.AnalyzeContentResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.analyze_content(
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].participant == "participant_value"
        assert args[0].event_input == session.EventInput(name="name_value")


@pytest.mark.asyncio
async def test_analyze_content_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.analyze_content(
            gcd_participant.AnalyzeContentRequest(),
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )


def test_suggest_articles(
    transport: str = "grpc", request_type=participant.SuggestArticlesRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestArticlesResponse(
            latest_message="latest_message_value", context_size=1311,
        )
        response = client.suggest_articles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestArticlesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_articles_from_dict():
    test_suggest_articles(request_type=dict)


def test_suggest_articles_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        client.suggest_articles()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()


@pytest.mark.asyncio
async def test_suggest_articles_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestArticlesRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse(
                latest_message="latest_message_value", context_size=1311,
            )
        )
        response = await client.suggest_articles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestArticlesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_articles_async_from_dict():
    await test_suggest_articles_async(request_type=dict)


def test_suggest_articles_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestArticlesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        call.return_value = participant.SuggestArticlesResponse()
        client.suggest_articles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_articles_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestArticlesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse()
        )
        await client.suggest_articles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_suggest_articles_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestArticlesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.suggest_articles(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_suggest_articles_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.suggest_articles(
            participant.SuggestArticlesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_articles_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestArticlesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.suggest_articles(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_suggest_articles_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.suggest_articles(
            participant.SuggestArticlesRequest(), parent="parent_value",
        )


def test_suggest_faq_answers(
    transport: str = "grpc", request_type=participant.SuggestFaqAnswersRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestFaqAnswersResponse(
            latest_message="latest_message_value", context_size=1311,
        )
        response = client.suggest_faq_answers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestFaqAnswersResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_faq_answers_from_dict():
    test_suggest_faq_answers(request_type=dict)


def test_suggest_faq_answers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        client.suggest_faq_answers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()


@pytest.mark.asyncio
async def test_suggest_faq_answers_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestFaqAnswersRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse(
                latest_message="latest_message_value", context_size=1311,
            )
        )
        response = await client.suggest_faq_answers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestFaqAnswersResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_faq_answers_async_from_dict():
    await test_suggest_faq_answers_async(request_type=dict)


def test_suggest_faq_answers_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestFaqAnswersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        call.return_value = participant.SuggestFaqAnswersResponse()
        client.suggest_faq_answers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_faq_answers_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestFaqAnswersRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse()
        )
        await client.suggest_faq_answers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_suggest_faq_answers_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestFaqAnswersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.suggest_faq_answers(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_suggest_faq_answers_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.suggest_faq_answers(
            participant.SuggestFaqAnswersRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_faq_answers_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestFaqAnswersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.suggest_faq_answers(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_suggest_faq_answers_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.suggest_faq_answers(
            participant.SuggestFaqAnswersRequest(), parent="parent_value",
        )


def test_suggest_smart_replies(
    transport: str = "grpc", request_type=participant.SuggestSmartRepliesRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestSmartRepliesResponse(
            latest_message="latest_message_value", context_size=1311,
        )
        response = client.suggest_smart_replies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestSmartRepliesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_smart_replies_from_dict():
    test_suggest_smart_replies(request_type=dict)


def test_suggest_smart_replies_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        client.suggest_smart_replies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()


@pytest.mark.asyncio
async def test_suggest_smart_replies_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestSmartRepliesRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse(
                latest_message="latest_message_value", context_size=1311,
            )
        )
        response = await client.suggest_smart_replies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.SuggestSmartRepliesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_smart_replies_async_from_dict():
    await test_suggest_smart_replies_async(request_type=dict)


def test_suggest_smart_replies_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestSmartRepliesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        call.return_value = participant.SuggestSmartRepliesResponse()
        client.suggest_smart_replies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_smart_replies_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.SuggestSmartRepliesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse()
        )
        await client.suggest_smart_replies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_suggest_smart_replies_flattened():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestSmartRepliesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.suggest_smart_replies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_suggest_smart_replies_flattened_error():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.suggest_smart_replies(
            participant.SuggestSmartRepliesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_smart_replies_flattened_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.SuggestSmartRepliesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.suggest_smart_replies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_suggest_smart_replies_flattened_error_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.suggest_smart_replies(
            participant.SuggestSmartRepliesRequest(), parent="parent_value",
        )


def test_list_suggestions(
    transport: str = "grpc", request_type=participant.ListSuggestionsRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.ListSuggestionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_suggestions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListSuggestionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSuggestionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_suggestions_from_dict():
    test_list_suggestions(request_type=dict)


def test_list_suggestions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        client.list_suggestions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListSuggestionsRequest()


@pytest.mark.asyncio
async def test_list_suggestions_async(
    transport: str = "grpc_asyncio", request_type=participant.ListSuggestionsRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListSuggestionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_suggestions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListSuggestionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSuggestionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_suggestions_async_from_dict():
    await test_list_suggestions_async(request_type=dict)


def test_list_suggestions_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.ListSuggestionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        call.return_value = participant.ListSuggestionsResponse()
        client.list_suggestions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_suggestions_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.ListSuggestionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListSuggestionsResponse()
        )
        await client.list_suggestions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_suggestions_pager():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListSuggestionsResponse(
                suggestions=[
                    participant.Suggestion(),
                    participant.Suggestion(),
                    participant.Suggestion(),
                ],
                next_page_token="abc",
            ),
            participant.ListSuggestionsResponse(suggestions=[], next_page_token="def",),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(),], next_page_token="ghi",
            ),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(), participant.Suggestion(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_suggestions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, participant.Suggestion) for i in results)


def test_list_suggestions_pages():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_suggestions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListSuggestionsResponse(
                suggestions=[
                    participant.Suggestion(),
                    participant.Suggestion(),
                    participant.Suggestion(),
                ],
                next_page_token="abc",
            ),
            participant.ListSuggestionsResponse(suggestions=[], next_page_token="def",),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(),], next_page_token="ghi",
            ),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(), participant.Suggestion(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_suggestions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_suggestions_async_pager():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_suggestions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListSuggestionsResponse(
                suggestions=[
                    participant.Suggestion(),
                    participant.Suggestion(),
                    participant.Suggestion(),
                ],
                next_page_token="abc",
            ),
            participant.ListSuggestionsResponse(suggestions=[], next_page_token="def",),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(),], next_page_token="ghi",
            ),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(), participant.Suggestion(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_suggestions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, participant.Suggestion) for i in responses)


@pytest.mark.asyncio
async def test_list_suggestions_async_pages():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_suggestions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            participant.ListSuggestionsResponse(
                suggestions=[
                    participant.Suggestion(),
                    participant.Suggestion(),
                    participant.Suggestion(),
                ],
                next_page_token="abc",
            ),
            participant.ListSuggestionsResponse(suggestions=[], next_page_token="def",),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(),], next_page_token="ghi",
            ),
            participant.ListSuggestionsResponse(
                suggestions=[participant.Suggestion(), participant.Suggestion(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_suggestions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_compile_suggestion(
    transport: str = "grpc", request_type=participant.CompileSuggestionRequest
):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compile_suggestion), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = participant.CompileSuggestionResponse(
            latest_message="latest_message_value", context_size=1311,
        )
        response = client.compile_suggestion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.CompileSuggestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.CompileSuggestionResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_compile_suggestion_from_dict():
    test_compile_suggestion(request_type=dict)


def test_compile_suggestion_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compile_suggestion), "__call__"
    ) as call:
        client.compile_suggestion()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.CompileSuggestionRequest()


@pytest.mark.asyncio
async def test_compile_suggestion_async(
    transport: str = "grpc_asyncio", request_type=participant.CompileSuggestionRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compile_suggestion), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.CompileSuggestionResponse(
                latest_message="latest_message_value", context_size=1311,
            )
        )
        response = await client.compile_suggestion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.CompileSuggestionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, participant.CompileSuggestionResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_compile_suggestion_async_from_dict():
    await test_compile_suggestion_async(request_type=dict)


def test_compile_suggestion_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.CompileSuggestionRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compile_suggestion), "__call__"
    ) as call:
        call.return_value = participant.CompileSuggestionResponse()
        client.compile_suggestion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_compile_suggestion_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = participant.CompileSuggestionRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compile_suggestion), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.CompileSuggestionResponse()
        )
        await client.compile_suggestion(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ParticipantsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ParticipantsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
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
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.ParticipantsGrpcTransport,)


def test_participants_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ParticipantsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_participants_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.participants.transports.ParticipantsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ParticipantsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_participant",
        "get_participant",
        "list_participants",
        "update_participant",
        "analyze_content",
        "suggest_articles",
        "suggest_faq_answers",
        "suggest_smart_replies",
        "list_suggestions",
        "compile_suggestion",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_participants_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.participants.transports.ParticipantsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ParticipantsTransport(
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
def test_participants_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.participants.transports.ParticipantsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ParticipantsTransport(
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


def test_participants_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.participants.transports.ParticipantsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ParticipantsTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_participants_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ParticipantsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_participants_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ParticipantsClient()
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
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_participants_transport_auth_adc(transport_class):
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
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_participants_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.ParticipantsGrpcTransport, grpc_helpers),
        (transports.ParticipantsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_participants_transport_create_channel(transport_class, grpc_helpers):
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
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_participants_host_no_port():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_participants_host_with_port():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_participants_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ParticipantsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_participants_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ParticipantsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_transport_channel_mtls_with_adc(transport_class):
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


def test_context_path():
    project = "squid"
    session = "clam"
    context = "whelk"
    expected = "projects/{project}/agent/sessions/{session}/contexts/{context}".format(
        project=project, session=session, context=context,
    )
    actual = ParticipantsClient.context_path(project, session, context)
    assert expected == actual


def test_parse_context_path():
    expected = {
        "project": "octopus",
        "session": "oyster",
        "context": "nudibranch",
    }
    path = ParticipantsClient.context_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_context_path(path)
    assert expected == actual


def test_document_path():
    project = "cuttlefish"
    knowledge_base = "mussel"
    document = "winkle"
    expected = "projects/{project}/knowledgeBases/{knowledge_base}/documents/{document}".format(
        project=project, knowledge_base=knowledge_base, document=document,
    )
    actual = ParticipantsClient.document_path(project, knowledge_base, document)
    assert expected == actual


def test_parse_document_path():
    expected = {
        "project": "nautilus",
        "knowledge_base": "scallop",
        "document": "abalone",
    }
    path = ParticipantsClient.document_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_document_path(path)
    assert expected == actual


def test_intent_path():
    project = "squid"
    intent = "clam"
    expected = "projects/{project}/agent/intents/{intent}".format(
        project=project, intent=intent,
    )
    actual = ParticipantsClient.intent_path(project, intent)
    assert expected == actual


def test_parse_intent_path():
    expected = {
        "project": "whelk",
        "intent": "octopus",
    }
    path = ParticipantsClient.intent_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_intent_path(path)
    assert expected == actual


def test_message_path():
    project = "oyster"
    conversation = "nudibranch"
    message = "cuttlefish"
    expected = "projects/{project}/conversations/{conversation}/messages/{message}".format(
        project=project, conversation=conversation, message=message,
    )
    actual = ParticipantsClient.message_path(project, conversation, message)
    assert expected == actual


def test_parse_message_path():
    expected = {
        "project": "mussel",
        "conversation": "winkle",
        "message": "nautilus",
    }
    path = ParticipantsClient.message_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_message_path(path)
    assert expected == actual


def test_participant_path():
    project = "scallop"
    conversation = "abalone"
    participant = "squid"
    expected = "projects/{project}/conversations/{conversation}/participants/{participant}".format(
        project=project, conversation=conversation, participant=participant,
    )
    actual = ParticipantsClient.participant_path(project, conversation, participant)
    assert expected == actual


def test_parse_participant_path():
    expected = {
        "project": "clam",
        "conversation": "whelk",
        "participant": "octopus",
    }
    path = ParticipantsClient.participant_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_participant_path(path)
    assert expected == actual


def test_session_entity_type_path():
    project = "oyster"
    session = "nudibranch"
    entity_type = "cuttlefish"
    expected = "projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}".format(
        project=project, session=session, entity_type=entity_type,
    )
    actual = ParticipantsClient.session_entity_type_path(project, session, entity_type)
    assert expected == actual


def test_parse_session_entity_type_path():
    expected = {
        "project": "mussel",
        "session": "winkle",
        "entity_type": "nautilus",
    }
    path = ParticipantsClient.session_entity_type_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_session_entity_type_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ParticipantsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = ParticipantsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(folder=folder,)
    actual = ParticipantsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = ParticipantsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = ParticipantsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = ParticipantsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(project=project,)
    actual = ParticipantsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = ParticipantsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ParticipantsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = ParticipantsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ParticipantsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ParticipantsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ParticipantsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ParticipantsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
