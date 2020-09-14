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

from google.cloud import trace_v2


def create_span(
    project_id: str,
    trace_id: str,
    span_id: str,
    display_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
):
    """Create a new span.

    Args:
        project_id: The name of the project.
        trace_id: A unique identifier for a trace within a
            project; it is a 32-character hexadecimal encoding of a
            16-byte array.
        span_id: A unique identifier for a span within a trace;
            it is a 16-character hexadecimal encoding of an 8-byte
        display_name: A description of the span's
            operation (up to 128 bytes)
        start_time: The start time of the span.
        end_time: The end time of the span.
    """

    client = trace_v2.TraceServiceClient()

    name = client.span_path(project_id, trace_id, span_id)
    display_name = trace_v2.TruncatableString(value=display_name)

    request = trace_v2.Span(
        name=name,
        span_id=span_id,
        display_name=display_name,
        start_time=start_time,
        end_time=end_time,
    )

    span = client.create_span(request=request)

    print(span)
    return span
