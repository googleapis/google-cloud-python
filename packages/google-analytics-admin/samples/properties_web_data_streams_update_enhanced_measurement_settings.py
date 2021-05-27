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

"""Google Analytics Admin API sample application which updates the enhanced
measurement settings for the web stream.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.webDataStreams/updateEnhancedMeasurementSettings
for more information.
"""
# [START analyticsadmin_properties_web_data_streams_update_enhanced_measurement_settings]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import EnhancedMeasurementSettings
from google.protobuf.field_mask_pb2 import FieldMask



def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics property ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your web data stream ID
    #  (e.g. "123456") before running the sample.
    stream_id = "YOUR-WEB-DATA-STREAM-ID"

    update_enhanced_measurement_settings(property_id, stream_id)


def update_enhanced_measurement_settings(property_id, stream_id):
    """Updates the enhanced measurement settings for the web stream."""
    client = AnalyticsAdminServiceClient()
    # This call updates the `streamEnabled`, `fileDownloadsEnabled` measurement
    # settings of the web data stream, as indicated by the value of the
    # `update_mask` field. The web data stream to update is specified in the
    # `name` field of the `EnhancedMeasurementSettings` instance.
    enhanced_measurement_settings = client.update_enhanced_measurement_settings(
        enhanced_measurement_settings=EnhancedMeasurementSettings(
            name=f"properties/{property_id}/webDataStreams/{stream_id}/enhancedMeasurementSettings",
            stream_enabled=False,
            file_downloads_enabled=False,
        ),
        update_mask=FieldMask(paths=["stream_enabled", "file_downloads_enabled"]),
    )

    print("Result:")
    print(enhanced_measurement_settings)


# [END analyticsadmin_properties_web_data_streams_update_enhanced_measurement_settings]


if __name__ == "__main__":
    run_sample()
