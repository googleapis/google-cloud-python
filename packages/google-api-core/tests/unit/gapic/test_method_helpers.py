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

import re
from google.api_core.gapic_v1.method_helpers import setup_request_id


def test_setup_request_id():
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

    # Test with proto3 optional field not in request
    request = MockRequest()
    setup_request_id(request, "request_id", True)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request.request_id,
    )

    # Test with proto3 optional field already in request
    request = MockRequest(request_id="already_set")
    setup_request_id(request, "request_id", True)
    assert request.request_id == "already_set"

    # Test with non-proto3 optional field empty
    request = MockRequest(request_id="")
    setup_request_id(request, "request_id", False)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request.request_id,
    )

    # Test with non-proto3 optional field already set
    request = MockRequest(request_id="already_set")
    setup_request_id(request, "request_id", False)
    assert request.request_id == "already_set"

    # Test with proto3 optional field not in request (MockProtoRequest)
    request = MockProtoRequest()
    setup_request_id(request, "request_id", True)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request.request_id,
    )

    # Test with proto3 optional field already in request (MockProtoRequest)
    request = MockProtoRequest(request_id="already_set")
    setup_request_id(request, "request_id", True)
    assert request.request_id == "already_set"

    # Test with ValueError
    class MockValueErrorRequest:
        def HasField(self, key):
            raise ValueError("Mismatched field")

        def __contains__(self, key):
            return hasattr(self, key)

    request = MockValueErrorRequest()
    setup_request_id(request, "request_id", True)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request.request_id,
    )

    # Test with dict and proto3 optional field not in request
    request = {}
    setup_request_id(request, "request_id", True)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request["request_id"],
    )

    # Test with dict and proto3 optional field already in request
    request = {"request_id": "already_set"}
    setup_request_id(request, "request_id", True)
    assert request["request_id"] == "already_set"

    # Test with dict and non-proto3 optional field empty
    request = {"request_id": ""}
    setup_request_id(request, "request_id", False)
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        request["request_id"],
    )

    # Test with dict and non-proto3 optional field already set
    request = {"request_id": "already_set"}
    setup_request_id(request, "request_id", False)
    assert request["request_id"] == "already_set"

    # Test with None request (should handle gracefully without raising exception)
    setup_request_id(None, "request_id", True)
