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

from google.cloud.vision_v1.services.image_annotator.async_client import (
    ImageAnnotatorAsyncClient,
)
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1.services.product_search.async_client import (
    ProductSearchAsyncClient,
)
from google.cloud.vision_v1.services.product_search.client import ProductSearchClient
from google.cloud.vision_v1.types.geometry import BoundingPoly
from google.cloud.vision_v1.types.geometry import NormalizedVertex
from google.cloud.vision_v1.types.geometry import Position
from google.cloud.vision_v1.types.geometry import Vertex
from google.cloud.vision_v1.types.image_annotator import AnnotateFileRequest
from google.cloud.vision_v1.types.image_annotator import AnnotateFileResponse
from google.cloud.vision_v1.types.image_annotator import AnnotateImageRequest
from google.cloud.vision_v1.types.image_annotator import AnnotateImageResponse
from google.cloud.vision_v1.types.image_annotator import AsyncAnnotateFileRequest
from google.cloud.vision_v1.types.image_annotator import AsyncAnnotateFileResponse
from google.cloud.vision_v1.types.image_annotator import AsyncBatchAnnotateFilesRequest
from google.cloud.vision_v1.types.image_annotator import AsyncBatchAnnotateFilesResponse
from google.cloud.vision_v1.types.image_annotator import AsyncBatchAnnotateImagesRequest
from google.cloud.vision_v1.types.image_annotator import (
    AsyncBatchAnnotateImagesResponse,
)
from google.cloud.vision_v1.types.image_annotator import BatchAnnotateFilesRequest
from google.cloud.vision_v1.types.image_annotator import BatchAnnotateFilesResponse
from google.cloud.vision_v1.types.image_annotator import BatchAnnotateImagesRequest
from google.cloud.vision_v1.types.image_annotator import BatchAnnotateImagesResponse
from google.cloud.vision_v1.types.image_annotator import ColorInfo
from google.cloud.vision_v1.types.image_annotator import CropHint
from google.cloud.vision_v1.types.image_annotator import CropHintsAnnotation
from google.cloud.vision_v1.types.image_annotator import CropHintsParams
from google.cloud.vision_v1.types.image_annotator import DominantColorsAnnotation
from google.cloud.vision_v1.types.image_annotator import EntityAnnotation
from google.cloud.vision_v1.types.image_annotator import FaceAnnotation
from google.cloud.vision_v1.types.image_annotator import Feature
from google.cloud.vision_v1.types.image_annotator import GcsDestination
from google.cloud.vision_v1.types.image_annotator import GcsSource
from google.cloud.vision_v1.types.image_annotator import Image
from google.cloud.vision_v1.types.image_annotator import ImageAnnotationContext
from google.cloud.vision_v1.types.image_annotator import ImageContext
from google.cloud.vision_v1.types.image_annotator import ImageProperties
from google.cloud.vision_v1.types.image_annotator import ImageSource
from google.cloud.vision_v1.types.image_annotator import InputConfig
from google.cloud.vision_v1.types.image_annotator import LatLongRect
from google.cloud.vision_v1.types.image_annotator import Likelihood
from google.cloud.vision_v1.types.image_annotator import LocalizedObjectAnnotation
from google.cloud.vision_v1.types.image_annotator import LocationInfo
from google.cloud.vision_v1.types.image_annotator import OperationMetadata
from google.cloud.vision_v1.types.image_annotator import OutputConfig
from google.cloud.vision_v1.types.image_annotator import Property
from google.cloud.vision_v1.types.image_annotator import SafeSearchAnnotation
from google.cloud.vision_v1.types.image_annotator import TextDetectionParams
from google.cloud.vision_v1.types.image_annotator import WebDetectionParams
from google.cloud.vision_v1.types.product_search import ProductSearchParams
from google.cloud.vision_v1.types.product_search import ProductSearchResults
from google.cloud.vision_v1.types.product_search_service import (
    AddProductToProductSetRequest,
)
from google.cloud.vision_v1.types.product_search_service import BatchOperationMetadata
from google.cloud.vision_v1.types.product_search_service import CreateProductRequest
from google.cloud.vision_v1.types.product_search_service import CreateProductSetRequest
from google.cloud.vision_v1.types.product_search_service import (
    CreateReferenceImageRequest,
)
from google.cloud.vision_v1.types.product_search_service import DeleteProductRequest
from google.cloud.vision_v1.types.product_search_service import DeleteProductSetRequest
from google.cloud.vision_v1.types.product_search_service import (
    DeleteReferenceImageRequest,
)
from google.cloud.vision_v1.types.product_search_service import GetProductRequest
from google.cloud.vision_v1.types.product_search_service import GetProductSetRequest
from google.cloud.vision_v1.types.product_search_service import GetReferenceImageRequest
from google.cloud.vision_v1.types.product_search_service import (
    ImportProductSetsGcsSource,
)
from google.cloud.vision_v1.types.product_search_service import (
    ImportProductSetsInputConfig,
)
from google.cloud.vision_v1.types.product_search_service import ImportProductSetsRequest
from google.cloud.vision_v1.types.product_search_service import (
    ImportProductSetsResponse,
)
from google.cloud.vision_v1.types.product_search_service import ListProductSetsRequest
from google.cloud.vision_v1.types.product_search_service import ListProductSetsResponse
from google.cloud.vision_v1.types.product_search_service import (
    ListProductsInProductSetRequest,
)
from google.cloud.vision_v1.types.product_search_service import (
    ListProductsInProductSetResponse,
)
from google.cloud.vision_v1.types.product_search_service import ListProductsRequest
from google.cloud.vision_v1.types.product_search_service import ListProductsResponse
from google.cloud.vision_v1.types.product_search_service import (
    ListReferenceImagesRequest,
)
from google.cloud.vision_v1.types.product_search_service import (
    ListReferenceImagesResponse,
)
from google.cloud.vision_v1.types.product_search_service import Product
from google.cloud.vision_v1.types.product_search_service import ProductSet
from google.cloud.vision_v1.types.product_search_service import ProductSetPurgeConfig
from google.cloud.vision_v1.types.product_search_service import PurgeProductsRequest
from google.cloud.vision_v1.types.product_search_service import ReferenceImage
from google.cloud.vision_v1.types.product_search_service import (
    RemoveProductFromProductSetRequest,
)
from google.cloud.vision_v1.types.product_search_service import UpdateProductRequest
from google.cloud.vision_v1.types.product_search_service import UpdateProductSetRequest
from google.cloud.vision_v1.types.text_annotation import Block
from google.cloud.vision_v1.types.text_annotation import Page
from google.cloud.vision_v1.types.text_annotation import Paragraph
from google.cloud.vision_v1.types.text_annotation import Symbol
from google.cloud.vision_v1.types.text_annotation import TextAnnotation
from google.cloud.vision_v1.types.text_annotation import Word
from google.cloud.vision_v1.types.web_detection import WebDetection

__all__ = (
    "AddProductToProductSetRequest",
    "AnnotateFileRequest",
    "AnnotateFileResponse",
    "AnnotateImageRequest",
    "AnnotateImageResponse",
    "AsyncAnnotateFileRequest",
    "AsyncAnnotateFileResponse",
    "AsyncBatchAnnotateFilesRequest",
    "AsyncBatchAnnotateFilesResponse",
    "AsyncBatchAnnotateImagesRequest",
    "AsyncBatchAnnotateImagesResponse",
    "BatchAnnotateFilesRequest",
    "BatchAnnotateFilesResponse",
    "BatchAnnotateImagesRequest",
    "BatchAnnotateImagesResponse",
    "BatchOperationMetadata",
    "Block",
    "BoundingPoly",
    "ColorInfo",
    "CreateProductRequest",
    "CreateProductSetRequest",
    "CreateReferenceImageRequest",
    "CropHint",
    "CropHintsAnnotation",
    "CropHintsParams",
    "DeleteProductRequest",
    "DeleteProductSetRequest",
    "DeleteReferenceImageRequest",
    "DominantColorsAnnotation",
    "EntityAnnotation",
    "FaceAnnotation",
    "Feature",
    "GcsDestination",
    "GcsSource",
    "GetProductRequest",
    "GetProductSetRequest",
    "GetReferenceImageRequest",
    "Image",
    "ImageAnnotationContext",
    "ImageAnnotatorAsyncClient",
    "ImageAnnotatorClient",
    "ImageContext",
    "ImageProperties",
    "ImageSource",
    "ImportProductSetsGcsSource",
    "ImportProductSetsInputConfig",
    "ImportProductSetsRequest",
    "ImportProductSetsResponse",
    "InputConfig",
    "LatLongRect",
    "Likelihood",
    "ListProductSetsRequest",
    "ListProductSetsResponse",
    "ListProductsInProductSetRequest",
    "ListProductsInProductSetResponse",
    "ListProductsRequest",
    "ListProductsResponse",
    "ListReferenceImagesRequest",
    "ListReferenceImagesResponse",
    "LocalizedObjectAnnotation",
    "LocationInfo",
    "NormalizedVertex",
    "OperationMetadata",
    "OutputConfig",
    "Page",
    "Paragraph",
    "Position",
    "Product",
    "ProductSearchAsyncClient",
    "ProductSearchClient",
    "ProductSearchParams",
    "ProductSearchResults",
    "ProductSet",
    "ProductSetPurgeConfig",
    "Property",
    "PurgeProductsRequest",
    "ReferenceImage",
    "RemoveProductFromProductSetRequest",
    "SafeSearchAnnotation",
    "Symbol",
    "TextAnnotation",
    "TextDetectionParams",
    "UpdateProductRequest",
    "UpdateProductSetRequest",
    "Vertex",
    "WebDetection",
    "WebDetectionParams",
    "Word",
)
