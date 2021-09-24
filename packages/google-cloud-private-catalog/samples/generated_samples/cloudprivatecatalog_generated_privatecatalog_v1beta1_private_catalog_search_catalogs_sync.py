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
# Snippet for SearchCatalogs
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-private-catalog


# [START cloudprivatecatalog_generated_privatecatalog_v1beta1_PrivateCatalog_SearchCatalogs_sync]
from google.cloud import privatecatalog_v1beta1


def sample_search_catalogs():
    """Snippet for search_catalogs"""

    # Create a client
    client = privatecatalog_v1beta1.PrivateCatalogClient()

    # Initialize request argument(s)
    request = privatecatalog_v1beta1.SearchCatalogsRequest(
        resource="resource_value",
    )

    # Make the request
    page_result = client.search_catalogs(request=request)
    for response in page_result:
        print(response)

# [END cloudprivatecatalog_generated_privatecatalog_v1beta1_PrivateCatalog_SearchCatalogs_sync]
