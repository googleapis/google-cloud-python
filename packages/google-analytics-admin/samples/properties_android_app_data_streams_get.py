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

"""Google Analytics Admin API sample application which prints the details for
an Android app data stream.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.androidAppDataStreams/get
for more information.
"""
# [START analyticsadmin_properties_android_app_data_streams_get]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your Android app data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-ANDROID-APP-DATA-STREAM-ID"

    get_android_app_data_stream(property_id, stream_id)


def get_android_app_data_stream(property_id, stream_id):
    """Retrieves the details for an Android app data stream."""
    client = AnalyticsAdminServiceClient()
    android_app_data_stream = client.get_android_app_data_stream(
        name=f"properties/{property_id}/androidAppDataStreams/{stream_id}"
    )

    print("Result:")
    print_android_app_data_stream(android_app_data_stream)


def print_android_app_data_stream(android_app_data_stream):
    """Prints the Android app data stream details."""
    print(f"Resource name: {android_app_data_stream.name}")
    print(f"Display name: {android_app_data_stream.display_name}")
    print(f"Firebase app ID: {android_app_data_stream.firebase_app_id}")
    print(f"Package name: {android_app_data_stream.package_name}")
    print(f"Create time: {android_app_data_stream.create_time}")
    print(f"Update time: {android_app_data_stream.update_time}")


# [END analyticsadmin_properties_android_app_data_streams_get]


if __name__ == "__main__":
    run_sample()
