# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from .services.catalog_service import CatalogServiceAsyncClient, CatalogServiceClient
from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .services.product_service import ProductServiceAsyncClient, ProductServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.catalog import Catalog, ProductLevelConfig
from .types.catalog_service import (
    GetDefaultBranchRequest,
    GetDefaultBranchResponse,
    ListCatalogsRequest,
    ListCatalogsResponse,
    SetDefaultBranchRequest,
    UpdateCatalogRequest,
)
from .types.common import (
    Audience,
    ColorInfo,
    CustomAttribute,
    FulfillmentInfo,
    Image,
    Interval,
    LocalInventory,
    PriceInfo,
    Rating,
    UserInfo,
)
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.import_config import (
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
from .types.prediction_service import PredictRequest, PredictResponse
from .types.product import Product
from .types.product_service import (
    AddFulfillmentPlacesMetadata,
    AddFulfillmentPlacesRequest,
    AddFulfillmentPlacesResponse,
    AddLocalInventoriesMetadata,
    AddLocalInventoriesRequest,
    AddLocalInventoriesResponse,
    CreateProductRequest,
    DeleteProductRequest,
    GetProductRequest,
    ListProductsRequest,
    ListProductsResponse,
    RemoveFulfillmentPlacesMetadata,
    RemoveFulfillmentPlacesRequest,
    RemoveFulfillmentPlacesResponse,
    RemoveLocalInventoriesMetadata,
    RemoveLocalInventoriesRequest,
    RemoveLocalInventoriesResponse,
    SetInventoryMetadata,
    SetInventoryRequest,
    SetInventoryResponse,
    UpdateProductRequest,
)
from .types.promotion import Promotion
from .types.purge_config import (
    PurgeMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .types.search_service import SearchRequest, SearchResponse
from .types.user_event import (
    CompletionDetail,
    ProductDetail,
    PurchaseTransaction,
    UserEvent,
)
from .types.user_event_service import (
    CollectUserEventRequest,
    RejoinUserEventsMetadata,
    RejoinUserEventsRequest,
    RejoinUserEventsResponse,
    WriteUserEventRequest,
)

__all__ = (
    "CatalogServiceAsyncClient",
    "CompletionServiceAsyncClient",
    "PredictionServiceAsyncClient",
    "ProductServiceAsyncClient",
    "SearchServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AddFulfillmentPlacesMetadata",
    "AddFulfillmentPlacesRequest",
    "AddFulfillmentPlacesResponse",
    "AddLocalInventoriesMetadata",
    "AddLocalInventoriesRequest",
    "AddLocalInventoriesResponse",
    "Audience",
    "BigQuerySource",
    "Catalog",
    "CatalogServiceClient",
    "CollectUserEventRequest",
    "ColorInfo",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionDataInputConfig",
    "CompletionDetail",
    "CompletionServiceClient",
    "CreateProductRequest",
    "CustomAttribute",
    "DeleteProductRequest",
    "FulfillmentInfo",
    "GcsSource",
    "GetDefaultBranchRequest",
    "GetDefaultBranchResponse",
    "GetProductRequest",
    "Image",
    "ImportCompletionDataRequest",
    "ImportCompletionDataResponse",
    "ImportErrorsConfig",
    "ImportMetadata",
    "ImportProductsRequest",
    "ImportProductsResponse",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "Interval",
    "ListCatalogsRequest",
    "ListCatalogsResponse",
    "ListProductsRequest",
    "ListProductsResponse",
    "LocalInventory",
    "PredictRequest",
    "PredictResponse",
    "PredictionServiceClient",
    "PriceInfo",
    "Product",
    "ProductDetail",
    "ProductInlineSource",
    "ProductInputConfig",
    "ProductLevelConfig",
    "ProductServiceClient",
    "Promotion",
    "PurchaseTransaction",
    "PurgeMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "Rating",
    "RejoinUserEventsMetadata",
    "RejoinUserEventsRequest",
    "RejoinUserEventsResponse",
    "RemoveFulfillmentPlacesMetadata",
    "RemoveFulfillmentPlacesRequest",
    "RemoveFulfillmentPlacesResponse",
    "RemoveLocalInventoriesMetadata",
    "RemoveLocalInventoriesRequest",
    "RemoveLocalInventoriesResponse",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SetDefaultBranchRequest",
    "SetInventoryMetadata",
    "SetInventoryRequest",
    "SetInventoryResponse",
    "UpdateCatalogRequest",
    "UpdateProductRequest",
    "UserEvent",
    "UserEventImportSummary",
    "UserEventInlineSource",
    "UserEventInputConfig",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
