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
# Snippet for CreateChannel
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-eventarc


# [START eventarc_generated_eventarc_v1_Eventarc_CreateChannel_async]
from google.cloud import eventarc_v1


async def sample_create_channel():
    # Create a client
    client = eventarc_v1.EventarcAsyncClient()

    # Initialize request argument(s)
    channel = eventarc_v1.Channel()
    channel.pubsub_topic = "pubsub_topic_value"
    channel.name = "name_value"
    channel.provider = "provider_value"

    request = eventarc_v1.CreateChannelRequest(
        parent="parent_value",
        channel=channel,
        channel_id="channel_id_value",
        validate_only=True,
    )

    # Make the request
    operation = client.create_channel(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END eventarc_generated_eventarc_v1_Eventarc_CreateChannel_async]
