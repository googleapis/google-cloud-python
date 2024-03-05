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
from google.shopping.css_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.account_labels_service import (
    AccountLabelsServiceAsyncClient,
    AccountLabelsServiceClient,
)
from .services.accounts_service import AccountsServiceAsyncClient, AccountsServiceClient
from .services.css_product_inputs_service import (
    CssProductInputsServiceAsyncClient,
    CssProductInputsServiceClient,
)
from .services.css_products_service import (
    CssProductsServiceAsyncClient,
    CssProductsServiceClient,
)
from .types.accounts import (
    Account,
    GetAccountRequest,
    ListChildAccountsRequest,
    ListChildAccountsResponse,
    UpdateAccountLabelsRequest,
)
from .types.accounts_labels import (
    AccountLabel,
    CreateAccountLabelRequest,
    DeleteAccountLabelRequest,
    ListAccountLabelsRequest,
    ListAccountLabelsResponse,
    UpdateAccountLabelRequest,
)
from .types.css_product_common import (
    Attributes,
    Certification,
    CssProductStatus,
    ProductDetail,
    ProductDimension,
    ProductWeight,
)
from .types.css_product_inputs import (
    CssProductInput,
    DeleteCssProductInputRequest,
    InsertCssProductInputRequest,
)
from .types.css_products import (
    CssProduct,
    GetCssProductRequest,
    ListCssProductsRequest,
    ListCssProductsResponse,
)

__all__ = (
    "AccountLabelsServiceAsyncClient",
    "AccountsServiceAsyncClient",
    "CssProductInputsServiceAsyncClient",
    "CssProductsServiceAsyncClient",
    "Account",
    "AccountLabel",
    "AccountLabelsServiceClient",
    "AccountsServiceClient",
    "Attributes",
    "Certification",
    "CreateAccountLabelRequest",
    "CssProduct",
    "CssProductInput",
    "CssProductInputsServiceClient",
    "CssProductStatus",
    "CssProductsServiceClient",
    "DeleteAccountLabelRequest",
    "DeleteCssProductInputRequest",
    "GetAccountRequest",
    "GetCssProductRequest",
    "InsertCssProductInputRequest",
    "ListAccountLabelsRequest",
    "ListAccountLabelsResponse",
    "ListChildAccountsRequest",
    "ListChildAccountsResponse",
    "ListCssProductsRequest",
    "ListCssProductsResponse",
    "ProductDetail",
    "ProductDimension",
    "ProductWeight",
    "UpdateAccountLabelRequest",
    "UpdateAccountLabelsRequest",
)
