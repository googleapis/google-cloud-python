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
# Snippet for SearchNearby
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-maps-places


# [START places_v1_generated_Places_SearchNearby_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.maps import places_v1


async def sample_search_nearby():
    # Create a client
    client = places_v1.PlacesAsyncClient()

    # Initialize request argument(s)
    location_restriction = places_v1.LocationRestriction()
    location_restriction.circle.radius = 0.648

    request = places_v1.SearchNearbyRequest(
        location_restriction=location_restriction,
    )

    # Make the request
    response = await client.search_nearby(request=request)

    # Handle the response
    print(response)

# [END places_v1_generated_Places_SearchNearby_async]
