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
# Snippet for AdaptiveMtTranslate
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-translate


# [START translate_v3_generated_TranslationService_AdaptiveMtTranslate_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import translate_v3


def sample_adaptive_mt_translate():
    # Create a client
    client = translate_v3.TranslationServiceClient()

    # Initialize request argument(s)
    request = translate_v3.AdaptiveMtTranslateRequest(
        parent="parent_value",
        dataset="dataset_value",
        content=['content_value1', 'content_value2'],
    )

    # Make the request
    response = client.adaptive_mt_translate(request=request)

    # Handle the response
    print(response)

# [END translate_v3_generated_TranslationService_AdaptiveMtTranslate_sync]
