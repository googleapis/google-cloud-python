# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
# Snippet for UpdateAttributionSettings
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-analytics-admin


# [START analyticsadmin_v1alpha_generated_AnalyticsAdminService_UpdateAttributionSettings_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.analytics import admin_v1alpha


def sample_update_attribution_settings():
    # Create a client
    client = admin_v1alpha.AnalyticsAdminServiceClient()

    # Initialize request argument(s)
    attribution_settings = admin_v1alpha.AttributionSettings()
    attribution_settings.acquisition_conversion_event_lookback_window = "ACQUISITION_CONVERSION_EVENT_LOOKBACK_WINDOW_30_DAYS"
    attribution_settings.other_conversion_event_lookback_window = "OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_90_DAYS"
    attribution_settings.reporting_attribution_model = "ADS_PREFERRED_LAST_CLICK"

    request = admin_v1alpha.UpdateAttributionSettingsRequest(
        attribution_settings=attribution_settings,
    )

    # Make the request
    response = client.update_attribution_settings(request=request)

    # Handle the response
    print(response)

# [END analyticsadmin_v1alpha_generated_AnalyticsAdminService_UpdateAttributionSettings_sync]
