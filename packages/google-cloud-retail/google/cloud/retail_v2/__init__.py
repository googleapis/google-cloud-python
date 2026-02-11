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
import sys

import google.api_core as api_core

from google.cloud.retail_v2 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.analytics_service import (
    AnalyticsServiceAsyncClient,
    AnalyticsServiceClient,
)
from .services.catalog_service import CatalogServiceAsyncClient, CatalogServiceClient
from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.control_service import ControlServiceAsyncClient, ControlServiceClient
from .services.conversational_search_service import (
    ConversationalSearchServiceAsyncClient,
    ConversationalSearchServiceClient,
)
from .services.generative_question_service import (
    GenerativeQuestionServiceAsyncClient,
    GenerativeQuestionServiceClient,
)
from .services.model_service import ModelServiceAsyncClient, ModelServiceClient
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .services.product_service import ProductServiceAsyncClient, ProductServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.serving_config_service import (
    ServingConfigServiceAsyncClient,
    ServingConfigServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.catalog import (
    AttributesConfig,
    Catalog,
    CatalogAttribute,
    CompletionConfig,
    ProductLevelConfig,
)
from .types.catalog_service import (
    AddCatalogAttributeRequest,
    GetAttributesConfigRequest,
    GetCompletionConfigRequest,
    GetDefaultBranchRequest,
    GetDefaultBranchResponse,
    ListCatalogsRequest,
    ListCatalogsResponse,
    RemoveCatalogAttributeRequest,
    ReplaceCatalogAttributeRequest,
    SetDefaultBranchRequest,
    UpdateAttributesConfigRequest,
    UpdateCatalogRequest,
    UpdateCompletionConfigRequest,
)
from .types.common import (
    AttributeConfigLevel,
    Audience,
    ColorInfo,
    Condition,
    CustomAttribute,
    DoubleList,
    FulfillmentInfo,
    Image,
    Interval,
    LocalInventory,
    PinControlMetadata,
    PriceInfo,
    Rating,
    RecommendationsFilteringOption,
    Rule,
    SearchSolutionUseCase,
    SolutionType,
    StringList,
    UserInfo,
)
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.control import Control
from .types.control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from .types.conversational_search_service import (
    ConversationalSearchRequest,
    ConversationalSearchResponse,
)
from .types.export_config import (
    BigQueryOutputResult,
    ExportAnalyticsMetricsRequest,
    ExportAnalyticsMetricsResponse,
    ExportErrorsConfig,
    ExportMetadata,
    GcsOutputResult,
    OutputConfig,
    OutputResult,
)
from .types.generative_question import (
    GenerativeQuestionConfig,
    GenerativeQuestionsFeatureConfig,
)
from .types.generative_question_service import (
    BatchUpdateGenerativeQuestionConfigsRequest,
    BatchUpdateGenerativeQuestionConfigsResponse,
    GetGenerativeQuestionsFeatureConfigRequest,
    ListGenerativeQuestionConfigsRequest,
    ListGenerativeQuestionConfigsResponse,
    UpdateGenerativeQuestionConfigRequest,
    UpdateGenerativeQuestionsFeatureConfigRequest,
)
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
from .types.model import Model
from .types.model_service import (
    CreateModelMetadata,
    CreateModelRequest,
    DeleteModelRequest,
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    PauseModelRequest,
    ResumeModelRequest,
    TuneModelMetadata,
    TuneModelRequest,
    TuneModelResponse,
    UpdateModelRequest,
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
    PurgeProductsMetadata,
    PurgeProductsRequest,
    PurgeProductsResponse,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .types.safety import HarmCategory, SafetySetting
from .types.search_service import (
    ExperimentInfo,
    ProductAttributeInterval,
    ProductAttributeValue,
    SearchRequest,
    SearchResponse,
    Tile,
)
from .types.serving_config import ServingConfig
from .types.serving_config_service import (
    AddControlRequest,
    CreateServingConfigRequest,
    DeleteServingConfigRequest,
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    RemoveControlRequest,
    UpdateServingConfigRequest,
)
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

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.retail_v2")  # type: ignore
    api_core.check_dependency_versions("google.cloud.retail_v2")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.retail_v2"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "AnalyticsServiceAsyncClient",
    "CatalogServiceAsyncClient",
    "CompletionServiceAsyncClient",
    "ControlServiceAsyncClient",
    "ConversationalSearchServiceAsyncClient",
    "GenerativeQuestionServiceAsyncClient",
    "ModelServiceAsyncClient",
    "PredictionServiceAsyncClient",
    "ProductServiceAsyncClient",
    "SearchServiceAsyncClient",
    "ServingConfigServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AddCatalogAttributeRequest",
    "AddControlRequest",
    "AddFulfillmentPlacesMetadata",
    "AddFulfillmentPlacesRequest",
    "AddFulfillmentPlacesResponse",
    "AddLocalInventoriesMetadata",
    "AddLocalInventoriesRequest",
    "AddLocalInventoriesResponse",
    "AnalyticsServiceClient",
    "AttributeConfigLevel",
    "AttributesConfig",
    "Audience",
    "BatchUpdateGenerativeQuestionConfigsRequest",
    "BatchUpdateGenerativeQuestionConfigsResponse",
    "BigQueryOutputResult",
    "BigQuerySource",
    "Catalog",
    "CatalogAttribute",
    "CatalogServiceClient",
    "CollectUserEventRequest",
    "ColorInfo",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionConfig",
    "CompletionDataInputConfig",
    "CompletionDetail",
    "CompletionServiceClient",
    "Condition",
    "Control",
    "ControlServiceClient",
    "ConversationalSearchRequest",
    "ConversationalSearchResponse",
    "ConversationalSearchServiceClient",
    "CreateControlRequest",
    "CreateModelMetadata",
    "CreateModelRequest",
    "CreateProductRequest",
    "CreateServingConfigRequest",
    "CustomAttribute",
    "DeleteControlRequest",
    "DeleteModelRequest",
    "DeleteProductRequest",
    "DeleteServingConfigRequest",
    "DoubleList",
    "ExperimentInfo",
    "ExportAnalyticsMetricsRequest",
    "ExportAnalyticsMetricsResponse",
    "ExportErrorsConfig",
    "ExportMetadata",
    "FulfillmentInfo",
    "GcsOutputResult",
    "GcsSource",
    "GenerativeQuestionConfig",
    "GenerativeQuestionServiceClient",
    "GenerativeQuestionsFeatureConfig",
    "GetAttributesConfigRequest",
    "GetCompletionConfigRequest",
    "GetControlRequest",
    "GetDefaultBranchRequest",
    "GetDefaultBranchResponse",
    "GetGenerativeQuestionsFeatureConfigRequest",
    "GetModelRequest",
    "GetProductRequest",
    "GetServingConfigRequest",
    "HarmCategory",
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
    "ListControlsRequest",
    "ListControlsResponse",
    "ListGenerativeQuestionConfigsRequest",
    "ListGenerativeQuestionConfigsResponse",
    "ListModelsRequest",
    "ListModelsResponse",
    "ListProductsRequest",
    "ListProductsResponse",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "LocalInventory",
    "Model",
    "ModelServiceClient",
    "OutputConfig",
    "OutputResult",
    "PauseModelRequest",
    "PinControlMetadata",
    "PredictRequest",
    "PredictResponse",
    "PredictionServiceClient",
    "PriceInfo",
    "Product",
    "ProductAttributeInterval",
    "ProductAttributeValue",
    "ProductDetail",
    "ProductInlineSource",
    "ProductInputConfig",
    "ProductLevelConfig",
    "ProductServiceClient",
    "Promotion",
    "PurchaseTransaction",
    "PurgeMetadata",
    "PurgeProductsMetadata",
    "PurgeProductsRequest",
    "PurgeProductsResponse",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "Rating",
    "RecommendationsFilteringOption",
    "RejoinUserEventsMetadata",
    "RejoinUserEventsRequest",
    "RejoinUserEventsResponse",
    "RemoveCatalogAttributeRequest",
    "RemoveControlRequest",
    "RemoveFulfillmentPlacesMetadata",
    "RemoveFulfillmentPlacesRequest",
    "RemoveFulfillmentPlacesResponse",
    "RemoveLocalInventoriesMetadata",
    "RemoveLocalInventoriesRequest",
    "RemoveLocalInventoriesResponse",
    "ReplaceCatalogAttributeRequest",
    "ResumeModelRequest",
    "Rule",
    "SafetySetting",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SearchSolutionUseCase",
    "ServingConfig",
    "ServingConfigServiceClient",
    "SetDefaultBranchRequest",
    "SetInventoryMetadata",
    "SetInventoryRequest",
    "SetInventoryResponse",
    "SolutionType",
    "StringList",
    "Tile",
    "TuneModelMetadata",
    "TuneModelRequest",
    "TuneModelResponse",
    "UpdateAttributesConfigRequest",
    "UpdateCatalogRequest",
    "UpdateCompletionConfigRequest",
    "UpdateControlRequest",
    "UpdateGenerativeQuestionConfigRequest",
    "UpdateGenerativeQuestionsFeatureConfigRequest",
    "UpdateModelRequest",
    "UpdateProductRequest",
    "UpdateServingConfigRequest",
    "UserEvent",
    "UserEventImportSummary",
    "UserEventInlineSource",
    "UserEventInputConfig",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
