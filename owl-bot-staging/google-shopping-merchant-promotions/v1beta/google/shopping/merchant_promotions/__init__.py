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
from google.shopping.merchant_promotions import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_promotions_v1beta.services.promotions_service.client import PromotionsServiceClient
from google.shopping.merchant_promotions_v1beta.services.promotions_service.async_client import PromotionsServiceAsyncClient

from google.shopping.merchant_promotions_v1beta.types.promotions import GetPromotionRequest
from google.shopping.merchant_promotions_v1beta.types.promotions import InsertPromotionRequest
from google.shopping.merchant_promotions_v1beta.types.promotions import ListPromotionsRequest
from google.shopping.merchant_promotions_v1beta.types.promotions import ListPromotionsResponse
from google.shopping.merchant_promotions_v1beta.types.promotions import Promotion
from google.shopping.merchant_promotions_v1beta.types.promotions_common import Attributes
from google.shopping.merchant_promotions_v1beta.types.promotions_common import PromotionStatus
from google.shopping.merchant_promotions_v1beta.types.promotions_common import CouponValueType
from google.shopping.merchant_promotions_v1beta.types.promotions_common import OfferType
from google.shopping.merchant_promotions_v1beta.types.promotions_common import ProductApplicability
from google.shopping.merchant_promotions_v1beta.types.promotions_common import RedemptionChannel
from google.shopping.merchant_promotions_v1beta.types.promotions_common import StoreApplicability

__all__ = ('PromotionsServiceClient',
    'PromotionsServiceAsyncClient',
    'GetPromotionRequest',
    'InsertPromotionRequest',
    'ListPromotionsRequest',
    'ListPromotionsResponse',
    'Promotion',
    'Attributes',
    'PromotionStatus',
    'CouponValueType',
    'OfferType',
    'ProductApplicability',
    'RedemptionChannel',
    'StoreApplicability',
)
