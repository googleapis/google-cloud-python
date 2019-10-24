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
