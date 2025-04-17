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
from google.cloud.retail import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.retail_v2alpha.services.analytics_service.client import AnalyticsServiceClient
from google.cloud.retail_v2alpha.services.analytics_service.async_client import AnalyticsServiceAsyncClient
from google.cloud.retail_v2alpha.services.branch_service.client import BranchServiceClient
from google.cloud.retail_v2alpha.services.branch_service.async_client import BranchServiceAsyncClient
from google.cloud.retail_v2alpha.services.catalog_service.client import CatalogServiceClient
from google.cloud.retail_v2alpha.services.catalog_service.async_client import CatalogServiceAsyncClient
from google.cloud.retail_v2alpha.services.completion_service.client import CompletionServiceClient
from google.cloud.retail_v2alpha.services.completion_service.async_client import CompletionServiceAsyncClient
from google.cloud.retail_v2alpha.services.control_service.client import ControlServiceClient
from google.cloud.retail_v2alpha.services.control_service.async_client import ControlServiceAsyncClient
from google.cloud.retail_v2alpha.services.generative_question_service.client import GenerativeQuestionServiceClient
from google.cloud.retail_v2alpha.services.generative_question_service.async_client import GenerativeQuestionServiceAsyncClient
from google.cloud.retail_v2alpha.services.merchant_center_account_link_service.client import MerchantCenterAccountLinkServiceClient
from google.cloud.retail_v2alpha.services.merchant_center_account_link_service.async_client import MerchantCenterAccountLinkServiceAsyncClient
from google.cloud.retail_v2alpha.services.model_service.client import ModelServiceClient
from google.cloud.retail_v2alpha.services.model_service.async_client import ModelServiceAsyncClient
from google.cloud.retail_v2alpha.services.prediction_service.client import PredictionServiceClient
from google.cloud.retail_v2alpha.services.prediction_service.async_client import PredictionServiceAsyncClient
from google.cloud.retail_v2alpha.services.product_service.client import ProductServiceClient
from google.cloud.retail_v2alpha.services.product_service.async_client import ProductServiceAsyncClient
from google.cloud.retail_v2alpha.services.project_service.client import ProjectServiceClient
from google.cloud.retail_v2alpha.services.project_service.async_client import ProjectServiceAsyncClient
from google.cloud.retail_v2alpha.services.search_service.client import SearchServiceClient
from google.cloud.retail_v2alpha.services.search_service.async_client import SearchServiceAsyncClient
from google.cloud.retail_v2alpha.services.serving_config_service.client import ServingConfigServiceClient
from google.cloud.retail_v2alpha.services.serving_config_service.async_client import ServingConfigServiceAsyncClient
from google.cloud.retail_v2alpha.services.user_event_service.client import UserEventServiceClient
from google.cloud.retail_v2alpha.services.user_event_service.async_client import UserEventServiceAsyncClient

from google.cloud.retail_v2alpha.types.branch import Branch
from google.cloud.retail_v2alpha.types.branch import BranchView
from google.cloud.retail_v2alpha.types.branch_service import GetBranchRequest
from google.cloud.retail_v2alpha.types.branch_service import ListBranchesRequest
from google.cloud.retail_v2alpha.types.branch_service import ListBranchesResponse
from google.cloud.retail_v2alpha.types.catalog import AttributesConfig
from google.cloud.retail_v2alpha.types.catalog import Catalog
from google.cloud.retail_v2alpha.types.catalog import CatalogAttribute
from google.cloud.retail_v2alpha.types.catalog import CompletionConfig
from google.cloud.retail_v2alpha.types.catalog import MerchantCenterFeedFilter
from google.cloud.retail_v2alpha.types.catalog import MerchantCenterLink
from google.cloud.retail_v2alpha.types.catalog import MerchantCenterLinkingConfig
from google.cloud.retail_v2alpha.types.catalog import ProductLevelConfig
from google.cloud.retail_v2alpha.types.catalog_service import AddCatalogAttributeRequest
from google.cloud.retail_v2alpha.types.catalog_service import BatchRemoveCatalogAttributesRequest
from google.cloud.retail_v2alpha.types.catalog_service import BatchRemoveCatalogAttributesResponse
from google.cloud.retail_v2alpha.types.catalog_service import GetAttributesConfigRequest
from google.cloud.retail_v2alpha.types.catalog_service import GetCompletionConfigRequest
from google.cloud.retail_v2alpha.types.catalog_service import GetDefaultBranchRequest
from google.cloud.retail_v2alpha.types.catalog_service import GetDefaultBranchResponse
from google.cloud.retail_v2alpha.types.catalog_service import ListCatalogsRequest
from google.cloud.retail_v2alpha.types.catalog_service import ListCatalogsResponse
from google.cloud.retail_v2alpha.types.catalog_service import RemoveCatalogAttributeRequest
from google.cloud.retail_v2alpha.types.catalog_service import ReplaceCatalogAttributeRequest
from google.cloud.retail_v2alpha.types.catalog_service import SetDefaultBranchRequest
from google.cloud.retail_v2alpha.types.catalog_service import UpdateAttributesConfigRequest
from google.cloud.retail_v2alpha.types.catalog_service import UpdateCatalogRequest
from google.cloud.retail_v2alpha.types.catalog_service import UpdateCompletionConfigRequest
from google.cloud.retail_v2alpha.types.common import Audience
from google.cloud.retail_v2alpha.types.common import ColorInfo
from google.cloud.retail_v2alpha.types.common import Condition
from google.cloud.retail_v2alpha.types.common import CustomAttribute
from google.cloud.retail_v2alpha.types.common import FulfillmentInfo
from google.cloud.retail_v2alpha.types.common import Image
from google.cloud.retail_v2alpha.types.common import Interval
from google.cloud.retail_v2alpha.types.common import LocalInventory
from google.cloud.retail_v2alpha.types.common import PriceInfo
from google.cloud.retail_v2alpha.types.common import Rating
from google.cloud.retail_v2alpha.types.common import Rule
from google.cloud.retail_v2alpha.types.common import UserInfo
from google.cloud.retail_v2alpha.types.common import AttributeConfigLevel
from google.cloud.retail_v2alpha.types.common import RecommendationsFilteringOption
from google.cloud.retail_v2alpha.types.common import SearchSolutionUseCase
from google.cloud.retail_v2alpha.types.common import SolutionType
from google.cloud.retail_v2alpha.types.completion_service import CompleteQueryRequest
from google.cloud.retail_v2alpha.types.completion_service import CompleteQueryResponse
from google.cloud.retail_v2alpha.types.control import Control
from google.cloud.retail_v2alpha.types.control_service import CreateControlRequest
from google.cloud.retail_v2alpha.types.control_service import DeleteControlRequest
from google.cloud.retail_v2alpha.types.control_service import GetControlRequest
from google.cloud.retail_v2alpha.types.control_service import ListControlsRequest
from google.cloud.retail_v2alpha.types.control_service import ListControlsResponse
from google.cloud.retail_v2alpha.types.control_service import UpdateControlRequest
from google.cloud.retail_v2alpha.types.export_config import BigQueryOutputResult
from google.cloud.retail_v2alpha.types.export_config import ExportAnalyticsMetricsRequest
from google.cloud.retail_v2alpha.types.export_config import ExportAnalyticsMetricsResponse
from google.cloud.retail_v2alpha.types.export_config import ExportErrorsConfig
from google.cloud.retail_v2alpha.types.export_config import ExportMetadata
from google.cloud.retail_v2alpha.types.export_config import ExportProductsRequest
from google.cloud.retail_v2alpha.types.export_config import ExportProductsResponse
from google.cloud.retail_v2alpha.types.export_config import ExportUserEventsRequest
from google.cloud.retail_v2alpha.types.export_config import ExportUserEventsResponse
from google.cloud.retail_v2alpha.types.export_config import GcsOutputResult
from google.cloud.retail_v2alpha.types.export_config import OutputConfig
from google.cloud.retail_v2alpha.types.export_config import OutputResult
from google.cloud.retail_v2alpha.types.generative_question import GenerativeQuestionConfig
from google.cloud.retail_v2alpha.types.generative_question import GenerativeQuestionsFeatureConfig
from google.cloud.retail_v2alpha.types.generative_question_service import BatchUpdateGenerativeQuestionConfigsRequest
from google.cloud.retail_v2alpha.types.generative_question_service import BatchUpdateGenerativeQuestionConfigsResponse
from google.cloud.retail_v2alpha.types.generative_question_service import GetGenerativeQuestionsFeatureConfigRequest
from google.cloud.retail_v2alpha.types.generative_question_service import ListGenerativeQuestionConfigsRequest
from google.cloud.retail_v2alpha.types.generative_question_service import ListGenerativeQuestionConfigsResponse
from google.cloud.retail_v2alpha.types.generative_question_service import UpdateGenerativeQuestionConfigRequest
from google.cloud.retail_v2alpha.types.generative_question_service import UpdateGenerativeQuestionsFeatureConfigRequest
from google.cloud.retail_v2alpha.types.import_config import BigQuerySource
from google.cloud.retail_v2alpha.types.import_config import CompletionDataInputConfig
from google.cloud.retail_v2alpha.types.import_config import GcsSource
from google.cloud.retail_v2alpha.types.import_config import ImportCompletionDataRequest
from google.cloud.retail_v2alpha.types.import_config import ImportCompletionDataResponse
from google.cloud.retail_v2alpha.types.import_config import ImportErrorsConfig
from google.cloud.retail_v2alpha.types.import_config import ImportMetadata
from google.cloud.retail_v2alpha.types.import_config import ImportProductsRequest
from google.cloud.retail_v2alpha.types.import_config import ImportProductsResponse
from google.cloud.retail_v2alpha.types.import_config import ImportUserEventsRequest
from google.cloud.retail_v2alpha.types.import_config import ImportUserEventsResponse
from google.cloud.retail_v2alpha.types.import_config import ProductInlineSource
from google.cloud.retail_v2alpha.types.import_config import ProductInputConfig
from google.cloud.retail_v2alpha.types.import_config import TransformedUserEventsMetadata
from google.cloud.retail_v2alpha.types.import_config import UserEventImportSummary
from google.cloud.retail_v2alpha.types.import_config import UserEventInlineSource
from google.cloud.retail_v2alpha.types.import_config import UserEventInputConfig
from google.cloud.retail_v2alpha.types.merchant_center_account_link import CreateMerchantCenterAccountLinkMetadata
from google.cloud.retail_v2alpha.types.merchant_center_account_link import MerchantCenterAccountLink
from google.cloud.retail_v2alpha.types.merchant_center_account_link_service import CreateMerchantCenterAccountLinkRequest
from google.cloud.retail_v2alpha.types.merchant_center_account_link_service import DeleteMerchantCenterAccountLinkRequest
from google.cloud.retail_v2alpha.types.merchant_center_account_link_service import ListMerchantCenterAccountLinksRequest
from google.cloud.retail_v2alpha.types.merchant_center_account_link_service import ListMerchantCenterAccountLinksResponse
from google.cloud.retail_v2alpha.types.model import Model
from google.cloud.retail_v2alpha.types.model_service import CreateModelMetadata
from google.cloud.retail_v2alpha.types.model_service import CreateModelRequest
from google.cloud.retail_v2alpha.types.model_service import DeleteModelRequest
from google.cloud.retail_v2alpha.types.model_service import GetModelRequest
from google.cloud.retail_v2alpha.types.model_service import ListModelsRequest
from google.cloud.retail_v2alpha.types.model_service import ListModelsResponse
from google.cloud.retail_v2alpha.types.model_service import PauseModelRequest
from google.cloud.retail_v2alpha.types.model_service import ResumeModelRequest
from google.cloud.retail_v2alpha.types.model_service import TuneModelMetadata
from google.cloud.retail_v2alpha.types.model_service import TuneModelRequest
from google.cloud.retail_v2alpha.types.model_service import TuneModelResponse
from google.cloud.retail_v2alpha.types.model_service import UpdateModelRequest
from google.cloud.retail_v2alpha.types.prediction_service import PredictRequest
from google.cloud.retail_v2alpha.types.prediction_service import PredictResponse
from google.cloud.retail_v2alpha.types.product import Product
from google.cloud.retail_v2alpha.types.product_service import AddFulfillmentPlacesMetadata
from google.cloud.retail_v2alpha.types.product_service import AddFulfillmentPlacesRequest
from google.cloud.retail_v2alpha.types.product_service import AddFulfillmentPlacesResponse
from google.cloud.retail_v2alpha.types.product_service import AddLocalInventoriesMetadata
from google.cloud.retail_v2alpha.types.product_service import AddLocalInventoriesRequest
from google.cloud.retail_v2alpha.types.product_service import AddLocalInventoriesResponse
from google.cloud.retail_v2alpha.types.product_service import CreateProductRequest
from google.cloud.retail_v2alpha.types.product_service import DeleteProductRequest
from google.cloud.retail_v2alpha.types.product_service import GetProductRequest
from google.cloud.retail_v2alpha.types.product_service import ListProductsRequest
from google.cloud.retail_v2alpha.types.product_service import ListProductsResponse
from google.cloud.retail_v2alpha.types.product_service import RemoveFulfillmentPlacesMetadata
from google.cloud.retail_v2alpha.types.product_service import RemoveFulfillmentPlacesRequest
from google.cloud.retail_v2alpha.types.product_service import RemoveFulfillmentPlacesResponse
from google.cloud.retail_v2alpha.types.product_service import RemoveLocalInventoriesMetadata
from google.cloud.retail_v2alpha.types.product_service import RemoveLocalInventoriesRequest
from google.cloud.retail_v2alpha.types.product_service import RemoveLocalInventoriesResponse
from google.cloud.retail_v2alpha.types.product_service import SetInventoryMetadata
from google.cloud.retail_v2alpha.types.product_service import SetInventoryRequest
from google.cloud.retail_v2alpha.types.product_service import SetInventoryResponse
from google.cloud.retail_v2alpha.types.product_service import UpdateProductRequest
from google.cloud.retail_v2alpha.types.project import AlertConfig
from google.cloud.retail_v2alpha.types.project import LoggingConfig
from google.cloud.retail_v2alpha.types.project import Project
from google.cloud.retail_v2alpha.types.project_service import AcceptTermsRequest
from google.cloud.retail_v2alpha.types.project_service import EnrollSolutionMetadata
from google.cloud.retail_v2alpha.types.project_service import EnrollSolutionRequest
from google.cloud.retail_v2alpha.types.project_service import EnrollSolutionResponse
from google.cloud.retail_v2alpha.types.project_service import GetAlertConfigRequest
from google.cloud.retail_v2alpha.types.project_service import GetLoggingConfigRequest
from google.cloud.retail_v2alpha.types.project_service import GetProjectRequest
from google.cloud.retail_v2alpha.types.project_service import ListEnrolledSolutionsRequest
from google.cloud.retail_v2alpha.types.project_service import ListEnrolledSolutionsResponse
from google.cloud.retail_v2alpha.types.project_service import UpdateAlertConfigRequest
from google.cloud.retail_v2alpha.types.project_service import UpdateLoggingConfigRequest
from google.cloud.retail_v2alpha.types.promotion import Promotion
from google.cloud.retail_v2alpha.types.purge_config import PurgeMetadata
from google.cloud.retail_v2alpha.types.purge_config import PurgeProductsMetadata
from google.cloud.retail_v2alpha.types.purge_config import PurgeProductsRequest
from google.cloud.retail_v2alpha.types.purge_config import PurgeProductsResponse
from google.cloud.retail_v2alpha.types.purge_config import PurgeUserEventsRequest
from google.cloud.retail_v2alpha.types.purge_config import PurgeUserEventsResponse
from google.cloud.retail_v2alpha.types.search_service import ExperimentInfo
from google.cloud.retail_v2alpha.types.search_service import ProductAttributeInterval
from google.cloud.retail_v2alpha.types.search_service import ProductAttributeValue
from google.cloud.retail_v2alpha.types.search_service import SearchRequest
from google.cloud.retail_v2alpha.types.search_service import SearchResponse
from google.cloud.retail_v2alpha.types.search_service import Tile
from google.cloud.retail_v2alpha.types.serving_config import ServingConfig
from google.cloud.retail_v2alpha.types.serving_config_service import AddControlRequest
from google.cloud.retail_v2alpha.types.serving_config_service import CreateServingConfigRequest
from google.cloud.retail_v2alpha.types.serving_config_service import DeleteServingConfigRequest
from google.cloud.retail_v2alpha.types.serving_config_service import GetServingConfigRequest
from google.cloud.retail_v2alpha.types.serving_config_service import ListServingConfigsRequest
from google.cloud.retail_v2alpha.types.serving_config_service import ListServingConfigsResponse
from google.cloud.retail_v2alpha.types.serving_config_service import RemoveControlRequest
from google.cloud.retail_v2alpha.types.serving_config_service import UpdateServingConfigRequest
from google.cloud.retail_v2alpha.types.user_event import CompletionDetail
from google.cloud.retail_v2alpha.types.user_event import ProductDetail
from google.cloud.retail_v2alpha.types.user_event import PurchaseTransaction
from google.cloud.retail_v2alpha.types.user_event import UserEvent
from google.cloud.retail_v2alpha.types.user_event_service import CollectUserEventRequest
from google.cloud.retail_v2alpha.types.user_event_service import RejoinUserEventsMetadata
from google.cloud.retail_v2alpha.types.user_event_service import RejoinUserEventsRequest
from google.cloud.retail_v2alpha.types.user_event_service import RejoinUserEventsResponse
from google.cloud.retail_v2alpha.types.user_event_service import WriteUserEventRequest

__all__ = ('AnalyticsServiceClient',
    'AnalyticsServiceAsyncClient',
    'BranchServiceClient',
    'BranchServiceAsyncClient',
    'CatalogServiceClient',
    'CatalogServiceAsyncClient',
    'CompletionServiceClient',
    'CompletionServiceAsyncClient',
    'ControlServiceClient',
    'ControlServiceAsyncClient',
    'GenerativeQuestionServiceClient',
    'GenerativeQuestionServiceAsyncClient',
    'MerchantCenterAccountLinkServiceClient',
    'MerchantCenterAccountLinkServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'PredictionServiceClient',
    'PredictionServiceAsyncClient',
    'ProductServiceClient',
    'ProductServiceAsyncClient',
    'ProjectServiceClient',
    'ProjectServiceAsyncClient',
    'SearchServiceClient',
    'SearchServiceAsyncClient',
    'ServingConfigServiceClient',
    'ServingConfigServiceAsyncClient',
    'UserEventServiceClient',
    'UserEventServiceAsyncClient',
    'Branch',
    'BranchView',
    'GetBranchRequest',
    'ListBranchesRequest',
    'ListBranchesResponse',
    'AttributesConfig',
    'Catalog',
    'CatalogAttribute',
    'CompletionConfig',
    'MerchantCenterFeedFilter',
    'MerchantCenterLink',
    'MerchantCenterLinkingConfig',
    'ProductLevelConfig',
    'AddCatalogAttributeRequest',
    'BatchRemoveCatalogAttributesRequest',
    'BatchRemoveCatalogAttributesResponse',
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
    'BigQueryOutputResult',
    'ExportAnalyticsMetricsRequest',
    'ExportAnalyticsMetricsResponse',
    'ExportErrorsConfig',
    'ExportMetadata',
    'ExportProductsRequest',
    'ExportProductsResponse',
    'ExportUserEventsRequest',
    'ExportUserEventsResponse',
    'GcsOutputResult',
    'OutputConfig',
    'OutputResult',
    'GenerativeQuestionConfig',
    'GenerativeQuestionsFeatureConfig',
    'BatchUpdateGenerativeQuestionConfigsRequest',
    'BatchUpdateGenerativeQuestionConfigsResponse',
    'GetGenerativeQuestionsFeatureConfigRequest',
    'ListGenerativeQuestionConfigsRequest',
    'ListGenerativeQuestionConfigsResponse',
    'UpdateGenerativeQuestionConfigRequest',
    'UpdateGenerativeQuestionsFeatureConfigRequest',
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
    'TransformedUserEventsMetadata',
    'UserEventImportSummary',
    'UserEventInlineSource',
    'UserEventInputConfig',
    'CreateMerchantCenterAccountLinkMetadata',
    'MerchantCenterAccountLink',
    'CreateMerchantCenterAccountLinkRequest',
    'DeleteMerchantCenterAccountLinkRequest',
    'ListMerchantCenterAccountLinksRequest',
    'ListMerchantCenterAccountLinksResponse',
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
    'AlertConfig',
    'LoggingConfig',
    'Project',
    'AcceptTermsRequest',
    'EnrollSolutionMetadata',
    'EnrollSolutionRequest',
    'EnrollSolutionResponse',
    'GetAlertConfigRequest',
    'GetLoggingConfigRequest',
    'GetProjectRequest',
    'ListEnrolledSolutionsRequest',
    'ListEnrolledSolutionsResponse',
    'UpdateAlertConfigRequest',
    'UpdateLoggingConfigRequest',
    'Promotion',
    'PurgeMetadata',
    'PurgeProductsMetadata',
    'PurgeProductsRequest',
    'PurgeProductsResponse',
    'PurgeUserEventsRequest',
    'PurgeUserEventsResponse',
    'ExperimentInfo',
    'ProductAttributeInterval',
    'ProductAttributeValue',
    'SearchRequest',
    'SearchResponse',
    'Tile',
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
