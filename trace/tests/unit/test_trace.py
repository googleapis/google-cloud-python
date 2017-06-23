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


class TestTrace(unittest.TestCase):

    PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.trace import Trace

        return Trace

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        TRACE_ID = 'test_trace_id'

        client = mock.Mock(project=self.PROJECT, spec=['project'])
        patch = mock.patch(
            'google.cloud.trace.trace.generate_trace_id',
            return_value=TRACE_ID)

        with patch:
            trace = self._make_one(client)

        self.assertIs(trace.client, client)
        self.assertEqual(trace.project_id, self.PROJECT)
        self.assertEqual(trace.trace_id, TRACE_ID)

    def test_constructor_explicit(self):
        TRACE_ID = 'test_trace_id'

        client = mock.Mock(project=self.PROJECT, spec=['project'])
        trace = self._make_one(
            client=client,
            project_id=self.PROJECT,
            trace_id=TRACE_ID)

        self.assertIs(trace.client, client)
        self.assertEqual(trace.project_id, self.PROJECT)
        self.assertEqual(trace.trace_id, TRACE_ID)

    def test_start(self):
        client = object()
        trace = self._make_one(client=client, project_id=self.PROJECT)
        trace.start()

        self.assertEqual(trace.spans, [])

    def test_finish(self):
        pass

    def test_span(self):
        from google.cloud.trace.trace_span import TraceSpan

        SPAN_NAME = 'test_span_name'

        client = object()
        trace = self._make_one(client=client, project_id=self.PROJECT)
        trace.spans = []

        trace.span(name=SPAN_NAME)
        self.assertEqual(len(trace.spans), 1)

        result_span = trace.spans[0]
        self.assertIsInstance(result_span, TraceSpan)
        self.assertEqual(result_span.name, SPAN_NAME)


    def test_send(self):
        pass


class Test_traverse_span_tree(unittest.TestCase):
    pass


class Test_generate_span_id(unittest.TestCase):
    pass
