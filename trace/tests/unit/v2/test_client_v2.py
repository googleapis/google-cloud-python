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


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    project = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        self.assertEqual(client.project, self.project)

    def test_trace_api(self):
        clients = []
        api_obj = object()

        def make_api(client_obj):
            clients.append(client_obj)
            return api_obj

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)

        patch = mock.patch("google.cloud.trace.client.make_trace_api", new=make_api)

        with patch:
            api = client.trace_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])

    def test_batch_write_spans(self):
        from google.cloud.trace._gapic import _TraceAPI

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        name = "projects/{}".format(self.project)
        spans = "fake_spans_for_test"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.patch_traces = mock.Mock()
        patch = mock.patch(
            "google.cloud.trace.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            client.batch_write_spans(name=name, spans=spans)

        mock_trace_api.batch_write_spans.assert_called_with(
            name=name, spans=spans, retry=None, timeout=None
        )

    def test_create_span(self):
        from google.cloud.trace._gapic import _TraceAPI

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        name = "projects/{}".format(self.project)
        span_id = "1111"
        display_name = "test display name"
        start_time = "test start time"
        end_time = "test end time"
        parent_span_id = "test parent span id"
        attributes = "test attributes"
        stack_trace = "test stack trace"
        time_events = "test time events"
        links = "test links"
        status = "test status"
        same_process_as_parent_span = "test same process as parent span"
        child_span_count = "test child span count"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.patch_traces = mock.Mock()
        patch = mock.patch(
            "google.cloud.trace.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            client.create_span(
                name=name,
                span_id=span_id,
                display_name=display_name,
                start_time=start_time,
                end_time=end_time,
                parent_span_id=parent_span_id,
                attributes=attributes,
                stack_trace=stack_trace,
                time_events=time_events,
                links=links,
                status=status,
                same_process_as_parent_span=same_process_as_parent_span,
                child_span_count=child_span_count,
            )

        mock_trace_api.create_span.assert_called_with(
            name=name,
            span_id=span_id,
            display_name=display_name,
            start_time=start_time,
            end_time=end_time,
            parent_span_id=parent_span_id,
            attributes=attributes,
            stack_trace=stack_trace,
            time_events=time_events,
            links=links,
            status=status,
            same_process_as_parent_span=same_process_as_parent_span,
            child_span_count=child_span_count,
        )
