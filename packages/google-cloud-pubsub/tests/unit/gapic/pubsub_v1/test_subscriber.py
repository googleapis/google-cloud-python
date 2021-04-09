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
import warnings

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
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.pubsub_v1.services.subscriber import SubscriberAsyncClient
from google.pubsub_v1.services.subscriber import SubscriberClient
from google.pubsub_v1.services.subscriber import pagers
from google.pubsub_v1.services.subscriber import transports
from google.pubsub_v1.types import pubsub


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

    assert SubscriberClient._get_default_mtls_endpoint(None) is None
    assert (
        SubscriberClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        SubscriberClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SubscriberClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SubscriberClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert SubscriberClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [SubscriberClient, SubscriberAsyncClient,])
def test_subscriber_client_from_service_account_info(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "pubsub.googleapis.com:443"


@pytest.mark.parametrize("client_class", [SubscriberClient, SubscriberAsyncClient,])
def test_subscriber_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
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

        assert client.transport._host == "pubsub.googleapis.com:443"


def test_subscriber_client_get_transport_class():
    transport = SubscriberClient.get_transport_class()
    available_transports = [
        transports.SubscriberGrpcTransport,
    ]
    assert transport in available_transports

    transport = SubscriberClient.get_transport_class("grpc")
    assert transport == transports.SubscriberGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SubscriberClient, transports.SubscriberGrpcTransport, "grpc"),
        (
            SubscriberAsyncClient,
            transports.SubscriberGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    SubscriberClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SubscriberClient)
)
@mock.patch.object(
    SubscriberAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SubscriberAsyncClient),
)
def test_subscriber_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SubscriberClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SubscriberClient, "get_transport_class") as gtc:
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
        (SubscriberClient, transports.SubscriberGrpcTransport, "grpc", "true"),
        (
            SubscriberAsyncClient,
            transports.SubscriberGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SubscriberClient, transports.SubscriberGrpcTransport, "grpc", "false"),
        (
            SubscriberAsyncClient,
            transports.SubscriberGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    SubscriberClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SubscriberClient)
)
@mock.patch.object(
    SubscriberAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SubscriberAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_subscriber_client_mtls_env_auto(
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
        (SubscriberClient, transports.SubscriberGrpcTransport, "grpc"),
        (
            SubscriberAsyncClient,
            transports.SubscriberGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_subscriber_client_client_options_scopes(
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
        (SubscriberClient, transports.SubscriberGrpcTransport, "grpc"),
        (
            SubscriberAsyncClient,
            transports.SubscriberGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_subscriber_client_client_options_credentials_file(
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


def test_subscriber_client_client_options_from_dict():
    with mock.patch(
        "google.pubsub_v1.services.subscriber.transports.SubscriberGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SubscriberClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_subscription(transport: str = "grpc", request_type=pubsub.Subscription):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name="name_value",
            topic="topic_value",
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter="filter_value",
            detached=True,
        )

        response = client.create_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.Subscription()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


def test_create_subscription_from_dict():
    test_create_subscription(request_type=dict)


def test_create_subscription_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        client.create_subscription()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.Subscription()


@pytest.mark.asyncio
async def test_create_subscription_async(
    transport: str = "grpc_asyncio", request_type=pubsub.Subscription
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Subscription(
                name="name_value",
                topic="topic_value",
                ack_deadline_seconds=2066,
                retain_acked_messages=True,
                enable_message_ordering=True,
                filter="filter_value",
                detached=True,
            )
        )

        response = await client.create_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.Subscription()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


@pytest.mark.asyncio
async def test_create_subscription_async_from_dict():
    await test_create_subscription_async(request_type=dict)


def test_create_subscription_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.Subscription()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        call.return_value = pubsub.Subscription()

        client.create_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_subscription_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.Subscription()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Subscription())

        await client.create_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_subscription_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_subscription(
            name="name_value",
            topic="topic_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].topic == "topic_value"

        assert args[0].push_config == pubsub.PushConfig(
            push_endpoint="push_endpoint_value"
        )

        assert args[0].ack_deadline_seconds == 2066


def test_create_subscription_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_subscription(
            pubsub.Subscription(),
            name="name_value",
            topic="topic_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
            ack_deadline_seconds=2066,
        )


@pytest.mark.asyncio
async def test_create_subscription_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Subscription())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_subscription(
            name="name_value",
            topic="topic_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].topic == "topic_value"

        assert args[0].push_config == pubsub.PushConfig(
            push_endpoint="push_endpoint_value"
        )

        assert args[0].ack_deadline_seconds == 2066


@pytest.mark.asyncio
async def test_create_subscription_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_subscription(
            pubsub.Subscription(),
            name="name_value",
            topic="topic_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
            ack_deadline_seconds=2066,
        )


def test_get_subscription(
    transport: str = "grpc", request_type=pubsub.GetSubscriptionRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name="name_value",
            topic="topic_value",
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter="filter_value",
            detached=True,
        )

        response = client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSubscriptionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


def test_get_subscription_from_dict():
    test_get_subscription(request_type=dict)


def test_get_subscription_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        client.get_subscription()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSubscriptionRequest()


@pytest.mark.asyncio
async def test_get_subscription_async(
    transport: str = "grpc_asyncio", request_type=pubsub.GetSubscriptionRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Subscription(
                name="name_value",
                topic="topic_value",
                ack_deadline_seconds=2066,
                retain_acked_messages=True,
                enable_message_ordering=True,
                filter="filter_value",
                detached=True,
            )
        )

        response = await client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSubscriptionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


@pytest.mark.asyncio
async def test_get_subscription_async_from_dict():
    await test_get_subscription_async(request_type=dict)


def test_get_subscription_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        call.return_value = pubsub.Subscription()

        client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_get_subscription_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Subscription())

        await client.get_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_get_subscription_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_subscription(subscription="subscription_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"


def test_get_subscription_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_subscription(
            pubsub.GetSubscriptionRequest(), subscription="subscription_value",
        )


@pytest.mark.asyncio
async def test_get_subscription_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_subscription), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Subscription())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_subscription(subscription="subscription_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"


@pytest.mark.asyncio
async def test_get_subscription_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_subscription(
            pubsub.GetSubscriptionRequest(), subscription="subscription_value",
        )


def test_update_subscription(
    transport: str = "grpc", request_type=pubsub.UpdateSubscriptionRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Subscription(
            name="name_value",
            topic="topic_value",
            ack_deadline_seconds=2066,
            retain_acked_messages=True,
            enable_message_ordering=True,
            filter="filter_value",
            detached=True,
        )

        response = client.update_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSubscriptionRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


def test_update_subscription_from_dict():
    test_update_subscription(request_type=dict)


def test_update_subscription_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_subscription), "__call__"
    ) as call:
        client.update_subscription()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSubscriptionRequest()


@pytest.mark.asyncio
async def test_update_subscription_async(
    transport: str = "grpc_asyncio", request_type=pubsub.UpdateSubscriptionRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Subscription(
                name="name_value",
                topic="topic_value",
                ack_deadline_seconds=2066,
                retain_acked_messages=True,
                enable_message_ordering=True,
                filter="filter_value",
                detached=True,
            )
        )

        response = await client.update_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSubscriptionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Subscription)

    assert response.name == "name_value"

    assert response.topic == "topic_value"

    assert response.ack_deadline_seconds == 2066

    assert response.retain_acked_messages is True

    assert response.enable_message_ordering is True

    assert response.filter == "filter_value"

    assert response.detached is True


@pytest.mark.asyncio
async def test_update_subscription_async_from_dict():
    await test_update_subscription_async(request_type=dict)


def test_update_subscription_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateSubscriptionRequest()
    request.subscription.name = "subscription.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_subscription), "__call__"
    ) as call:
        call.return_value = pubsub.Subscription()

        client.update_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "subscription.name=subscription.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_subscription_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateSubscriptionRequest()
    request.subscription.name = "subscription.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_subscription), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Subscription())

        await client.update_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "subscription.name=subscription.name/value",
    ) in kw["metadata"]


def test_list_subscriptions(
    transport: str = "grpc", request_type=pubsub.ListSubscriptionsRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSubscriptionsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSubscriptionsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListSubscriptionsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_subscriptions_from_dict():
    test_list_subscriptions(request_type=dict)


def test_list_subscriptions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        client.list_subscriptions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSubscriptionsRequest()


@pytest.mark.asyncio
async def test_list_subscriptions_async(
    transport: str = "grpc_asyncio", request_type=pubsub.ListSubscriptionsRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSubscriptionsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSubscriptionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSubscriptionsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_subscriptions_async_from_dict():
    await test_list_subscriptions_async(request_type=dict)


def test_list_subscriptions_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSubscriptionsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        call.return_value = pubsub.ListSubscriptionsResponse()

        client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_subscriptions_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSubscriptionsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSubscriptionsResponse()
        )

        await client.list_subscriptions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


def test_list_subscriptions_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSubscriptionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_subscriptions(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


def test_list_subscriptions_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_subscriptions(
            pubsub.ListSubscriptionsRequest(), project="project_value",
        )


@pytest.mark.asyncio
async def test_list_subscriptions_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSubscriptionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSubscriptionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_subscriptions(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


@pytest.mark.asyncio
async def test_list_subscriptions_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_subscriptions(
            pubsub.ListSubscriptionsRequest(), project="project_value",
        )


def test_list_subscriptions_pager():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token="abc",
            ),
            pubsub.ListSubscriptionsResponse(subscriptions=[], next_page_token="def",),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(),], next_page_token="ghi",
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(), pubsub.Subscription(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", ""),)),
        )
        pager = client.list_subscriptions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Subscription) for i in results)


def test_list_subscriptions_pages():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token="abc",
            ),
            pubsub.ListSubscriptionsResponse(subscriptions=[], next_page_token="def",),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(),], next_page_token="ghi",
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(), pubsub.Subscription(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_subscriptions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_subscriptions_async_pager():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token="abc",
            ),
            pubsub.ListSubscriptionsResponse(subscriptions=[], next_page_token="def",),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(),], next_page_token="ghi",
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(), pubsub.Subscription(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_subscriptions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, pubsub.Subscription) for i in responses)


@pytest.mark.asyncio
async def test_list_subscriptions_async_pages():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_subscriptions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSubscriptionsResponse(
                subscriptions=[
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                    pubsub.Subscription(),
                ],
                next_page_token="abc",
            ),
            pubsub.ListSubscriptionsResponse(subscriptions=[], next_page_token="def",),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(),], next_page_token="ghi",
            ),
            pubsub.ListSubscriptionsResponse(
                subscriptions=[pubsub.Subscription(), pubsub.Subscription(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_subscriptions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_subscription(
    transport: str = "grpc", request_type=pubsub.DeleteSubscriptionRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSubscriptionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_subscription_from_dict():
    test_delete_subscription(request_type=dict)


def test_delete_subscription_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        client.delete_subscription()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSubscriptionRequest()


@pytest.mark.asyncio
async def test_delete_subscription_async(
    transport: str = "grpc_asyncio", request_type=pubsub.DeleteSubscriptionRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSubscriptionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_subscription_async_from_dict():
    await test_delete_subscription_async(request_type=dict)


def test_delete_subscription_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        call.return_value = None

        client.delete_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_delete_subscription_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteSubscriptionRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_subscription(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_delete_subscription_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_subscription(subscription="subscription_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"


def test_delete_subscription_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_subscription(
            pubsub.DeleteSubscriptionRequest(), subscription="subscription_value",
        )


@pytest.mark.asyncio
async def test_delete_subscription_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_subscription), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_subscription(subscription="subscription_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"


@pytest.mark.asyncio
async def test_delete_subscription_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_subscription(
            pubsub.DeleteSubscriptionRequest(), subscription="subscription_value",
        )


def test_modify_ack_deadline(
    transport: str = "grpc", request_type=pubsub.ModifyAckDeadlineRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.modify_ack_deadline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyAckDeadlineRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_modify_ack_deadline_from_dict():
    test_modify_ack_deadline(request_type=dict)


def test_modify_ack_deadline_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        client.modify_ack_deadline()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyAckDeadlineRequest()


@pytest.mark.asyncio
async def test_modify_ack_deadline_async(
    transport: str = "grpc_asyncio", request_type=pubsub.ModifyAckDeadlineRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.modify_ack_deadline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyAckDeadlineRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_modify_ack_deadline_async_from_dict():
    await test_modify_ack_deadline_async(request_type=dict)


def test_modify_ack_deadline_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ModifyAckDeadlineRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        call.return_value = None

        client.modify_ack_deadline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_modify_ack_deadline_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ModifyAckDeadlineRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.modify_ack_deadline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_modify_ack_deadline_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.modify_ack_deadline(
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].ack_ids == ["ack_ids_value"]

        assert args[0].ack_deadline_seconds == 2066


def test_modify_ack_deadline_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_ack_deadline(
            pubsub.ModifyAckDeadlineRequest(),
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
            ack_deadline_seconds=2066,
        )


@pytest.mark.asyncio
async def test_modify_ack_deadline_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_ack_deadline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.modify_ack_deadline(
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
            ack_deadline_seconds=2066,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].ack_ids == ["ack_ids_value"]

        assert args[0].ack_deadline_seconds == 2066


@pytest.mark.asyncio
async def test_modify_ack_deadline_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.modify_ack_deadline(
            pubsub.ModifyAckDeadlineRequest(),
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
            ack_deadline_seconds=2066,
        )


def test_acknowledge(transport: str = "grpc", request_type=pubsub.AcknowledgeRequest):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.acknowledge(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.AcknowledgeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_acknowledge_from_dict():
    test_acknowledge(request_type=dict)


def test_acknowledge_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        client.acknowledge()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.AcknowledgeRequest()


@pytest.mark.asyncio
async def test_acknowledge_async(
    transport: str = "grpc_asyncio", request_type=pubsub.AcknowledgeRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.acknowledge(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.AcknowledgeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_acknowledge_async_from_dict():
    await test_acknowledge_async(request_type=dict)


def test_acknowledge_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.AcknowledgeRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        call.return_value = None

        client.acknowledge(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_acknowledge_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.AcknowledgeRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.acknowledge(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_acknowledge_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.acknowledge(
            subscription="subscription_value", ack_ids=["ack_ids_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].ack_ids == ["ack_ids_value"]


def test_acknowledge_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.acknowledge(
            pubsub.AcknowledgeRequest(),
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
        )


@pytest.mark.asyncio
async def test_acknowledge_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.acknowledge), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.acknowledge(
            subscription="subscription_value", ack_ids=["ack_ids_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].ack_ids == ["ack_ids_value"]


@pytest.mark.asyncio
async def test_acknowledge_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.acknowledge(
            pubsub.AcknowledgeRequest(),
            subscription="subscription_value",
            ack_ids=["ack_ids_value"],
        )


def test_pull(transport: str = "grpc", request_type=pubsub.PullRequest):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PullResponse()

        response = client.pull(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.PullRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.PullResponse)


def test_pull_from_dict():
    test_pull(request_type=dict)


def test_pull_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        client.pull()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.PullRequest()


@pytest.mark.asyncio
async def test_pull_async(
    transport: str = "grpc_asyncio", request_type=pubsub.PullRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.PullResponse())

        response = await client.pull(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.PullRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.PullResponse)


@pytest.mark.asyncio
async def test_pull_async_from_dict():
    await test_pull_async(request_type=dict)


def test_pull_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.PullRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        call.return_value = pubsub.PullResponse()

        client.pull(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_pull_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.PullRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.PullResponse())

        await client.pull(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_pull_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PullResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            client.pull(
                subscription="subscription_value",
                return_immediately=True,
                max_messages=1277,
            )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].return_immediately == True

        assert args[0].max_messages == 1277


def test_pull_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pull(
            pubsub.PullRequest(),
            subscription="subscription_value",
            return_immediately=True,
            max_messages=1277,
        )


@pytest.mark.asyncio
async def test_pull_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.PullResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.PullResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            await client.pull(
                subscription="subscription_value",
                return_immediately=True,
                max_messages=1277,
            )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].return_immediately == True

        assert args[0].max_messages == 1277


@pytest.mark.asyncio
async def test_pull_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.pull(
            pubsub.PullRequest(),
            subscription="subscription_value",
            return_immediately=True,
            max_messages=1277,
        )


def test_streaming_pull(
    transport: str = "grpc", request_type=pubsub.StreamingPullRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([pubsub.StreamingPullResponse()])

        response = client.streaming_pull(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, pubsub.StreamingPullResponse)


def test_streaming_pull_from_dict():
    test_streaming_pull(request_type=dict)


@pytest.mark.asyncio
async def test_streaming_pull_async(
    transport: str = "grpc_asyncio", request_type=pubsub.StreamingPullRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.streaming_pull), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[pubsub.StreamingPullResponse()]
        )

        response = await client.streaming_pull(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, pubsub.StreamingPullResponse)


@pytest.mark.asyncio
async def test_streaming_pull_async_from_dict():
    await test_streaming_pull_async(request_type=dict)


def test_modify_push_config(
    transport: str = "grpc", request_type=pubsub.ModifyPushConfigRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.modify_push_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyPushConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_modify_push_config_from_dict():
    test_modify_push_config(request_type=dict)


def test_modify_push_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        client.modify_push_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyPushConfigRequest()


@pytest.mark.asyncio
async def test_modify_push_config_async(
    transport: str = "grpc_asyncio", request_type=pubsub.ModifyPushConfigRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.modify_push_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ModifyPushConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_modify_push_config_async_from_dict():
    await test_modify_push_config_async(request_type=dict)


def test_modify_push_config_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ModifyPushConfigRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        call.return_value = None

        client.modify_push_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_modify_push_config_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ModifyPushConfigRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.modify_push_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_modify_push_config_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.modify_push_config(
            subscription="subscription_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].push_config == pubsub.PushConfig(
            push_endpoint="push_endpoint_value"
        )


def test_modify_push_config_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_push_config(
            pubsub.ModifyPushConfigRequest(),
            subscription="subscription_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
        )


@pytest.mark.asyncio
async def test_modify_push_config_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_push_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.modify_push_config(
            subscription="subscription_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].subscription == "subscription_value"

        assert args[0].push_config == pubsub.PushConfig(
            push_endpoint="push_endpoint_value"
        )


@pytest.mark.asyncio
async def test_modify_push_config_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.modify_push_config(
            pubsub.ModifyPushConfigRequest(),
            subscription="subscription_value",
            push_config=pubsub.PushConfig(push_endpoint="push_endpoint_value"),
        )


def test_get_snapshot(transport: str = "grpc", request_type=pubsub.GetSnapshotRequest):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(name="name_value", topic="topic_value",)

        response = client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSnapshotRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


def test_get_snapshot_from_dict():
    test_get_snapshot(request_type=dict)


def test_get_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        client.get_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSnapshotRequest()


@pytest.mark.asyncio
async def test_get_snapshot_async(
    transport: str = "grpc_asyncio", request_type=pubsub.GetSnapshotRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Snapshot(name="name_value", topic="topic_value",)
        )

        response = await client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.GetSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


@pytest.mark.asyncio
async def test_get_snapshot_async_from_dict():
    await test_get_snapshot_async(request_type=dict)


def test_get_snapshot_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSnapshotRequest()
    request.snapshot = "snapshot/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        call.return_value = pubsub.Snapshot()

        client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot=snapshot/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_snapshot_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.GetSnapshotRequest()
    request.snapshot = "snapshot/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Snapshot())

        await client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot=snapshot/value",) in kw["metadata"]


def test_get_snapshot_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_snapshot(snapshot="snapshot_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].snapshot == "snapshot_value"


def test_get_snapshot_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_snapshot(
            pubsub.GetSnapshotRequest(), snapshot="snapshot_value",
        )


@pytest.mark.asyncio
async def test_get_snapshot_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Snapshot())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_snapshot(snapshot="snapshot_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].snapshot == "snapshot_value"


@pytest.mark.asyncio
async def test_get_snapshot_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_snapshot(
            pubsub.GetSnapshotRequest(), snapshot="snapshot_value",
        )


def test_list_snapshots(
    transport: str = "grpc", request_type=pubsub.ListSnapshotsRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSnapshotsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSnapshotsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListSnapshotsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_snapshots_from_dict():
    test_list_snapshots(request_type=dict)


def test_list_snapshots_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        client.list_snapshots()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSnapshotsRequest()


@pytest.mark.asyncio
async def test_list_snapshots_async(
    transport: str = "grpc_asyncio", request_type=pubsub.ListSnapshotsRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSnapshotsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.ListSnapshotsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSnapshotsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_snapshots_async_from_dict():
    await test_list_snapshots_async(request_type=dict)


def test_list_snapshots_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSnapshotsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        call.return_value = pubsub.ListSnapshotsResponse()

        client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_snapshots_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.ListSnapshotsRequest()
    request.project = "project/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSnapshotsResponse()
        )

        await client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project=project/value",) in kw["metadata"]


def test_list_snapshots_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSnapshotsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_snapshots(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


def test_list_snapshots_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_snapshots(
            pubsub.ListSnapshotsRequest(), project="project_value",
        )


@pytest.mark.asyncio
async def test_list_snapshots_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.ListSnapshotsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.ListSnapshotsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_snapshots(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project == "project_value"


@pytest.mark.asyncio
async def test_list_snapshots_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_snapshots(
            pubsub.ListSnapshotsRequest(), project="project_value",
        )


def test_list_snapshots_pager():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(), pubsub.Snapshot(),],
                next_page_token="abc",
            ),
            pubsub.ListSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(),], next_page_token="ghi",
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", ""),)),
        )
        pager = client.list_snapshots(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, pubsub.Snapshot) for i in results)


def test_list_snapshots_pages():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(), pubsub.Snapshot(),],
                next_page_token="abc",
            ),
            pubsub.ListSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(),], next_page_token="ghi",
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_snapshots(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_snapshots_async_pager():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_snapshots), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(), pubsub.Snapshot(),],
                next_page_token="abc",
            ),
            pubsub.ListSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(),], next_page_token="ghi",
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_snapshots(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, pubsub.Snapshot) for i in responses)


@pytest.mark.asyncio
async def test_list_snapshots_async_pages():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_snapshots), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(), pubsub.Snapshot(),],
                next_page_token="abc",
            ),
            pubsub.ListSnapshotsResponse(snapshots=[], next_page_token="def",),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(),], next_page_token="ghi",
            ),
            pubsub.ListSnapshotsResponse(
                snapshots=[pubsub.Snapshot(), pubsub.Snapshot(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_snapshots(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_snapshot(
    transport: str = "grpc", request_type=pubsub.CreateSnapshotRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(name="name_value", topic="topic_value",)

        response = client.create_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.CreateSnapshotRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


def test_create_snapshot_from_dict():
    test_create_snapshot(request_type=dict)


def test_create_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        client.create_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.CreateSnapshotRequest()


@pytest.mark.asyncio
async def test_create_snapshot_async(
    transport: str = "grpc_asyncio", request_type=pubsub.CreateSnapshotRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Snapshot(name="name_value", topic="topic_value",)
        )

        response = await client.create_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.CreateSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


@pytest.mark.asyncio
async def test_create_snapshot_async_from_dict():
    await test_create_snapshot_async(request_type=dict)


def test_create_snapshot_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.CreateSnapshotRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        call.return_value = pubsub.Snapshot()

        client.create_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_snapshot_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.CreateSnapshotRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Snapshot())

        await client.create_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_snapshot_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_snapshot(
            name="name_value", subscription="subscription_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].subscription == "subscription_value"


def test_create_snapshot_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_snapshot(
            pubsub.CreateSnapshotRequest(),
            name="name_value",
            subscription="subscription_value",
        )


@pytest.mark.asyncio
async def test_create_snapshot_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Snapshot())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_snapshot(
            name="name_value", subscription="subscription_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].subscription == "subscription_value"


@pytest.mark.asyncio
async def test_create_snapshot_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_snapshot(
            pubsub.CreateSnapshotRequest(),
            name="name_value",
            subscription="subscription_value",
        )


def test_update_snapshot(
    transport: str = "grpc", request_type=pubsub.UpdateSnapshotRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.Snapshot(name="name_value", topic="topic_value",)

        response = client.update_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSnapshotRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


def test_update_snapshot_from_dict():
    test_update_snapshot(request_type=dict)


def test_update_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_snapshot), "__call__") as call:
        client.update_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSnapshotRequest()


@pytest.mark.asyncio
async def test_update_snapshot_async(
    transport: str = "grpc_asyncio", request_type=pubsub.UpdateSnapshotRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            pubsub.Snapshot(name="name_value", topic="topic_value",)
        )

        response = await client.update_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.UpdateSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.Snapshot)

    assert response.name == "name_value"

    assert response.topic == "topic_value"


@pytest.mark.asyncio
async def test_update_snapshot_async_from_dict():
    await test_update_snapshot_async(request_type=dict)


def test_update_snapshot_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateSnapshotRequest()
    request.snapshot.name = "snapshot.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_snapshot), "__call__") as call:
        call.return_value = pubsub.Snapshot()

        client.update_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot.name=snapshot.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_snapshot_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.UpdateSnapshotRequest()
    request.snapshot.name = "snapshot.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.Snapshot())

        await client.update_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot.name=snapshot.name/value",) in kw[
        "metadata"
    ]


def test_delete_snapshot(
    transport: str = "grpc", request_type=pubsub.DeleteSnapshotRequest
):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_snapshot_from_dict():
    test_delete_snapshot(request_type=dict)


def test_delete_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        client.delete_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSnapshotRequest()


@pytest.mark.asyncio
async def test_delete_snapshot_async(
    transport: str = "grpc_asyncio", request_type=pubsub.DeleteSnapshotRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.DeleteSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_snapshot_async_from_dict():
    await test_delete_snapshot_async(request_type=dict)


def test_delete_snapshot_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteSnapshotRequest()
    request.snapshot = "snapshot/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        call.return_value = None

        client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot=snapshot/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_snapshot_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.DeleteSnapshotRequest()
    request.snapshot = "snapshot/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "snapshot=snapshot/value",) in kw["metadata"]


def test_delete_snapshot_flattened():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_snapshot(snapshot="snapshot_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].snapshot == "snapshot_value"


def test_delete_snapshot_flattened_error():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_snapshot(
            pubsub.DeleteSnapshotRequest(), snapshot="snapshot_value",
        )


@pytest.mark.asyncio
async def test_delete_snapshot_flattened_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_snapshot(snapshot="snapshot_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].snapshot == "snapshot_value"


@pytest.mark.asyncio
async def test_delete_snapshot_flattened_error_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_snapshot(
            pubsub.DeleteSnapshotRequest(), snapshot="snapshot_value",
        )


def test_seek(transport: str = "grpc", request_type=pubsub.SeekRequest):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.seek), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = pubsub.SeekResponse()

        response = client.seek(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.SeekRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pubsub.SeekResponse)


def test_seek_from_dict():
    test_seek(request_type=dict)


def test_seek_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.seek), "__call__") as call:
        client.seek()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.SeekRequest()


@pytest.mark.asyncio
async def test_seek_async(
    transport: str = "grpc_asyncio", request_type=pubsub.SeekRequest
):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.seek), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.SeekResponse())

        response = await client.seek(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == pubsub.SeekRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pubsub.SeekResponse)


@pytest.mark.asyncio
async def test_seek_async_from_dict():
    await test_seek_async(request_type=dict)


def test_seek_field_headers():
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.SeekRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.seek), "__call__") as call:
        call.return_value = pubsub.SeekResponse()

        client.seek(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_seek_field_headers_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = pubsub.SeekRequest()
    request.subscription = "subscription/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.seek), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(pubsub.SeekResponse())

        await client.seek(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "subscription=subscription/value",) in kw[
        "metadata"
    ]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubscriberClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubscriberClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubscriberClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = SubscriberClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SubscriberGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SubscriberGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.SubscriberGrpcTransport, transports.SubscriberGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.SubscriberGrpcTransport,)


def test_subscriber_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.SubscriberTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_subscriber_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.pubsub_v1.services.subscriber.transports.SubscriberTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SubscriberTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_subscription",
        "get_subscription",
        "update_subscription",
        "list_subscriptions",
        "delete_subscription",
        "modify_ack_deadline",
        "acknowledge",
        "pull",
        "streaming_pull",
        "modify_push_config",
        "get_snapshot",
        "list_snapshots",
        "create_snapshot",
        "update_snapshot",
        "delete_snapshot",
        "seek",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_subscriber_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.pubsub_v1.services.subscriber.transports.SubscriberTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SubscriberTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


def test_subscriber_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.pubsub_v1.services.subscriber.transports.SubscriberTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.SubscriberTransport()
        adc.assert_called_once()


def test_subscriber_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SubscriberClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id=None,
        )


def test_subscriber_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.SubscriberGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.SubscriberGrpcTransport, transports.SubscriberGrpcAsyncIOTransport],
)
def test_subscriber_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = credentials.AnonymousCredentials()

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
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
                ("grpc.keepalive_time_ms", 30000),
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


def test_subscriber_host_no_port():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com"
        ),
    )
    assert client.transport._host == "pubsub.googleapis.com:443"


def test_subscriber_host_with_port():
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "pubsub.googleapis.com:8000"


def test_subscriber_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SubscriberGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_subscriber_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SubscriberGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.SubscriberGrpcTransport, transports.SubscriberGrpcAsyncIOTransport],
)
def test_subscriber_transport_channel_mtls_with_client_cert_source(transport_class):
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

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/pubsub",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 30000),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.SubscriberGrpcTransport, transports.SubscriberGrpcAsyncIOTransport],
)
def test_subscriber_transport_channel_mtls_with_adc(transport_class):
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
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/pubsub",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 30000),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_snapshot_path():
    project = "squid"
    snapshot = "clam"

    expected = "projects/{project}/snapshots/{snapshot}".format(
        project=project, snapshot=snapshot,
    )
    actual = SubscriberClient.snapshot_path(project, snapshot)
    assert expected == actual


def test_parse_snapshot_path():
    expected = {
        "project": "whelk",
        "snapshot": "octopus",
    }
    path = SubscriberClient.snapshot_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_snapshot_path(path)
    assert expected == actual


def test_subscription_path():
    project = "oyster"
    subscription = "nudibranch"

    expected = "projects/{project}/subscriptions/{subscription}".format(
        project=project, subscription=subscription,
    )
    actual = SubscriberClient.subscription_path(project, subscription)
    assert expected == actual


def test_parse_subscription_path():
    expected = {
        "project": "cuttlefish",
        "subscription": "mussel",
    }
    path = SubscriberClient.subscription_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_subscription_path(path)
    assert expected == actual


def test_topic_path():
    project = "winkle"
    topic = "nautilus"

    expected = "projects/{project}/topics/{topic}".format(project=project, topic=topic,)
    actual = SubscriberClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "scallop",
        "topic": "abalone",
    }
    path = SubscriberClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_topic_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SubscriberClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = SubscriberClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"

    expected = "folders/{folder}".format(folder=folder,)
    actual = SubscriberClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = SubscriberClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = SubscriberClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = SubscriberClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"

    expected = "projects/{project}".format(project=project,)
    actual = SubscriberClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = SubscriberClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = SubscriberClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = SubscriberClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SubscriberClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SubscriberTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SubscriberClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SubscriberTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SubscriberClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_set_iam_policy(transport: str = "grpc"):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
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
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
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
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = SubscriberClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = SubscriberAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
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
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
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
    client = SubscriberClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
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


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = SubscriberAsyncClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()
