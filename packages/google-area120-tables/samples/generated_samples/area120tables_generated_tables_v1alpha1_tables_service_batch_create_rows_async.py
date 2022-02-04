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
# Snippet for BatchCreateRows
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-area120-tables


# [START area120tables_generated_tables_v1alpha1_TablesService_BatchCreateRows_async]
from google.area120 import tables_v1alpha1


async def sample_batch_create_rows():
    # Create a client
    client = tables_v1alpha1.TablesServiceAsyncClient()

    # Initialize request argument(s)
    requests = tables_v1alpha1.CreateRowRequest()
    requests.parent = "parent_value"

    request = tables_v1alpha1.BatchCreateRowsRequest(
        parent="parent_value",
        requests=requests,
    )

    # Make the request
    response = await client.batch_create_rows(request=request)

    # Handle response
    print(response)

# [END area120tables_generated_tables_v1alpha1_TablesService_BatchCreateRows_async]
