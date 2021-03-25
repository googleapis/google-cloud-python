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

"""Google Analytics Data API sample quickstart application.

This application demonstrates the usage of the Analytics Data API using
OAuth2 credentials.

Before you start the application, please review the comments starting with
"TODO(developer)" and update the code to use correct values.

Usage:
  pip3 install --upgrade google-auth-oauthlib
  pip3 install --upgrade google-analytics-data
  python3 quickstart_oauth2.py
"""
# [START analyticsdata_quickstart_oauth2]
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google_auth_oauthlib import flow


def sample_run_report(credentials=None, property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    client = BetaAnalyticsDataClient(credentials=credentials)
    request = RunReportRequest(
        property="properties/" + str(property_id),
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
    )

    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)


def get_credentials():
    """Creates an OAuth2 credentials instance."""
    # [START analyticsdata_initialize]
    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    # TODO(developer): Update the line below to set the `launch_browser` variable.
    # The `launch_browser` boolean variable indicates if a local server is used
    # as the callback URL in the auth flow. A value of `True` is recommended,
    # but a local server does not work if accessing the application remotely,
    # such as over SSH or from a remote Jupyter notebook.
    launch_browser = True
    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()
    return appflow.credentials
    # [END analyticsdata_initialize]


def main():
    credentials = get_credentials()
    sample_run_report(credentials)


# [END analyticsdata_quickstart_oauth2]

if __name__ == "__main__":
    main()
