# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from .catalog import (
    ProductLevelConfig,
    Catalog,
)
from .catalog_service import (
    ListCatalogsRequest,
    ListCatalogsResponse,
    UpdateCatalogRequest,
)
from .common import (
    CustomAttribute,
    Image,
    PriceInfo,
    UserInfo,
)
from .product import Product
from .user_event import (
    UserEvent,
    ProductDetail,
    PurchaseTransaction,
)
from .import_config import (
    GcsSource,
    BigQuerySource,
    ProductInlineSource,
    UserEventInlineSource,
    ImportErrorsConfig,
    ImportProductsRequest,
    ImportUserEventsRequest,
    ProductInputConfig,
    UserEventInputConfig,
    ImportMetadata,
    ImportProductsResponse,
    ImportUserEventsResponse,
    UserEventImportSummary,
)
from .prediction_service import (
    PredictRequest,
    PredictResponse,
)
from .purge_config import (
    PurgeMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .product_service import (
    CreateProductRequest,
    GetProductRequest,
    UpdateProductRequest,
    DeleteProductRequest,
)
from .user_event_service import (
    WriteUserEventRequest,
    CollectUserEventRequest,
    RejoinUserEventsRequest,
    RejoinUserEventsResponse,
    RejoinUserEventsMetadata,
)

__all__ = (
    "ProductLevelConfig",
    "Catalog",
    "ListCatalogsRequest",
    "ListCatalogsResponse",
    "UpdateCatalogRequest",
    "CustomAttribute",
    "Image",
    "PriceInfo",
    "UserInfo",
    "Product",
    "UserEvent",
    "ProductDetail",
    "PurchaseTransaction",
    "GcsSource",
    "BigQuerySource",
    "ProductInlineSource",
    "UserEventInlineSource",
    "ImportErrorsConfig",
    "ImportProductsRequest",
    "ImportUserEventsRequest",
    "ProductInputConfig",
    "UserEventInputConfig",
    "ImportMetadata",
    "ImportProductsResponse",
    "ImportUserEventsResponse",
    "UserEventImportSummary",
    "PredictRequest",
    "PredictResponse",
    "PurgeMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "CreateProductRequest",
    "GetProductRequest",
    "UpdateProductRequest",
    "DeleteProductRequest",
    "WriteUserEventRequest",
    "CollectUserEventRequest",
    "RejoinUserEventsRequest",
    "RejoinUserEventsResponse",
    "RejoinUserEventsMetadata",
)
