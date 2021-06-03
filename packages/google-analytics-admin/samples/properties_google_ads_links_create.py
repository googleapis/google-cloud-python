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

"""Google Analytics Admin API sample application which creates a Google Ads
link for the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.googleAdsLinks/create
for more information.
"""
# [START analyticsadmin_properties_google_ads_links_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import GoogleAdsLink


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with a ten-digit Google Ads
    #  customer ID (digits only, e.g. "1234567890").
    #  This Google Ads account will be linked to the GA4 property.
    google_ads_customer_id = "YOUR-GOOGLE-ADS-CUSTOMER-ID"

    create_google_ads_link(property_id, google_ads_customer_id)


def create_google_ads_link(property_id, google_ads_customer_id):
    """Creates a Google Ads link for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    google_ads_link = client.create_google_ads_link(
        parent=f"properties/{property_id}",
        google_ads_link=GoogleAdsLink(customer_id=f"{google_ads_customer_id}"),
    )

    print("Result:")
    print(google_ads_link)


# [END analyticsadmin_properties_google_ads_links_create]

if __name__ == "__main__":
    run_sample()
