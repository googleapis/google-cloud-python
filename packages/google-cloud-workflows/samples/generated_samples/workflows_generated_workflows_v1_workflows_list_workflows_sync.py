# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
# Snippet for ListWorkflows
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-workflows


# [START workflows_generated_workflows_v1_Workflows_ListWorkflows_sync]
from google.cloud import workflows_v1


def sample_list_workflows():
    # Create a client
    client = workflows_v1.WorkflowsClient()

    # Initialize request argument(s)
    request = workflows_v1.ListWorkflowsRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.list_workflows(request=request)

    # Handle the response
    for response in page_result:
        print(response)

# [END workflows_generated_workflows_v1_Workflows_ListWorkflows_sync]
