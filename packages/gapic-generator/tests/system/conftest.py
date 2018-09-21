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

from google.auth.credentials import AnonymousCredentials
from google.showcase import Showcase
from google.showcase_v1alpha1.services.showcase.transports.grpc import (
    ShowcaseGrpcTransport,
)

import grpc


@pytest.fixture
def showcase():
    transport = ShowcaseGrpcTransport(credentials=AnonymousCredentials())
    transport.__dict__['grpc_channel'] = grpc.insecure_channel(
        transport.SERVICE_ADDRESS,
    )
    return Showcase(transport=transport)
