# Copyright 2018 Google LLC
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

import os
import time

from google.cloud import trace_v2
from google.cloud.trace_v2.proto import trace_pb2
from google.cloud.trace_v2.proto import tracing_pb2


class TestSystemTraceService(object):
    def test_batch_write_spans(self):
        project_id = os.environ["PROJECT_ID"]

        client = trace_v2.TraceServiceClient()
        name = client.project_path(project_id)
        spans = []
        client.batch_write_spans(name, spans)
