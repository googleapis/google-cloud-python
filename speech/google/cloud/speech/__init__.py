# Copyright 2016 Google LLC
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

"""Google Cloud Speech API wrapper."""


from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-speech').version

from google.cloud.speech.alternative import Alternative
from google.cloud.speech.client import Client
from google.cloud.speech.encoding import Encoding
from google.cloud.speech.operation import Operation

from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1 import types


__all__ = (
    # Common
    '__version__',

    # Deprecated Manual Layer
    'Alternative',
    'Client',
    'Encoding',
    'Operation',

    # GAPIC & Partial Manual Layer
    'enums',
    'SpeechClient',
    'types',
)
