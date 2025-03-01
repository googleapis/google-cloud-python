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
# Snippet for IngestConversations
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-contact-center-insights


# [START contactcenterinsights_v1_generated_ContactCenterInsights_IngestConversations_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import contact_center_insights_v1


async def sample_ingest_conversations():
    # Create a client
    client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

    # Initialize request argument(s)
    gcs_source = contact_center_insights_v1.GcsSource()
    gcs_source.bucket_uri = "bucket_uri_value"

    transcript_object_config = contact_center_insights_v1.TranscriptObjectConfig()
    transcript_object_config.medium = "CHAT"

    request = contact_center_insights_v1.IngestConversationsRequest(
        gcs_source=gcs_source,
        transcript_object_config=transcript_object_config,
        parent="parent_value",
    )

    # Make the request
    operation = client.ingest_conversations(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END contactcenterinsights_v1_generated_ContactCenterInsights_IngestConversations_async]
