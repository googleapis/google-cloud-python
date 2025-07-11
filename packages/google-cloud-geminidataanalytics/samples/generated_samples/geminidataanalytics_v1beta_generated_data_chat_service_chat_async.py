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
# Snippet for Chat
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-geminidataanalytics


# [START geminidataanalytics_v1beta_generated_DataChatService_Chat_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import geminidataanalytics_v1beta


async def sample_chat():
    # Create a client
    client = geminidataanalytics_v1beta.DataChatServiceAsyncClient()

    # Initialize request argument(s)
    inline_context = geminidataanalytics_v1beta.Context()
    inline_context.datasource_references.bq.table_references.project_id = "project_id_value"
    inline_context.datasource_references.bq.table_references.dataset_id = "dataset_id_value"
    inline_context.datasource_references.bq.table_references.table_id = "table_id_value"

    messages = geminidataanalytics_v1beta.Message()
    messages.user_message.text = "text_value"

    request = geminidataanalytics_v1beta.ChatRequest(
        inline_context=inline_context,
        parent="parent_value",
        messages=messages,
    )

    # Make the request
    stream = await client.chat(request=request)

    # Handle the response
    async for response in stream:
        print(response)

# [END geminidataanalytics_v1beta_generated_DataChatService_Chat_async]
