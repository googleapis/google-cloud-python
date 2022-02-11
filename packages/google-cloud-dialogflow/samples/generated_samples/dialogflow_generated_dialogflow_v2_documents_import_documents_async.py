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
# Snippet for ImportDocuments
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dialogflow


# [START dialogflow_generated_dialogflow_v2_Documents_ImportDocuments_async]
from google.cloud import dialogflow_v2


async def sample_import_documents():
    # Create a client
    client = dialogflow_v2.DocumentsAsyncClient()

    # Initialize request argument(s)
    gcs_source = dialogflow_v2.GcsSources()
    gcs_source.uris = ['uris_value_1', 'uris_value_2']

    document_template = dialogflow_v2.ImportDocumentTemplate()
    document_template.mime_type = "mime_type_value"
    document_template.knowledge_types = "ARTICLE_SUGGESTION"

    request = dialogflow_v2.ImportDocumentsRequest(
        gcs_source=gcs_source,
        parent="parent_value",
        document_template=document_template,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END dialogflow_generated_dialogflow_v2_Documents_ImportDocuments_async]
