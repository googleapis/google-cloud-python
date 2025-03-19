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
from google.shopping.merchant_reviews_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.merchant_reviews_service import MerchantReviewsServiceClient
from .services.merchant_reviews_service import MerchantReviewsServiceAsyncClient
from .services.product_reviews_service import ProductReviewsServiceClient
from .services.product_reviews_service import ProductReviewsServiceAsyncClient

from .types.merchantreviews import DeleteMerchantReviewRequest
from .types.merchantreviews import GetMerchantReviewRequest
from .types.merchantreviews import InsertMerchantReviewRequest
from .types.merchantreviews import ListMerchantReviewsRequest
from .types.merchantreviews import ListMerchantReviewsResponse
from .types.merchantreviews import MerchantReview
from .types.merchantreviews_common import MerchantReviewAttributes
from .types.merchantreviews_common import MerchantReviewStatus
from .types.productreviews import DeleteProductReviewRequest
from .types.productreviews import GetProductReviewRequest
from .types.productreviews import InsertProductReviewRequest
from .types.productreviews import ListProductReviewsRequest
from .types.productreviews import ListProductReviewsResponse
from .types.productreviews import ProductReview
from .types.productreviews_common import ProductReviewAttributes
from .types.productreviews_common import ProductReviewStatus

__all__ = (
    'MerchantReviewsServiceAsyncClient',
    'ProductReviewsServiceAsyncClient',
'DeleteMerchantReviewRequest',
'DeleteProductReviewRequest',
'GetMerchantReviewRequest',
'GetProductReviewRequest',
'InsertMerchantReviewRequest',
'InsertProductReviewRequest',
'ListMerchantReviewsRequest',
'ListMerchantReviewsResponse',
'ListProductReviewsRequest',
'ListProductReviewsResponse',
'MerchantReview',
'MerchantReviewAttributes',
'MerchantReviewStatus',
'MerchantReviewsServiceClient',
'ProductReview',
'ProductReviewAttributes',
'ProductReviewStatus',
'ProductReviewsServiceClient',
)
