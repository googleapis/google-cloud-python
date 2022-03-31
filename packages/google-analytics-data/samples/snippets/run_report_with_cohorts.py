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
cohort specification in a report.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport#body.request_body.FIELDS.cohort_spec
for more information.
"""
# [START analyticsdata_run_report_with_cohorts]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Cohort
from google.analytics.data_v1beta.types import CohortSpec
from google.analytics.data_v1beta.types import CohortsRange
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
    run_report_with_cohorts(property_id)


def run_report_with_cohorts(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a report on a cohort of users whose first session happened on the
    same week. The number of active users and user retention rate is calculated
    for the cohort using WEEKLY granularity."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="cohort"), Dimension(name="cohortNthWeek")],
        metrics=[
            Metric(name="cohortActiveUsers"),
            Metric(
                name="cohortRetentionRate",
                expression="cohortActiveUsers/cohortTotalUsers",
            ),
        ],
        cohort_spec=CohortSpec(
            cohorts=[
                Cohort(
                    dimension="firstSessionDate",
                    name="cohort",
                    date_range=DateRange(
                        start_date="2021-01-03", end_date="2021-01-09"
                    ),
                )
            ],
            cohorts_range=CohortsRange(
                start_offset=0,
                end_offset=4,
                granularity=CohortsRange.Granularity.WEEKLY,
            ),
        ),
    )
    response = client.run_report(request)
    print_run_report_response(response)


# [END analyticsdata_run_report_with_cohorts]


if __name__ == "__main__":
    run_sample()
