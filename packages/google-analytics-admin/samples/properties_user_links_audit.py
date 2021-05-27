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

"""Google Analytics Admin API sample application which prints user links audit
data on the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.userLinks/audit
for more information.
"""
# [START analyticsadmin_properties_user_links_audit]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import AuditUserLinksRequest


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    audit_property_user_links(property_id)


def audit_property_user_links(property_id):
    """Lists all user links on the Google Analytics 4 property, including
    implicit ones that come from effective permissions granted by groups or
    organization admin roles."""
    client = AnalyticsAdminServiceClient()
    results = client.audit_user_links(
        AuditUserLinksRequest(parent=f"properties/{property_id}")
    )

    print("Result:")
    for user_link in results:
        print(f"Resource name: {user_link.name}")
        print(f"Email address: {user_link.email_address}")
        for direct_role in user_link.direct_roles:
            print(f"Direct role: {direct_role}")

        for effective_role in user_link.effective_roles:
            print(f"Effective role: {effective_role}")
        print()


# [END analyticsadmin_properties_user_links_audit]


if __name__ == "__main__":
    run_sample()
