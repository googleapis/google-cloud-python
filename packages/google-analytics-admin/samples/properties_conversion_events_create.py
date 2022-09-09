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

"""Google Analytics Admin API sample application which creates a conversion
event for the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.conversionEvents/create
for more information.
"""
# [START analyticsadmin_properties_conversion_events_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha import ConversionEvent


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    create_conversion_event(property_id)


def create_conversion_event(property_id: str, transport: str = None):
    """
    Creates a conversion event for the Google Analytics 4 property.

    Args:
        property_id(str): The Google Analytics Property ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    conversion_event = client.create_conversion_event(
        parent=f"properties/{property_id}",
        conversion_event=ConversionEvent(event_name="test_purchase"),
    )

    print("Result:")
    print(f"Resource name: {conversion_event.name}")
    print(f"Event name: {conversion_event.event_name}")
    print(f"Create time: {conversion_event.create_time}")
    print(f"Deletable: {conversion_event.deletable}")
    print(f"Custom: {conversion_event.custom}")


# [END analyticsadmin_properties_conversion_events_create]

if __name__ == "__main__":
    run_sample()
