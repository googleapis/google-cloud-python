#!/usr/bin/env python
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

""" Examples of listing assets in Cloud Security Command Center."""
import os
from datetime import datetime, timedelta


# The numeric identifier for the organization.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]


def test_list_all_assets():
    """Demonstrate listing and printing all assets."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_all_assets]
    client = securitycenter.SecurityCenterClient()
    # ORGANIZATION_ID is the numeric ID of the organization (e.g. 123213123121)
    org_name = "organizations/{org_id}".format(org_id=ORGANIZATION_ID)
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(client.list_assets(org_name))
    # [END demo_list_all_assets]
    assert len(assets) > 0
    # [START demo_list_all_assets]
    print(assets)
    # [END demo_list_all_assets]


def test_list_assets_with_filters():
    """Demonstrate listing assets with a filter."""
    from google.cloud import securitycenter_v1beta1 as securitycenter

    # [START demo_list_assets_with_filter]
    client = securitycenter.SecurityCenterClient()

    # ORGANIZATION_ID is the numeric ID of the organization (e.g. 123213123121)
    org_name = "organizations/{org_id}".format(org_id=ORGANIZATION_ID)

    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(client.list_assets(org_name, filter_=project_filter))
    # [END demo_list_assets_with_filter]
    assert len(assets) > 0
    # [START demo_list_assets_with_filter]
    print(assets)
    # [END demo_list_assets_with_filter]


def test_list_assets_with_filters_and_read_time():
    """Demonstrate listing assets with a filter."""
    from datetime import datetime, timedelta
    from google.cloud import securitycenter_v1beta1 as securitycenter
    from google.protobuf.timestamp_pb2 import Timestamp

    # [START demo_list_assets_with_filter_and_time]
    client = securitycenter.SecurityCenterClient()

    # ORGANIZATION_ID is the numeric ID of the organization (e.g. 123213123121)
    org_name = "organizations/{org_id}".format(org_id=ORGANIZATION_ID)

    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )

    # Lists assets as of yesterday.
    read_time = datetime.utcnow() - timedelta(days=1)
    timestamp_proto = Timestamp()
    timestamp_proto.FromDatetime(read_time)

    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(
        client.list_assets(org_name, filter_=project_filter, read_time=timestamp_proto)
    )
    # [END demo_list_assets_with_filter_and_time]
    assert len(assets) > 0
    # [START demo_list_assets_with_filter_and_time]
    print(assets)
    # [END demo_list_assets_with_filter_and_time]


def test_list_point_in_time_changes():
    """Demonstrate listing assets along with their state changes."""
    from google.cloud import securitycenter_v1beta1 as securitycenter
    from google.protobuf.duration_pb2 import Duration
    from datetime import timedelta

    # [START demo_list_assets_changes]
    client = securitycenter.SecurityCenterClient()

    # ORGANIZATION_ID is the numeric ID of the organization (e.g. 123213123121)
    org_name = "organizations/{org_id}".format(org_id=ORGANIZATION_ID)

    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )

    # List assets and their state change the last 30 days
    compare_delta = timedelta(days=30)
    # Convert the timedelta to a Duration
    duration_proto = Duration()
    duration_proto.FromTimedelta(compare_delta)
    # list_assets returns an iterator.  We convert it to a list
    # here for demonstration purposes only.  Processing each element
    # from the iterator is recommended.
    assets = list(
        client.list_assets(
            org_name, filter_=project_filter, compare_duration=duration_proto
        )
    )
    # [END demo_list_assets_changes]
    assert len(assets) > 0
    # [START demo_list_assets_changes]
    print(assets)
    # [END demo_list_assets_changes]
