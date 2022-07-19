#!/usr/bin/env python

# Copyright 2022 Google Inc. All Rights Reserved.
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

"""Google Analytics Data API sample application demonstrating the creation of
a funnel report.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1alpha/properties/runFunnelReport
for more information.
"""
# [START analyticsdata_run_funnel_report]
from google.analytics.data_v1alpha import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.types import DateRange
from google.analytics.data_v1alpha.types import Dimension
from google.analytics.data_v1alpha.types import Funnel
from google.analytics.data_v1alpha.types import FunnelBreakdown
from google.analytics.data_v1alpha.types import FunnelEventFilter
from google.analytics.data_v1alpha.types import FunnelFieldFilter
from google.analytics.data_v1alpha.types import FunnelFilterExpression
from google.analytics.data_v1alpha.types import FunnelFilterExpressionList
from google.analytics.data_v1alpha.types import FunnelStep
from google.analytics.data_v1alpha.types import RunFunnelReportRequest
from google.analytics.data_v1alpha.types import StringFilter


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_funnel_report(property_id)


def run_funnel_report(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a funnel query to build a report with 5 funnel steps.
      Step 1: First open/visit (event name is `first_open` or `first_visit`).
      Step 2: Organic visitors (`firstUserMedium` dimension contains the term
      "organic").
      Step 3: Session start (event name is `session_start`).
      Step 4: Screen/Page view (event name is `screen_view` or `page_view`).
      Step 5: Purchase (event name is `purchase` or `in_app_purchase`).

    The report configuration reproduces the default funnel report provided in
    the Funnel Exploration template of the Google Analytics UI.
    See more at https://support.google.com/analytics/answer/9327974
    """
    client = AlphaAnalyticsDataClient()

    request = RunFunnelReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        funnel_breakdown=FunnelBreakdown(
            breakdown_dimension=Dimension(name="deviceCategory")
        ),
        funnel=Funnel(
            steps=[
                FunnelStep(
                    name="First open/visit",
                    filter_expression=FunnelFilterExpression(
                        or_group=FunnelFilterExpressionList(
                            expressions=[
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="first_open"
                                    )
                                ),
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="first_visit"
                                    )
                                ),
                            ]
                        )
                    ),
                ),
                FunnelStep(
                    name="Organic visitors",
                    filter_expression=FunnelFilterExpression(
                        funnel_field_filter=FunnelFieldFilter(
                            field_name="firstUserMedium",
                            string_filter=StringFilter(
                                match_type=StringFilter.MatchType.CONTAINS,
                                case_sensitive=False,
                                value="organic",
                            ),
                        )
                    ),
                ),
                FunnelStep(
                    name="Session start",
                    filter_expression=FunnelFilterExpression(
                        funnel_event_filter=FunnelEventFilter(
                            event_name="session_start"
                        )
                    ),
                ),
                FunnelStep(
                    name="Screen/Page view",
                    filter_expression=FunnelFilterExpression(
                        or_group=FunnelFilterExpressionList(
                            expressions=[
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="screen_view"
                                    )
                                ),
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="page_view"
                                    )
                                ),
                            ]
                        )
                    ),
                ),
                FunnelStep(
                    name="Purchase",
                    filter_expression=FunnelFilterExpression(
                        or_group=FunnelFilterExpressionList(
                            expressions=[
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="purchase"
                                    )
                                ),
                                FunnelFilterExpression(
                                    funnel_event_filter=FunnelEventFilter(
                                        event_name="in_app_purchase"
                                    )
                                ),
                            ]
                        )
                    ),
                ),
            ]
        ),
    )
    response = client.run_funnel_report(request)
    print_run_funnel_report_response(response)


# [START analyticsdata_print_run_funnel_report_response]
def print_funnel_sub_report(funnel_sub_report):
    """Prints the contents of a FunnelSubReport object."""
    print("Dimension headers:")
    for dimension_header in funnel_sub_report.dimension_headers:
        print(dimension_header.name)

    print("\nMetric headers:")
    for metric_header in funnel_sub_report.metric_headers:
        print(metric_header.name)

    print("\nDimensions and metric values for each row in the report:")
    for row_idx, row in enumerate(funnel_sub_report.rows):
        print("\nRow #{}".format(row_idx))
        for field_idx, dimension_value in enumerate(row.dimension_values):
            dimension_name = funnel_sub_report.dimension_headers[field_idx].name
            print("{}: '{}'".format(dimension_name, dimension_value.value))

        for field_idx, metric_value in enumerate(row.metric_values):
            metric_name = funnel_sub_report.metric_headers[field_idx].name
            print("{}: '{}'".format(metric_name, metric_value.value))

    print("\nSampling metadata for each date range:")
    for metadata_idx, metadata in enumerate(
        funnel_sub_report.metadata.sampling_metadatas
    ):
        print(
            "Sampling metadata for date range #{}: samplesReadCount={}, "
            "samplingSpaceSize={}".format(
                metadata_idx, metadata.samples_read_count, metadata.sampling_space_size
            )
        )


def print_run_funnel_report_response(response):
    """Prints results of a runFunnelReport call."""
    print("Report result:")
    print("=== FUNNEL VISUALIZATION ===")
    print_funnel_sub_report(response.funnel_visualization)

    print("=== FUNNEL TABLE ===")
    print_funnel_sub_report(response.funnel_table)


# [END analyticsdata_print_run_funnel_report_response]


# [END analyticsdata_run_funnel_report]


if __name__ == "__main__":
    run_sample()
