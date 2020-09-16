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

from .temporal import TimeSegment
from .classification import (
    ClassificationAnnotation,
    VideoClassificationAnnotation,
    ClassificationEvaluationMetrics,
)
from .geometry import (
    NormalizedVertex,
    BoundingPoly,
)
from .detection import (
    ImageObjectDetectionAnnotation,
    VideoObjectTrackingAnnotation,
    BoundingBoxMetricsEntry,
    ImageObjectDetectionEvaluationMetrics,
    VideoObjectTrackingEvaluationMetrics,
)
from .data_stats import (
    DataStats,
    Float64Stats,
    StringStats,
    TimestampStats,
    ArrayStats,
    StructStats,
    CategoryStats,
    CorrelationStats,
)
from .data_types import (
    DataType,
    StructType,
)
from .column_spec import ColumnSpec
from .io import (
    InputConfig,
    BatchPredictInputConfig,
    DocumentInputConfig,
    OutputConfig,
    BatchPredictOutputConfig,
    ModelExportOutputConfig,
    ExportEvaluatedExamplesOutputConfig,
    GcsSource,
    BigQuerySource,
    GcsDestination,
    BigQueryDestination,
    GcrDestination,
)
from .text_segment import TextSegment
from .data_items import (
    Image,
    TextSnippet,
    DocumentDimensions,
    Document,
    Row,
    ExamplePayload,
)
from .ranges import DoubleRange
from .regression import RegressionEvaluationMetrics
from .tables import (
    TablesDatasetMetadata,
    TablesModelMetadata,
    TablesAnnotation,
    TablesModelColumnInfo,
)
from .text_extraction import (
    TextExtractionAnnotation,
    TextExtractionEvaluationMetrics,
)
from .text_sentiment import (
    TextSentimentAnnotation,
    TextSentimentEvaluationMetrics,
)
from .translation import (
    TranslationDatasetMetadata,
    TranslationEvaluationMetrics,
    TranslationModelMetadata,
    TranslationAnnotation,
)
from .annotation_payload import AnnotationPayload
from .annotation_spec import AnnotationSpec
from .image import (
    ImageClassificationDatasetMetadata,
    ImageObjectDetectionDatasetMetadata,
    ImageClassificationModelMetadata,
    ImageObjectDetectionModelMetadata,
    ImageClassificationModelDeploymentMetadata,
    ImageObjectDetectionModelDeploymentMetadata,
)
from .text import (
    TextClassificationDatasetMetadata,
    TextClassificationModelMetadata,
    TextExtractionDatasetMetadata,
    TextExtractionModelMetadata,
    TextSentimentDatasetMetadata,
    TextSentimentModelMetadata,
)
from .video import (
    VideoClassificationDatasetMetadata,
    VideoObjectTrackingDatasetMetadata,
    VideoClassificationModelMetadata,
    VideoObjectTrackingModelMetadata,
)
from .dataset import Dataset
from .model import Model
from .model_evaluation import ModelEvaluation
from .operations import (
    OperationMetadata,
    DeleteOperationMetadata,
    DeployModelOperationMetadata,
    UndeployModelOperationMetadata,
    CreateModelOperationMetadata,
    ImportDataOperationMetadata,
    ExportDataOperationMetadata,
    BatchPredictOperationMetadata,
    ExportModelOperationMetadata,
    ExportEvaluatedExamplesOperationMetadata,
)
from .prediction_service import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResult,
)
from .table_spec import TableSpec
from .service import (
    CreateDatasetRequest,
    GetDatasetRequest,
    ListDatasetsRequest,
    ListDatasetsResponse,
    UpdateDatasetRequest,
    DeleteDatasetRequest,
    ImportDataRequest,
    ExportDataRequest,
    GetAnnotationSpecRequest,
    GetTableSpecRequest,
    ListTableSpecsRequest,
    ListTableSpecsResponse,
    UpdateTableSpecRequest,
    GetColumnSpecRequest,
    ListColumnSpecsRequest,
    ListColumnSpecsResponse,
    UpdateColumnSpecRequest,
    CreateModelRequest,
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    DeleteModelRequest,
    DeployModelRequest,
    UndeployModelRequest,
    ExportModelRequest,
    ExportEvaluatedExamplesRequest,
    GetModelEvaluationRequest,
    ListModelEvaluationsRequest,
    ListModelEvaluationsResponse,
)


__all__ = (
    "TimeSegment",
    "ClassificationAnnotation",
    "VideoClassificationAnnotation",
    "ClassificationEvaluationMetrics",
    "NormalizedVertex",
    "BoundingPoly",
    "ImageObjectDetectionAnnotation",
    "VideoObjectTrackingAnnotation",
    "BoundingBoxMetricsEntry",
    "ImageObjectDetectionEvaluationMetrics",
    "VideoObjectTrackingEvaluationMetrics",
    "DataStats",
    "Float64Stats",
    "StringStats",
    "TimestampStats",
    "ArrayStats",
    "StructStats",
    "CategoryStats",
    "CorrelationStats",
    "DataType",
    "StructType",
    "ColumnSpec",
    "InputConfig",
    "BatchPredictInputConfig",
    "DocumentInputConfig",
    "OutputConfig",
    "BatchPredictOutputConfig",
    "ModelExportOutputConfig",
    "ExportEvaluatedExamplesOutputConfig",
    "GcsSource",
    "BigQuerySource",
    "GcsDestination",
    "BigQueryDestination",
    "GcrDestination",
    "TextSegment",
    "Image",
    "TextSnippet",
    "DocumentDimensions",
    "Document",
    "Row",
    "ExamplePayload",
    "DoubleRange",
    "RegressionEvaluationMetrics",
    "TablesDatasetMetadata",
    "TablesModelMetadata",
    "TablesAnnotation",
    "TablesModelColumnInfo",
    "TextExtractionAnnotation",
    "TextExtractionEvaluationMetrics",
    "TextSentimentAnnotation",
    "TextSentimentEvaluationMetrics",
    "TranslationDatasetMetadata",
    "TranslationEvaluationMetrics",
    "TranslationModelMetadata",
    "TranslationAnnotation",
    "AnnotationPayload",
    "AnnotationSpec",
    "ImageClassificationDatasetMetadata",
    "ImageObjectDetectionDatasetMetadata",
    "ImageClassificationModelMetadata",
    "ImageObjectDetectionModelMetadata",
    "ImageClassificationModelDeploymentMetadata",
    "ImageObjectDetectionModelDeploymentMetadata",
    "TextClassificationDatasetMetadata",
    "TextClassificationModelMetadata",
    "TextExtractionDatasetMetadata",
    "TextExtractionModelMetadata",
    "TextSentimentDatasetMetadata",
    "TextSentimentModelMetadata",
    "VideoClassificationDatasetMetadata",
    "VideoObjectTrackingDatasetMetadata",
    "VideoClassificationModelMetadata",
    "VideoObjectTrackingModelMetadata",
    "Dataset",
    "Model",
    "ModelEvaluation",
    "OperationMetadata",
    "DeleteOperationMetadata",
    "DeployModelOperationMetadata",
    "UndeployModelOperationMetadata",
    "CreateModelOperationMetadata",
    "ImportDataOperationMetadata",
    "ExportDataOperationMetadata",
    "BatchPredictOperationMetadata",
    "ExportModelOperationMetadata",
    "ExportEvaluatedExamplesOperationMetadata",
    "PredictRequest",
    "PredictResponse",
    "BatchPredictRequest",
    "BatchPredictResult",
    "TableSpec",
    "CreateDatasetRequest",
    "GetDatasetRequest",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "UpdateDatasetRequest",
    "DeleteDatasetRequest",
    "ImportDataRequest",
    "ExportDataRequest",
    "GetAnnotationSpecRequest",
    "GetTableSpecRequest",
    "ListTableSpecsRequest",
    "ListTableSpecsResponse",
    "UpdateTableSpecRequest",
    "GetColumnSpecRequest",
    "ListColumnSpecsRequest",
    "ListColumnSpecsResponse",
    "UpdateColumnSpecRequest",
    "CreateModelRequest",
    "GetModelRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "DeleteModelRequest",
    "DeployModelRequest",
    "UndeployModelRequest",
    "ExportModelRequest",
    "ExportEvaluatedExamplesRequest",
    "GetModelEvaluationRequest",
    "ListModelEvaluationsRequest",
    "ListModelEvaluationsResponse",
)
