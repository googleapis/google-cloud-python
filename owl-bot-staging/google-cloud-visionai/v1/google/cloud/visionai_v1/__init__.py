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
from google.cloud.visionai_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.app_platform import AppPlatformClient
from .services.app_platform import AppPlatformAsyncClient
from .services.health_check_service import HealthCheckServiceClient
from .services.health_check_service import HealthCheckServiceAsyncClient
from .services.live_video_analytics import LiveVideoAnalyticsClient
from .services.live_video_analytics import LiveVideoAnalyticsAsyncClient
from .services.streaming_service import StreamingServiceClient
from .services.streaming_service import StreamingServiceAsyncClient
from .services.streams_service import StreamsServiceClient
from .services.streams_service import StreamsServiceAsyncClient
from .services.warehouse import WarehouseClient
from .services.warehouse import WarehouseAsyncClient

from .types.annotations import AppPlatformCloudFunctionRequest
from .types.annotations import AppPlatformCloudFunctionResponse
from .types.annotations import AppPlatformEventBody
from .types.annotations import AppPlatformMetadata
from .types.annotations import ClassificationPredictionResult
from .types.annotations import ImageObjectDetectionPredictionResult
from .types.annotations import ImageSegmentationPredictionResult
from .types.annotations import NormalizedPolygon
from .types.annotations import NormalizedPolyline
from .types.annotations import NormalizedVertex
from .types.annotations import ObjectDetectionPredictionResult
from .types.annotations import OccupancyCountingPredictionResult
from .types.annotations import PersonalProtectiveEquipmentDetectionOutput
from .types.annotations import StreamAnnotation
from .types.annotations import StreamAnnotations
from .types.annotations import VideoActionRecognitionPredictionResult
from .types.annotations import VideoClassificationPredictionResult
from .types.annotations import VideoObjectTrackingPredictionResult
from .types.annotations import StreamAnnotationType
from .types.common import Cluster
from .types.common import GcsSource
from .types.common import OperationMetadata
from .types.health_service import ClusterInfo
from .types.health_service import HealthCheckRequest
from .types.health_service import HealthCheckResponse
from .types.lva import AnalysisDefinition
from .types.lva import AnalyzerDefinition
from .types.lva import AttributeValue
from .types.lva import OperatorDefinition
from .types.lva import ResourceSpecification
from .types.lva import RunStatus
from .types.lva import RunMode
from .types.lva_resources import Analysis
from .types.lva_resources import Operator
from .types.lva_resources import Process
from .types.lva_service import BatchRunProcessRequest
from .types.lva_service import BatchRunProcessResponse
from .types.lva_service import CreateAnalysisRequest
from .types.lva_service import CreateOperatorRequest
from .types.lva_service import CreateProcessRequest
from .types.lva_service import DeleteAnalysisRequest
from .types.lva_service import DeleteOperatorRequest
from .types.lva_service import DeleteProcessRequest
from .types.lva_service import GetAnalysisRequest
from .types.lva_service import GetOperatorRequest
from .types.lva_service import GetProcessRequest
from .types.lva_service import ListAnalysesRequest
from .types.lva_service import ListAnalysesResponse
from .types.lva_service import ListOperatorsRequest
from .types.lva_service import ListOperatorsResponse
from .types.lva_service import ListProcessesRequest
from .types.lva_service import ListProcessesResponse
from .types.lva_service import ListPublicOperatorsRequest
from .types.lva_service import ListPublicOperatorsResponse
from .types.lva_service import OperatorQuery
from .types.lva_service import ResolveOperatorInfoRequest
from .types.lva_service import ResolveOperatorInfoResponse
from .types.lva_service import UpdateAnalysisRequest
from .types.lva_service import UpdateOperatorRequest
from .types.lva_service import UpdateProcessRequest
from .types.lva_service import Registry
from .types.platform import AddApplicationStreamInputRequest
from .types.platform import AddApplicationStreamInputResponse
from .types.platform import AIEnabledDevicesInputConfig
from .types.platform import Application
from .types.platform import ApplicationConfigs
from .types.platform import ApplicationInstance
from .types.platform import ApplicationNodeAnnotation
from .types.platform import ApplicationStreamInput
from .types.platform import AutoscalingMetricSpec
from .types.platform import BigQueryConfig
from .types.platform import CreateApplicationInstancesRequest
from .types.platform import CreateApplicationInstancesResponse
from .types.platform import CreateApplicationRequest
from .types.platform import CreateDraftRequest
from .types.platform import CreateProcessorRequest
from .types.platform import CustomProcessorSourceInfo
from .types.platform import DedicatedResources
from .types.platform import DeleteApplicationInstancesRequest
from .types.platform import DeleteApplicationInstancesResponse
from .types.platform import DeleteApplicationRequest
from .types.platform import DeleteDraftRequest
from .types.platform import DeleteProcessorRequest
from .types.platform import DeployApplicationRequest
from .types.platform import DeployApplicationResponse
from .types.platform import Draft
from .types.platform import GcsOutputConfig
from .types.platform import GeneralObjectDetectionConfig
from .types.platform import GetApplicationRequest
from .types.platform import GetDraftRequest
from .types.platform import GetInstanceRequest
from .types.platform import GetProcessorRequest
from .types.platform import Instance
from .types.platform import ListApplicationsRequest
from .types.platform import ListApplicationsResponse
from .types.platform import ListDraftsRequest
from .types.platform import ListDraftsResponse
from .types.platform import ListInstancesRequest
from .types.platform import ListInstancesResponse
from .types.platform import ListPrebuiltProcessorsRequest
from .types.platform import ListPrebuiltProcessorsResponse
from .types.platform import ListProcessorsRequest
from .types.platform import ListProcessorsResponse
from .types.platform import MachineSpec
from .types.platform import MediaWarehouseConfig
from .types.platform import Node
from .types.platform import OccupancyCountConfig
from .types.platform import PersonalProtectiveEquipmentDetectionConfig
from .types.platform import PersonBlurConfig
from .types.platform import PersonVehicleDetectionConfig
from .types.platform import Processor
from .types.platform import ProcessorConfig
from .types.platform import ProcessorIOSpec
from .types.platform import ProductRecognizerConfig
from .types.platform import RemoveApplicationStreamInputRequest
from .types.platform import RemoveApplicationStreamInputResponse
from .types.platform import ResourceAnnotations
from .types.platform import StreamWithAnnotation
from .types.platform import TagParsingConfig
from .types.platform import TagRecognizerConfig
from .types.platform import UndeployApplicationRequest
from .types.platform import UndeployApplicationResponse
from .types.platform import UniversalInputConfig
from .types.platform import UpdateApplicationInstancesRequest
from .types.platform import UpdateApplicationInstancesResponse
from .types.platform import UpdateApplicationRequest
from .types.platform import UpdateApplicationStreamInputRequest
from .types.platform import UpdateApplicationStreamInputResponse
from .types.platform import UpdateDraftRequest
from .types.platform import UpdateProcessorRequest
from .types.platform import VertexAutoMLVideoConfig
from .types.platform import VertexAutoMLVisionConfig
from .types.platform import VertexCustomConfig
from .types.platform import VideoStreamInputConfig
from .types.platform import AcceleratorType
from .types.platform import DataType
from .types.platform import ModelType
from .types.streaming_resources import GstreamerBufferDescriptor
from .types.streaming_resources import Packet
from .types.streaming_resources import PacketHeader
from .types.streaming_resources import PacketType
from .types.streaming_resources import RawImageDescriptor
from .types.streaming_resources import SeriesMetadata
from .types.streaming_resources import ServerMetadata
from .types.streaming_service import AcquireLeaseRequest
from .types.streaming_service import CommitRequest
from .types.streaming_service import ControlledMode
from .types.streaming_service import EagerMode
from .types.streaming_service import EventUpdate
from .types.streaming_service import Lease
from .types.streaming_service import ReceiveEventsControlResponse
from .types.streaming_service import ReceiveEventsRequest
from .types.streaming_service import ReceiveEventsResponse
from .types.streaming_service import ReceivePacketsControlResponse
from .types.streaming_service import ReceivePacketsRequest
from .types.streaming_service import ReceivePacketsResponse
from .types.streaming_service import ReleaseLeaseRequest
from .types.streaming_service import ReleaseLeaseResponse
from .types.streaming_service import RenewLeaseRequest
from .types.streaming_service import RequestMetadata
from .types.streaming_service import SendPacketsRequest
from .types.streaming_service import SendPacketsResponse
from .types.streaming_service import LeaseType
from .types.streams_resources import Channel
from .types.streams_resources import Event
from .types.streams_resources import Series
from .types.streams_resources import Stream
from .types.streams_service import CreateClusterRequest
from .types.streams_service import CreateEventRequest
from .types.streams_service import CreateSeriesRequest
from .types.streams_service import CreateStreamRequest
from .types.streams_service import DeleteClusterRequest
from .types.streams_service import DeleteEventRequest
from .types.streams_service import DeleteSeriesRequest
from .types.streams_service import DeleteStreamRequest
from .types.streams_service import GenerateStreamHlsTokenRequest
from .types.streams_service import GenerateStreamHlsTokenResponse
from .types.streams_service import GetClusterRequest
from .types.streams_service import GetEventRequest
from .types.streams_service import GetSeriesRequest
from .types.streams_service import GetStreamRequest
from .types.streams_service import GetStreamThumbnailRequest
from .types.streams_service import GetStreamThumbnailResponse
from .types.streams_service import ListClustersRequest
from .types.streams_service import ListClustersResponse
from .types.streams_service import ListEventsRequest
from .types.streams_service import ListEventsResponse
from .types.streams_service import ListSeriesRequest
from .types.streams_service import ListSeriesResponse
from .types.streams_service import ListStreamsRequest
from .types.streams_service import ListStreamsResponse
from .types.streams_service import MaterializeChannelRequest
from .types.streams_service import UpdateClusterRequest
from .types.streams_service import UpdateEventRequest
from .types.streams_service import UpdateSeriesRequest
from .types.streams_service import UpdateStreamRequest
from .types.warehouse import AddCollectionItemRequest
from .types.warehouse import AddCollectionItemResponse
from .types.warehouse import AnalyzeAssetMetadata
from .types.warehouse import AnalyzeAssetRequest
from .types.warehouse import AnalyzeAssetResponse
from .types.warehouse import AnalyzeCorpusMetadata
from .types.warehouse import AnalyzeCorpusRequest
from .types.warehouse import AnalyzeCorpusResponse
from .types.warehouse import Annotation
from .types.warehouse import AnnotationCustomizedStruct
from .types.warehouse import AnnotationList
from .types.warehouse import AnnotationMatchingResult
from .types.warehouse import AnnotationValue
from .types.warehouse import Asset
from .types.warehouse import AssetSource
from .types.warehouse import BoolValue
from .types.warehouse import CircleArea
from .types.warehouse import ClipAssetRequest
from .types.warehouse import ClipAssetResponse
from .types.warehouse import Collection
from .types.warehouse import CollectionItem
from .types.warehouse import Corpus
from .types.warehouse import CreateAnnotationRequest
from .types.warehouse import CreateAssetRequest
from .types.warehouse import CreateCollectionMetadata
from .types.warehouse import CreateCollectionRequest
from .types.warehouse import CreateCorpusMetadata
from .types.warehouse import CreateCorpusRequest
from .types.warehouse import CreateDataSchemaRequest
from .types.warehouse import CreateIndexEndpointMetadata
from .types.warehouse import CreateIndexEndpointRequest
from .types.warehouse import CreateIndexMetadata
from .types.warehouse import CreateIndexRequest
from .types.warehouse import CreateSearchConfigRequest
from .types.warehouse import CreateSearchHypernymRequest
from .types.warehouse import Criteria
from .types.warehouse import DataSchema
from .types.warehouse import DataSchemaDetails
from .types.warehouse import DateTimeRange
from .types.warehouse import DateTimeRangeArray
from .types.warehouse import DeleteAnnotationRequest
from .types.warehouse import DeleteAssetMetadata
from .types.warehouse import DeleteAssetRequest
from .types.warehouse import DeleteCollectionMetadata
from .types.warehouse import DeleteCollectionRequest
from .types.warehouse import DeleteCorpusRequest
from .types.warehouse import DeleteDataSchemaRequest
from .types.warehouse import DeleteIndexEndpointMetadata
from .types.warehouse import DeleteIndexEndpointRequest
from .types.warehouse import DeleteIndexMetadata
from .types.warehouse import DeleteIndexRequest
from .types.warehouse import DeleteSearchConfigRequest
from .types.warehouse import DeleteSearchHypernymRequest
from .types.warehouse import DeployedIndex
from .types.warehouse import DeployedIndexReference
from .types.warehouse import DeployIndexMetadata
from .types.warehouse import DeployIndexRequest
from .types.warehouse import DeployIndexResponse
from .types.warehouse import FacetBucket
from .types.warehouse import FacetGroup
from .types.warehouse import FacetProperty
from .types.warehouse import FacetValue
from .types.warehouse import FloatRange
from .types.warehouse import FloatRangeArray
from .types.warehouse import GenerateHlsUriRequest
from .types.warehouse import GenerateHlsUriResponse
from .types.warehouse import GenerateRetrievalUrlRequest
from .types.warehouse import GenerateRetrievalUrlResponse
from .types.warehouse import GeoCoordinate
from .types.warehouse import GeoLocationArray
from .types.warehouse import GetAnnotationRequest
from .types.warehouse import GetAssetRequest
from .types.warehouse import GetCollectionRequest
from .types.warehouse import GetCorpusRequest
from .types.warehouse import GetDataSchemaRequest
from .types.warehouse import GetIndexEndpointRequest
from .types.warehouse import GetIndexRequest
from .types.warehouse import GetSearchConfigRequest
from .types.warehouse import GetSearchHypernymRequest
from .types.warehouse import ImageQuery
from .types.warehouse import ImportAssetsMetadata
from .types.warehouse import ImportAssetsRequest
from .types.warehouse import ImportAssetsResponse
from .types.warehouse import Index
from .types.warehouse import IndexAssetMetadata
from .types.warehouse import IndexAssetRequest
from .types.warehouse import IndexAssetResponse
from .types.warehouse import IndexedAsset
from .types.warehouse import IndexEndpoint
from .types.warehouse import IndexingStatus
from .types.warehouse import IngestAssetRequest
from .types.warehouse import IngestAssetResponse
from .types.warehouse import IntRange
from .types.warehouse import IntRangeArray
from .types.warehouse import ListAnnotationsRequest
from .types.warehouse import ListAnnotationsResponse
from .types.warehouse import ListAssetsRequest
from .types.warehouse import ListAssetsResponse
from .types.warehouse import ListCollectionsRequest
from .types.warehouse import ListCollectionsResponse
from .types.warehouse import ListCorporaRequest
from .types.warehouse import ListCorporaResponse
from .types.warehouse import ListDataSchemasRequest
from .types.warehouse import ListDataSchemasResponse
from .types.warehouse import ListIndexEndpointsRequest
from .types.warehouse import ListIndexEndpointsResponse
from .types.warehouse import ListIndexesRequest
from .types.warehouse import ListIndexesResponse
from .types.warehouse import ListSearchConfigsRequest
from .types.warehouse import ListSearchConfigsResponse
from .types.warehouse import ListSearchHypernymsRequest
from .types.warehouse import ListSearchHypernymsResponse
from .types.warehouse import Partition
from .types.warehouse import RemoveCollectionItemRequest
from .types.warehouse import RemoveCollectionItemResponse
from .types.warehouse import RemoveIndexAssetMetadata
from .types.warehouse import RemoveIndexAssetRequest
from .types.warehouse import RemoveIndexAssetResponse
from .types.warehouse import SchemaKeySortingStrategy
from .types.warehouse import SearchAssetsRequest
from .types.warehouse import SearchAssetsResponse
from .types.warehouse import SearchCapability
from .types.warehouse import SearchCapabilitySetting
from .types.warehouse import SearchConfig
from .types.warehouse import SearchCriteriaProperty
from .types.warehouse import SearchHypernym
from .types.warehouse import SearchIndexEndpointRequest
from .types.warehouse import SearchIndexEndpointResponse
from .types.warehouse import SearchResultItem
from .types.warehouse import StringArray
from .types.warehouse import UndeployIndexMetadata
from .types.warehouse import UndeployIndexRequest
from .types.warehouse import UndeployIndexResponse
from .types.warehouse import UpdateAnnotationRequest
from .types.warehouse import UpdateAssetRequest
from .types.warehouse import UpdateCollectionRequest
from .types.warehouse import UpdateCorpusRequest
from .types.warehouse import UpdateDataSchemaRequest
from .types.warehouse import UpdateIndexEndpointMetadata
from .types.warehouse import UpdateIndexEndpointRequest
from .types.warehouse import UpdateIndexMetadata
from .types.warehouse import UpdateIndexRequest
from .types.warehouse import UpdateSearchConfigRequest
from .types.warehouse import UpdateSearchHypernymRequest
from .types.warehouse import UploadAssetMetadata
from .types.warehouse import UploadAssetRequest
from .types.warehouse import UploadAssetResponse
from .types.warehouse import UserSpecifiedAnnotation
from .types.warehouse import ViewCollectionItemsRequest
from .types.warehouse import ViewCollectionItemsResponse
from .types.warehouse import ViewIndexedAssetsRequest
from .types.warehouse import ViewIndexedAssetsResponse
from .types.warehouse import FacetBucketType

__all__ = (
    'AppPlatformAsyncClient',
    'HealthCheckServiceAsyncClient',
    'LiveVideoAnalyticsAsyncClient',
    'StreamingServiceAsyncClient',
    'StreamsServiceAsyncClient',
    'WarehouseAsyncClient',
'AIEnabledDevicesInputConfig',
'AcceleratorType',
'AcquireLeaseRequest',
'AddApplicationStreamInputRequest',
'AddApplicationStreamInputResponse',
'AddCollectionItemRequest',
'AddCollectionItemResponse',
'Analysis',
'AnalysisDefinition',
'AnalyzeAssetMetadata',
'AnalyzeAssetRequest',
'AnalyzeAssetResponse',
'AnalyzeCorpusMetadata',
'AnalyzeCorpusRequest',
'AnalyzeCorpusResponse',
'AnalyzerDefinition',
'Annotation',
'AnnotationCustomizedStruct',
'AnnotationList',
'AnnotationMatchingResult',
'AnnotationValue',
'AppPlatformClient',
'AppPlatformCloudFunctionRequest',
'AppPlatformCloudFunctionResponse',
'AppPlatformEventBody',
'AppPlatformMetadata',
'Application',
'ApplicationConfigs',
'ApplicationInstance',
'ApplicationNodeAnnotation',
'ApplicationStreamInput',
'Asset',
'AssetSource',
'AttributeValue',
'AutoscalingMetricSpec',
'BatchRunProcessRequest',
'BatchRunProcessResponse',
'BigQueryConfig',
'BoolValue',
'Channel',
'CircleArea',
'ClassificationPredictionResult',
'ClipAssetRequest',
'ClipAssetResponse',
'Cluster',
'ClusterInfo',
'Collection',
'CollectionItem',
'CommitRequest',
'ControlledMode',
'Corpus',
'CreateAnalysisRequest',
'CreateAnnotationRequest',
'CreateApplicationInstancesRequest',
'CreateApplicationInstancesResponse',
'CreateApplicationRequest',
'CreateAssetRequest',
'CreateClusterRequest',
'CreateCollectionMetadata',
'CreateCollectionRequest',
'CreateCorpusMetadata',
'CreateCorpusRequest',
'CreateDataSchemaRequest',
'CreateDraftRequest',
'CreateEventRequest',
'CreateIndexEndpointMetadata',
'CreateIndexEndpointRequest',
'CreateIndexMetadata',
'CreateIndexRequest',
'CreateOperatorRequest',
'CreateProcessRequest',
'CreateProcessorRequest',
'CreateSearchConfigRequest',
'CreateSearchHypernymRequest',
'CreateSeriesRequest',
'CreateStreamRequest',
'Criteria',
'CustomProcessorSourceInfo',
'DataSchema',
'DataSchemaDetails',
'DataType',
'DateTimeRange',
'DateTimeRangeArray',
'DedicatedResources',
'DeleteAnalysisRequest',
'DeleteAnnotationRequest',
'DeleteApplicationInstancesRequest',
'DeleteApplicationInstancesResponse',
'DeleteApplicationRequest',
'DeleteAssetMetadata',
'DeleteAssetRequest',
'DeleteClusterRequest',
'DeleteCollectionMetadata',
'DeleteCollectionRequest',
'DeleteCorpusRequest',
'DeleteDataSchemaRequest',
'DeleteDraftRequest',
'DeleteEventRequest',
'DeleteIndexEndpointMetadata',
'DeleteIndexEndpointRequest',
'DeleteIndexMetadata',
'DeleteIndexRequest',
'DeleteOperatorRequest',
'DeleteProcessRequest',
'DeleteProcessorRequest',
'DeleteSearchConfigRequest',
'DeleteSearchHypernymRequest',
'DeleteSeriesRequest',
'DeleteStreamRequest',
'DeployApplicationRequest',
'DeployApplicationResponse',
'DeployIndexMetadata',
'DeployIndexRequest',
'DeployIndexResponse',
'DeployedIndex',
'DeployedIndexReference',
'Draft',
'EagerMode',
'Event',
'EventUpdate',
'FacetBucket',
'FacetBucketType',
'FacetGroup',
'FacetProperty',
'FacetValue',
'FloatRange',
'FloatRangeArray',
'GcsOutputConfig',
'GcsSource',
'GeneralObjectDetectionConfig',
'GenerateHlsUriRequest',
'GenerateHlsUriResponse',
'GenerateRetrievalUrlRequest',
'GenerateRetrievalUrlResponse',
'GenerateStreamHlsTokenRequest',
'GenerateStreamHlsTokenResponse',
'GeoCoordinate',
'GeoLocationArray',
'GetAnalysisRequest',
'GetAnnotationRequest',
'GetApplicationRequest',
'GetAssetRequest',
'GetClusterRequest',
'GetCollectionRequest',
'GetCorpusRequest',
'GetDataSchemaRequest',
'GetDraftRequest',
'GetEventRequest',
'GetIndexEndpointRequest',
'GetIndexRequest',
'GetInstanceRequest',
'GetOperatorRequest',
'GetProcessRequest',
'GetProcessorRequest',
'GetSearchConfigRequest',
'GetSearchHypernymRequest',
'GetSeriesRequest',
'GetStreamRequest',
'GetStreamThumbnailRequest',
'GetStreamThumbnailResponse',
'GstreamerBufferDescriptor',
'HealthCheckRequest',
'HealthCheckResponse',
'HealthCheckServiceClient',
'ImageObjectDetectionPredictionResult',
'ImageQuery',
'ImageSegmentationPredictionResult',
'ImportAssetsMetadata',
'ImportAssetsRequest',
'ImportAssetsResponse',
'Index',
'IndexAssetMetadata',
'IndexAssetRequest',
'IndexAssetResponse',
'IndexEndpoint',
'IndexedAsset',
'IndexingStatus',
'IngestAssetRequest',
'IngestAssetResponse',
'Instance',
'IntRange',
'IntRangeArray',
'Lease',
'LeaseType',
'ListAnalysesRequest',
'ListAnalysesResponse',
'ListAnnotationsRequest',
'ListAnnotationsResponse',
'ListApplicationsRequest',
'ListApplicationsResponse',
'ListAssetsRequest',
'ListAssetsResponse',
'ListClustersRequest',
'ListClustersResponse',
'ListCollectionsRequest',
'ListCollectionsResponse',
'ListCorporaRequest',
'ListCorporaResponse',
'ListDataSchemasRequest',
'ListDataSchemasResponse',
'ListDraftsRequest',
'ListDraftsResponse',
'ListEventsRequest',
'ListEventsResponse',
'ListIndexEndpointsRequest',
'ListIndexEndpointsResponse',
'ListIndexesRequest',
'ListIndexesResponse',
'ListInstancesRequest',
'ListInstancesResponse',
'ListOperatorsRequest',
'ListOperatorsResponse',
'ListPrebuiltProcessorsRequest',
'ListPrebuiltProcessorsResponse',
'ListProcessesRequest',
'ListProcessesResponse',
'ListProcessorsRequest',
'ListProcessorsResponse',
'ListPublicOperatorsRequest',
'ListPublicOperatorsResponse',
'ListSearchConfigsRequest',
'ListSearchConfigsResponse',
'ListSearchHypernymsRequest',
'ListSearchHypernymsResponse',
'ListSeriesRequest',
'ListSeriesResponse',
'ListStreamsRequest',
'ListStreamsResponse',
'LiveVideoAnalyticsClient',
'MachineSpec',
'MaterializeChannelRequest',
'MediaWarehouseConfig',
'ModelType',
'Node',
'NormalizedPolygon',
'NormalizedPolyline',
'NormalizedVertex',
'ObjectDetectionPredictionResult',
'OccupancyCountConfig',
'OccupancyCountingPredictionResult',
'OperationMetadata',
'Operator',
'OperatorDefinition',
'OperatorQuery',
'Packet',
'PacketHeader',
'PacketType',
'Partition',
'PersonBlurConfig',
'PersonVehicleDetectionConfig',
'PersonalProtectiveEquipmentDetectionConfig',
'PersonalProtectiveEquipmentDetectionOutput',
'Process',
'Processor',
'ProcessorConfig',
'ProcessorIOSpec',
'ProductRecognizerConfig',
'RawImageDescriptor',
'ReceiveEventsControlResponse',
'ReceiveEventsRequest',
'ReceiveEventsResponse',
'ReceivePacketsControlResponse',
'ReceivePacketsRequest',
'ReceivePacketsResponse',
'Registry',
'ReleaseLeaseRequest',
'ReleaseLeaseResponse',
'RemoveApplicationStreamInputRequest',
'RemoveApplicationStreamInputResponse',
'RemoveCollectionItemRequest',
'RemoveCollectionItemResponse',
'RemoveIndexAssetMetadata',
'RemoveIndexAssetRequest',
'RemoveIndexAssetResponse',
'RenewLeaseRequest',
'RequestMetadata',
'ResolveOperatorInfoRequest',
'ResolveOperatorInfoResponse',
'ResourceAnnotations',
'ResourceSpecification',
'RunMode',
'RunStatus',
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
'SendPacketsRequest',
'SendPacketsResponse',
'Series',
'SeriesMetadata',
'ServerMetadata',
'Stream',
'StreamAnnotation',
'StreamAnnotationType',
'StreamAnnotations',
'StreamWithAnnotation',
'StreamingServiceClient',
'StreamsServiceClient',
'StringArray',
'TagParsingConfig',
'TagRecognizerConfig',
'UndeployApplicationRequest',
'UndeployApplicationResponse',
'UndeployIndexMetadata',
'UndeployIndexRequest',
'UndeployIndexResponse',
'UniversalInputConfig',
'UpdateAnalysisRequest',
'UpdateAnnotationRequest',
'UpdateApplicationInstancesRequest',
'UpdateApplicationInstancesResponse',
'UpdateApplicationRequest',
'UpdateApplicationStreamInputRequest',
'UpdateApplicationStreamInputResponse',
'UpdateAssetRequest',
'UpdateClusterRequest',
'UpdateCollectionRequest',
'UpdateCorpusRequest',
'UpdateDataSchemaRequest',
'UpdateDraftRequest',
'UpdateEventRequest',
'UpdateIndexEndpointMetadata',
'UpdateIndexEndpointRequest',
'UpdateIndexMetadata',
'UpdateIndexRequest',
'UpdateOperatorRequest',
'UpdateProcessRequest',
'UpdateProcessorRequest',
'UpdateSearchConfigRequest',
'UpdateSearchHypernymRequest',
'UpdateSeriesRequest',
'UpdateStreamRequest',
'UploadAssetMetadata',
'UploadAssetRequest',
'UploadAssetResponse',
'UserSpecifiedAnnotation',
'VertexAutoMLVideoConfig',
'VertexAutoMLVisionConfig',
'VertexCustomConfig',
'VideoActionRecognitionPredictionResult',
'VideoClassificationPredictionResult',
'VideoObjectTrackingPredictionResult',
'VideoStreamInputConfig',
'ViewCollectionItemsRequest',
'ViewCollectionItemsResponse',
'ViewIndexedAssetsRequest',
'ViewIndexedAssetsResponse',
'WarehouseClient',
)
