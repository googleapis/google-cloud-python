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

"""Google Analytics Admin API sample application which prints the data sharing
settings on an account.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/getDataSharingSettings
for more information.
"""
# [START analyticsadmin_accounts_get_data_sharing_settings]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""

    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    get_data_sharing_settings(account_id)


def get_data_sharing_settings(account_id: str):
    """Gets data sharing settings on an account."""
    client = AnalyticsAdminServiceClient()
    data_sharing_settings = client.get_data_sharing_settings(
        name=f"accounts/{account_id}/dataSharingSettings"
    )

    print("Result:")
    print(f"Resource name: {data_sharing_settings.name}")
    print(
        f"Sharing with Google support enabled: {data_sharing_settings.sharing_with_google_support_enabled}"
    )
    print(
        f"Sharing with Google assigned sales enabled: {data_sharing_settings.sharing_with_google_assigned_sales_enabled}"
    )
    print(
        f"Sharing with others enabled: {data_sharing_settings.sharing_with_others_enabled}"
    )


# [END analyticsadmin_accounts_get_data_sharing_settings]


if __name__ == "__main__":
    run_sample()
