#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Data API sample application retrieving dimension and metrics
metadata.

See https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getMetadata
for more information.
"""
# [START analyticsdata_get_metadata_by_property_id]
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import GetMetadataRequest

from get_common_metadata import print_get_metadata_response


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    get_metadata_by_property_id(property_id)


def get_metadata_by_property_id(property_id="YOUR-GA4-PROPERTY-ID"):
    """Retrieves dimensions and metrics available for a Google Analytics 4
    property, including custom fields."""
    client = BetaAnalyticsDataClient()

    request = GetMetadataRequest(name=f"properties/{property_id}/metadata")
    response = client.get_metadata(request)

    print(
        f"Dimensions and metrics available for Google Analytics 4 "
        f"property {property_id} (including custom fields):"
    )
    print_get_metadata_response(response)


# [END analyticsdata_get_metadata_by_property_id]

if __name__ == "__main__":
    run_sample()
