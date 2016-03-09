# Copyright 2016 Google Inc. All rights reserved.
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

import unittest2


class TestLogger(unittest2.TestCase):

    PROJECT = 'test-project'
    LOGGER_NAME = 'logger-name'

    def _getTargetClass(self):
        from gcloud.logging.logger import Logger
        return Logger

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        conn = _Connection()
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.project, self.PROJECT)
        self.assertEqual(logger.full_name, 'projects/%s/logs/%s'
                         % (self.PROJECT, self.LOGGER_NAME))

    def test_log_text_w_str_implicit_client(self):
        TEXT = 'TEXT'
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        logger.log_text(TEXT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'textPayload': TEXT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_text_w_unicode_explicit_client(self):
        TEXT = u'TEXT'
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        logger.log_text(TEXT, client=client2)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'textPayload': TEXT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_struct_w_implicit_client(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        conn = _Connection({})
        client = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client)
        logger.log_struct(STRUCT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'jsonPayload': STRUCT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)

    def test_log_struct_w_explicit_client(self):
        STRUCT = {'message': 'MESSAGE', 'weather': 'cloudy'}
        conn = _Connection({})
        client1 = _Client(self.PROJECT, object())
        client2 = _Client(self.PROJECT, conn)
        logger = self._makeOne(self.LOGGER_NAME, client=client1)
        logger.log_struct(STRUCT, client=client2)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        SENT = {
            'entries': [{
                'logName': 'projects/%s/logs/%s' % (
                    self.PROJECT, self.LOGGER_NAME),
                'jsonPayload': STRUCT,
                'resource': {
                    'type': 'global',
                },
            }],
        }
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/entries:write')
        self.assertEqual(req['data'], SENT)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection
