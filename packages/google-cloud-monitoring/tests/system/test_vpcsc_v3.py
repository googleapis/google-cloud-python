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
from test_utils.vpcsc_config import vpcsc_config


_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy"


@pytest.fixture(scope="module")
def aps_client():
    return monitoring_v3.AlertPolicyServiceClient()


@pytest.fixture(scope="module")
def name_inside(aps_client):
    return f"projects/{vpcsc_config.project_inside}"


@pytest.fixture(scope="module")
def name_outside(aps_client):
    return f"projects/{vpcsc_config.project_outside}"


@pytest.fixture(scope="module")
def alert_policy_path_inside(aps_client):
    alert_policy_id = "mock_alert_policy"
    return aps_client.alert_policy_path(vpcsc_config.project_inside, alert_policy_id)


@pytest.fixture(scope="module")
def alert_policy_path_outside(aps_client):
    alert_policy_id = "mock_alert_policy"
    return aps_client.alert_policy_path(vpcsc_config.project_outside, alert_policy_id)


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDAlertPolicies(object):
    @staticmethod
    def test_create_alert_policy_inside(aps_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            aps_client.create_alert_policy(
                request={"name": name_inside, "alert_policy": {}}
            )

    @staticmethod
    def test_create_alert_policy_outside(aps_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            aps_client.create_alert_policy(
                request={"name": name_outside, "alert_policy": {}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_alert_policies_inside(aps_client, name_inside):
        list(aps_client.list_alert_policies(request={"name": name_inside}))

    @staticmethod
    def test_list_alert_policies_outside(aps_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(aps_client.list_alert_policies(request={"name": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_alert_policy_inside(aps_client, alert_policy_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            aps_client.get_alert_policy(request={"name": alert_policy_path_inside})

    @staticmethod
    def test_get_alert_policy_outside(aps_client, alert_policy_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            aps_client.get_alert_policy(request={"name": alert_policy_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_alert_policy_inside(aps_client, alert_policy_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            aps_client.update_alert_policy(
                request={"alert_policy": {"name": alert_policy_path_inside}}
            )

    @staticmethod
    def test_update_alert_policy_outside(aps_client, alert_policy_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            aps_client.update_alert_policy(
                request={"alert_policy": {"name": alert_policy_path_outside}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_alert_policy_inside(aps_client, alert_policy_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            aps_client.delete_alert_policy(request={"name": alert_policy_path_inside})

    @staticmethod
    def test_delete_alert_policy_outside(aps_client, alert_policy_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            aps_client.delete_alert_policy(request={"name": alert_policy_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def gs_client():
    return monitoring_v3.GroupServiceClient()


@pytest.fixture(scope="module")
def group_path_inside(gs_client):
    group_id = "mock_group"
    return gs_client.group_path(vpcsc_config.project_inside, group_id)


@pytest.fixture(scope="module")
def group_path_outside(gs_client):
    group_id = "mock_group"
    return gs_client.group_path(vpcsc_config.project_outside, group_id)


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDGroups(object):
    @staticmethod
    def test_create_group_inside(gs_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            gs_client.create_group(request={"name": name_inside, "group": {}})

    @staticmethod
    def test_create_group_outside(gs_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            gs_client.create_group(request={"name": name_outside, "group": {}})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_groups_inside(gs_client, name_inside):
        list(gs_client.list_groups(request={"name": name_inside}))

    @staticmethod
    def test_list_groups_outside(gs_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(gs_client.list_groups(request={"name": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_group_inside(gs_client, group_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            gs_client.get_group(request={"name": group_path_inside})

    @staticmethod
    def test_get_group_outside(gs_client, group_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            gs_client.get_group(request={"name": group_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_group_members_inside(gs_client, group_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            list(gs_client.list_group_members(request={"name": group_path_inside}))

    @staticmethod
    def test_list_group_members_outside(gs_client, group_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(gs_client.list_group_members(request={"name": group_path_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_group_inside(gs_client, group_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            gs_client.update_group(request={"group": {"name": group_path_inside}})

    @staticmethod
    def test_update_group_outside(gs_client, group_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            gs_client.update_group(request={"group": {"name": group_path_outside}})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_group_inside(gs_client, group_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            gs_client.delete_group(request={"name": group_path_inside})

    @staticmethod
    def test_delete_group_outside(gs_client, group_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            gs_client.delete_group(request={"name": group_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def ms_client():
    return monitoring_v3.MetricServiceClient()


@pytest.fixture(scope="module")
def metric_descriptor_path_inside(ms_client):
    metric_descriptor_id = "mock_metric_descriptor"
    return ms_client.metric_descriptor_path(
        vpcsc_config.project_inside, metric_descriptor_id
    )


@pytest.fixture(scope="module")
def metric_descriptor_path_outside(ms_client):
    metric_descriptor_id = "mock_metric_descriptor"
    return ms_client.metric_descriptor_path(
        vpcsc_config.project_outside, metric_descriptor_id
    )


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDMetricDescriptors(object):
    @staticmethod
    def test_create_metric_descriptor_inside(ms_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ms_client.create_metric_descriptor(
                request={"name": name_inside, "metric_descriptor": {}}
            )

    @staticmethod
    def test_create_metric_descriptor_outside(ms_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ms_client.create_metric_descriptor(
                request={"name": name_outside, "metric_descriptor": {}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_metric_descriptors_inside(ms_client, name_inside):
        list(ms_client.list_metric_descriptors(request={"name": name_inside}))

    @staticmethod
    def test_list_metric_descriptors_outside(ms_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(ms_client.list_metric_descriptors(request={"name": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_metric_descriptor_inside(ms_client, metric_descriptor_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ms_client.get_metric_descriptor(
                request={"name": metric_descriptor_path_inside}
            )

    @staticmethod
    def test_get_metric_descriptor_outside(ms_client, metric_descriptor_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ms_client.get_metric_descriptor(
                request={"name": metric_descriptor_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_metric_descriptor_inside(ms_client, metric_descriptor_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ms_client.delete_metric_descriptor(
                request={"name": metric_descriptor_path_inside}
            )

    @staticmethod
    def test_delete_metric_descriptor_outside(
        ms_client, metric_descriptor_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ms_client.delete_metric_descriptor(
                request={"name": metric_descriptor_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDTimeSeries(object):
    @staticmethod
    def test_create_time_series_inside(ms_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ms_client.create_time_series(
                request={"name": name_inside, "time_series": {}}
            )

    @staticmethod
    def test_create_time_series_outside(ms_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ms_client.create_time_series(
                request={"name": name_outside, "time_series": {}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_time_series_inside(ms_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            list(
                ms_client.list_time_series(
                    request={
                        "name": name_inside,
                        "filter": "",
                        "interval": {},
                        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                    }
                )
            )

    @staticmethod
    def test_list_time_series_outside(ms_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(
                ms_client.list_time_series(
                    request={
                        "name": name_outside,
                        "filter": "",
                        "interval": {},
                        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                    }
                )
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def monitored_resource_descriptor_path_inside(ms_client):
    monitored_resource_descriptor_id = "mock_monitored_resource_descriptor"
    return ms_client.monitored_resource_descriptor_path(
        vpcsc_config.project_inside, monitored_resource_descriptor_id
    )


@pytest.fixture(scope="module")
def monitored_resource_descriptor_path_outside(ms_client):
    monitored_resource_descriptor_id = "mock_monitored_resource_descriptor"
    return ms_client.monitored_resource_descriptor_path(
        vpcsc_config.project_outside, monitored_resource_descriptor_id
    )


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDMonitoredResourceDescriptor(object):
    @staticmethod
    def test_list_monitored_resource_descriptors_inside(ms_client, name_inside):
        list(
            ms_client.list_monitored_resource_descriptors(request={"name": name_inside})
        )

    @staticmethod
    def test_list_monitored_resource_descriptors_outside(ms_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(
                ms_client.list_monitored_resource_descriptors(
                    request={"name": name_outside}
                )
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_monitored_resource_descriptor_inside(
        ms_client, monitored_resource_descriptor_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ms_client.get_monitored_resource_descriptor(
                request={"name": monitored_resource_descriptor_path_inside}
            )

    @staticmethod
    def test_get_monitored_resource_descriptor_outside(
        ms_client, monitored_resource_descriptor_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ms_client.get_monitored_resource_descriptor(
                request={"name": monitored_resource_descriptor_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def ncs_client():
    return monitoring_v3.NotificationChannelServiceClient()


@pytest.fixture(scope="module")
def notification_channel_path_inside(ncs_client):
    notification_channel_id = "mock_notification_channel"
    return ncs_client.notification_channel_path(
        vpcsc_config.project_inside, notification_channel_id
    )


@pytest.fixture(scope="module")
def notification_channel_descriptor_path_inside(ncs_client):
    notification_channel_descriptor_id = "mock_notification_channel_descriptor"
    return ncs_client.notification_channel_descriptor_path(
        vpcsc_config.project_inside, notification_channel_descriptor_id
    )


@pytest.fixture(scope="module")
def notification_channel_path_outside(ncs_client):
    notification_channel_id = "mock_notification_channel"
    return ncs_client.notification_channel_path(
        vpcsc_config.project_outside, notification_channel_id
    )


@pytest.fixture(scope="module")
def notification_channel_descriptor_path_outside(ncs_client):
    notification_channel_descriptor_id = "mock_notification_channel_descriptor"
    return ncs_client.notification_channel_descriptor_path(
        vpcsc_config.project_outside, notification_channel_descriptor_id
    )


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDNotificationChannels(object):
    @staticmethod
    def test_create_notification_channel_inside(ncs_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ncs_client.create_notification_channel(
                request={"name": name_inside, "notification_channel": {}}
            )

    @staticmethod
    def test_create_notification_channel_outside(ncs_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.create_notification_channel(
                request={"name": name_outside, "notification_channel": {}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_notification_channels_inside(ncs_client, name_inside):
        list(ncs_client.list_notification_channels(request={"name": name_inside}))

    @staticmethod
    def test_list_notification_channels_outside(ncs_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(ncs_client.list_notification_channels(request={"name": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_notification_channel_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.get_notification_channel(
                request={"name": notification_channel_path_inside}
            )

    @staticmethod
    def test_get_notification_channel_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.get_notification_channel(
                request={"name": notification_channel_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_notification_channel_verification_code_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.get_notification_channel_verification_code(
                request={"name": notification_channel_path_inside}
            )

    @staticmethod
    def test_get_notification_channel_verification_code_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.get_notification_channel_verification_code(
                request={"name": notification_channel_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_send_notification_channel_verification_code_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.send_notification_channel_verification_code(
                request={"name": notification_channel_path_inside}
            )

    @staticmethod
    def test_send_notification_channel_verification_code_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.send_notification_channel_verification_code(
                request={"name": notification_channel_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_verify_notification_channel_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.verify_notification_channel(
                request={"name": notification_channel_path_inside, "code": ""}
            )

    @staticmethod
    def test_verify_notification_channel_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.verify_notification_channel(
                request={"name": notification_channel_path_outside, "code": ""}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_notification_channel_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ncs_client.update_notification_channel(
                request={
                    "notification_channel": {"name": notification_channel_path_inside}
                }
            )

    @staticmethod
    def test_update_notification_channel_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.update_notification_channel(
                request={
                    "notification_channel": {"name": notification_channel_path_outside}
                }
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_notification_channel_inside(
        ncs_client, notification_channel_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.delete_notification_channel(
                request={"name": notification_channel_path_inside}
            )

    @staticmethod
    def test_delete_notification_channel_outside(
        ncs_client, notification_channel_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.delete_notification_channel(
                request={"name": notification_channel_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_notification_channel_descriptors_inside(ncs_client, name_inside):
        list(
            ncs_client.list_notification_channel_descriptors(
                request={"name": name_inside}
            )
        )

    @staticmethod
    def test_list_notification_channel_descriptors_outside(ncs_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(
                ncs_client.list_notification_channel_descriptors(
                    request={"name": name_outside}
                )
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_notification_channel_descriptor_inside(
        ncs_client, notification_channel_descriptor_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ncs_client.get_notification_channel_descriptor(
                request={"name": notification_channel_descriptor_path_inside}
            )

    @staticmethod
    def test_get_notification_channel_descriptor_outside(
        ncs_client, notification_channel_descriptor_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ncs_client.get_notification_channel_descriptor(
                request={"name": notification_channel_descriptor_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def ucc_client():
    return monitoring_v3.UptimeCheckServiceClient()


@pytest.fixture(scope="module")
def uptime_check_config_path_inside(ucc_client):
    uptime_check_config_id = "mock_notification_channel"
    return ucc_client.uptime_check_config_path(
        vpcsc_config.project_inside, uptime_check_config_id
    )


@pytest.fixture(scope="module")
def uptime_check_config_path_outside(ucc_client):
    uptime_check_config_id = "mock_notification_channel"
    return ucc_client.uptime_check_config_path(
        vpcsc_config.project_outside, uptime_check_config_id
    )


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDUptimeCheckConfigs(object):
    @staticmethod
    def test_create_uptime_check_config_inside(ucc_client, name_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            ucc_client.create_uptime_check_config(
                request={"parent": name_inside, "uptime_check_config": {}}
            )

    @staticmethod
    def test_create_uptime_check_config_outside(ucc_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ucc_client.create_uptime_check_config(
                request={"parent": name_outside, "uptime_check_config": {}}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_uptime_check_configs_inside(ucc_client, name_inside):
        list(ucc_client.list_uptime_check_configs(request={"parent": name_inside}))

    @staticmethod
    def test_list_uptime_check_configs_outside(ucc_client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(ucc_client.list_uptime_check_configs(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_uptime_check_config_inside(
        ucc_client, uptime_check_config_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ucc_client.get_uptime_check_config(
                request={"name": uptime_check_config_path_inside}
            )

    @staticmethod
    def test_get_uptime_check_config_outside(
        ucc_client, uptime_check_config_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ucc_client.get_uptime_check_config(
                request={"name": uptime_check_config_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_uptime_check_config_inside(
        ucc_client, uptime_check_config_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ucc_client.update_uptime_check_config(
                request={
                    "uptime_check_config": {"name": uptime_check_config_path_inside}
                }
            )

    @staticmethod
    def test_update_uptime_check_config_outside(
        ucc_client, uptime_check_config_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ucc_client.update_uptime_check_config(
                request={
                    "uptime_check_config": {"name": uptime_check_config_path_outside}
                }
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_uptime_check_config_inside(
        ucc_client, uptime_check_config_path_inside
    ):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            ucc_client.delete_uptime_check_config(
                request={"name": uptime_check_config_path_inside}
            )

    @staticmethod
    def test_delete_uptime_check_config_outside(
        ucc_client, uptime_check_config_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            ucc_client.delete_uptime_check_config(
                request={"name": uptime_check_config_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message
