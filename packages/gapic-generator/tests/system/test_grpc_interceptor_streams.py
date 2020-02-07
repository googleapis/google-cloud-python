# Copyright 2020 Google LLC
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


# intercetped_metadata will be added by the interceptor automatically, and
# showcase server will echo it (since it has key 'showcase-trailer') as trailing
# metadata.
intercepted_metadata = (('showcase-trailer', 'intercepted'),)


def test_unary_stream(intercepted_echo):
    content = 'The hail in Wales falls mainly on the snails.'
    responses = intercepted_echo.expand({
        'content': content,
    })

    for ground_truth, response in zip(content.split(' '), responses):
        assert response.content == ground_truth
    assert ground_truth == 'snails.'

    assert responses.trailing_metadata() == intercepted_metadata


def test_stream_stream(intercepted_echo):
    requests = []
    requests.append(showcase.EchoRequest(content="hello"))
    requests.append(showcase.EchoRequest(content="world!"))
    responses = intercepted_echo.chat(iter(requests))

    contents = [response.content for response in responses]
    assert contents == ['hello', 'world!']

    assert responses.trailing_metadata() == intercepted_metadata
