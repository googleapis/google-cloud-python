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
# Snippet for ReviewDocument
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-documentai


# [START documentai_generated_documentai_v1_DocumentProcessorService_ReviewDocument_async]
from google.cloud import documentai_v1


async def sample_review_document():
    """Snippet for review_document"""

    # Create a client
    client = documentai_v1.DocumentProcessorServiceAsyncClient()

    # Initialize request argument(s)
    inline_document = documentai_v1.Document()
    inline_document.uri = "uri_value"

    project = "my-project-id"
    location = "us-central1"
    processor = "processor_value"
    human_review_config = f"projects/{project}/locations/{location}/processors/{processor}/humanReviewConfig"

    request = documentai_v1.ReviewDocumentRequest(
        inline_document=inline_document,
        human_review_config=human_review_config,
    )

    # Make the request
    operation = client.review_document(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()
    print(response)

# [END documentai_generated_documentai_v1_DocumentProcessorService_ReviewDocument_async]
