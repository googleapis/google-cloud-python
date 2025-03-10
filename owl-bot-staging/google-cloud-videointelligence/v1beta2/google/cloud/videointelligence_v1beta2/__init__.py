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
from google.cloud.videointelligence_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.video_intelligence_service import VideoIntelligenceServiceClient
from .services.video_intelligence_service import VideoIntelligenceServiceAsyncClient

from .types.video_intelligence import AnnotateVideoProgress
from .types.video_intelligence import AnnotateVideoRequest
from .types.video_intelligence import AnnotateVideoResponse
from .types.video_intelligence import Entity
from .types.video_intelligence import ExplicitContentAnnotation
from .types.video_intelligence import ExplicitContentDetectionConfig
from .types.video_intelligence import ExplicitContentFrame
from .types.video_intelligence import FaceAnnotation
from .types.video_intelligence import FaceDetectionConfig
from .types.video_intelligence import FaceFrame
from .types.video_intelligence import FaceSegment
from .types.video_intelligence import LabelAnnotation
from .types.video_intelligence import LabelDetectionConfig
from .types.video_intelligence import LabelFrame
from .types.video_intelligence import LabelSegment
from .types.video_intelligence import NormalizedBoundingBox
from .types.video_intelligence import ShotChangeDetectionConfig
from .types.video_intelligence import VideoAnnotationProgress
from .types.video_intelligence import VideoAnnotationResults
from .types.video_intelligence import VideoContext
from .types.video_intelligence import VideoSegment
from .types.video_intelligence import Feature
from .types.video_intelligence import LabelDetectionMode
from .types.video_intelligence import Likelihood

__all__ = (
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
'Feature',
'LabelAnnotation',
'LabelDetectionConfig',
'LabelDetectionMode',
'LabelFrame',
'LabelSegment',
'Likelihood',
'NormalizedBoundingBox',
'ShotChangeDetectionConfig',
'VideoAnnotationProgress',
'VideoAnnotationResults',
'VideoContext',
'VideoIntelligenceServiceClient',
'VideoSegment',
)
