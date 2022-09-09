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

"""Google Analytics Admin API sample application which creates a measurement
protocol secret for the data stream.

"""
# [START analyticsadmin_properties_data_streams_measurement_protocol_secrets_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha import MeasurementProtocolSecret


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics property ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-DATA-STREAM-ID"

    create_measurement_protocol_secret(property_id, stream_id)


def create_measurement_protocol_secret(
    property_id: str, stream_id: str, transport: str = None
):
    """
    Creates a measurement protocol secret for the data stream.

    Args:
        property_id(str): The Google Analytics Property ID.
        stream_id(str): The data stream ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    measurement_protocol_secret = client.create_measurement_protocol_secret(
        parent=f"properties/{property_id}/dataStreams/{stream_id}",
        measurement_protocol_secret=MeasurementProtocolSecret(
            display_name="New secret"
        ),
    )

    print("Result:")
    print(f"Resource name: {measurement_protocol_secret.name}")
    print(f"Secret value: {measurement_protocol_secret.secret_value}")
    print(f"Display name: {measurement_protocol_secret.display_name}")


# [END analyticsadmin_properties_data_streams_measurement_protocol_secrets_create]


if __name__ == "__main__":
    run_sample()
