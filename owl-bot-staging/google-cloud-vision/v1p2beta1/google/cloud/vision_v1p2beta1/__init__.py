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
from google.cloud.vision_v1p2beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.image_annotator import ImageAnnotatorClient
from .services.image_annotator import ImageAnnotatorAsyncClient

from .types.geometry import BoundingPoly
from .types.geometry import NormalizedVertex
from .types.geometry import Position
from .types.geometry import Vertex
from .types.image_annotator import AnnotateFileResponse
from .types.image_annotator import AnnotateImageRequest
from .types.image_annotator import AnnotateImageResponse
from .types.image_annotator import AsyncAnnotateFileRequest
from .types.image_annotator import AsyncAnnotateFileResponse
from .types.image_annotator import AsyncBatchAnnotateFilesRequest
from .types.image_annotator import AsyncBatchAnnotateFilesResponse
from .types.image_annotator import BatchAnnotateImagesRequest
from .types.image_annotator import BatchAnnotateImagesResponse
from .types.image_annotator import ColorInfo
from .types.image_annotator import CropHint
from .types.image_annotator import CropHintsAnnotation
from .types.image_annotator import CropHintsParams
from .types.image_annotator import DominantColorsAnnotation
from .types.image_annotator import EntityAnnotation
from .types.image_annotator import FaceAnnotation
from .types.image_annotator import Feature
from .types.image_annotator import GcsDestination
from .types.image_annotator import GcsSource
from .types.image_annotator import Image
from .types.image_annotator import ImageAnnotationContext
from .types.image_annotator import ImageContext
from .types.image_annotator import ImageProperties
from .types.image_annotator import ImageSource
from .types.image_annotator import InputConfig
from .types.image_annotator import LatLongRect
from .types.image_annotator import LocationInfo
from .types.image_annotator import OperationMetadata
from .types.image_annotator import OutputConfig
from .types.image_annotator import Property
from .types.image_annotator import SafeSearchAnnotation
from .types.image_annotator import TextDetectionParams
from .types.image_annotator import WebDetectionParams
from .types.image_annotator import Likelihood
from .types.text_annotation import Block
from .types.text_annotation import Page
from .types.text_annotation import Paragraph
from .types.text_annotation import Symbol
from .types.text_annotation import TextAnnotation
from .types.text_annotation import Word
from .types.web_detection import WebDetection

__all__ = (
    'ImageAnnotatorAsyncClient',
'AnnotateFileResponse',
'AnnotateImageRequest',
'AnnotateImageResponse',
'AsyncAnnotateFileRequest',
'AsyncAnnotateFileResponse',
'AsyncBatchAnnotateFilesRequest',
'AsyncBatchAnnotateFilesResponse',
'BatchAnnotateImagesRequest',
'BatchAnnotateImagesResponse',
'Block',
'BoundingPoly',
'ColorInfo',
'CropHint',
'CropHintsAnnotation',
'CropHintsParams',
'DominantColorsAnnotation',
'EntityAnnotation',
'FaceAnnotation',
'Feature',
'GcsDestination',
'GcsSource',
'Image',
'ImageAnnotationContext',
'ImageAnnotatorClient',
'ImageContext',
'ImageProperties',
'ImageSource',
'InputConfig',
'LatLongRect',
'Likelihood',
'LocationInfo',
'NormalizedVertex',
'OperationMetadata',
'OutputConfig',
'Page',
'Paragraph',
'Position',
'Property',
'SafeSearchAnnotation',
'Symbol',
'TextAnnotation',
'TextDetectionParams',
'Vertex',
'WebDetection',
'WebDetectionParams',
'Word',
)
