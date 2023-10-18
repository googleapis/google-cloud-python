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


from google.cloud.videointelligence_v1beta2.services.video_intelligence_service.client import VideoIntelligenceServiceClient
from google.cloud.videointelligence_v1beta2.services.video_intelligence_service.async_client import VideoIntelligenceServiceAsyncClient

from google.cloud.videointelligence_v1beta2.types.video_intelligence import AnnotateVideoProgress
from google.cloud.videointelligence_v1beta2.types.video_intelligence import AnnotateVideoRequest
from google.cloud.videointelligence_v1beta2.types.video_intelligence import AnnotateVideoResponse
from google.cloud.videointelligence_v1beta2.types.video_intelligence import Entity
from google.cloud.videointelligence_v1beta2.types.video_intelligence import ExplicitContentAnnotation
from google.cloud.videointelligence_v1beta2.types.video_intelligence import ExplicitContentDetectionConfig
from google.cloud.videointelligence_v1beta2.types.video_intelligence import ExplicitContentFrame
from google.cloud.videointelligence_v1beta2.types.video_intelligence import FaceAnnotation
from google.cloud.videointelligence_v1beta2.types.video_intelligence import FaceDetectionConfig
from google.cloud.videointelligence_v1beta2.types.video_intelligence import FaceFrame
from google.cloud.videointelligence_v1beta2.types.video_intelligence import FaceSegment
from google.cloud.videointelligence_v1beta2.types.video_intelligence import LabelAnnotation
from google.cloud.videointelligence_v1beta2.types.video_intelligence import LabelDetectionConfig
from google.cloud.videointelligence_v1beta2.types.video_intelligence import LabelFrame
from google.cloud.videointelligence_v1beta2.types.video_intelligence import LabelSegment
from google.cloud.videointelligence_v1beta2.types.video_intelligence import NormalizedBoundingBox
from google.cloud.videointelligence_v1beta2.types.video_intelligence import ShotChangeDetectionConfig
from google.cloud.videointelligence_v1beta2.types.video_intelligence import VideoAnnotationProgress
from google.cloud.videointelligence_v1beta2.types.video_intelligence import VideoAnnotationResults
from google.cloud.videointelligence_v1beta2.types.video_intelligence import VideoContext
from google.cloud.videointelligence_v1beta2.types.video_intelligence import VideoSegment
from google.cloud.videointelligence_v1beta2.types.video_intelligence import Feature
from google.cloud.videointelligence_v1beta2.types.video_intelligence import LabelDetectionMode
from google.cloud.videointelligence_v1beta2.types.video_intelligence import Likelihood

__all__ = ('VideoIntelligenceServiceClient',
    'VideoIntelligenceServiceAsyncClient',
    'AnnotateVideoProgress',
    'AnnotateVideoRequest',
    'AnnotateVideoResponse',
    'Entity',
    'ExplicitContentAnnotation',
    'ExplicitContentDetectionConfig',
    'ExplicitContentFrame',
    'FaceAnnotation',
    'FaceDetectionConfig',
    'FaceFrame',
    'FaceSegment',
    'LabelAnnotation',
    'LabelDetectionConfig',
    'LabelFrame',
    'LabelSegment',
    'NormalizedBoundingBox',
    'ShotChangeDetectionConfig',
    'VideoAnnotationProgress',
    'VideoAnnotationResults',
    'VideoContext',
    'VideoSegment',
    'Feature',
    'LabelDetectionMode',
    'Likelihood',
)
