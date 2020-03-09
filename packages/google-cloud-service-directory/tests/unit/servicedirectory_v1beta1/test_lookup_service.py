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
from google.cloud.servicedirectory_v1beta1.services.lookup_service import (
    LookupServiceClient,
)
from google.cloud.servicedirectory_v1beta1.services.lookup_service import transports
from google.cloud.servicedirectory_v1beta1.types import lookup_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.oauth2 import service_account


def test_lookup_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = LookupServiceClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = LookupServiceClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "servicedirectory.googleapis.com:443"


def test_lookup_service_client_client_options():
    # Check the default options have their expected values.
    assert (
        LookupServiceClient.DEFAULT_OPTIONS.api_endpoint
        == "servicedirectory.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.lookup_service.LookupServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = LookupServiceClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_lookup_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.lookup_service.LookupServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = LookupServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_resolve_service(transport: str = "grpc"):
    client = LookupServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = lookup_service.ResolveServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.resolve_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lookup_service.ResolveServiceResponse()

        response = client.resolve_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, lookup_service.ResolveServiceResponse)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.LookupServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = LookupServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LookupServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = LookupServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = LookupServiceClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.LookupServiceGrpcTransport)


def test_lookup_service_base_transport():
    # Instantiate the base transport.
    transport = transports.LookupServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = ("resolve_service",)
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_lookup_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        LookupServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_lookup_service_host_no_port():
    client = LookupServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicedirectory.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "servicedirectory.googleapis.com:443"


def test_lookup_service_host_with_port():
    client = LookupServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicedirectory.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "servicedirectory.googleapis.com:8000"


def test_lookup_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.LookupServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
