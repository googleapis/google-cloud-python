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

from .services.auto_ml import AutoMlClient
from .services.auto_ml import AutoMlAsyncClient
from .services.prediction_service import PredictionServiceClient
from .services.tables.gcs_client import GcsClient
from .services.tables.tables_client import TablesClient
from .services.prediction_service import PredictionServiceAsyncClient

from .types.annotation_payload import AnnotationPayload
from .types.annotation_spec import AnnotationSpec
from .types.classification import ClassificationAnnotation
from .types.classification import ClassificationEvaluationMetrics
from .types.classification import VideoClassificationAnnotation
from .types.classification import ClassificationType
from .types.column_spec import ColumnSpec
from .types.data_items import Document
from .types.data_items import DocumentDimensions
from .types.data_items import ExamplePayload
from .types.data_items import Image
from .types.data_items import Row
from .types.data_items import TextSnippet
from .types.data_stats import ArrayStats
from .types.data_stats import CategoryStats
from .types.data_stats import CorrelationStats
from .types.data_stats import DataStats
from .types.data_stats import Float64Stats
from .types.data_stats import StringStats
from .types.data_stats import StructStats
from .types.data_stats import TimestampStats
from .types.data_types import DataType
from .types.data_types import StructType
from .types.data_types import TypeCode
from .types.dataset import Dataset
from .types.detection import BoundingBoxMetricsEntry
from .types.detection import ImageObjectDetectionAnnotation
from .types.detection import ImageObjectDetectionEvaluationMetrics
from .types.detection import VideoObjectTrackingAnnotation
from .types.detection import VideoObjectTrackingEvaluationMetrics
from .types.geometry import BoundingPoly
from .types.geometry import NormalizedVertex
from .types.image import ImageClassificationDatasetMetadata
from .types.image import ImageClassificationModelDeploymentMetadata
from .types.image import ImageClassificationModelMetadata
from .types.image import ImageObjectDetectionDatasetMetadata
from .types.image import ImageObjectDetectionModelDeploymentMetadata
from .types.image import ImageObjectDetectionModelMetadata
from .types.io import BatchPredictInputConfig
from .types.io import BatchPredictOutputConfig
from .types.io import BigQueryDestination
from .types.io import BigQuerySource
from .types.io import DocumentInputConfig
from .types.io import ExportEvaluatedExamplesOutputConfig
from .types.io import GcrDestination
from .types.io import GcsDestination
from .types.io import GcsSource
from .types.io import InputConfig
from .types.io import ModelExportOutputConfig
from .types.io import OutputConfig
from .types.model import Model
from .types.model_evaluation import ModelEvaluation
from .types.operations import BatchPredictOperationMetadata
from .types.operations import CreateModelOperationMetadata
from .types.operations import DeleteOperationMetadata
from .types.operations import DeployModelOperationMetadata
from .types.operations import ExportDataOperationMetadata
from .types.operations import ExportEvaluatedExamplesOperationMetadata
from .types.operations import ExportModelOperationMetadata
from .types.operations import ImportDataOperationMetadata
from .types.operations import OperationMetadata
from .types.operations import UndeployModelOperationMetadata
from .types.prediction_service import BatchPredictRequest
from .types.prediction_service import BatchPredictResult
from .types.prediction_service import PredictRequest
from .types.prediction_service import PredictResponse
from .types.ranges import DoubleRange
from .types.regression import RegressionEvaluationMetrics
from .types.service import CreateDatasetRequest
from .types.service import CreateModelRequest
from .types.service import DeleteDatasetRequest
from .types.service import DeleteModelRequest
from .types.service import DeployModelRequest
from .types.service import ExportDataRequest
from .types.service import ExportEvaluatedExamplesRequest
from .types.service import ExportModelRequest
from .types.service import GetAnnotationSpecRequest
from .types.service import GetColumnSpecRequest
from .types.service import GetDatasetRequest
from .types.service import GetModelEvaluationRequest
from .types.service import GetModelRequest
from .types.service import GetTableSpecRequest
from .types.service import ImportDataRequest
from .types.service import ListColumnSpecsRequest
from .types.service import ListColumnSpecsResponse
from .types.service import ListDatasetsRequest
from .types.service import ListDatasetsResponse
from .types.service import ListModelEvaluationsRequest
from .types.service import ListModelEvaluationsResponse
from .types.service import ListModelsRequest
from .types.service import ListModelsResponse
from .types.service import ListTableSpecsRequest
from .types.service import ListTableSpecsResponse
from .types.service import UndeployModelRequest
from .types.service import UpdateColumnSpecRequest
from .types.service import UpdateDatasetRequest
from .types.service import UpdateTableSpecRequest
from .types.table_spec import TableSpec
from .types.tables import TablesAnnotation
from .types.tables import TablesDatasetMetadata
from .types.tables import TablesModelColumnInfo
from .types.tables import TablesModelMetadata
from .types.temporal import TimeSegment
from .types.text import TextClassificationDatasetMetadata
from .types.text import TextClassificationModelMetadata
from .types.text import TextExtractionDatasetMetadata
from .types.text import TextExtractionModelMetadata
from .types.text import TextSentimentDatasetMetadata
from .types.text import TextSentimentModelMetadata
from .types.text_extraction import TextExtractionAnnotation
from .types.text_extraction import TextExtractionEvaluationMetrics
from .types.text_segment import TextSegment
from .types.text_sentiment import TextSentimentAnnotation
from .types.text_sentiment import TextSentimentEvaluationMetrics
from .types.translation import TranslationAnnotation
from .types.translation import TranslationDatasetMetadata
from .types.translation import TranslationEvaluationMetrics
from .types.translation import TranslationModelMetadata
from .types.video import VideoClassificationDatasetMetadata
from .types.video import VideoClassificationModelMetadata
from .types.video import VideoObjectTrackingDatasetMetadata
from .types.video import VideoObjectTrackingModelMetadata

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
