#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.
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

"""Google Analytics Admin API sample application which lists measurement
protocol secrets for the data stream.

"""
# [START analyticsadmin_properties_data_streams_measurement_protocol_secrets_list]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-DATA-STREAM-ID"
    list_measurement_protocol_secrets(property_id, stream_id)


def list_measurement_protocol_secrets(
    property_id: str, stream_id: str, transport: str = None
):
    """
    Lists measurement protocol secrets for the data stream.

    Args:
        property_id(str): The Google Analytics Property ID.
        stream_id(str): The data stream ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    results = client.list_measurement_protocol_secrets(
        parent=f"properties/{property_id}/dataStreams/{stream_id}"
    )

    print("Result:")
    for measurement_protocol_secret in results:
        print("Result:")
        print(f"Resource name: {measurement_protocol_secret.name}")
        print(f"Secret value: {measurement_protocol_secret.secret_value}")
        print(f"Display name: {measurement_protocol_secret.display_name}")
        print()


# [END analyticsadmin_properties_data_streams_measurement_protocol_secrets_list]


if __name__ == "__main__":
    run_sample()
