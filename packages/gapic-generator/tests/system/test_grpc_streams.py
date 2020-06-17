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

import logging
import pytest
import asyncio
import threading
from google import showcase


metadata = (("showcase-trailer", "hello world"),)


def test_unary_stream(echo):
    content = 'The hail in Wales falls mainly on the snails.'
    responses = echo.expand({
        'content': content,
    }, metadata=metadata)

    # Consume the response and ensure it matches what we expect.
    # with pytest.raises(exceptions.NotFound) as exc:
    for ground_truth, response in zip(content.split(' '), responses):
        assert response.content == ground_truth
    assert ground_truth == 'snails.'

    assert responses.trailing_metadata() == metadata


def test_stream_unary(echo):
    requests = []
    requests.append(showcase.EchoRequest(content="hello"))
    requests.append(showcase.EchoRequest(content="world!"))
    response = echo.collect(iter(requests))
    assert response.content == 'hello world!'


def test_stream_unary_passing_dict(echo):
    requests = [{'content': 'hello'}, {'content': 'world!'}]
    response = echo.collect(iter(requests))
    assert response.content == 'hello world!'


def test_stream_stream(echo):
    requests = []
    requests.append(showcase.EchoRequest(content="hello"))
    requests.append(showcase.EchoRequest(content="world!"))
    responses = echo.chat(iter(requests), metadata=metadata)

    contents = []
    for response in responses:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    assert responses.trailing_metadata() == metadata


def test_stream_stream_passing_dict(echo):
    requests = [{'content': 'hello'}, {'content': 'world!'}]
    responses = echo.chat(iter(requests), metadata=metadata)

    contents = []
    for response in responses:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    assert responses.trailing_metadata() == metadata


@pytest.mark.asyncio
async def test_async_unary_stream_reader(async_echo):
    content = 'The hail in Wales falls mainly on the snails.'
    call = await async_echo.expand({
        'content': content,
    }, metadata=metadata)

    # Consume the response and ensure it matches what we expect.
    # with pytest.raises(exceptions.NotFound) as exc:
    for ground_truth in content.split(' '):
        response = await call.read()
        assert response.content == ground_truth
    assert ground_truth == 'snails.'

    trailing_metadata = await call.trailing_metadata()
    assert trailing_metadata == metadata


@pytest.mark.asyncio
async def test_async_unary_stream_async_generator(async_echo):
    content = 'The hail in Wales falls mainly on the snails.'
    call = await async_echo.expand({
        'content': content,
    }, metadata=metadata)

    # Consume the response and ensure it matches what we expect.
    # with pytest.raises(exceptions.NotFound) as exc:
    tokens = iter(content.split(' '))
    async for response in call:
        ground_truth = next(tokens)
        assert response.content == ground_truth
    assert ground_truth == 'snails.'

    trailing_metadata = await call.trailing_metadata()
    assert trailing_metadata == metadata


@pytest.mark.asyncio
async def test_async_stream_unary_iterable(async_echo):
    requests = []
    requests.append(showcase.EchoRequest(content="hello"))
    requests.append(showcase.EchoRequest(content="world!"))

    call = await async_echo.collect(requests)
    response = await call
    assert response.content == 'hello world!'


@pytest.mark.asyncio
async def test_async_stream_unary_async_generator(async_echo):

    async def async_generator():
        yield showcase.EchoRequest(content="hello")
        yield showcase.EchoRequest(content="world!")

    call = await async_echo.collect(async_generator())
    response = await call
    assert response.content == 'hello world!'


@pytest.mark.asyncio
async def test_async_stream_unary_writer(async_echo):
    call = await async_echo.collect()
    await call.write(showcase.EchoRequest(content="hello"))
    await call.write(showcase.EchoRequest(content="world!"))
    await call.done_writing()

    response = await call
    assert response.content == 'hello world!'


@pytest.mark.asyncio
async def test_async_stream_unary_passing_dict(async_echo):
    requests = [{'content': 'hello'}, {'content': 'world!'}]
    call = await async_echo.collect(iter(requests))
    response = await call
    assert response.content == 'hello world!'


@pytest.mark.asyncio
async def test_async_stream_stream_reader_writier(async_echo):
    call = await async_echo.chat(metadata=metadata)
    await call.write(showcase.EchoRequest(content="hello"))
    await call.write(showcase.EchoRequest(content="world!"))
    await call.done_writing()

    contents = [
        (await call.read()).content,
        (await call.read()).content
    ]
    assert contents == ['hello', 'world!']

    trailing_metadata = await call.trailing_metadata()
    assert trailing_metadata == metadata


@pytest.mark.asyncio
async def test_async_stream_stream_async_generator(async_echo):

    async def async_generator():
        yield showcase.EchoRequest(content="hello")
        yield showcase.EchoRequest(content="world!")

    call = await async_echo.chat(async_generator(), metadata=metadata)

    contents = []
    async for response in call:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    trailing_metadata = await call.trailing_metadata()
    assert trailing_metadata == metadata


@pytest.mark.asyncio
async def test_async_stream_stream_passing_dict(async_echo):
    requests = [{'content': 'hello'}, {'content': 'world!'}]
    call = await async_echo.chat(iter(requests), metadata=metadata)

    contents = []
    async for response in call:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    trailing_metadata = await call.trailing_metadata()
    assert trailing_metadata == metadata
