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
from .productinputs import (
    DeleteProductInputRequest,
    InsertProductInputRequest,
    ProductInput,
    UpdateProductInputRequest,
)
from .products import (
    GetProductRequest,
    ListProductsRequest,
    ListProductsResponse,
    Product,
)
from .products_common import (
    AgeGroup,
    AutomatedDiscounts,
    Availability,
    CertificationAuthority,
    CertificationName,
    CloudExportAdditionalProperties,
    Condition,
    CreditType,
    DigitalSourceType,
    EnergyEfficiencyClass,
    FreeShippingThreshold,
    Gender,
    LoyaltyPoints,
    LoyaltyProgram,
    Pause,
    PickupMethod,
    PickupSla,
    ProductAttributes,
    ProductCertification,
    ProductDetail,
    ProductDimension,
    ProductInstallment,
    ProductStatus,
    ProductSustainabilityIncentive,
    ProductWeight,
    Shipping,
    ShippingDimension,
    ShippingWeight,
    SizeSystem,
    SizeType,
    StructuredDescription,
    StructuredTitle,
    SubscriptionCost,
    SubscriptionPeriod,
    UnitPricingBaseMeasure,
    UnitPricingMeasure,
)

__all__ = (
    "DeleteProductInputRequest",
    "InsertProductInputRequest",
    "ProductInput",
    "UpdateProductInputRequest",
    "GetProductRequest",
    "ListProductsRequest",
    "ListProductsResponse",
    "Product",
    "AutomatedDiscounts",
    "CloudExportAdditionalProperties",
    "FreeShippingThreshold",
    "LoyaltyPoints",
    "LoyaltyProgram",
    "ProductAttributes",
    "ProductCertification",
    "ProductDetail",
    "ProductDimension",
    "ProductInstallment",
    "ProductStatus",
    "ProductSustainabilityIncentive",
    "ProductWeight",
    "Shipping",
    "ShippingDimension",
    "ShippingWeight",
    "StructuredDescription",
    "StructuredTitle",
    "SubscriptionCost",
    "UnitPricingBaseMeasure",
    "UnitPricingMeasure",
    "AgeGroup",
    "Availability",
    "CertificationAuthority",
    "CertificationName",
    "Condition",
    "CreditType",
    "DigitalSourceType",
    "EnergyEfficiencyClass",
    "Gender",
    "Pause",
    "PickupMethod",
    "PickupSla",
    "SizeSystem",
    "SizeType",
    "SubscriptionPeriod",
)
