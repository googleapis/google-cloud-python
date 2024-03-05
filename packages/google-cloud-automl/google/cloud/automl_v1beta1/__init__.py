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
from google.cloud.automl_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


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
