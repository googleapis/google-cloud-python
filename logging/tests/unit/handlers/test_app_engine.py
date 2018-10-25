# Copyright 2016 Google LLC All Rights Reserved.
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

import mock


class TestAppEngineHandler(unittest.TestCase):
    PROJECT = 'PROJECT'

    def _get_target_class(self):
        from google.cloud.logging.handlers.app_engine import AppEngineHandler

        return AppEngineHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        from google.cloud.logging.handlers.app_engine import (
            _GAE_PROJECT_ENV_FLEX)
        from google.cloud.logging.handlers.app_engine import (
            _GAE_PROJECT_ENV_STANDARD)
        from google.cloud.logging.handlers.app_engine import _GAE_SERVICE_ENV
        from google.cloud.logging.handlers.app_engine import _GAE_VERSION_ENV

        client = mock.Mock(project=self.PROJECT, spec=['project'])

        # Verify that project/service/version are picked up from the
        # environment.
        with mock.patch('os.environ', new={
            _GAE_PROJECT_ENV_STANDARD: 'test_project',
            _GAE_SERVICE_ENV: 'test_service',
            _GAE_VERSION_ENV: 'test_version',
        }):
            handler = self._make_one(client, transport=_Transport)
        self.assertIs(handler.client, client)
        self.assertEqual(handler.resource.type, 'gae_app')
        self.assertEqual(handler.resource.labels['project_id'], 'test_project')
        self.assertEqual(handler.resource.labels['module_id'], 'test_service')
        self.assertEqual(handler.resource.labels['version_id'], 'test_version')

        # Verify that _GAE_PROJECT_ENV_FLEX environment variable takes
        # precedence over _GAE_PROJECT_ENV_STANDARD.
        with mock.patch('os.environ', new={
            _GAE_PROJECT_ENV_FLEX: 'test_project_2',
            _GAE_PROJECT_ENV_STANDARD: 'test_project_should_be_overridden',
            _GAE_SERVICE_ENV: 'test_service_2',
            _GAE_VERSION_ENV: 'test_version_2',
        }):
            handler = self._make_one(client, transport=_Transport)
        self.assertIs(handler.client, client)
        self.assertEqual(handler.resource.type, 'gae_app')
        self.assertEqual(
            handler.resource.labels['project_id'], 'test_project_2')
        self.assertEqual(
            handler.resource.labels['module_id'], 'test_service_2')
        self.assertEqual(
            handler.resource.labels['version_id'], 'test_version_2')

    def test_emit(self):
        client = mock.Mock(project=self.PROJECT, spec=['project'])
        handler = self._make_one(client, transport=_Transport)
        gae_resource = handler.get_gae_resource()
        gae_labels = handler.get_gae_labels()
        trace = None
        logname = 'app'
        message = 'hello world'
        record = logging.LogRecord(logname, logging, None, None, message,
                                   None, None)
        handler.emit(record)

        self.assertIs(handler.transport.client, client)
        self.assertEqual(handler.transport.name, logname)
        self.assertEqual(
            handler.transport.send_called_with,
            (record, message, gae_resource, gae_labels, trace))

    def _get_gae_labels_helper(self, trace_id):
        get_trace_patch = mock.patch(
            'google.cloud.logging.handlers.app_engine.get_trace_id',
            return_value=trace_id)

        client = mock.Mock(project=self.PROJECT, spec=['project'])
        # The handler actually calls ``get_gae_labels()``.
        with get_trace_patch as mock_get_trace:
            handler = self._make_one(client, transport=_Transport)

            gae_labels = handler.get_gae_labels()
            self.assertEqual(mock_get_trace.mock_calls,
                             [mock.call()])

        return gae_labels

    def test_get_gae_labels_with_label(self):
        from google.cloud.logging.handlers import app_engine

        trace_id = 'test-gae-trace-id'
        gae_labels = self._get_gae_labels_helper(trace_id)
        expected_labels = {app_engine._TRACE_ID_LABEL: trace_id}
        self.assertEqual(gae_labels, expected_labels)

    def test_get_gae_labels_without_label(self):
        gae_labels = self._get_gae_labels_helper(None)
        self.assertEqual(gae_labels, {})


class _Transport(object):

    def __init__(self, client, name):
        self.client = client
        self.name = name

    def send(self, record, message, resource, labels, trace):
        self.send_called_with = (record, message, resource, labels, trace)
