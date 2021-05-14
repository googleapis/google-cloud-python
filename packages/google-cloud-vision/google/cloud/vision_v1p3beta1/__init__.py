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

from google.cloud.vision_helpers.decorators import add_single_feature_methods
from google.cloud.vision_helpers import VisionHelpers

from .services.image_annotator import ImageAnnotatorClient as IacImageAnnotatorClient
from .services.image_annotator import ImageAnnotatorAsyncClient
from .services.product_search import ProductSearchClient
from .services.product_search import ProductSearchAsyncClient

from .types.geometry import BoundingPoly
from .types.geometry import NormalizedBoundingPoly
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
from .types.image_annotator import LocalizedObjectAnnotation
from .types.image_annotator import LocationInfo
from .types.image_annotator import OperationMetadata
from .types.image_annotator import OutputConfig
from .types.image_annotator import Property
from .types.image_annotator import SafeSearchAnnotation
from .types.image_annotator import TextDetectionParams
from .types.image_annotator import WebDetectionParams
from .types.image_annotator import Likelihood
from .types.product_search import ProductSearchParams
from .types.product_search import ProductSearchResults
from .types.product_search import ProductSearchCategory
from .types.product_search import ProductSearchResultsView
from .types.product_search_service import AddProductToProductSetRequest
from .types.product_search_service import BatchOperationMetadata
from .types.product_search_service import CreateProductRequest
from .types.product_search_service import CreateProductSetRequest
from .types.product_search_service import CreateReferenceImageRequest
from .types.product_search_service import DeleteProductRequest
from .types.product_search_service import DeleteProductSetRequest
from .types.product_search_service import DeleteReferenceImageRequest
from .types.product_search_service import GetProductRequest
from .types.product_search_service import GetProductSetRequest
from .types.product_search_service import GetReferenceImageRequest
from .types.product_search_service import ImportProductSetsGcsSource
from .types.product_search_service import ImportProductSetsInputConfig
from .types.product_search_service import ImportProductSetsRequest
from .types.product_search_service import ImportProductSetsResponse
from .types.product_search_service import ListProductSetsRequest
from .types.product_search_service import ListProductSetsResponse
from .types.product_search_service import ListProductsInProductSetRequest
from .types.product_search_service import ListProductsInProductSetResponse
from .types.product_search_service import ListProductsRequest
from .types.product_search_service import ListProductsResponse
from .types.product_search_service import ListReferenceImagesRequest
from .types.product_search_service import ListReferenceImagesResponse
from .types.product_search_service import Product
from .types.product_search_service import ProductSet
from .types.product_search_service import ReferenceImage
from .types.product_search_service import RemoveProductFromProductSetRequest
from .types.product_search_service import UpdateProductRequest
from .types.product_search_service import UpdateProductSetRequest
from .types.text_annotation import Block
from .types.text_annotation import Page
from .types.text_annotation import Paragraph
from .types.text_annotation import Symbol
from .types.text_annotation import TextAnnotation
from .types.text_annotation import Word
from .types.web_detection import WebDetection


@add_single_feature_methods
class ImageAnnotatorClient(VisionHelpers, IacImageAnnotatorClient):
    __doc__ = IacImageAnnotatorClient.__doc__
    Feature = Feature


__all__ = (
    "ImageAnnotatorAsyncClient",
    "ProductSearchAsyncClient",
    "AddProductToProductSetRequest",
    "AnnotateFileResponse",
    "AnnotateImageRequest",
    "AnnotateImageResponse",
    "AsyncAnnotateFileRequest",
    "AsyncAnnotateFileResponse",
    "AsyncBatchAnnotateFilesRequest",
    "AsyncBatchAnnotateFilesResponse",
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
    "NormalizedBoundingPoly",
    "NormalizedVertex",
    "OperationMetadata",
    "OutputConfig",
    "Page",
    "Paragraph",
    "Position",
    "Product",
    "ProductSearchCategory",
    "ProductSearchClient",
    "ProductSearchParams",
    "ProductSearchResults",
    "ProductSearchResultsView",
    "ProductSet",
    "Property",
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
