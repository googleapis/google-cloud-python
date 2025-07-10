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
# Snippet for CreateReferenceList
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-chronicle


# [START chronicle_v1_generated_ReferenceListService_CreateReferenceList_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import chronicle_v1


def sample_create_reference_list():
    # Create a client
    client = chronicle_v1.ReferenceListServiceClient()

    # Initialize request argument(s)
    reference_list = chronicle_v1.ReferenceList()
    reference_list.description = "description_value"
    reference_list.entries.value = "value_value"
    reference_list.syntax_type = "REFERENCE_LIST_SYNTAX_TYPE_CIDR"

    request = chronicle_v1.CreateReferenceListRequest(
        parent="parent_value",
        reference_list=reference_list,
        reference_list_id="reference_list_id_value",
    )

    # Make the request
    response = client.create_reference_list(request=request)

    # Handle the response
    print(response)

# [END chronicle_v1_generated_ReferenceListService_CreateReferenceList_sync]
