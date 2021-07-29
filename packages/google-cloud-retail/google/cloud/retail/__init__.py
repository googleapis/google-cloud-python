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

from google.cloud.retail_v2.services.catalog_service.client import CatalogServiceClient
from google.cloud.retail_v2.services.catalog_service.async_client import (
    CatalogServiceAsyncClient,
)
from google.cloud.retail_v2.services.completion_service.client import (
    CompletionServiceClient,
)
from google.cloud.retail_v2.services.completion_service.async_client import (
    CompletionServiceAsyncClient,
)
from google.cloud.retail_v2.services.prediction_service.client import (
    PredictionServiceClient,
)
from google.cloud.retail_v2.services.prediction_service.async_client import (
    PredictionServiceAsyncClient,
)
from google.cloud.retail_v2.services.product_service.client import ProductServiceClient
from google.cloud.retail_v2.services.product_service.async_client import (
    ProductServiceAsyncClient,
)
from google.cloud.retail_v2.services.search_service.client import SearchServiceClient
from google.cloud.retail_v2.services.search_service.async_client import (
    SearchServiceAsyncClient,
)
from google.cloud.retail_v2.services.user_event_service.client import (
    UserEventServiceClient,
)
from google.cloud.retail_v2.services.user_event_service.async_client import (
    UserEventServiceAsyncClient,
)

from google.cloud.retail_v2.types.catalog import Catalog
from google.cloud.retail_v2.types.catalog import ProductLevelConfig
from google.cloud.retail_v2.types.catalog_service import GetDefaultBranchRequest
from google.cloud.retail_v2.types.catalog_service import GetDefaultBranchResponse
from google.cloud.retail_v2.types.catalog_service import ListCatalogsRequest
from google.cloud.retail_v2.types.catalog_service import ListCatalogsResponse
from google.cloud.retail_v2.types.catalog_service import SetDefaultBranchRequest
from google.cloud.retail_v2.types.catalog_service import UpdateCatalogRequest
from google.cloud.retail_v2.types.common import Audience
from google.cloud.retail_v2.types.common import ColorInfo
from google.cloud.retail_v2.types.common import CustomAttribute
from google.cloud.retail_v2.types.common import FulfillmentInfo
from google.cloud.retail_v2.types.common import Image
from google.cloud.retail_v2.types.common import Interval
from google.cloud.retail_v2.types.common import PriceInfo
from google.cloud.retail_v2.types.common import Promotion
from google.cloud.retail_v2.types.common import Rating
from google.cloud.retail_v2.types.common import UserInfo
from google.cloud.retail_v2.types.completion_service import CompleteQueryRequest
from google.cloud.retail_v2.types.completion_service import CompleteQueryResponse
from google.cloud.retail_v2.types.import_config import BigQuerySource
from google.cloud.retail_v2.types.import_config import CompletionDataInputConfig
from google.cloud.retail_v2.types.import_config import GcsSource
from google.cloud.retail_v2.types.import_config import ImportCompletionDataRequest
from google.cloud.retail_v2.types.import_config import ImportCompletionDataResponse
from google.cloud.retail_v2.types.import_config import ImportErrorsConfig
from google.cloud.retail_v2.types.import_config import ImportMetadata
from google.cloud.retail_v2.types.import_config import ImportProductsRequest
from google.cloud.retail_v2.types.import_config import ImportProductsResponse
from google.cloud.retail_v2.types.import_config import ImportUserEventsRequest
from google.cloud.retail_v2.types.import_config import ImportUserEventsResponse
from google.cloud.retail_v2.types.import_config import ProductInlineSource
from google.cloud.retail_v2.types.import_config import ProductInputConfig
from google.cloud.retail_v2.types.import_config import UserEventImportSummary
from google.cloud.retail_v2.types.import_config import UserEventInlineSource
from google.cloud.retail_v2.types.import_config import UserEventInputConfig
from google.cloud.retail_v2.types.prediction_service import PredictRequest
from google.cloud.retail_v2.types.prediction_service import PredictResponse
from google.cloud.retail_v2.types.product import Product
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesMetadata
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesRequest
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesResponse
from google.cloud.retail_v2.types.product_service import CreateProductRequest
from google.cloud.retail_v2.types.product_service import DeleteProductRequest
from google.cloud.retail_v2.types.product_service import GetProductRequest
from google.cloud.retail_v2.types.product_service import ListProductsRequest
from google.cloud.retail_v2.types.product_service import ListProductsResponse
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesMetadata
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesRequest
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesResponse
from google.cloud.retail_v2.types.product_service import SetInventoryMetadata
from google.cloud.retail_v2.types.product_service import SetInventoryRequest
from google.cloud.retail_v2.types.product_service import SetInventoryResponse
from google.cloud.retail_v2.types.product_service import UpdateProductRequest
from google.cloud.retail_v2.types.purge_config import PurgeMetadata
from google.cloud.retail_v2.types.purge_config import PurgeUserEventsRequest
from google.cloud.retail_v2.types.purge_config import PurgeUserEventsResponse
from google.cloud.retail_v2.types.search_service import SearchRequest
from google.cloud.retail_v2.types.search_service import SearchResponse
from google.cloud.retail_v2.types.user_event import CompletionDetail
from google.cloud.retail_v2.types.user_event import ProductDetail
from google.cloud.retail_v2.types.user_event import PurchaseTransaction
from google.cloud.retail_v2.types.user_event import UserEvent
from google.cloud.retail_v2.types.user_event_service import CollectUserEventRequest
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsMetadata
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsRequest
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsResponse
from google.cloud.retail_v2.types.user_event_service import WriteUserEventRequest

__all__ = (
    "CatalogServiceClient",
    "CatalogServiceAsyncClient",
    "CompletionServiceClient",
    "CompletionServiceAsyncClient",
    "PredictionServiceClient",
    "PredictionServiceAsyncClient",
    "ProductServiceClient",
    "ProductServiceAsyncClient",
    "SearchServiceClient",
    "SearchServiceAsyncClient",
    "UserEventServiceClient",
    "UserEventServiceAsyncClient",
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
