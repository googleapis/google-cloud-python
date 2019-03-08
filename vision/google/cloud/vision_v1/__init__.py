# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.cloud.vision_helpers.decorators import add_single_feature_methods
from google.cloud.vision_helpers import VisionHelpers

from google.cloud.vision_v1 import types
from google.cloud.vision_v1.gapic import enums
from google.cloud.vision_v1.gapic import image_annotator_client as iac
from google.cloud.vision_v1.gapic import product_search_client


class ProductSearchClient(product_search_client.ProductSearchClient):
    __doc__ = product_search_client.ProductSearchClient.__doc__
    enums = enums


@add_single_feature_methods
class ImageAnnotatorClient(VisionHelpers, iac.ImageAnnotatorClient):
    __doc__ = iac.ImageAnnotatorClient.__doc__
    enums = enums


__all__ = ("enums", "types", "ProductSearchClient", "ImageAnnotatorClient")
