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


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.trace.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        self.assertEqual(client.project, self.PROJECT)

    def test_trace_api(self):
        clients = []
        api_obj = object()

        def make_api(client_obj):
            clients.append(client_obj)
            return api_obj

        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)

        patch = mock.patch(
            'google.cloud.trace.client.make_gax_trace_api',
            new=make_api)

        with patch:
            api = client.trace_api

        self.assertIs(api, api_obj)
        self.assertEqual(clients, [client])

    def test_trace(self):
        from google.cloud.trace.trace import Trace

        TRACE_ID = '5e6e73b4131303cb6f5c9dfbaf104e33'
        credentials = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=credentials)
        trace = Trace(client=client, project_id=self.PROJECT, trace_id=TRACE_ID)

        self.assertIsInstance(trace, Trace)
        self.assertIs(trace.client, client)
        self.assertEqual(trace.project_id, self.PROJECT)
        self.assertEqual(trace.trace_id, TRACE_ID)

    def test_patch_traces(self):
        TRACES = 'fake_traces_for_test'
        api = _DummyTraceAPI()

        api.patch_traces(project_id=self.PROJECT, traces=TRACES)
        self.assertEqual(api._patch_traces_called_with, (self.PROJECT, TRACES, None))

    def test_get_trace(self):
        TRACE_ID = '5e6e73b4131303cb6f5c9dfbaf104e33'
        api = _DummyTraceAPI()

        api.get_trace(project_id=self.PROJECT, trace_id=TRACE_ID)
        self.assertEqual(api._get_traces_called_with, (self.PROJECT, TRACE_ID, None))

    def test_list_traces(self):
        api = _DummyTraceAPI()

        api.list_traces(project_id=self.PROJECT)
        api.list_traces(api._list_traces_called_with, (
            self.PROJECT,
            None, None, None, None, None, None, None))


class _DummyTraceAPI(object):
    def patch_traces(self, project_id, traces, options=None):
        self._patch_traces_called_with = (project_id, traces, options)

    def get_trace(self, project_id, trace_id, options=None):
        self._get_traces_called_with = (project_id, trace_id, options)

    def list_traces(
            self,
            project_id,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            page_token=None):
        self._list_traces_called_with = (
            project_id,
            view,
            page_size,
            start_time,
            end_time,
            filter_,
            order_by,
            page_token)
