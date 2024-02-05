# Copyright 2019 Google LLC
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

import os
import pytest

from google.api_core import exceptions
from google.rpc import code_pb2


def test_retry_bubble(echo):
    with pytest.raises(exceptions.GatewayTimeout):
        echo.echo({
            'error': {
                'code': code_pb2.Code.Value('DEADLINE_EXCEEDED'),
                'message': 'This took longer than you said it should.',
            },
        })

    if isinstance(echo.transport, type(echo).get_transport_class("grpc")):
        # Under gRPC, we raise exceptions.DeadlineExceeded, which is a
        # sub-class of exceptions.GatewayTimeout.
        with pytest.raises(exceptions.DeadlineExceeded):
            echo.echo({
                'error': {
                    'code': code_pb2.Code.Value('DEADLINE_EXCEEDED'),
                    'message': 'This took longer than you said it should.',
                },
            })


if os.environ.get("GAPIC_PYTHON_ASYNC", "true") == "true":

    @pytest.mark.asyncio
    async def test_retry_bubble_async(async_echo):
        with pytest.raises(exceptions.DeadlineExceeded):
            await async_echo.echo({
                'error': {
                    'code': code_pb2.Code.Value('DEADLINE_EXCEEDED'),
                    'message': 'This took longer than you said it should.',
                },
            })
