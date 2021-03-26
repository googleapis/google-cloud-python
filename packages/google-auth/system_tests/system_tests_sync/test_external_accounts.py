# Copyright 2021 Google LLC
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

# Prerequisites:
# Make sure to run the setup in scripts/setup_external_accounts.sh
# and copy the logged constant strings (_AUDIENCE_OIDC, _AUDIENCE_AWS)
# into this file before running this test suite.
# Once that is done, this test can be run indefinitely.
#
# The only requirement for this test suite to run is to set the environment
# variable GOOGLE_APPLICATION_CREDENTIALS to point to the expected service
# account keys whose email is referred to in the setup script.
#
# This script follows the following logic.
# OIDC provider (file-sourced and url-sourced credentials):
# Use the service account keys to generate a Google ID token using the
# iamcredentials generateIdToken API, using the default STS audience.
# This will use the service account client ID as the sub field of the token.
# This OIDC token will be used as the external subject token to be exchanged
# for a Google access token via GCP STS endpoint and then to impersonate the
# original service account key.


import json
import os
from tempfile import NamedTemporaryFile

import sys
import google.auth
from googleapiclient import discovery
from google.oauth2 import service_account
import pytest
from mock import patch

# Populate values from the output of scripts/setup_external_accounts.sh.
_AUDIENCE_OIDC = "//iam.googleapis.com/projects/79992041559/locations/global/workloadIdentityPools/pool-73wslmxn/providers/oidc-73wslmxn"


def dns_access_direct(request, project_id):
    # First, get the default credentials.
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform.read-only"],
        request=request,
    )

    # Apply the default credentials to the headers to make the request.
    headers = {}
    credentials.apply(headers)
    response = request(
        url="https://dns.googleapis.com/dns/v1/projects/{}".format(project_id),
        headers=headers,
    )

    if response.status == 200:
        return response.data


def dns_access_client_library(_, project_id):
    service = discovery.build("dns", "v1")
    request = service.projects().get(project=project_id)
    return request.execute()


@pytest.fixture(params=[dns_access_direct, dns_access_client_library])
def dns_access(request, http_request, service_account_info):
    # Fill in the fixtures on the functions,
    # so that we don't have to fill in the parameters manually.
    def wrapper():
        return request.param(http_request, service_account_info["project_id"])

    yield wrapper


@pytest.fixture
def oidc_credentials(service_account_file, http_request):
    result = service_account.IDTokenCredentials.from_service_account_file(
        service_account_file, target_audience=_AUDIENCE_OIDC
    )
    result.refresh(http_request)
    yield result


@pytest.fixture
def service_account_info(service_account_file):
    with open(service_account_file) as f:
        yield json.load(f)


# Our external accounts tests involve setting up some preconditions, setting a
# credential file, and then making sure that our client libraries can work with
# the set credentials.
def get_project_dns(dns_access, credential_data):
    with NamedTemporaryFile() as credfile:
        credfile.write(json.dumps(credential_data).encode("utf-8"))
        credfile.flush()
        old_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        with patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": credfile.name}):
            # If our setup and credential file are correct,
            # discovery.build should be able to establish these as the default credentials.
            return dns_access()


# This test makes sure that setting an accesible credential file
# works to allow access to Google resources.
def test_file_based_external_account(
    oidc_credentials, service_account_info, dns_access
):
    with NamedTemporaryFile() as tmpfile:
        tmpfile.write(oidc_credentials.token.encode("utf-8"))
        tmpfile.flush()

        assert get_project_dns(
            dns_access,
            {
                "type": "external_account",
                "audience": _AUDIENCE_OIDC,
                "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
                "token_url": "https://sts.googleapis.com/v1/token",
                "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{}:generateAccessToken".format(
                    oidc_credentials.service_account_email
                ),
                "credential_source": {
                    "file": tmpfile.name,
                },
            },
        )
