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
from google.shopping.merchant_productstudio import gapic_version as package_version

__version__ = package_version.__version__


from google.shopping.merchant_productstudio_v1alpha.services.image_service.client import ImageServiceClient
from google.shopping.merchant_productstudio_v1alpha.services.image_service.async_client import ImageServiceAsyncClient
from google.shopping.merchant_productstudio_v1alpha.services.text_suggestions_service.client import TextSuggestionsServiceClient
from google.shopping.merchant_productstudio_v1alpha.services.text_suggestions_service.async_client import TextSuggestionsServiceAsyncClient

from google.shopping.merchant_productstudio_v1alpha.types.image import GeneratedImage
from google.shopping.merchant_productstudio_v1alpha.types.image import GenerateImageBackgroundConfig
from google.shopping.merchant_productstudio_v1alpha.types.image import GenerateProductImageBackgroundRequest
from google.shopping.merchant_productstudio_v1alpha.types.image import GenerateProductImageBackgroundResponse
from google.shopping.merchant_productstudio_v1alpha.types.image import OutputImageConfig
from google.shopping.merchant_productstudio_v1alpha.types.image import RemoveImageBackgroundConfig
from google.shopping.merchant_productstudio_v1alpha.types.image import RemoveProductImageBackgroundRequest
from google.shopping.merchant_productstudio_v1alpha.types.image import RemoveProductImageBackgroundResponse
from google.shopping.merchant_productstudio_v1alpha.types.image import RgbColor
from google.shopping.merchant_productstudio_v1alpha.types.image import UpscaleProductImageRequest
from google.shopping.merchant_productstudio_v1alpha.types.image import UpscaleProductImageResponse
from google.shopping.merchant_productstudio_v1alpha.types.productstudio_common import InputImage
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import GenerateProductTextSuggestionsRequest
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import GenerateProductTextSuggestionsResponse
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import Image
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import OutputSpec
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import ProductInfo
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import ProductTextGenerationMetadata
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import ProductTextGenerationSuggestion
from google.shopping.merchant_productstudio_v1alpha.types.textsuggestions import TitleExample

__all__ = ('ImageServiceClient',
    'ImageServiceAsyncClient',
    'TextSuggestionsServiceClient',
    'TextSuggestionsServiceAsyncClient',
    'GeneratedImage',
    'GenerateImageBackgroundConfig',
    'GenerateProductImageBackgroundRequest',
    'GenerateProductImageBackgroundResponse',
    'OutputImageConfig',
    'RemoveImageBackgroundConfig',
    'RemoveProductImageBackgroundRequest',
    'RemoveProductImageBackgroundResponse',
    'RgbColor',
    'UpscaleProductImageRequest',
    'UpscaleProductImageResponse',
    'InputImage',
    'GenerateProductTextSuggestionsRequest',
    'GenerateProductTextSuggestionsResponse',
    'Image',
    'OutputSpec',
    'ProductInfo',
    'ProductTextGenerationMetadata',
    'ProductTextGenerationSuggestion',
    'TitleExample',
)
