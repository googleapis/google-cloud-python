# -*- coding: utf-8 -*-
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
#
"""Tests for the compatibility module for older versions of google-api-core."""
<<<<<<< HEAD


import re
import pytest

from google.cloud.asset_v1._compat import setup_request_id

class MockRequest:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __contains__(self, key):
        return hasattr(self, key)


class MockProtoRequest:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def HasField(self, key):
        return hasattr(self, key)


class MockValueErrorRequest:
    def HasField(self, key):
        raise ValueError("Mismatched field")

    def __contains__(self, key):
        return hasattr(self, key)

UUID_REGEX = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

@pytest.mark.parametrize(
    "request_obj, is_proto3_optional, expected",
    [
        (MockRequest(), True, "uuid"),
        (MockRequest(request_id="already_set"), True, "already_set"),
        (MockRequest(request_id=""), False, "uuid"),
        (MockRequest(request_id="already_set"), False, "already_set"),
        (MockProtoRequest(), True, "uuid"),
        (MockProtoRequest(request_id="already_set"), True, "already_set"),
        (MockValueErrorRequest(), True, "uuid"),
        ({}, True, "uuid"),
        ({"request_id": None}, True, "uuid"),
        ({"request_id": "already_set"}, True, "already_set"),
        ({"request_id": ""}, False, "uuid"),
        ({"request_id": None}, False, "uuid"),
        ({"request_id": "already_set"}, False, "already_set"),
        (None, True, "none"),
    ],
    ids=[
        "proto3_optional_not_in_request",
        "proto3_optional_already_in_request",
        "non_proto3_optional_empty",
        "non_proto3_optional_already_set",
        "proto3_optional_not_in_request_proto",
        "proto3_optional_already_in_request_proto",
        "value_error_fallback",
        "dict_proto3_optional_not_in_request",
        "dict_proto3_optional_value_none",
        "dict_proto3_optional_already_in_request",
        "dict_non_proto3_optional_empty",
        "dict_non_proto3_optional_value_none",
        "dict_non_proto3_optional_already_set",
        "none_request",
    ],
)
def test_setup_request_id(request_obj, is_proto3_optional, expected):
    setup_request_id(request_obj, "request_id", is_proto3_optional)

    if expected == "none":
        assert request_obj is None
        return

    value = (
        request_obj["request_id"]
        if isinstance(request_obj, dict)
        else request_obj.request_id
    )

    if expected == "uuid":
        assert re.match(UUID_REGEX, value)
    else:
        assert value == expected
=======
>>>>>>> main
