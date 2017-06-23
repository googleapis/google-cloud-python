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

from google.cloud._testing import _GAXBaseAPI


class _Base(object):
    PROJECT = 'PROJECT'
    PROJECT_PATH = 'projects/%s' % (PROJECT,)

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)


class Test__TraceAPI(_Base, unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.trace._gax import _TraceAPI

        return _TraceAPI

    def test_constructor(self):
        gax_api = _GAXTraceAPI()
        client = object()
        api = self._make_one(gax_api, client)
        self.assertIs(api._gax_api, gax_api)
        self.assertIs(api.client, client)

    def test_patch_traces(self):
        from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
            TraceSpan, Trace, Traces)
        from google.cloud._helpers import _datetime_to_pb_timestamp

        from datetime import datetime

        PROJECT = 'PROJECT'
        TRACE_ID = 'test_trace_id'
        SPAN_ID = 1234
        SPAN_NAME = 'test_span_name'
        START_TIME = datetime.utcnow()
        END_TIME = datetime.utcnow()

        TRACES = {
            'traces': [
                {
                    'projectId': PROJECT,
                    'traceId': TRACE_ID,
                    'spans': [
                        {
                            'spanId': SPAN_ID,
                            'name': SPAN_NAME,
                            'startTime': START_TIME.isoformat() + 'Z',
                            'endTime': END_TIME.isoformat() + 'Z',
                        },
                    ],
                },
            ],
        }

        gax_api = _GAXTraceAPI()
        api = self._make_one(gax_api, None)
        api.patch_traces(project_id=PROJECT, traces=TRACES)
        project_id, traces, options = (gax_api._patch_traces_called_with)

        self.assertEqual(len(traces.traces), 1)
        trace = traces.traces[0]

        self.assertEqual(len(trace.spans), 1)
        span = trace.spans[0]

        self.assertIsInstance(traces, Traces)
        self.assertEqual(trace.project_id, PROJECT)
        self.assertEqual(trace.trace_id, TRACE_ID)
        self.assertIsInstance(trace, Trace)

        self.assertEqual(span.span_id, SPAN_ID)
        self.assertEqual(span.name, SPAN_NAME)
        self.assertEqual(
            span.start_time,
            _datetime_to_pb_timestamp(START_TIME))
        self.assertEqual(
            span.end_time,
            _datetime_to_pb_timestamp(END_TIME))
        self.assertIsInstance(span, TraceSpan)

        self.assertIsNone(options)

    def test_get_trace(self):
        from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
            Trace)

        PROJECT = 'PROJECT'
        TRACE_ID = 'test_trace_id'
        TRACE_PB = Trace(project_id=PROJECT, trace_id=TRACE_ID)

        gax_api = _GAXTraceAPI(_get_trace_response=TRACE_PB)
        api = self._make_one(gax_api, None)

        api.get_trace(project_id=PROJECT, trace_id=TRACE_ID)

        project_id, trace_id, options = gax_api._get_traces_called_with
        self.assertEqual(project_id, PROJECT)
        self.assertEqual(trace_id, TRACE_ID)
        self.assertIsNone(options)

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

        SPAN_KIND = 2

        TRACES = {
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
                            'kind': SPAN_KIND,
                            'parentSpanId': parent_span_id,
                            'labels': labels,
                        },
                    ],
                },
            ],
        }

        traces_pb = _traces_mapping_to_pb(TRACES)
        trace_pb = traces_pb.traces
        return trace_pb

    def test_list_traces(self):
        from google.cloud._testing import _GAXPageIterator
        from google.cloud.gapic.trace.v1.enums import ListTracesRequest as Enum

        from datetime import datetime

        PROJECT = 'PROJECT'
        TRACE_ID = 'test_trace_id'
        SPAN_ID = 1234
        SPAN_NAME = 'test_span_name'
        SPAN_KIND = 'RPC_CLIENT'
        PARENT_SPAN_ID = 123
        START_TIME = datetime.utcnow().isoformat() + 'Z'
        END_TIME = datetime.utcnow().isoformat() + 'Z'
        LABELS = {
            '/http/status_code': '200',
            '/component': 'HTTP load balancer',
        }

        SIZE = 10
        TOKEN = 'TOKEN'
        VIEW_TYPE = Enum.ViewType.COMPLETE

        trace_pb = self._make_trace_pb(
            PROJECT,
            TRACE_ID,
            SPAN_ID,
            SPAN_NAME,
            START_TIME,
            END_TIME,
            PARENT_SPAN_ID,
            LABELS)

        response = _GAXPageIterator(trace_pb)
        gax_api = _GAXTraceAPI(_list_traces_response=response)
        api = self._make_one(gax_api, None)

        iterator = api.list_traces(
            project_id=PROJECT,
            view=VIEW_TYPE,
            page_size=SIZE,
            page_token=TOKEN)

        traces = list(iterator)

        self.assertEqual(len(traces), 1)
        trace = traces[0]

        self.assertEqual(len(trace['spans']), 1)
        span = trace['spans'][0]

        self.assertEqual(trace['projectId'], PROJECT)
        self.assertEqual(trace['traceId'], TRACE_ID)

        self.assertEqual(span['spanId'], str(SPAN_ID))
        self.assertEqual(span['name'], SPAN_NAME)

        self.assertEqual(
            span['startTime'], START_TIME)
        self.assertEqual(
            span['endTime'], END_TIME)
        self.assertEqual(span['kind'], SPAN_KIND)
        self.assertEqual(span['parentSpanId'], str(PARENT_SPAN_ID))
        self.assertEqual(span['labels'], LABELS)

        project_id, view, page_size, start_time, end_time, filter_, order_by, options = (
            gax_api._list_traces_called_with
        )
        self.assertEqual(project_id, PROJECT)
        self.assertEqual(view, VIEW_TYPE)
        self.assertEqual(page_size, SIZE)
        self.assertIsNone(start_time)
        self.assertIsNone(end_time)
        self.assertIsNone(filter_)
        self.assertIsNone(order_by)
        self.assertEqual(options.page_token, TOKEN)


class Test__parse_trace_pb(unittest.TestCase):

    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.trace._gax import _parse_trace_pb

        return _parse_trace_pb(*args, **kwargs)

    def test_registered_type(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
            TraceSpan, Trace)

        from datetime import datetime

        PROJECT = u'PROJECT'
        TRACE_ID = u'test_trace_id'
        SPAN_ID = 1234
        SPAN_NAME = u'test_span_name'
        START_TIME = datetime.utcnow()
        END_TIME = datetime.utcnow()

        start_time_pb = _datetime_to_pb_timestamp(START_TIME)
        end_time_pb = _datetime_to_pb_timestamp(END_TIME)

        span_pb = TraceSpan(
            span_id=SPAN_ID,
            name=SPAN_NAME,
            start_time=start_time_pb,
            end_time=end_time_pb)

        trace_pb = Trace(
            project_id=PROJECT,
            trace_id=TRACE_ID,
            spans=[span_pb])

        parse_result = self._call_fut(trace_pb)

        expected_result = {
            'projectId': PROJECT,
            'traceId': TRACE_ID,
            'spans': [
                {
                    'spanId': str(SPAN_ID),
                    'name': SPAN_NAME,
                    'startTime': START_TIME.isoformat() + 'Z',
                    'endTime': END_TIME.isoformat() + 'Z',
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

        patch = mock.patch.multiple(
            'google.cloud.trace._gax',
            TraceServiceClient=generated_api,
            make_secure_channel=make_channel)
        with patch:
            trace_api = self._call_fut(client)

        self.assertEqual(channels, [channel_obj])
        self.assertEqual(channel_args,
                         [(credentials, DEFAULT_USER_AGENT, host)])

        self.assertEqual(len(generated_api_kwargs), 1)
        self.assertEqual(generated_api_kwargs[0]['lib_name'], 'gccl')

        self.assertIsInstance(trace_api, _TraceAPI)
        self.assertIs(trace_api._gax_api, generated)
        self.assertIs(trace_api.client, client)


class _GAXTraceAPI(_GAXBaseAPI):
    def patch_traces(self, project_id, traces, options=None):
        self._patch_traces_called_with = (project_id, traces, options)

    def get_trace(self, project_id, trace_id, options=None):
        self._get_traces_called_with = (project_id, trace_id, options)
        return self._get_trace_response

    def list_traces(
            self,
            project_id,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            options=None):
        self._list_traces_called_with = (
            project_id,
            view,
            page_size,
            start_time,
            end_time,
            filter_,
            order_by,
            options)
        return self._list_traces_response
