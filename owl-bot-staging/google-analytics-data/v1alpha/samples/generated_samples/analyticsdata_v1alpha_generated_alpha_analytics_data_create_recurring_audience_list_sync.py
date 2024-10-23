# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
# Snippet for CreateRecurringAudienceList
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-analytics-data


# [START analyticsdata_v1alpha_generated_AlphaAnalyticsData_CreateRecurringAudienceList_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.analytics import data_v1alpha


def sample_create_recurring_audience_list():
    # Create a client
    client = data_v1alpha.AlphaAnalyticsDataClient()

    # Initialize request argument(s)
    recurring_audience_list = data_v1alpha.RecurringAudienceList()
    recurring_audience_list.audience = "audience_value"

    request = data_v1alpha.CreateRecurringAudienceListRequest(
        parent="parent_value",
        recurring_audience_list=recurring_audience_list,
    )

    # Make the request
    response = client.create_recurring_audience_list(request=request)

    # Handle the response
    print(response)

# [END analyticsdata_v1alpha_generated_AlphaAnalyticsData_CreateRecurringAudienceList_sync]
