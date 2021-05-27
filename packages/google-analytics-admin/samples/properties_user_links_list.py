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

"""Google Analytics Admin API sample application which prints user links under
the specified parent Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.userLinks/list
for more information.
"""
# [START analyticsadmin_properties_user_links_list]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    list_property_user_links(property_id)


def list_property_user_links(property_id):
    """Lists user links under the specified parent Google Analytics 4
    property."""
    client = AnalyticsAdminServiceClient()
    results = client.list_user_links(parent=f"properties/{property_id}")

    print("Result:")
    for user_link in results:
        print(user_link)
        print()


# [END analyticsadmin_properties_user_links_list]


if __name__ == "__main__":
    run_sample()
