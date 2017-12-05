# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-vision').version

from google.cloud.vision_v1 import enums
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1 import types


__all__ = (
    # Common
    '__version__',

    # GAPIC & Partial Manual Layer
    'enums',
    'ImageAnnotatorClient',
    'types',
)
