# Copyright 2016 Google LLC
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

from google.api_core.exceptions import BadGateway
from google.api_core.exceptions import Conflict
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import TooManyRequests
from google.api_core.exceptions import ResourceExhausted
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import ServiceUnavailable
from google.cloud._helpers import UTC
import google.cloud.logging
import google.cloud.logging.handlers.handlers
from google.cloud.logging.handlers.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.transports import SyncTransport
from google.cloud.logging import client
from google.cloud.logging.resource import Resource

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id

_RESOURCE_ID = unique_resource_id("-")
DEFAULT_FILTER = "logName:syslog AND severity>=INFO"
DEFAULT_DESCRIPTION = "System testing"
retry_429 = RetryErrors(TooManyRequests)


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
    inner = RetryResult(_has_entries, max_tries=9)(_consume_entries)
    outer = RetryErrors((ServiceUnavailable, ResourceExhausted), max_tries=9)(inner)
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
        "message": "System test: test_log_struct",
        "weather": {
            "clouds": "party or partly",
            "temperature": 70,
            "precipitation": False,
        },
    }
    TYPE_FILTER = 'protoPayload.@type = "{}"'

    def setUp(self):
        self.to_delete = []
        self._handlers_cache = logging.getLogger().handlers[:]

    def tearDown(self):
        retry = RetryErrors((NotFound, TooManyRequests, RetryError), max_tries=9)
        for doomed in self.to_delete:
            try:
                retry(doomed.delete)()
            except AttributeError:
                client, dataset = doomed
                retry(client.delete_dataset)(dataset)
        logging.getLogger().handlers = self._handlers_cache[:]

    @staticmethod
    def _logger_name(prefix):
        return prefix + unique_resource_id("-")

    def test_list_entry_with_unregistered(self):
        from google.protobuf import any_pb2
        from google.protobuf import descriptor_pool
        from google.cloud.logging import entries

        pool = descriptor_pool.Default()
        type_name = "google.cloud.audit.AuditLog"
        # Make sure the descriptor is not known in the registry.
        with self.assertRaises(KeyError):
            pool.FindMessageTypeByName(type_name)

        type_url = "type.googleapis.com/" + type_name
        filter_ = self.TYPE_FILTER.format(type_url)
        entry_iter = iter(Config.CLIENT.list_entries(page_size=1, filter_=filter_))

        retry = RetryErrors(TooManyRequests)
        protobuf_entry = retry(lambda: next(entry_iter))()

        self.assertIsInstance(protobuf_entry, entries.ProtobufEntry)
        if Config.CLIENT._use_grpc:
            self.assertIsNone(protobuf_entry.payload_json)
            self.assertIsInstance(protobuf_entry.payload_pb, any_pb2.Any)
            self.assertEqual(protobuf_entry.payload_pb.type_url, type_url)
        else:
            self.assertIsNone(protobuf_entry.payload_pb)
            self.assertEqual(protobuf_entry.payload_json["@type"], type_url)

    def test_log_text(self):
        TEXT_PAYLOAD = "System test: test_log_text"
        logger = Config.CLIENT.logger(self._logger_name("log_text"))
        self.to_delete.append(logger)
        logger.log_text(TEXT_PAYLOAD)
        entries = _list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, TEXT_PAYLOAD)

    def test_log_text_with_timestamp(self):
        import datetime

        text_payload = "System test: test_log_text_with_timestamp"
        logger = Config.CLIENT.logger(self._logger_name("log_text_ts"))
        now = datetime.datetime.utcnow()

        self.to_delete.append(logger)

        logger.log_text(text_payload, timestamp=now)
        entries = _list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, text_payload)
        self.assertEqual(entries[0].timestamp, now.replace(tzinfo=UTC))
        self.assertIsInstance(entries[0].received_timestamp, datetime.datetime)

    def test_log_text_with_resource(self):
        text_payload = "System test: test_log_text_with_timestamp"

        logger = Config.CLIENT.logger(self._logger_name("log_text_res"))
        now = datetime.datetime.utcnow()
        resource = Resource(
            type="gae_app", labels={"module_id": "default", "version_id": "test"}
        )

        self.to_delete.append(logger)

        logger.log_text(text_payload, timestamp=now, resource=resource)
        entries = _list_entries(logger)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, text_payload)
        # project_id is output only so we don't want it in assertion
        del entries[0].resource.labels["project_id"]
        self.assertEqual(entries[0].resource, resource)

    def test_log_text_w_metadata(self):
        TEXT_PAYLOAD = "System test: test_log_text"
        INSERT_ID = "INSERTID"
        SEVERITY = "INFO"
        METHOD = "POST"
        URI = "https://api.example.com/endpoint"
        STATUS = 500
        REQUEST = {"requestMethod": METHOD, "requestUrl": URI, "status": STATUS}
        logger = Config.CLIENT.logger(self._logger_name("log_text_md"))
        self.to_delete.append(logger)

        logger.log_text(
            TEXT_PAYLOAD, insert_id=INSERT_ID, severity=SEVERITY, http_request=REQUEST
        )
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.payload, TEXT_PAYLOAD)
        self.assertEqual(entry.insert_id, INSERT_ID)
        self.assertEqual(entry.severity, SEVERITY)

        request = entry.http_request
        self.assertEqual(request["requestMethod"], METHOD)
        self.assertEqual(request["requestUrl"], URI)
        self.assertEqual(request["status"], STATUS)

    def test_log_struct(self):
        logger = Config.CLIENT.logger(self._logger_name("log_struct"))
        self.to_delete.append(logger)

        logger.log_struct(self.JSON_PAYLOAD)
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, self.JSON_PAYLOAD)

    def test_log_struct_w_metadata(self):
        INSERT_ID = "INSERTID"
        SEVERITY = "INFO"
        METHOD = "POST"
        URI = "https://api.example.com/endpoint"
        STATUS = 500
        REQUEST = {"requestMethod": METHOD, "requestUrl": URI, "status": STATUS}
        logger = Config.CLIENT.logger(self._logger_name("log_struct_md"))
        self.to_delete.append(logger)

        logger.log_struct(
            self.JSON_PAYLOAD,
            insert_id=INSERT_ID,
            severity=SEVERITY,
            http_request=REQUEST,
        )
        entries = _list_entries(logger)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, self.JSON_PAYLOAD)
        self.assertEqual(entries[0].insert_id, INSERT_ID)
        self.assertEqual(entries[0].severity, SEVERITY)
        request = entries[0].http_request
        self.assertEqual(request["requestMethod"], METHOD)
        self.assertEqual(request["requestUrl"], URI)
        self.assertEqual(request["status"], STATUS)

    def test_log_handler_async(self):
        LOG_MESSAGE = "It was the worst of times"

        handler_name = self._logger_name("handler_async")
        handler = CloudLoggingHandler(Config.CLIENT, name=handler_name)
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler_name)
        self.to_delete.append(logger)

        cloud_logger = logging.getLogger(handler.name)
        cloud_logger.addHandler(handler)
        cloud_logger.warn(LOG_MESSAGE)
        handler.flush()
        entries = _list_entries(logger)
        expected_payload = {"message": LOG_MESSAGE, "python_logger": handler.name}
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_log_handler_sync(self):
        LOG_MESSAGE = "It was the best of times."

        handler_name = self._logger_name("handler_sync")
        handler = CloudLoggingHandler(
            Config.CLIENT, name=handler_name, transport=SyncTransport
        )

        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        LOGGER_NAME = "mylogger"
        cloud_logger = logging.getLogger(LOGGER_NAME)
        cloud_logger.addHandler(handler)
        cloud_logger.warn(LOG_MESSAGE)

        entries = _list_entries(logger)
        expected_payload = {"message": LOG_MESSAGE, "python_logger": LOGGER_NAME}
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_log_root_handler(self):
        LOG_MESSAGE = "It was the best of times."

        handler = CloudLoggingHandler(
            Config.CLIENT, name=self._logger_name("handler_root")
        )
        # only create the logger to delete, hidden otherwise
        logger = Config.CLIENT.logger(handler.name)
        self.to_delete.append(logger)

        google.cloud.logging.handlers.handlers.setup_logging(handler)
        logging.warn(LOG_MESSAGE)

        entries = _list_entries(logger)
        expected_payload = {"message": LOG_MESSAGE, "python_logger": "root"}

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, expected_payload)

    def test_create_metric(self):
        METRIC_NAME = "test-create-metric%s" % (_RESOURCE_ID,)
        metric = Config.CLIENT.metric(METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry = RetryErrors(Conflict)

        retry(metric.create)()

        self.to_delete.append(metric)
        self.assertTrue(metric.exists())

    def test_list_metrics(self):
        METRIC_NAME = "test-list-metrics%s" % (_RESOURCE_ID,)
        metric = Config.CLIENT.metric(METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        before_metrics = list(Config.CLIENT.list_metrics())
        before_names = set(before.name for before in before_metrics)
        self.assertFalse(metric.name in before_names)
        retry = RetryErrors(Conflict)
        retry(metric.create)()
        self.to_delete.append(metric)
        self.assertTrue(metric.exists())

        after_metrics = list(Config.CLIENT.list_metrics())

        after_names = set(after.name for after in after_metrics)
        self.assertTrue(metric.name in after_names)

    def test_reload_metric(self):
        METRIC_NAME = "test-reload-metric%s" % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict)
        metric = Config.CLIENT.metric(METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        retry(metric.create)()
        self.to_delete.append(metric)
        metric.filter_ = "logName:other"
        metric.description = "local changes"

        metric.reload()

        self.assertEqual(metric.filter_, DEFAULT_FILTER)
        self.assertEqual(metric.description, DEFAULT_DESCRIPTION)

    def test_update_metric(self):
        METRIC_NAME = "test-update-metric%s" % (_RESOURCE_ID,)
        retry = RetryErrors(Conflict)
        NEW_FILTER = "logName:other"
        NEW_DESCRIPTION = "updated"
        metric = Config.CLIENT.metric(METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
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

        BUCKET_NAME = "g-c-python-testing%s" % (_RESOURCE_ID,)
        BUCKET_URI = "storage.googleapis.com/%s" % (BUCKET_NAME,)

        # Create the destination bucket, and set up the ACL to allow
        # Stackdriver Logging to write into it.
        retry = RetryErrors((Conflict, TooManyRequests, ServiceUnavailable))
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        retry(bucket.create)()
        self.to_delete.append(bucket)
        bucket.acl.reload()
        logs_group = bucket.acl.group("cloud-logs@google.com")
        logs_group.grant_owner()
        bucket.acl.add_entity(logs_group)
        bucket.acl.save()

        return BUCKET_URI

    def test_create_sink_storage_bucket(self):
        uri = self._init_storage_bucket()
        SINK_NAME = "test-create-sink-bucket%s" % (_RESOURCE_ID,)

        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())

        retry(sink.create)()

        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_create_sink_pubsub_topic(self):
        from google.cloud import pubsub_v1

        SINK_NAME = "test-create-sink-topic%s" % (_RESOURCE_ID,)
        TOPIC_NAME = "logging-systest{}".format(unique_resource_id("-"))

        # Create the destination topic, and set up the IAM policy to allow
        # Stackdriver Logging to write into it.
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(Config.CLIENT.project, TOPIC_NAME)
        self.to_delete.append(_DeleteWrapper(publisher, topic_path))
        publisher.create_topic(topic_path)

        policy = publisher.get_iam_policy(topic_path)
        policy.bindings.add(role="roles/owner", members=["group:cloud-logs@google.com"])
        publisher.set_iam_policy(topic_path, policy)

        TOPIC_URI = "pubsub.googleapis.com/%s" % (topic_path,)

        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, TOPIC_URI)
        self.assertFalse(sink.exists())

        retry(sink.create)()

        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def _init_bigquery_dataset(self):
        from google.cloud import bigquery
        from google.cloud.bigquery.dataset import AccessEntry

        dataset_name = ("system_testing_dataset" + _RESOURCE_ID).replace("-", "_")
        dataset_uri = "bigquery.googleapis.com/projects/%s/datasets/%s" % (
            Config.CLIENT.project,
            dataset_name,
        )

        # Create the destination dataset, and set up the ACL to allow
        # Stackdriver Logging to write into it.
        retry = RetryErrors((TooManyRequests, BadGateway, ServiceUnavailable))
        bigquery_client = bigquery.Client()
        dataset_ref = bigquery_client.dataset(dataset_name)
        dataset = retry(bigquery_client.create_dataset)(bigquery.Dataset(dataset_ref))
        self.to_delete.append((bigquery_client, dataset))
        bigquery_client.get_dataset(dataset)
        access = AccessEntry("WRITER", "groupByEmail", "cloud-logs@google.com")
        dataset.access_entries.append(access)
        bigquery_client.update_dataset(dataset, ["access_entries"])
        return dataset_uri

    def test_create_sink_bigquery_dataset(self):
        SINK_NAME = "test-create-sink-dataset%s" % (_RESOURCE_ID,)
        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())

        retry(sink.create)()

        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_list_sinks(self):
        SINK_NAME = "test-list-sinks%s" % (_RESOURCE_ID,)
        uri = self._init_storage_bucket()
        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        before_sinks = list(Config.CLIENT.list_sinks())
        before_names = set(before.name for before in before_sinks)
        self.assertFalse(sink.name in before_names)
        retry(sink.create)()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

        after_sinks = list(Config.CLIENT.list_sinks())

        after_names = set(after.name for after in after_sinks)
        self.assertTrue(sink.name in after_names)

    def test_reload_sink(self):
        SINK_NAME = "test-reload-sink%s" % (_RESOURCE_ID,)
        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        uri = self._init_bigquery_dataset()
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = "BOGUS FILTER"
        sink.destination = "BOGUS DESTINATION"

        sink.reload()

        self.assertEqual(sink.filter_, DEFAULT_FILTER)
        self.assertEqual(sink.destination, uri)

    def test_update_sink(self):
        SINK_NAME = "test-update-sink%s" % (_RESOURCE_ID,)
        retry = RetryErrors((Conflict, ServiceUnavailable), max_tries=10)
        bucket_uri = self._init_storage_bucket()
        dataset_uri = self._init_bigquery_dataset()
        UPDATED_FILTER = "logName:syslog"
        sink = Config.CLIENT.sink(SINK_NAME, DEFAULT_FILTER, bucket_uri)
        self.assertFalse(sink.exists())
        retry(sink.create)()
        self.to_delete.append(sink)
        sink.filter_ = UPDATED_FILTER
        sink.destination = dataset_uri

        sink.update()

        self.assertEqual(sink.filter_, UPDATED_FILTER)
        self.assertEqual(sink.destination, dataset_uri)


class _DeleteWrapper(object):
    def __init__(self, publisher, topic_path):
        self.publisher = publisher
        self.topic_path = topic_path

    def delete(self):
        self.publisher.delete_topic(self.topic_path)
