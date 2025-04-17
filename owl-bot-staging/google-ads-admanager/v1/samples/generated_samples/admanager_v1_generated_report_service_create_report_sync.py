# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generated code. DO NOT EDIT!
#
# Snippet for CreateReport
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-ads-admanager


# [START admanager_v1_generated_ReportService_CreateReport_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.ads import admanager_v1


def sample_create_report():
    # Create a client
    client = admanager_v1.ReportServiceClient()

    # Initialize request argument(s)
    report = admanager_v1.Report()
    report.report_definition.dimensions = ['CUSTOM_DIMENSION_9_VALUE']
    report.report_definition.metrics = ['YIELD_GROUP_MEDIATION_THIRD_PARTY_ECPM']
    report.report_definition.report_type = "HISTORICAL"

    request = admanager_v1.CreateReportRequest(
        parent="parent_value",
        report=report,
    )

    # Make the request
    response = client.create_report(request=request)

    # Handle the response
    print(response)

# [END admanager_v1_generated_ReportService_CreateReport_sync]
