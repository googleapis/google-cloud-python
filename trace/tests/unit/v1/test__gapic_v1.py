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

import datetime
import unittest

import mock

from google.api_core import grpc_helpers


class _Base(object):
    project = "PROJECT"

    def _make_one(self, gapic_client=None, handwritten_client=None):
        from google.cloud.trace_v1.gapic import trace_service_client

        channel = grpc_helpers.ChannelStub()
        if gapic_client is None:
            gapic_client = trace_service_client.TraceServiceClient(channel=channel)
        if handwritten_client is None:
            handwritten_client = mock.Mock()
        api = self._get_target_class()(gapic_client, handwritten_client)
        return channel, api


class Test__TraceAPI(_Base, unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.trace.v1._gapic import _TraceAPI

        return _TraceAPI

    def test_constructor(self):
        from google.cloud.trace_v1.gapic import trace_service_client

        channel = grpc_helpers.ChannelStub()
        gapic_client = trace_service_client.TraceServiceClient(channel=channel)
        _, api = self._make_one(gapic_client, mock.sentinel.client)
        self.assertIs(api._gapic_api, gapic_client)
        self.assertIs(api.client, mock.sentinel.client)

    def test_patch_traces(self):
        from google.cloud.trace_v1.gapic import trace_service_client
        from google.cloud.trace_v1.proto.trace_pb2 import TraceSpan, Trace, Traces
        from google.cloud.trace.v1._gapic import _traces_mapping_to_pb
        from google.cloud._helpers import _datetime_to_pb_timestamp

        trace_id = "test_trace_id"
        span_id = 1234
        span_name = "test_span_name"
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()

        traces = {
            "traces": [
                {
                    "projectId": self.project,
                    "traceId": trace_id,
                    "spans": [
                        {
                            "spanId": span_id,
                            "name": span_name,
                            "startTime": start_time.isoformat() + "Z",
                            "endTime": end_time.isoformat() + "Z",
                        }
                    ],
                }
            ]
        }

        traces_pb = _traces_mapping_to_pb(traces)

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        _, api = self._make_one(gapic_api, None)
        api.patch_traces(project_id=self.project, traces=traces)

        gapic_api.patch_traces.assert_called_with(self.project, traces_pb)

        call_args = gapic_api.patch_traces.call_args[0]
        self.assertEqual(len(call_args), 2)
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
        self.assertEqual(span.start_time, _datetime_to_pb_timestamp(start_time))
        self.assertEqual(span.end_time, _datetime_to_pb_timestamp(end_time))
        self.assertIsInstance(span, TraceSpan)

    def test_get_trace(self):
        from google.cloud.trace_v1.gapic import trace_service_client

        trace_id = "test_trace_id"

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        _, api = self._make_one(gapic_api, None)
        patch = mock.patch(
            "google.cloud.trace.v1._gapic._parse_trace_pb",
            return_value="fake_pb_result",
        )

        with patch:
            api.get_trace(project_id=self.project, trace_id=trace_id)

        gapic_api.get_trace.assert_called_with(self.project, trace_id)

    def _make_trace_pb(
        self,
        project,
        trace_id,
        span_id,
        span_name,
        start_time,
        end_time,
        parent_span_id,
        labels,
    ):
        from google.cloud.trace.v1._gapic import _traces_mapping_to_pb

        span_kind = 2

        traces = {
            "traces": [
                {
                    "projectId": project,
                    "traceId": trace_id,
                    "spans": [
                        {
                            "spanId": span_id,
                            "name": span_name,
                            "startTime": start_time,
                            "endTime": end_time,
                            "kind": span_kind,
                            "parentSpanId": parent_span_id,
                            "labels": labels,
                        }
                    ],
                }
            ]
        }

        traces_pb = _traces_mapping_to_pb(traces)
        trace_pb = traces_pb.traces
        return trace_pb

    def test_list_traces(self):
        from google.cloud._helpers import _rfc3339_to_datetime
        from google.cloud._helpers import UTC
        from google.cloud.trace_v1.gapic import trace_service_client
        from google.cloud.trace_v1.gapic.enums import ListTracesRequest as Enum
        from google.cloud.trace_v1.proto import trace_pb2

        trace_id = "test_trace_id"
        span_id = 1234
        span_name = "test_span_name"
        span_kind = "RPC_CLIENT"
        parent_span_id = 123
        start_ts = datetime.datetime.utcnow()
        end_ts = datetime.datetime.utcnow()
        labels = {"/http/status_code": "200", "/component": "HTTP load balancer"}
        size = 10
        view_type = Enum.ViewType.COMPLETE
        token = "TOKEN"

        trace_pb = self._make_trace_pb(
            self.project,
            trace_id,
            span_id,
            span_name,
            start_ts.isoformat() + "Z",
            end_ts.isoformat() + "Z",
            parent_span_id,
            labels,
        )

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        gapic_api.list_traces = mock.create_autospec(gapic_api.list_traces)
        channel, api = self._make_one()

        channel.ListTraces.response = trace_pb2.ListTracesResponse(traces=[trace_pb[0]])
        iterator = api.list_traces(
            project_id=self.project, view=view_type, page_size=size, page_token=token
        )

        traces = list(iterator)

        self.assertEqual(len(traces), 1)
        trace = traces[0]

        self.assertEqual(len(trace["spans"]), 1)
        span = trace["spans"][0]

        self.assertEqual(trace["projectId"], self.project)
        self.assertEqual(trace["traceId"], trace_id)

        self.assertEqual(span["spanId"], str(span_id))
        self.assertEqual(span["name"], span_name)

        self.assertEqual(
            _rfc3339_to_datetime(span["startTime"]), start_ts.replace(tzinfo=UTC)
        )
        self.assertEqual(
            _rfc3339_to_datetime(span["endTime"]), end_ts.replace(tzinfo=UTC)
        )
        self.assertEqual(span["kind"], span_kind)
        self.assertEqual(span["parentSpanId"], str(parent_span_id))
        self.assertEqual(span["labels"], labels)

        self.assertEqual(len(channel.ListTraces.requests), 1)
        request = channel.ListTraces.requests[0]

        self.assertEqual(request.project_id, self.project)
        self.assertEqual(request.view, view_type)
        self.assertEqual(request.page_size, size)
        self.assertEqual(
            request.start_time.ToDatetime(), datetime.datetime(1970, 1, 1, 0, 0)
        )
        self.assertEqual(
            request.end_time.ToDatetime(), datetime.datetime(1970, 1, 1, 0, 0)
        )
        self.assertEqual(request.filter, "")
        self.assertEqual(request.order_by, "")


class Test__parse_trace_pb(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.trace.v1._gapic import _parse_trace_pb

        return _parse_trace_pb(*args, **kwargs)

    def test_registered_type(self):
        from google.cloud.trace_v1.proto.trace_pb2 import TraceSpan, Trace
        from google.protobuf.timestamp_pb2 import Timestamp

        project = u"PROJECT"
        trace_id = u"test_trace_id"
        span_id = 1234
        span_name = u"test_span_name"
        start_time = "2017-06-24T00:12:50.369990Z"
        end_time = "2017-06-24T00:13:39.633255Z"
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
            end_time=end_time_pb,
        )

        trace_pb = Trace(project_id=project, trace_id=trace_id, spans=[span_pb])

        parse_result = self._call_fut(trace_pb)

        expected_result = {
            "projectId": project,
            "traceId": trace_id,
            "spans": [
                {
                    "spanId": str(span_id),
                    "name": span_name,
                    "startTime": start_time,
                    "endTime": end_time,
                }
            ],
        }

        self.assertEqual(parse_result, expected_result)

    @mock.patch("google.cloud.trace.v1._gapic.MessageToDict", side_effect=TypeError)
    def test_unregistered_type(self, msg_to_dict_mock):
        trace_pb = mock.Mock(spec=["HasField"])
        trace_pb.HasField.return_value = False
        with self.assertRaises(TypeError):
            self._call_fut(trace_pb)


class Test_make_trace_api(unittest.TestCase):
    def _call_fut(self, client):
        from google.cloud.trace.v1._gapic import make_trace_api

        return make_trace_api(client)

    def test_it(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        credentials = object()
        client = mock.Mock(_credentials=credentials, spec=["_credentials"])
        generated_api_kwargs = []
        generated = object()

        def generated_api(**kwargs):
            generated_api_kwargs.append(kwargs)
            return generated

        host = "foo.apis.invalid"
        generated_api.SERVICE_ADDRESS = host

        patch_api = mock.patch(
            "google.cloud.trace.v1._gapic.trace_service_client." "TraceServiceClient",
            new=generated_api,
        )

        with patch_api:
            trace_api = self._call_fut(client)

        self.assertEqual(len(generated_api_kwargs), 1)

        self.assertIsInstance(trace_api, _TraceAPI)
        self.assertIs(trace_api._gapic_api, generated)
        self.assertIs(trace_api.client, client)
