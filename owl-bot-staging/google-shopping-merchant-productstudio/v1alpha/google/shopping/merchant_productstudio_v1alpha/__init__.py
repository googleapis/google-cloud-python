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
from google.shopping.merchant_productstudio_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.image_service import ImageServiceClient
from .services.image_service import ImageServiceAsyncClient
from .services.text_suggestions_service import TextSuggestionsServiceClient
from .services.text_suggestions_service import TextSuggestionsServiceAsyncClient

from .types.image import GeneratedImage
from .types.image import GenerateImageBackgroundConfig
from .types.image import GenerateProductImageBackgroundRequest
from .types.image import GenerateProductImageBackgroundResponse
from .types.image import OutputImageConfig
from .types.image import RemoveImageBackgroundConfig
from .types.image import RemoveProductImageBackgroundRequest
from .types.image import RemoveProductImageBackgroundResponse
from .types.image import RgbColor
from .types.image import UpscaleProductImageRequest
from .types.image import UpscaleProductImageResponse
from .types.productstudio_common import InputImage
from .types.textsuggestions import GenerateProductTextSuggestionsRequest
from .types.textsuggestions import GenerateProductTextSuggestionsResponse
from .types.textsuggestions import Image
from .types.textsuggestions import OutputSpec
from .types.textsuggestions import ProductInfo
from .types.textsuggestions import ProductTextGenerationMetadata
from .types.textsuggestions import ProductTextGenerationSuggestion
from .types.textsuggestions import TitleExample

__all__ = (
    'ImageServiceAsyncClient',
    'TextSuggestionsServiceAsyncClient',
'GenerateImageBackgroundConfig',
'GenerateProductImageBackgroundRequest',
'GenerateProductImageBackgroundResponse',
'GenerateProductTextSuggestionsRequest',
'GenerateProductTextSuggestionsResponse',
'GeneratedImage',
'Image',
'ImageServiceClient',
'InputImage',
'OutputImageConfig',
'OutputSpec',
'ProductInfo',
'ProductTextGenerationMetadata',
'ProductTextGenerationSuggestion',
'RemoveImageBackgroundConfig',
'RemoveProductImageBackgroundRequest',
'RemoveProductImageBackgroundResponse',
'RgbColor',
'TextSuggestionsServiceClient',
'TitleExample',
'UpscaleProductImageRequest',
'UpscaleProductImageResponse',
)
