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
# Snippet for MaterializeChannel
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-visionai


# [START visionai_v1alpha1_generated_StreamsService_MaterializeChannel_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import visionai_v1alpha1


async def sample_materialize_channel():
    # Create a client
    client = visionai_v1alpha1.StreamsServiceAsyncClient()

    # Initialize request argument(s)
    channel = visionai_v1alpha1.Channel()
    channel.stream = "stream_value"
    channel.event = "event_value"

    request = visionai_v1alpha1.MaterializeChannelRequest(
        parent="parent_value",
        channel_id="channel_id_value",
        channel=channel,
    )

    # Make the request
    operation = client.materialize_channel(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END visionai_v1alpha1_generated_StreamsService_MaterializeChannel_async]
