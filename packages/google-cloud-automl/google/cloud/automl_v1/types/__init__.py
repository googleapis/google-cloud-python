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

from .classification import (
    ClassificationAnnotation,
    ClassificationEvaluationMetrics,
)
from .geometry import (
    NormalizedVertex,
    BoundingPoly,
)
from .detection import (
    ImageObjectDetectionAnnotation,
    BoundingBoxMetricsEntry,
    ImageObjectDetectionEvaluationMetrics,
)
from .text_segment import TextSegment
from .text_extraction import (
    TextExtractionAnnotation,
    TextExtractionEvaluationMetrics,
)
from .text_sentiment import (
    TextSentimentAnnotation,
    TextSentimentEvaluationMetrics,
)
from .io import (
    InputConfig,
    BatchPredictInputConfig,
    DocumentInputConfig,
    OutputConfig,
    BatchPredictOutputConfig,
    ModelExportOutputConfig,
    GcsSource,
    GcsDestination,
)
from .data_items import (
    Image,
    TextSnippet,
    DocumentDimensions,
    Document,
    ExamplePayload,
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
from .dataset import Dataset
from .model import Model
from .model_evaluation import ModelEvaluation
from .operations import (
    OperationMetadata,
    DeleteOperationMetadata,
    DeployModelOperationMetadata,
    UndeployModelOperationMetadata,
    CreateDatasetOperationMetadata,
    CreateModelOperationMetadata,
    ImportDataOperationMetadata,
    ExportDataOperationMetadata,
    BatchPredictOperationMetadata,
    ExportModelOperationMetadata,
)
from .prediction_service import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResult,
)
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
    CreateModelRequest,
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    DeleteModelRequest,
    UpdateModelRequest,
    DeployModelRequest,
    UndeployModelRequest,
    ExportModelRequest,
    GetModelEvaluationRequest,
    ListModelEvaluationsRequest,
    ListModelEvaluationsResponse,
)


__all__ = (
    "ClassificationAnnotation",
    "ClassificationEvaluationMetrics",
    "NormalizedVertex",
    "BoundingPoly",
    "ImageObjectDetectionAnnotation",
    "BoundingBoxMetricsEntry",
    "ImageObjectDetectionEvaluationMetrics",
    "TextSegment",
    "TextExtractionAnnotation",
    "TextExtractionEvaluationMetrics",
    "TextSentimentAnnotation",
    "TextSentimentEvaluationMetrics",
    "InputConfig",
    "BatchPredictInputConfig",
    "DocumentInputConfig",
    "OutputConfig",
    "BatchPredictOutputConfig",
    "ModelExportOutputConfig",
    "GcsSource",
    "GcsDestination",
    "Image",
    "TextSnippet",
    "DocumentDimensions",
    "Document",
    "ExamplePayload",
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
    "Dataset",
    "Model",
    "ModelEvaluation",
    "OperationMetadata",
    "DeleteOperationMetadata",
    "DeployModelOperationMetadata",
    "UndeployModelOperationMetadata",
    "CreateDatasetOperationMetadata",
    "CreateModelOperationMetadata",
    "ImportDataOperationMetadata",
    "ExportDataOperationMetadata",
    "BatchPredictOperationMetadata",
    "ExportModelOperationMetadata",
    "PredictRequest",
    "PredictResponse",
    "BatchPredictRequest",
    "BatchPredictResult",
    "CreateDatasetRequest",
    "GetDatasetRequest",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "UpdateDatasetRequest",
    "DeleteDatasetRequest",
    "ImportDataRequest",
    "ExportDataRequest",
    "GetAnnotationSpecRequest",
    "CreateModelRequest",
    "GetModelRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "DeleteModelRequest",
    "UpdateModelRequest",
    "DeployModelRequest",
    "UndeployModelRequest",
    "ExportModelRequest",
    "GetModelEvaluationRequest",
    "ListModelEvaluationsRequest",
    "ListModelEvaluationsResponse",
)
