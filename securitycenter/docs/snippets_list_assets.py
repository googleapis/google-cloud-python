#!/usr/bin/env python

# Copyright 2018, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Examples of listing assets in Cloud Security Command Center."""
import os
from datetime import datetime, timedelta


# [START organization_id]
# The numeric identifier for the organization.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
# [END organization_id]

# [START asset_resource_project_filter]
PROJECT_ASSET_FILTER = (
    "security_center_properties.resource_type="
    + '"google.cloud.resourcemanager.Project"'
)
# [END asset_resource_project_filter]


def org_name(org_id):
    """Returns the relative resource name (i.e. organizatoin/[org_id) for
    the given ord_id.

    Args:
        org_id (str) - The organizations unique numerical ID.
    """
    return "organizations/{org_id}".format(org_id=org_id)


def to_timestamp_pb2(dt):
    """Converts the given timezone aware datetime to a protocol buffer
    Timestamp.

    Args:
        dt (:class:`datetime.datetime`): The datetime to convert.
    """
    from google.api_core.datetime_helpers import to_microseconds
    from google.protobuf.timestamp_pb2 import Timestamp

    micros = to_microseconds(dt)
    MICRO_PER_SEC = 1000000
    return Timestamp(
        seconds=micros // MICRO_PER_SEC, nanos=(micros % MICRO_PER_SEC) * 1000
    )


def to_duration_pb2(delta):
    """Converts the given timedelta protocol buffer Duration.

    Args:
        delta (:class:`datetime.timedelta`): The duration to convert.
    """
    from google.api_core.datetime_helpers import to_microseconds
    from google.protobuf.duration_pb2 import Duration

    secs = int(delta.total_seconds())
    nanos = delta.microseconds * 1000
    return Duration(seconds=secs, nanos=nanos)


def test_list_all_assets():
    """Demonstrate listing and printing all assets."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_all_assets]
    client = securitycenter.SecurityCenterClient()
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    # [END demo_list_all_assets]
    assets = list(client.list_assets(org_name(ORGANIZATION_ID)))
    assert len(assets) > 0
    # [START demo_list_all_assets]
    print(assets)
    # [END demo_list_all_assets]


def test_list_assets_with_filters():
    """Demonstrate listing assets with a filter."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_assets_with_filter]
    client = securitycenter.SecurityCenterClient()

    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(
        client.list_assets(org_name(ORGANIZATION_ID), filter_=PROJECT_ASSET_FILTER)
    )
    # [END demo_list_assets_with_filter]
    assert len(assets) > 0
    # [START demo_list_assets_with_filter]
    print(assets)
    # [END demo_list_assets_with_filter]


def test_list_assets_with_filters_and_read_time():
    """Demonstrate listing assets with a filter."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_assets_with_filter_and_time]
    client = securitycenter.SecurityCenterClient()

    # Lists assets as of yesterday.
    read_time = to_timestamp_pb2(datetime.utcnow() - timedelta(days=1))
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(
        client.list_assets(
            org_name(ORGANIZATION_ID), filter_=PROJECT_ASSET_FILTER, read_time=read_time
        )
    )
    # [END demo_list_assets_with_filter_and_time]
    assert len(assets) > 0
    # [START demo_list_assets_with_filter_and_time]
    print(assets)
    # [END demo_list_assets_with_filter_and_time]


def test_list_point_in_time_changes():
    """Demonstrate listing assets along with their state changes."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_assets_changes]
    client = securitycenter.SecurityCenterClient()

    # Lists assets as of yesterday.
    read_time = datetime(2019, 3, 18)
    one_month_before = read_time - datetime(2019, 2, 18)
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(
        client.list_assets(
            org_name(ORGANIZATION_ID),
            filter_=PROJECT_ASSET_FILTER,
            read_time=to_timestamp_pb2(read_time),
            compare_duration=to_duration_pb2(one_month_before),
        )
    )
    # [END demo_list_assets_changes]
    assert len(assets) > 0
    # [START demo_list_assets_changes]
    print(assets)
    # [END demo_list_assets_changes]
