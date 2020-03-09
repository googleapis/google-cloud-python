# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api import httpbody_pb2 as httpbody  # type: ignore
from google.api_core import client_options
from google.api_core import future
from google.api_core import operations_v1
from google.auth import credentials
from google.cloud.recommendationengine_v1beta1.services.user_event_service import (
    UserEventServiceClient,
)
from google.cloud.recommendationengine_v1beta1.services.user_event_service import pagers
from google.cloud.recommendationengine_v1beta1.services.user_event_service import (
    transports,
)
from google.cloud.recommendationengine_v1beta1.types import import_
from google.cloud.recommendationengine_v1beta1.types import user_event
from google.cloud.recommendationengine_v1beta1.types import user_event_service
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2 as any  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def test_user_event_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = UserEventServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = UserEventServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_user_event_service_client_client_options():
    # Check the default options have their expected values.
    assert (
        UserEventServiceClient.DEFAULT_OPTIONS.api_endpoint
        == "recommendationengine.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.user_event_service.UserEventServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = UserEventServiceClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_user_event_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.user_event_service.UserEventServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = UserEventServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_write_user_event(transport: str = "grpc"):
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = user_event_service.WriteUserEventRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.write_user_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_event.UserEvent(
            event_type="event_type_value",
            event_source=user_event.UserEvent.EventSource.AUTOML,
        )

        response = client.write_user_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, user_event.UserEvent)
    assert response.event_type == "event_type_value"
    assert response.event_source == user_event.UserEvent.EventSource.AUTOML


def test_collect_user_event(transport: str = "grpc"):
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = user_event_service.CollectUserEventRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.collect_user_event), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = httpbody.HttpBody(
            content_type="content_type_value", data=b"data_blob"
        )

        response = client.collect_user_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, httpbody.HttpBody)
    assert response.content_type == "content_type_value"
    assert response.data == b"data_blob"


def test_collect_user_event_field_headers():
    client = UserEventServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = user_event_service.CollectUserEventRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.collect_user_event), "__call__"
    ) as call:
        call.return_value = httpbody.HttpBody()
        client.collect_user_event(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_user_events(transport: str = "grpc"):
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = user_event_service.ListUserEventsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_user_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = user_event_service.ListUserEventsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_user_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUserEventsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_user_events_field_headers():
    client = UserEventServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = user_event_service.ListUserEventsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_user_events), "__call__"
    ) as call:
        call.return_value = user_event_service.ListUserEventsResponse()
        client.list_user_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_user_events_pager():
    client = UserEventServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_user_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            user_event_service.ListUserEventsResponse(
                user_events=[
                    user_event.UserEvent(),
                    user_event.UserEvent(),
                    user_event.UserEvent(),
                ],
                next_page_token="abc",
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[], next_page_token="def"
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[user_event.UserEvent()], next_page_token="ghi"
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[user_event.UserEvent(), user_event.UserEvent()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_user_events(request={})]
        assert len(results) == 6
        assert all(isinstance(i, user_event.UserEvent) for i in results)


def test_list_user_events_pages():
    client = UserEventServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_user_events), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            user_event_service.ListUserEventsResponse(
                user_events=[
                    user_event.UserEvent(),
                    user_event.UserEvent(),
                    user_event.UserEvent(),
                ],
                next_page_token="abc",
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[], next_page_token="def"
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[user_event.UserEvent()], next_page_token="ghi"
            ),
            user_event_service.ListUserEventsResponse(
                user_events=[user_event.UserEvent(), user_event.UserEvent()]
            ),
            RuntimeError,
        )
        pages = list(client.list_user_events(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_purge_user_events(transport: str = "grpc"):
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = user_event_service.PurgeUserEventsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.purge_user_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.purge_user_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_user_events(transport: str = "grpc"):
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = import_.ImportUserEventsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_user_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.import_user_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.UserEventServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = UserEventServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UserEventServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = UserEventServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = UserEventServiceClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.UserEventServiceGrpcTransport)


def test_user_event_service_base_transport():
    # Instantiate the base transport.
    transport = transports.UserEventServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "write_user_event",
        "collect_user_event",
        "list_user_events",
        "purge_user_events",
        "import_user_events",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_user_event_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        UserEventServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_user_event_service_host_no_port():
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_user_event_service_host_with_port():
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:8000"


def test_user_event_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.UserEventServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_user_event_service_grpc_lro_client():
    client = UserEventServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
