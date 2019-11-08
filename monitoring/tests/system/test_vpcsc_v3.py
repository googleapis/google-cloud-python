# -*- coding: utf-8 -*-
#
# flake8: noqa
#
# DO NOT MODIFY! THIS FILE IS AUTO-GENERATED.
# This file is auto-generated on 08 Nov 19 20:09 UTC.

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest
import logging
from google.api_core import exceptions
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import enums

PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)
IS_INSIDE_VPCSC = os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC", "false")
logging.basicConfig(level=logging.DEBUG)


class TestVPCServiceControlV3(object):
    @staticmethod
    def _get_error(call):
        logger = logging.getLogger(__name__)
        try:
            responses = call()

            # If we reach this line, then call() did not raise. The return
            # result must be either a google.api_core.page_iterator.Iterator
            # instance, or None.
            list(responses)
        except Exception as e:
            logger.debug(e)
            return e
        logger.debug("no error")
        return None

    @staticmethod
    def _do_test(delayed_inside, delayed_outside):
        logger = logging.getLogger(__name__)
        msg = "Request is prohibited by organization's policy".lower()
        if IS_INSIDE_VPCSC.lower() == "true":
            logger.debug("inside perimeter")
            e = TestVPCServiceControlV3._get_error(delayed_outside)
            assert (
                isinstance(e, exceptions.PermissionDenied) and msg in e.message.lower()
            )
            e = TestVPCServiceControlV3._get_error(delayed_inside)
            assert not (
                isinstance(e, exceptions.PermissionDenied) and msg in e.message.lower()
            )
        else:
            logger.debug("outside perimeter")
            e = TestVPCServiceControlV3._get_error(delayed_outside)
            assert not (
                isinstance(e, exceptions.PermissionDenied) and msg in e.message.lower()
            )
            e = TestVPCServiceControlV3._get_error(delayed_inside)
            assert (
                isinstance(e, exceptions.PermissionDenied) and msg in e.message.lower()
            )

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_alert_policy: requesting {name_inside}"
            )
            return client.create_alert_policy(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_alert_policy: requesting {name_outside}"
            )
            return client.create_alert_policy(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_delete_alert_policy: requesting {name_inside}"
            )
            return client.delete_alert_policy(name_inside)

        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_delete_alert_policy: requesting {name_outside}"
            )
            return client.delete_alert_policy(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_alert_policy: requesting {name_inside}"
            )
            return client.get_alert_policy(name_inside)

        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_alert_policy: requesting {name_outside}"
            )
            return client.get_alert_policy(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_alert_policies(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_alert_policies: requesting {name_inside}"
            )
            return client.list_alert_policies(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_alert_policies: requesting {name_outside}"
            )
            return client.list_alert_policies(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_update_alert_policy: requesting {name_inside}"
            )
            return client.update_alert_policy({"name": name_inside})

        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_update_alert_policy: requesting {name_outside}"
            )
            return client.update_alert_policy({"name": name_outside})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_group: requesting {name_inside}"
            )
            return client.create_group(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_group: requesting {name_outside}"
            )
            return client.create_group(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_delete_group: requesting {name_inside}"
            )
            return client.delete_group(name_inside)

        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_delete_group: requesting {name_outside}"
            )
            return client.delete_group(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_group: requesting {name_inside}"
            )
            return client.get_group(name_inside)

        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_group: requesting {name_outside}"
            )
            return client.get_group(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_group_members(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_group_members: requesting {name_inside}"
            )
            return client.list_group_members(name_inside)

        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_group_members: requesting {name_outside}"
            )
            return client.list_group_members(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_groups(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_groups: requesting {name_inside}"
            )
            return client.list_groups(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_groups: requesting {name_outside}"
            )
            return client.list_groups(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_update_group: requesting {name_inside}"
            )
            return client.update_group({"name": name_inside})

        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_update_group: requesting {name_outside}"
            )
            return client.update_group({"name": name_outside})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_metric_descriptor: requesting {name_inside}"
            )
            return client.create_metric_descriptor(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_metric_descriptor: requesting {name_outside}"
            )
            return client.create_metric_descriptor(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_time_series: requesting {name_inside}"
            )
            return client.create_time_series(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_time_series: requesting {name_outside}"
            )
            return client.create_time_series(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            PROJECT_INSIDE, "mock_metric_descriptor"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_delete_metric_descriptor: requesting {name_inside}"
            )
            return client.delete_metric_descriptor(name_inside)

        name_outside = client.metric_descriptor_path(
            PROJECT_OUTSIDE, "mock_metric_descriptor"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_delete_metric_descriptor: requesting {name_outside}"
            )
            return client.delete_metric_descriptor(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            PROJECT_INSIDE, "mock_metric_descriptor"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_metric_descriptor: requesting {name_inside}"
            )
            return client.get_metric_descriptor(name_inside)

        name_outside = client.metric_descriptor_path(
            PROJECT_OUTSIDE, "mock_metric_descriptor"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_metric_descriptor: requesting {name_outside}"
            )
            return client.get_metric_descriptor(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_monitored_resource_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.monitored_resource_descriptor_path(
            PROJECT_INSIDE, "mock_monitored_resource_descriptor"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_monitored_resource_descriptor: requesting {name_inside}"
            )
            return client.get_monitored_resource_descriptor(name_inside)

        name_outside = client.monitored_resource_descriptor_path(
            PROJECT_OUTSIDE, "mock_monitored_resource_descriptor"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_monitored_resource_descriptor: requesting {name_outside}"
            )
            return client.get_monitored_resource_descriptor(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_metric_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_metric_descriptors: requesting {name_inside}"
            )
            return client.list_metric_descriptors(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_metric_descriptors: requesting {name_outside}"
            )
            return client.list_metric_descriptors(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_monitored_resource_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_monitored_resource_descriptors: requesting {name_inside}"
            )
            return client.list_monitored_resource_descriptors(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_monitored_resource_descriptors: requesting {name_outside}"
            )
            return client.list_monitored_resource_descriptors(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_time_series: requesting {name_inside}"
            )
            return client.list_time_series(
                name_inside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
            )

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_time_series: requesting {name_outside}"
            )
            return client.list_time_series(
                name_outside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
            )

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_notification_channel: requesting {name_inside}"
            )
            return client.create_notification_channel(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_notification_channel: requesting {name_outside}"
            )
            return client.create_notification_channel(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_delete_notification_channel: requesting {name_inside}"
            )
            return client.delete_notification_channel(name_inside)

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_delete_notification_channel: requesting {name_outside}"
            )
            return client.delete_notification_channel(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel: requesting {name_inside}"
            )
            return client.get_notification_channel(name_inside)

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel: requesting {name_outside}"
            )
            return client.get_notification_channel(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_notification_channel_descriptor(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_descriptor_path(
            PROJECT_INSIDE, "mock_notification_channel_descriptor"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel_descriptor: requesting {name_inside}"
            )
            return client.get_notification_channel_descriptor(name_inside)

        name_outside = client.notification_channel_descriptor_path(
            PROJECT_OUTSIDE, "mock_notification_channel_descriptor"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel_descriptor: requesting {name_outside}"
            )
            return client.get_notification_channel_descriptor(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_notification_channel_verification_code(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel_verification_code: requesting {name_inside}"
            )
            return client.get_notification_channel_verification_code(name_inside)

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_notification_channel_verification_code: requesting {name_outside}"
            )
            return client.get_notification_channel_verification_code(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_notification_channel_descriptors(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_notification_channel_descriptors: requesting {name_inside}"
            )
            return client.list_notification_channel_descriptors(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_notification_channel_descriptors: requesting {name_outside}"
            )
            return client.list_notification_channel_descriptors(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_notification_channels(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_notification_channels: requesting {name_inside}"
            )
            return client.list_notification_channels(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_notification_channels: requesting {name_outside}"
            )
            return client.list_notification_channels(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_send_notification_channel_verification_code(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_send_notification_channel_verification_code: requesting {name_inside}"
            )
            return client.send_notification_channel_verification_code(name_inside)

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_send_notification_channel_verification_code: requesting {name_outside}"
            )
            return client.send_notification_channel_verification_code(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_update_notification_channel: requesting {name_inside}"
            )
            return client.update_notification_channel({"name": name_inside})

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_update_notification_channel: requesting {name_outside}"
            )
            return client.update_notification_channel({"name": name_outside})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_verify_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_verify_notification_channel: requesting {name_inside}"
            )
            return client.verify_notification_channel(name_inside, "")

        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_verify_notification_channel: requesting {name_outside}"
            )
            return client.verify_notification_channel(name_outside, "")

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_create_uptime_check_config: requesting {name_inside}"
            )
            return client.create_uptime_check_config(name_inside, {})

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_create_uptime_check_config: requesting {name_outside}"
            )
            return client.create_uptime_check_config(name_outside, {})

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_delete_uptime_check_config: requesting {name_inside}"
            )
            return client.delete_uptime_check_config(name_inside)

        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_delete_uptime_check_config: requesting {name_outside}"
            )
            return client.delete_uptime_check_config(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_get_uptime_check_config: requesting {name_inside}"
            )
            return client.get_uptime_check_config(name_inside)

        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_get_uptime_check_config: requesting {name_outside}"
            )
            return client.get_uptime_check_config(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_uptime_check_configs(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_list_uptime_check_configs: requesting {name_inside}"
            )
            return client.list_uptime_check_configs(name_inside)

        name_outside = client.project_path(PROJECT_OUTSIDE)

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_list_uptime_check_configs: requesting {name_outside}"
            )
            return client.list_uptime_check_configs(name_outside)

        self._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        not PROJECT_INSIDE, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        not PROJECT_OUTSIDE,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )

        def delayed_inside():
            logging.getLogger(__name__).debug(
                f"test_update_uptime_check_config: requesting {name_inside}"
            )
            return client.update_uptime_check_config({"name": name_inside})

        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )

        def delayed_outside():
            logging.getLogger(__name__).debug(
                f"test_update_uptime_check_config: requesting {name_outside}"
            )
            return client.update_uptime_check_config({"name": name_outside})

        self._do_test(delayed_inside, delayed_outside)
