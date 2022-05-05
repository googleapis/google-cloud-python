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

"""Google Analytics Data API sample application retrieving dimension and metrics
metadata.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getMetadata
for more information.
"""
# [START analyticsdata_get_common_metadata]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import GetMetadataRequest
from google.analytics.data_v1beta.types import MetricType


def run_sample():
    """Runs the sample."""
    get_common_metadata()


def get_common_metadata():
    """Retrieves dimensions and metrics available for all Google Analytics 4
    properties."""
    client = BetaAnalyticsDataClient()

    # Set the Property ID to 0 for dimensions and metrics common
    # to all properties. In this special mode, this method will
    # not return custom dimensions and metrics.
    property_id = 0
    request = GetMetadataRequest(name=f"properties/{property_id}/metadata")
    response = client.get_metadata(request)

    print("Dimensions and metrics available for all Google Analytics 4 properties:")
    print_get_metadata_response(response)


def print_get_metadata_response(response):
    """Prints results of the getMetadata call."""
    # [START analyticsdata_print_get_metadata_response]
    for dimension in response.dimensions:
        print("DIMENSION")
        print(f"{dimension.api_name} ({dimension.ui_name}): {dimension.description}")
        print(f"custom_definition: {dimension.custom_definition}")
        if dimension.deprecated_api_names:
            print(f"Deprecated API names: {dimension.deprecated_api_names}")
        print("")

    for metric in response.metrics:
        print("METRIC")
        print(f"{metric.api_name} ({metric.ui_name}): {metric.description}")
        print(f"custom_definition: {metric.custom_definition}")
        if metric.expression:
            print(f"Expression: {metric.expression}")

        metric_type = MetricType(metric.type_).name
        print(f"Type: {metric_type}")

        if metric.deprecated_api_names:
            print(f"Deprecated API names: {metric.deprecated_api_names}")
        print("")
    # [END analyticsdata_print_get_metadata_response]


# [END analyticsdata_get_common_metadata]


if __name__ == "__main__":
    run_sample()
