# Copyright 2021 Google LLC
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

import logging
import unittest
import inspect

import google.cloud.logging

from ..common.common import Common
from ..common.stdout import CommonStdout


class TestCloudFunctions(Common, CommonStdout, unittest.TestCase):

    environment = "functions"
    language = "nodejs"

    monitored_resource_name = "cloud_function"
    monitored_resource_labels = [
        "region",
        "function_name",
        "project_id",
    ]

    request_props = [
        "requestMethod",
        "requestUrl",
        "protocol",
    ]

    stdout_payload_props = [
        "message",
        "resource",
        "timestamp",
        "logName",
    ]
    stdout_severity = "WARNING"
    stdout_request_props = request_props
    stdout_labels = [
        "foo",
        # Nicely inserted by the agent
        "execution_id",
    ]
    # Randomly dropped by Functions agent:
    # stdout_insert_id = '42'
    # stdout_trace = /traces/0679686673a'
    # stdout_span_id = '000000000000004a'
    # stdout_trace_sampled = 'true'
    # =============================
    # Not lifted and just left in JSONPayload:
    # stdout_resource_type
    # stdout_resource_labels
    # stdout_log_name
    # stdout_timestamp
