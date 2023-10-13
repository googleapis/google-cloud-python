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
from google.cloud.retail import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.retail_v2.services.catalog_service.client import CatalogServiceClient
from google.cloud.retail_v2.services.catalog_service.async_client import CatalogServiceAsyncClient
from google.cloud.retail_v2.services.completion_service.client import CompletionServiceClient
from google.cloud.retail_v2.services.completion_service.async_client import CompletionServiceAsyncClient
from google.cloud.retail_v2.services.control_service.client import ControlServiceClient
from google.cloud.retail_v2.services.control_service.async_client import ControlServiceAsyncClient
from google.cloud.retail_v2.services.model_service.client import ModelServiceClient
from google.cloud.retail_v2.services.model_service.async_client import ModelServiceAsyncClient
from google.cloud.retail_v2.services.prediction_service.client import PredictionServiceClient
from google.cloud.retail_v2.services.prediction_service.async_client import PredictionServiceAsyncClient
from google.cloud.retail_v2.services.product_service.client import ProductServiceClient
from google.cloud.retail_v2.services.product_service.async_client import ProductServiceAsyncClient
from google.cloud.retail_v2.services.search_service.client import SearchServiceClient
from google.cloud.retail_v2.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.retail_v2.services.serving_config_service.client import ServingConfigServiceClient
from google.cloud.retail_v2.services.serving_config_service.async_client import ServingConfigServiceAsyncClient
from google.cloud.retail_v2.services.user_event_service.client import UserEventServiceClient
from google.cloud.retail_v2.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.retail_v2.types.catalog import AttributesConfig
from google.cloud.retail_v2.types.catalog import Catalog
from google.cloud.retail_v2.types.catalog import CatalogAttribute
from google.cloud.retail_v2.types.catalog import CompletionConfig
from google.cloud.retail_v2.types.catalog import ProductLevelConfig
from google.cloud.retail_v2.types.catalog_service import AddCatalogAttributeRequest
from google.cloud.retail_v2.types.catalog_service import GetAttributesConfigRequest
from google.cloud.retail_v2.types.catalog_service import GetCompletionConfigRequest
from google.cloud.retail_v2.types.catalog_service import GetDefaultBranchRequest
from google.cloud.retail_v2.types.catalog_service import GetDefaultBranchResponse
from google.cloud.retail_v2.types.catalog_service import ListCatalogsRequest
from google.cloud.retail_v2.types.catalog_service import ListCatalogsResponse
from google.cloud.retail_v2.types.catalog_service import RemoveCatalogAttributeRequest
from google.cloud.retail_v2.types.catalog_service import ReplaceCatalogAttributeRequest
from google.cloud.retail_v2.types.catalog_service import SetDefaultBranchRequest
from google.cloud.retail_v2.types.catalog_service import UpdateAttributesConfigRequest
from google.cloud.retail_v2.types.catalog_service import UpdateCatalogRequest
from google.cloud.retail_v2.types.catalog_service import UpdateCompletionConfigRequest
from google.cloud.retail_v2.types.common import Audience
from google.cloud.retail_v2.types.common import ColorInfo
from google.cloud.retail_v2.types.common import Condition
from google.cloud.retail_v2.types.common import CustomAttribute
from google.cloud.retail_v2.types.common import FulfillmentInfo
from google.cloud.retail_v2.types.common import Image
from google.cloud.retail_v2.types.common import Interval
from google.cloud.retail_v2.types.common import LocalInventory
from google.cloud.retail_v2.types.common import PriceInfo
from google.cloud.retail_v2.types.common import Rating
from google.cloud.retail_v2.types.common import Rule
from google.cloud.retail_v2.types.common import UserInfo
from google.cloud.retail_v2.types.common import AttributeConfigLevel
from google.cloud.retail_v2.types.common import RecommendationsFilteringOption
from google.cloud.retail_v2.types.common import SearchSolutionUseCase
from google.cloud.retail_v2.types.common import SolutionType
from google.cloud.retail_v2.types.completion_service import CompleteQueryRequest
from google.cloud.retail_v2.types.completion_service import CompleteQueryResponse
from google.cloud.retail_v2.types.control import Control
from google.cloud.retail_v2.types.control_service import CreateControlRequest
from google.cloud.retail_v2.types.control_service import DeleteControlRequest
from google.cloud.retail_v2.types.control_service import GetControlRequest
from google.cloud.retail_v2.types.control_service import ListControlsRequest
from google.cloud.retail_v2.types.control_service import ListControlsResponse
from google.cloud.retail_v2.types.control_service import UpdateControlRequest
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
from google.cloud.retail_v2.types.model import Model
from google.cloud.retail_v2.types.model_service import CreateModelMetadata
from google.cloud.retail_v2.types.model_service import CreateModelRequest
from google.cloud.retail_v2.types.model_service import DeleteModelRequest
from google.cloud.retail_v2.types.model_service import GetModelRequest
from google.cloud.retail_v2.types.model_service import ListModelsRequest
from google.cloud.retail_v2.types.model_service import ListModelsResponse
from google.cloud.retail_v2.types.model_service import PauseModelRequest
from google.cloud.retail_v2.types.model_service import ResumeModelRequest
from google.cloud.retail_v2.types.model_service import TuneModelMetadata
from google.cloud.retail_v2.types.model_service import TuneModelRequest
from google.cloud.retail_v2.types.model_service import TuneModelResponse
from google.cloud.retail_v2.types.model_service import UpdateModelRequest
from google.cloud.retail_v2.types.prediction_service import PredictRequest
from google.cloud.retail_v2.types.prediction_service import PredictResponse
from google.cloud.retail_v2.types.product import Product
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesMetadata
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesRequest
from google.cloud.retail_v2.types.product_service import AddFulfillmentPlacesResponse
from google.cloud.retail_v2.types.product_service import AddLocalInventoriesMetadata
from google.cloud.retail_v2.types.product_service import AddLocalInventoriesRequest
from google.cloud.retail_v2.types.product_service import AddLocalInventoriesResponse
from google.cloud.retail_v2.types.product_service import CreateProductRequest
from google.cloud.retail_v2.types.product_service import DeleteProductRequest
from google.cloud.retail_v2.types.product_service import GetProductRequest
from google.cloud.retail_v2.types.product_service import ListProductsRequest
from google.cloud.retail_v2.types.product_service import ListProductsResponse
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesMetadata
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesRequest
from google.cloud.retail_v2.types.product_service import RemoveFulfillmentPlacesResponse
from google.cloud.retail_v2.types.product_service import RemoveLocalInventoriesMetadata
from google.cloud.retail_v2.types.product_service import RemoveLocalInventoriesRequest
from google.cloud.retail_v2.types.product_service import RemoveLocalInventoriesResponse
from google.cloud.retail_v2.types.product_service import SetInventoryMetadata
from google.cloud.retail_v2.types.product_service import SetInventoryRequest
from google.cloud.retail_v2.types.product_service import SetInventoryResponse
from google.cloud.retail_v2.types.product_service import UpdateProductRequest
from google.cloud.retail_v2.types.promotion import Promotion
from google.cloud.retail_v2.types.purge_config import PurgeMetadata
from google.cloud.retail_v2.types.purge_config import PurgeUserEventsRequest
from google.cloud.retail_v2.types.purge_config import PurgeUserEventsResponse
from google.cloud.retail_v2.types.search_service import ExperimentInfo
from google.cloud.retail_v2.types.search_service import SearchRequest
from google.cloud.retail_v2.types.search_service import SearchResponse
from google.cloud.retail_v2.types.serving_config import ServingConfig
from google.cloud.retail_v2.types.serving_config_service import AddControlRequest
from google.cloud.retail_v2.types.serving_config_service import CreateServingConfigRequest
from google.cloud.retail_v2.types.serving_config_service import DeleteServingConfigRequest
from google.cloud.retail_v2.types.serving_config_service import GetServingConfigRequest
from google.cloud.retail_v2.types.serving_config_service import ListServingConfigsRequest
from google.cloud.retail_v2.types.serving_config_service import ListServingConfigsResponse
from google.cloud.retail_v2.types.serving_config_service import RemoveControlRequest
from google.cloud.retail_v2.types.serving_config_service import UpdateServingConfigRequest
from google.cloud.retail_v2.types.user_event import CompletionDetail
from google.cloud.retail_v2.types.user_event import ProductDetail
from google.cloud.retail_v2.types.user_event import PurchaseTransaction
from google.cloud.retail_v2.types.user_event import UserEvent
from google.cloud.retail_v2.types.user_event_service import CollectUserEventRequest
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsMetadata
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsRequest
from google.cloud.retail_v2.types.user_event_service import RejoinUserEventsResponse
from google.cloud.retail_v2.types.user_event_service import WriteUserEventRequest

__all__ = ('CatalogServiceClient',
    'CatalogServiceAsyncClient',
    'CompletionServiceClient',
    'CompletionServiceAsyncClient',
    'ControlServiceClient',
    'ControlServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'PredictionServiceClient',
    'PredictionServiceAsyncClient',
    'ProductServiceClient',
    'ProductServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'ServingConfigServiceClient',
    'ServingConfigServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'AttributesConfig',
    'Catalog',
    'CatalogAttribute',
    'CompletionConfig',
    'ProductLevelConfig',
    'AddCatalogAttributeRequest',
    'GetAttributesConfigRequest',
    'GetCompletionConfigRequest',
    'GetDefaultBranchRequest',
    'GetDefaultBranchResponse',
    'ListCatalogsRequest',
    'ListCatalogsResponse',
    'RemoveCatalogAttributeRequest',
    'ReplaceCatalogAttributeRequest',
    'SetDefaultBranchRequest',
    'UpdateAttributesConfigRequest',
    'UpdateCatalogRequest',
    'UpdateCompletionConfigRequest',
    'Audience',
    'ColorInfo',
    'Condition',
    'CustomAttribute',
    'FulfillmentInfo',
    'Image',
    'Interval',
    'LocalInventory',
    'PriceInfo',
    'Rating',
    'Rule',
    'UserInfo',
    'AttributeConfigLevel',
    'RecommendationsFilteringOption',
    'SearchSolutionUseCase',
    'SolutionType',
    'CompleteQueryRequest',
    'CompleteQueryResponse',
    'Control',
    'CreateControlRequest',
    'DeleteControlRequest',
    'GetControlRequest',
    'ListControlsRequest',
    'ListControlsResponse',
    'UpdateControlRequest',
    'BigQuerySource',
    'CompletionDataInputConfig',
    'GcsSource',
    'ImportCompletionDataRequest',
    'ImportCompletionDataResponse',
    'ImportErrorsConfig',
    'ImportMetadata',
    'ImportProductsRequest',
    'ImportProductsResponse',
    'ImportUserEventsRequest',
    'ImportUserEventsResponse',
    'ProductInlineSource',
    'ProductInputConfig',
    'UserEventImportSummary',
    'UserEventInlineSource',
    'UserEventInputConfig',
    'Model',
    'CreateModelMetadata',
    'CreateModelRequest',
    'DeleteModelRequest',
    'GetModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'PauseModelRequest',
    'ResumeModelRequest',
    'TuneModelMetadata',
    'TuneModelRequest',
    'TuneModelResponse',
    'UpdateModelRequest',
    'PredictRequest',
    'PredictResponse',
    'Product',
    'AddFulfillmentPlacesMetadata',
    'AddFulfillmentPlacesRequest',
    'AddFulfillmentPlacesResponse',
    'AddLocalInventoriesMetadata',
    'AddLocalInventoriesRequest',
    'AddLocalInventoriesResponse',
    'CreateProductRequest',
    'DeleteProductRequest',
    'GetProductRequest',
    'ListProductsRequest',
    'ListProductsResponse',
    'RemoveFulfillmentPlacesMetadata',
    'RemoveFulfillmentPlacesRequest',
    'RemoveFulfillmentPlacesResponse',
    'RemoveLocalInventoriesMetadata',
    'RemoveLocalInventoriesRequest',
    'RemoveLocalInventoriesResponse',
    'SetInventoryMetadata',
    'SetInventoryRequest',
    'SetInventoryResponse',
    'UpdateProductRequest',
    'Promotion',
    'PurgeMetadata',
    'PurgeUserEventsRequest',
    'PurgeUserEventsResponse',
    'ExperimentInfo',
    'SearchRequest',
    'SearchResponse',
    'ServingConfig',
    'AddControlRequest',
    'CreateServingConfigRequest',
    'DeleteServingConfigRequest',
    'GetServingConfigRequest',
    'ListServingConfigsRequest',
    'ListServingConfigsResponse',
    'RemoveControlRequest',
    'UpdateServingConfigRequest',
    'CompletionDetail',
    'ProductDetail',
    'PurchaseTransaction',
    'UserEvent',
    'CollectUserEventRequest',
    'RejoinUserEventsMetadata',
    'RejoinUserEventsRequest',
    'RejoinUserEventsResponse',
    'WriteUserEventRequest',
)
