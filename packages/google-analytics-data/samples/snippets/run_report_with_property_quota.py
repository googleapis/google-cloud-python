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

"""Google Analytics Data API sample application demonstrating the usage of
property quota metadata.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.return_property_quota
for more information.
"""
# [START analyticsdata_run_report_with_property_quota]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_report_with_property_quota(property_id)


def run_report_with_property_quota(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report and prints property quota information."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        return_property_quota=True,
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )
    response = client.run_report(request)

    # [START analyticsdata_run_report_with_property_quota_print_response]
    if response.property_quota:
        print(
            f"Tokens per day quota consumed: {response.property_quota.tokens_per_day.consumed}, "
            f"remaining: {response.property_quota.tokens_per_day.remaining}."
        )

        print(
            f"Tokens per hour quota consumed: {response.property_quota.tokens_per_hour.consumed}, "
            f"remaining: {response.property_quota.tokens_per_hour.remaining}."
        )

        print(
            f"Concurrent requests quota consumed: {response.property_quota.concurrent_requests.consumed}, "
            f"remaining: {response.property_quota.concurrent_requests.remaining}."
        )

        print(
            f"Server errors per project per hour quota consumed: {response.property_quota.server_errors_per_project_per_hour.consumed}, "
            f"remaining: {response.property_quota.server_errors_per_project_per_hour.remaining}."
        )
        print(
            f"Potentially thresholded requests per hour quota consumed: {response.property_quota.potentially_thresholded_requests_per_hour.consumed}, "
            f"remaining: {response.property_quota.potentially_thresholded_requests_per_hour.remaining}."
        )
    # [END analyticsdata_run_report_with_property_quota_print_response]


# [END analyticsdata_run_report_with_property_quota]


if __name__ == "__main__":
    run_sample()
