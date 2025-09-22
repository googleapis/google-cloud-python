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
# Snippet for QueryCapacityPlanInsights
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-capacityplanner


# [START capacityplanner_v1beta_generated_CapacityPlanningService_QueryCapacityPlanInsights_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import capacityplanner_v1beta


def sample_query_capacity_plan_insights():
    # Create a client
    client = capacityplanner_v1beta.CapacityPlanningServiceClient()

    # Initialize request argument(s)
    capacity_plan_filters = capacityplanner_v1beta.CapacityPlanFilters()
    capacity_plan_filters.keys.resource_container.id = "id_value"
    capacity_plan_filters.keys.resource_id_key.resource_code = "resource_code_value"
    capacity_plan_filters.keys.location_id.source = "source_value"
    capacity_plan_filters.capacity_types = ['CAPACITY_TYPE_INORGANIC_APPROVED']

    request = capacityplanner_v1beta.QueryCapacityPlanInsightsRequest(
        parent="parent_value",
        capacity_plan_filters=capacity_plan_filters,
    )

    # Make the request
    response = client.query_capacity_plan_insights(request=request)

    # Handle the response
    print(response)

# [END capacityplanner_v1beta_generated_CapacityPlanningService_QueryCapacityPlanInsights_sync]
