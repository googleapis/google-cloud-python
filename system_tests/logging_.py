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

import time

import unittest2

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import logging


_MILLIS = 1000 * time.time()
DEFAULT_LOGGER_NAME = 'system-tests-logger-%d' % (_MILLIS,)
DEFAULT_METRIC_NAME = 'system-tests-metric-%d' % (_MILLIS,)
DEFAULT_SINK_NAME = 'system-tests-sink-%d' % (_MILLIS,)
DEFAULT_FILTER = 'logName:syslog AND severity>=INFO'
DEFAULT_DESCRIPTION = 'System testing'
BUCKET_NAME = 'gcloud-python-system-testing-%d' % (_MILLIS,)
DATASET_NAME = 'system_testing_dataset_%d' % (_MILLIS,)
TOPIC_NAME = 'gcloud-python-system-testing-%d' % (_MILLIS,)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT
    Config.CLIENT = logging.Client()


class TestLogging(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_log_text(self):
        TEXT_PAYLOAD = 'System test: test_log_text'
        logger = Config.CLIENT.logger(DEFAULT_LOGGER_NAME)
        self.to_delete.append(logger)
        logger.log_text(TEXT_PAYLOAD)
        time.sleep(2)
        entries, _ = logger.list_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, TEXT_PAYLOAD)

    def test_log_struct(self):
        JSON_PAYLOAD = {
            'message': 'System test: test_log_struct',
            'weather': 'partly cloudy',
        }
        logger = Config.CLIENT.logger(DEFAULT_LOGGER_NAME)
        self.to_delete.append(logger)
        logger.log_struct(JSON_PAYLOAD)
        time.sleep(2)
        entries, _ = logger.list_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)

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
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        metric.create()
        self.to_delete.append(metric)
        metric.filter_ = 'logName:other'
        metric.description = 'local changes'
        metric.reload()
        self.assertEqual(metric.filter_, DEFAULT_FILTER)
        self.assertEqual(metric.description, DEFAULT_DESCRIPTION)

    def test_update_metric(self):
        NEW_FILTER = 'logName:other'
        NEW_DESCRIPTION = 'updated'
        metric = Config.CLIENT.metric(
            DEFAULT_METRIC_NAME, DEFAULT_FILTER, DEFAULT_DESCRIPTION)
        self.assertFalse(metric.exists())
        metric.create()
        self.to_delete.append(metric)
        metric.filter_ = NEW_FILTER
        metric.description = NEW_DESCRIPTION
        metric.update()
        after_metrics, _ = Config.CLIENT.list_metrics()
        after_info = dict((metric.name, metric) for metric in after_metrics)
        after = after_info[DEFAULT_METRIC_NAME]
        self.assertEqual(after.filter_, NEW_FILTER)
        self.assertEqual(after.description, NEW_DESCRIPTION)

    def test_create_sink_storage_bucket(self):
        from gcloud import storage
        BUCKET_URI = 'storage.googleapis.com/%s' % (BUCKET_NAME,)

        # Create the destination bucket, and set up the ACL to allow
        # Cloud Logging to write into it.
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(BUCKET_NAME)
        self.to_delete.append(bucket)
        bucket.acl.reload()
        logs_group = bucket.acl.group('cloud-logs@google.com')
        logs_group.grant_owner()
        bucket.acl.add_entity(logs_group)
        bucket.acl.save()

        sink = Config.CLIENT.sink(
            DEFAULT_SINK_NAME, DEFAULT_FILTER, BUCKET_URI)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_create_sink_bigquery_dataset(self):
        from gcloud import bigquery
        from gcloud.bigquery.dataset import AccessGrant
        DATASET_URI = 'bigquery.googleapis.com/projects/%s/datasets/%s' % (
            Config.CLIENT.project, DATASET_NAME,)

        # Create the destination dataset, and set up the ACL to allow
        # Cloud Logging to write into it.
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

        sink = Config.CLIENT.sink(
            DEFAULT_SINK_NAME, DEFAULT_FILTER, DATASET_URI)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())

    def test_create_sink_pubsub_topic(self):
        from gcloud import pubsub
        TOPIC_URI = 'pubsub.googleapis.com/projects/%s/topic/%s' % (
            Config.CLIENT.project, TOPIC_NAME)

        # Create the destination topic, and set up the IAM policy to allow
        # Cloud Logging to write into it.
        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic(TOPIC_NAME)
        topic.create()
        self.to_delete.append(topic)
        policy = topic.get_iam_policy()
        policy.owners.add(policy.group('cloud-logs@google.com'))
        topic.set_iam_policy(policy)

        sink = Config.CLIENT.sink(
            DEFAULT_SINK_NAME, DEFAULT_FILTER, TOPIC_URI)
        self.assertFalse(sink.exists())
        sink.create()
        self.to_delete.append(sink)
        self.assertTrue(sink.exists())
