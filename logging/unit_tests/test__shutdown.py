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


class Test_setup_stacktrace_crash_report(unittest.TestCase):

    def _call_fut(self, request):
        from google.cloud.logging._shutdown import (
            setup_stacktrace_crash_report)
        return setup_stacktrace_crash_report(request)

    def test_outside_of_gae(self):
        is_on_gae_patch = mock.patch(
            'google.cloud.logging._shutdown._is_on_appengine',
            return_value=False)
        with is_on_gae_patch:
            with self.assertRaises(RuntimeError):
                self._call_fut(mock.sentinel.client)

    def test_success(self):
        import signal
        from google.cloud.logging._environment_vars import (
            APPENGINE_FLEXIBLE_ENV_VM)

        signal_patch = mock.patch('google.cloud.logging._shutdown.signal')
        environ_patch = mock.patch(
            'os.environ',
            new={APPENGINE_FLEXIBLE_ENV_VM: 'True'})

        with environ_patch:
            with signal_patch as signal_mock:
                signal_mock.SIGTERM = signal.SIGTERM
                self._call_fut(mock.sentinel.client)
                self.assertTrue(signal_mock.signal.called)
                positional = signal_mock.signal.call_args[0]
                self.assertEqual(positional[0], signal.SIGTERM)
                self.assertTrue(callable(type(positional[1])))


class Test_write_stackrace_log(unittest.TestCase):

    def _call_fut(self, client, traces):
        from google.cloud.logging._shutdown import (_write_stacktrace_log)
        return _write_stacktrace_log(client, traces)

    def test_write_stracktrace_log(self):
        from google.cloud.logging._gax import _LoggingAPI

        mock_client = mock.Mock(spec=['project'])
        mock_client.logging_api = mock.Mock(spec=_LoggingAPI)

        trace = 'a simple stack trace'
        environ_patch = mock.patch(
            'os.environ', new={'GAE_INSTANCE': 'myversion'})
        with environ_patch:
            self._call_fut(mock_client, trace)
            self.assertEqual(
                len(mock_client.logging_api.write_entries.mock_calls), 1)
            positional, _ = mock_client.logging_api.write_entries.call_args
        expected_payload = 'myversion\nThread traces\n{}'.format(
            trace).encode('utf-8')
        self.assertEqual(positional[0], [{'text_payload': expected_payload}])


class Test__report_stacktraces(unittest.TestCase):

    def _call_fut(self, client, signal, frame):
        from google.cloud.logging._shutdown import (
            _report_stacktraces
        )
        return _report_stacktraces(client, signal, frame)

    def test_success(self):
        import re
        patch = mock.patch(
            'google.cloud.logging._shutdown._write_stacktrace_log')
        with patch as write_log_mock:
            self._call_fut(mock.sentinel.client, None, None)

            traces = write_log_mock.call_args[0][1]

        match = re.match(
            '.*ThreadID: .*File:.*test__shutdown.*',
            traces,
            re.DOTALL)
        self.assertIsNotNone(match)
