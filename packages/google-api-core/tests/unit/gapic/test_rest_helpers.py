# Copyright 2026 Google LLC
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

import json

from google.protobuf import descriptor_pb2

from google.api_core.gapic_v1.rest_helpers import transcode


def test_transcode_basic():
    # We use FieldDescriptorProto as it has standard primitive fields and nested messages.
    http_options = [
        {
            "method": "get",
            "uri": "/v1/test/{name}",
        }
    ]

    request = descriptor_pb2.FieldDescriptorProto()
    request.name = "my-field"
    request.number = 123

    transcoded, body, query_params = transcode(http_options, request)

    assert transcoded["method"] == "get"
    assert transcoded["uri"] == "/v1/test/my-field"
    assert body is None
    # 'number' should be in query parameters
    assert "number" in query_params
    assert query_params["number"] == 123


def test_transcode_with_nested_field():
    http_options = [
        {
            "method": "get",
            "uri": "/v1/test/{options.deprecated}/{name}",
        }
    ]

    request = descriptor_pb2.FieldDescriptorProto()
    request.name = "my-field"
    request.options.deprecated = True
    request.number = 123

    transcoded, body, query_params = transcode(http_options, request)

    assert transcoded["method"] == "get"
    assert transcoded["uri"] == "/v1/test/True/my-field"
    assert body is None
    assert "number" in query_params
    assert query_params["number"] == 123


def test_transcode_with_body():
    http_options = [
        {
            "method": "post",
            "uri": "/v1/test/{name}",
            "body": "options",
        }
    ]

    request = descriptor_pb2.FieldDescriptorProto()
    request.name = "my-field"
    request.options.deprecated = True
    request.number = 123

    transcoded, body, query_params = transcode(http_options, request)

    assert transcoded["method"] == "post"
    assert transcoded["uri"] == "/v1/test/my-field"
    assert body is not None
    body_data = json.loads(body)
    assert body_data["deprecated"] is True
    # Query parameters should not contain 'options' (the body)
    assert "number" in query_params
    assert query_params["number"] == 123
    assert "options" not in query_params


def test_transcode_with_required_fields_default_values():
    http_options = [
        {
            "method": "get",
            "uri": "/v1/test/{name}",
        }
    ]

    request = descriptor_pb2.FieldDescriptorProto()
    request.name = "my-field"

    required_defaults = {"requiredQueryParam": "default-val"}

    transcoded, body, query_params = transcode(
        http_options,
        request,
        required_fields_default_values=required_defaults,
    )

    assert query_params["requiredQueryParam"] == "default-val"


def test_transcode_with_numeric_enums():
    http_options = [
        {
            "method": "get",
            "uri": "/v1/test/{name}",
        }
    ]

    request = descriptor_pb2.FieldDescriptorProto()
    request.name = "my-field"
    request.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    # Without numeric enums
    _, _, query_params = transcode(http_options, request, rest_numeric_enums=False)
    assert query_params["type"] == "TYPE_STRING"

    # With numeric enums
    _, _, query_params = transcode(http_options, request, rest_numeric_enums=True)
    # Type number for TYPE_STRING is 9
    assert query_params["type"] == 9
    assert query_params["$alt"] == "json;enum-encoding=int"
