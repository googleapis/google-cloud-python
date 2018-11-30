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
        from google.cloud.trace.v1.client import Client

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

        patch = mock.patch("google.cloud.trace.v1.client.make_trace_api", new=make_api)

        with patch:
            api = client.trace_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])

    def test_patch_traces_default(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        traces = "fake_traces_for_test"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.patch_traces = mock.Mock()
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            client.patch_traces(traces=traces)

        mock_trace_api.patch_traces.assert_called_with(
            project_id="PROJECT", traces="fake_traces_for_test"
        )

    def test_patch_traces_explicit(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        traces = "fake_traces_for_test"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.patch_traces = mock.Mock()
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            client.patch_traces(project_id=self.project, traces=traces)

        mock_trace_api.patch_traces.assert_called_with(
            project_id="PROJECT", traces="fake_traces_for_test"
        )

    def test_get_trace_default(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        def get_trace(trace_id, project_id=None, options=None):
            _get_trace_called_with = (trace_id, project_id, options)
            return _get_trace_called_with

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        trace_id = "5e6e73b4131303cb6f5c9dfbaf104e33"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.get_trace = get_trace
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            get_trace_called_with = client.get_trace(trace_id=trace_id)

        self.assertEqual(get_trace_called_with, (trace_id, self.project, None))

    def test_get_trace_explicit(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        def get_trace(trace_id, project_id=None, options=None):
            _get_trace_called_with = (trace_id, project_id, options)
            return _get_trace_called_with

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)
        trace_id = "5e6e73b4131303cb6f5c9dfbaf104e33"

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.get_trace = get_trace
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            get_trace_called_with = client.get_trace(
                trace_id=trace_id, project_id=self.project
            )

        self.assertEqual(get_trace_called_with, (trace_id, self.project, None))

    def test_list_traces_default(self):
        from google.cloud.trace.v1._gapic import _TraceAPI

        def list_traces(
            project_id,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            page_token=None,
        ):
            _list_traces_called_with = (
                project_id,
                view,
                page_size,
                start_time,
                end_time,
                filter_,
                order_by,
                page_token,
            )
            return _list_traces_called_with

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.list_traces = list_traces
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        with patch:
            list_traces_called_with = client.list_traces()

        self.assertEqual(
            list_traces_called_with,
            (self.project, None, None, None, None, None, None, None),
        )

    def test_list_traces_explicit(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.trace_v1.gapic.enums import ListTracesRequest as Enum
        from google.cloud.trace.v1._gapic import _TraceAPI

        from datetime import datetime

        def list_traces(
            project_id,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            page_token=None,
        ):
            _list_traces_called_with = (
                project_id,
                view,
                page_size,
                start_time,
                end_time,
                filter_,
                order_by,
                page_token,
            )
            return _list_traces_called_with

        credentials = _make_credentials()
        client = self._make_one(project=self.project, credentials=credentials)

        mock_trace_api = mock.Mock(spec=_TraceAPI)
        mock_trace_api.list_traces = list_traces
        patch = mock.patch(
            "google.cloud.trace.v1.client.make_trace_api", return_value=mock_trace_api
        )

        view = Enum.ViewType.COMPLETE
        page_size = 10
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        filter_ = "+span:span1"
        order_by = "traceId"
        page_token = "TOKEN"

        with patch:
            list_traces_called_with = client.list_traces(
                project_id=self.project,
                view=view,
                page_size=page_size,
                start_time=start_time,
                end_time=end_time,
                filter_=filter_,
                order_by=order_by,
                page_token=page_token,
            )

        self.assertEqual(
            list_traces_called_with,
            (
                self.project,
                view,
                page_size,
                _datetime_to_pb_timestamp(start_time),
                _datetime_to_pb_timestamp(end_time),
                filter_,
                order_by,
                page_token,
            ),
        )
