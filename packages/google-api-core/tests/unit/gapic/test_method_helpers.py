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

import pytest

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)
from google.api_core.gapic_v1._method_helpers import setup_request_id


def test_setup_request_id():
    import uuid

    # test dict request
    req = {}
    setup_request_id(req, "request_id", True)
    assert "request_id" in req
    uuid_str = req["request_id"]
    uuid.UUID(uuid_str)  # verify it is a valid UUID

    # test dict request when already set
    req = {"request_id": "existing"}
    setup_request_id(req, "request_id", True)
    assert req["request_id"] == "existing"

    class DummyRequest:
        def __init__(self):
            self.request_id = ""

        def HasField(self, field_name):
            if not hasattr(self, field_name):
                raise ValueError()
            return bool(getattr(self, field_name))

    # test object request proto3 optional true
    req_obj = DummyRequest()
    setup_request_id(req_obj, "request_id", True)
    assert req_obj.request_id != ""
    uuid.UUID(req_obj.request_id)

    # test object request proto3 optional false
    req_obj2 = DummyRequest()
    setup_request_id(req_obj2, "request_id", False)
    assert req_obj2.request_id != ""
    uuid.UUID(req_obj2.request_id)
