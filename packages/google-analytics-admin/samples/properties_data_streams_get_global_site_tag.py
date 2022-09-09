#!/usr/bin/env python

# Copyright 2021 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Admin API sample application which prints the Site Tag data
for the specified web stream.
"""
# [START analyticsadmin_properties_data_streams_get_global_site_tag]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-DATA-STREAM-ID"

    get_global_site_tag(property_id, stream_id)


def get_global_site_tag(property_id: str, stream_id: str, transport: str = None):
    """
    Retrieves the Site Tag for the specified data stream.

    Args:
        property_id(str): The Google Analytics Property ID.
        stream_id(str): The data stream ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    global_site_tag = client.get_global_site_tag(
        name=f"properties/{property_id}/dataStreams/{stream_id}/globalSiteTag"
    )

    print("Result:")
    print(global_site_tag.snippet)


# [END analyticsadmin_properties_data_streams_get_global_site_tag]


if __name__ == "__main__":
    run_sample()
