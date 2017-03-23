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

import unittest

from google.cloud.exceptions import BadRequest
from google.cloud.exceptions import InternalServerError
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import ServiceUnavailable
from google.cloud import monitoring

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id

retry_404 = RetryErrors(NotFound, max_tries=5)
retry_404_500 = RetryErrors((NotFound, InternalServerError))
retry_500 = RetryErrors(InternalServerError)
retry_503 = RetryErrors(ServiceUnavailable)


class TestMonitoring(unittest.TestCase):

    def test_fetch_metric_descriptor(self):
        METRIC_TYPE = (
            'pubsub.googleapis.com/topic/send_message_operation_count')
        METRIC_KIND = monitoring.MetricKind.DELTA
        VALUE_TYPE = monitoring.ValueType.INT64

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
        METRIC_TYPE = (
            'pubsub.googleapis.com/topic/send_message_operation_count')
        METRIC_KIND = monitoring.MetricKind.DELTA
        VALUE_TYPE = monitoring.ValueType.INT64

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

    def test_list_metric_descriptors_filtered(self):
        client = monitoring.Client()

        PREFIX = 'compute.googleapis.com/'
        descriptors = client.list_metric_descriptors(type_prefix=PREFIX)

        # There are currently 18 types with this prefix, but that may change.
        self.assertGreater(len(descriptors), 10)

        for descriptor in descriptors:
            self.assertTrue(descriptor.type.startswith(PREFIX))

    def test_fetch_resource_descriptor(self):
        RESOURCE_TYPE = 'pubsub_topic'

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
        RESOURCE_TYPE = 'pubsub_topic'

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
        METRIC_TYPE = (
            'pubsub.googleapis.com/topic/send_message_operation_count')
        client = monitoring.Client()
        query = client.query(METRIC_TYPE, hours=1)
        # There may be no data, but we can ask anyway.
        for _ in query:
            pass    # Not necessarily reached.

    def test_create_and_delete_metric_descriptor(self):
        METRIC_TYPE = ('custom.googleapis.com/tmp/system_test_example' +
                       unique_resource_id())
        METRIC_KIND = monitoring.MetricKind.GAUGE
        VALUE_TYPE = monitoring.ValueType.DOUBLE
        DESCRIPTION = 'System test example -- DELETE ME!'

        client = monitoring.Client()
        descriptor = client.metric_descriptor(
            METRIC_TYPE,
            metric_kind=METRIC_KIND,
            value_type=VALUE_TYPE,
            description=DESCRIPTION,
        )

        retry_500(descriptor.create)()
        retry_404_500(descriptor.delete)()

    def test_write_point(self):
        METRIC_TYPE = ('custom.googleapis.com/tmp/system_test_example' +
                       unique_resource_id())
        METRIC_KIND = monitoring.MetricKind.GAUGE
        VALUE_TYPE = monitoring.ValueType.DOUBLE
        DESCRIPTION = 'System test example -- DELETE ME!'
        VALUE = 3.14

        client = monitoring.Client()
        descriptor = client.metric_descriptor(
            METRIC_TYPE,
            metric_kind=METRIC_KIND,
            value_type=VALUE_TYPE,
            description=DESCRIPTION,
        )

        descriptor.create()

        metric = client.metric(METRIC_TYPE, {})
        resource = client.resource('global', {})

        retry_500(client.write_point)(metric, resource, VALUE)

        def _query_timeseries_with_retries():
            MAX_RETRIES = 10

            def _has_timeseries(result):
                return len(list(result)) > 0

            retry_result = RetryResult(_has_timeseries,
                                       max_tries=MAX_RETRIES)(client.query)
            return RetryErrors(BadRequest, max_tries=MAX_RETRIES)(retry_result)

        query = _query_timeseries_with_retries()(METRIC_TYPE, minutes=5)
        timeseries_list = list(query)
        self.assertEqual(len(timeseries_list), 1)
        timeseries = timeseries_list[0]
        self.assertEqual(timeseries.metric, metric)
        # project_id label only exists on output.
        del timeseries.resource.labels['project_id']
        self.assertEqual(timeseries.resource, resource)

        descriptor.delete()

        with self.assertRaises(NotFound):
            descriptor.delete()


class TestMonitoringGroups(unittest.TestCase):

    def setUp(self):
        self.to_delete = []
        self.DISPLAY_NAME = 'Testing: New group'
        self.FILTER = 'resource.type = "gce_instance"'
        self.IS_CLUSTER = True

    def tearDown(self):
        for group in self.to_delete:
            retry_404(group.delete)()

    def test_create_group(self):
        client = monitoring.Client()
        group = client.group(
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER,
            is_cluster=self.IS_CLUSTER,
        )

        retry_503(group.create)()
        self.to_delete.append(group)

        self.assertTrue(group.exists())

    def test_list_groups(self):
        client = monitoring.Client()
        new_group = client.group(
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER,
            is_cluster=self.IS_CLUSTER,
        )
        before_groups = client.list_groups()
        before_names = set(group.name for group in before_groups)

        retry_503(new_group.create)()
        self.to_delete.append(new_group)

        self.assertTrue(new_group.exists())
        after_groups = client.list_groups()
        after_names = set(group.name for group in after_groups)
        self.assertEqual(after_names - before_names,
                         set([new_group.name]))

    def test_reload_group(self):
        client = monitoring.Client()
        group = client.group(
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER,
            is_cluster=self.IS_CLUSTER,
        )

        retry_503(group.create)()
        self.to_delete.append(group)

        group.filter = 'resource.type = "aws_ec2_instance"'
        group.display_name = 'locally changed name'
        group.reload()
        self.assertEqual(group.filter, self.FILTER)
        self.assertEqual(group.display_name, self.DISPLAY_NAME)

    def test_update_group(self):
        NEW_FILTER = 'resource.type = "aws_ec2_instance"'
        NEW_DISPLAY_NAME = 'updated'

        client = monitoring.Client()
        group = client.group(
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER,
            is_cluster=self.IS_CLUSTER,
        )

        retry_503(group.create)()
        self.to_delete.append(group)

        group.filter = NEW_FILTER
        group.display_name = NEW_DISPLAY_NAME
        group.update()

        after = client.fetch_group(group.id)
        self.assertEqual(after.filter, NEW_FILTER)
        self.assertEqual(after.display_name, NEW_DISPLAY_NAME)

    def test_list_group_members(self):
        client = monitoring.Client()
        group = client.group(
            display_name=self.DISPLAY_NAME,
            filter_string=self.FILTER,
            is_cluster=self.IS_CLUSTER,
        )

        retry_503(group.create)()
        self.to_delete.append(group)

        for member in group.list_members():
            self.assertIsInstance(member, monitoring.Resource)

    def test_group_hierarchy(self):
        client = monitoring.Client()
        root_group = client.group(
            display_name='Testing: Root group',
            filter_string=self.FILTER,
        )

        retry_503(root_group.create)()
        self.to_delete.insert(0, root_group)

        middle_group = client.group(
            display_name='Testing: Middle group',
            filter_string=self.FILTER,
            parent_id=root_group.id,
        )

        retry_503(middle_group.create)()
        self.to_delete.insert(0, middle_group)

        leaf_group = client.group(
            display_name='Testing: Leaf group',
            filter_string=self.FILTER,
            parent_id=middle_group.id,
        )

        retry_503(leaf_group.create)()
        self.to_delete.insert(0, leaf_group)

        # Test for parent.
        actual_parent = middle_group.fetch_parent()
        self.assertTrue(actual_parent.name, root_group.name)

        # Test for children.
        actual_children = middle_group.list_children()
        children_names = [group.name for group in actual_children]
        self.assertEqual(children_names, [leaf_group.name])

        # Test for descendants.
        actual_descendants = root_group.list_descendants()
        descendant_names = {group.name for group in actual_descendants}
        self.assertEqual(descendant_names,
                         set([middle_group.name, leaf_group.name]))

        # Test for ancestors.
        actual_ancestors = leaf_group.list_ancestors()
        ancestor_names = [group.name for group in actual_ancestors]
        self.assertEqual(ancestor_names, [middle_group.name, root_group.name])
