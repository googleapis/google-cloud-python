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

"""Google Analytics Admin API sample application which prints the Google
Analytics account data.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/get
for more information.
"""
# [START analyticsadmin_accounts_get]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    get_account(account_id)


def get_account(account_id: str):
    """Retrieves the Google Analytics account data."""
    client = AnalyticsAdminServiceClient()
    account = client.get_account(name=f"accounts/{account_id}")

    print("Result:")
    print_account(account)


def print_account(account: str):
    """Prints account data."""
    print(f"Resource name: {account.name}")
    print(f"Display name: {account.display_name}")
    print(f"Region code: {account.region_code}")
    print(f"Create time: {account.create_time}")
    print(f"Update time: {account.update_time}")


# [END analyticsadmin_accounts_get]


if __name__ == "__main__":
    run_sample()
