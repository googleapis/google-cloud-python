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

"""Google Analytics Admin API sample application which prints the enhanced
measurement settings for the web stream.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.webDataStreams/getEnhancedMeasurementSettings
for more information.
"""
# [START analyticsadmin_properties_web_data_streams_get_enhanced_measurement_settings]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your web data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-WEB-DATA-STREAM-ID"

    get_enhanced_measurement_settings(property_id, stream_id)


def get_enhanced_measurement_settings(property_id, stream_id):
    """Retrieves the enhanced measurement settings for the web stream."""
    client = AnalyticsAdminServiceClient()
    enhanced_measurement_settings = client.get_enhanced_measurement_settings(
        name=f"properties/{property_id}/webDataStreams/{stream_id}/enhancedMeasurementSettings"
    )

    print("Result:")
    print_enhanced_measurement_settings(enhanced_measurement_settings)


def print_enhanced_measurement_settings(enhanced_measurement_settings):
    """Prints the enhanced measurement settings for a web stream."""
    print(f"Resource name: {enhanced_measurement_settings.name}")
    print(f"Stream enabled: {enhanced_measurement_settings.streamEnabled}")
    print(f"Page views enabled: {enhanced_measurement_settings.pageViewsEnabled}")
    print(f"Scrolls enabled: {enhanced_measurement_settings.scrollsEnabled}")
    print(
        f"Outbound clicks enabled: {enhanced_measurement_settings.outboundClicksEnabled}"
    )
    print(f"Site search enabled: {enhanced_measurement_settings.siteSearchEnabled}")
    print(
        f"Video engagement enabled: {enhanced_measurement_settings.videoEngagementEnabled}"
    )
    print(
        f"File downloads enabled: {enhanced_measurement_settings.fileDownloadsEnabled}"
    )
    print(f"Page loads enabled: {enhanced_measurement_settings.pageLoadsEnabled}")
    print(f"Page changes enabled: {enhanced_measurement_settings.pageChangesEnabled}")
    print(
        f"Search query parameter: {enhanced_measurement_settings.searchQueryParameter}"
    )
    print(f"Uri query parameter: {enhanced_measurement_settings.uriQueryParameter}")


# [END analyticsadmin_properties_web_data_streams_get_enhanced_measurement_settings]


if __name__ == "__main__":
    run_sample()
