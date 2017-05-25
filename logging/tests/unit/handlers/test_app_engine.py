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

import logging
import unittest


class TestAppEngineHandlerHandler(unittest.TestCase):
    PROJECT = 'PROJECT'

    def _get_target_class(self):
        from google.cloud.logging.handlers.app_engine import AppEngineHandler

        return AppEngineHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        import mock
        from google.cloud.logging.handlers.app_engine import _GAE_PROJECT_ENV
        from google.cloud.logging.handlers.app_engine import _GAE_SERVICE_ENV
        from google.cloud.logging.handlers.app_engine import _GAE_VERSION_ENV
        from google.cloud.logging.handlers._helpers import _EMPTY_TRACE_ID

        TRACE_ID_LABEL = 'appengine.googleapis.com/trace_id'

        client = mock.Mock(project=self.PROJECT, spec=['project'])

        with mock.patch('os.environ', new={_GAE_PROJECT_ENV: 'test_project',
                                           _GAE_SERVICE_ENV: 'test_service',
                                           _GAE_VERSION_ENV: 'test_version'}):
            handler = self._make_one(client, transport=_Transport)
        self.assertIs(handler.client, client)
        self.assertEqual(handler.resource.type, 'gae_app')
        self.assertEqual(handler.resource.labels['project_id'], 'test_project')
        self.assertEqual(handler.resource.labels['module_id'], 'test_service')
        self.assertEqual(handler.resource.labels['version_id'], 'test_version')
        self.assertEqual(handler.labels[TRACE_ID_LABEL], _EMPTY_TRACE_ID)

    def test_emit(self):
        import mock

        client = mock.Mock(project=self.PROJECT, spec=['project'])
        handler = self._make_one(client, transport=_Transport)
        gae_resource = handler.get_gae_resource()
        gae_labels = handler.get_gae_labels()
        logname = 'app'
        message = 'hello world'
        record = logging.LogRecord(logname, logging, None, None, message,
                                   None, None)
        handler.emit(record)

        self.assertIs(handler.transport.client, client)
        self.assertEqual(handler.transport.name, logname)
        self.assertEqual(
            handler.transport.send_called_with,
            (record, message, gae_resource, gae_labels))


class _Transport(object):

    def __init__(self, client, name):
        self.client = client
        self.name = name

    def send(self, record, message, resource, labels):
        self.send_called_with = (record, message, resource, labels)
