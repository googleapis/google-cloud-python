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

import datetime
import uuid

from google.cloud import trace_v2


def batch_write_spans(project_id: str):
    """Send new spans to new or existing traces."""

    client = trace_v2.TraceServiceClient()

    display_name = trace_v2.TruncatableString(value="Test Span Display Name")
    trace_id = str(uuid.uuid4()).replace("-", "")
    span_id = str(uuid.uuid4()).replace("-", "")[:16]

    end_time = datetime.datetime.now(tz=datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(seconds=5)

    # Create a single span
    span = trace_v2.Span(
        name=client.span_path(project_id, trace_id, span_id),
        span_id=span_id,
        display_name=display_name,
        start_time=start_time,
        end_time=end_time,
    )

    client.batch_write_spans(name=f"projects/{project_id}", spans=[span])
