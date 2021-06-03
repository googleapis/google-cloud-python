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

"""Google Analytics Admin API sample application which creates a Google
Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/create
for more information.
"""
# [START analyticsadmin_properties_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import Property


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    create_property(account_id)


def create_property(account_id):
    """Creates a Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    property_ = client.create_property(
        property=Property(
            parent=f"accounts/{account_id}",
            currency_code="USD",
            display_name="Test property",
            industry_category="OTHER",
            time_zone="America/Los_Angeles",
        )
    )

    print("Result:")
    print(property_)


# [END analyticsadmin_properties_create]


if __name__ == "__main__":
    run_sample()
