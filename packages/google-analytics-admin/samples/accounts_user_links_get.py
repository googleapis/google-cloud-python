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

"""Google Analytics Admin API sample application which prints the account user
link details.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts.userLinks/get
for more information.
"""
# [START analyticsadmin_accounts_user_links_get]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"

    # TODO(developer): Replace this variable with your Google Analytics
    #  account user link ID (e.g. "123456") before running the sample.
    account_user_link_id = "YOUR-ACCOUNT-USER-LINK-ID"

    get_account_user_link(account_id, account_user_link_id)


def get_account_user_link(account_id, account_user_link_id):
    """Retrieves the account user link details."""
    client = AnalyticsAdminServiceClient()
    user_link = client.get_user_link(
        name=f"accounts/{account_id}/userLinks/{account_user_link_id}"
    )

    print("Result:")
    print_user_link(user_link)


def print_user_link(user_link):
    """Prints the user link details."""
    print(f"Resource name: {user_link.name}")
    print(f"Email address: {user_link.email_address}")
    for direct_role in user_link.direct_roles:
        print(f"Direct role: {direct_role}")


# [END analyticsadmin_accounts_user_links_get]


if __name__ == "__main__":
    run_sample()
