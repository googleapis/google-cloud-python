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

from google.cloud.automl_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.auto_ml import AutoMlAsyncClient, AutoMlClient
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .services.tables.gcs_client import GcsClient
from .services.tables.tables_client import TablesClient
from .types.annotation_payload import AnnotationPayload
from .types.annotation_spec import AnnotationSpec
from .types.classification import (
    ClassificationAnnotation,
    ClassificationEvaluationMetrics,
    ClassificationType,
    VideoClassificationAnnotation,
)
from .types.column_spec import ColumnSpec
from .types.data_items import (
    Document,
    DocumentDimensions,
    ExamplePayload,
    Image,
    Row,
    TextSnippet,
)
from .types.data_stats import (
    ArrayStats,
    CategoryStats,
    CorrelationStats,
    DataStats,
    Float64Stats,
    StringStats,
    StructStats,
    TimestampStats,
)
from .types.data_types import DataType, StructType, TypeCode
from .types.dataset import Dataset
from .types.detection import (
    BoundingBoxMetricsEntry,
    ImageObjectDetectionAnnotation,
    ImageObjectDetectionEvaluationMetrics,
    VideoObjectTrackingAnnotation,
    VideoObjectTrackingEvaluationMetrics,
)
from .types.geometry import BoundingPoly, NormalizedVertex
from .types.image import (
    ImageClassificationDatasetMetadata,
    ImageClassificationModelDeploymentMetadata,
    ImageClassificationModelMetadata,
    ImageObjectDetectionDatasetMetadata,
    ImageObjectDetectionModelDeploymentMetadata,
    ImageObjectDetectionModelMetadata,
)
from .types.io import (
    BatchPredictInputConfig,
    BatchPredictOutputConfig,
    BigQueryDestination,
    BigQuerySource,
    DocumentInputConfig,
    ExportEvaluatedExamplesOutputConfig,
    GcrDestination,
    GcsDestination,
    GcsSource,
    InputConfig,
    ModelExportOutputConfig,
    OutputConfig,
)
from .types.model import Model
from .types.model_evaluation import ModelEvaluation
from .types.operations import (
    BatchPredictOperationMetadata,
    CreateModelOperationMetadata,
    DeleteOperationMetadata,
    DeployModelOperationMetadata,
    ExportDataOperationMetadata,
    ExportEvaluatedExamplesOperationMetadata,
    ExportModelOperationMetadata,
    ImportDataOperationMetadata,
    OperationMetadata,
    UndeployModelOperationMetadata,
)
from .types.prediction_service import (
    BatchPredictRequest,
    BatchPredictResult,
    PredictRequest,
    PredictResponse,
)
from .types.ranges import DoubleRange
from .types.regression import RegressionEvaluationMetrics
from .types.service import (
    CreateDatasetRequest,
    CreateModelRequest,
    DeleteDatasetRequest,
    DeleteModelRequest,
    DeployModelRequest,
    ExportDataRequest,
    ExportEvaluatedExamplesRequest,
    ExportModelRequest,
    GetAnnotationSpecRequest,
    GetColumnSpecRequest,
    GetDatasetRequest,
    GetModelEvaluationRequest,
    GetModelRequest,
    GetTableSpecRequest,
    ImportDataRequest,
    ListColumnSpecsRequest,
    ListColumnSpecsResponse,
    ListDatasetsRequest,
    ListDatasetsResponse,
    ListModelEvaluationsRequest,
    ListModelEvaluationsResponse,
    ListModelsRequest,
    ListModelsResponse,
    ListTableSpecsRequest,
    ListTableSpecsResponse,
    UndeployModelRequest,
    UpdateColumnSpecRequest,
    UpdateDatasetRequest,
    UpdateTableSpecRequest,
)
from .types.table_spec import TableSpec
from .types.tables import (
    TablesAnnotation,
    TablesDatasetMetadata,
    TablesModelColumnInfo,
    TablesModelMetadata,
)
from .types.temporal import TimeSegment
from .types.text import (
    TextClassificationDatasetMetadata,
    TextClassificationModelMetadata,
    TextExtractionDatasetMetadata,
    TextExtractionModelMetadata,
    TextSentimentDatasetMetadata,
    TextSentimentModelMetadata,
)
from .types.text_extraction import (
    TextExtractionAnnotation,
    TextExtractionEvaluationMetrics,
)
from .types.text_segment import TextSegment
from .types.text_sentiment import (
    TextSentimentAnnotation,
    TextSentimentEvaluationMetrics,
)
from .types.translation import (
    TranslationAnnotation,
    TranslationDatasetMetadata,
    TranslationEvaluationMetrics,
    TranslationModelMetadata,
)
from .types.video import (
    VideoClassificationDatasetMetadata,
    VideoClassificationModelMetadata,
    VideoObjectTrackingDatasetMetadata,
    VideoObjectTrackingModelMetadata,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.automl_v1beta1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.automl_v1beta1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.automl_v1beta1"
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
    "GcsClient",
    "TablesClient",
    "AutoMlAsyncClient",
    "PredictionServiceAsyncClient",
    "AnnotationPayload",
    "AnnotationSpec",
    "ArrayStats",
    "AutoMlClient",
    "BatchPredictInputConfig",
    "BatchPredictOperationMetadata",
    "BatchPredictOutputConfig",
    "BatchPredictRequest",
    "BatchPredictResult",
    "BigQueryDestination",
    "BigQuerySource",
    "BoundingBoxMetricsEntry",
    "BoundingPoly",
    "CategoryStats",
    "ClassificationAnnotation",
    "ClassificationEvaluationMetrics",
    "ClassificationType",
    "ColumnSpec",
    "CorrelationStats",
    "CreateDatasetRequest",
    "CreateModelOperationMetadata",
    "CreateModelRequest",
    "DataStats",
    "DataType",
    "Dataset",
    "DeleteDatasetRequest",
    "DeleteModelRequest",
    "DeleteOperationMetadata",
    "DeployModelOperationMetadata",
    "DeployModelRequest",
    "Document",
    "DocumentDimensions",
    "DocumentInputConfig",
    "DoubleRange",
    "ExamplePayload",
    "ExportDataOperationMetadata",
    "ExportDataRequest",
    "ExportEvaluatedExamplesOperationMetadata",
    "ExportEvaluatedExamplesOutputConfig",
    "ExportEvaluatedExamplesRequest",
    "ExportModelOperationMetadata",
    "ExportModelRequest",
    "Float64Stats",
    "GcrDestination",
    "GcsDestination",
    "GcsSource",
    "GetAnnotationSpecRequest",
    "GetColumnSpecRequest",
    "GetDatasetRequest",
    "GetModelEvaluationRequest",
    "GetModelRequest",
    "GetTableSpecRequest",
    "Image",
    "ImageClassificationDatasetMetadata",
    "ImageClassificationModelDeploymentMetadata",
    "ImageClassificationModelMetadata",
    "ImageObjectDetectionAnnotation",
    "ImageObjectDetectionDatasetMetadata",
    "ImageObjectDetectionEvaluationMetrics",
    "ImageObjectDetectionModelDeploymentMetadata",
    "ImageObjectDetectionModelMetadata",
    "ImportDataOperationMetadata",
    "ImportDataRequest",
    "InputConfig",
    "ListColumnSpecsRequest",
    "ListColumnSpecsResponse",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "ListModelEvaluationsRequest",
    "ListModelEvaluationsResponse",
    "ListModelsRequest",
    "ListModelsResponse",
    "ListTableSpecsRequest",
    "ListTableSpecsResponse",
    "Model",
    "ModelEvaluation",
    "ModelExportOutputConfig",
    "NormalizedVertex",
    "OperationMetadata",
    "OutputConfig",
    "PredictRequest",
    "PredictResponse",
    "PredictionServiceClient",
    "RegressionEvaluationMetrics",
    "Row",
    "StringStats",
    "StructStats",
    "StructType",
    "TableSpec",
    "TablesAnnotation",
    "TablesDatasetMetadata",
    "TablesModelColumnInfo",
    "TablesModelMetadata",
    "TextClassificationDatasetMetadata",
    "TextClassificationModelMetadata",
    "TextExtractionAnnotation",
    "TextExtractionDatasetMetadata",
    "TextExtractionEvaluationMetrics",
    "TextExtractionModelMetadata",
    "TextSegment",
    "TextSentimentAnnotation",
    "TextSentimentDatasetMetadata",
    "TextSentimentEvaluationMetrics",
    "TextSentimentModelMetadata",
    "TextSnippet",
    "TimeSegment",
    "TimestampStats",
    "TranslationAnnotation",
    "TranslationDatasetMetadata",
    "TranslationEvaluationMetrics",
    "TranslationModelMetadata",
    "TypeCode",
    "UndeployModelOperationMetadata",
    "UndeployModelRequest",
    "UpdateColumnSpecRequest",
    "UpdateDatasetRequest",
    "UpdateTableSpecRequest",
    "VideoClassificationAnnotation",
    "VideoClassificationDatasetMetadata",
    "VideoClassificationModelMetadata",
    "VideoObjectTrackingAnnotation",
    "VideoObjectTrackingDatasetMetadata",
    "VideoObjectTrackingEvaluationMetrics",
    "VideoObjectTrackingModelMetadata",
)
