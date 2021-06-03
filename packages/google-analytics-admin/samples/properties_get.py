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

"""Google Analytics Admin API sample application which print the Google
Analytics 4 property details.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/get
for more information.
"""
# [START analyticsadmin_properties_get]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import IndustryCategory


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    get_property(property_id)


def get_property(property_id):
    """Retrieves the Google Analytics 4 property details."""
    client = AnalyticsAdminServiceClient()
    property_ = client.get_property(name=f"properties/{property_id}")

    print("Result:")
    print_property(property_)


def print_property(property):
    """Prints the Google Analytics 4 property details."""
    print(f"Resource name: {property.name}")
    print(f"Parent: {property.parent}")
    print(f"Display name: {property.display_name}")
    print(f"Create time: {property.create_time}")
    print(f"Update time: {property.update_time}")
    # print(f"Delete time: {property.delete_time}")
    # print(f"Expire time: {property.expire_time}")

    if property.industry_category:
        print(f"Industry category: {IndustryCategory(property.industry_category).name}")

    print(f"Time zone: {property.time_zone}")
    print(f"Currency code: {property.currency_code}")


# [END analyticsadmin_properties_get]


if __name__ == "__main__":
    run_sample()
