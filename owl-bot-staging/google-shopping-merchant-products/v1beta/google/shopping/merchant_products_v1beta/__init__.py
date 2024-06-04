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
from google.shopping.merchant_products_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.product_inputs_service import ProductInputsServiceClient
from .services.product_inputs_service import ProductInputsServiceAsyncClient
from .services.products_service import ProductsServiceClient
from .services.products_service import ProductsServiceAsyncClient

from .types.productinputs import DeleteProductInputRequest
from .types.productinputs import InsertProductInputRequest
from .types.productinputs import ProductInput
from .types.products import GetProductRequest
from .types.products import ListProductsRequest
from .types.products import ListProductsResponse
from .types.products import Product
from .types.products_common import Attributes
from .types.products_common import Certification
from .types.products_common import CloudExportAdditionalProperties
from .types.products_common import FreeShippingThreshold
from .types.products_common import Installment
from .types.products_common import LoyaltyPoints
from .types.products_common import LoyaltyProgram
from .types.products_common import ProductDetail
from .types.products_common import ProductDimension
from .types.products_common import ProductStatus
from .types.products_common import ProductStructuredDescription
from .types.products_common import ProductStructuredTitle
from .types.products_common import ProductWeight
from .types.products_common import Shipping
from .types.products_common import ShippingDimension
from .types.products_common import ShippingWeight
from .types.products_common import SubscriptionCost
from .types.products_common import Tax
from .types.products_common import UnitPricingBaseMeasure
from .types.products_common import UnitPricingMeasure
from .types.products_common import SubscriptionPeriod

__all__ = (
    'ProductInputsServiceAsyncClient',
    'ProductsServiceAsyncClient',
'Attributes',
'Certification',
'CloudExportAdditionalProperties',
'DeleteProductInputRequest',
'FreeShippingThreshold',
'GetProductRequest',
'InsertProductInputRequest',
'Installment',
'ListProductsRequest',
'ListProductsResponse',
'LoyaltyPoints',
'LoyaltyProgram',
'Product',
'ProductDetail',
'ProductDimension',
'ProductInput',
'ProductInputsServiceClient',
'ProductStatus',
'ProductStructuredDescription',
'ProductStructuredTitle',
'ProductWeight',
'ProductsServiceClient',
'Shipping',
'ShippingDimension',
'ShippingWeight',
'SubscriptionCost',
'SubscriptionPeriod',
'Tax',
'UnitPricingBaseMeasure',
'UnitPricingMeasure',
)
