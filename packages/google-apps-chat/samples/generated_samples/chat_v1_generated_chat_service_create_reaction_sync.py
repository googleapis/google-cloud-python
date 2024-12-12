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
# Snippet for CreateReaction
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-apps-chat


# [START chat_v1_generated_ChatService_CreateReaction_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.apps import chat_v1


def sample_create_reaction():
    # Create a client
    client = chat_v1.ChatServiceClient()

    # Initialize request argument(s)
    reaction = chat_v1.Reaction()
    reaction.emoji.unicode = "unicode_value"

    request = chat_v1.CreateReactionRequest(
        parent="parent_value",
        reaction=reaction,
    )

    # Make the request
    response = client.create_reaction(request=request)

    # Handle the response
    print(response)

# [END chat_v1_generated_ChatService_CreateReaction_sync]
