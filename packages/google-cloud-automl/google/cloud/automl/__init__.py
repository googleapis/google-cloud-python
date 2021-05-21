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

from google.cloud.automl_v1.services.auto_ml.client import AutoMlClient
from google.cloud.automl_v1.services.auto_ml.async_client import AutoMlAsyncClient
from google.cloud.automl_v1.services.prediction_service.client import (
    PredictionServiceClient,
)
from google.cloud.automl_v1.services.prediction_service.async_client import (
    PredictionServiceAsyncClient,
)

from google.cloud.automl_v1.types.annotation_payload import AnnotationPayload
from google.cloud.automl_v1.types.annotation_spec import AnnotationSpec
from google.cloud.automl_v1.types.classification import ClassificationAnnotation
from google.cloud.automl_v1.types.classification import ClassificationEvaluationMetrics
from google.cloud.automl_v1.types.classification import ClassificationType
from google.cloud.automl_v1.types.data_items import Document
from google.cloud.automl_v1.types.data_items import DocumentDimensions
from google.cloud.automl_v1.types.data_items import ExamplePayload
from google.cloud.automl_v1.types.data_items import Image
from google.cloud.automl_v1.types.data_items import TextSnippet
from google.cloud.automl_v1.types.dataset import Dataset
from google.cloud.automl_v1.types.detection import BoundingBoxMetricsEntry
from google.cloud.automl_v1.types.detection import ImageObjectDetectionAnnotation
from google.cloud.automl_v1.types.detection import ImageObjectDetectionEvaluationMetrics
from google.cloud.automl_v1.types.geometry import BoundingPoly
from google.cloud.automl_v1.types.geometry import NormalizedVertex
from google.cloud.automl_v1.types.image import ImageClassificationDatasetMetadata
from google.cloud.automl_v1.types.image import (
    ImageClassificationModelDeploymentMetadata,
)
from google.cloud.automl_v1.types.image import ImageClassificationModelMetadata
from google.cloud.automl_v1.types.image import ImageObjectDetectionDatasetMetadata
from google.cloud.automl_v1.types.image import (
    ImageObjectDetectionModelDeploymentMetadata,
)
from google.cloud.automl_v1.types.image import ImageObjectDetectionModelMetadata
from google.cloud.automl_v1.types.io import BatchPredictInputConfig
from google.cloud.automl_v1.types.io import BatchPredictOutputConfig
from google.cloud.automl_v1.types.io import DocumentInputConfig
from google.cloud.automl_v1.types.io import GcsDestination
from google.cloud.automl_v1.types.io import GcsSource
from google.cloud.automl_v1.types.io import InputConfig
from google.cloud.automl_v1.types.io import ModelExportOutputConfig
from google.cloud.automl_v1.types.io import OutputConfig
from google.cloud.automl_v1.types.model import Model
from google.cloud.automl_v1.types.model_evaluation import ModelEvaluation
from google.cloud.automl_v1.types.operations import BatchPredictOperationMetadata
from google.cloud.automl_v1.types.operations import CreateDatasetOperationMetadata
from google.cloud.automl_v1.types.operations import CreateModelOperationMetadata
from google.cloud.automl_v1.types.operations import DeleteOperationMetadata
from google.cloud.automl_v1.types.operations import DeployModelOperationMetadata
from google.cloud.automl_v1.types.operations import ExportDataOperationMetadata
from google.cloud.automl_v1.types.operations import ExportModelOperationMetadata
from google.cloud.automl_v1.types.operations import ImportDataOperationMetadata
from google.cloud.automl_v1.types.operations import OperationMetadata
from google.cloud.automl_v1.types.operations import UndeployModelOperationMetadata
from google.cloud.automl_v1.types.prediction_service import BatchPredictRequest
from google.cloud.automl_v1.types.prediction_service import BatchPredictResult
from google.cloud.automl_v1.types.prediction_service import PredictRequest
from google.cloud.automl_v1.types.prediction_service import PredictResponse
from google.cloud.automl_v1.types.service import CreateDatasetRequest
from google.cloud.automl_v1.types.service import CreateModelRequest
from google.cloud.automl_v1.types.service import DeleteDatasetRequest
from google.cloud.automl_v1.types.service import DeleteModelRequest
from google.cloud.automl_v1.types.service import DeployModelRequest
from google.cloud.automl_v1.types.service import ExportDataRequest
from google.cloud.automl_v1.types.service import ExportModelRequest
from google.cloud.automl_v1.types.service import GetAnnotationSpecRequest
from google.cloud.automl_v1.types.service import GetDatasetRequest
from google.cloud.automl_v1.types.service import GetModelEvaluationRequest
from google.cloud.automl_v1.types.service import GetModelRequest
from google.cloud.automl_v1.types.service import ImportDataRequest
from google.cloud.automl_v1.types.service import ListDatasetsRequest
from google.cloud.automl_v1.types.service import ListDatasetsResponse
from google.cloud.automl_v1.types.service import ListModelEvaluationsRequest
from google.cloud.automl_v1.types.service import ListModelEvaluationsResponse
from google.cloud.automl_v1.types.service import ListModelsRequest
from google.cloud.automl_v1.types.service import ListModelsResponse
from google.cloud.automl_v1.types.service import UndeployModelRequest
from google.cloud.automl_v1.types.service import UpdateDatasetRequest
from google.cloud.automl_v1.types.service import UpdateModelRequest
from google.cloud.automl_v1.types.text import TextClassificationDatasetMetadata
from google.cloud.automl_v1.types.text import TextClassificationModelMetadata
from google.cloud.automl_v1.types.text import TextExtractionDatasetMetadata
from google.cloud.automl_v1.types.text import TextExtractionModelMetadata
from google.cloud.automl_v1.types.text import TextSentimentDatasetMetadata
from google.cloud.automl_v1.types.text import TextSentimentModelMetadata
from google.cloud.automl_v1.types.text_extraction import TextExtractionAnnotation
from google.cloud.automl_v1.types.text_extraction import TextExtractionEvaluationMetrics
from google.cloud.automl_v1.types.text_segment import TextSegment
from google.cloud.automl_v1.types.text_sentiment import TextSentimentAnnotation
from google.cloud.automl_v1.types.text_sentiment import TextSentimentEvaluationMetrics
from google.cloud.automl_v1.types.translation import TranslationAnnotation
from google.cloud.automl_v1.types.translation import TranslationDatasetMetadata
from google.cloud.automl_v1.types.translation import TranslationEvaluationMetrics
from google.cloud.automl_v1.types.translation import TranslationModelMetadata

__all__ = (
    "AutoMlClient",
    "AutoMlAsyncClient",
    "PredictionServiceClient",
    "PredictionServiceAsyncClient",
    "AnnotationPayload",
    "AnnotationSpec",
    "ClassificationAnnotation",
    "ClassificationEvaluationMetrics",
    "ClassificationType",
    "Document",
    "DocumentDimensions",
    "ExamplePayload",
    "Image",
    "TextSnippet",
    "Dataset",
    "BoundingBoxMetricsEntry",
    "ImageObjectDetectionAnnotation",
    "ImageObjectDetectionEvaluationMetrics",
    "BoundingPoly",
    "NormalizedVertex",
    "ImageClassificationDatasetMetadata",
    "ImageClassificationModelDeploymentMetadata",
    "ImageClassificationModelMetadata",
    "ImageObjectDetectionDatasetMetadata",
    "ImageObjectDetectionModelDeploymentMetadata",
    "ImageObjectDetectionModelMetadata",
    "BatchPredictInputConfig",
    "BatchPredictOutputConfig",
    "DocumentInputConfig",
    "GcsDestination",
    "GcsSource",
    "InputConfig",
    "ModelExportOutputConfig",
    "OutputConfig",
    "Model",
    "ModelEvaluation",
    "BatchPredictOperationMetadata",
    "CreateDatasetOperationMetadata",
    "CreateModelOperationMetadata",
    "DeleteOperationMetadata",
    "DeployModelOperationMetadata",
    "ExportDataOperationMetadata",
    "ExportModelOperationMetadata",
    "ImportDataOperationMetadata",
    "OperationMetadata",
    "UndeployModelOperationMetadata",
    "BatchPredictRequest",
    "BatchPredictResult",
    "PredictRequest",
    "PredictResponse",
    "CreateDatasetRequest",
    "CreateModelRequest",
    "DeleteDatasetRequest",
    "DeleteModelRequest",
    "DeployModelRequest",
    "ExportDataRequest",
    "ExportModelRequest",
    "GetAnnotationSpecRequest",
    "GetDatasetRequest",
    "GetModelEvaluationRequest",
    "GetModelRequest",
    "ImportDataRequest",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "ListModelEvaluationsRequest",
    "ListModelEvaluationsResponse",
    "ListModelsRequest",
    "ListModelsResponse",
    "UndeployModelRequest",
    "UpdateDatasetRequest",
    "UpdateModelRequest",
    "TextClassificationDatasetMetadata",
    "TextClassificationModelMetadata",
    "TextExtractionDatasetMetadata",
    "TextExtractionModelMetadata",
    "TextSentimentDatasetMetadata",
    "TextSentimentModelMetadata",
    "TextExtractionAnnotation",
    "TextExtractionEvaluationMetrics",
    "TextSegment",
    "TextSentimentAnnotation",
    "TextSentimentEvaluationMetrics",
    "TranslationAnnotation",
    "TranslationDatasetMetadata",
    "TranslationEvaluationMetrics",
    "TranslationModelMetadata",
)
