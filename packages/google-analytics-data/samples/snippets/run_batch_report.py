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

"""Google Analytics Data API sample application demonstrating the batch creation
of multiple reports.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/batchRunReports
for more information.
"""
# [START analyticsdata_run_batch_report]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import BatchRunReportsRequest
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_batch_report(property_id)


def run_batch_report(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a batch report on a Google Analytics 4 property."""
    client = BetaAnalyticsDataClient()

    request = BatchRunReportsRequest(
        property=f"properties/{property_id}",
        requests=[
            RunReportRequest(
                dimensions=[
                    Dimension(name="country"),
                    Dimension(name="region"),
                    Dimension(name="city"),
                ],
                metrics=[Metric(name="activeUsers")],
                date_ranges=[DateRange(start_date="2021-01-03", end_date="2021-01-09")],
            ),
            RunReportRequest(
                dimensions=[Dimension(name="browser")],
                metrics=[Metric(name="activeUsers")],
                date_ranges=[DateRange(start_date="2021-01-01", end_date="2021-01-31")],
            ),
        ],
    )
    response = client.batch_run_reports(request)

    print("Batch report results:")
    for report in response.reports:
        print_run_report_response(report)


# [END analyticsdata_run_batch_report]


if __name__ == "__main__":
    run_sample()
