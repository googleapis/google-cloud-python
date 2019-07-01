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
from google.cloud import trace_v2

PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)


class TestVPCServiceControlV2(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        except:
            pass
        return False

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_batch_write_spans(self):
        client = trace_v2.TraceServiceClient()

        proejct_inside = client.project_path(PROJECT_INSIDE)
        proejct_outside = client.project_path(PROJECT_OUTSIDE)
        spans = []

        write_inside = lambda: client.batch_write_spans(proejct_inside, spans)
        write_outside = lambda: client.batch_write_spans(proejct_outside, spans)

        assert not TestVPCServiceControlV2._is_rejected(write_inside)
        assert TestVPCServiceControlV2._is_rejected(write_outside)
