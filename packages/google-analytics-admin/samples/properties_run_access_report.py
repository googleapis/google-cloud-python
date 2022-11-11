#!/usr/bin/env python

# Copyright 2022 Google LLC All Rights Reserved.
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

"""Google Analytics Admin API sample application which runs an access report
on a property.
See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/runAccessReport
for more information.
"""
# [START analyticsadmin_properties_run_access_report]
from datetime import datetime

from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import (
    AccessDateRange,
    AccessDimension,
    AccessMetric,
    RunAccessReportRequest,
)


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    run_access_report(property_id)


def run_access_report(property_id: str, transport: str = None):
    """
    Runs an access report for a Google Analytics property. The report will
    aggregate over dimensions `userEmail`, `accessedPropertyId`,
    `propertyUserLink`, `reportType`, `revenueDataReturned`, `costDataReturned`,
    `userIP`, and return the access count, as well as the most recent access
    time for each combination.
    See https://developers.google.com/analytics/devguides/config/admin/v1/access-api-schema
    for the description of each field used in a data access report query.
    Args:
        property_id(str): The Google Analytics Property ID.
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    request = RunAccessReportRequest(
        entity=f"properties/{property_id}",
        dimensions=[
            AccessDimension(dimension_name="userEmail"),
            AccessDimension(dimension_name="accessedPropertyId"),
            AccessDimension(dimension_name="propertyUserLink"),
            AccessDimension(dimension_name="reportType"),
            AccessDimension(dimension_name="revenueDataReturned"),
            AccessDimension(dimension_name="costDataReturned"),
            AccessDimension(dimension_name="userIP"),
            AccessDimension(dimension_name="mostRecentAccessEpochTimeMicros"),
        ],
        metrics=[AccessMetric(metric_name="accessCount")],
        date_ranges=[AccessDateRange(start_date="yesterday", end_date="today")],
    )

    access_report = client.run_access_report(request)

    print("Result:")
    print_access_report(access_report)


def print_access_report(response):
    """Prints the access report."""
    print(f"{response.row_count} rows received")
    for dimensionHeader in response.dimension_headers:
        print(f"Dimension header name: {dimensionHeader.dimension_name}")
    for metricHeader in response.metric_headers:
        print(f"Metric header name: {metricHeader.metric_name})")

    for rowIdx, row in enumerate(response.rows):
        print(f"\nRow {rowIdx}")
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].dimension_name
            if dimension_name.endswith("Micros"):
                # Convert microseconds since Unix Epoch to datetime object.
                dimension_value_formatted = datetime.utcfromtimestamp(
                    int(dimension_value.value) / 1000000
                )
            else:
                dimension_value_formatted = dimension_value.value
            print(f"{dimension_name}: {dimension_value_formatted}")

        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].metric_name
            print(f"{metric_name}: {metric_value.value}")


# [END analyticsadmin_properties_run_access_report]


if __name__ == "__main__":
    run_sample()
