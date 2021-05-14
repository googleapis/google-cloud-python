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

"""Google Analytics Admin API sample application which updates the Google
Analytics account.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/update
for more information.
"""
# [START analyticsadmin_accounts_update]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import Account
from google.protobuf.field_mask_pb2 import FieldMask

from accounts_get import print_account


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    # your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"
    update_account(account_id)


def update_account(account_id: str):
    """Updates the Google Analytics account."""
    client = AnalyticsAdminServiceClient()
    # This call updates the display name and region code of the account, as
    # indicated by the value of the `update_mask` field.
    # The account to update is specified in the `name` field of the `Account`
    # instance.
    account = client.update_account(
        account=Account(
            name=f"accounts/{account_id}",
            display_name="This is a test account",
            region_code="US",
        ),
        update_mask=FieldMask(paths=["display_name", "region_code"]),
    )

    print("Result:")
    print_account(account)


# [END analyticsadmin_accounts_update]


if __name__ == "__main__":
    run_sample()
