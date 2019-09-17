# -*- coding: utf-8 -*-
from google.cloud.vision_v1.services.image_annotator.client import ImageAnnotator
from google.cloud.vision_v1.services.product_search.client import ProductSearch
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
from google.cloud.vision_v1.types.image_annotator import LocalizedObjectAnnotation
from google.cloud.vision_v1.types.image_annotator import LocationInfo
from google.cloud.vision_v1.types.image_annotator import OperationMetadata
from google.cloud.vision_v1.types.image_annotator import OutputConfig
from google.cloud.vision_v1.types.image_annotator import Property
from google.cloud.vision_v1.types.image_annotator import SafeSearchAnnotation
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
    "ImageAnnotator",
    "ProductSearch",
    "BoundingPoly",
    "NormalizedVertex",
    "Position",
    "Vertex",
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
    "ColorInfo",
    "CropHint",
    "CropHintsAnnotation",
    "CropHintsParams",
    "DominantColorsAnnotation",
    "EntityAnnotation",
    "FaceAnnotation",
    "Feature",
    "GcsDestination",
    "GcsSource",
    "Image",
    "ImageAnnotationContext",
    "ImageContext",
    "ImageProperties",
    "ImageSource",
    "InputConfig",
    "LatLongRect",
    "LocalizedObjectAnnotation",
    "LocationInfo",
    "OperationMetadata",
    "OutputConfig",
    "Property",
    "SafeSearchAnnotation",
    "WebDetectionParams",
    "ProductSearchParams",
    "ProductSearchResults",
    "AddProductToProductSetRequest",
    "BatchOperationMetadata",
    "CreateProductRequest",
    "CreateProductSetRequest",
    "CreateReferenceImageRequest",
    "DeleteProductRequest",
    "DeleteProductSetRequest",
    "DeleteReferenceImageRequest",
    "GetProductRequest",
    "GetProductSetRequest",
    "GetReferenceImageRequest",
    "ImportProductSetsGcsSource",
    "ImportProductSetsInputConfig",
    "ImportProductSetsRequest",
    "ImportProductSetsResponse",
    "ListProductSetsRequest",
    "ListProductSetsResponse",
    "ListProductsInProductSetRequest",
    "ListProductsInProductSetResponse",
    "ListProductsRequest",
    "ListProductsResponse",
    "ListReferenceImagesRequest",
    "ListReferenceImagesResponse",
    "Product",
    "ProductSet",
    "ProductSetPurgeConfig",
    "PurgeProductsRequest",
    "ReferenceImage",
    "RemoveProductFromProductSetRequest",
    "UpdateProductRequest",
    "UpdateProductSetRequest",
    "Block",
    "Page",
    "Paragraph",
    "Symbol",
    "TextAnnotation",
    "Word",
    "WebDetection",
)
