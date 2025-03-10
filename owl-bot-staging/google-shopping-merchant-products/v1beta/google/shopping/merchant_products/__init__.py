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
from google.shopping.merchant_products import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_products_v1beta.services.product_inputs_service.client import ProductInputsServiceClient
from google.shopping.merchant_products_v1beta.services.product_inputs_service.async_client import ProductInputsServiceAsyncClient
from google.shopping.merchant_products_v1beta.services.products_service.client import ProductsServiceClient
from google.shopping.merchant_products_v1beta.services.products_service.async_client import ProductsServiceAsyncClient

from google.shopping.merchant_products_v1beta.types.productinputs import DeleteProductInputRequest
from google.shopping.merchant_products_v1beta.types.productinputs import InsertProductInputRequest
from google.shopping.merchant_products_v1beta.types.productinputs import ProductInput
from google.shopping.merchant_products_v1beta.types.products import GetProductRequest
from google.shopping.merchant_products_v1beta.types.products import ListProductsRequest
from google.shopping.merchant_products_v1beta.types.products import ListProductsResponse
from google.shopping.merchant_products_v1beta.types.products import Product
from google.shopping.merchant_products_v1beta.types.products_common import Attributes
from google.shopping.merchant_products_v1beta.types.products_common import Certification
from google.shopping.merchant_products_v1beta.types.products_common import CloudExportAdditionalProperties
from google.shopping.merchant_products_v1beta.types.products_common import FreeShippingThreshold
from google.shopping.merchant_products_v1beta.types.products_common import Installment
from google.shopping.merchant_products_v1beta.types.products_common import LoyaltyPoints
from google.shopping.merchant_products_v1beta.types.products_common import LoyaltyProgram
from google.shopping.merchant_products_v1beta.types.products_common import ProductDetail
from google.shopping.merchant_products_v1beta.types.products_common import ProductDimension
from google.shopping.merchant_products_v1beta.types.products_common import ProductStatus
from google.shopping.merchant_products_v1beta.types.products_common import ProductStructuredDescription
from google.shopping.merchant_products_v1beta.types.products_common import ProductStructuredTitle
from google.shopping.merchant_products_v1beta.types.products_common import ProductWeight
from google.shopping.merchant_products_v1beta.types.products_common import Shipping
from google.shopping.merchant_products_v1beta.types.products_common import ShippingDimension
from google.shopping.merchant_products_v1beta.types.products_common import ShippingWeight
from google.shopping.merchant_products_v1beta.types.products_common import SubscriptionCost
from google.shopping.merchant_products_v1beta.types.products_common import Tax
from google.shopping.merchant_products_v1beta.types.products_common import UnitPricingBaseMeasure
from google.shopping.merchant_products_v1beta.types.products_common import UnitPricingMeasure
from google.shopping.merchant_products_v1beta.types.products_common import SubscriptionPeriod

__all__ = ('ProductInputsServiceClient',
    'ProductInputsServiceAsyncClient',
    'ProductsServiceClient',
    'ProductsServiceAsyncClient',
    'DeleteProductInputRequest',
    'InsertProductInputRequest',
    'ProductInput',
    'GetProductRequest',
    'ListProductsRequest',
    'ListProductsResponse',
    'Product',
    'Attributes',
    'Certification',
    'CloudExportAdditionalProperties',
    'FreeShippingThreshold',
    'Installment',
    'LoyaltyPoints',
    'LoyaltyProgram',
    'ProductDetail',
    'ProductDimension',
    'ProductStatus',
    'ProductStructuredDescription',
    'ProductStructuredTitle',
    'ProductWeight',
    'Shipping',
    'ShippingDimension',
    'ShippingWeight',
    'SubscriptionCost',
    'Tax',
    'UnitPricingBaseMeasure',
    'UnitPricingMeasure',
    'SubscriptionPeriod',
)
