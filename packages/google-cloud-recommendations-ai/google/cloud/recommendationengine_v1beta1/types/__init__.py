# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from .common import FeatureMap
from .catalog import CatalogItem, ProductCatalogItem, Image
from .user_event import (
    UserEvent,
    UserInfo,
    EventDetail,
    ProductEventDetail,
    PurchaseTransaction,
    ProductDetail,
)
from .prediction_service import PredictRequest, PredictResponse
from .import_ import (
    GcsSource,
    CatalogInlineSource,
    UserEventInlineSource,
    ImportErrorsConfig,
    ImportCatalogItemsRequest,
    ImportUserEventsRequest,
    InputConfig,
    ImportMetadata,
    ImportCatalogItemsResponse,
    ImportUserEventsResponse,
    UserEventImportSummary,
)
from .user_event_service import (
    PurgeUserEventsRequest,
    PurgeUserEventsMetadata,
    PurgeUserEventsResponse,
    WriteUserEventRequest,
    CollectUserEventRequest,
    ListUserEventsRequest,
    ListUserEventsResponse,
)
from .prediction_apikey_registry_service import (
    PredictionApiKeyRegistration,
    CreatePredictionApiKeyRegistrationRequest,
    ListPredictionApiKeyRegistrationsRequest,
    ListPredictionApiKeyRegistrationsResponse,
    DeletePredictionApiKeyRegistrationRequest,
)
from .catalog_service import (
    CreateCatalogItemRequest,
    GetCatalogItemRequest,
    ListCatalogItemsRequest,
    ListCatalogItemsResponse,
    UpdateCatalogItemRequest,
    DeleteCatalogItemRequest,
)


__all__ = (
    "FeatureMap",
    "CatalogItem",
    "ProductCatalogItem",
    "Image",
    "UserEvent",
    "UserInfo",
    "EventDetail",
    "ProductEventDetail",
    "PurchaseTransaction",
    "ProductDetail",
    "PredictRequest",
    "PredictResponse",
    "GcsSource",
    "CatalogInlineSource",
    "UserEventInlineSource",
    "ImportErrorsConfig",
    "ImportCatalogItemsRequest",
    "ImportUserEventsRequest",
    "InputConfig",
    "ImportMetadata",
    "ImportCatalogItemsResponse",
    "ImportUserEventsResponse",
    "UserEventImportSummary",
    "PurgeUserEventsRequest",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsResponse",
    "WriteUserEventRequest",
    "CollectUserEventRequest",
    "ListUserEventsRequest",
    "ListUserEventsResponse",
    "PredictionApiKeyRegistration",
    "CreatePredictionApiKeyRegistrationRequest",
    "ListPredictionApiKeyRegistrationsRequest",
    "ListPredictionApiKeyRegistrationsResponse",
    "DeletePredictionApiKeyRegistrationRequest",
    "CreateCatalogItemRequest",
    "GetCatalogItemRequest",
    "ListCatalogItemsRequest",
    "ListCatalogItemsResponse",
    "UpdateCatalogItemRequest",
    "DeleteCatalogItemRequest",
)
