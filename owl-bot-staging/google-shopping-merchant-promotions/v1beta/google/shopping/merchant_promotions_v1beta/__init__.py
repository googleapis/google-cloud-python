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
from google.shopping.merchant_promotions_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.promotions_service import PromotionsServiceClient
from .services.promotions_service import PromotionsServiceAsyncClient

from .types.promotions import GetPromotionRequest
from .types.promotions import InsertPromotionRequest
from .types.promotions import ListPromotionsRequest
from .types.promotions import ListPromotionsResponse
from .types.promotions import Promotion
from .types.promotions_common import Attributes
from .types.promotions_common import PromotionStatus
from .types.promotions_common import CouponValueType
from .types.promotions_common import OfferType
from .types.promotions_common import ProductApplicability
from .types.promotions_common import RedemptionChannel
from .types.promotions_common import StoreApplicability

__all__ = (
    'PromotionsServiceAsyncClient',
'Attributes',
'CouponValueType',
'GetPromotionRequest',
'InsertPromotionRequest',
'ListPromotionsRequest',
'ListPromotionsResponse',
'OfferType',
'ProductApplicability',
'Promotion',
'PromotionStatus',
'PromotionsServiceClient',
'RedemptionChannel',
'StoreApplicability',
)
