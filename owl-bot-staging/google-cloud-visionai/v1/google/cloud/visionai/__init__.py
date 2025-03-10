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
from google.cloud.visionai import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.visionai_v1.services.app_platform.client import AppPlatformClient
from google.cloud.visionai_v1.services.app_platform.async_client import AppPlatformAsyncClient
from google.cloud.visionai_v1.services.health_check_service.client import HealthCheckServiceClient
from google.cloud.visionai_v1.services.health_check_service.async_client import HealthCheckServiceAsyncClient
from google.cloud.visionai_v1.services.live_video_analytics.client import LiveVideoAnalyticsClient
from google.cloud.visionai_v1.services.live_video_analytics.async_client import LiveVideoAnalyticsAsyncClient
from google.cloud.visionai_v1.services.streaming_service.client import StreamingServiceClient
from google.cloud.visionai_v1.services.streaming_service.async_client import StreamingServiceAsyncClient
from google.cloud.visionai_v1.services.streams_service.client import StreamsServiceClient
from google.cloud.visionai_v1.services.streams_service.async_client import StreamsServiceAsyncClient
from google.cloud.visionai_v1.services.warehouse.client import WarehouseClient
from google.cloud.visionai_v1.services.warehouse.async_client import WarehouseAsyncClient

from google.cloud.visionai_v1.types.annotations import AppPlatformCloudFunctionRequest
from google.cloud.visionai_v1.types.annotations import AppPlatformCloudFunctionResponse
from google.cloud.visionai_v1.types.annotations import AppPlatformEventBody
from google.cloud.visionai_v1.types.annotations import AppPlatformMetadata
from google.cloud.visionai_v1.types.annotations import ClassificationPredictionResult
from google.cloud.visionai_v1.types.annotations import ImageObjectDetectionPredictionResult
from google.cloud.visionai_v1.types.annotations import ImageSegmentationPredictionResult
from google.cloud.visionai_v1.types.annotations import NormalizedPolygon
from google.cloud.visionai_v1.types.annotations import NormalizedPolyline
from google.cloud.visionai_v1.types.annotations import NormalizedVertex
from google.cloud.visionai_v1.types.annotations import ObjectDetectionPredictionResult
from google.cloud.visionai_v1.types.annotations import OccupancyCountingPredictionResult
from google.cloud.visionai_v1.types.annotations import PersonalProtectiveEquipmentDetectionOutput
from google.cloud.visionai_v1.types.annotations import StreamAnnotation
from google.cloud.visionai_v1.types.annotations import StreamAnnotations
from google.cloud.visionai_v1.types.annotations import VideoActionRecognitionPredictionResult
from google.cloud.visionai_v1.types.annotations import VideoClassificationPredictionResult
from google.cloud.visionai_v1.types.annotations import VideoObjectTrackingPredictionResult
from google.cloud.visionai_v1.types.annotations import StreamAnnotationType
from google.cloud.visionai_v1.types.common import Cluster
from google.cloud.visionai_v1.types.common import GcsSource
from google.cloud.visionai_v1.types.common import OperationMetadata
from google.cloud.visionai_v1.types.health_service import ClusterInfo
from google.cloud.visionai_v1.types.health_service import HealthCheckRequest
from google.cloud.visionai_v1.types.health_service import HealthCheckResponse
from google.cloud.visionai_v1.types.lva import AnalysisDefinition
from google.cloud.visionai_v1.types.lva import AnalyzerDefinition
from google.cloud.visionai_v1.types.lva import AttributeValue
from google.cloud.visionai_v1.types.lva import OperatorDefinition
from google.cloud.visionai_v1.types.lva import ResourceSpecification
from google.cloud.visionai_v1.types.lva import RunStatus
from google.cloud.visionai_v1.types.lva import RunMode
from google.cloud.visionai_v1.types.lva_resources import Analysis
from google.cloud.visionai_v1.types.lva_resources import Operator
from google.cloud.visionai_v1.types.lva_resources import Process
from google.cloud.visionai_v1.types.lva_service import BatchRunProcessRequest
from google.cloud.visionai_v1.types.lva_service import BatchRunProcessResponse
from google.cloud.visionai_v1.types.lva_service import CreateAnalysisRequest
from google.cloud.visionai_v1.types.lva_service import CreateOperatorRequest
from google.cloud.visionai_v1.types.lva_service import CreateProcessRequest
from google.cloud.visionai_v1.types.lva_service import DeleteAnalysisRequest
from google.cloud.visionai_v1.types.lva_service import DeleteOperatorRequest
from google.cloud.visionai_v1.types.lva_service import DeleteProcessRequest
from google.cloud.visionai_v1.types.lva_service import GetAnalysisRequest
from google.cloud.visionai_v1.types.lva_service import GetOperatorRequest
from google.cloud.visionai_v1.types.lva_service import GetProcessRequest
from google.cloud.visionai_v1.types.lva_service import ListAnalysesRequest
from google.cloud.visionai_v1.types.lva_service import ListAnalysesResponse
from google.cloud.visionai_v1.types.lva_service import ListOperatorsRequest
from google.cloud.visionai_v1.types.lva_service import ListOperatorsResponse
from google.cloud.visionai_v1.types.lva_service import ListProcessesRequest
from google.cloud.visionai_v1.types.lva_service import ListProcessesResponse
from google.cloud.visionai_v1.types.lva_service import ListPublicOperatorsRequest
from google.cloud.visionai_v1.types.lva_service import ListPublicOperatorsResponse
from google.cloud.visionai_v1.types.lva_service import OperatorQuery
from google.cloud.visionai_v1.types.lva_service import ResolveOperatorInfoRequest
from google.cloud.visionai_v1.types.lva_service import ResolveOperatorInfoResponse
from google.cloud.visionai_v1.types.lva_service import UpdateAnalysisRequest
from google.cloud.visionai_v1.types.lva_service import UpdateOperatorRequest
from google.cloud.visionai_v1.types.lva_service import UpdateProcessRequest
from google.cloud.visionai_v1.types.lva_service import Registry
from google.cloud.visionai_v1.types.platform import AddApplicationStreamInputRequest
from google.cloud.visionai_v1.types.platform import AddApplicationStreamInputResponse
from google.cloud.visionai_v1.types.platform import AIEnabledDevicesInputConfig
from google.cloud.visionai_v1.types.platform import Application
from google.cloud.visionai_v1.types.platform import ApplicationConfigs
from google.cloud.visionai_v1.types.platform import ApplicationInstance
from google.cloud.visionai_v1.types.platform import ApplicationNodeAnnotation
from google.cloud.visionai_v1.types.platform import ApplicationStreamInput
from google.cloud.visionai_v1.types.platform import AutoscalingMetricSpec
from google.cloud.visionai_v1.types.platform import BigQueryConfig
from google.cloud.visionai_v1.types.platform import CreateApplicationInstancesRequest
from google.cloud.visionai_v1.types.platform import CreateApplicationInstancesResponse
from google.cloud.visionai_v1.types.platform import CreateApplicationRequest
from google.cloud.visionai_v1.types.platform import CreateDraftRequest
from google.cloud.visionai_v1.types.platform import CreateProcessorRequest
from google.cloud.visionai_v1.types.platform import CustomProcessorSourceInfo
from google.cloud.visionai_v1.types.platform import DedicatedResources
from google.cloud.visionai_v1.types.platform import DeleteApplicationInstancesRequest
from google.cloud.visionai_v1.types.platform import DeleteApplicationInstancesResponse
from google.cloud.visionai_v1.types.platform import DeleteApplicationRequest
from google.cloud.visionai_v1.types.platform import DeleteDraftRequest
from google.cloud.visionai_v1.types.platform import DeleteProcessorRequest
from google.cloud.visionai_v1.types.platform import DeployApplicationRequest
from google.cloud.visionai_v1.types.platform import DeployApplicationResponse
from google.cloud.visionai_v1.types.platform import Draft
from google.cloud.visionai_v1.types.platform import GcsOutputConfig
from google.cloud.visionai_v1.types.platform import GeneralObjectDetectionConfig
from google.cloud.visionai_v1.types.platform import GetApplicationRequest
from google.cloud.visionai_v1.types.platform import GetDraftRequest
from google.cloud.visionai_v1.types.platform import GetInstanceRequest
from google.cloud.visionai_v1.types.platform import GetProcessorRequest
from google.cloud.visionai_v1.types.platform import Instance
from google.cloud.visionai_v1.types.platform import ListApplicationsRequest
from google.cloud.visionai_v1.types.platform import ListApplicationsResponse
from google.cloud.visionai_v1.types.platform import ListDraftsRequest
from google.cloud.visionai_v1.types.platform import ListDraftsResponse
from google.cloud.visionai_v1.types.platform import ListInstancesRequest
from google.cloud.visionai_v1.types.platform import ListInstancesResponse
from google.cloud.visionai_v1.types.platform import ListPrebuiltProcessorsRequest
from google.cloud.visionai_v1.types.platform import ListPrebuiltProcessorsResponse
from google.cloud.visionai_v1.types.platform import ListProcessorsRequest
from google.cloud.visionai_v1.types.platform import ListProcessorsResponse
from google.cloud.visionai_v1.types.platform import MachineSpec
from google.cloud.visionai_v1.types.platform import MediaWarehouseConfig
from google.cloud.visionai_v1.types.platform import Node
from google.cloud.visionai_v1.types.platform import OccupancyCountConfig
from google.cloud.visionai_v1.types.platform import PersonalProtectiveEquipmentDetectionConfig
from google.cloud.visionai_v1.types.platform import PersonBlurConfig
from google.cloud.visionai_v1.types.platform import PersonVehicleDetectionConfig
from google.cloud.visionai_v1.types.platform import Processor
from google.cloud.visionai_v1.types.platform import ProcessorConfig
from google.cloud.visionai_v1.types.platform import ProcessorIOSpec
from google.cloud.visionai_v1.types.platform import ProductRecognizerConfig
from google.cloud.visionai_v1.types.platform import RemoveApplicationStreamInputRequest
from google.cloud.visionai_v1.types.platform import RemoveApplicationStreamInputResponse
from google.cloud.visionai_v1.types.platform import ResourceAnnotations
from google.cloud.visionai_v1.types.platform import StreamWithAnnotation
from google.cloud.visionai_v1.types.platform import TagParsingConfig
from google.cloud.visionai_v1.types.platform import TagRecognizerConfig
from google.cloud.visionai_v1.types.platform import UndeployApplicationRequest
from google.cloud.visionai_v1.types.platform import UndeployApplicationResponse
from google.cloud.visionai_v1.types.platform import UniversalInputConfig
from google.cloud.visionai_v1.types.platform import UpdateApplicationInstancesRequest
from google.cloud.visionai_v1.types.platform import UpdateApplicationInstancesResponse
from google.cloud.visionai_v1.types.platform import UpdateApplicationRequest
from google.cloud.visionai_v1.types.platform import UpdateApplicationStreamInputRequest
from google.cloud.visionai_v1.types.platform import UpdateApplicationStreamInputResponse
from google.cloud.visionai_v1.types.platform import UpdateDraftRequest
from google.cloud.visionai_v1.types.platform import UpdateProcessorRequest
from google.cloud.visionai_v1.types.platform import VertexAutoMLVideoConfig
from google.cloud.visionai_v1.types.platform import VertexAutoMLVisionConfig
from google.cloud.visionai_v1.types.platform import VertexCustomConfig
from google.cloud.visionai_v1.types.platform import VideoStreamInputConfig
from google.cloud.visionai_v1.types.platform import AcceleratorType
from google.cloud.visionai_v1.types.platform import DataType
from google.cloud.visionai_v1.types.platform import ModelType
from google.cloud.visionai_v1.types.streaming_resources import GstreamerBufferDescriptor
from google.cloud.visionai_v1.types.streaming_resources import Packet
from google.cloud.visionai_v1.types.streaming_resources import PacketHeader
from google.cloud.visionai_v1.types.streaming_resources import PacketType
from google.cloud.visionai_v1.types.streaming_resources import RawImageDescriptor
from google.cloud.visionai_v1.types.streaming_resources import SeriesMetadata
from google.cloud.visionai_v1.types.streaming_resources import ServerMetadata
from google.cloud.visionai_v1.types.streaming_service import AcquireLeaseRequest
from google.cloud.visionai_v1.types.streaming_service import CommitRequest
from google.cloud.visionai_v1.types.streaming_service import ControlledMode
from google.cloud.visionai_v1.types.streaming_service import EagerMode
from google.cloud.visionai_v1.types.streaming_service import EventUpdate
from google.cloud.visionai_v1.types.streaming_service import Lease
from google.cloud.visionai_v1.types.streaming_service import ReceiveEventsControlResponse
from google.cloud.visionai_v1.types.streaming_service import ReceiveEventsRequest
from google.cloud.visionai_v1.types.streaming_service import ReceiveEventsResponse
from google.cloud.visionai_v1.types.streaming_service import ReceivePacketsControlResponse
from google.cloud.visionai_v1.types.streaming_service import ReceivePacketsRequest
from google.cloud.visionai_v1.types.streaming_service import ReceivePacketsResponse
from google.cloud.visionai_v1.types.streaming_service import ReleaseLeaseRequest
from google.cloud.visionai_v1.types.streaming_service import ReleaseLeaseResponse
from google.cloud.visionai_v1.types.streaming_service import RenewLeaseRequest
from google.cloud.visionai_v1.types.streaming_service import RequestMetadata
from google.cloud.visionai_v1.types.streaming_service import SendPacketsRequest
from google.cloud.visionai_v1.types.streaming_service import SendPacketsResponse
from google.cloud.visionai_v1.types.streaming_service import LeaseType
from google.cloud.visionai_v1.types.streams_resources import Channel
from google.cloud.visionai_v1.types.streams_resources import Event
from google.cloud.visionai_v1.types.streams_resources import Series
from google.cloud.visionai_v1.types.streams_resources import Stream
from google.cloud.visionai_v1.types.streams_service import CreateClusterRequest
from google.cloud.visionai_v1.types.streams_service import CreateEventRequest
from google.cloud.visionai_v1.types.streams_service import CreateSeriesRequest
from google.cloud.visionai_v1.types.streams_service import CreateStreamRequest
from google.cloud.visionai_v1.types.streams_service import DeleteClusterRequest
from google.cloud.visionai_v1.types.streams_service import DeleteEventRequest
from google.cloud.visionai_v1.types.streams_service import DeleteSeriesRequest
from google.cloud.visionai_v1.types.streams_service import DeleteStreamRequest
from google.cloud.visionai_v1.types.streams_service import GenerateStreamHlsTokenRequest
from google.cloud.visionai_v1.types.streams_service import GenerateStreamHlsTokenResponse
from google.cloud.visionai_v1.types.streams_service import GetClusterRequest
from google.cloud.visionai_v1.types.streams_service import GetEventRequest
from google.cloud.visionai_v1.types.streams_service import GetSeriesRequest
from google.cloud.visionai_v1.types.streams_service import GetStreamRequest
from google.cloud.visionai_v1.types.streams_service import GetStreamThumbnailRequest
from google.cloud.visionai_v1.types.streams_service import GetStreamThumbnailResponse
from google.cloud.visionai_v1.types.streams_service import ListClustersRequest
from google.cloud.visionai_v1.types.streams_service import ListClustersResponse
from google.cloud.visionai_v1.types.streams_service import ListEventsRequest
from google.cloud.visionai_v1.types.streams_service import ListEventsResponse
from google.cloud.visionai_v1.types.streams_service import ListSeriesRequest
from google.cloud.visionai_v1.types.streams_service import ListSeriesResponse
from google.cloud.visionai_v1.types.streams_service import ListStreamsRequest
from google.cloud.visionai_v1.types.streams_service import ListStreamsResponse
from google.cloud.visionai_v1.types.streams_service import MaterializeChannelRequest
from google.cloud.visionai_v1.types.streams_service import UpdateClusterRequest
from google.cloud.visionai_v1.types.streams_service import UpdateEventRequest
from google.cloud.visionai_v1.types.streams_service import UpdateSeriesRequest
from google.cloud.visionai_v1.types.streams_service import UpdateStreamRequest
from google.cloud.visionai_v1.types.warehouse import AddCollectionItemRequest
from google.cloud.visionai_v1.types.warehouse import AddCollectionItemResponse
from google.cloud.visionai_v1.types.warehouse import AnalyzeAssetMetadata
from google.cloud.visionai_v1.types.warehouse import AnalyzeAssetRequest
from google.cloud.visionai_v1.types.warehouse import AnalyzeAssetResponse
from google.cloud.visionai_v1.types.warehouse import AnalyzeCorpusMetadata
from google.cloud.visionai_v1.types.warehouse import AnalyzeCorpusRequest
from google.cloud.visionai_v1.types.warehouse import AnalyzeCorpusResponse
from google.cloud.visionai_v1.types.warehouse import Annotation
from google.cloud.visionai_v1.types.warehouse import AnnotationCustomizedStruct
from google.cloud.visionai_v1.types.warehouse import AnnotationList
from google.cloud.visionai_v1.types.warehouse import AnnotationMatchingResult
from google.cloud.visionai_v1.types.warehouse import AnnotationValue
from google.cloud.visionai_v1.types.warehouse import Asset
from google.cloud.visionai_v1.types.warehouse import AssetSource
from google.cloud.visionai_v1.types.warehouse import BatchOperationStatus
from google.cloud.visionai_v1.types.warehouse import BoolValue
from google.cloud.visionai_v1.types.warehouse import CircleArea
from google.cloud.visionai_v1.types.warehouse import ClipAssetRequest
from google.cloud.visionai_v1.types.warehouse import ClipAssetResponse
from google.cloud.visionai_v1.types.warehouse import Collection
from google.cloud.visionai_v1.types.warehouse import CollectionItem
from google.cloud.visionai_v1.types.warehouse import Corpus
from google.cloud.visionai_v1.types.warehouse import CreateAnnotationRequest
from google.cloud.visionai_v1.types.warehouse import CreateAssetRequest
from google.cloud.visionai_v1.types.warehouse import CreateCollectionMetadata
from google.cloud.visionai_v1.types.warehouse import CreateCollectionRequest
from google.cloud.visionai_v1.types.warehouse import CreateCorpusMetadata
from google.cloud.visionai_v1.types.warehouse import CreateCorpusRequest
from google.cloud.visionai_v1.types.warehouse import CreateDataSchemaRequest
from google.cloud.visionai_v1.types.warehouse import CreateIndexEndpointMetadata
from google.cloud.visionai_v1.types.warehouse import CreateIndexEndpointRequest
from google.cloud.visionai_v1.types.warehouse import CreateIndexMetadata
from google.cloud.visionai_v1.types.warehouse import CreateIndexRequest
from google.cloud.visionai_v1.types.warehouse import CreateSearchConfigRequest
from google.cloud.visionai_v1.types.warehouse import CreateSearchHypernymRequest
from google.cloud.visionai_v1.types.warehouse import Criteria
from google.cloud.visionai_v1.types.warehouse import DataSchema
from google.cloud.visionai_v1.types.warehouse import DataSchemaDetails
from google.cloud.visionai_v1.types.warehouse import DateTimeRange
from google.cloud.visionai_v1.types.warehouse import DateTimeRangeArray
from google.cloud.visionai_v1.types.warehouse import DeleteAnnotationRequest
from google.cloud.visionai_v1.types.warehouse import DeleteAssetMetadata
from google.cloud.visionai_v1.types.warehouse import DeleteAssetRequest
from google.cloud.visionai_v1.types.warehouse import DeleteCollectionMetadata
from google.cloud.visionai_v1.types.warehouse import DeleteCollectionRequest
from google.cloud.visionai_v1.types.warehouse import DeleteCorpusRequest
from google.cloud.visionai_v1.types.warehouse import DeleteDataSchemaRequest
from google.cloud.visionai_v1.types.warehouse import DeleteIndexEndpointMetadata
from google.cloud.visionai_v1.types.warehouse import DeleteIndexEndpointRequest
from google.cloud.visionai_v1.types.warehouse import DeleteIndexMetadata
from google.cloud.visionai_v1.types.warehouse import DeleteIndexRequest
from google.cloud.visionai_v1.types.warehouse import DeleteSearchConfigRequest
from google.cloud.visionai_v1.types.warehouse import DeleteSearchHypernymRequest
from google.cloud.visionai_v1.types.warehouse import DeployedIndex
from google.cloud.visionai_v1.types.warehouse import DeployedIndexReference
from google.cloud.visionai_v1.types.warehouse import DeployIndexMetadata
from google.cloud.visionai_v1.types.warehouse import DeployIndexRequest
from google.cloud.visionai_v1.types.warehouse import DeployIndexResponse
from google.cloud.visionai_v1.types.warehouse import FacetBucket
from google.cloud.visionai_v1.types.warehouse import FacetGroup
from google.cloud.visionai_v1.types.warehouse import FacetProperty
from google.cloud.visionai_v1.types.warehouse import FacetValue
from google.cloud.visionai_v1.types.warehouse import FloatRange
from google.cloud.visionai_v1.types.warehouse import FloatRangeArray
from google.cloud.visionai_v1.types.warehouse import GenerateHlsUriRequest
from google.cloud.visionai_v1.types.warehouse import GenerateHlsUriResponse
from google.cloud.visionai_v1.types.warehouse import GenerateRetrievalUrlRequest
from google.cloud.visionai_v1.types.warehouse import GenerateRetrievalUrlResponse
from google.cloud.visionai_v1.types.warehouse import GeoCoordinate
from google.cloud.visionai_v1.types.warehouse import GeoLocationArray
from google.cloud.visionai_v1.types.warehouse import GetAnnotationRequest
from google.cloud.visionai_v1.types.warehouse import GetAssetRequest
from google.cloud.visionai_v1.types.warehouse import GetCollectionRequest
from google.cloud.visionai_v1.types.warehouse import GetCorpusRequest
from google.cloud.visionai_v1.types.warehouse import GetDataSchemaRequest
from google.cloud.visionai_v1.types.warehouse import GetIndexEndpointRequest
from google.cloud.visionai_v1.types.warehouse import GetIndexRequest
from google.cloud.visionai_v1.types.warehouse import GetSearchConfigRequest
from google.cloud.visionai_v1.types.warehouse import GetSearchHypernymRequest
from google.cloud.visionai_v1.types.warehouse import ImageQuery
from google.cloud.visionai_v1.types.warehouse import ImportAssetsMetadata
from google.cloud.visionai_v1.types.warehouse import ImportAssetsRequest
from google.cloud.visionai_v1.types.warehouse import ImportAssetsResponse
from google.cloud.visionai_v1.types.warehouse import Index
from google.cloud.visionai_v1.types.warehouse import IndexAssetMetadata
from google.cloud.visionai_v1.types.warehouse import IndexAssetRequest
from google.cloud.visionai_v1.types.warehouse import IndexAssetResponse
from google.cloud.visionai_v1.types.warehouse import IndexedAsset
from google.cloud.visionai_v1.types.warehouse import IndexEndpoint
from google.cloud.visionai_v1.types.warehouse import IndexingStatus
from google.cloud.visionai_v1.types.warehouse import IngestAssetRequest
from google.cloud.visionai_v1.types.warehouse import IngestAssetResponse
from google.cloud.visionai_v1.types.warehouse import IntRange
from google.cloud.visionai_v1.types.warehouse import IntRangeArray
from google.cloud.visionai_v1.types.warehouse import ListAnnotationsRequest
from google.cloud.visionai_v1.types.warehouse import ListAnnotationsResponse
from google.cloud.visionai_v1.types.warehouse import ListAssetsRequest
from google.cloud.visionai_v1.types.warehouse import ListAssetsResponse
from google.cloud.visionai_v1.types.warehouse import ListCollectionsRequest
from google.cloud.visionai_v1.types.warehouse import ListCollectionsResponse
from google.cloud.visionai_v1.types.warehouse import ListCorporaRequest
from google.cloud.visionai_v1.types.warehouse import ListCorporaResponse
from google.cloud.visionai_v1.types.warehouse import ListDataSchemasRequest
from google.cloud.visionai_v1.types.warehouse import ListDataSchemasResponse
from google.cloud.visionai_v1.types.warehouse import ListIndexEndpointsRequest
from google.cloud.visionai_v1.types.warehouse import ListIndexEndpointsResponse
from google.cloud.visionai_v1.types.warehouse import ListIndexesRequest
from google.cloud.visionai_v1.types.warehouse import ListIndexesResponse
from google.cloud.visionai_v1.types.warehouse import ListSearchConfigsRequest
from google.cloud.visionai_v1.types.warehouse import ListSearchConfigsResponse
from google.cloud.visionai_v1.types.warehouse import ListSearchHypernymsRequest
from google.cloud.visionai_v1.types.warehouse import ListSearchHypernymsResponse
from google.cloud.visionai_v1.types.warehouse import Partition
from google.cloud.visionai_v1.types.warehouse import RemoveCollectionItemRequest
from google.cloud.visionai_v1.types.warehouse import RemoveCollectionItemResponse
from google.cloud.visionai_v1.types.warehouse import RemoveIndexAssetMetadata
from google.cloud.visionai_v1.types.warehouse import RemoveIndexAssetRequest
from google.cloud.visionai_v1.types.warehouse import RemoveIndexAssetResponse
from google.cloud.visionai_v1.types.warehouse import SchemaKeySortingStrategy
from google.cloud.visionai_v1.types.warehouse import SearchAssetsRequest
from google.cloud.visionai_v1.types.warehouse import SearchAssetsResponse
from google.cloud.visionai_v1.types.warehouse import SearchCapability
from google.cloud.visionai_v1.types.warehouse import SearchCapabilitySetting
from google.cloud.visionai_v1.types.warehouse import SearchConfig
from google.cloud.visionai_v1.types.warehouse import SearchCriteriaProperty
from google.cloud.visionai_v1.types.warehouse import SearchHypernym
from google.cloud.visionai_v1.types.warehouse import SearchIndexEndpointRequest
from google.cloud.visionai_v1.types.warehouse import SearchIndexEndpointResponse
from google.cloud.visionai_v1.types.warehouse import SearchResultItem
from google.cloud.visionai_v1.types.warehouse import StringArray
from google.cloud.visionai_v1.types.warehouse import UndeployIndexMetadata
from google.cloud.visionai_v1.types.warehouse import UndeployIndexRequest
from google.cloud.visionai_v1.types.warehouse import UndeployIndexResponse
from google.cloud.visionai_v1.types.warehouse import UpdateAnnotationRequest
from google.cloud.visionai_v1.types.warehouse import UpdateAssetRequest
from google.cloud.visionai_v1.types.warehouse import UpdateCollectionRequest
from google.cloud.visionai_v1.types.warehouse import UpdateCorpusRequest
from google.cloud.visionai_v1.types.warehouse import UpdateDataSchemaRequest
from google.cloud.visionai_v1.types.warehouse import UpdateIndexEndpointMetadata
from google.cloud.visionai_v1.types.warehouse import UpdateIndexEndpointRequest
from google.cloud.visionai_v1.types.warehouse import UpdateIndexMetadata
from google.cloud.visionai_v1.types.warehouse import UpdateIndexRequest
from google.cloud.visionai_v1.types.warehouse import UpdateSearchConfigRequest
from google.cloud.visionai_v1.types.warehouse import UpdateSearchHypernymRequest
from google.cloud.visionai_v1.types.warehouse import UploadAssetMetadata
from google.cloud.visionai_v1.types.warehouse import UploadAssetRequest
from google.cloud.visionai_v1.types.warehouse import UploadAssetResponse
from google.cloud.visionai_v1.types.warehouse import UserSpecifiedAnnotation
from google.cloud.visionai_v1.types.warehouse import ViewCollectionItemsRequest
from google.cloud.visionai_v1.types.warehouse import ViewCollectionItemsResponse
from google.cloud.visionai_v1.types.warehouse import ViewIndexedAssetsRequest
from google.cloud.visionai_v1.types.warehouse import ViewIndexedAssetsResponse
from google.cloud.visionai_v1.types.warehouse import FacetBucketType

__all__ = ('AppPlatformClient',
    'AppPlatformAsyncClient',
    'HealthCheckServiceClient',
    'HealthCheckServiceAsyncClient',
    'LiveVideoAnalyticsClient',
    'LiveVideoAnalyticsAsyncClient',
    'StreamingServiceClient',
    'StreamingServiceAsyncClient',
    'StreamsServiceClient',
    'StreamsServiceAsyncClient',
    'WarehouseClient',
    'WarehouseAsyncClient',
    'AppPlatformCloudFunctionRequest',
    'AppPlatformCloudFunctionResponse',
    'AppPlatformEventBody',
    'AppPlatformMetadata',
    'ClassificationPredictionResult',
    'ImageObjectDetectionPredictionResult',
    'ImageSegmentationPredictionResult',
    'NormalizedPolygon',
    'NormalizedPolyline',
    'NormalizedVertex',
    'ObjectDetectionPredictionResult',
    'OccupancyCountingPredictionResult',
    'PersonalProtectiveEquipmentDetectionOutput',
    'StreamAnnotation',
    'StreamAnnotations',
    'VideoActionRecognitionPredictionResult',
    'VideoClassificationPredictionResult',
    'VideoObjectTrackingPredictionResult',
    'StreamAnnotationType',
    'Cluster',
    'GcsSource',
    'OperationMetadata',
    'ClusterInfo',
    'HealthCheckRequest',
    'HealthCheckResponse',
    'AnalysisDefinition',
    'AnalyzerDefinition',
    'AttributeValue',
    'OperatorDefinition',
    'ResourceSpecification',
    'RunStatus',
    'RunMode',
    'Analysis',
    'Operator',
    'Process',
    'BatchRunProcessRequest',
    'BatchRunProcessResponse',
    'CreateAnalysisRequest',
    'CreateOperatorRequest',
    'CreateProcessRequest',
    'DeleteAnalysisRequest',
    'DeleteOperatorRequest',
    'DeleteProcessRequest',
    'GetAnalysisRequest',
    'GetOperatorRequest',
    'GetProcessRequest',
    'ListAnalysesRequest',
    'ListAnalysesResponse',
    'ListOperatorsRequest',
    'ListOperatorsResponse',
    'ListProcessesRequest',
    'ListProcessesResponse',
    'ListPublicOperatorsRequest',
    'ListPublicOperatorsResponse',
    'OperatorQuery',
    'ResolveOperatorInfoRequest',
    'ResolveOperatorInfoResponse',
    'UpdateAnalysisRequest',
    'UpdateOperatorRequest',
    'UpdateProcessRequest',
    'Registry',
    'AddApplicationStreamInputRequest',
    'AddApplicationStreamInputResponse',
    'AIEnabledDevicesInputConfig',
    'Application',
    'ApplicationConfigs',
    'ApplicationInstance',
    'ApplicationNodeAnnotation',
    'ApplicationStreamInput',
    'AutoscalingMetricSpec',
    'BigQueryConfig',
    'CreateApplicationInstancesRequest',
    'CreateApplicationInstancesResponse',
    'CreateApplicationRequest',
    'CreateDraftRequest',
    'CreateProcessorRequest',
    'CustomProcessorSourceInfo',
    'DedicatedResources',
    'DeleteApplicationInstancesRequest',
    'DeleteApplicationInstancesResponse',
    'DeleteApplicationRequest',
    'DeleteDraftRequest',
    'DeleteProcessorRequest',
    'DeployApplicationRequest',
    'DeployApplicationResponse',
    'Draft',
    'GcsOutputConfig',
    'GeneralObjectDetectionConfig',
    'GetApplicationRequest',
    'GetDraftRequest',
    'GetInstanceRequest',
    'GetProcessorRequest',
    'Instance',
    'ListApplicationsRequest',
    'ListApplicationsResponse',
    'ListDraftsRequest',
    'ListDraftsResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListPrebuiltProcessorsRequest',
    'ListPrebuiltProcessorsResponse',
    'ListProcessorsRequest',
    'ListProcessorsResponse',
    'MachineSpec',
    'MediaWarehouseConfig',
    'Node',
    'OccupancyCountConfig',
    'PersonalProtectiveEquipmentDetectionConfig',
    'PersonBlurConfig',
    'PersonVehicleDetectionConfig',
    'Processor',
    'ProcessorConfig',
    'ProcessorIOSpec',
    'ProductRecognizerConfig',
    'RemoveApplicationStreamInputRequest',
    'RemoveApplicationStreamInputResponse',
    'ResourceAnnotations',
    'StreamWithAnnotation',
    'TagParsingConfig',
    'TagRecognizerConfig',
    'UndeployApplicationRequest',
    'UndeployApplicationResponse',
    'UniversalInputConfig',
    'UpdateApplicationInstancesRequest',
    'UpdateApplicationInstancesResponse',
    'UpdateApplicationRequest',
    'UpdateApplicationStreamInputRequest',
    'UpdateApplicationStreamInputResponse',
    'UpdateDraftRequest',
    'UpdateProcessorRequest',
    'VertexAutoMLVideoConfig',
    'VertexAutoMLVisionConfig',
    'VertexCustomConfig',
    'VideoStreamInputConfig',
    'AcceleratorType',
    'DataType',
    'ModelType',
    'GstreamerBufferDescriptor',
    'Packet',
    'PacketHeader',
    'PacketType',
    'RawImageDescriptor',
    'SeriesMetadata',
    'ServerMetadata',
    'AcquireLeaseRequest',
    'CommitRequest',
    'ControlledMode',
    'EagerMode',
    'EventUpdate',
    'Lease',
    'ReceiveEventsControlResponse',
    'ReceiveEventsRequest',
    'ReceiveEventsResponse',
    'ReceivePacketsControlResponse',
    'ReceivePacketsRequest',
    'ReceivePacketsResponse',
    'ReleaseLeaseRequest',
    'ReleaseLeaseResponse',
    'RenewLeaseRequest',
    'RequestMetadata',
    'SendPacketsRequest',
    'SendPacketsResponse',
    'LeaseType',
    'Channel',
    'Event',
    'Series',
    'Stream',
    'CreateClusterRequest',
    'CreateEventRequest',
    'CreateSeriesRequest',
    'CreateStreamRequest',
    'DeleteClusterRequest',
    'DeleteEventRequest',
    'DeleteSeriesRequest',
    'DeleteStreamRequest',
    'GenerateStreamHlsTokenRequest',
    'GenerateStreamHlsTokenResponse',
    'GetClusterRequest',
    'GetEventRequest',
    'GetSeriesRequest',
    'GetStreamRequest',
    'GetStreamThumbnailRequest',
    'GetStreamThumbnailResponse',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListEventsRequest',
    'ListEventsResponse',
    'ListSeriesRequest',
    'ListSeriesResponse',
    'ListStreamsRequest',
    'ListStreamsResponse',
    'MaterializeChannelRequest',
    'UpdateClusterRequest',
    'UpdateEventRequest',
    'UpdateSeriesRequest',
    'UpdateStreamRequest',
    'AddCollectionItemRequest',
    'AddCollectionItemResponse',
    'AnalyzeAssetMetadata',
    'AnalyzeAssetRequest',
    'AnalyzeAssetResponse',
    'AnalyzeCorpusMetadata',
    'AnalyzeCorpusRequest',
    'AnalyzeCorpusResponse',
    'Annotation',
    'AnnotationCustomizedStruct',
    'AnnotationList',
    'AnnotationMatchingResult',
    'AnnotationValue',
    'Asset',
    'AssetSource',
    'BatchOperationStatus',
    'BoolValue',
    'CircleArea',
    'ClipAssetRequest',
    'ClipAssetResponse',
    'Collection',
    'CollectionItem',
    'Corpus',
    'CreateAnnotationRequest',
    'CreateAssetRequest',
    'CreateCollectionMetadata',
    'CreateCollectionRequest',
    'CreateCorpusMetadata',
    'CreateCorpusRequest',
    'CreateDataSchemaRequest',
    'CreateIndexEndpointMetadata',
    'CreateIndexEndpointRequest',
    'CreateIndexMetadata',
    'CreateIndexRequest',
    'CreateSearchConfigRequest',
    'CreateSearchHypernymRequest',
    'Criteria',
    'DataSchema',
    'DataSchemaDetails',
    'DateTimeRange',
    'DateTimeRangeArray',
    'DeleteAnnotationRequest',
    'DeleteAssetMetadata',
    'DeleteAssetRequest',
    'DeleteCollectionMetadata',
    'DeleteCollectionRequest',
    'DeleteCorpusRequest',
    'DeleteDataSchemaRequest',
    'DeleteIndexEndpointMetadata',
    'DeleteIndexEndpointRequest',
    'DeleteIndexMetadata',
    'DeleteIndexRequest',
    'DeleteSearchConfigRequest',
    'DeleteSearchHypernymRequest',
    'DeployedIndex',
    'DeployedIndexReference',
    'DeployIndexMetadata',
    'DeployIndexRequest',
    'DeployIndexResponse',
    'FacetBucket',
    'FacetGroup',
    'FacetProperty',
    'FacetValue',
    'FloatRange',
    'FloatRangeArray',
    'GenerateHlsUriRequest',
    'GenerateHlsUriResponse',
    'GenerateRetrievalUrlRequest',
    'GenerateRetrievalUrlResponse',
    'GeoCoordinate',
    'GeoLocationArray',
    'GetAnnotationRequest',
    'GetAssetRequest',
    'GetCollectionRequest',
    'GetCorpusRequest',
    'GetDataSchemaRequest',
    'GetIndexEndpointRequest',
    'GetIndexRequest',
    'GetSearchConfigRequest',
    'GetSearchHypernymRequest',
    'ImageQuery',
    'ImportAssetsMetadata',
    'ImportAssetsRequest',
    'ImportAssetsResponse',
    'Index',
    'IndexAssetMetadata',
    'IndexAssetRequest',
    'IndexAssetResponse',
    'IndexedAsset',
    'IndexEndpoint',
    'IndexingStatus',
    'IngestAssetRequest',
    'IngestAssetResponse',
    'IntRange',
    'IntRangeArray',
    'ListAnnotationsRequest',
    'ListAnnotationsResponse',
    'ListAssetsRequest',
    'ListAssetsResponse',
    'ListCollectionsRequest',
    'ListCollectionsResponse',
    'ListCorporaRequest',
    'ListCorporaResponse',
    'ListDataSchemasRequest',
    'ListDataSchemasResponse',
    'ListIndexEndpointsRequest',
    'ListIndexEndpointsResponse',
    'ListIndexesRequest',
    'ListIndexesResponse',
    'ListSearchConfigsRequest',
    'ListSearchConfigsResponse',
    'ListSearchHypernymsRequest',
    'ListSearchHypernymsResponse',
    'Partition',
    'RemoveCollectionItemRequest',
    'RemoveCollectionItemResponse',
    'RemoveIndexAssetMetadata',
    'RemoveIndexAssetRequest',
    'RemoveIndexAssetResponse',
    'SchemaKeySortingStrategy',
    'SearchAssetsRequest',
    'SearchAssetsResponse',
    'SearchCapability',
    'SearchCapabilitySetting',
    'SearchConfig',
    'SearchCriteriaProperty',
    'SearchHypernym',
    'SearchIndexEndpointRequest',
    'SearchIndexEndpointResponse',
    'SearchResultItem',
    'StringArray',
    'UndeployIndexMetadata',
    'UndeployIndexRequest',
    'UndeployIndexResponse',
    'UpdateAnnotationRequest',
    'UpdateAssetRequest',
    'UpdateCollectionRequest',
    'UpdateCorpusRequest',
    'UpdateDataSchemaRequest',
    'UpdateIndexEndpointMetadata',
    'UpdateIndexEndpointRequest',
    'UpdateIndexMetadata',
    'UpdateIndexRequest',
    'UpdateSearchConfigRequest',
    'UpdateSearchHypernymRequest',
    'UploadAssetMetadata',
    'UploadAssetRequest',
    'UploadAssetResponse',
    'UserSpecifiedAnnotation',
    'ViewCollectionItemsRequest',
    'ViewCollectionItemsResponse',
    'ViewIndexedAssetsRequest',
    'ViewIndexedAssetsResponse',
    'FacetBucketType',
)
