# Copyright 2017 Google Inc.
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

import unittest

import mock


class TestTraceSpan(unittest.TestCase):

    PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.trace_span import TraceSpan

        return TraceSpan

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

        SPAN_ID = 'test_span_id'
        SPAN_NAME = 'test_span_name'

        patch = mock.patch(
            'google.cloud.trace.trace_span.generate_span_id',
            return_value=SPAN_ID)

        with patch:
            span = self._make_one(SPAN_NAME)

        self.assertEqual(span.name, SPAN_NAME)
        self.assertEqual(span.span_id, SPAN_ID)
        self.assertEqual(span.kind, Enum.SpanKind.SPAN_KIND_UNSPECIFIED)
        self.assertIsNone(span.parent_span_id)
        self.assertIsNone(span.labels)
        self.assertIsNone(span.start_time)
        self.assertIsNone(span.end_time)

    def test_constructor_explicit(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

        from datetime import datetime

        SPAN_ID = 'test_span_id'
        SPAN_NAME = 'test_span_name'
        KIND = Enum.SpanKind.RPC_CLIENT
        PARENT_SPAN_ID = 1234
        START_TIME = datetime.utcnow().isoformat() + 'Z'
        END_TIME = datetime.utcnow().isoformat() + 'Z'
        LABELS = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }

        span = self._make_one(
            name=SPAN_NAME,
            kind=KIND,
            parent_span_id=PARENT_SPAN_ID,
            labels=LABELS,
            start_time=START_TIME,
            end_time=END_TIME,
            span_id=SPAN_ID)

        self.assertEqual(span.name, SPAN_NAME)
        self.assertEqual(span.span_id, SPAN_ID)
        self.assertEqual(span.kind, KIND)
        self.assertEqual(span.parent_span_id, PARENT_SPAN_ID)
        self.assertEqual(span.labels, LABELS)
        self.assertEqual(span.start_time, START_TIME)
        self.assertEqual(span.end_time, END_TIME)

    def test_span(self):
        pass

    def test_set_start_time(self):
        pass

    def test_set_end_time(self):
        pass


class Test_generate_span_id(unittest.TestCase):
    pass


class Test_format_span_json(unittest.TestCase):
    pass
