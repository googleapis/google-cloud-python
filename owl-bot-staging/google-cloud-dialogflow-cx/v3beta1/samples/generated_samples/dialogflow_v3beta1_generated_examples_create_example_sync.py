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
# Snippet for CreateExample
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dialogflow-cx


# [START dialogflow_v3beta1_generated_Examples_CreateExample_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dialogflowcx_v3beta1


def sample_create_example():
    # Create a client
    client = dialogflowcx_v3beta1.ExamplesClient()

    # Initialize request argument(s)
    example = dialogflowcx_v3beta1.Example()
    example.actions.user_utterance.text = "text_value"
    example.display_name = "display_name_value"
    example.conversation_state = "OUTPUT_STATE_PENDING"

    request = dialogflowcx_v3beta1.CreateExampleRequest(
        parent="parent_value",
        example=example,
    )

    # Make the request
    response = client.create_example(request=request)

    # Handle the response
    print(response)

# [END dialogflow_v3beta1_generated_Examples_CreateExample_sync]
