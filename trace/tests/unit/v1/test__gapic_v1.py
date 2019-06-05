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


class Test__TraceAPI(unittest.TestCase):
    project = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.v1._gapic import _TraceAPI

        return _TraceAPI

    def _make_one(self, gapic_client=None, handwritten_client=None):
        from google.cloud.trace_v1.gapic import trace_service_client

        if gapic_client is None:
            gapic_client = mock.create_autospec(trace_service_client.TraceServiceClient)
        if handwritten_client is None:
            handwritten_client = mock.Mock()
        api = self._get_target_class()(gapic_client, handwritten_client)
        return api

    def test_constructor(self):
        from google.cloud.trace_v1.gapic import trace_service_client

        gapic_client = mock.create_autospec(trace_service_client.TraceServiceClient)
        api = self._make_one(gapic_client, mock.sentinel.client)
        self.assertIs(api._gapic_api, gapic_client)
        self.assertIs(api.client, mock.sentinel.client)

    def test_patch_traces(self):
        from google.cloud.trace_v1.gapic import trace_service_client
        from google.cloud.trace.v1._gapic import _traces_mapping_to_pb

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
        gapic_api = mock.create_autospec(trace_service_client.TraceServiceClient)
        api = self._make_one(gapic_api, None)

        api.patch_traces(project_id=self.project, traces=traces)

        gapic_api.patch_traces.assert_called_once_with(self.project, traces_pb)

    def test_get_trace(self):
        from google.cloud.trace_v1.gapic import trace_service_client
        from google.cloud.trace_v1.proto.trace_pb2 import Trace

        trace_id = "test_trace_id"
        trace_pb = Trace(project_id=self.project, trace_id=trace_id)

        gapic_api = mock.create_autospec(trace_service_client.TraceServiceClient)
        gapic_api.get_trace.return_value = trace_pb
        api = self._make_one(gapic_api, None)

        trace = api.get_trace(project_id=self.project, trace_id=trace_id)

        expected_trace = {"projectId": self.project, "traceId": trace_id}
        self.assertEqual(trace, expected_trace)

        gapic_api.get_trace.assert_called_with(self.project, trace_id)

    def test_list_traces(self):
        from google.api_core.page_iterator import GRPCIterator
        from google.cloud.trace_v1.gapic import trace_service_client
        from google.cloud.trace_v1.gapic.enums import ListTracesRequest as Enum
        from google.cloud.trace.v1._gapic import _item_to_mapping

        page_size = 10
        view_type = Enum.ViewType.COMPLETE
        page_token = "TOKEN"
        gapic_api = mock.create_autospec(trace_service_client.TraceServiceClient)
        response_iter = mock.create_autospec(GRPCIterator)
        gapic_api.list_traces.return_value = response_iter
        api = self._make_one(gapic_api)

        iterator = api.list_traces(
            project_id=self.project,
            view=view_type,
            page_size=page_size,
            page_token=page_token,
        )

        self.assertIs(iterator, response_iter)
        self.assertIs(iterator.item_to_value, _item_to_mapping)
        self.assertEqual(iterator.next_page_token, page_token)

        gapic_api.list_traces.assert_called_once_with(
            project_id=self.project,
            view=view_type,
            page_size=page_size,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
        )


class _TracePbBase(object):
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

    @classmethod
    def _make_trace_pb(cls):
        from google.cloud.trace_v1.proto.trace_pb2 import Trace
        from google.cloud.trace_v1.proto.trace_pb2 import TraceSpan
        from google.protobuf.timestamp_pb2 import Timestamp

        start_time_pb = Timestamp(seconds=cls.start_seconds, nanos=cls.start_nanos)
        end_time_pb = Timestamp(seconds=cls.end_seconds, nanos=cls.end_nanos)

        span_pb = TraceSpan(
            span_id=cls.span_id,
            name=cls.span_name,
            start_time=start_time_pb,
            end_time=end_time_pb,
        )

        return Trace(project_id=cls.project, trace_id=cls.trace_id, spans=[span_pb])

    @classmethod
    def _expected_json(cls):
        return {
            "projectId": cls.project,
            "traceId": cls.trace_id,
            "spans": [
                {
                    "spanId": str(cls.span_id),
                    "name": cls.span_name,
                    "startTime": cls.start_time,
                    "endTime": cls.end_time,
                }
            ],
        }


class Test__item_to_mapping(unittest.TestCase, _TracePbBase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.trace.v1._gapic import _item_to_mapping

        return _item_to_mapping(*args, **kwargs)

    def test_registered_type(self):
        iterator = object()
        trace_pb = self._make_trace_pb()

        parsed_json = self._call_fut(iterator, trace_pb)

        expected_result = self._expected_json()
        self.assertEqual(parsed_json, expected_result)


class Test__parse_trace_pb(unittest.TestCase, _TracePbBase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.trace.v1._gapic import _parse_trace_pb

        return _parse_trace_pb(*args, **kwargs)

    def test_registered_type(self):
        trace_pb = self._make_trace_pb()

        parsed_json = self._call_fut(trace_pb)

        expected_result = self._expected_json()
        self.assertEqual(parsed_json, expected_result)

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

        client = mock.Mock(spec=["_credentials", "_client_info"])

        patch_api = mock.patch(
            "google.cloud.trace.v1._gapic.trace_service_client.TraceServiceClient"
        )

        with patch_api as patched:
            trace_api = self._call_fut(client)

        patched.assert_called_once_with(
            credentials=client._credentials, client_info=client._client_info
        )

        self.assertIsInstance(trace_api, _TraceAPI)
        self.assertIs(trace_api._gapic_api, patched.return_value)
        self.assertIs(trace_api.client, client)
