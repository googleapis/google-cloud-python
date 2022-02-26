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
# Snippet for CreateNote
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install grafeas-grafeas


# [START containeranalysis_v1_generated_Grafeas_CreateNote_async]
from grafeas import grafeas_v1


async def sample_create_note():
    # Create a client
    client = grafeas_v1.GrafeasAsyncClient()

    # Initialize request argument(s)
    request = grafeas_v1.CreateNoteRequest(
        parent="parent_value",
        note_id="note_id_value",
    )

    # Make the request
    response = await client.create_note(request=request)

    # Handle the response
    print(response)

# [END containeranalysis_v1_generated_Grafeas_CreateNote_async]
