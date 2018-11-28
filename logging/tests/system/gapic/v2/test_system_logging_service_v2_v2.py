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

import google.auth
from google.api import monitored_resource_pb2
from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_pb2


class TestSystemLoggingServiceV2(object):
    def test_write_log_entries(self):
        _, project_id = google.auth.default()

        client = logging_v2.LoggingServiceV2Client()
        log_name = client.log_path(project_id, "test-{0}".format(time.time()))
        resource = {}
        labels = {}
        entries = []
        response = client.write_log_entries(
            entries, log_name=log_name, resource=resource, labels=labels
        )
