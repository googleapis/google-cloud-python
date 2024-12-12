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
# Snippet for InsertProductReview
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-shopping-merchant-reviews


# [START merchantapi_v1beta_generated_ProductReviewsService_InsertProductReview_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.shopping import merchant_reviews_v1beta


async def sample_insert_product_review():
    # Create a client
    client = merchant_reviews_v1beta.ProductReviewsServiceAsyncClient()

    # Initialize request argument(s)
    product_review = merchant_reviews_v1beta.ProductReview()
    product_review.product_review_id = "product_review_id_value"

    request = merchant_reviews_v1beta.InsertProductReviewRequest(
        parent="parent_value",
        product_review=product_review,
        data_source="data_source_value",
    )

    # Make the request
    response = await client.insert_product_review(request=request)

    # Handle the response
    print(response)

# [END merchantapi_v1beta_generated_ProductReviewsService_InsertProductReview_async]
