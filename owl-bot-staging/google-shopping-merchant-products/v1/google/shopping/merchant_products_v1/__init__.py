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
from google.shopping.merchant_products_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.product_inputs_service import ProductInputsServiceClient
from .services.product_inputs_service import ProductInputsServiceAsyncClient
from .services.products_service import ProductsServiceClient
from .services.products_service import ProductsServiceAsyncClient

from .types.productinputs import DeleteProductInputRequest
from .types.productinputs import InsertProductInputRequest
from .types.productinputs import ProductInput
from .types.productinputs import UpdateProductInputRequest
from .types.products import GetProductRequest
from .types.products import ListProductsRequest
from .types.products import ListProductsResponse
from .types.products import Product
from .types.products_common import AutomatedDiscounts
from .types.products_common import CloudExportAdditionalProperties
from .types.products_common import FreeShippingThreshold
from .types.products_common import LoyaltyPoints
from .types.products_common import LoyaltyProgram
from .types.products_common import ProductAttributes
from .types.products_common import ProductCertification
from .types.products_common import ProductDetail
from .types.products_common import ProductDimension
from .types.products_common import ProductInstallment
from .types.products_common import ProductStatus
from .types.products_common import ProductSustainabilityIncentive
from .types.products_common import ProductWeight
from .types.products_common import Shipping
from .types.products_common import ShippingDimension
from .types.products_common import ShippingWeight
from .types.products_common import StructuredDescription
from .types.products_common import StructuredTitle
from .types.products_common import SubscriptionCost
from .types.products_common import UnitPricingBaseMeasure
from .types.products_common import UnitPricingMeasure
from .types.products_common import AgeGroup
from .types.products_common import Availability
from .types.products_common import CertificationAuthority
from .types.products_common import CertificationName
from .types.products_common import Condition
from .types.products_common import CreditType
from .types.products_common import DigitalSourceType
from .types.products_common import EnergyEfficiencyClass
from .types.products_common import Gender
from .types.products_common import Pause
from .types.products_common import PickupMethod
from .types.products_common import PickupSla
from .types.products_common import SizeSystem
from .types.products_common import SizeType
from .types.products_common import SubscriptionPeriod

__all__ = (
    'ProductInputsServiceAsyncClient',
    'ProductsServiceAsyncClient',
'AgeGroup',
'AutomatedDiscounts',
'Availability',
'CertificationAuthority',
'CertificationName',
'CloudExportAdditionalProperties',
'Condition',
'CreditType',
'DeleteProductInputRequest',
'DigitalSourceType',
'EnergyEfficiencyClass',
'FreeShippingThreshold',
'Gender',
'GetProductRequest',
'InsertProductInputRequest',
'ListProductsRequest',
'ListProductsResponse',
'LoyaltyPoints',
'LoyaltyProgram',
'Pause',
'PickupMethod',
'PickupSla',
'Product',
'ProductAttributes',
'ProductCertification',
'ProductDetail',
'ProductDimension',
'ProductInput',
'ProductInputsServiceClient',
'ProductInstallment',
'ProductStatus',
'ProductSustainabilityIncentive',
'ProductWeight',
'ProductsServiceClient',
'Shipping',
'ShippingDimension',
'ShippingWeight',
'SizeSystem',
'SizeType',
'StructuredDescription',
'StructuredTitle',
'SubscriptionCost',
'SubscriptionPeriod',
'UnitPricingBaseMeasure',
'UnitPricingMeasure',
'UpdateProductInputRequest',
)
