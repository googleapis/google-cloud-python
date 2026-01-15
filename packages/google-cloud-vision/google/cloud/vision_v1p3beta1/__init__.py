# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.vision_v1p3beta1 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.image_annotator import ImageAnnotatorClient
from .services.image_annotator import ImageAnnotatorAsyncClient
from .services.product_search import ProductSearchClient
from .services.product_search import ProductSearchAsyncClient

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

if hasattr(api_core, "check_python_version") and hasattr(api_core, "check_dependency_versions"):   # pragma: NO COVER
    api_core.check_python_version("google.cloud.vision_v1p3beta1") # type: ignore
    api_core.check_dependency_versions("google.cloud.vision_v1p3beta1") # type: ignore
else:   # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.vision_v1p3beta1"
        if sys.version_info < (3, 9):
            warnings.warn("You are using a non-supported Python version " +
                          f"({_py_version_str}).  Google will not post any further " +
                          f"updates to {_package_label} supporting this Python version. " +
                          "Please upgrade to the latest Python version, or at " +
                          f"least to Python 3.9, and then update {_package_label}.",
                          FutureWarning)
        if sys.version_info[:2] == (3, 9):
            warnings.warn(f"You are using a Python version ({_py_version_str}) " +
                          f"which Google will stop supporting in {_package_label} in " +
                          "January 2026. Please " +
                          "upgrade to the latest Python version, or at " +
                          "least to Python 3.10, before then, and " +
                          f"then update {_package_label}.",
                          FutureWarning)

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(f"Package {_package_label} depends on " +
                          f"{_dependency_package}, currently installed at version " +
                          f"{_version_used_string}. Future updates to " +
                          f"{_package_label} will require {_dependency_package} at " +
                          f"version {_next_supported_version} or higher{_recommendation}." +
                          " Please ensure " +
                          "that either (a) your Python environment doesn't pin the " +
                          f"version of {_dependency_package}, so that updates to " +
                          f"{_package_label} can require the higher version, or " +
                          "(b) you manually update your Python environment to use at " +
                          f"least version {_next_supported_version} of " +
                          f"{_dependency_package}.",
                          FutureWarning)
    except Exception:
            warnings.warn("Could not determine the version of Python " +
                          "currently being used. To continue receiving " +
                          "updates for {_package_label}, ensure you are " +
                          "using a supported version of Python; see " +
                          "https://devguide.python.org/versions/")

__all__ = (
    'ImageAnnotatorAsyncClient',
    'ProductSearchAsyncClient',
'AddProductToProductSetRequest',
'AnnotateFileResponse',
'AnnotateImageRequest',
'AnnotateImageResponse',
'AsyncAnnotateFileRequest',
'AsyncAnnotateFileResponse',
'AsyncBatchAnnotateFilesRequest',
'AsyncBatchAnnotateFilesResponse',
'BatchAnnotateImagesRequest',
'BatchAnnotateImagesResponse',
'BatchOperationMetadata',
'Block',
'BoundingPoly',
'ColorInfo',
'CreateProductRequest',
'CreateProductSetRequest',
'CreateReferenceImageRequest',
'CropHint',
'CropHintsAnnotation',
'CropHintsParams',
'DeleteProductRequest',
'DeleteProductSetRequest',
'DeleteReferenceImageRequest',
'DominantColorsAnnotation',
'EntityAnnotation',
'FaceAnnotation',
'Feature',
'GcsDestination',
'GcsSource',
'GetProductRequest',
'GetProductSetRequest',
'GetReferenceImageRequest',
'Image',
'ImageAnnotationContext',
'ImageAnnotatorClient',
'ImageContext',
'ImageProperties',
'ImageSource',
'ImportProductSetsGcsSource',
'ImportProductSetsInputConfig',
'ImportProductSetsRequest',
'ImportProductSetsResponse',
'InputConfig',
'LatLongRect',
'Likelihood',
'ListProductSetsRequest',
'ListProductSetsResponse',
'ListProductsInProductSetRequest',
'ListProductsInProductSetResponse',
'ListProductsRequest',
'ListProductsResponse',
'ListReferenceImagesRequest',
'ListReferenceImagesResponse',
'LocalizedObjectAnnotation',
'LocationInfo',
'NormalizedVertex',
'OperationMetadata',
'OutputConfig',
'Page',
'Paragraph',
'Position',
'Product',
'ProductSearchClient',
'ProductSearchParams',
'ProductSearchResults',
'ProductSet',
'Property',
'ReferenceImage',
'RemoveProductFromProductSetRequest',
'SafeSearchAnnotation',
'Symbol',
'TextAnnotation',
'TextDetectionParams',
'UpdateProductRequest',
'UpdateProductSetRequest',
'Vertex',
'WebDetection',
'WebDetectionParams',
'Word',
)
