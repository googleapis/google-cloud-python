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
from google.cloud.vision import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.vision_v1p2beta1.services.image_annotator.client import ImageAnnotatorClient
from google.cloud.vision_v1p2beta1.services.image_annotator.async_client import ImageAnnotatorAsyncClient

from google.cloud.vision_v1p2beta1.types.geometry import BoundingPoly
from google.cloud.vision_v1p2beta1.types.geometry import NormalizedVertex
from google.cloud.vision_v1p2beta1.types.geometry import Position
from google.cloud.vision_v1p2beta1.types.geometry import Vertex
from google.cloud.vision_v1p2beta1.types.image_annotator import AnnotateFileResponse
from google.cloud.vision_v1p2beta1.types.image_annotator import AnnotateImageRequest
from google.cloud.vision_v1p2beta1.types.image_annotator import AnnotateImageResponse
from google.cloud.vision_v1p2beta1.types.image_annotator import AsyncAnnotateFileRequest
from google.cloud.vision_v1p2beta1.types.image_annotator import AsyncAnnotateFileResponse
from google.cloud.vision_v1p2beta1.types.image_annotator import AsyncBatchAnnotateFilesRequest
from google.cloud.vision_v1p2beta1.types.image_annotator import AsyncBatchAnnotateFilesResponse
from google.cloud.vision_v1p2beta1.types.image_annotator import BatchAnnotateImagesRequest
from google.cloud.vision_v1p2beta1.types.image_annotator import BatchAnnotateImagesResponse
from google.cloud.vision_v1p2beta1.types.image_annotator import ColorInfo
from google.cloud.vision_v1p2beta1.types.image_annotator import CropHint
from google.cloud.vision_v1p2beta1.types.image_annotator import CropHintsAnnotation
from google.cloud.vision_v1p2beta1.types.image_annotator import CropHintsParams
from google.cloud.vision_v1p2beta1.types.image_annotator import DominantColorsAnnotation
from google.cloud.vision_v1p2beta1.types.image_annotator import EntityAnnotation
from google.cloud.vision_v1p2beta1.types.image_annotator import FaceAnnotation
from google.cloud.vision_v1p2beta1.types.image_annotator import Feature
from google.cloud.vision_v1p2beta1.types.image_annotator import GcsDestination
from google.cloud.vision_v1p2beta1.types.image_annotator import GcsSource
from google.cloud.vision_v1p2beta1.types.image_annotator import Image
from google.cloud.vision_v1p2beta1.types.image_annotator import ImageAnnotationContext
from google.cloud.vision_v1p2beta1.types.image_annotator import ImageContext
from google.cloud.vision_v1p2beta1.types.image_annotator import ImageProperties
from google.cloud.vision_v1p2beta1.types.image_annotator import ImageSource
from google.cloud.vision_v1p2beta1.types.image_annotator import InputConfig
from google.cloud.vision_v1p2beta1.types.image_annotator import LatLongRect
from google.cloud.vision_v1p2beta1.types.image_annotator import LocationInfo
from google.cloud.vision_v1p2beta1.types.image_annotator import OperationMetadata
from google.cloud.vision_v1p2beta1.types.image_annotator import OutputConfig
from google.cloud.vision_v1p2beta1.types.image_annotator import Property
from google.cloud.vision_v1p2beta1.types.image_annotator import SafeSearchAnnotation
from google.cloud.vision_v1p2beta1.types.image_annotator import TextDetectionParams
from google.cloud.vision_v1p2beta1.types.image_annotator import WebDetectionParams
from google.cloud.vision_v1p2beta1.types.image_annotator import Likelihood
from google.cloud.vision_v1p2beta1.types.text_annotation import Block
from google.cloud.vision_v1p2beta1.types.text_annotation import Page
from google.cloud.vision_v1p2beta1.types.text_annotation import Paragraph
from google.cloud.vision_v1p2beta1.types.text_annotation import Symbol
from google.cloud.vision_v1p2beta1.types.text_annotation import TextAnnotation
from google.cloud.vision_v1p2beta1.types.text_annotation import Word
from google.cloud.vision_v1p2beta1.types.web_detection import WebDetection

__all__ = ('ImageAnnotatorClient',
    'ImageAnnotatorAsyncClient',
    'BoundingPoly',
    'NormalizedVertex',
    'Position',
    'Vertex',
    'AnnotateFileResponse',
    'AnnotateImageRequest',
    'AnnotateImageResponse',
    'AsyncAnnotateFileRequest',
    'AsyncAnnotateFileResponse',
    'AsyncBatchAnnotateFilesRequest',
    'AsyncBatchAnnotateFilesResponse',
    'BatchAnnotateImagesRequest',
    'BatchAnnotateImagesResponse',
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
    'ImageContext',
    'ImageProperties',
    'ImageSource',
    'InputConfig',
    'LatLongRect',
    'LocationInfo',
    'OperationMetadata',
    'OutputConfig',
    'Property',
    'SafeSearchAnnotation',
    'TextDetectionParams',
    'WebDetectionParams',
    'Likelihood',
    'Block',
    'Page',
    'Paragraph',
    'Symbol',
    'TextAnnotation',
    'Word',
    'WebDetection',
)
