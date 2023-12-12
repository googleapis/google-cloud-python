# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.shopping.css_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.account_labels_service import AccountLabelsServiceClient
from .services.account_labels_service import AccountLabelsServiceAsyncClient
from .services.accounts_service import AccountsServiceClient
from .services.accounts_service import AccountsServiceAsyncClient
from .services.css_product_inputs_service import CssProductInputsServiceClient
from .services.css_product_inputs_service import CssProductInputsServiceAsyncClient
from .services.css_products_service import CssProductsServiceClient
from .services.css_products_service import CssProductsServiceAsyncClient

from .types.accounts import Account
from .types.accounts import GetAccountRequest
from .types.accounts import ListChildAccountsRequest
from .types.accounts import ListChildAccountsResponse
from .types.accounts import UpdateAccountLabelsRequest
from .types.accounts_labels import AccountLabel
from .types.accounts_labels import CreateAccountLabelRequest
from .types.accounts_labels import DeleteAccountLabelRequest
from .types.accounts_labels import ListAccountLabelsRequest
from .types.accounts_labels import ListAccountLabelsResponse
from .types.accounts_labels import UpdateAccountLabelRequest
from .types.css_product_common import Attributes
from .types.css_product_common import Certification
from .types.css_product_common import CssProductStatus
from .types.css_product_common import ProductDetail
from .types.css_product_common import ProductDimension
from .types.css_product_common import ProductWeight
from .types.css_product_inputs import CssProductInput
from .types.css_product_inputs import DeleteCssProductInputRequest
from .types.css_product_inputs import InsertCssProductInputRequest
from .types.css_products import CssProduct
from .types.css_products import GetCssProductRequest
from .types.css_products import ListCssProductsRequest
from .types.css_products import ListCssProductsResponse

__all__ = (
    'AccountLabelsServiceAsyncClient',
    'AccountsServiceAsyncClient',
    'CssProductInputsServiceAsyncClient',
    'CssProductsServiceAsyncClient',
'Account',
'AccountLabel',
'AccountLabelsServiceClient',
'AccountsServiceClient',
'Attributes',
'Certification',
'CreateAccountLabelRequest',
'CssProduct',
'CssProductInput',
'CssProductInputsServiceClient',
'CssProductStatus',
'CssProductsServiceClient',
'DeleteAccountLabelRequest',
'DeleteCssProductInputRequest',
'GetAccountRequest',
'GetCssProductRequest',
'InsertCssProductInputRequest',
'ListAccountLabelsRequest',
'ListAccountLabelsResponse',
'ListChildAccountsRequest',
'ListChildAccountsResponse',
'ListCssProductsRequest',
'ListCssProductsResponse',
'ProductDetail',
'ProductDimension',
'ProductWeight',
'UpdateAccountLabelRequest',
'UpdateAccountLabelsRequest',
)
