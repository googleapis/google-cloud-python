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

# -----------------------------------------------------------------------------
# TRANSITION CODE
# -----------------------------------------------------------------------------
# The old Vision manual layer is now deprecated, but to allow
# users the time to move from the manual layer to the mostly auto-generated
# layer, they are both living side by side for a few months.
#
# Instantiating the old manual layer (`google.cloud.vision.Client`) will
# issue a DeprecationWarning.
#
# When it comes time to remove the old layer, everything in this directory
# should go away EXCEPT __init__.py, decorators.py, and helpers.py.
# Additionally, the import and export of `Client` should be removed from this
# file (along with this note), and the rest should be left intact.
# -----------------------------------------------------------------------------

from __future__ import absolute_import

from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-vision').version

from google.cloud.vision.client import Client

from google.cloud.vision_v1 import enums
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1 import types


__all__ = (
    # Common
    '__version__',

    # Manual Layer
    'Client',

    # GAPIC & Partial Manual Layer
    'enums',
    'ImageAnnotatorClient',
    'types',
)
