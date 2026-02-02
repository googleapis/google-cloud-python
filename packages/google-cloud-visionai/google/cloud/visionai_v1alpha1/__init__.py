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

from google.cloud.visionai_v1alpha1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.app_platform import AppPlatformAsyncClient, AppPlatformClient
from .services.live_video_analytics import (
    LiveVideoAnalyticsAsyncClient,
    LiveVideoAnalyticsClient,
)
from .services.streaming_service import (
    StreamingServiceAsyncClient,
    StreamingServiceClient,
)
from .services.streams_service import StreamsServiceAsyncClient, StreamsServiceClient
from .services.warehouse import WarehouseAsyncClient, WarehouseClient
from .types.annotations import (
    AppPlatformCloudFunctionRequest,
    AppPlatformCloudFunctionResponse,
    AppPlatformEventBody,
    AppPlatformMetadata,
    ClassificationPredictionResult,
    ImageObjectDetectionPredictionResult,
    ImageSegmentationPredictionResult,
    NormalizedPolygon,
    NormalizedPolyline,
    NormalizedVertex,
    ObjectDetectionPredictionResult,
    OccupancyCountingPredictionResult,
    PersonalProtectiveEquipmentDetectionOutput,
    StreamAnnotation,
    StreamAnnotations,
    StreamAnnotationType,
    VideoActionRecognitionPredictionResult,
    VideoClassificationPredictionResult,
    VideoObjectTrackingPredictionResult,
)
from .types.common import Cluster, GcsSource, OperationMetadata
from .types.lva import AnalysisDefinition, AnalyzerDefinition, AttributeValue
from .types.lva_resources import Analysis
from .types.lva_service import (
    CreateAnalysisRequest,
    DeleteAnalysisRequest,
    GetAnalysisRequest,
    ListAnalysesRequest,
    ListAnalysesResponse,
    UpdateAnalysisRequest,
)
from .types.platform import (
    AcceleratorType,
    AddApplicationStreamInputRequest,
    AddApplicationStreamInputResponse,
    AIEnabledDevicesInputConfig,
    Application,
    ApplicationConfigs,
    ApplicationInstance,
    ApplicationNodeAnnotation,
    ApplicationStreamInput,
    AutoscalingMetricSpec,
    BigQueryConfig,
    CreateApplicationInstancesRequest,
    CreateApplicationInstancesResponse,
    CreateApplicationRequest,
    CreateDraftRequest,
    CreateProcessorRequest,
    CustomProcessorSourceInfo,
    DedicatedResources,
    DeleteApplicationInstancesRequest,
    DeleteApplicationInstancesResponse,
    DeleteApplicationRequest,
    DeleteDraftRequest,
    DeleteProcessorRequest,
    DeployApplicationRequest,
    DeployApplicationResponse,
    Draft,
    GeneralObjectDetectionConfig,
    GetApplicationRequest,
    GetDraftRequest,
    GetInstanceRequest,
    GetProcessorRequest,
    Instance,
    ListApplicationsRequest,
    ListApplicationsResponse,
    ListDraftsRequest,
    ListDraftsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListPrebuiltProcessorsRequest,
    ListPrebuiltProcessorsResponse,
    ListProcessorsRequest,
    ListProcessorsResponse,
    MachineSpec,
    MediaWarehouseConfig,
    ModelType,
    Node,
    OccupancyCountConfig,
    PersonalProtectiveEquipmentDetectionConfig,
    PersonBlurConfig,
    PersonVehicleDetectionConfig,
    Processor,
    ProcessorConfig,
    ProcessorIOSpec,
    RemoveApplicationStreamInputRequest,
    RemoveApplicationStreamInputResponse,
    ResourceAnnotations,
    StreamWithAnnotation,
    UndeployApplicationRequest,
    UndeployApplicationResponse,
    UpdateApplicationInstancesRequest,
    UpdateApplicationInstancesResponse,
    UpdateApplicationRequest,
    UpdateApplicationStreamInputRequest,
    UpdateApplicationStreamInputResponse,
    UpdateDraftRequest,
    UpdateProcessorRequest,
    VertexAutoMLVideoConfig,
    VertexAutoMLVisionConfig,
    VertexCustomConfig,
    VideoStreamInputConfig,
)
from .types.streaming_resources import (
    GstreamerBufferDescriptor,
    Packet,
    PacketHeader,
    PacketType,
    RawImageDescriptor,
    SeriesMetadata,
    ServerMetadata,
)
from .types.streaming_service import (
    AcquireLeaseRequest,
    CommitRequest,
    ControlledMode,
    EagerMode,
    EventUpdate,
    Lease,
    LeaseType,
    ReceiveEventsControlResponse,
    ReceiveEventsRequest,
    ReceiveEventsResponse,
    ReceivePacketsControlResponse,
    ReceivePacketsRequest,
    ReceivePacketsResponse,
    ReleaseLeaseRequest,
    ReleaseLeaseResponse,
    RenewLeaseRequest,
    RequestMetadata,
    SendPacketsRequest,
    SendPacketsResponse,
)
from .types.streams_resources import Channel, Event, Series, Stream
from .types.streams_service import (
    CreateClusterRequest,
    CreateEventRequest,
    CreateSeriesRequest,
    CreateStreamRequest,
    DeleteClusterRequest,
    DeleteEventRequest,
    DeleteSeriesRequest,
    DeleteStreamRequest,
    GenerateStreamHlsTokenRequest,
    GenerateStreamHlsTokenResponse,
    GetClusterRequest,
    GetEventRequest,
    GetSeriesRequest,
    GetStreamRequest,
    GetStreamThumbnailResponse,
    ListClustersRequest,
    ListClustersResponse,
    ListEventsRequest,
    ListEventsResponse,
    ListSeriesRequest,
    ListSeriesResponse,
    ListStreamsRequest,
    ListStreamsResponse,
    MaterializeChannelRequest,
    UpdateClusterRequest,
    UpdateEventRequest,
    UpdateSeriesRequest,
    UpdateStreamRequest,
)
from .types.warehouse import (
    Annotation,
    AnnotationMatchingResult,
    AnnotationValue,
    Asset,
    BoolValue,
    CircleArea,
    ClipAssetRequest,
    ClipAssetResponse,
    Corpus,
    CreateAnnotationRequest,
    CreateAssetRequest,
    CreateCorpusMetadata,
    CreateCorpusRequest,
    CreateDataSchemaRequest,
    CreateSearchConfigRequest,
    Criteria,
    DataSchema,
    DataSchemaDetails,
    DateTimeRange,
    DateTimeRangeArray,
    DeleteAnnotationRequest,
    DeleteAssetMetadata,
    DeleteAssetRequest,
    DeleteCorpusRequest,
    DeleteDataSchemaRequest,
    DeleteSearchConfigRequest,
    FacetBucket,
    FacetBucketType,
    FacetGroup,
    FacetProperty,
    FacetValue,
    FloatRange,
    FloatRangeArray,
    GenerateHlsUriRequest,
    GenerateHlsUriResponse,
    GeoCoordinate,
    GeoLocationArray,
    GetAnnotationRequest,
    GetAssetRequest,
    GetCorpusRequest,
    GetDataSchemaRequest,
    GetSearchConfigRequest,
    IngestAssetRequest,
    IngestAssetResponse,
    IntRange,
    IntRangeArray,
    ListAnnotationsRequest,
    ListAnnotationsResponse,
    ListAssetsRequest,
    ListAssetsResponse,
    ListCorporaRequest,
    ListCorporaResponse,
    ListDataSchemasRequest,
    ListDataSchemasResponse,
    ListSearchConfigsRequest,
    ListSearchConfigsResponse,
    Partition,
    SearchAssetsRequest,
    SearchAssetsResponse,
    SearchConfig,
    SearchCriteriaProperty,
    SearchResultItem,
    StringArray,
    UpdateAnnotationRequest,
    UpdateAssetRequest,
    UpdateCorpusRequest,
    UpdateDataSchemaRequest,
    UpdateSearchConfigRequest,
    UserSpecifiedAnnotation,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.visionai_v1alpha1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.visionai_v1alpha1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.visionai_v1alpha1"
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
    "AppPlatformAsyncClient",
    "LiveVideoAnalyticsAsyncClient",
    "StreamingServiceAsyncClient",
    "StreamsServiceAsyncClient",
    "WarehouseAsyncClient",
    "AIEnabledDevicesInputConfig",
    "AcceleratorType",
    "AcquireLeaseRequest",
    "AddApplicationStreamInputRequest",
    "AddApplicationStreamInputResponse",
    "Analysis",
    "AnalysisDefinition",
    "AnalyzerDefinition",
    "Annotation",
    "AnnotationMatchingResult",
    "AnnotationValue",
    "AppPlatformClient",
    "AppPlatformCloudFunctionRequest",
    "AppPlatformCloudFunctionResponse",
    "AppPlatformEventBody",
    "AppPlatformMetadata",
    "Application",
    "ApplicationConfigs",
    "ApplicationInstance",
    "ApplicationNodeAnnotation",
    "ApplicationStreamInput",
    "Asset",
    "AttributeValue",
    "AutoscalingMetricSpec",
    "BigQueryConfig",
    "BoolValue",
    "Channel",
    "CircleArea",
    "ClassificationPredictionResult",
    "ClipAssetRequest",
    "ClipAssetResponse",
    "Cluster",
    "CommitRequest",
    "ControlledMode",
    "Corpus",
    "CreateAnalysisRequest",
    "CreateAnnotationRequest",
    "CreateApplicationInstancesRequest",
    "CreateApplicationInstancesResponse",
    "CreateApplicationRequest",
    "CreateAssetRequest",
    "CreateClusterRequest",
    "CreateCorpusMetadata",
    "CreateCorpusRequest",
    "CreateDataSchemaRequest",
    "CreateDraftRequest",
    "CreateEventRequest",
    "CreateProcessorRequest",
    "CreateSearchConfigRequest",
    "CreateSeriesRequest",
    "CreateStreamRequest",
    "Criteria",
    "CustomProcessorSourceInfo",
    "DataSchema",
    "DataSchemaDetails",
    "DateTimeRange",
    "DateTimeRangeArray",
    "DedicatedResources",
    "DeleteAnalysisRequest",
    "DeleteAnnotationRequest",
    "DeleteApplicationInstancesRequest",
    "DeleteApplicationInstancesResponse",
    "DeleteApplicationRequest",
    "DeleteAssetMetadata",
    "DeleteAssetRequest",
    "DeleteClusterRequest",
    "DeleteCorpusRequest",
    "DeleteDataSchemaRequest",
    "DeleteDraftRequest",
    "DeleteEventRequest",
    "DeleteProcessorRequest",
    "DeleteSearchConfigRequest",
    "DeleteSeriesRequest",
    "DeleteStreamRequest",
    "DeployApplicationRequest",
    "DeployApplicationResponse",
    "Draft",
    "EagerMode",
    "Event",
    "EventUpdate",
    "FacetBucket",
    "FacetBucketType",
    "FacetGroup",
    "FacetProperty",
    "FacetValue",
    "FloatRange",
    "FloatRangeArray",
    "GcsSource",
    "GeneralObjectDetectionConfig",
    "GenerateHlsUriRequest",
    "GenerateHlsUriResponse",
    "GenerateStreamHlsTokenRequest",
    "GenerateStreamHlsTokenResponse",
    "GeoCoordinate",
    "GeoLocationArray",
    "GetAnalysisRequest",
    "GetAnnotationRequest",
    "GetApplicationRequest",
    "GetAssetRequest",
    "GetClusterRequest",
    "GetCorpusRequest",
    "GetDataSchemaRequest",
    "GetDraftRequest",
    "GetEventRequest",
    "GetInstanceRequest",
    "GetProcessorRequest",
    "GetSearchConfigRequest",
    "GetSeriesRequest",
    "GetStreamRequest",
    "GetStreamThumbnailResponse",
    "GstreamerBufferDescriptor",
    "ImageObjectDetectionPredictionResult",
    "ImageSegmentationPredictionResult",
    "IngestAssetRequest",
    "IngestAssetResponse",
    "Instance",
    "IntRange",
    "IntRangeArray",
    "Lease",
    "LeaseType",
    "ListAnalysesRequest",
    "ListAnalysesResponse",
    "ListAnnotationsRequest",
    "ListAnnotationsResponse",
    "ListApplicationsRequest",
    "ListApplicationsResponse",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListCorporaRequest",
    "ListCorporaResponse",
    "ListDataSchemasRequest",
    "ListDataSchemasResponse",
    "ListDraftsRequest",
    "ListDraftsResponse",
    "ListEventsRequest",
    "ListEventsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListPrebuiltProcessorsRequest",
    "ListPrebuiltProcessorsResponse",
    "ListProcessorsRequest",
    "ListProcessorsResponse",
    "ListSearchConfigsRequest",
    "ListSearchConfigsResponse",
    "ListSeriesRequest",
    "ListSeriesResponse",
    "ListStreamsRequest",
    "ListStreamsResponse",
    "LiveVideoAnalyticsClient",
    "MachineSpec",
    "MaterializeChannelRequest",
    "MediaWarehouseConfig",
    "ModelType",
    "Node",
    "NormalizedPolygon",
    "NormalizedPolyline",
    "NormalizedVertex",
    "ObjectDetectionPredictionResult",
    "OccupancyCountConfig",
    "OccupancyCountingPredictionResult",
    "OperationMetadata",
    "Packet",
    "PacketHeader",
    "PacketType",
    "Partition",
    "PersonBlurConfig",
    "PersonVehicleDetectionConfig",
    "PersonalProtectiveEquipmentDetectionConfig",
    "PersonalProtectiveEquipmentDetectionOutput",
    "Processor",
    "ProcessorConfig",
    "ProcessorIOSpec",
    "RawImageDescriptor",
    "ReceiveEventsControlResponse",
    "ReceiveEventsRequest",
    "ReceiveEventsResponse",
    "ReceivePacketsControlResponse",
    "ReceivePacketsRequest",
    "ReceivePacketsResponse",
    "ReleaseLeaseRequest",
    "ReleaseLeaseResponse",
    "RemoveApplicationStreamInputRequest",
    "RemoveApplicationStreamInputResponse",
    "RenewLeaseRequest",
    "RequestMetadata",
    "ResourceAnnotations",
    "SearchAssetsRequest",
    "SearchAssetsResponse",
    "SearchConfig",
    "SearchCriteriaProperty",
    "SearchResultItem",
    "SendPacketsRequest",
    "SendPacketsResponse",
    "Series",
    "SeriesMetadata",
    "ServerMetadata",
    "Stream",
    "StreamAnnotation",
    "StreamAnnotationType",
    "StreamAnnotations",
    "StreamWithAnnotation",
    "StreamingServiceClient",
    "StreamsServiceClient",
    "StringArray",
    "UndeployApplicationRequest",
    "UndeployApplicationResponse",
    "UpdateAnalysisRequest",
    "UpdateAnnotationRequest",
    "UpdateApplicationInstancesRequest",
    "UpdateApplicationInstancesResponse",
    "UpdateApplicationRequest",
    "UpdateApplicationStreamInputRequest",
    "UpdateApplicationStreamInputResponse",
    "UpdateAssetRequest",
    "UpdateClusterRequest",
    "UpdateCorpusRequest",
    "UpdateDataSchemaRequest",
    "UpdateDraftRequest",
    "UpdateEventRequest",
    "UpdateProcessorRequest",
    "UpdateSearchConfigRequest",
    "UpdateSeriesRequest",
    "UpdateStreamRequest",
    "UserSpecifiedAnnotation",
    "VertexAutoMLVideoConfig",
    "VertexAutoMLVisionConfig",
    "VertexCustomConfig",
    "VideoActionRecognitionPredictionResult",
    "VideoClassificationPredictionResult",
    "VideoObjectTrackingPredictionResult",
    "VideoStreamInputConfig",
    "WarehouseClient",
)
