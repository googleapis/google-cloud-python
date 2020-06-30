# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import mock
import os
import pytest
import asyncio

import google.api_core.client_options as ClientOptions
from google.auth import credentials
from google.showcase import EchoClient, EchoAsyncClient
from google.showcase import IdentityClient, IdentityAsyncClient
from google.showcase import MessagingClient

import grpc
from grpc.experimental import aio

_test_event_loop = asyncio.new_event_loop()

# NOTE(lidiz) We must override the default event_loop fixture from
# pytest-asyncio. pytest fixture frees resources once there isn't any reference
# to it. So, the event loop might close before tests finishes. In the
# customized version, we don't close the event loop.


@pytest.fixture
def event_loop():
    asyncio.set_event_loop(_test_event_loop)
    return asyncio.get_event_loop()


dir = os.path.dirname(__file__)
with open(os.path.join(dir, "../cert/mtls.crt"), "rb") as fh:
    cert = fh.read()
with open(os.path.join(dir, "../cert/mtls.key"), "rb") as fh:
    key = fh.read()

ssl_credentials = grpc.ssl_channel_credentials(
    root_certificates=cert, certificate_chain=cert, private_key=key
)


def callback():
    return cert, key


client_options = ClientOptions.ClientOptions()
client_options.client_cert_source = callback


def pytest_addoption(parser):
    parser.addoption(
        "--mtls", action="store_true", help="Run system test with mutual TLS channel"
    )


def construct_client(client_class,
                     use_mtls,
                     transport="grpc",
                     channel_creator=grpc.insecure_channel):
    if use_mtls:
        with mock.patch("grpc.ssl_channel_credentials", autospec=True) as mock_ssl_cred:
            mock_ssl_cred.return_value = ssl_credentials
            client = client_class(
                credentials=credentials.AnonymousCredentials(),
                client_options=client_options,
            )
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=cert, private_key=key
            )
            return client
    else:
        transport = client_class.get_transport_class(transport)(
            channel=channel_creator("localhost:7469")
        )
        return client_class(transport=transport)


@pytest.fixture
def use_mtls(request):
    return request.config.getoption("--mtls")


@pytest.fixture
def echo(use_mtls):
    return construct_client(EchoClient, use_mtls)


@pytest.fixture
def async_echo(use_mtls, event_loop):
    return construct_client(
        EchoAsyncClient,
        use_mtls,
        transport="grpc_asyncio",
        channel_creator=aio.insecure_channel
    )


@pytest.fixture
def identity():
    transport = IdentityClient.get_transport_class('grpc')(
        channel=grpc.insecure_channel('localhost:7469'),
    )
    return IdentityClient(transport=transport)


@pytest.fixture
def async_identity(use_mtls, event_loop):
    return construct_client(
        IdentityAsyncClient,
        use_mtls,
        transport="grpc_asyncio",
        channel_creator=aio.insecure_channel
    )


@pytest.fixture
def identity(use_mtls):
    return construct_client(IdentityClient, use_mtls)


@pytest.fixture
def messaging(use_mtls):
    return construct_client(MessagingClient, use_mtls)


class MetadataClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def _add_metadata(self, client_call_details):
        if client_call_details.metadata is not None:
            client_call_details.metadata.append((self._key, self._value))

    def intercept_unary_unary(self, continuation, client_call_details, request):
        self._add_metadata(client_call_details)
        response = continuation(client_call_details, request)
        return response

    def intercept_unary_stream(self, continuation, client_call_details, request):
        self._add_metadata(client_call_details)
        response_it = continuation(client_call_details, request)
        return response_it

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        self._add_metadata(client_call_details)
        response = continuation(client_call_details, request_iterator)
        return response

    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        self._add_metadata(client_call_details)
        response_it = continuation(client_call_details, request_iterator)
        return response_it


@pytest.fixture
def intercepted_echo(use_mtls):
    # The interceptor adds 'showcase-trailer' client metadata. Showcase server
    # echos any metadata with key 'showcase-trailer', so the same metadata
    # should appear as trailing metadata in the response.
    interceptor = MetadataClientInterceptor("showcase-trailer", "intercepted")
    host = "localhost:7469"
    channel = (
        grpc.secure_channel(host, ssl_credentials)
        if use_mtls
        else grpc.insecure_channel(host)
    )
    intercept_channel = grpc.intercept_channel(channel, interceptor)
    transport = EchoClient.get_transport_class("grpc")(
        channel=intercept_channel
    )
    return EchoClient(transport=transport)
