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
metric aggregations in a report.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.metric_aggregations
for more information.
"""
# [START analyticsdata_run_report_with_aggregations]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    MetricAggregation,
    RunReportRequest,
)

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_report_with_aggregations(property_id)


def run_report_with_aggregations(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report which includes total, maximum and minimum values for
    each metric."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="365daysAgo", end_date="today")],
        metric_aggregations=[
            MetricAggregation.TOTAL,
            MetricAggregation.MAXIMUM,
            MetricAggregation.MINIMUM,
        ],
    )
    response = client.run_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_report_with_aggregations]


if __name__ == "__main__":
    run_sample()
