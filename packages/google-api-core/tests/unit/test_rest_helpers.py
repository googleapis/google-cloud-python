# Copyright 2021 Google LLC
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
import pytest
from google.protobuf import descriptor_pb2

from google.api_core import rest_helpers
from google.api_core.rest_helpers import transcode, RestTransportInterceptor


def test_flatten_simple_value():
    with pytest.raises(TypeError):
        rest_helpers.flatten_query_params("abc")


def test_flatten_list():
    with pytest.raises(TypeError):
        rest_helpers.flatten_query_params(["abc", "def"])


def test_flatten_none():
    assert rest_helpers.flatten_query_params(None) == []


def test_flatten_empty_dict():
    assert rest_helpers.flatten_query_params({}) == []


def test_flatten_simple_dict():
    obj = {"a": "abc", "b": "def", "c": True, "d": False, "e": 10, "f": -3.76}
    assert rest_helpers.flatten_query_params(obj) == [
        ("a", "abc"),
        ("b", "def"),
        ("c", True),
        ("d", False),
        ("e", 10),
        ("f", -3.76),
    ]


def test_flatten_simple_dict_strict():
    obj = {"a": "abc", "b": "def", "c": True, "d": False, "e": 10, "f": -3.76}
    assert rest_helpers.flatten_query_params(obj, strict=True) == [
        ("a", "abc"),
        ("b", "def"),
        ("c", "true"),
        ("d", "false"),
        ("e", "10"),
        ("f", "-3.76"),
    ]


def test_flatten_repeated_field():
    assert rest_helpers.flatten_query_params({"a": ["x", "y", "z", None]}) == [
        ("a", "x"),
        ("a", "y"),
        ("a", "z"),
    ]


def test_flatten_nested_dict():
    obj = {"a": {"b": {"c": ["x", "y", "z"]}}, "d": {"e": "uvw"}}
    expected_result = [("a.b.c", "x"), ("a.b.c", "y"), ("a.b.c", "z"), ("d.e", "uvw")]

    assert rest_helpers.flatten_query_params(obj) == expected_result


def test_flatten_repeated_dict():
    obj = {
        "a": {"b": {"c": [{"v": 1}, {"v": 2}]}},
        "d": "uvw",
    }

    with pytest.raises(ValueError):
        rest_helpers.flatten_query_params(obj)


def test_flatten_repeated_list():
    obj = {
        "a": {"b": {"c": [["e", "f"], ["g", "h"]]}},
        "d": "uvw",
    }

    with pytest.raises(ValueError):
        rest_helpers.flatten_query_params(obj)


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


def test_rest_transport_interceptor():
    import pytest

    interceptor = RestTransportInterceptor()

    # pre_ hook
    req, metadata = interceptor.pre_some_rpc("my-request", [("key", "val")])
    assert req == "my-request"
    assert metadata == [("key", "val")]

    # post_ hook
    res = interceptor.post_some_rpc("my-response")
    assert res == "my-response"

    # post_ with metadata hook
    res, metadata = interceptor.post_some_rpc_with_metadata("my-response", [("key", "val")])
    assert res == "my-response"
    assert metadata == [("key", "val")]

    # Non-hook lookup raises AttributeError
    with pytest.raises(AttributeError) as excinfo:
        getattr(interceptor, "some_other_method")
    assert "object has no attribute 'some_other_method'" in str(excinfo.value)
