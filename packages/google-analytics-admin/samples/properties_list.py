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

"""Google Analytics Admin API sample application which prints Google Analytics 4
properties under the specified parent account that are available to the
current user.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/list
for more information.
"""
# [START analyticsadmin_properties_list]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import ListPropertiesRequest


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    list_properties(account_id)


def list_properties(account_id):
    """Lists Google Analytics 4 properties under the specified parent account
    that are available to the current user."""
    client = AnalyticsAdminServiceClient()
    results = client.list_properties(
        ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=True)
    )

    print("Result:")
    for property_ in results:
        print(property_)
        print()


# [END analyticsadmin_properties_list]


if __name__ == "__main__":
    run_sample()
