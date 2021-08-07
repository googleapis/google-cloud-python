# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import unittest
import inspect
import re

import google.cloud.logging

from ..common.common import Common

class CommonStdout:
    def test_stdout_log(self):
        if self.language not in ["nodejs"]:
            # TODO: other languages to also support this test
            return True
        if self.environment in ["compute"]:
           # No logging agent support in GCE
           return True
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "stdoutlog")
        # Note: 2 logs are spawned, use the one containing http_request prop.
        found = log_list[-1]
        if found.http_request is None:
            found = log_list[-2]
        # Agents lift fields inconsistently among envs, so check if is expected.
        if hasattr(self, 'stdout_log_name'):
           self.assertTrue(self.stdout_log_name in found.log_name)
        if hasattr(self, 'stdout_severity'):
            self.assertEqual(found.severity, self.stdout_severity)
        if hasattr(self, 'stdout_insert_id'):
            self.assertEqual(found.insert_id, self.stdout_insert_id)
        if hasattr(self, 'stdout_timestamp'):
            self.assertEqual(found.timestamp, self.stdout_timestamp)
        if hasattr(self, 'stdout_trace'):
            self.assertTrue(self.stdout_trace in found.trace)
        if hasattr(self, 'stdout_span_id'):
            self.assertEqual(found.span_id, self.stdout_span_id)
        # TODO: uncomment this again once python-logging accepts trace_samples
        # if hasattr(self, 'stdout_trace_sampled'):
        #   self.assertEqual(found.trace_sampled, self.stdout_trace_sampled)
        if hasattr(self, 'stdout_labels'):
            for prop in self.stdout_labels:
                self.assertTrue(found.labels[prop],
                f'{prop} is not set')
        if hasattr(self, 'stdout_resource_type'):
            self.assertEqual(found.resource.type, self.stdout_resource_type)
        if hasattr(self, 'stdout_resource_labels'):
            for prop in self.stdout_resource_labels:
                self.assertTrue(found.resource.labels[prop],
                f'{prop} is not set')
        if hasattr(self, 'stdout_payload_props'):
            for prop in self.stdout_payload_props:
                self.assertTrue(found.payload[prop],
                f'{prop} is not set')
