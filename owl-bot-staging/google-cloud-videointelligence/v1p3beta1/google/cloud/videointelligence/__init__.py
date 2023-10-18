# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.videointelligence import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.videointelligence_v1p3beta1.services.streaming_video_intelligence_service.client import StreamingVideoIntelligenceServiceClient
from google.cloud.videointelligence_v1p3beta1.services.streaming_video_intelligence_service.async_client import StreamingVideoIntelligenceServiceAsyncClient
from google.cloud.videointelligence_v1p3beta1.services.video_intelligence_service.client import VideoIntelligenceServiceClient
from google.cloud.videointelligence_v1p3beta1.services.video_intelligence_service.async_client import VideoIntelligenceServiceAsyncClient

from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import AnnotateVideoProgress
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import AnnotateVideoRequest
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import AnnotateVideoResponse
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import Celebrity
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import CelebrityRecognitionAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import CelebrityTrack
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import DetectedAttribute
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import DetectedLandmark
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import Entity
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ExplicitContentAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ExplicitContentDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ExplicitContentFrame
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import FaceDetectionAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import FaceDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LabelAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LabelDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LabelFrame
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LabelSegment
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LogoRecognitionAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import NormalizedBoundingBox
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import NormalizedBoundingPoly
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import NormalizedVertex
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ObjectTrackingAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ObjectTrackingConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ObjectTrackingFrame
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import PersonDetectionAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import PersonDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import ShotChangeDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import SpeechContext
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import SpeechRecognitionAlternative
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import SpeechTranscription
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import SpeechTranscriptionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingAnnotateVideoRequest
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingAnnotateVideoResponse
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingAutomlActionRecognitionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingAutomlClassificationConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingAutomlObjectTrackingConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingExplicitContentDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingLabelDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingObjectTrackingConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingShotChangeDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingStorageConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingVideoAnnotationResults
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingVideoConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import TextAnnotation
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import TextDetectionConfig
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import TextFrame
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import TextSegment
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import TimestampedObject
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import Track
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import VideoAnnotationProgress
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import VideoAnnotationResults
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import VideoContext
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import VideoSegment
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import WordInfo
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import Feature
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import LabelDetectionMode
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import Likelihood
from google.cloud.videointelligence_v1p3beta1.types.video_intelligence import StreamingFeature

__all__ = ('StreamingVideoIntelligenceServiceClient',
    'StreamingVideoIntelligenceServiceAsyncClient',
    'VideoIntelligenceServiceClient',
    'VideoIntelligenceServiceAsyncClient',
    'AnnotateVideoProgress',
    'AnnotateVideoRequest',
    'AnnotateVideoResponse',
    'Celebrity',
    'CelebrityRecognitionAnnotation',
    'CelebrityTrack',
    'DetectedAttribute',
    'DetectedLandmark',
    'Entity',
    'ExplicitContentAnnotation',
    'ExplicitContentDetectionConfig',
    'ExplicitContentFrame',
    'FaceDetectionAnnotation',
    'FaceDetectionConfig',
    'LabelAnnotation',
    'LabelDetectionConfig',
    'LabelFrame',
    'LabelSegment',
    'LogoRecognitionAnnotation',
    'NormalizedBoundingBox',
    'NormalizedBoundingPoly',
    'NormalizedVertex',
    'ObjectTrackingAnnotation',
    'ObjectTrackingConfig',
    'ObjectTrackingFrame',
    'PersonDetectionAnnotation',
    'PersonDetectionConfig',
    'ShotChangeDetectionConfig',
    'SpeechContext',
    'SpeechRecognitionAlternative',
    'SpeechTranscription',
    'SpeechTranscriptionConfig',
    'StreamingAnnotateVideoRequest',
    'StreamingAnnotateVideoResponse',
    'StreamingAutomlActionRecognitionConfig',
    'StreamingAutomlClassificationConfig',
    'StreamingAutomlObjectTrackingConfig',
    'StreamingExplicitContentDetectionConfig',
    'StreamingLabelDetectionConfig',
    'StreamingObjectTrackingConfig',
    'StreamingShotChangeDetectionConfig',
    'StreamingStorageConfig',
    'StreamingVideoAnnotationResults',
    'StreamingVideoConfig',
    'TextAnnotation',
    'TextDetectionConfig',
    'TextFrame',
    'TextSegment',
    'TimestampedObject',
    'Track',
    'VideoAnnotationProgress',
    'VideoAnnotationResults',
    'VideoContext',
    'VideoSegment',
    'WordInfo',
    'Feature',
    'LabelDetectionMode',
    'Likelihood',
    'StreamingFeature',
)
