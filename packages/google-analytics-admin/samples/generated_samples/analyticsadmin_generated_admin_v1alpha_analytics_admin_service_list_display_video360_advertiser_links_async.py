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
# Snippet for ListDisplayVideo360AdvertiserLinks
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-analytics-admin


# [START analyticsadmin_generated_admin_v1alpha_AnalyticsAdminService_ListDisplayVideo360AdvertiserLinks_async]
from google.analytics import admin_v1alpha


async def sample_list_display_video360_advertiser_links():
    # Create a client
    client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

    # Initialize request argument(s)
    request = admin_v1alpha.ListDisplayVideo360AdvertiserLinksRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.list_display_video360_advertiser_links(request=request)
    async for response in page_result:
        print(response)

# [END analyticsadmin_generated_admin_v1alpha_AnalyticsAdminService_ListDisplayVideo360AdvertiserLinks_async]
