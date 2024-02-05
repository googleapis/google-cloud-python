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

import os
import pytest

from google.api_core import exceptions
from google.rpc import code_pb2

from google import showcase


def test_unary_with_request_object(echo):
    response = echo.echo(showcase.EchoRequest(
        content='The hail in Wales falls mainly on the snails.',
    ))
    assert response.content == 'The hail in Wales falls mainly on the snails.'


def test_unary_with_dict(echo):
    response = echo.echo({
        'content': 'The hail in Wales falls mainly on the snails.',
    })
    assert response.content == 'The hail in Wales falls mainly on the snails.'


def test_unary_error(echo):
    message = 'Bad things! Bad things!'
    # Note: InvalidArgument is from gRPC, InternalServerError from http
    with pytest.raises(exceptions.BadRequest) as exc:
        echo.echo({
            'error': {
                'code': code_pb2.Code.Value('INVALID_ARGUMENT'),
                'message': message,
            },
        })
        assert exc.value.code == 400
        assert exc.value.message == message

    if isinstance(echo.transport, type(echo).get_transport_class("grpc")):
        # Under gRPC, we raise exceptions.InvalidArgument, which is a
        # sub-class of exceptions.BadRequest.
        with pytest.raises(exceptions.InvalidArgument) as exc:
            echo.echo({
                'error': {
                    'code': code_pb2.Code.Value('INVALID_ARGUMENT'),
                    'message': message,
                },
            })
            assert exc.value.code == 400
            assert exc.value.message == message


if os.environ.get("GAPIC_PYTHON_ASYNC", "true") == "true":
    import asyncio

    @pytest.mark.asyncio
    async def test_async_unary_with_request_object(async_echo):
        response = await async_echo.echo(showcase.EchoRequest(
            content='The hail in Wales falls mainly on the snails.',
        ), timeout=1)
        assert response.content == 'The hail in Wales falls mainly on the snails.'

    @pytest.mark.asyncio
    async def test_async_unary_with_dict(async_echo):
        response = await async_echo.echo({
            'content': 'The hail in Wales falls mainly on the snails.',
        })
        assert response.content == 'The hail in Wales falls mainly on the snails.'

    @pytest.mark.asyncio
    async def test_async_unary_error(async_echo):
        message = 'Bad things! Bad things!'
        with pytest.raises(exceptions.InvalidArgument) as exc:
            await async_echo.echo({
                'error': {
                    'code': code_pb2.Code.Value('INVALID_ARGUMENT'),
                    'message': message,
                },
            })
            assert exc.value.code == 400
            assert exc.value.message == message
