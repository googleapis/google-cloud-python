# -*- coding: utf-8 -*-
#
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


# DO NOT MODIFY! AUTO-GENERATED!
# This file is auto-generated on 2019-05-03.

# flake8: noqa

import os
import pytest

from google.api_core import exceptions
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import enums

PROJECT_INSIDE = os.environ.get("PROJECT_ID", None)
if not PROJECT_INSIDE:
    PROJECT_INSIDE = None
PROJECT_OUTSIDE = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT", None
)
IS_INSIDE_VPCSC = os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC", "false")


class TestVPCServiceControlV3(object):
    @staticmethod
    def _is_rejected(call):
        try:
            responses = call()

            # If we reach this line, then call() did not raise. The return
            # result must be either a google.api_core.page_iterator.Iterator
            # instance, or None.
            list(responses)
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        except:
            pass
        return False

    @staticmethod
    def _do_test(delayed_inside, delayed_outside):
        if IS_INSIDE_VPCSC.lower() == "true":
            assert TestVPCServiceControlV3._is_rejected(delayed_outside)
            assert not (TestVPCServiceControlV3._is_rejected(delayed_inside))
        else:
            assert not (TestVPCServiceControlV3._is_rejected(delayed_outside))
            assert TestVPCServiceControlV3._is_rejected(delayed_inside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_alert_policy(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_alert_policy(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")
        delayed_inside = lambda: client.delete_alert_policy(name_inside)
        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")
        delayed_outside = lambda: client.delete_alert_policy(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")
        delayed_inside = lambda: client.get_alert_policy(name_inside)
        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")
        delayed_outside = lambda: client.get_alert_policy(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_alert_policies(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_alert_policies(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_alert_policies(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(PROJECT_INSIDE, "mock_alert_policy")
        delayed_inside = lambda: client.update_alert_policy({"name": name_inside})
        name_outside = client.alert_policy_path(PROJECT_OUTSIDE, "mock_alert_policy")
        delayed_outside = lambda: client.update_alert_policy({"name": name_outside})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_group(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_group(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")
        delayed_inside = lambda: client.delete_group(name_inside)
        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")
        delayed_outside = lambda: client.delete_group(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")
        delayed_inside = lambda: client.get_group(name_inside)
        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")
        delayed_outside = lambda: client.get_group(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_group_members(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_group_members(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_group_members(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_groups(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_groups(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_groups(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(PROJECT_INSIDE, "mock_group")
        delayed_inside = lambda: client.update_group({"name": name_inside})
        name_outside = client.group_path(PROJECT_OUTSIDE, "mock_group")
        delayed_outside = lambda: client.update_group({"name": name_outside})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_metric_descriptor(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_metric_descriptor(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_time_series(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_time_series(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            PROJECT_INSIDE, "mock_metric_descriptor"
        )
        delayed_inside = lambda: client.delete_metric_descriptor(name_inside)
        name_outside = client.metric_descriptor_path(
            PROJECT_OUTSIDE, "mock_metric_descriptor"
        )
        delayed_outside = lambda: client.delete_metric_descriptor(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            PROJECT_INSIDE, "mock_metric_descriptor"
        )
        delayed_inside = lambda: client.get_metric_descriptor(name_inside)
        name_outside = client.metric_descriptor_path(
            PROJECT_OUTSIDE, "mock_metric_descriptor"
        )
        delayed_outside = lambda: client.get_metric_descriptor(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_monitored_resource_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.monitored_resource_descriptor_path(
            PROJECT_INSIDE, "mock_monitored_resource_descriptor"
        )
        delayed_inside = lambda: client.get_monitored_resource_descriptor(name_inside)
        name_outside = client.monitored_resource_descriptor_path(
            PROJECT_OUTSIDE, "mock_monitored_resource_descriptor"
        )
        delayed_outside = lambda: client.get_monitored_resource_descriptor(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_metric_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_metric_descriptors(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_metric_descriptors(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_monitored_resource_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_monitored_resource_descriptors(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_monitored_resource_descriptors(
            name_outside
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_time_series(
            name_inside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_time_series(
            name_outside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_notification_channel(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_notification_channel(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )
        delayed_inside = lambda: client.delete_notification_channel(name_inside)
        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )
        delayed_outside = lambda: client.delete_notification_channel(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )
        delayed_inside = lambda: client.get_notification_channel(name_inside)
        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )
        delayed_outside = lambda: client.get_notification_channel(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_notification_channel_descriptor(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_descriptor_path(
            PROJECT_INSIDE, "mock_notification_channel_descriptor"
        )
        delayed_inside = lambda: client.get_notification_channel_descriptor(name_inside)
        name_outside = client.notification_channel_descriptor_path(
            PROJECT_OUTSIDE, "mock_notification_channel_descriptor"
        )
        delayed_outside = lambda: client.get_notification_channel_descriptor(
            name_outside
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_notification_channel_descriptors(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_notification_channel_descriptors(
            name_inside
        )
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_notification_channel_descriptors(
            name_outside
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_notification_channels(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_notification_channels(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_notification_channels(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            PROJECT_INSIDE, "mock_notification_channel"
        )
        delayed_inside = lambda: client.update_notification_channel(
            {"name": name_inside}
        )
        name_outside = client.notification_channel_path(
            PROJECT_OUTSIDE, "mock_notification_channel"
        )
        delayed_outside = lambda: client.update_notification_channel(
            {"name": name_outside}
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_create_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.create_uptime_check_config(name_inside, {})
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.create_uptime_check_config(name_outside, {})
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_delete_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.delete_uptime_check_config(name_inside)
        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.delete_uptime_check_config(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_get_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.get_uptime_check_config(name_inside)
        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.get_uptime_check_config(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_list_uptime_check_configs(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(PROJECT_INSIDE)
        delayed_inside = lambda: client.list_uptime_check_configs(name_inside)
        name_outside = client.project_path(PROJECT_OUTSIDE)
        delayed_outside = lambda: client.list_uptime_check_configs(name_outside)
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)

    @pytest.mark.skipif(
        PROJECT_INSIDE is None, reason="Missing environment variable: PROJECT_ID"
    )
    @pytest.mark.skipif(
        PROJECT_OUTSIDE is None,
        reason="Missing environment variable: GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT",
    )
    def test_update_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            PROJECT_INSIDE, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.update_uptime_check_config(
            {"name": name_inside}
        )
        name_outside = client.uptime_check_config_path(
            PROJECT_OUTSIDE, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.update_uptime_check_config(
            {"name": name_outside}
        )
        TestVPCServiceControlV3._do_test(delayed_inside, delayed_outside)
