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

"""Google Analytics Admin API sample application which prints the conversion
event details.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.conversionEvents/get
for more information.
"""
# [START analyticsadmin_properties_conversion_events_get]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your conversion event ID
    #  (e.g. "123456") before running the sample.
    conversion_event_id = "YOUR-CONVERSION-EVENT-ID"

    get_conversion_event(property_id, conversion_event_id)


def get_conversion_event(
    property_id: str, conversion_event_id: str, transport: str = None
):
    """
    Retrieves the details for the conversion event.
    Args:
        property_id(str): The Google Analytics Property ID.
        conversion_event_id(str): The conversion event ID
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    conversion_event = client.get_conversion_event(
        name=f"properties/{property_id}/conversionEvents/{conversion_event_id}"
    )

    print("Result:")
    print(f"Resource name: {conversion_event.name}")
    print(f"Event name: {conversion_event.event_name}")
    print(f"Create time: {conversion_event.create_time}")
    print(f"Deletable: {conversion_event.deletable}")
    print(f"Custom: {conversion_event.custom}")


# [END analyticsadmin_properties_conversion_events_get]


if __name__ == "__main__":
    run_sample()
