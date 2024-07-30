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
from google.cloud.retail_v2alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.analytics_service import AnalyticsServiceClient
from .services.analytics_service import AnalyticsServiceAsyncClient
from .services.branch_service import BranchServiceClient
from .services.branch_service import BranchServiceAsyncClient
from .services.catalog_service import CatalogServiceClient
from .services.catalog_service import CatalogServiceAsyncClient
from .services.completion_service import CompletionServiceClient
from .services.completion_service import CompletionServiceAsyncClient
from .services.control_service import ControlServiceClient
from .services.control_service import ControlServiceAsyncClient
from .services.merchant_center_account_link_service import MerchantCenterAccountLinkServiceClient
from .services.merchant_center_account_link_service import MerchantCenterAccountLinkServiceAsyncClient
from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient
from .services.prediction_service import PredictionServiceClient
from .services.prediction_service import PredictionServiceAsyncClient
from .services.product_service import ProductServiceClient
from .services.product_service import ProductServiceAsyncClient
from .services.project_service import ProjectServiceClient
from .services.project_service import ProjectServiceAsyncClient
from .services.search_service import SearchServiceClient
from .services.search_service import SearchServiceAsyncClient
from .services.serving_config_service import ServingConfigServiceClient
from .services.serving_config_service import ServingConfigServiceAsyncClient
from .services.user_event_service import UserEventServiceClient
from .services.user_event_service import UserEventServiceAsyncClient

from .types.branch import Branch
from .types.branch import BranchView
from .types.branch_service import GetBranchRequest
from .types.branch_service import ListBranchesRequest
from .types.branch_service import ListBranchesResponse
from .types.catalog import AttributesConfig
from .types.catalog import Catalog
from .types.catalog import CatalogAttribute
from .types.catalog import CompletionConfig
from .types.catalog import MerchantCenterFeedFilter
from .types.catalog import MerchantCenterLink
from .types.catalog import MerchantCenterLinkingConfig
from .types.catalog import ProductLevelConfig
from .types.catalog_service import AddCatalogAttributeRequest
from .types.catalog_service import BatchRemoveCatalogAttributesRequest
from .types.catalog_service import BatchRemoveCatalogAttributesResponse
from .types.catalog_service import GetAttributesConfigRequest
from .types.catalog_service import GetCompletionConfigRequest
from .types.catalog_service import GetDefaultBranchRequest
from .types.catalog_service import GetDefaultBranchResponse
from .types.catalog_service import ListCatalogsRequest
from .types.catalog_service import ListCatalogsResponse
from .types.catalog_service import RemoveCatalogAttributeRequest
from .types.catalog_service import ReplaceCatalogAttributeRequest
from .types.catalog_service import SetDefaultBranchRequest
from .types.catalog_service import UpdateAttributesConfigRequest
from .types.catalog_service import UpdateCatalogRequest
from .types.catalog_service import UpdateCompletionConfigRequest
from .types.common import Audience
from .types.common import ColorInfo
from .types.common import Condition
from .types.common import CustomAttribute
from .types.common import FulfillmentInfo
from .types.common import Image
from .types.common import Interval
from .types.common import LocalInventory
from .types.common import PriceInfo
from .types.common import Rating
from .types.common import Rule
from .types.common import UserInfo
from .types.common import AttributeConfigLevel
from .types.common import RecommendationsFilteringOption
from .types.common import SearchSolutionUseCase
from .types.common import SolutionType
from .types.completion_service import CompleteQueryRequest
from .types.completion_service import CompleteQueryResponse
from .types.control import Control
from .types.control_service import CreateControlRequest
from .types.control_service import DeleteControlRequest
from .types.control_service import GetControlRequest
from .types.control_service import ListControlsRequest
from .types.control_service import ListControlsResponse
from .types.control_service import UpdateControlRequest
from .types.export_config import BigQueryOutputResult
from .types.export_config import ExportAnalyticsMetricsRequest
from .types.export_config import ExportAnalyticsMetricsResponse
from .types.export_config import ExportErrorsConfig
from .types.export_config import ExportMetadata
from .types.export_config import ExportProductsResponse
from .types.export_config import ExportUserEventsResponse
from .types.export_config import GcsOutputResult
from .types.export_config import OutputConfig
from .types.export_config import OutputResult
from .types.import_config import BigQuerySource
from .types.import_config import CompletionDataInputConfig
from .types.import_config import GcsSource
from .types.import_config import ImportCompletionDataRequest
from .types.import_config import ImportCompletionDataResponse
from .types.import_config import ImportErrorsConfig
from .types.import_config import ImportMetadata
from .types.import_config import ImportProductsRequest
from .types.import_config import ImportProductsResponse
from .types.import_config import ImportUserEventsRequest
from .types.import_config import ImportUserEventsResponse
from .types.import_config import ProductInlineSource
from .types.import_config import ProductInputConfig
from .types.import_config import TransformedUserEventsMetadata
from .types.import_config import UserEventImportSummary
from .types.import_config import UserEventInlineSource
from .types.import_config import UserEventInputConfig
from .types.merchant_center_account_link import CreateMerchantCenterAccountLinkMetadata
from .types.merchant_center_account_link import MerchantCenterAccountLink
from .types.merchant_center_account_link_service import CreateMerchantCenterAccountLinkRequest
from .types.merchant_center_account_link_service import DeleteMerchantCenterAccountLinkRequest
from .types.merchant_center_account_link_service import ListMerchantCenterAccountLinksRequest
from .types.merchant_center_account_link_service import ListMerchantCenterAccountLinksResponse
from .types.model import Model
from .types.model_service import CreateModelMetadata
from .types.model_service import CreateModelRequest
from .types.model_service import DeleteModelRequest
from .types.model_service import GetModelRequest
from .types.model_service import ListModelsRequest
from .types.model_service import ListModelsResponse
from .types.model_service import PauseModelRequest
from .types.model_service import ResumeModelRequest
from .types.model_service import TuneModelMetadata
from .types.model_service import TuneModelRequest
from .types.model_service import TuneModelResponse
from .types.model_service import UpdateModelRequest
from .types.prediction_service import PredictRequest
from .types.prediction_service import PredictResponse
from .types.product import Product
from .types.product_service import AddFulfillmentPlacesMetadata
from .types.product_service import AddFulfillmentPlacesRequest
from .types.product_service import AddFulfillmentPlacesResponse
from .types.product_service import AddLocalInventoriesMetadata
from .types.product_service import AddLocalInventoriesRequest
from .types.product_service import AddLocalInventoriesResponse
from .types.product_service import CreateProductRequest
from .types.product_service import DeleteProductRequest
from .types.product_service import GetProductRequest
from .types.product_service import ListProductsRequest
from .types.product_service import ListProductsResponse
from .types.product_service import RemoveFulfillmentPlacesMetadata
from .types.product_service import RemoveFulfillmentPlacesRequest
from .types.product_service import RemoveFulfillmentPlacesResponse
from .types.product_service import RemoveLocalInventoriesMetadata
from .types.product_service import RemoveLocalInventoriesRequest
from .types.product_service import RemoveLocalInventoriesResponse
from .types.product_service import SetInventoryMetadata
from .types.product_service import SetInventoryRequest
from .types.product_service import SetInventoryResponse
from .types.product_service import UpdateProductRequest
from .types.project import AlertConfig
from .types.project import LoggingConfig
from .types.project import Project
from .types.project_service import AcceptTermsRequest
from .types.project_service import EnrollSolutionMetadata
from .types.project_service import EnrollSolutionRequest
from .types.project_service import EnrollSolutionResponse
from .types.project_service import GetAlertConfigRequest
from .types.project_service import GetLoggingConfigRequest
from .types.project_service import GetProjectRequest
from .types.project_service import ListEnrolledSolutionsRequest
from .types.project_service import ListEnrolledSolutionsResponse
from .types.project_service import UpdateAlertConfigRequest
from .types.project_service import UpdateLoggingConfigRequest
from .types.promotion import Promotion
from .types.purge_config import PurgeMetadata
from .types.purge_config import PurgeProductsMetadata
from .types.purge_config import PurgeProductsRequest
from .types.purge_config import PurgeProductsResponse
from .types.purge_config import PurgeUserEventsRequest
from .types.purge_config import PurgeUserEventsResponse
from .types.search_service import ExperimentInfo
from .types.search_service import SearchRequest
from .types.search_service import SearchResponse
from .types.serving_config import ServingConfig
from .types.serving_config_service import AddControlRequest
from .types.serving_config_service import CreateServingConfigRequest
from .types.serving_config_service import DeleteServingConfigRequest
from .types.serving_config_service import GetServingConfigRequest
from .types.serving_config_service import ListServingConfigsRequest
from .types.serving_config_service import ListServingConfigsResponse
from .types.serving_config_service import RemoveControlRequest
from .types.serving_config_service import UpdateServingConfigRequest
from .types.user_event import CompletionDetail
from .types.user_event import ProductDetail
from .types.user_event import PurchaseTransaction
from .types.user_event import UserEvent
from .types.user_event_service import CollectUserEventRequest
from .types.user_event_service import RejoinUserEventsMetadata
from .types.user_event_service import RejoinUserEventsRequest
from .types.user_event_service import RejoinUserEventsResponse
from .types.user_event_service import WriteUserEventRequest

__all__ = (
    'AnalyticsServiceAsyncClient',
    'BranchServiceAsyncClient',
    'CatalogServiceAsyncClient',
    'CompletionServiceAsyncClient',
    'ControlServiceAsyncClient',
    'MerchantCenterAccountLinkServiceAsyncClient',
    'ModelServiceAsyncClient',
    'PredictionServiceAsyncClient',
    'ProductServiceAsyncClient',
    'ProjectServiceAsyncClient',
    'SearchServiceAsyncClient',
    'ServingConfigServiceAsyncClient',
    'UserEventServiceAsyncClient',
'AcceptTermsRequest',
'AddCatalogAttributeRequest',
'AddControlRequest',
'AddFulfillmentPlacesMetadata',
'AddFulfillmentPlacesRequest',
'AddFulfillmentPlacesResponse',
'AddLocalInventoriesMetadata',
'AddLocalInventoriesRequest',
'AddLocalInventoriesResponse',
'AlertConfig',
'AnalyticsServiceClient',
'AttributeConfigLevel',
'AttributesConfig',
'Audience',
'BatchRemoveCatalogAttributesRequest',
'BatchRemoveCatalogAttributesResponse',
'BigQueryOutputResult',
'BigQuerySource',
'Branch',
'BranchServiceClient',
'BranchView',
'Catalog',
'CatalogAttribute',
'CatalogServiceClient',
'CollectUserEventRequest',
'ColorInfo',
'CompleteQueryRequest',
'CompleteQueryResponse',
'CompletionConfig',
'CompletionDataInputConfig',
'CompletionDetail',
'CompletionServiceClient',
'Condition',
'Control',
'ControlServiceClient',
'CreateControlRequest',
'CreateMerchantCenterAccountLinkMetadata',
'CreateMerchantCenterAccountLinkRequest',
'CreateModelMetadata',
'CreateModelRequest',
'CreateProductRequest',
'CreateServingConfigRequest',
'CustomAttribute',
'DeleteControlRequest',
'DeleteMerchantCenterAccountLinkRequest',
'DeleteModelRequest',
'DeleteProductRequest',
'DeleteServingConfigRequest',
'EnrollSolutionMetadata',
'EnrollSolutionRequest',
'EnrollSolutionResponse',
'ExperimentInfo',
'ExportAnalyticsMetricsRequest',
'ExportAnalyticsMetricsResponse',
'ExportErrorsConfig',
'ExportMetadata',
'ExportProductsResponse',
'ExportUserEventsResponse',
'FulfillmentInfo',
'GcsOutputResult',
'GcsSource',
'GetAlertConfigRequest',
'GetAttributesConfigRequest',
'GetBranchRequest',
'GetCompletionConfigRequest',
'GetControlRequest',
'GetDefaultBranchRequest',
'GetDefaultBranchResponse',
'GetLoggingConfigRequest',
'GetModelRequest',
'GetProductRequest',
'GetProjectRequest',
'GetServingConfigRequest',
'Image',
'ImportCompletionDataRequest',
'ImportCompletionDataResponse',
'ImportErrorsConfig',
'ImportMetadata',
'ImportProductsRequest',
'ImportProductsResponse',
'ImportUserEventsRequest',
'ImportUserEventsResponse',
'Interval',
'ListBranchesRequest',
'ListBranchesResponse',
'ListCatalogsRequest',
'ListCatalogsResponse',
'ListControlsRequest',
'ListControlsResponse',
'ListEnrolledSolutionsRequest',
'ListEnrolledSolutionsResponse',
'ListMerchantCenterAccountLinksRequest',
'ListMerchantCenterAccountLinksResponse',
'ListModelsRequest',
'ListModelsResponse',
'ListProductsRequest',
'ListProductsResponse',
'ListServingConfigsRequest',
'ListServingConfigsResponse',
'LocalInventory',
'LoggingConfig',
'MerchantCenterAccountLink',
'MerchantCenterAccountLinkServiceClient',
'MerchantCenterFeedFilter',
'MerchantCenterLink',
'MerchantCenterLinkingConfig',
'Model',
'ModelServiceClient',
'OutputConfig',
'OutputResult',
'PauseModelRequest',
'PredictRequest',
'PredictResponse',
'PredictionServiceClient',
'PriceInfo',
'Product',
'ProductDetail',
'ProductInlineSource',
'ProductInputConfig',
'ProductLevelConfig',
'ProductServiceClient',
'Project',
'ProjectServiceClient',
'Promotion',
'PurchaseTransaction',
'PurgeMetadata',
'PurgeProductsMetadata',
'PurgeProductsRequest',
'PurgeProductsResponse',
'PurgeUserEventsRequest',
'PurgeUserEventsResponse',
'Rating',
'RecommendationsFilteringOption',
'RejoinUserEventsMetadata',
'RejoinUserEventsRequest',
'RejoinUserEventsResponse',
'RemoveCatalogAttributeRequest',
'RemoveControlRequest',
'RemoveFulfillmentPlacesMetadata',
'RemoveFulfillmentPlacesRequest',
'RemoveFulfillmentPlacesResponse',
'RemoveLocalInventoriesMetadata',
'RemoveLocalInventoriesRequest',
'RemoveLocalInventoriesResponse',
'ReplaceCatalogAttributeRequest',
'ResumeModelRequest',
'Rule',
'SearchRequest',
'SearchResponse',
'SearchServiceClient',
'SearchSolutionUseCase',
'ServingConfig',
'ServingConfigServiceClient',
'SetDefaultBranchRequest',
'SetInventoryMetadata',
'SetInventoryRequest',
'SetInventoryResponse',
'SolutionType',
'TransformedUserEventsMetadata',
'TuneModelMetadata',
'TuneModelRequest',
'TuneModelResponse',
'UpdateAlertConfigRequest',
'UpdateAttributesConfigRequest',
'UpdateCatalogRequest',
'UpdateCompletionConfigRequest',
'UpdateControlRequest',
'UpdateLoggingConfigRequest',
'UpdateModelRequest',
'UpdateProductRequest',
'UpdateServingConfigRequest',
'UserEvent',
'UserEventImportSummary',
'UserEventInlineSource',
'UserEventInputConfig',
'UserEventServiceClient',
'UserInfo',
'WriteUserEventRequest',
)
