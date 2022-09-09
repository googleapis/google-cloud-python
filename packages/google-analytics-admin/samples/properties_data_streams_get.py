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

"""Google Analytics Admin API sample application which prints the details for
the data stream.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams/get
for more information.
"""
# [START analyticsadmin_properties_data_streams_get]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-DATA-STREAM-ID"

    get_data_stream(property_id, stream_id)


def get_data_stream(property_id: str, stream_id: str, transport: str = None):
    """
    Retrieves the details for the data stream.

    Args:
        property_id(str): The Google Analytics Property ID.
        stream_id(str): The data stream ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    data_stream = client.get_data_stream(
        name=f"properties/{property_id}/dataStreams/{stream_id}"
    )

    print("Result:")
    print_data_stream(data_stream)


def print_data_stream(data_stream):
    """Prints the data stream details."""
    print(f"Resource name: {data_stream.name}")
    print(f"Display name: {data_stream.display_name}")
    print(f"Type: {data_stream.type}")
    print(f"Default URI: {data_stream.web_stream_data.default_uri}")
    print(f"Measurement ID: {data_stream.web_stream_data.measurement_id}")
    print(f"Firebase App ID: {data_stream.web_stream_data.firebase_app_id}")
    print(f"Create time: {data_stream.create_time}")
    print(f"Update time: {data_stream.update_time}")


# [END analyticsadmin_properties_data_streams_get]


if __name__ == "__main__":
    run_sample()
