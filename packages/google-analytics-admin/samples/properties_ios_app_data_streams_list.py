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

"""Google Analytics Admin API sample application which prints iOS app data
streams for the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.iosAppDataStreams/list
for more information.
"""
# [START analyticsadmin_properties_ios_app_data_streams_list]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    list_ios_app_data_streams(property_id)


def list_ios_app_data_streams(property_id):
    """Lists iOS app data streams for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    results = client.list_ios_app_data_streams(parent=f"properties/{property_id}")

    print("Result:")
    for ios_app_data_stream in results:
        print(ios_app_data_stream)
        print()


# [END analyticsadmin_properties_ios_app_data_streams_list]


if __name__ == "__main__":
    run_sample()
