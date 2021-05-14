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

"""Google Analytics Admin API sample application which provisions the Google
Analytics account creation ticket and prints the Terms of Service link that
can be used by an end user to complete the account creation flow.

This sample invokes the provision_account_ticket() method of the Google
Analytics Admin API to start the Google Analytics account creation
process for a user. This method returns an account ticket which shall be used
to generate the Terms Of Service url that an end user should visit in order
to accept the Terms and complete the account creation flow.

You have to authenticate as an end user in order to run this sample. Only
the authenticated user will be able to use the Terms of Service url generated
as part of the account provisioning flow.

To authenticate as an end user prior to running this sample, use the
gcloud tool:

 gcloud auth application-default login --scopes=https://www.googleapis.com/auth/analytics.edit --client-id-file=PATH_TO_YOUR_CLIENT_SECRET_JSON


See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/provisionAccountTicket
for more information.
"""
# [START analyticsadmin_accounts_provision_account_ticket]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import Account
from google.analytics.admin_v1alpha.types import ProvisionAccountTicketRequest


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with a redirect URI where the user
    #  will be sent after accepting Terms of Service. Must be configured in
    #  Developers Console as a Redirect URI
    redirect_uri = "YOUR-REDIRECT-URI"

    provision_account_ticket(redirect_uri)


def provision_account_ticket(redirect_uri: str):
    """Provisions the Google Analytics account creation ticket."""
    client = AnalyticsAdminServiceClient()
    response = client.provision_account_ticket(
        ProvisionAccountTicketRequest(
            account=Account(display_name="Test Account", region_code="US"),
            redirect_uri=redirect_uri,
        )
    )

    print("Result:")
    print(f"Account ticket id: {response.account_ticket_id}")
    print(
        f"You can now open the following URL to complete the account creation:"
        f"https://analytics.google.com/analytics/web/?provisioningSignup=false#/termsofservice/{response.account_ticket_id}"
    )
    print()
    print(
        "Attention: make sure your browser is signed in to the same user "
        "account that was used to provision the ticket."
    )


# [END analyticsadmin_accounts_provision_account_ticket]


if __name__ == "__main__":
    run_sample()
