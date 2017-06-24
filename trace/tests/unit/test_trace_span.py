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

    project = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.trace_span import TraceSpan

        return TraceSpan

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

        span_id = 'test_span_id'
        span_name = 'test_span_name'

        patch = mock.patch(
            'google.cloud.trace.trace_span.generate_span_id',
            return_value=span_id)

        with patch:
            span = self._make_one(span_name)

        self.assertEqual(span.name, span_name)
        self.assertEqual(span.span_id, span_id)
        self.assertEqual(span.kind, Enum.SpanKind.SPAN_KIND_UNSPECIFIED)
        self.assertIsNone(span.parent_span_id)
        self.assertIsNone(span.labels)
        self.assertIsNone(span.start_time)
        self.assertIsNone(span.end_time)
        self.assertEqual(span.children, [])

    def test_constructor_explicit(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

        from datetime import datetime

        span_id = 'test_span_id'
        span_name = 'test_span_name'
        kind = Enum.SpanKind.RPC_CLIENT
        parent_span_id = 1234
        start_time = datetime.utcnow().isoformat() + 'Z'
        end_time = datetime.utcnow().isoformat() + 'Z'
        labels = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }

        span = self._make_one(
            name=span_name,
            kind=kind,
            parent_span_id=parent_span_id,
            labels=labels,
            start_time=start_time,
            end_time=end_time,
            span_id=span_id)

        self.assertEqual(span.name, span_name)
        self.assertEqual(span.span_id, span_id)
        self.assertEqual(span.kind, kind)
        self.assertEqual(span.parent_span_id, parent_span_id)
        self.assertEqual(span.labels, labels)
        self.assertEqual(span.start_time, start_time)
        self.assertEqual(span.end_time, end_time)
        self.assertEqual(span.children, [])

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
