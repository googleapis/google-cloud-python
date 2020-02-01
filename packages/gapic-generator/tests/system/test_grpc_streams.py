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

from google import showcase


def test_unary_stream(echo):
    content = 'The hail in Wales falls mainly on the snails.'
    responses = echo.expand({
        'content': content,
    })

    # Consume the response and ensure it matches what we expect.
    # with pytest.raises(exceptions.NotFound) as exc:
    for ground_truth, response in zip(content.split(' '), responses):
        assert response.content == ground_truth
    assert ground_truth == 'snails.'

    # TODO. Check responses.trailing_metadata() content once gapic-showcase
    # server returns non-empty trailing metadata.
    assert len(responses.trailing_metadata()) == 0


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
    responses = echo.chat(iter(requests))

    contents = []
    for response in responses:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    # TODO. Check responses.trailing_metadata() content once gapic-showcase
    # server returns non-empty trailing metadata.
    assert len(responses.trailing_metadata()) == 0


def test_stream_stream_passing_dict(echo):
    requests = [{'content': 'hello'}, {'content': 'world!'}]
    responses = echo.chat(iter(requests))

    contents = []
    for response in responses:
        contents.append(response.content)
    assert contents == ['hello', 'world!']

    # TODO. Check responses.trailing_metadata() content once gapic-showcase
    # server returns non-empty trailing metadata.
    assert len(responses.trailing_metadata()) == 0
