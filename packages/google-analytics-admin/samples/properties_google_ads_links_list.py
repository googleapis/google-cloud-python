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

"""Google Analytics Admin API sample application which prints Google Ads links
under the specified parent Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.googleAdsLinks/list
for more information.
"""
# [START analyticsadmin_properties_google_ads_links_list]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    list_google_ads_links(property_id)


def list_google_ads_links(property_id):
    """Lists Google Ads links under the specified parent Google Analytics 4
    property."""
    client = AnalyticsAdminServiceClient()
    results = client.list_google_ads_links(parent=f"properties/{property_id}")

    print("Result:")
    for google_ads_link in results:
        print_google_ads_link(google_ads_link)
        print()


def print_google_ads_link(google_ads_link):
    """Prints the Google Ads link details."""
    print(f"Resource name: {google_ads_link.name}")
    print(f"Google Ads customer ID: {google_ads_link.customer_id}")
    print(f"Can manage clients: {google_ads_link.can_manage_clients}")
    print(f"Ads personalization enabled: {google_ads_link.ads_personalization_enabled}")
    print(f"Email address of the link creator: {google_ads_link.email_address}")
    print(f"Create time: {google_ads_link.create_time}")
    print(f"Update time: {google_ads_link.update_time}")


# [END analyticsadmin_properties_google_ads_links_list]


if __name__ == "__main__":
    run_sample()
