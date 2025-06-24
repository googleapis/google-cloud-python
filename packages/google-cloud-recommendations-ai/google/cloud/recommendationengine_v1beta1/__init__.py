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
from google.cloud.recommendationengine_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.catalog_service import CatalogServiceAsyncClient, CatalogServiceClient
from .services.prediction_api_key_registry import (
    PredictionApiKeyRegistryAsyncClient,
    PredictionApiKeyRegistryClient,
)
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.catalog import CatalogItem, Image, ProductCatalogItem
from .types.catalog_service import (
    CreateCatalogItemRequest,
    DeleteCatalogItemRequest,
    GetCatalogItemRequest,
    ListCatalogItemsRequest,
    ListCatalogItemsResponse,
    UpdateCatalogItemRequest,
)
from .types.common import FeatureMap
from .types.import_ import (
    CatalogInlineSource,
    GcsSource,
    ImportCatalogItemsRequest,
    ImportCatalogItemsResponse,
    ImportErrorsConfig,
    ImportMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    InputConfig,
    UserEventImportSummary,
    UserEventInlineSource,
)
from .types.prediction_apikey_registry_service import (
    CreatePredictionApiKeyRegistrationRequest,
    DeletePredictionApiKeyRegistrationRequest,
    ListPredictionApiKeyRegistrationsRequest,
    ListPredictionApiKeyRegistrationsResponse,
    PredictionApiKeyRegistration,
)
from .types.prediction_service import PredictRequest, PredictResponse
from .types.user_event import (
    EventDetail,
    ProductDetail,
    ProductEventDetail,
    PurchaseTransaction,
    UserEvent,
    UserInfo,
)
from .types.user_event_service import (
    CollectUserEventRequest,
    ListUserEventsRequest,
    ListUserEventsResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
    WriteUserEventRequest,
)

__all__ = (
    "CatalogServiceAsyncClient",
    "PredictionApiKeyRegistryAsyncClient",
    "PredictionServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "CatalogInlineSource",
    "CatalogItem",
    "CatalogServiceClient",
    "CollectUserEventRequest",
    "CreateCatalogItemRequest",
    "CreatePredictionApiKeyRegistrationRequest",
    "DeleteCatalogItemRequest",
    "DeletePredictionApiKeyRegistrationRequest",
    "EventDetail",
    "FeatureMap",
    "GcsSource",
    "GetCatalogItemRequest",
    "Image",
    "ImportCatalogItemsRequest",
    "ImportCatalogItemsResponse",
    "ImportErrorsConfig",
    "ImportMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "InputConfig",
    "ListCatalogItemsRequest",
    "ListCatalogItemsResponse",
    "ListPredictionApiKeyRegistrationsRequest",
    "ListPredictionApiKeyRegistrationsResponse",
    "ListUserEventsRequest",
    "ListUserEventsResponse",
    "PredictRequest",
    "PredictResponse",
    "PredictionApiKeyRegistration",
    "PredictionApiKeyRegistryClient",
    "PredictionServiceClient",
    "ProductCatalogItem",
    "ProductDetail",
    "ProductEventDetail",
    "PurchaseTransaction",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "UpdateCatalogItemRequest",
    "UserEvent",
    "UserEventImportSummary",
    "UserEventInlineSource",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
