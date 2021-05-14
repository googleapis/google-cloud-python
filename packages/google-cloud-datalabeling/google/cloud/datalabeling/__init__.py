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

from google.cloud.datalabeling_v1beta1.services.data_labeling_service.client import (
    DataLabelingServiceClient,
)
from google.cloud.datalabeling_v1beta1.services.data_labeling_service.async_client import (
    DataLabelingServiceAsyncClient,
)

from google.cloud.datalabeling_v1beta1.types.annotation import Annotation
from google.cloud.datalabeling_v1beta1.types.annotation import AnnotationMetadata
from google.cloud.datalabeling_v1beta1.types.annotation import AnnotationValue
from google.cloud.datalabeling_v1beta1.types.annotation import BoundingPoly
from google.cloud.datalabeling_v1beta1.types.annotation import (
    ImageBoundingPolyAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import (
    ImageClassificationAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import ImagePolylineAnnotation
from google.cloud.datalabeling_v1beta1.types.annotation import (
    ImageSegmentationAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import NormalizedBoundingPoly
from google.cloud.datalabeling_v1beta1.types.annotation import NormalizedPolyline
from google.cloud.datalabeling_v1beta1.types.annotation import NormalizedVertex
from google.cloud.datalabeling_v1beta1.types.annotation import ObjectTrackingFrame
from google.cloud.datalabeling_v1beta1.types.annotation import OperatorMetadata
from google.cloud.datalabeling_v1beta1.types.annotation import Polyline
from google.cloud.datalabeling_v1beta1.types.annotation import SequentialSegment
from google.cloud.datalabeling_v1beta1.types.annotation import (
    TextClassificationAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import (
    TextEntityExtractionAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import TimeSegment
from google.cloud.datalabeling_v1beta1.types.annotation import Vertex
from google.cloud.datalabeling_v1beta1.types.annotation import (
    VideoClassificationAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import VideoEventAnnotation
from google.cloud.datalabeling_v1beta1.types.annotation import (
    VideoObjectTrackingAnnotation,
)
from google.cloud.datalabeling_v1beta1.types.annotation import AnnotationSentiment
from google.cloud.datalabeling_v1beta1.types.annotation import AnnotationSource
from google.cloud.datalabeling_v1beta1.types.annotation import AnnotationType
from google.cloud.datalabeling_v1beta1.types.annotation_spec_set import AnnotationSpec
from google.cloud.datalabeling_v1beta1.types.annotation_spec_set import (
    AnnotationSpecSet,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    CreateAnnotationSpecSetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    CreateDatasetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    CreateEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    CreateInstructionRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    DeleteAnnotatedDatasetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    DeleteAnnotationSpecSetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    DeleteDatasetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    DeleteEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    DeleteInstructionRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ExportDataRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetAnnotatedDatasetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetAnnotationSpecSetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetDataItemRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetDatasetRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetEvaluationRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetExampleRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    GetInstructionRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ImportDataRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    LabelImageRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    LabelTextRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    LabelVideoRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListAnnotatedDatasetsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListAnnotatedDatasetsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListAnnotationSpecSetsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListAnnotationSpecSetsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListDataItemsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListDataItemsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListDatasetsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListDatasetsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListEvaluationJobsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListEvaluationJobsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListExamplesRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListExamplesResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListInstructionsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ListInstructionsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    PauseEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    ResumeEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    SearchEvaluationsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    SearchEvaluationsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    SearchExampleComparisonsRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    SearchExampleComparisonsResponse,
)
from google.cloud.datalabeling_v1beta1.types.data_labeling_service import (
    UpdateEvaluationJobRequest,
)
from google.cloud.datalabeling_v1beta1.types.data_payloads import ImagePayload
from google.cloud.datalabeling_v1beta1.types.data_payloads import TextPayload
from google.cloud.datalabeling_v1beta1.types.data_payloads import VideoPayload
from google.cloud.datalabeling_v1beta1.types.data_payloads import VideoThumbnail
from google.cloud.datalabeling_v1beta1.types.dataset import AnnotatedDataset
from google.cloud.datalabeling_v1beta1.types.dataset import AnnotatedDatasetMetadata
from google.cloud.datalabeling_v1beta1.types.dataset import BigQuerySource
from google.cloud.datalabeling_v1beta1.types.dataset import ClassificationMetadata
from google.cloud.datalabeling_v1beta1.types.dataset import DataItem
from google.cloud.datalabeling_v1beta1.types.dataset import Dataset
from google.cloud.datalabeling_v1beta1.types.dataset import Example
from google.cloud.datalabeling_v1beta1.types.dataset import GcsDestination
from google.cloud.datalabeling_v1beta1.types.dataset import GcsFolderDestination
from google.cloud.datalabeling_v1beta1.types.dataset import GcsSource
from google.cloud.datalabeling_v1beta1.types.dataset import InputConfig
from google.cloud.datalabeling_v1beta1.types.dataset import LabelStats
from google.cloud.datalabeling_v1beta1.types.dataset import OutputConfig
from google.cloud.datalabeling_v1beta1.types.dataset import TextMetadata
from google.cloud.datalabeling_v1beta1.types.dataset import DataType
from google.cloud.datalabeling_v1beta1.types.evaluation import (
    BoundingBoxEvaluationOptions,
)
from google.cloud.datalabeling_v1beta1.types.evaluation import ClassificationMetrics
from google.cloud.datalabeling_v1beta1.types.evaluation import ConfusionMatrix
from google.cloud.datalabeling_v1beta1.types.evaluation import Evaluation
from google.cloud.datalabeling_v1beta1.types.evaluation import EvaluationConfig
from google.cloud.datalabeling_v1beta1.types.evaluation import EvaluationMetrics
from google.cloud.datalabeling_v1beta1.types.evaluation import ObjectDetectionMetrics
from google.cloud.datalabeling_v1beta1.types.evaluation import PrCurve
from google.cloud.datalabeling_v1beta1.types.evaluation_job import Attempt
from google.cloud.datalabeling_v1beta1.types.evaluation_job import EvaluationJob
from google.cloud.datalabeling_v1beta1.types.evaluation_job import (
    EvaluationJobAlertConfig,
)
from google.cloud.datalabeling_v1beta1.types.evaluation_job import EvaluationJobConfig
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    BoundingPolyConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import EventConfig
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    HumanAnnotationConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    ImageClassificationConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    ObjectDetectionConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    ObjectTrackingConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    PolylineConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    SegmentationConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    SentimentConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    TextClassificationConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    TextEntityExtractionConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    VideoClassificationConfig,
)
from google.cloud.datalabeling_v1beta1.types.human_annotation_config import (
    StringAggregationType,
)
from google.cloud.datalabeling_v1beta1.types.instruction import CsvInstruction
from google.cloud.datalabeling_v1beta1.types.instruction import Instruction
from google.cloud.datalabeling_v1beta1.types.instruction import PdfInstruction
from google.cloud.datalabeling_v1beta1.types.operations import CreateInstructionMetadata
from google.cloud.datalabeling_v1beta1.types.operations import (
    ExportDataOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    ExportDataOperationResponse,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    ImportDataOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    ImportDataOperationResponse,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImageBoundingBoxOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImageBoundingPolyOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImageClassificationOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImageOrientedBoundingBoxOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImagePolylineOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelImageSegmentationOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import LabelOperationMetadata
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelTextClassificationOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelTextEntityExtractionOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelVideoClassificationOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelVideoEventOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelVideoObjectDetectionOperationMetadata,
)
from google.cloud.datalabeling_v1beta1.types.operations import (
    LabelVideoObjectTrackingOperationMetadata,
)

__all__ = (
    "DataLabelingServiceClient",
    "DataLabelingServiceAsyncClient",
    "Annotation",
    "AnnotationMetadata",
    "AnnotationValue",
    "BoundingPoly",
    "ImageBoundingPolyAnnotation",
    "ImageClassificationAnnotation",
    "ImagePolylineAnnotation",
    "ImageSegmentationAnnotation",
    "NormalizedBoundingPoly",
    "NormalizedPolyline",
    "NormalizedVertex",
    "ObjectTrackingFrame",
    "OperatorMetadata",
    "Polyline",
    "SequentialSegment",
    "TextClassificationAnnotation",
    "TextEntityExtractionAnnotation",
    "TimeSegment",
    "Vertex",
    "VideoClassificationAnnotation",
    "VideoEventAnnotation",
    "VideoObjectTrackingAnnotation",
    "AnnotationSentiment",
    "AnnotationSource",
    "AnnotationType",
    "AnnotationSpec",
    "AnnotationSpecSet",
    "CreateAnnotationSpecSetRequest",
    "CreateDatasetRequest",
    "CreateEvaluationJobRequest",
    "CreateInstructionRequest",
    "DeleteAnnotatedDatasetRequest",
    "DeleteAnnotationSpecSetRequest",
    "DeleteDatasetRequest",
    "DeleteEvaluationJobRequest",
    "DeleteInstructionRequest",
    "ExportDataRequest",
    "GetAnnotatedDatasetRequest",
    "GetAnnotationSpecSetRequest",
    "GetDataItemRequest",
    "GetDatasetRequest",
    "GetEvaluationJobRequest",
    "GetEvaluationRequest",
    "GetExampleRequest",
    "GetInstructionRequest",
    "ImportDataRequest",
    "LabelImageRequest",
    "LabelTextRequest",
    "LabelVideoRequest",
    "ListAnnotatedDatasetsRequest",
    "ListAnnotatedDatasetsResponse",
    "ListAnnotationSpecSetsRequest",
    "ListAnnotationSpecSetsResponse",
    "ListDataItemsRequest",
    "ListDataItemsResponse",
    "ListDatasetsRequest",
    "ListDatasetsResponse",
    "ListEvaluationJobsRequest",
    "ListEvaluationJobsResponse",
    "ListExamplesRequest",
    "ListExamplesResponse",
    "ListInstructionsRequest",
    "ListInstructionsResponse",
    "PauseEvaluationJobRequest",
    "ResumeEvaluationJobRequest",
    "SearchEvaluationsRequest",
    "SearchEvaluationsResponse",
    "SearchExampleComparisonsRequest",
    "SearchExampleComparisonsResponse",
    "UpdateEvaluationJobRequest",
    "ImagePayload",
    "TextPayload",
    "VideoPayload",
    "VideoThumbnail",
    "AnnotatedDataset",
    "AnnotatedDatasetMetadata",
    "BigQuerySource",
    "ClassificationMetadata",
    "DataItem",
    "Dataset",
    "Example",
    "GcsDestination",
    "GcsFolderDestination",
    "GcsSource",
    "InputConfig",
    "LabelStats",
    "OutputConfig",
    "TextMetadata",
    "DataType",
    "BoundingBoxEvaluationOptions",
    "ClassificationMetrics",
    "ConfusionMatrix",
    "Evaluation",
    "EvaluationConfig",
    "EvaluationMetrics",
    "ObjectDetectionMetrics",
    "PrCurve",
    "Attempt",
    "EvaluationJob",
    "EvaluationJobAlertConfig",
    "EvaluationJobConfig",
    "BoundingPolyConfig",
    "EventConfig",
    "HumanAnnotationConfig",
    "ImageClassificationConfig",
    "ObjectDetectionConfig",
    "ObjectTrackingConfig",
    "PolylineConfig",
    "SegmentationConfig",
    "SentimentConfig",
    "TextClassificationConfig",
    "TextEntityExtractionConfig",
    "VideoClassificationConfig",
    "StringAggregationType",
    "CsvInstruction",
    "Instruction",
    "PdfInstruction",
    "CreateInstructionMetadata",
    "ExportDataOperationMetadata",
    "ExportDataOperationResponse",
    "ImportDataOperationMetadata",
    "ImportDataOperationResponse",
    "LabelImageBoundingBoxOperationMetadata",
    "LabelImageBoundingPolyOperationMetadata",
    "LabelImageClassificationOperationMetadata",
    "LabelImageOrientedBoundingBoxOperationMetadata",
    "LabelImagePolylineOperationMetadata",
    "LabelImageSegmentationOperationMetadata",
    "LabelOperationMetadata",
    "LabelTextClassificationOperationMetadata",
    "LabelTextEntityExtractionOperationMetadata",
    "LabelVideoClassificationOperationMetadata",
    "LabelVideoEventOperationMetadata",
    "LabelVideoObjectDetectionOperationMetadata",
    "LabelVideoObjectTrackingOperationMetadata",
)
