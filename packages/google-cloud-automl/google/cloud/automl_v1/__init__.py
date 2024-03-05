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
from google.cloud.automl_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.auto_ml import AutoMlAsyncClient, AutoMlClient
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .types.annotation_payload import AnnotationPayload
from .types.annotation_spec import AnnotationSpec
from .types.classification import (
    ClassificationAnnotation,
    ClassificationEvaluationMetrics,
    ClassificationType,
)
from .types.data_items import (
    Document,
    DocumentDimensions,
    ExamplePayload,
    Image,
    TextSnippet,
)
from .types.dataset import Dataset
from .types.detection import (
    BoundingBoxMetricsEntry,
    ImageObjectDetectionAnnotation,
    ImageObjectDetectionEvaluationMetrics,
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
    DocumentInputConfig,
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
    CreateDatasetOperationMetadata,
    CreateModelOperationMetadata,
    DeleteOperationMetadata,
    DeployModelOperationMetadata,
    ExportDataOperationMetadata,
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
from .types.service import (
    CreateDatasetRequest,
    CreateModelRequest,
    DeleteDatasetRequest,
    DeleteModelRequest,
    DeployModelRequest,
    ExportDataRequest,
    ExportModelRequest,
    GetAnnotationSpecRequest,
    GetDatasetRequest,
    GetModelEvaluationRequest,
    GetModelRequest,
    ImportDataRequest,
    ListDatasetsRequest,
    ListDatasetsResponse,
    ListModelEvaluationsRequest,
    ListModelEvaluationsResponse,
    ListModelsRequest,
    ListModelsResponse,
    UndeployModelRequest,
    UpdateDatasetRequest,
    UpdateModelRequest,
)
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

__all__ = (
    "AutoMlAsyncClient",
    "PredictionServiceAsyncClient",
    "AnnotationPayload",
    "AnnotationSpec",
    "AutoMlClient",
    "BatchPredictInputConfig",
    "BatchPredictOperationMetadata",
    "BatchPredictOutputConfig",
    "BatchPredictRequest",
    "BatchPredictResult",
    "BoundingBoxMetricsEntry",
    "BoundingPoly",
    "ClassificationAnnotation",
    "ClassificationEvaluationMetrics",
    "ClassificationType",
    "CreateDatasetOperationMetadata",
    "CreateDatasetRequest",
    "CreateModelOperationMetadata",
    "CreateModelRequest",
    "Dataset",
    "DeleteDatasetRequest",
    "DeleteModelRequest",
    "DeleteOperationMetadata",
    "DeployModelOperationMetadata",
    "DeployModelRequest",
    "Document",
    "DocumentDimensions",
    "DocumentInputConfig",
    "ExamplePayload",
    "ExportDataOperationMetadata",
    "ExportDataRequest",
    "ExportModelOperationMetadata",
    "ExportModelRequest",
    "GcsDestination",
    "GcsSource",
    "GetAnnotationSpecRequest",
    "GetDatasetRequest",
    "GetModelEvaluationRequest",
    "GetModelRequest",
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
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "ListModelEvaluationsRequest",
    "ListModelEvaluationsResponse",
    "ListModelsRequest",
    "ListModelsResponse",
    "Model",
    "ModelEvaluation",
    "ModelExportOutputConfig",
    "NormalizedVertex",
    "OperationMetadata",
    "OutputConfig",
    "PredictRequest",
    "PredictResponse",
    "PredictionServiceClient",
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
    "TranslationAnnotation",
    "TranslationDatasetMetadata",
    "TranslationEvaluationMetrics",
    "TranslationModelMetadata",
    "UndeployModelOperationMetadata",
    "UndeployModelRequest",
    "UpdateDatasetRequest",
    "UpdateModelRequest",
)
