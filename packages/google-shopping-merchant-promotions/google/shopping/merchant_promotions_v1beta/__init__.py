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


from .services.promotions_service import (
    PromotionsServiceAsyncClient,
    PromotionsServiceClient,
)
from .types.promotions import (
    GetPromotionRequest,
    InsertPromotionRequest,
    ListPromotionsRequest,
    ListPromotionsResponse,
    Promotion,
)
from .types.promotions_common import (
    Attributes,
    CouponValueType,
    OfferType,
    ProductApplicability,
    PromotionStatus,
    RedemptionChannel,
    StoreApplicability,
)

__all__ = (
    "PromotionsServiceAsyncClient",
    "Attributes",
    "CouponValueType",
    "GetPromotionRequest",
    "InsertPromotionRequest",
    "ListPromotionsRequest",
    "ListPromotionsResponse",
    "OfferType",
    "ProductApplicability",
    "Promotion",
    "PromotionStatus",
    "PromotionsServiceClient",
    "RedemptionChannel",
    "StoreApplicability",
)
