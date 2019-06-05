# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# flake8: noqa

import os
import pytest

from google.api_core import exceptions
from google.cloud import trace_v1

PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)


class TestVPCServiceControlV1(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        except:
            return False
        return False

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_traces(self):
        client = trace_v1.TraceServiceClient()

        list_inside = lambda: list(client.list_traces(PROJECT_INSIDE))
        list_outside = lambda: list(client.list_traces(PROJECT_OUTSIDE))

        assert not TestVPCServiceControlV1._is_rejected(list_inside)
        assert TestVPCServiceControlV1._is_rejected(list_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_trace(self):
        client = trace_v1.TraceServiceClient()

        get_inside = lambda: client.get_trace(PROJECT_INSIDE, "")
        get_outside = lambda: client.get_trace(PROJECT_OUTSIDE, "")

        assert not TestVPCServiceControlV1._is_rejected(get_inside)
        assert TestVPCServiceControlV1._is_rejected(get_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_patch_traces(self):
        client = trace_v1.TraceServiceClient()

        patch_inside = lambda: client.patch_traces(PROJECT_INSIDE, {})
        patch_outside = lambda: client.patch_traces(PROJECT_OUTSIDE, {})

        assert not TestVPCServiceControlV1._is_rejected(patch_inside)
        assert TestVPCServiceControlV1._is_rejected(patch_outside)
