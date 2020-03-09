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
from google.api_core import client_options
from google.auth import credentials
from google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry import (
    PredictionApiKeyRegistryClient,
)
from google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry import (
    pagers,
)
from google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry import (
    transports,
)
from google.cloud.recommendationengine_v1beta1.types import (
    prediction_apikey_registry_service,
)
from google.oauth2 import service_account


def test_prediction_api_key_registry_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = PredictionApiKeyRegistryClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = PredictionApiKeyRegistryClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_prediction_api_key_registry_client_client_options():
    # Check the default options have their expected values.
    assert (
        PredictionApiKeyRegistryClient.DEFAULT_OPTIONS.api_endpoint
        == "recommendationengine.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry.PredictionApiKeyRegistryClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = PredictionApiKeyRegistryClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_prediction_api_key_registry_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry.PredictionApiKeyRegistryClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = PredictionApiKeyRegistryClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_create_prediction_api_key_registration(transport: str = "grpc"):
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = (
        prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_prediction_api_key_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = prediction_apikey_registry_service.PredictionApiKeyRegistration(
            api_key="api_key_value"
        )

        response = client.create_prediction_api_key_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, prediction_apikey_registry_service.PredictionApiKeyRegistration
    )
    assert response.api_key == "api_key_value"


def test_list_prediction_api_key_registrations(transport: str = "grpc"):
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = (
        prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_prediction_api_key_registrations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_prediction_api_key_registrations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPredictionApiKeyRegistrationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_prediction_api_key_registrations_field_headers():
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest(
        parent="parent/value"
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_prediction_api_key_registrations), "__call__"
    ) as call:
        call.return_value = (
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse()
        )
        client.list_prediction_api_key_registrations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_prediction_api_key_registrations_pager():
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_prediction_api_key_registrations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                ],
                next_page_token="abc",
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[], next_page_token="def"
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration()
                ],
                next_page_token="ghi",
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_prediction_api_key_registrations(request={})]
        assert len(results) == 6
        assert all(
            isinstance(
                i, prediction_apikey_registry_service.PredictionApiKeyRegistration
            )
            for i in results
        )


def test_list_prediction_api_key_registrations_pages():
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_prediction_api_key_registrations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                ],
                next_page_token="abc",
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[], next_page_token="def"
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration()
                ],
                next_page_token="ghi",
            ),
            prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsResponse(
                prediction_api_key_registrations=[
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                    prediction_apikey_registry_service.PredictionApiKeyRegistration(),
                ]
            ),
            RuntimeError,
        )
        pages = list(client.list_prediction_api_key_registrations(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_prediction_api_key_registration(transport: str = "grpc"):
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = (
        prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_prediction_api_key_registration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_prediction_api_key_registration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PredictionApiKeyRegistryGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = PredictionApiKeyRegistryClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PredictionApiKeyRegistryGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = PredictionApiKeyRegistryClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials()
    )
    assert isinstance(
        client._transport, transports.PredictionApiKeyRegistryGrpcTransport
    )


def test_prediction_api_key_registry_base_transport():
    # Instantiate the base transport.
    transport = transports.PredictionApiKeyRegistryTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_prediction_api_key_registration",
        "list_prediction_api_key_registrations",
        "delete_prediction_api_key_registration",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_prediction_api_key_registry_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        PredictionApiKeyRegistryClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_prediction_api_key_registry_host_no_port():
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_prediction_api_key_registry_host_with_port():
    client = PredictionApiKeyRegistryClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:8000"


def test_prediction_api_key_registry_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.PredictionApiKeyRegistryGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
