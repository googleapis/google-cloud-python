# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import os

from google.cloud import trace_v1
import pytest

import patch_traces

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def trace_id():
    # list all traces in the project and return the first
    client = trace_v1.TraceServiceClient()
    traces = client.list_traces(project_id=PROJECT_ID)

    return list(traces)[0].trace_id


def test_patch_traces():
    patch_traces.patch_traces(project_id=PROJECT_ID)
