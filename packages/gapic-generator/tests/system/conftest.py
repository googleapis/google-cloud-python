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
import pytest

from google.showcase import EchoClient
from google.showcase import IdentityClient

import grpc


@pytest.fixture
def echo():
    transport = EchoClient.get_transport_class('grpc')(
        channel=grpc.insecure_channel('localhost:7469'),
    )
    return EchoClient(transport=transport)


@pytest.fixture
def identity():
    transport = IdentityClient.get_transport_class('grpc')(
        channel=grpc.insecure_channel('localhost:7469'),
    )
    return IdentityClient(transport=transport)


class MetadataClientInterceptor(grpc.UnaryUnaryClientInterceptor,
                                grpc.UnaryStreamClientInterceptor,
                                grpc.StreamUnaryClientInterceptor,
                                grpc.StreamStreamClientInterceptor):

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def _add_metadata(self, client_call_details):
        if client_call_details.metadata is not None:
            client_call_details.metadata.append((self._key, self._value,))

    def intercept_unary_unary(self, continuation, client_call_details, request):
        self._add_metadata(client_call_details)
        response = continuation(client_call_details, request)
        return response

    def intercept_unary_stream(self, continuation, client_call_details,
                               request):
        self._add_metadata(client_call_details)
        response_it = continuation(client_call_details, request)
        return response_it

    def intercept_stream_unary(self, continuation, client_call_details,
                               request_iterator):
        self._add_metadata(client_call_details)
        response = continuation(client_call_details, request_iterator)
        return response

    def intercept_stream_stream(self, continuation, client_call_details,
                                request_iterator):
        self._add_metadata(client_call_details)
        response_it = continuation(client_call_details, request_iterator)
        return response_it


@pytest.fixture
def intercepted_echo():
    # The interceptor adds 'showcase-trailer' client metadata. Showcase server
    # echos any metadata with key 'showcase-trailer', so the same metadata
    # should appear as trailing metadata in the response.
    interceptor = MetadataClientInterceptor('showcase-trailer', 'intercepted')
    channel = grpc.insecure_channel('localhost:7469')
    intercept_channel = grpc.intercept_channel(channel, interceptor)
    transport = EchoClient.get_transport_class('grpc')(
        channel=intercept_channel,
    )
    return EchoClient(transport=transport)
