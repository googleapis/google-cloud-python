# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.speech_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.adaptation import AdaptationClient
from .services.adaptation import AdaptationAsyncClient
from .services.speech import SpeechClient
from .services.speech import SpeechAsyncClient

from .types.cloud_speech import LongRunningRecognizeMetadata
from .types.cloud_speech import LongRunningRecognizeRequest
from .types.cloud_speech import LongRunningRecognizeResponse
from .types.cloud_speech import RecognitionAudio
from .types.cloud_speech import RecognitionConfig
from .types.cloud_speech import RecognitionMetadata
from .types.cloud_speech import RecognizeRequest
from .types.cloud_speech import RecognizeResponse
from .types.cloud_speech import SpeakerDiarizationConfig
from .types.cloud_speech import SpeechAdaptationInfo
from .types.cloud_speech import SpeechContext
from .types.cloud_speech import SpeechRecognitionAlternative
from .types.cloud_speech import SpeechRecognitionResult
from .types.cloud_speech import StreamingRecognitionConfig
from .types.cloud_speech import StreamingRecognitionResult
from .types.cloud_speech import StreamingRecognizeRequest
from .types.cloud_speech import StreamingRecognizeResponse
from .types.cloud_speech import TranscriptOutputConfig
from .types.cloud_speech import WordInfo
from .types.cloud_speech_adaptation import CreateCustomClassRequest
from .types.cloud_speech_adaptation import CreatePhraseSetRequest
from .types.cloud_speech_adaptation import DeleteCustomClassRequest
from .types.cloud_speech_adaptation import DeletePhraseSetRequest
from .types.cloud_speech_adaptation import GetCustomClassRequest
from .types.cloud_speech_adaptation import GetPhraseSetRequest
from .types.cloud_speech_adaptation import ListCustomClassesRequest
from .types.cloud_speech_adaptation import ListCustomClassesResponse
from .types.cloud_speech_adaptation import ListPhraseSetRequest
from .types.cloud_speech_adaptation import ListPhraseSetResponse
from .types.cloud_speech_adaptation import UpdateCustomClassRequest
from .types.cloud_speech_adaptation import UpdatePhraseSetRequest
from .types.resource import CustomClass
from .types.resource import PhraseSet
from .types.resource import SpeechAdaptation

from google.cloud.speech_v1.helpers import SpeechHelpers


class SpeechClient(SpeechHelpers, SpeechClient):
    __doc__ = SpeechClient.__doc__


__all__ = (
    "AdaptationAsyncClient",
    "SpeechAsyncClient",
    "AdaptationClient",
    "CreateCustomClassRequest",
    "CreatePhraseSetRequest",
    "CustomClass",
    "DeleteCustomClassRequest",
    "DeletePhraseSetRequest",
    "GetCustomClassRequest",
    "GetPhraseSetRequest",
    "ListCustomClassesRequest",
    "ListCustomClassesResponse",
    "ListPhraseSetRequest",
    "ListPhraseSetResponse",
    "LongRunningRecognizeMetadata",
    "LongRunningRecognizeRequest",
    "LongRunningRecognizeResponse",
    "PhraseSet",
    "RecognitionAudio",
    "RecognitionConfig",
    "RecognitionMetadata",
    "RecognizeRequest",
    "RecognizeResponse",
    "SpeakerDiarizationConfig",
    "SpeechAdaptation",
    "SpeechAdaptationInfo",
    "SpeechClient",
    "SpeechContext",
    "SpeechRecognitionAlternative",
    "SpeechRecognitionResult",
    "StreamingRecognitionConfig",
    "StreamingRecognitionResult",
    "StreamingRecognizeRequest",
    "StreamingRecognizeResponse",
    "TranscriptOutputConfig",
    "UpdateCustomClassRequest",
    "UpdatePhraseSetRequest",
    "WordInfo",
)
