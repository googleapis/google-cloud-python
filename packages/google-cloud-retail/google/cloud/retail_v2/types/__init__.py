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
    Catalog,
    ProductLevelConfig,
)
from .catalog_service import (
    GetDefaultBranchRequest,
    GetDefaultBranchResponse,
    ListCatalogsRequest,
    ListCatalogsResponse,
    SetDefaultBranchRequest,
    UpdateCatalogRequest,
)
from .common import (
    Audience,
    ColorInfo,
    CustomAttribute,
    FulfillmentInfo,
    Image,
    Interval,
    PriceInfo,
    Promotion,
    Rating,
    UserInfo,
)
from .completion_service import (
    CompleteQueryRequest,
    CompleteQueryResponse,
)
from .import_config import (
    BigQuerySource,
    CompletionDataInputConfig,
    GcsSource,
    ImportCompletionDataRequest,
    ImportCompletionDataResponse,
    ImportErrorsConfig,
    ImportMetadata,
    ImportProductsRequest,
    ImportProductsResponse,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    ProductInlineSource,
    ProductInputConfig,
    UserEventImportSummary,
    UserEventInlineSource,
    UserEventInputConfig,
)
from .prediction_service import (
    PredictRequest,
    PredictResponse,
)
from .product import Product
from .product_service import (
    AddFulfillmentPlacesMetadata,
    AddFulfillmentPlacesRequest,
    AddFulfillmentPlacesResponse,
    CreateProductRequest,
    DeleteProductRequest,
    GetProductRequest,
    ListProductsRequest,
    ListProductsResponse,
    RemoveFulfillmentPlacesMetadata,
    RemoveFulfillmentPlacesRequest,
    RemoveFulfillmentPlacesResponse,
    SetInventoryMetadata,
    SetInventoryRequest,
    SetInventoryResponse,
    UpdateProductRequest,
)
from .purge_config import (
    PurgeMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .search_service import (
    SearchRequest,
    SearchResponse,
)
from .user_event import (
    CompletionDetail,
    ProductDetail,
    PurchaseTransaction,
    UserEvent,
)
from .user_event_service import (
    CollectUserEventRequest,
    RejoinUserEventsMetadata,
    RejoinUserEventsRequest,
    RejoinUserEventsResponse,
    WriteUserEventRequest,
)

__all__ = (
    "Catalog",
    "ProductLevelConfig",
    "GetDefaultBranchRequest",
    "GetDefaultBranchResponse",
    "ListCatalogsRequest",
    "ListCatalogsResponse",
    "SetDefaultBranchRequest",
    "UpdateCatalogRequest",
    "Audience",
    "ColorInfo",
    "CustomAttribute",
    "FulfillmentInfo",
    "Image",
    "Interval",
    "PriceInfo",
    "Promotion",
    "Rating",
    "UserInfo",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "BigQuerySource",
    "CompletionDataInputConfig",
    "GcsSource",
    "ImportCompletionDataRequest",
    "ImportCompletionDataResponse",
    "ImportErrorsConfig",
    "ImportMetadata",
    "ImportProductsRequest",
    "ImportProductsResponse",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "ProductInlineSource",
    "ProductInputConfig",
    "UserEventImportSummary",
    "UserEventInlineSource",
    "UserEventInputConfig",
    "PredictRequest",
    "PredictResponse",
    "Product",
    "AddFulfillmentPlacesMetadata",
    "AddFulfillmentPlacesRequest",
    "AddFulfillmentPlacesResponse",
    "CreateProductRequest",
    "DeleteProductRequest",
    "GetProductRequest",
    "ListProductsRequest",
    "ListProductsResponse",
    "RemoveFulfillmentPlacesMetadata",
    "RemoveFulfillmentPlacesRequest",
    "RemoveFulfillmentPlacesResponse",
    "SetInventoryMetadata",
    "SetInventoryRequest",
    "SetInventoryResponse",
    "UpdateProductRequest",
    "PurgeMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "SearchRequest",
    "SearchResponse",
    "CompletionDetail",
    "ProductDetail",
    "PurchaseTransaction",
    "UserEvent",
    "CollectUserEventRequest",
    "RejoinUserEventsMetadata",
    "RejoinUserEventsRequest",
    "RejoinUserEventsResponse",
    "WriteUserEventRequest",
)
