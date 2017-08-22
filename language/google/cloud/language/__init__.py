# Copyright 2016 Google Inc.
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
# The old Language manual layer is now deprecated, but to allow
# users the time to move from the manual layer to the mostly auto-generated
# layer, they are both living side by side for a few months.
#
# Instantiating the old manual layer (`google.cloud.language.Client`) will
# issue a DeprecationWarning.
#
# When it comes time to remove the old layer, everything in this directory
# should go away EXCEPT __init__.py (which can be renamed to language.py and
# put one directory above).
#
# Additionally, the import and export of `Client`, `Document`, and `Encoding`
# should be removed from this file (along with this note), and the rest should
# be left intact.
# -----------------------------------------------------------------------------

"""Client library for Google Cloud Natural Language API."""

from __future__ import absolute_import

from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-language').version

from google.cloud.language_v1 import *  # noqa

from google.cloud.language.client import Client
from google.cloud.language.document import Document
from google.cloud.language.document import Encoding

__all__ = (
    # Common
    '__version__',

    # Manual Layer
    'Client',
    'Document',
    'Encoding',

    # Auto-gen
    'enums',
    'LanguageServiceClient',
    'types',
)
