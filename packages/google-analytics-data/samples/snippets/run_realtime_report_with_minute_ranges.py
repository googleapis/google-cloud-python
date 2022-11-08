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
a realtime report using minute ranges.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runRealtimeReport#body.request_body.FIELDS.minute_ranges
for more information.
"""
# [START analyticsdata_run_realtime_report_with_minute_ranges]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import MinuteRange
from google.analytics.data_v1beta.types import RunRealtimeReportRequest

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_realtime_report_with_minute_ranges(property_id)


def run_realtime_report_with_minute_ranges(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a realtime report on a Google Analytics 4 property. Dimensions
    field is omitted in the query, which results in total values of active users
    returned for each minute range in the report.

    Note the `dateRange` dimension added to the report response automatically
    as a result of querying multiple minute ranges.
    """
    client = BetaAnalyticsDataClient()

    request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="activeUsers")],
        minute_ranges=[
            MinuteRange(name="0-4 minutes ago", start_minutes_ago=4),
            MinuteRange(
                name="25-29 minutes ago", start_minutes_ago=29, end_minutes_ago=25
            ),
        ],
    )
    response = client.run_realtime_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_realtime_report_with_minute_ranges]


if __name__ == "__main__":
    run_sample()
