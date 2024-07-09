# Copyright 2024 Google LLC All rights reserved.
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

import pytest


def _make_async_stream_generator(iterable):
    from google.cloud.firestore_v1.async_stream_generator import AsyncStreamGenerator

    async def _inner_generator():
        for i in iterable:
            X = yield i
            if X:
                yield X

    return AsyncStreamGenerator(_inner_generator())


@pytest.mark.asyncio
async def test_async_stream_generator_aiter():
    expected_results = [0, 1, 2]
    inst = _make_async_stream_generator(expected_results)

    actual_results = []
    async for result in inst:
        actual_results.append(result)

    assert expected_results == actual_results


@pytest.mark.asyncio
async def test_async_stream_generator_anext():
    expected_results = [0, 1]
    inst = _make_async_stream_generator(expected_results)

    actual_results = []

    # Use inst.__anext__() instead of anext(inst), because built-in anext()
    # was introduced in Python 3.10.
    actual_results.append(await inst.__anext__())
    actual_results.append(await inst.__anext__())

    with pytest.raises(StopAsyncIteration):
        await inst.__anext__()

    assert expected_results == actual_results


@pytest.mark.asyncio
async def test_async_stream_generator_asend():
    expected_results = [0, 1]
    inst = _make_async_stream_generator(expected_results)

    actual_results = []

    # Use inst.__anext__() instead of anext(inst), because built-in anext()
    # was introduced in Python 3.10.
    actual_results.append(await inst.__anext__())
    assert await inst.asend(2) == 2
    actual_results.append(await inst.__anext__())

    with pytest.raises(StopAsyncIteration):
        await inst.__anext__()

    assert expected_results == actual_results


@pytest.mark.asyncio
async def test_async_stream_generator_athrow():
    inst = _make_async_stream_generator([])
    with pytest.raises(ValueError):
        await inst.athrow(ValueError)


@pytest.mark.asyncio
async def test_stream_generator_aclose():
    expected_results = [0, 1]
    inst = _make_async_stream_generator(expected_results)

    await inst.aclose()

    # Verifies that generator is closed.
    with pytest.raises(StopAsyncIteration):
        await inst.__anext__()
