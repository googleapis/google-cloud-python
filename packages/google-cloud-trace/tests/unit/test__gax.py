# Copyright 2017 Google LLC
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


class _Base(object):
    project = 'PROJECT'

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)


class Test__TraceAPI(_Base, unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.trace._gax import _TraceAPI

        return _TraceAPI

    def test_constructor(self):
        gax_api = object()
        client = object()
        api = self._make_one(gax_api, client)
        self.assertIs(api._gax_api, gax_api)
        self.assertIs(api.client, client)

    def test_patch_traces(self):
        from google.cloud.gapic.trace.v1 import trace_service_client
        from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
            TraceSpan, Trace, Traces)
        from google.cloud.trace._gax import _traces_mapping_to_pb
        from google.cloud._helpers import _datetime_to_pb_timestamp

        from datetime import datetime

        trace_id = 'test_trace_id'
        span_id = 1234
        span_name = 'test_span_name'
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()

        traces = {
            'traces': [
                {
                    'projectId': self.project,
                    'traceId': trace_id,
                    'spans': [
                        {
                            'spanId': span_id,
                            'name': span_name,
                            'startTime': start_time.isoformat() + 'Z',
                            'endTime': end_time.isoformat() + 'Z',
                        },
                    ],
                },
            ],
        }

        traces_pb = _traces_mapping_to_pb(traces)

        gax_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        api = self._make_one(gax_api, None)
        api.patch_traces(project_id=self.project, traces=traces)

        gax_api.patch_traces.assert_called_with(self.project, traces_pb, None)

        call_args = gax_api.patch_traces.call_args[0]
        self.assertEqual(len(call_args), 3)
        traces_called = call_args[1]
        self.assertEqual(len(traces_called.traces), 1)
        trace = traces_called.traces[0]

        self.assertEqual(len(trace.spans), 1)
        span = trace.spans[0]

        self.assertIsInstance(traces_called, Traces)
        self.assertEqual(trace.project_id, self.project)
        self.assertEqual(trace.trace_id, trace_id)
        self.assertIsInstance(trace, Trace)

        self.assertEqual(span.span_id, span_id)
        self.assertEqual(span.name, span_name)
        self.assertEqual(
            span.start_time,
            _datetime_to_pb_timestamp(start_time))
        self.assertEqual(
            span.end_time,
            _datetime_to_pb_timestamp(end_time))
        self.assertIsInstance(span, TraceSpan)

    def test_get_trace(self):
        from google.cloud.gapic.trace.v1 import trace_service_client

        trace_id = 'test_trace_id'

        gax_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        api = self._make_one(gax_api, None)
        patch = mock.patch('google.cloud.trace._gax._parse_trace_pb',
                           return_value='fake_pb_result')

        with patch:
            api.get_trace(project_id=self.project, trace_id=trace_id)

        gax_api.get_trace.assert_called_with(self.project, trace_id, None)

    def _make_trace_pb(
            self,
            project,
            trace_id,
            span_id,
            span_name,
            start_time,
            end_time,
            parent_span_id,
            labels):
        from google.cloud.trace._gax import _traces_mapping_to_pb

        span_kind = 2

        traces = {
            'traces': [
                {
                    'projectId': project,
                    'traceId': trace_id,
                    'spans': [
                        {
                            'spanId': span_id,
                            'name': span_name,
                            'startTime': start_time,
                            'endTime': end_time,
                            'kind': span_kind,
                            'parentSpanId': parent_span_id,
                            'labels': labels,
                        },
                    ],
                },
            ],
        }

        traces_pb = _traces_mapping_to_pb(traces)
        trace_pb = traces_pb.traces
        return trace_pb

    def test_list_traces_no_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.gapic.trace.v1 import trace_service_client
        from google.cloud.gapic.trace.v1.enums import ListTracesRequest as Enum
        from google.gax import INITIAL_PAGE

        from datetime import datetime

        trace_id = 'test_trace_id'
        span_id = 1234
        span_name = 'test_span_name'
        span_kind = 'RPC_CLIENT'
        parent_span_id = 123
        start_time = datetime.utcnow().isoformat() + 'Z'
        end_time = datetime.utcnow().isoformat() + 'Z'
        labels = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }
        size = 10
        view_type = Enum.ViewType.COMPLETE

        trace_pb = self._make_trace_pb(
            self.project,
            trace_id,
            span_id,
            span_name,
            start_time,
            end_time,
            parent_span_id,
            labels)

        response = _GAXPageIterator(trace_pb)
        gax_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        gax_api.list_traces.return_value = response
        api = self._make_one(gax_api, None)

        iterator = api.list_traces(
            project_id=self.project,
            view=view_type,
            page_size=size)

        traces = list(iterator)

        self.assertEqual(len(traces), 1)
        trace = traces[0]

        self.assertEqual(len(trace['spans']), 1)
        span = trace['spans'][0]

        self.assertEqual(trace['projectId'], self.project)
        self.assertEqual(trace['traceId'], trace_id)

        self.assertEqual(span['spanId'], str(span_id))
        self.assertEqual(span['name'], span_name)

        self.assertEqual(
            span['startTime'], start_time)
        self.assertEqual(
            span['endTime'], end_time)
        self.assertEqual(span['kind'], span_kind)
        self.assertEqual(span['parentSpanId'], str(parent_span_id))
        self.assertEqual(span['labels'], labels)

        call_args = gax_api.list_traces.call_args[1]

        self.assertEqual(call_args['project_id'], self.project)
        self.assertEqual(call_args['view'], view_type)
        self.assertEqual(call_args['page_size'], size)
        self.assertIsNone(call_args['start_time'])
        self.assertIsNone(call_args['end_time'])
        self.assertIsNone(call_args['filter_'])
        self.assertIsNone(call_args['order_by'])
        self.assertEqual(call_args['options'].page_token, INITIAL_PAGE)

    def test_list_traces_with_paging(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.gapic.trace.v1 import trace_service_client
        from google.cloud.gapic.trace.v1.enums import ListTracesRequest as Enum

        from datetime import datetime

        trace_id = 'test_trace_id'
        span_id = 1234
        span_name = 'test_span_name'
        span_kind = 'RPC_CLIENT'
        parent_span_id = 123
        start_time = datetime.utcnow().isoformat() + 'Z'
        end_time = datetime.utcnow().isoformat() + 'Z'
        labels = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }
        size = 10
        view_type = Enum.ViewType.COMPLETE
        token = 'TOKEN'

        trace_pb = self._make_trace_pb(
            self.project,
            trace_id,
            span_id,
            span_name,
            start_time,
            end_time,
            parent_span_id,
            labels)

        response = _GAXPageIterator(trace_pb)
        gax_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        gax_api.list_traces.return_value = response
        api = self._make_one(gax_api, None)

        iterator = api.list_traces(
            project_id=self.project,
            view=view_type,
            page_size=size,
            page_token=token)

        traces = list(iterator)

        self.assertEqual(len(traces), 1)
        trace = traces[0]

        self.assertEqual(len(trace['spans']), 1)
        span = trace['spans'][0]

        self.assertEqual(trace['projectId'], self.project)
        self.assertEqual(trace['traceId'], trace_id)

        self.assertEqual(span['spanId'], str(span_id))
        self.assertEqual(span['name'], span_name)

        self.assertEqual(
            span['startTime'], start_time)
        self.assertEqual(
            span['endTime'], end_time)
        self.assertEqual(span['kind'], span_kind)
        self.assertEqual(span['parentSpanId'], str(parent_span_id))
        self.assertEqual(span['labels'], labels)

        call_args = gax_api.list_traces.call_args[1]

        self.assertEqual(call_args['project_id'], self.project)
        self.assertEqual(call_args['view'], view_type)
        self.assertEqual(call_args['page_size'], size)
        self.assertIsNone(call_args['start_time'])
        self.assertIsNone(call_args['end_time'])
        self.assertIsNone(call_args['filter_'])
        self.assertIsNone(call_args['order_by'])
        self.assertEqual(call_args['options'].page_token, token)


class Test__parse_trace_pb(unittest.TestCase):

    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.trace._gax import _parse_trace_pb

        return _parse_trace_pb(*args, **kwargs)

    def test_registered_type(self):
        from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
            TraceSpan, Trace)
        from google.protobuf.timestamp_pb2 import Timestamp

        project = u'PROJECT'
        trace_id = u'test_trace_id'
        span_id = 1234
        span_name = u'test_span_name'
        start_time = '2017-06-24T00:12:50.369990Z'
        end_time = '2017-06-24T00:13:39.633255Z'
        start_seconds = 1498263170
        start_nanos = 369990000
        end_seconds = 1498263219
        end_nanos = 633255000

        start_time_pb = Timestamp(seconds=start_seconds, nanos=start_nanos)
        end_time_pb = Timestamp(seconds=end_seconds, nanos=end_nanos)

        span_pb = TraceSpan(
            span_id=span_id,
            name=span_name,
            start_time=start_time_pb,
            end_time=end_time_pb)

        trace_pb = Trace(
            project_id=project,
            trace_id=trace_id,
            spans=[span_pb])

        parse_result = self._call_fut(trace_pb)

        expected_result = {
            'projectId': project,
            'traceId': trace_id,
            'spans': [
                {
                    'spanId': str(span_id),
                    'name': span_name,
                    'startTime': start_time,
                    'endTime': end_time,
                },
            ],
        }

        self.assertEqual(parse_result, expected_result)

    @mock.patch('google.cloud.trace._gax.MessageToDict',
                side_effect=TypeError)
    def test_unregistered_type(self, msg_to_dict_mock):
        trace_pb = mock.Mock(spec=['HasField'])
        trace_pb.HasField.return_value = False
        with self.assertRaises(TypeError):
            self._call_fut(trace_pb)


class Test_make_gax_trace_api(unittest.TestCase):

    def _call_fut(self, client):
        from google.cloud.trace._gax import make_gax_trace_api

        return make_gax_trace_api(client)

    def test_it(self):
        from google.cloud.trace._gax import _TraceAPI
        from google.cloud._http import DEFAULT_USER_AGENT

        credentials = object()
        client = mock.Mock(_credentials=credentials, spec=['_credentials'])
        channels = []
        channel_args = []
        generated_api_kwargs = []
        channel_obj = object()
        generated = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def generated_api(channel=None, **kwargs):
            channels.append(channel)
            generated_api_kwargs.append(kwargs)
            return generated

        host = 'foo.apis.invalid'
        generated_api.SERVICE_ADDRESS = host

        patch_channel = mock.patch(
            'google.cloud.trace._gax.make_secure_channel',
            new=make_channel)

        patch_api = mock.patch(
            'google.cloud.trace._gax.trace_service_client.TraceServiceClient',
            new=generated_api)

        with patch_api:
            with patch_channel:
                trace_api = self._call_fut(client)

        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(credentials, DEFAULT_USER_AGENT, host)])

        self.assertEqual(len(generated_api_kwargs), 1)
        self.assertEqual(generated_api_kwargs[0]['lib_name'], 'gccl')

        self.assertIsInstance(trace_api, _TraceAPI)
        self.assertIs(trace_api._gax_api, generated)
        self.assertIs(trace_api.client, client)
