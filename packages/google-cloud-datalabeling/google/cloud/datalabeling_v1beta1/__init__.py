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

from .services.data_labeling_service import DataLabelingServiceClient
from .services.data_labeling_service import DataLabelingServiceAsyncClient

from .types.annotation import Annotation
from .types.annotation import AnnotationMetadata
from .types.annotation import AnnotationValue
from .types.annotation import BoundingPoly
from .types.annotation import ImageBoundingPolyAnnotation
from .types.annotation import ImageClassificationAnnotation
from .types.annotation import ImagePolylineAnnotation
from .types.annotation import ImageSegmentationAnnotation
from .types.annotation import NormalizedBoundingPoly
from .types.annotation import NormalizedPolyline
from .types.annotation import NormalizedVertex
from .types.annotation import ObjectTrackingFrame
from .types.annotation import OperatorMetadata
from .types.annotation import Polyline
from .types.annotation import SequentialSegment
from .types.annotation import TextClassificationAnnotation
from .types.annotation import TextEntityExtractionAnnotation
from .types.annotation import TimeSegment
from .types.annotation import Vertex
from .types.annotation import VideoClassificationAnnotation
from .types.annotation import VideoEventAnnotation
from .types.annotation import VideoObjectTrackingAnnotation
from .types.annotation import AnnotationSentiment
from .types.annotation import AnnotationSource
from .types.annotation import AnnotationType
from .types.annotation_spec_set import AnnotationSpec
from .types.annotation_spec_set import AnnotationSpecSet
from .types.data_labeling_service import CreateAnnotationSpecSetRequest
from .types.data_labeling_service import CreateDatasetRequest
from .types.data_labeling_service import CreateEvaluationJobRequest
from .types.data_labeling_service import CreateInstructionRequest
from .types.data_labeling_service import DeleteAnnotatedDatasetRequest
from .types.data_labeling_service import DeleteAnnotationSpecSetRequest
from .types.data_labeling_service import DeleteDatasetRequest
from .types.data_labeling_service import DeleteEvaluationJobRequest
from .types.data_labeling_service import DeleteInstructionRequest
from .types.data_labeling_service import ExportDataRequest
from .types.data_labeling_service import GetAnnotatedDatasetRequest
from .types.data_labeling_service import GetAnnotationSpecSetRequest
from .types.data_labeling_service import GetDataItemRequest
from .types.data_labeling_service import GetDatasetRequest
from .types.data_labeling_service import GetEvaluationJobRequest
from .types.data_labeling_service import GetEvaluationRequest
from .types.data_labeling_service import GetExampleRequest
from .types.data_labeling_service import GetInstructionRequest
from .types.data_labeling_service import ImportDataRequest
from .types.data_labeling_service import LabelImageRequest
from .types.data_labeling_service import LabelTextRequest
from .types.data_labeling_service import LabelVideoRequest
from .types.data_labeling_service import ListAnnotatedDatasetsRequest
from .types.data_labeling_service import ListAnnotatedDatasetsResponse
from .types.data_labeling_service import ListAnnotationSpecSetsRequest
from .types.data_labeling_service import ListAnnotationSpecSetsResponse
from .types.data_labeling_service import ListDataItemsRequest
from .types.data_labeling_service import ListDataItemsResponse
from .types.data_labeling_service import ListDatasetsRequest
from .types.data_labeling_service import ListDatasetsResponse
from .types.data_labeling_service import ListEvaluationJobsRequest
from .types.data_labeling_service import ListEvaluationJobsResponse
from .types.data_labeling_service import ListExamplesRequest
from .types.data_labeling_service import ListExamplesResponse
from .types.data_labeling_service import ListInstructionsRequest
from .types.data_labeling_service import ListInstructionsResponse
from .types.data_labeling_service import PauseEvaluationJobRequest
from .types.data_labeling_service import ResumeEvaluationJobRequest
from .types.data_labeling_service import SearchEvaluationsRequest
from .types.data_labeling_service import SearchEvaluationsResponse
from .types.data_labeling_service import SearchExampleComparisonsRequest
from .types.data_labeling_service import SearchExampleComparisonsResponse
from .types.data_labeling_service import UpdateEvaluationJobRequest
from .types.data_payloads import ImagePayload
from .types.data_payloads import TextPayload
from .types.data_payloads import VideoPayload
from .types.data_payloads import VideoThumbnail
from .types.dataset import AnnotatedDataset
from .types.dataset import AnnotatedDatasetMetadata
from .types.dataset import BigQuerySource
from .types.dataset import ClassificationMetadata
from .types.dataset import DataItem
from .types.dataset import Dataset
from .types.dataset import Example
from .types.dataset import GcsDestination
from .types.dataset import GcsFolderDestination
from .types.dataset import GcsSource
from .types.dataset import InputConfig
from .types.dataset import LabelStats
from .types.dataset import OutputConfig
from .types.dataset import TextMetadata
from .types.dataset import DataType
from .types.evaluation import BoundingBoxEvaluationOptions
from .types.evaluation import ClassificationMetrics
from .types.evaluation import ConfusionMatrix
from .types.evaluation import Evaluation
from .types.evaluation import EvaluationConfig
from .types.evaluation import EvaluationMetrics
from .types.evaluation import ObjectDetectionMetrics
from .types.evaluation import PrCurve
from .types.evaluation_job import Attempt
from .types.evaluation_job import EvaluationJob
from .types.evaluation_job import EvaluationJobAlertConfig
from .types.evaluation_job import EvaluationJobConfig
from .types.human_annotation_config import BoundingPolyConfig
from .types.human_annotation_config import EventConfig
from .types.human_annotation_config import HumanAnnotationConfig
from .types.human_annotation_config import ImageClassificationConfig
from .types.human_annotation_config import ObjectDetectionConfig
from .types.human_annotation_config import ObjectTrackingConfig
from .types.human_annotation_config import PolylineConfig
from .types.human_annotation_config import SegmentationConfig
from .types.human_annotation_config import SentimentConfig
from .types.human_annotation_config import TextClassificationConfig
from .types.human_annotation_config import TextEntityExtractionConfig
from .types.human_annotation_config import VideoClassificationConfig
from .types.human_annotation_config import StringAggregationType
from .types.instruction import CsvInstruction
from .types.instruction import Instruction
from .types.instruction import PdfInstruction
from .types.operations import CreateInstructionMetadata
from .types.operations import ExportDataOperationMetadata
from .types.operations import ExportDataOperationResponse
from .types.operations import ImportDataOperationMetadata
from .types.operations import ImportDataOperationResponse
from .types.operations import LabelImageBoundingBoxOperationMetadata
from .types.operations import LabelImageBoundingPolyOperationMetadata
from .types.operations import LabelImageClassificationOperationMetadata
from .types.operations import LabelImageOrientedBoundingBoxOperationMetadata
from .types.operations import LabelImagePolylineOperationMetadata
from .types.operations import LabelImageSegmentationOperationMetadata
from .types.operations import LabelOperationMetadata
from .types.operations import LabelTextClassificationOperationMetadata
from .types.operations import LabelTextEntityExtractionOperationMetadata
from .types.operations import LabelVideoClassificationOperationMetadata
from .types.operations import LabelVideoEventOperationMetadata
from .types.operations import LabelVideoObjectDetectionOperationMetadata
from .types.operations import LabelVideoObjectTrackingOperationMetadata

__all__ = (
    "DataLabelingServiceAsyncClient",
    "AnnotatedDataset",
    "AnnotatedDatasetMetadata",
    "Annotation",
    "AnnotationMetadata",
    "AnnotationSentiment",
    "AnnotationSource",
    "AnnotationSpec",
    "AnnotationSpecSet",
    "AnnotationType",
    "AnnotationValue",
    "Attempt",
    "BigQuerySource",
    "BoundingBoxEvaluationOptions",
    "BoundingPoly",
    "BoundingPolyConfig",
    "ClassificationMetadata",
    "ClassificationMetrics",
    "ConfusionMatrix",
    "CreateAnnotationSpecSetRequest",
    "CreateDatasetRequest",
    "CreateEvaluationJobRequest",
    "CreateInstructionMetadata",
    "CreateInstructionRequest",
    "CsvInstruction",
    "DataItem",
    "DataLabelingServiceClient",
    "DataType",
    "Dataset",
    "DeleteAnnotatedDatasetRequest",
    "DeleteAnnotationSpecSetRequest",
    "DeleteDatasetRequest",
    "DeleteEvaluationJobRequest",
    "DeleteInstructionRequest",
    "Evaluation",
    "EvaluationConfig",
    "EvaluationJob",
    "EvaluationJobAlertConfig",
    "EvaluationJobConfig",
    "EvaluationMetrics",
    "EventConfig",
    "Example",
    "ExportDataOperationMetadata",
    "ExportDataOperationResponse",
    "ExportDataRequest",
    "GcsDestination",
    "GcsFolderDestination",
    "GcsSource",
    "GetAnnotatedDatasetRequest",
    "GetAnnotationSpecSetRequest",
    "GetDataItemRequest",
    "GetDatasetRequest",
    "GetEvaluationJobRequest",
    "GetEvaluationRequest",
    "GetExampleRequest",
    "GetInstructionRequest",
    "HumanAnnotationConfig",
    "ImageBoundingPolyAnnotation",
    "ImageClassificationAnnotation",
    "ImageClassificationConfig",
    "ImagePayload",
    "ImagePolylineAnnotation",
    "ImageSegmentationAnnotation",
    "ImportDataOperationMetadata",
    "ImportDataOperationResponse",
    "ImportDataRequest",
    "InputConfig",
    "Instruction",
    "LabelImageBoundingBoxOperationMetadata",
    "LabelImageBoundingPolyOperationMetadata",
    "LabelImageClassificationOperationMetadata",
    "LabelImageOrientedBoundingBoxOperationMetadata",
    "LabelImagePolylineOperationMetadata",
    "LabelImageRequest",
    "LabelImageSegmentationOperationMetadata",
    "LabelOperationMetadata",
    "LabelStats",
    "LabelTextClassificationOperationMetadata",
    "LabelTextEntityExtractionOperationMetadata",
    "LabelTextRequest",
    "LabelVideoClassificationOperationMetadata",
    "LabelVideoEventOperationMetadata",
    "LabelVideoObjectDetectionOperationMetadata",
    "LabelVideoObjectTrackingOperationMetadata",
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
    "NormalizedBoundingPoly",
    "NormalizedPolyline",
    "NormalizedVertex",
    "ObjectDetectionConfig",
    "ObjectDetectionMetrics",
    "ObjectTrackingConfig",
    "ObjectTrackingFrame",
    "OperatorMetadata",
    "OutputConfig",
    "PauseEvaluationJobRequest",
    "PdfInstruction",
    "Polyline",
    "PolylineConfig",
    "PrCurve",
    "ResumeEvaluationJobRequest",
    "SearchEvaluationsRequest",
    "SearchEvaluationsResponse",
    "SearchExampleComparisonsRequest",
    "SearchExampleComparisonsResponse",
    "SegmentationConfig",
    "SentimentConfig",
    "SequentialSegment",
    "StringAggregationType",
    "TextClassificationAnnotation",
    "TextClassificationConfig",
    "TextEntityExtractionAnnotation",
    "TextEntityExtractionConfig",
    "TextMetadata",
    "TextPayload",
    "TimeSegment",
    "UpdateEvaluationJobRequest",
    "Vertex",
    "VideoClassificationAnnotation",
    "VideoClassificationConfig",
    "VideoEventAnnotation",
    "VideoObjectTrackingAnnotation",
    "VideoPayload",
    "VideoThumbnail",
)
