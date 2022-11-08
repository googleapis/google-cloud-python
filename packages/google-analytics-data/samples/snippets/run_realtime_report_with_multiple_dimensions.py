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

"""Google Analytics Data API sample application demonstrating the creation of
a realtime report.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
for more information.
"""
# [START analyticsdata_run_realtime_report_with_multiple_dimensions]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    Dimension,
    Metric,
    RunRealtimeReportRequest,
)

from run_report import print_run_report_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_realtime_report_with_multiple_dimensions(property_id)


def run_realtime_report_with_multiple_dimensions(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a realtime report on a Google Analytics 4 property."""
    client = BetaAnalyticsDataClient()

    request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country"), Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
    )
    response = client.run_realtime_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_realtime_report_with_multiple_dimensions]


if __name__ == "__main__":
    run_sample()
