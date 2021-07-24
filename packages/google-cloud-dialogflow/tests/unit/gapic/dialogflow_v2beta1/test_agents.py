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
from google.cloud.dialogflow_v2beta1.services.agents import AgentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.agents import AgentsClient
from google.cloud.dialogflow_v2beta1.services.agents import pagers
from google.cloud.dialogflow_v2beta1.services.agents import transports
from google.cloud.dialogflow_v2beta1.services.agents.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.dialogflow_v2beta1.types import agent
from google.cloud.dialogflow_v2beta1.types import agent as gcd_agent
from google.cloud.dialogflow_v2beta1.types import validation_result
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
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

    assert AgentsClient._get_default_mtls_endpoint(None) is None
    assert AgentsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        AgentsClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        AgentsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AgentsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert AgentsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [AgentsClient, AgentsAsyncClient,])
def test_agents_client_from_service_account_info(client_class):
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
        (transports.AgentsGrpcTransport, "grpc"),
        (transports.AgentsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_agents_client_service_account_always_use_jwt(transport_class, transport_name):
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


@pytest.mark.parametrize("client_class", [AgentsClient, AgentsAsyncClient,])
def test_agents_client_from_service_account_file(client_class):
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


def test_agents_client_get_transport_class():
    transport = AgentsClient.get_transport_class()
    available_transports = [
        transports.AgentsGrpcTransport,
    ]
    assert transport in available_transports

    transport = AgentsClient.get_transport_class("grpc")
    assert transport == transports.AgentsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AgentsClient, transports.AgentsGrpcTransport, "grpc"),
        (AgentsAsyncClient, transports.AgentsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    AgentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AgentsClient)
)
@mock.patch.object(
    AgentsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AgentsAsyncClient)
)
def test_agents_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AgentsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AgentsClient, "get_transport_class") as gtc:
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
        (AgentsClient, transports.AgentsGrpcTransport, "grpc", "true"),
        (
            AgentsAsyncClient,
            transports.AgentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (AgentsClient, transports.AgentsGrpcTransport, "grpc", "false"),
        (
            AgentsAsyncClient,
            transports.AgentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AgentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AgentsClient)
)
@mock.patch.object(
    AgentsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AgentsAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_agents_client_mtls_env_auto(
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
        (AgentsClient, transports.AgentsGrpcTransport, "grpc"),
        (AgentsAsyncClient, transports.AgentsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_agents_client_client_options_scopes(
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
        (AgentsClient, transports.AgentsGrpcTransport, "grpc"),
        (AgentsAsyncClient, transports.AgentsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_agents_client_client_options_credentials_file(
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


def test_agents_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.agents.transports.AgentsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AgentsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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


def test_get_agent(transport: str = "grpc", request_type=agent.GetAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.Agent(
            parent="parent_value",
            display_name="display_name_value",
            default_language_code="default_language_code_value",
            supported_language_codes=["supported_language_codes_value"],
            time_zone="time_zone_value",
            description="description_value",
            avatar_uri="avatar_uri_value",
            enable_logging=True,
            match_mode=agent.Agent.MatchMode.MATCH_MODE_HYBRID,
            classification_threshold=0.2552,
            api_version=agent.Agent.ApiVersion.API_VERSION_V1,
            tier=agent.Agent.Tier.TIER_STANDARD,
        )
        response = client.get_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, agent.Agent)
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.default_language_code == "default_language_code_value"
    assert response.supported_language_codes == ["supported_language_codes_value"]
    assert response.time_zone == "time_zone_value"
    assert response.description == "description_value"
    assert response.avatar_uri == "avatar_uri_value"
    assert response.enable_logging is True
    assert response.match_mode == agent.Agent.MatchMode.MATCH_MODE_HYBRID
    assert math.isclose(response.classification_threshold, 0.2552, rel_tol=1e-6)
    assert response.api_version == agent.Agent.ApiVersion.API_VERSION_V1
    assert response.tier == agent.Agent.Tier.TIER_STANDARD


def test_get_agent_from_dict():
    test_get_agent(request_type=dict)


def test_get_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        client.get_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetAgentRequest()


@pytest.mark.asyncio
async def test_get_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.GetAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            agent.Agent(
                parent="parent_value",
                display_name="display_name_value",
                default_language_code="default_language_code_value",
                supported_language_codes=["supported_language_codes_value"],
                time_zone="time_zone_value",
                description="description_value",
                avatar_uri="avatar_uri_value",
                enable_logging=True,
                match_mode=agent.Agent.MatchMode.MATCH_MODE_HYBRID,
                classification_threshold=0.2552,
                api_version=agent.Agent.ApiVersion.API_VERSION_V1,
                tier=agent.Agent.Tier.TIER_STANDARD,
            )
        )
        response = await client.get_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, agent.Agent)
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.default_language_code == "default_language_code_value"
    assert response.supported_language_codes == ["supported_language_codes_value"]
    assert response.time_zone == "time_zone_value"
    assert response.description == "description_value"
    assert response.avatar_uri == "avatar_uri_value"
    assert response.enable_logging is True
    assert response.match_mode == agent.Agent.MatchMode.MATCH_MODE_HYBRID
    assert math.isclose(response.classification_threshold, 0.2552, rel_tol=1e-6)
    assert response.api_version == agent.Agent.ApiVersion.API_VERSION_V1
    assert response.tier == agent.Agent.Tier.TIER_STANDARD


@pytest.mark.asyncio
async def test_get_agent_async_from_dict():
    await test_get_agent_async(request_type=dict)


def test_get_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.GetAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        call.return_value = agent.Agent()
        client.get_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.GetAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(agent.Agent())
        await client.get_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_get_agent_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.Agent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_get_agent_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_agent(
            agent.GetAgentRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_get_agent_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.Agent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(agent.Agent())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_get_agent_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_agent(
            agent.GetAgentRequest(), parent="parent_value",
        )


def test_set_agent(transport: str = "grpc", request_type=gcd_agent.SetAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_agent.Agent(
            parent="parent_value",
            display_name="display_name_value",
            default_language_code="default_language_code_value",
            supported_language_codes=["supported_language_codes_value"],
            time_zone="time_zone_value",
            description="description_value",
            avatar_uri="avatar_uri_value",
            enable_logging=True,
            match_mode=gcd_agent.Agent.MatchMode.MATCH_MODE_HYBRID,
            classification_threshold=0.2552,
            api_version=gcd_agent.Agent.ApiVersion.API_VERSION_V1,
            tier=gcd_agent.Agent.Tier.TIER_STANDARD,
        )
        response = client.set_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_agent.SetAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_agent.Agent)
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.default_language_code == "default_language_code_value"
    assert response.supported_language_codes == ["supported_language_codes_value"]
    assert response.time_zone == "time_zone_value"
    assert response.description == "description_value"
    assert response.avatar_uri == "avatar_uri_value"
    assert response.enable_logging is True
    assert response.match_mode == gcd_agent.Agent.MatchMode.MATCH_MODE_HYBRID
    assert math.isclose(response.classification_threshold, 0.2552, rel_tol=1e-6)
    assert response.api_version == gcd_agent.Agent.ApiVersion.API_VERSION_V1
    assert response.tier == gcd_agent.Agent.Tier.TIER_STANDARD


def test_set_agent_from_dict():
    test_set_agent(request_type=dict)


def test_set_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        client.set_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_agent.SetAgentRequest()


@pytest.mark.asyncio
async def test_set_agent_async(
    transport: str = "grpc_asyncio", request_type=gcd_agent.SetAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_agent.Agent(
                parent="parent_value",
                display_name="display_name_value",
                default_language_code="default_language_code_value",
                supported_language_codes=["supported_language_codes_value"],
                time_zone="time_zone_value",
                description="description_value",
                avatar_uri="avatar_uri_value",
                enable_logging=True,
                match_mode=gcd_agent.Agent.MatchMode.MATCH_MODE_HYBRID,
                classification_threshold=0.2552,
                api_version=gcd_agent.Agent.ApiVersion.API_VERSION_V1,
                tier=gcd_agent.Agent.Tier.TIER_STANDARD,
            )
        )
        response = await client.set_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_agent.SetAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcd_agent.Agent)
    assert response.parent == "parent_value"
    assert response.display_name == "display_name_value"
    assert response.default_language_code == "default_language_code_value"
    assert response.supported_language_codes == ["supported_language_codes_value"]
    assert response.time_zone == "time_zone_value"
    assert response.description == "description_value"
    assert response.avatar_uri == "avatar_uri_value"
    assert response.enable_logging is True
    assert response.match_mode == gcd_agent.Agent.MatchMode.MATCH_MODE_HYBRID
    assert math.isclose(response.classification_threshold, 0.2552, rel_tol=1e-6)
    assert response.api_version == gcd_agent.Agent.ApiVersion.API_VERSION_V1
    assert response.tier == gcd_agent.Agent.Tier.TIER_STANDARD


@pytest.mark.asyncio
async def test_set_agent_async_from_dict():
    await test_set_agent_async(request_type=dict)


def test_set_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_agent.SetAgentRequest()

    request.agent.parent = "agent.parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        call.return_value = gcd_agent.Agent()
        client.set_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "agent.parent=agent.parent/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_set_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcd_agent.SetAgentRequest()

    request.agent.parent = "agent.parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcd_agent.Agent())
        await client.set_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "agent.parent=agent.parent/value",) in kw[
        "metadata"
    ]


def test_set_agent_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_agent.Agent()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_agent(agent=gcd_agent.Agent(parent="parent_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].agent == gcd_agent.Agent(parent="parent_value")


def test_set_agent_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_agent(
            gcd_agent.SetAgentRequest(), agent=gcd_agent.Agent(parent="parent_value"),
        )


@pytest.mark.asyncio
async def test_set_agent_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcd_agent.Agent()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcd_agent.Agent())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_agent(agent=gcd_agent.Agent(parent="parent_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].agent == gcd_agent.Agent(parent="parent_value")


@pytest.mark.asyncio
async def test_set_agent_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_agent(
            gcd_agent.SetAgentRequest(), agent=gcd_agent.Agent(parent="parent_value"),
        )


def test_delete_agent(transport: str = "grpc", request_type=agent.DeleteAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.DeleteAgentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_agent_from_dict():
    test_delete_agent(request_type=dict)


def test_delete_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        client.delete_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.DeleteAgentRequest()


@pytest.mark.asyncio
async def test_delete_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.DeleteAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.DeleteAgentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_agent_async_from_dict():
    await test_delete_agent_async(request_type=dict)


def test_delete_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.DeleteAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        call.return_value = None
        client.delete_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.DeleteAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_delete_agent_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_delete_agent_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_agent(
            agent.DeleteAgentRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_delete_agent_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_delete_agent_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_agent(
            agent.DeleteAgentRequest(), parent="parent_value",
        )


def test_search_agents(transport: str = "grpc", request_type=agent.SearchAgentsRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.SearchAgentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_agents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.SearchAgentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAgentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_agents_from_dict():
    test_search_agents(request_type=dict)


def test_search_agents_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        client.search_agents()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.SearchAgentsRequest()


@pytest.mark.asyncio
async def test_search_agents_async(
    transport: str = "grpc_asyncio", request_type=agent.SearchAgentsRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            agent.SearchAgentsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.search_agents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.SearchAgentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchAgentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_agents_async_from_dict():
    await test_search_agents_async(request_type=dict)


def test_search_agents_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.SearchAgentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        call.return_value = agent.SearchAgentsResponse()
        client.search_agents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_agents_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.SearchAgentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            agent.SearchAgentsResponse()
        )
        await client.search_agents(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_search_agents_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.SearchAgentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_agents(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_search_agents_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_agents(
            agent.SearchAgentsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_search_agents_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = agent.SearchAgentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            agent.SearchAgentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_agents(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_search_agents_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_agents(
            agent.SearchAgentsRequest(), parent="parent_value",
        )


def test_search_agents_pager():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            agent.SearchAgentsResponse(
                agents=[agent.Agent(), agent.Agent(), agent.Agent(),],
                next_page_token="abc",
            ),
            agent.SearchAgentsResponse(agents=[], next_page_token="def",),
            agent.SearchAgentsResponse(agents=[agent.Agent(),], next_page_token="ghi",),
            agent.SearchAgentsResponse(agents=[agent.Agent(), agent.Agent(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_agents(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, agent.Agent) for i in results)


def test_search_agents_pages():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_agents), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            agent.SearchAgentsResponse(
                agents=[agent.Agent(), agent.Agent(), agent.Agent(),],
                next_page_token="abc",
            ),
            agent.SearchAgentsResponse(agents=[], next_page_token="def",),
            agent.SearchAgentsResponse(agents=[agent.Agent(),], next_page_token="ghi",),
            agent.SearchAgentsResponse(agents=[agent.Agent(), agent.Agent(),],),
            RuntimeError,
        )
        pages = list(client.search_agents(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_agents_async_pager():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_agents), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            agent.SearchAgentsResponse(
                agents=[agent.Agent(), agent.Agent(), agent.Agent(),],
                next_page_token="abc",
            ),
            agent.SearchAgentsResponse(agents=[], next_page_token="def",),
            agent.SearchAgentsResponse(agents=[agent.Agent(),], next_page_token="ghi",),
            agent.SearchAgentsResponse(agents=[agent.Agent(), agent.Agent(),],),
            RuntimeError,
        )
        async_pager = await client.search_agents(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, agent.Agent) for i in responses)


@pytest.mark.asyncio
async def test_search_agents_async_pages():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_agents), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            agent.SearchAgentsResponse(
                agents=[agent.Agent(), agent.Agent(), agent.Agent(),],
                next_page_token="abc",
            ),
            agent.SearchAgentsResponse(agents=[], next_page_token="def",),
            agent.SearchAgentsResponse(agents=[agent.Agent(),], next_page_token="ghi",),
            agent.SearchAgentsResponse(agents=[agent.Agent(), agent.Agent(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.search_agents(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_train_agent(transport: str = "grpc", request_type=agent.TrainAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.train_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.TrainAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_train_agent_from_dict():
    test_train_agent(request_type=dict)


def test_train_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        client.train_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.TrainAgentRequest()


@pytest.mark.asyncio
async def test_train_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.TrainAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.train_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.TrainAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_train_agent_async_from_dict():
    await test_train_agent_async(request_type=dict)


def test_train_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.TrainAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.train_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_train_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.TrainAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.train_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_train_agent_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.train_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_train_agent_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.train_agent(
            agent.TrainAgentRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_train_agent_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.train_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.train_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_train_agent_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.train_agent(
            agent.TrainAgentRequest(), parent="parent_value",
        )


def test_export_agent(transport: str = "grpc", request_type=agent.ExportAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ExportAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_agent_from_dict():
    test_export_agent(request_type=dict)


def test_export_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        client.export_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ExportAgentRequest()


@pytest.mark.asyncio
async def test_export_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.ExportAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ExportAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_agent_async_from_dict():
    await test_export_agent_async(request_type=dict)


def test_export_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.ExportAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.ExportAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_export_agent_flattened():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_export_agent_flattened_error():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_agent(
            agent.ExportAgentRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_export_agent_flattened_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_agent(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_export_agent_flattened_error_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_agent(
            agent.ExportAgentRequest(), parent="parent_value",
        )


def test_import_agent(transport: str = "grpc", request_type=agent.ImportAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ImportAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_agent_from_dict():
    test_import_agent(request_type=dict)


def test_import_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_agent), "__call__") as call:
        client.import_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ImportAgentRequest()


@pytest.mark.asyncio
async def test_import_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.ImportAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.ImportAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_agent_async_from_dict():
    await test_import_agent_async(request_type=dict)


def test_import_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.ImportAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_agent), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.ImportAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_restore_agent(transport: str = "grpc", request_type=agent.RestoreAgentRequest):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restore_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.RestoreAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restore_agent_from_dict():
    test_restore_agent(request_type=dict)


def test_restore_agent_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_agent), "__call__") as call:
        client.restore_agent()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.RestoreAgentRequest()


@pytest.mark.asyncio
async def test_restore_agent_async(
    transport: str = "grpc_asyncio", request_type=agent.RestoreAgentRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_agent), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restore_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.RestoreAgentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restore_agent_async_from_dict():
    await test_restore_agent_async(request_type=dict)


def test_restore_agent_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.RestoreAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_agent), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_restore_agent_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.RestoreAgentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_agent), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restore_agent(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_get_validation_result(
    transport: str = "grpc", request_type=agent.GetValidationResultRequest
):
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_validation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = validation_result.ValidationResult()
        response = client.get_validation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetValidationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, validation_result.ValidationResult)


def test_get_validation_result_from_dict():
    test_get_validation_result(request_type=dict)


def test_get_validation_result_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_validation_result), "__call__"
    ) as call:
        client.get_validation_result()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetValidationResultRequest()


@pytest.mark.asyncio
async def test_get_validation_result_async(
    transport: str = "grpc_asyncio", request_type=agent.GetValidationResultRequest
):
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_validation_result), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            validation_result.ValidationResult()
        )
        response = await client.get_validation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == agent.GetValidationResultRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, validation_result.ValidationResult)


@pytest.mark.asyncio
async def test_get_validation_result_async_from_dict():
    await test_get_validation_result_async(request_type=dict)


def test_get_validation_result_field_headers():
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.GetValidationResultRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_validation_result), "__call__"
    ) as call:
        call.return_value = validation_result.ValidationResult()
        client.get_validation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_validation_result_field_headers_async():
    client = AgentsAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = agent.GetValidationResultRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_validation_result), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            validation_result.ValidationResult()
        )
        await client.get_validation_result(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AgentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AgentsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AgentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AgentsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AgentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AgentsClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AgentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AgentsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AgentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AgentsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AgentsClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.AgentsGrpcTransport,)


def test_agents_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AgentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_agents_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.services.agents.transports.AgentsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AgentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_agent",
        "set_agent",
        "delete_agent",
        "search_agents",
        "train_agent",
        "export_agent",
        "import_agent",
        "restore_agent",
        "get_validation_result",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_agents_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.agents.transports.AgentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AgentsTransport(
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
def test_agents_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.agents.transports.AgentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AgentsTransport(
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


def test_agents_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflow_v2beta1.services.agents.transports.AgentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AgentsTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_agents_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AgentsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_agents_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AgentsClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
def test_agents_transport_auth_adc(transport_class):
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
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_agents_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.AgentsGrpcTransport, grpc_helpers),
        (transports.AgentsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_agents_transport_create_channel(transport_class, grpc_helpers):
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
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport],
)
def test_agents_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_agents_host_no_port():
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:443"


def test_agents_host_with_port():
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dialogflow.googleapis.com:8000"


def test_agents_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AgentsGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_agents_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AgentsGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport],
)
def test_agents_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.AgentsGrpcTransport, transports.AgentsGrpcAsyncIOTransport],
)
def test_agents_transport_channel_mtls_with_adc(transport_class):
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


def test_agents_grpc_lro_client():
    client = AgentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_agents_grpc_lro_async_client():
    client = AgentsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_agent_path():
    project = "squid"
    expected = "projects/{project}/agent".format(project=project,)
    actual = AgentsClient.agent_path(project)
    assert expected == actual


def test_parse_agent_path():
    expected = {
        "project": "clam",
    }
    path = AgentsClient.agent_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_agent_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AgentsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = AgentsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = AgentsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = AgentsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = AgentsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = AgentsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = AgentsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = AgentsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AgentsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = AgentsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AgentsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AgentsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AgentsClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AgentsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AgentsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
