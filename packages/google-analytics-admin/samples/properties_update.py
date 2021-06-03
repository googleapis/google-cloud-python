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

"""Google Analytics Admin API sample application.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/update
for more information.
"""
# [START analyticsadmin_properties_update]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import Property
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
    update_property(property_id)


def update_property(property_id):
    """Updates the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    # This call updates the display name, industry category and time zone of the
    # property, as indicated by the value of the `update_mask` field.
    # The property to update is specified in the `name` field of the `Property`
    # instance.
    property_ = client.update_property(
        property=Property(
            name=f"properties/{property_id}",
            display_name="This is an updated test property",
            industry_category="GAMES",
            time_zone="America/New_York",
        ),
        update_mask=FieldMask(paths=["display_name", "time_zone", "industry_category"]),
    )

    print("Result:")
    print(property_)


# [END analyticsadmin_properties_update]


if __name__ == "__main__":
    run_sample()
