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
dimension and metric filters in a report.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.dimension_filter
for more information.
"""
# [START analyticsdata_run_report_with_dimension_and_metric_filters]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import NumericValue
from google.analytics.data_v1beta.types import RunReportRequest

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_report_with_dimension_and_metric_filters(property_id)


def run_report_with_dimension_and_metric_filters(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report using both metric and dimension filters. A dimension filter
    limits the report to include only users who made an in-app purchase using
    Android platform. A metric filter specifies that only users with session
    counts larger than 1,000 should be included."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
        metric_filter=FilterExpression(
            filter=Filter(
                field_name="sessions",
                numeric_filter=Filter.NumericFilter(
                    operation=Filter.NumericFilter.Operation.GREATER_THAN,
                    value=NumericValue(int64_value=1000),
                ),
            )
        ),
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(
                        filter=Filter(
                            field_name="platform",
                            string_filter=Filter.StringFilter(
                                match_type=Filter.StringFilter.MatchType.EXACT,
                                value="Android",
                            ),
                        )
                    ),
                    FilterExpression(
                        filter=Filter(
                            field_name="eventName",
                            string_filter=Filter.StringFilter(
                                match_type=Filter.StringFilter.MatchType.EXACT,
                                value="in_app_purchase",
                            ),
                        )
                    ),
                ]
            )
        ),
    )
    response = client.run_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_report_with_dimension_and_metric_filters]


if __name__ == "__main__":
    run_sample()
