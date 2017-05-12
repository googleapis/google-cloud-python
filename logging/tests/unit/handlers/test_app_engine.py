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
from google.cloud.logging.resource import Resource


class TestAppEngineHandlerHandler(unittest.TestCase):
    PROJECT = 'PROJECT'

    def _get_target_class(self):
        from google.cloud.logging.handlers.app_engine import AppEngineHandler

        return AppEngineHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        handler = self._make_one(client, transport=_Transport)
        self.assertEqual(handler.client, client)

    def test_emit(self):
        RESOURCE = Resource(
            type='gae_app',
            labels={
                'module_id': 'default',
                'version_id': 'test',
        })

        client = _Client(self.PROJECT)
        handler = self._make_one(client, transport=_Transport, resource=RESOURCE)
        logname = 'loggername'
        message = 'hello world'
        record = logging.LogRecord(logname, logging, None, None, message,
                                   None, None)
        handler.emit(record)

        self.assertEqual(handler.transport.send_called_with, (record, message, RESOURCE))


class _Client(object):

    def __init__(self, project):
        self.project = project


class _Transport(object):

    def __init__(self, client, name):
        pass

    def send(self, record, message, resource):
        self.send_called_with = (record, message, resource)