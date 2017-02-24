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


class Test_setup_shutdown_stracktrace_reporting(unittest.TestCase):

    def _call_fut(self, request):
        from google.cloud.logging._shutdown import (
            setup_stacktrace_crash_report)
        return setup_stacktrace_crash_report(request)

    def test_setup_shutdown_stacktrace_reporting_no_gae(self):
        with self.assertRaises(RuntimeError):
            self._call_fut(mock.Mock())

    def test_setup_shutdown_stacktrace_reporting(self):
        from google.cloud.logging._environment_vars import (
            _APPENGINE_FLEXIBLE_ENV_VM)
        from google.cloud._testing import _Monkey
        import os

        signal_patch = mock.patch('google.cloud.logging._shutdown.signal')

        with _Monkey(os, environ={_APPENGINE_FLEXIBLE_ENV_VM: 'True'}):
            with signal_patch as signal_mock:
                self._call_fut(mock.Mock())
                self.assertTrue(signal_mock.signal.called)


class Test_write_stackrace_log(unittest.TestCase):

    def _call_fut(self, client, traces):
        from google.cloud.logging._shutdown import (
            _write_stacktrace_log
        )
        return _write_stacktrace_log(client, traces)

    def test_write_stracktrace_log(self):
        from google.cloud._testing import _Monkey
        import os

        mock_client = mock.Mock()

        trace = 'a simple stack trace'
        with _Monkey(os, environ={'GAE_INSTANCE': 'myversion'}):
            self._call_fut(mock_client, trace)
            called = mock_client.logging_api.write_entries.call_args

        expected_payload = 'myversion\nThread traces\n{}'.format(
            trace).encode('utf-8')
        self.assertEqual(called[0][0], [{'text_payload': expected_payload}])


class Test_report_stacktraces(unittest.TestCase):

    def _call_fut(self, client, signal, frame):
        from google.cloud.logging._shutdown import (
            _report_stacktraces
        )
        return _report_stacktraces(client, signal, frame)

    def test_report_stacktraces(self):
        patch = mock.patch(
            'google.cloud.logging._shutdown._write_stacktrace_log')
        with patch as write_log_mock:
            self._call_fut(mock.Mock(), mock.Mock(), mock.Mock())

            traces = write_log_mock.call_args[0][1]
        self.assertIn('test__shutdown', traces)
