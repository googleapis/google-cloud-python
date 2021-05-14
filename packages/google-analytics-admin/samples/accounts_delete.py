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

"""Google Analytics Admin API sample application which deletes a Google
Analytics account.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/delete
for more information.
"""
# [START analyticsadmin_accounts_delete]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    # your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    delete_account(account_id)


def delete_account(account_id: str):
    """Deletes the Google Analytics account."""
    client = AnalyticsAdminServiceClient()
    client.delete_account(name=f"accounts/{account_id}")
    print("Account deleted")


# [END analyticsadmin_accounts_delete]


if __name__ == "__main__":
    run_sample()
