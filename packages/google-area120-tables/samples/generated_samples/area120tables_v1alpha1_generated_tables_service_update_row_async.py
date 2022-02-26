# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
# Snippet for UpdateRow
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-area120-tables


# [START area120tables_v1alpha1_generated_TablesService_UpdateRow_async]
from google.area120 import tables_v1alpha1


async def sample_update_row():
    # Create a client
    client = tables_v1alpha1.TablesServiceAsyncClient()

    # Initialize request argument(s)
    request = tables_v1alpha1.UpdateRowRequest(
    )

    # Make the request
    response = await client.update_row(request=request)

    # Handle the response
    print(response)

# [END area120tables_v1alpha1_generated_TablesService_UpdateRow_async]
