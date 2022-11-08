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

"""Google Analytics Data API sample application demonstrating the ordering of
 report rows.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.order_bys
for more information.
"""
# [START analyticsdata_run_report_with_ordering]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    RunReportRequest,
)

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_report_with_ordering(property_id)


def run_report_with_ordering(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report of active users grouped by three dimensions, ordered by
    the total revenue in descending order."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="totalRevenue"),
        ],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        order_bys=[
            OrderBy(metric=OrderBy.MetricOrderBy(metric_name="totalRevenue"), desc=True)
        ],
    )
    response = client.run_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_report_with_ordering]


if __name__ == "__main__":
    run_sample()
