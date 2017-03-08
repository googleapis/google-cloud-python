# Copyright 2016 Google Inc. All Rights Reserved.
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


class TestAppEngineHandlerHandler(unittest.TestCase):
    PROJECT = 'PROJECT'

    def _get_target_class(self):
        from google.cloud.logging.handlers.app_engine import AppEngineHandler

        return AppEngineHandler

    def _make_one(self, *args, **kw):
        import tempfile

        from google.cloud._testing import _Monkey
        from google.cloud.logging.handlers import app_engine as _MUT

        tmpdir = tempfile.mktemp()
        with _Monkey(_MUT, _LOG_PATH_TEMPLATE=tmpdir):
            return self._get_target_class()(*args, **kw)

    def test_format(self):
        import json
        import logging

        handler = self._make_one()
        logname = 'loggername'
        message = 'hello world'
        record = logging.LogRecord(logname, logging.INFO, None,
                                   None, message, None, None)
        record.created = 5.03
        expected_payload = {
            'message': message,
            'timestamp': {
                'seconds': 5,
                'nanos': int(.03 * 1e9),
            },
            'thread': record.thread,
            'severity': record.levelname,
        }
        payload = handler.format(record)

        self.assertEqual(payload, json.dumps(expected_payload))
