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
# [START analyticsdata_run_report_with_multiple_dimension_filters]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_report_with_multiple_dimension_filters(property_id)


def run_report_with_multiple_dimension_filters(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report using multiple dimension filters joined as `and_group`
    expression. The filter selects for when both `browser` is `Chrome` and
    `countryId` is `US`.

    This sample uses relative date range values. See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/DateRange
    for more information.
    """
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="browser")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(
                        filter=Filter(
                            field_name="browser",
                            string_filter=Filter.StringFilter(value="Chrome"),
                        )
                    ),
                    FilterExpression(
                        filter=Filter(
                            field_name="countryId",
                            string_filter=Filter.StringFilter(value="US"),
                        )
                    ),
                ]
            )
        ),
    )
    response = client.run_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_report_with_multiple_dimension_filters]


if __name__ == "__main__":
    run_sample()
