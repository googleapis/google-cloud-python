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
import os
import uuid

import create_span

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_get_trace():
    trace_id = str(uuid.uuid4()).replace("-", "")
    span_id = str(uuid.uuid4()).replace("-", "")[:16]
    end_time = datetime.datetime.now(tz=datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(seconds=5)

    span = create_span.create_span(
        project_id=PROJECT_ID,
        trace_id=trace_id,
        span_id=span_id,
        display_name="test",
        start_time=start_time,
        end_time=end_time,
    )

    assert span.name == f"projects/{PROJECT_ID}/traces/{trace_id}/spans/{span_id}"
