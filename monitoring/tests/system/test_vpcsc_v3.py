# -*- coding: utf-8 -*-
#
# flake8: noqa
#
# DO NOT MODIFY! THIS FILE IS AUTO-GENERATED.
# This file is auto-generated on 11 Oct 19 21:43 UTC.

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 		https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest

from google.api_core import exceptions
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import enums
from test_utils.vpcsc_config import vpcsc_config


@vpcsc_config.skip_unless_inside_vpcsc
class TestVPCServiceControlV3(object):
    @staticmethod
    def _is_rejected(call):
        try:
            call()
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        return False

    @staticmethod
    def _is_rejected_w_iterator(call):
        try:
            list(call())
        except exceptions.PermissionDenied as e:
            return e.message == "Request is prohibited by organization's policy"
        return False

    def _do_test(self, delayed_inside, delayed_outside):
        assert self._is_rejected(delayed_outside)
        assert not self._is_rejected(delayed_inside)

    def _do_test_w_list(self, delayed_inside, delayed_outside):
        assert self._is_rejected_w_list(delayed_outside)
        assert not self._is_rejected_w_list(delayed_inside)

    def test_create_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_alert_policy(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_alert_policy(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(
            vpcsc_config.project_inside, "mock_alert_policy"
        )
        delayed_inside = lambda: client.delete_alert_policy(name_inside)
        name_outside = client.alert_policy_path(
            vpcsc_config.project_outside, "mock_alert_policy"
        )
        delayed_outside = lambda: client.delete_alert_policy(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(
            vpcsc_config.project_inside, "mock_alert_policy"
        )
        delayed_inside = lambda: client.get_alert_policy(name_inside)
        name_outside = client.alert_policy_path(
            vpcsc_config.project_outside, "mock_alert_policy"
        )
        delayed_outside = lambda: client.get_alert_policy(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_list_alert_policies(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_alert_policies(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_alert_policies(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_update_alert_policy(self):
        client = monitoring_v3.AlertPolicyServiceClient()
        name_inside = client.alert_policy_path(
            vpcsc_config.project_inside, "mock_alert_policy"
        )
        delayed_inside = lambda: client.update_alert_policy({"name": name_inside})
        name_outside = client.alert_policy_path(
            vpcsc_config.project_outside, "mock_alert_policy"
        )
        delayed_outside = lambda: client.update_alert_policy({"name": name_outside})
        self._do_test(delayed_inside, delayed_outside)

    def test_create_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_group(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_group(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(vpcsc_config.project_inside, "mock_group")
        delayed_inside = lambda: client.delete_group(name_inside)
        name_outside = client.group_path(vpcsc_config.project_outside, "mock_group")
        delayed_outside = lambda: client.delete_group(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(vpcsc_config.project_inside, "mock_group")
        delayed_inside = lambda: client.get_group(name_inside)
        name_outside = client.group_path(vpcsc_config.project_outside, "mock_group")
        delayed_outside = lambda: client.get_group(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_list_group_members(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(vpcsc_config.project_inside, "mock_group")
        delayed_inside = lambda: client.list_group_members(name_inside)
        name_outside = client.group_path(vpcsc_config.project_outside, "mock_group")
        delayed_outside = lambda: client.list_group_members(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_list_groups(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_groups(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_groups(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_update_group(self):
        client = monitoring_v3.GroupServiceClient()
        name_inside = client.group_path(vpcsc_config.project_inside, "mock_group")
        delayed_inside = lambda: client.update_group({"name": name_inside})
        name_outside = client.group_path(vpcsc_config.project_outside, "mock_group")
        delayed_outside = lambda: client.update_group({"name": name_outside})
        self._do_test(delayed_inside, delayed_outside)

    def test_create_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_metric_descriptor(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_metric_descriptor(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_create_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_time_series(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_time_series(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            vpcsc_config.project_inside, "mock_metric_descriptor"
        )
        delayed_inside = lambda: client.delete_metric_descriptor(name_inside)
        name_outside = client.metric_descriptor_path(
            vpcsc_config.project_outside, "mock_metric_descriptor"
        )
        delayed_outside = lambda: client.delete_metric_descriptor(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_metric_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.metric_descriptor_path(
            vpcsc_config.project_inside, "mock_metric_descriptor"
        )
        delayed_inside = lambda: client.get_metric_descriptor(name_inside)
        name_outside = client.metric_descriptor_path(
            vpcsc_config.project_outside, "mock_metric_descriptor"
        )
        delayed_outside = lambda: client.get_metric_descriptor(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_monitored_resource_descriptor(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.monitored_resource_descriptor_path(
            vpcsc_config.project_inside, "mock_monitored_resource_descriptor"
        )
        delayed_inside = lambda: client.get_monitored_resource_descriptor(name_inside)
        name_outside = client.monitored_resource_descriptor_path(
            vpcsc_config.project_outside, "mock_monitored_resource_descriptor"
        )
        delayed_outside = lambda: client.get_monitored_resource_descriptor(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_list_metric_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_metric_descriptors(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_metric_descriptors(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_list_monitored_resource_descriptors(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_monitored_resource_descriptors(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_monitored_resource_descriptors(
            name_outside
        )
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_list_time_series(self):
        client = monitoring_v3.MetricServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_time_series(
            name_inside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_time_series(
            name_outside, "", {}, enums.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_create_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_notification_channel(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_notification_channel(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.delete_notification_channel(name_inside)
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.delete_notification_channel(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.get_notification_channel(name_inside)
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.get_notification_channel(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_notification_channel_descriptor(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_descriptor_path(
            vpcsc_config.project_inside, "mock_notification_channel_descriptor"
        )
        delayed_inside = lambda: client.get_notification_channel_descriptor(name_inside)
        name_outside = client.notification_channel_descriptor_path(
            vpcsc_config.project_outside, "mock_notification_channel_descriptor"
        )
        delayed_outside = lambda: client.get_notification_channel_descriptor(
            name_outside
        )
        self._do_test(delayed_inside, delayed_outside)

    def test_get_notification_channel_verification_code(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.get_notification_channel_verification_code(
            name_inside
        )
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.get_notification_channel_verification_code(
            name_outside
        )
        self._do_test(delayed_inside, delayed_outside)

    def test_list_notification_channel_descriptors(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_notification_channel_descriptors(
            name_inside
        )
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_notification_channel_descriptors(
            name_outside
        )
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_list_notification_channels(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_notification_channels(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_notification_channels(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_send_notification_channel_verification_code(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.send_notification_channel_verification_code(
            name_inside
        )
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.send_notification_channel_verification_code(
            name_outside
        )
        self._do_test(delayed_inside, delayed_outside)

    def test_update_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.update_notification_channel(
            {"name": name_inside}
        )
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.update_notification_channel(
            {"name": name_outside}
        )
        self._do_test(delayed_inside, delayed_outside)

    def test_verify_notification_channel(self):
        client = monitoring_v3.NotificationChannelServiceClient()
        name_inside = client.notification_channel_path(
            vpcsc_config.project_inside, "mock_notification_channel"
        )
        delayed_inside = lambda: client.verify_notification_channel(name_inside, "")
        name_outside = client.notification_channel_path(
            vpcsc_config.project_outside, "mock_notification_channel"
        )
        delayed_outside = lambda: client.verify_notification_channel(name_outside, "")
        self._do_test(delayed_inside, delayed_outside)

    def test_create_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.create_uptime_check_config(name_inside, {})
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.create_uptime_check_config(name_outside, {})
        self._do_test(delayed_inside, delayed_outside)

    def test_delete_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            vpcsc_config.project_inside, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.delete_uptime_check_config(name_inside)
        name_outside = client.uptime_check_config_path(
            vpcsc_config.project_outside, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.delete_uptime_check_config(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_get_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            vpcsc_config.project_inside, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.get_uptime_check_config(name_inside)
        name_outside = client.uptime_check_config_path(
            vpcsc_config.project_outside, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.get_uptime_check_config(name_outside)
        self._do_test(delayed_inside, delayed_outside)

    def test_list_uptime_check_configs(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.project_path(vpcsc_config.project_inside)
        delayed_inside = lambda: client.list_uptime_check_configs(name_inside)
        name_outside = client.project_path(vpcsc_config.project_outside)
        delayed_outside = lambda: client.list_uptime_check_configs(name_outside)
        self._do_test_w_list(delayed_inside, delayed_outside)

    def test_update_uptime_check_config(self):
        client = monitoring_v3.UptimeCheckServiceClient()
        name_inside = client.uptime_check_config_path(
            vpcsc_config.project_inside, "mock_uptime_check_config"
        )
        delayed_inside = lambda: client.update_uptime_check_config(
            {"name": name_inside}
        )
        name_outside = client.uptime_check_config_path(
            vpcsc_config.project_outside, "mock_uptime_check_config"
        )
        delayed_outside = lambda: client.update_uptime_check_config(
            {"name": name_outside}
        )
        self._do_test(delayed_inside, delayed_outside)
