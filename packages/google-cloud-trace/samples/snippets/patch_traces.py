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

import uuid

from google.cloud import trace_v1


def patch_traces(project_id: str):
    """Send new traces or update existing traces."""

    client = trace_v1.TraceServiceClient()

    trace = trace_v1.Trace(
        project_id=project_id,
        trace_id=str(uuid.uuid4()).replace("-", ""),
        spans=[trace_v1.TraceSpan(span_id=1, name="test-span")],
    )

    request = trace_v1.PatchTracesRequest(
        project_id=project_id, traces=trace_v1.Traces(traces=[trace])
    )

    client.patch_traces(request=request)
