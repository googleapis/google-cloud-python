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

    project = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.trace import Trace

        return Trace

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        trace_id = 'test_trace_id'

        client = mock.Mock(project=self.project, spec=['project'])
        patch = mock.patch(
            'google.cloud.trace.trace.generate_trace_id',
            return_value=trace_id)

        with patch:
            trace = self._make_one(client)

        self.assertIs(trace.client, client)
        self.assertEqual(trace.project_id, self.project)
        self.assertEqual(trace.trace_id, trace_id)

    def test_constructor_explicit(self):
        trace_id = 'test_trace_id'

        client = mock.Mock(project=self.project, spec=['project'])
        trace = self._make_one(
            client=client,
            project_id=self.project,
            trace_id=trace_id)

        self.assertIs(trace.client, client)
        self.assertEqual(trace.project_id, self.project)
        self.assertEqual(trace.trace_id, trace_id)

    def test_start(self):
        client = object()
        trace = self._make_one(client=client, project_id=self.project)
        trace.start()

        self.assertEqual(trace.spans, [])

    def test_finish_with_empty_span(self):

        def patch_traces(traces, project_id=None, options=None):
            _patch_traces_called_with = (traces, project_id, options)
            return _patch_traces_called_with

        client = mock.Mock(project=self.project, spec=['project'])
        client.patch_traces = patch_traces
        trace = self._make_one(client=client)

        with trace:
            trace.spans = [None]
            self.assertEqual(trace.spans, [None])

        self.assertEqual(trace.spans, [])

    def test_finish_with_valid_span(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

        def patch_traces(traces, project_id=None, options=None):
            _patch_traces_called_with = (traces, project_id, options)
            return _patch_traces_called_with

        client = mock.Mock(project=self.project, spec=['project'])
        client.patch_traces = patch_traces
        trace = self._make_one(client=client)

        span_name = 'span'
        span_id = 123
        kind = Enum.SpanKind.SPAN_KIND_UNSPECIFIED
        start_time = '2017-06-25'
        end_time = '2017-06-26'

        span = mock.Mock(name=span_name,
                         kind=kind,
                         parent_span_id=None,
                         span_id=span_id,
                         start_time=start_time,
                         end_time=end_time,
                         labels=None,
                         children=[],
                         spec=['name',
                               'kind',
                               'parent_span_id',
                               'span_id',
                               'start_time',
                               'end_time',
                               'labels',
                               'children'])

        with trace:
            trace.spans = [span]
            self.assertEqual(trace.spans, [span])

        self.assertEqual(trace.spans, [])

    def test_span(self):
        from google.cloud.trace.trace_span import TraceSpan

        span_name = 'test_span_name'

        client = object()
        trace = self._make_one(client=client, project_id=self.project)
        trace.spans = []

        trace.span(name=span_name)
        self.assertEqual(len(trace.spans), 1)

        result_span = trace.spans[0]
        self.assertIsInstance(result_span, TraceSpan)
        self.assertEqual(result_span.name, span_name)

    def test_send_without_spans(self):
        client = mock.Mock(project=self.project, spec=['project'])
        trace_id = 'test_trace_id'
        trace = self._make_one(client=client, trace_id=trace_id)
        trace.spans = []

        trace.send()

        self.assertFalse(client.called)
        self.assertEqual(trace.project_id, self.project)
        self.assertEqual(trace.trace_id, trace_id)
        self.assertEqual(trace.spans, [])

    def test_send_with_spans(self):
        from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum
        from google.cloud.trace.client import Client

        client = mock.Mock(spec=Client)
        client.project = self.project
        trace_id = 'test_trace_id'
        trace = self._make_one(client=client, trace_id=trace_id)
        child_span_name = 'child_span'
        root_span_name = 'root_span'
        child_span_id = 123
        root_span_id = 456
        kind = Enum.SpanKind.SPAN_KIND_UNSPECIFIED
        start_time = '2017-06-25'
        end_time = '2017-06-26'
        labels = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }

        child_span = mock.Mock(name=child_span_name,
                               kind=kind,
                               parent_span_id=root_span_id,
                               span_id=child_span_id,
                               start_time=start_time,
                               end_time=end_time,
                               labels=labels,
                               children=[],
                               spec=['name',
                                     'kind',
                                     'parent_span_id',
                                     'span_id',
                                     'start_time',
                                     'end_time',
                                     'labels',
                                     'children'])
        root_span = mock.Mock(name=root_span_name,
                              kind=kind,
                              parent_span_id=None,
                              span_id=root_span_id,
                              start_time=start_time,
                              end_time=end_time,
                              labels=None,
                              children=[child_span],
                              spec=['name',
                                    'kind',
                                    'parent_span_id',
                                    'span_id',
                                    'start_time',
                                    'end_time',
                                    'labels',
                                    'children'])

        child_span_json = {
            'name': child_span.name,
            'kind': kind,
            'parentSpanId': root_span_id,
            'spanId': child_span_id,
            'startTime': start_time,
            'endTime': end_time,
            'labels': labels,
        }

        root_span_json = {
            'name': root_span.name,
            'kind': kind,
            'spanId': root_span_id,
            'startTime': start_time,
            'endTime': end_time,
        }

        trace.spans = [root_span]
        traces = {
            'traces': [
                {
                    'projectId': self.project,
                    'traceId': trace_id,
                    'spans': [
                        root_span_json,
                        child_span_json
                    ]
                }
            ]
        }

        trace.send()

        client.patch_traces.assert_called_with(project_id=self.project,
                                               traces=traces,
                                               options=None)

        self.assertEqual(trace.project_id, self.project)
        self.assertEqual(trace.trace_id, trace_id)
        self.assertEqual(trace.spans, [root_span])
