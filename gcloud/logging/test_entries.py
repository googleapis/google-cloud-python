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


class TestTextEntry(unittest2.TestCase):

    PROJECT = 'PROJECT'
    LOGGER_NAME = 'LOGGER_NAME'

    def _getTargetClass(self):
        from gcloud.logging.entries import TextEntry
        return TextEntry

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        PAYLOAD = 'PAYLOAD'
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)

    def test_ctor_explicit(self):
        import datetime
        PAYLOAD = 'PAYLOAD'
        IID = 'IID'
        TIMESTAMP = datetime.datetime.now()
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger, IID, TIMESTAMP)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, TIMESTAMP)

    def test_from_api_repr_missing_data_no_loggers(self):
        client = _Client(self.PROJECT)
        PAYLOAD = 'PAYLOAD'
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'textPayload': PAYLOAD,
            'logName': LOG_NAME,
        }
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)

    def test_from_api_repr_w_loggers_no_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = 'PAYLOAD'
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'textPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        loggers = {}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertEqual(loggers, {LOG_NAME: logger})

    def test_from_api_repr_w_loggers_w_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = 'PAYLOAD'
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'textPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        LOGGER = object()
        loggers = {LOG_NAME: LOGGER}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        self.assertTrue(entry.logger is LOGGER)


class TestStructEntry(unittest2.TestCase):

    PROJECT = 'PROJECT'
    LOGGER_NAME = 'LOGGER_NAME'

    def _getTargetClass(self):
        from gcloud.logging.entries import StructEntry
        return StructEntry

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)

    def test_ctor_explicit(self):
        import datetime
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        TIMESTAMP = datetime.datetime.now()
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger, IID, TIMESTAMP)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, TIMESTAMP)

    def test_from_api_repr_missing_data_no_loggers(self):
        client = _Client(self.PROJECT)
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'jsonPayload': PAYLOAD,
            'logName': LOG_NAME,
        }
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)

    def test_from_api_repr_w_loggers_no_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'jsonPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        loggers = {}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertEqual(loggers, {LOG_NAME: logger})

    def test_from_api_repr_w_loggers_w_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = {'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'jsonPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        LOGGER = object()
        loggers = {LOG_NAME: LOGGER}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        self.assertTrue(entry.logger is LOGGER)


class TestProtobufEntry(unittest2.TestCase):

    PROJECT = 'PROJECT'
    LOGGER_NAME = 'LOGGER_NAME'

    def _getTargetClass(self):
        from gcloud.logging.entries import ProtobufEntry
        return ProtobufEntry

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        PAYLOAD = {'@type': 'type.googleapis.com/testing.example',
                   'message': 'MESSAGE', 'weather': 'partly cloudy'}
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)

    def test_ctor_explicit(self):
        import datetime
        PAYLOAD = {'@type': 'type.googleapis.com/testing.example',
                   'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        TIMESTAMP = datetime.datetime.now()
        logger = _Logger(self.LOGGER_NAME, self.PROJECT)
        entry = self._makeOne(PAYLOAD, logger, IID, TIMESTAMP)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.logger is logger)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, TIMESTAMP)

    def test_from_api_repr_missing_data_no_loggers(self):
        client = _Client(self.PROJECT)
        PAYLOAD = {'@type': 'type.googleapis.com/testing.example',
                   'message': 'MESSAGE', 'weather': 'partly cloudy'}
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'protoPayload': PAYLOAD,
            'logName': LOG_NAME,
        }
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertTrue(entry.insert_id is None)
        self.assertTrue(entry.timestamp is None)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)

    def test_from_api_repr_w_loggers_no_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = {'@type': 'type.googleapis.com/testing.example',
                   'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'protoPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        loggers = {}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        logger = entry.logger
        self.assertTrue(isinstance(logger, _Logger))
        self.assertTrue(logger.client is client)
        self.assertEqual(logger.name, self.LOGGER_NAME)
        self.assertEqual(loggers, {LOG_NAME: logger})

    def test_from_api_repr_w_loggers_w_logger_match(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        client = _Client(self.PROJECT)
        PAYLOAD = {'@type': 'type.googleapis.com/testing.example',
                   'message': 'MESSAGE', 'weather': 'partly cloudy'}
        IID = 'IID'
        NOW = datetime.utcnow().replace(tzinfo=UTC)
        TIMESTAMP = _datetime_to_rfc3339_w_nanos(NOW)
        LOG_NAME = 'projects/%s/logs/%s' % (self.PROJECT, self.LOGGER_NAME)
        API_REPR = {
            'protoPayload': PAYLOAD,
            'logName': LOG_NAME,
            'insertId': IID,
            'timestamp': TIMESTAMP,
        }
        LOGGER = object()
        loggers = {LOG_NAME: LOGGER}
        klass = self._getTargetClass()
        entry = klass.from_api_repr(API_REPR, client, loggers=loggers)
        self.assertEqual(entry.payload, PAYLOAD)
        self.assertEqual(entry.insert_id, IID)
        self.assertEqual(entry.timestamp, NOW)
        self.assertTrue(entry.logger is LOGGER)


def _datetime_to_rfc3339_w_nanos(value):
    from gcloud._helpers import _RFC3339_NO_FRACTION
    no_fraction = value.strftime(_RFC3339_NO_FRACTION)
    return '%s.%09dZ' % (no_fraction, value.microsecond * 1000)


class _Logger(object):

    def __init__(self, name, client):
        self.name = name
        self.client = client


class _Client(object):

    def __init__(self, project):
        self.project = project

    def logger(self, name):
        return _Logger(name, self)
