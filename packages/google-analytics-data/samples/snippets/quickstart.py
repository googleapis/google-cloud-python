#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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
Example usage:
    python quickstart.py --property_id <PROPERTY_ID>

    where <PROPERTY_ID> is the Google Analytics property id to use for a query.

Note: you need to have the Google Analytics Data API enabled in your project
prior to running this sample. Please visit the following URL and make sure the
API is enabled:

https://console.developers.google.com/apis/library/analyticsdata.googleapis.com

This application demonstrates the usage of the Analytics Data API using
service account credentials. For more information on service accounts, see

https://cloud.google.com/iam/docs/understanding-service-accounts

The following document provides instructions on setting service account
credentials for your application:

  https://cloud.google.com/docs/authentication/production

In a nutshell, you need to:
1. Create a service account and download the key JSON file.

https://cloud.google.com/docs/authentication/production#creating_a_service_account

2. Provide service account credentials using one of the following options:
- set the GOOGLE_APPLICATION_CREDENTIALS environment variable, the API
client will use the value of this variable to find the service account key
JSON file.

https://cloud.google.com/docs/authentication/production#setting_the_environment_variable

OR
- manually pass the path to the service account key JSON file to the API client
by specifying the keyFilename parameter in the constructor:
https://cloud.google.com/docs/authentication/production#passing_the_path_to_the_service_account_key_in_code

To install the latest published package dependency, execute the following:
  pip install google-analytics-data
"""
import argparse

# [START ga_data_run_report]
from google.analytics.data_v1alpha import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.types import DateRange
from google.analytics.data_v1alpha.types import Dimension
from google.analytics.data_v1alpha.types import Entity
from google.analytics.data_v1alpha.types import Metric
from google.analytics.data_v1alpha.types import RunReportRequest


def sample_run_report(property_id):
    """Runs a simple report on a Google Analytics App+Web property."""

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = AlphaAnalyticsDataClient()
    request = RunReportRequest(entity=Entity(property_id=property_id),
                               dimensions=[Dimension(name='city')],
                               metrics=[Metric(name='activeUsers')],
                               date_ranges=[DateRange(start_date='2020-03-31',
                                                      end_date='today')])
    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)


# [END ga_data_run_report]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--property_id",
        type=str,
        required=True,
        help="Google Analytics property ID to use for a query.",
    )
    args = parser.parse_args()
    sample_run_report(args.property_id)
