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

from google.cloud.datalabeling_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.data_labeling_service import (
    DataLabelingServiceAsyncClient,
    DataLabelingServiceClient,
)
from .types.annotation import (
    Annotation,
    AnnotationMetadata,
    AnnotationSentiment,
    AnnotationSource,
    AnnotationType,
    AnnotationValue,
    BoundingPoly,
    ImageBoundingPolyAnnotation,
    ImageClassificationAnnotation,
    ImagePolylineAnnotation,
    ImageSegmentationAnnotation,
    NormalizedBoundingPoly,
    NormalizedPolyline,
    NormalizedVertex,
    ObjectTrackingFrame,
    OperatorMetadata,
    Polyline,
    SequentialSegment,
    TextClassificationAnnotation,
    TextEntityExtractionAnnotation,
    TimeSegment,
    Vertex,
    VideoClassificationAnnotation,
    VideoEventAnnotation,
    VideoObjectTrackingAnnotation,
)
from .types.annotation_spec_set import AnnotationSpec, AnnotationSpecSet
from .types.data_labeling_service import (
    CreateAnnotationSpecSetRequest,
    CreateDatasetRequest,
    CreateEvaluationJobRequest,
    CreateInstructionRequest,
    DeleteAnnotatedDatasetRequest,
    DeleteAnnotationSpecSetRequest,
    DeleteDatasetRequest,
    DeleteEvaluationJobRequest,
    DeleteInstructionRequest,
    ExportDataRequest,
    GetAnnotatedDatasetRequest,
    GetAnnotationSpecSetRequest,
    GetDataItemRequest,
    GetDatasetRequest,
    GetEvaluationJobRequest,
    GetEvaluationRequest,
    GetExampleRequest,
    GetInstructionRequest,
    ImportDataRequest,
    LabelImageRequest,
    LabelTextRequest,
    LabelVideoRequest,
    ListAnnotatedDatasetsRequest,
    ListAnnotatedDatasetsResponse,
    ListAnnotationSpecSetsRequest,
    ListAnnotationSpecSetsResponse,
    ListDataItemsRequest,
    ListDataItemsResponse,
    ListDatasetsRequest,
    ListDatasetsResponse,
    ListEvaluationJobsRequest,
    ListEvaluationJobsResponse,
    ListExamplesRequest,
    ListExamplesResponse,
    ListInstructionsRequest,
    ListInstructionsResponse,
    PauseEvaluationJobRequest,
    ResumeEvaluationJobRequest,
    SearchEvaluationsRequest,
    SearchEvaluationsResponse,
    SearchExampleComparisonsRequest,
    SearchExampleComparisonsResponse,
    UpdateEvaluationJobRequest,
)
from .types.data_payloads import ImagePayload, TextPayload, VideoPayload, VideoThumbnail
from .types.dataset import (
    AnnotatedDataset,
    AnnotatedDatasetMetadata,
    BigQuerySource,
    ClassificationMetadata,
    DataItem,
    Dataset,
    DataType,
    Example,
    GcsDestination,
    GcsFolderDestination,
    GcsSource,
    InputConfig,
    LabelStats,
    OutputConfig,
    TextMetadata,
)
from .types.evaluation import (
    BoundingBoxEvaluationOptions,
    ClassificationMetrics,
    ConfusionMatrix,
    Evaluation,
    EvaluationConfig,
    EvaluationMetrics,
    ObjectDetectionMetrics,
    PrCurve,
)
from .types.evaluation_job import (
    Attempt,
    EvaluationJob,
    EvaluationJobAlertConfig,
    EvaluationJobConfig,
)
from .types.human_annotation_config import (
    BoundingPolyConfig,
    EventConfig,
    HumanAnnotationConfig,
    ImageClassificationConfig,
    ObjectDetectionConfig,
    ObjectTrackingConfig,
    PolylineConfig,
    SegmentationConfig,
    SentimentConfig,
    StringAggregationType,
    TextClassificationConfig,
    TextEntityExtractionConfig,
    VideoClassificationConfig,
)
from .types.instruction import CsvInstruction, Instruction, PdfInstruction
from .types.operations import (
    CreateInstructionMetadata,
    ExportDataOperationMetadata,
    ExportDataOperationResponse,
    ImportDataOperationMetadata,
    ImportDataOperationResponse,
    LabelImageBoundingBoxOperationMetadata,
    LabelImageBoundingPolyOperationMetadata,
    LabelImageClassificationOperationMetadata,
    LabelImageOrientedBoundingBoxOperationMetadata,
    LabelImagePolylineOperationMetadata,
    LabelImageSegmentationOperationMetadata,
    LabelOperationMetadata,
    LabelTextClassificationOperationMetadata,
    LabelTextEntityExtractionOperationMetadata,
    LabelVideoClassificationOperationMetadata,
    LabelVideoEventOperationMetadata,
    LabelVideoObjectDetectionOperationMetadata,
    LabelVideoObjectTrackingOperationMetadata,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.datalabeling_v1beta1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.datalabeling_v1beta1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.datalabeling_v1beta1"
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
