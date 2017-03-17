# Copyright 2016 Google Inc.
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

import datetime
import logging
import unittest

from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from grpc import StatusCode

from google.cloud._helpers import UTC
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import TooManyRequests
import google.cloud.logging
import google.cloud.logging.handlers.handlers
from google.cloud.logging.handlers.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.transports import SyncTransport
from google.cloud.logging import client

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id

_RESOURCE_ID = unique_resource_id('-')
DEFAULT_FILTER = 'logName:syslog AND severity>=INFO'
DEFAULT_DESCRIPTION = 'System testing'
retry_429 = RetryErrors(TooManyRequests)


def _retry_on_unavailable(exc):
    """Retry only errors whose status code is 'UNAVAILABLE'.

    :type exc: :class:`~google.gax.errors.GaxError`
    :param exc: The exception that was caught.

    :rtype: bool
    :returns: Boolean indicating if the exception was UNAVAILABLE.
    """
    return exc_to_code(exc) == StatusCode.UNAVAILABLE


def _consume_entries(logger):
    """Consume all log entries from logger iterator.

    :type logger: :class:`~google.cloud.logging.logger.Logger`
    :param logger: A Logger containing entries.

    :rtype: list
    :returns: List of all entries consumed.
    """
    return list(logger.list_entries())


def _list_entries(logger):
    """Retry-ing list entries in a logger.

    Retry until there are actual results and retry on any
    failures.

    :type logger: :class:`~google.cloud.logging.logger.Logger`
    :param logger: A Logger containing entries.

    :rtype: list
    :returns: List of all entries consumed.
    """
    inner = RetryResult(_has_entries)(_consume_entries)
    outer = RetryErrors(GaxError, _retry_on_unavailable)(inner)
    return outer(logger)


def _has_entries(result):
    return len(result) > 0


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    Config.CLIENT = client.Client()


class TestLogging(unittest.TestCase):

    JSON_PAYLOAD = {
        'message': 'System test: test_log_struct',
        'weather': {
            'clouds': 'party or partly',
            'temperature': 70,
            'precipitation': False,
        },
    }

    def setUp(self):
        self.to_delete = []
        self._handlers_cache = logging.getLogger().handlers[:]

    def tearDown(self):
        retry = RetryErrors(NotFound, max_tries=10)
        for doomed in self.to_delete:
            retry(doomed.delete)()
        logging.getLogger().handlers = self._handlers_cache[:]

    @staticmethod
    def _logger_name():
        return 'system-tests-logger' + unique_resource_id('-')

    def test_log_text(self):
        TEXT_PAYLOAD = 'System test: test_log_text'
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)
        logger.log_text(TEXT_PAYLOAD)
        entries = _list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, TEXT_PAYLOAD)

    def test_log_text_with_timestamp(self):
        text_payload = 'System test: test_log_text_with_timestamp'
        logger = Config.CLIENT.logger(self._logger_name())
        now = datetime.datetime.utcnow()

        self.to_delete.append(logger)

        logger.log_text(text_payload, timestamp=now)
        entries = _list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, text_payload)
        self.assertEqual(entries[0].timestamp, now.replace(tzinfo=UTC))

    def test_log_text_w_metadata(self):
        TEXT_PAYLOAD = 'System test: test_log_text'
        INSERT_ID = 'INSERTID'
        SEVERITY = 'INFO'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = 500
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)

        logger.log_text(TEXT_PAYLOAD, insert_id=INSERT_ID, severity=SEVERITY,
                        http_request=REQUEST)
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.payload, TEXT_PAYLOAD)
        self.assertEqual(entry.insert_id, INSERT_ID)
        self.assertEqual(entry.severity, SEVERITY)

        request = entry.http_request
        self.assertEqual(request['requestMethod'], METHOD)
        self.assertEqual(request['requestUrl'], URI)
        self.assertEqual(request['status'], STATUS)

    def test_log_struct(self):
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)

        logger.log_struct(self.JSON_PAYLOAD)
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, self.JSON_PAYLOAD)

    def test_log_handler_async(self):
        LOG_MESSAGE = 'It was the worst of times'

        handler = CloudLoggingHandler(Config.CLIENT)
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        cloud_logger = logging.getLogger(handler.name)
        cloud_logger.addHandler(handler)
        cloud_logger.warn(LOG_MESSAGE)
        entries = _list_entries(logger)
        expected_payload = {
            'message': LOG_MESSAGE,
            'python_logger': handler.name
        }
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_log_handler_sync(self):
        LOG_MESSAGE = 'It was the best of times.'

        handler = CloudLoggingHandler(Config.CLIENT,
                                      name=self._logger_name(),
                                      transport=SyncTransport)

        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        LOGGER_NAME = 'mylogger'
        cloud_logger = logging.getLogger(LOGGER_NAME)
        cloud_logger.addHandler(handler)
        cloud_logger.warn(LOG_MESSAGE)

        entries = _list_entries(logger)
        expected_payload = {
            'message': LOG_MESSAGE,
            'python_logger': LOGGER_NAME
        }
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_log_root_handler(self):
        LOG_MESSAGE = 'It was the best of times.'

        handler = CloudLoggingHandler(Config.CLIENT, name=self._logger_name())
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        google.cloud.logging.handlers.handlers.setup_logging(handler)
        logging.warn(LOG_MESSAGE)

        entries = _list_entries(logger)
        expected_payload = {
            'message': LOG_MESSAGE,
            'python_logger': 'root'
        }

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_log_struct_w_metadata(self):
        INSERT_ID = 'INSERTID'
        SEVERITY = 'INFO'
        METHOD = 'POST'
        URI = 'https://api.example.com/endpoint'
        STATUS = 500
        REQUEST = {
            'requestMethod': METHOD,
            'requestUrl': URI,
            'status': STATUS,
        }
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)

        logger.log_struct(self.JSON_PAYLOAD, insert_id=INSERT_ID,
                          severity=SEVERITY, http_request=REQUEST)
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, self.JSON_PAYLOAD)
        self.assertEqual(entries[0].insert_id, INSERT_ID)
        self.assertEqual(entries[0].severity, SEVERITY)
        request = entries[0].http_request
        self.assertEqual(request['requestMethod'], METHOD)
        self.assertEqual(request['requestUrl'], URI)
        self.assertEqual(request['status'], STATUS)

    def test_create_metric(self):
        METRIC_NAME = 'test-create-metric%s' % (_RESOURCE_ID,)
        metric = Config.CLIENT.metric(
            METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        metric.create()
        self.to_delete.append(metric)
        self.assertTrue(metric.exists())

    def test_list_metrics(self):
        METRIC_NAME = 'test-list-metrics%s' % (_RESOURCE_ID,)
        metric = Config.CLIENT.metric(
            METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        before_metrics = list(Config.CLIENT.list_metrics())
        before_names = set(metric.name for metric in before_metrics)
        metric.create()
        self.to_delete.append(metric)
        self.assertTrue(metric.exists())
        after_metrics = list(Config.CLIENT.list_metrics())
        after_names = set(metric.name for metric in after_metrics)
        self.assertEqual(after_names - before_names,
                         set([METRIC_NAME]))

    def test_reload_metric(self):
        METRIC_NAME = 'test-reload-metric%s' % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict)
        metric = Config.CLIENT.metric(
            METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry(metric.create)()
        self.to_delete.append(metric)
        metric.filter_ = 'logName:other'
        metric.description = 'local changes'
        metric.reload()
        self.assertEqual(metric.filter_, DEFAULT_FILTER)
        self.assertEqual(metric.description, DEFAULT_DESCRIPTION)

    def test_update_metric(self):
        METRIC_NAME = 'test-update-metric%s' % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict)
        NEW_FILTER = 'logName:other'
        NEW_DESCRIPTION = 'updated'
        metric = Config.CLIENT.metric(
            METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry(metric.create)()
        self.to_delete.append(metric)
        metric.filter_ = NEW_FILTER
        metric.description = NEW_DESCRIPTION
        metric.update()
        after_metrics = list(Config.CLIENT.list_metrics())
        after_info = {metric.name: metric for metric in after_metrics}
        after = after_info[METRIC_NAME]
        self.assertEqual(after.filter_, NEW_FILTER)
        self.assertEqual(after.description, NEW_DESCRIPTION)

    def _init_storage_bucket(self):
        from google.cloud import storage
        BUCKET_NAME = 'g-c-python-testing%s' % (_RESOURCE_ID,)
        BUCKET_URI = 'storage.googleapis.com/%s' % (BUCKET_NAME,)

        # Create the destination bucket, and set up the ACL to allow
        # Stackdriver Logging to write into it.
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        retry_429(bucket.create)()
        self.to_delete.append(bucket)
        bucket.acl.reload()
        logs_group = bucket.acl.group('cloud-logs@google.com')
        logs_group.grant_owner()
        bucket.acl.add_entity(logs_group)
        bucket.acl.save()

        return BUCKET_URI

    def test_create_sink_storage_bucket(self):
        uri = self._init_storage_bucket()
        SINK_NAME = 'test-create-sink-bucket%s' % (_RESOURCE_ID,)

        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_create_sink_pubsub_topic(self):
        from google.cloud.pubsub import client as pubsub_client
        SINK_NAME = 'test-create-sink-topic%s' % (_RESOURCE_ID,)
        TOPIC_NAME = 'logging-test-sink%s' % (_RESOURCE_ID,)

        # Create the destination topic, and set up the IAM policy to allow
        # Stackdriver Logging to write into it.
        pubsub_client = pubsub_client.Client()
        topic = pubsub_client.topic(TOPIC_NAME)
        topic.create()
        self.to_delete.append(topic)
        policy = topic.get_iam_policy()
        policy.owners.add(policy.group('cloud-logs@google.com'))
        topic.set_iam_policy(policy)

        TOPIC_URI = 'pubsub.googleapis.com/%s' % (topic.full_name,)

        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, TOPIC_URI)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def _init_bigquery_dataset(self):
        from google.cloud import bigquery
        from google.cloud.bigquery.dataset import AccessGrant
        DATASET_NAME = (
            'system_testing_dataset' + _RESOURCE_ID).replace('-', '_')
        DATASET_URI = 'bigquery.googleapis.com/projects/%s/datasets/%s' % (
            Config.CLIENT.project, DATASET_NAME,)

        # Create the destination dataset, and set up the ACL to allow
        # Stackdriver Logging to write into it.
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset(DATASET_NAME)
        dataset.create()
        self.to_delete.append(dataset)
        dataset.reload()
        grants = dataset.access_grants
        grants.append(AccessGrant(
            'WRITER', 'groupByEmail', 'cloud-logs@google.com'))
        dataset.access_grants = grants
        dataset.update()
        return DATASET_URI

    def test_create_sink_bigquery_dataset(self):
        SINK_NAME = 'test-create-sink-dataset%s' % (_RESOURCE_ID,)
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_list_sinks(self):
        SINK_NAME = 'test-list-sinks%s' % (_RESOURCE_ID,)
        uri = self._init_storage_bucket()
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        before_sinks = list(Config.CLIENT.list_sinks())
        before_names = set(sink.name for sink in before_sinks)
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())
        after_sinks = list(Config.CLIENT.list_sinks())
        after_names = set(sink.name for sink in after_sinks)
        self.assertEqual(after_names - before_names,
                         set([SINK_NAME]))

    def test_reload_sink(self):
        SINK_NAME = 'test-reload-sink%s' % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict)
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = 'BOGUS FILTER'
        sink.destination = 'BOGUS DESTINATION'
        sink.reload()
        self.assertEqual(sink.filter_, DEFAULT_FILTER)
        self.assertEqual(sink.destination, uri)

    def test_update_sink(self):
        SINK_NAME = 'test-update-sink%s' % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict, max_tries=10)
        bucket_uri = self._init_storage_bucket()
        dataset_uri = self._init_bigquery_dataset()
        UPDATED_FILTER = 'logName:syslog'
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, bucket_uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = UPDATED_FILTER
        sink.destination = dataset_uri
        sink.update()
        self.assertEqual(sink.filter_, UPDATED_FILTER)
        self.assertEqual(sink.destination, dataset_uri)
