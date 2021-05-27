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

"""Google Analytics Admin API sample application which creates a web data stream
for the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.webDataStreams/create
for more information.
"""
# [START analyticsadmin_properties_web_data_streams_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import WebDataStream


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    create_web_data_stream(property_id)


def create_web_data_stream(property_id):
    """Creates a web data stream for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    web_data_stream = client.create_web_data_stream(
        parent=f"properties/{property_id}",
        web_data_stream=WebDataStream(
            default_uri="https://www.google.com", display_name="Test web data stream"
        ),
    )

    print("Result:")
    print(web_data_stream)


# [END analyticsadmin_properties_web_data_streams_create]


if __name__ == "__main__":
    run_sample()
