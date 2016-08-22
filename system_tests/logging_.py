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

import logging
import unittest

import gcloud.logging
import gcloud.logging.handlers.handlers
from gcloud.logging.handlers.handlers import CloudLoggingHandler
from gcloud.logging.handlers.transports import SyncTransport
from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT

from retry import RetryErrors
from retry import RetryResult
from system_test_utils import unique_resource_id

_RESOURCE_ID = unique_resource_id('-')
DEFAULT_METRIC_NAME = 'system-tests-metric%s' % (_RESOURCE_ID,)
DEFAULT_SINK_NAME = 'system-tests-sink%s' % (_RESOURCE_ID,)
DEFAULT_FILTER = 'logName:syslog AND severity>=INFO'
DEFAULT_DESCRIPTION = 'System testing'
BUCKET_NAME = 'gcloud-python-system-testing%s' % (_RESOURCE_ID,)
DATASET_NAME = ('system_testing_dataset' + _RESOURCE_ID).replace('-', '_')
TOPIC_NAME = 'gcloud-python-system-testing%s' % (_RESOURCE_ID,)


def _retry_on_unavailable(exc):
    """Retry only errors whose status code is 'UNAVAILABLE'."""
    from grpc import StatusCode
    return exc.code() == StatusCode.UNAVAILABLE


def _has_entries(result):
    return len(result[0]) > 0


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT
    Config.CLIENT = gcloud.logging.Client()


class TestLogging(unittest.TestCase):

    def setUp(self):
        self.to_delete = []
        self._handlers_cache = logging.getLogger().handlers[:]

    def tearDown(self):
        from gcloud.exceptions import NotFound
        retry = RetryErrors(NotFound)
        for doomed in self.to_delete:
            retry(doomed.delete)()
        logging.getLogger().handlers = self._handlers_cache[:]

    @staticmethod
    def _logger_name():
        return 'system-tests-logger' + unique_resource_id('-')

    def _list_entries(self, logger):
        from grpc._channel import _Rendezvous
        inner = RetryResult(_has_entries)(logger.list_entries)
        outer = RetryErrors(_Rendezvous, _retry_on_unavailable)(inner)
        return outer()

    def test_log_text(self):
        TEXT_PAYLOAD = 'System test: test_log_text'
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)
        logger.log_text(TEXT_PAYLOAD)
        entries, _ = self._list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, TEXT_PAYLOAD)

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
        entries, _ = self._list_entries(logger)

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
        JSON_PAYLOAD = {
            'message': 'System test: test_log_struct',
            'weather': 'partly cloudy',
        }
        logger = Config.CLIENT.logger(self._logger_name())
        self.to_delete.append(logger)

        logger.log_struct(JSON_PAYLOAD)
        entries, _ = self._list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)

    def test_log_handler_async(self):
        LOG_MESSAGE = 'It was the worst of times'

        handler = CloudLoggingHandler(Config.CLIENT)
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        cloud_logger = logging.getLogger(handler.name)
        cloud_logger.addHandler(handler)
        cloud_logger.warn(LOG_MESSAGE)
        entries, _ = self._list_entries(logger)
        JSON_PAYLOAD = {
            'message': LOG_MESSAGE,
            'python_logger': handler.name
        }
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)

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

        entries, _ = self._list_entries(logger)
        JSON_PAYLOAD = {
            'message': LOG_MESSAGE,
            'python_logger': LOGGER_NAME
        }
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)

    def test_log_root_handler(self):
        LOG_MESSAGE = 'It was the best of times.'

        handler = CloudLoggingHandler(Config.CLIENT, name=self._logger_name())
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        gcloud.logging.handlers.handlers.setup_logging(handler)
        logging.warn(LOG_MESSAGE)

        entries, _ = self._list_entries(logger)
        JSON_PAYLOAD = {
            'message': LOG_MESSAGE,
            'python_logger': 'root'
        }

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)

    def test_log_struct_w_metadata(self):
        JSON_PAYLOAD = {
            'message': 'System test: test_log_struct',
            'weather': 'partly cloudy',
        }
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

        logger.log_struct(JSON_PAYLOAD, insert_id=INSERT_ID, severity=SEVERITY,
                          http_request=REQUEST)
        entries, _ = self._list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)
        self.assertEqual(entries[0].insert_id, INSERT_ID)
        self.assertEqual(entries[0].severity, SEVERITY)
        request = entries[0].http_request
        self.assertEqual(request['requestMethod'], METHOD)
        self.assertEqual(request['requestUrl'], URI)
        self.assertEqual(request['status'], STATUS)

    def test_create_metric(self):
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        metric.create()
        self.to_delete.append(metric)
        self.assertTrue(metric.exists())

    def test_list_metrics(self):
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        before_metrics, _ = Config.CLIENT.list_metrics()
        before_names = set(metric.name for metric in before_metrics)
        metric.create()
        self.to_delete.append(metric)
        self.assertTrue(metric.exists())
        after_metrics, _ = Config.CLIENT.list_metrics()
        after_names = set(metric.name for metric in after_metrics)
        self.assertEqual(after_names - before_names,
                         set([DEFAULT_METRIC_NAME]))

    def test_reload_metric(self):
        from gcloud.exceptions import Conflict
        retry = RetryErrors(Conflict)
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry(metric.create)()
        self.to_delete.append(metric)
        metric.filter_ = 'logName:other'
        metric.description = 'local changes'
        metric.reload()
        self.assertEqual(metric.filter_, DEFAULT_FILTER)
        self.assertEqual(metric.description, DEFAULT_DESCRIPTION)

    def test_update_metric(self):
        from gcloud.exceptions import Conflict
        retry = RetryErrors(Conflict)
        NEW_FILTER = 'logName:other'
        NEW_DESCRIPTION = 'updated'
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry(metric.create)()
        self.to_delete.append(metric)
        metric.filter_ = NEW_FILTER
        metric.description = NEW_DESCRIPTION
        metric.update()
        after_metrics, _ = Config.CLIENT.list_metrics()
        after_info = dict((metric.name, metric) for metric in after_metrics)
        after = after_info[DEFAULT_METRIC_NAME]
        self.assertEqual(after.filter_, NEW_FILTER)
        self.assertEqual(after.description, NEW_DESCRIPTION)

    def _init_storage_bucket(self):
        from gcloud import storage
        BUCKET_URI = 'storage.googleapis.com/%s' % (BUCKET_NAME,)

        # Create the destination bucket, and set up the ACL to allow
        # Stackdriver Logging to write into it.
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(BUCKET_NAME)
        self.to_delete.append(bucket)
        bucket.acl.reload()
        logs_group = bucket.acl.group('cloud-logs@google.com')
        logs_group.grant_owner()
        bucket.acl.add_entity(logs_group)
        bucket.acl.save()

        return BUCKET_URI

    def test_create_sink_storage_bucket(self):
        uri = self._init_storage_bucket()

        sink = Config.CLIENT.sink(DEFAULT_SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_create_sink_pubsub_topic(self):
        from gcloud import pubsub

        # Create the destination topic, and set up the IAM policy to allow
        # Stackdriver Logging to write into it.
        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic(TOPIC_NAME)
        topic.create()
        self.to_delete.append(topic)
        policy = topic.get_iam_policy()
        policy.owners.add(policy.group('cloud-logs@google.com'))
        topic.set_iam_policy(policy)

        TOPIC_URI = 'pubsub.googleapis.com/%s' % (topic.full_name,)

        sink = Config.CLIENT.sink(
            DEFAULT_SINK_NAME, DEFAULT_FILTER, TOPIC_URI)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def _init_bigquery_dataset(self):
        from gcloud import bigquery
        from gcloud.bigquery.dataset import AccessGrant
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
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(DEFAULT_SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_list_sinks(self):
        uri = self._init_storage_bucket()
        sink = Config.CLIENT.sink(DEFAULT_SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        before_sinks, _ = Config.CLIENT.list_sinks()
        before_names = set(sink.name for sink in before_sinks)
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())
        after_sinks, _ = Config.CLIENT.list_sinks()
        after_names = set(sink.name for sink in after_sinks)
        self.assertEqual(after_names - before_names,
                         set([DEFAULT_SINK_NAME]))

    def test_reload_sink(self):
        from gcloud.exceptions import Conflict
        retry = RetryErrors(Conflict)
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(DEFAULT_SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = 'BOGUS FILTER'
        sink.destination = 'BOGUS DESTINATION'
        sink.reload()
        self.assertEqual(sink.filter_, DEFAULT_FILTER)
        self.assertEqual(sink.destination, uri)

    def test_update_sink(self):
        from gcloud.exceptions import Conflict
        retry = RetryErrors(Conflict)
        bucket_uri = self._init_storage_bucket()
        dataset_uri = self._init_bigquery_dataset()
        UPDATED_FILTER = 'logName:syslog'
        sink = Config.CLIENT.sink(
            DEFAULT_SINK_NAME, DEFAULT_FILTER, bucket_uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = UPDATED_FILTER
        sink.destination = dataset_uri
        sink.update()
        self.assertEqual(sink.filter_, UPDATED_FILTER)
        self.assertEqual(sink.destination, dataset_uri)
