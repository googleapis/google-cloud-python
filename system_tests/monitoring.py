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

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import monitoring


METRIC_TYPE = 'pubsub.googleapis.com/topic/send_message_operation_count'
METRIC_KIND = monitoring.MetricKind.DELTA
VALUE_TYPE = monitoring.ValueType.INT64

RESOURCE_TYPE = 'pubsub_topic'


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT


class TestMonitoring(unittest2.TestCase):

    def test_fetch_metric_descriptor(self):
        client = monitoring.Client()
        descriptor = client.fetch_metric_descriptor(METRIC_TYPE)

        expected_name = 'projects/{project}/metricDescriptors/{type}'.format(
            project=client.project,
            type=METRIC_TYPE,
        )
        self.assertEqual(descriptor.name, expected_name)
        self.assertEqual(descriptor.type, METRIC_TYPE)
        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)
        self.assertTrue(descriptor.description)

        self.assertTrue(descriptor.labels)
        for label in descriptor.labels:
            self.assertTrue(label.key)
            self.assertTrue(label.value_type)
            self.assertTrue(label.description)

    def test_list_metric_descriptors(self):
        client = monitoring.Client()

        descriptor = None
        for item in client.list_metric_descriptors():
            if item.type == METRIC_TYPE:
                descriptor = item

        self.assertIsNotNone(descriptor)

        expected_name = 'projects/{project}/{what}/{type}'.format(
            project=client.project,
            what='metricDescriptors',
            type=METRIC_TYPE,
        )
        self.assertEqual(descriptor.name, expected_name)
        self.assertEqual(descriptor.type, METRIC_TYPE)
        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)
        self.assertTrue(descriptor.description)

        self.assertTrue(descriptor.labels)
        for label in descriptor.labels:
            self.assertTrue(label.key)
            self.assertTrue(label.value_type)
            self.assertTrue(label.description)

    def test_fetch_resource_descriptor(self):
        client = monitoring.Client()
        descriptor = client.fetch_resource_descriptor(RESOURCE_TYPE)

        expected_name = 'projects/{project}/{what}/{type}'.format(
            project=client.project,
            what='monitoredResourceDescriptors',
            type=RESOURCE_TYPE,
        )
        self.assertEqual(descriptor.name, expected_name)
        self.assertEqual(descriptor.type, RESOURCE_TYPE)
        self.assertTrue(descriptor.display_name)
        self.assertTrue(descriptor.description)

        self.assertTrue(descriptor.labels)
        for label in descriptor.labels:
            self.assertTrue(label.key)
            self.assertTrue(label.value_type)
            self.assertTrue(label.description)

    def test_list_resource_descriptors(self):
        client = monitoring.Client()

        descriptor = None
        for item in client.list_resource_descriptors():
            if item.type == RESOURCE_TYPE:
                descriptor = item

        self.assertIsNotNone(descriptor)

        expected_name = 'projects/{project}/{what}/{type}'.format(
            project=client.project,
            what='monitoredResourceDescriptors',
            type=RESOURCE_TYPE,
        )
        self.assertEqual(descriptor.name, expected_name)
        self.assertEqual(descriptor.type, RESOURCE_TYPE)
        self.assertTrue(descriptor.display_name)
        self.assertTrue(descriptor.description)

        self.assertTrue(descriptor.labels)
        for label in descriptor.labels:
            self.assertTrue(label.key)
            self.assertTrue(label.value_type)
            self.assertTrue(label.description)

    def test_query(self):
        client = monitoring.Client()
        query = client.query(METRIC_TYPE, hours=1)
        # There may be no data, but we can ask anyway.
        for _ in query:
            pass    # Not necessarily reached.
