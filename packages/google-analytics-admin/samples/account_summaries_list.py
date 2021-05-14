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

"""Google Analytics Admin API sample application which prints summaries of
all accounts accessible by the caller.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accountSummaries/list
for more information.
"""
# [START analyticsadmin_account_summaries_list]
from google.analytics.admin import AnalyticsAdminServiceClient


def list_account_summaries():
    """Returns summaries of all accounts accessible by the caller."""
    client = AnalyticsAdminServiceClient()
    results = client.list_account_summaries()

    print("Result:")
    for account_summary in results:
        print("-- Account --")
        print(f"Resource name: {account_summary.name}")
        print(f"Account name: {account_summary.account}")
        print(f"Display name: {account_summary.display_name}")
        print()
        for property_summary in account_summary.property_summaries:
            print("-- Property --")
            print(f"Property resource name: {property_summary.property}")
            print(f"Property display name: {property_summary.display_name}")
            print()


# [END analyticsadmin_account_summaries_list]


if __name__ == "__main__":
    list_account_summaries()
