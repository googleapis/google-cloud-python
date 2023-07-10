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
from google.cloud.speech import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.speech_v1.services.adaptation.client import AdaptationClient
from google.cloud.speech_v1.services.adaptation.async_client import (
    AdaptationAsyncClient,
)
from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1.services.speech.async_client import SpeechAsyncClient

from google.cloud.speech_v1.types.cloud_speech import LongRunningRecognizeMetadata
from google.cloud.speech_v1.types.cloud_speech import LongRunningRecognizeRequest
from google.cloud.speech_v1.types.cloud_speech import LongRunningRecognizeResponse
from google.cloud.speech_v1.types.cloud_speech import RecognitionAudio
from google.cloud.speech_v1.types.cloud_speech import RecognitionConfig
from google.cloud.speech_v1.types.cloud_speech import RecognitionMetadata
from google.cloud.speech_v1.types.cloud_speech import RecognizeRequest
from google.cloud.speech_v1.types.cloud_speech import RecognizeResponse
from google.cloud.speech_v1.types.cloud_speech import SpeakerDiarizationConfig
from google.cloud.speech_v1.types.cloud_speech import SpeechAdaptationInfo
from google.cloud.speech_v1.types.cloud_speech import SpeechContext
from google.cloud.speech_v1.types.cloud_speech import SpeechRecognitionAlternative
from google.cloud.speech_v1.types.cloud_speech import SpeechRecognitionResult
from google.cloud.speech_v1.types.cloud_speech import StreamingRecognitionConfig
from google.cloud.speech_v1.types.cloud_speech import StreamingRecognitionResult
from google.cloud.speech_v1.types.cloud_speech import StreamingRecognizeRequest
from google.cloud.speech_v1.types.cloud_speech import StreamingRecognizeResponse
from google.cloud.speech_v1.types.cloud_speech import TranscriptOutputConfig
from google.cloud.speech_v1.types.cloud_speech import WordInfo
from google.cloud.speech_v1.types.cloud_speech_adaptation import (
    CreateCustomClassRequest,
)
from google.cloud.speech_v1.types.cloud_speech_adaptation import CreatePhraseSetRequest
from google.cloud.speech_v1.types.cloud_speech_adaptation import (
    DeleteCustomClassRequest,
)
from google.cloud.speech_v1.types.cloud_speech_adaptation import DeletePhraseSetRequest
from google.cloud.speech_v1.types.cloud_speech_adaptation import GetCustomClassRequest
from google.cloud.speech_v1.types.cloud_speech_adaptation import GetPhraseSetRequest
from google.cloud.speech_v1.types.cloud_speech_adaptation import (
    ListCustomClassesRequest,
)
from google.cloud.speech_v1.types.cloud_speech_adaptation import (
    ListCustomClassesResponse,
)
from google.cloud.speech_v1.types.cloud_speech_adaptation import ListPhraseSetRequest
from google.cloud.speech_v1.types.cloud_speech_adaptation import ListPhraseSetResponse
from google.cloud.speech_v1.types.cloud_speech_adaptation import (
    UpdateCustomClassRequest,
)
from google.cloud.speech_v1.types.cloud_speech_adaptation import UpdatePhraseSetRequest
from google.cloud.speech_v1.types.resource import CustomClass
from google.cloud.speech_v1.types.resource import PhraseSet
from google.cloud.speech_v1.types.resource import SpeechAdaptation

__all__ = (
    "AdaptationClient",
    "AdaptationAsyncClient",
    "SpeechClient",
    "SpeechAsyncClient",
    "LongRunningRecognizeMetadata",
    "LongRunningRecognizeRequest",
    "LongRunningRecognizeResponse",
    "RecognitionAudio",
    "RecognitionConfig",
    "RecognitionMetadata",
    "RecognizeRequest",
    "RecognizeResponse",
    "SpeakerDiarizationConfig",
    "SpeechAdaptationInfo",
    "SpeechContext",
    "SpeechRecognitionAlternative",
    "SpeechRecognitionResult",
    "StreamingRecognitionConfig",
    "StreamingRecognitionResult",
    "StreamingRecognizeRequest",
    "StreamingRecognizeResponse",
    "TranscriptOutputConfig",
    "WordInfo",
    "CreateCustomClassRequest",
    "CreatePhraseSetRequest",
    "DeleteCustomClassRequest",
    "DeletePhraseSetRequest",
    "GetCustomClassRequest",
    "GetPhraseSetRequest",
    "ListCustomClassesRequest",
    "ListCustomClassesResponse",
    "ListPhraseSetRequest",
    "ListPhraseSetResponse",
    "UpdateCustomClassRequest",
    "UpdatePhraseSetRequest",
    "CustomClass",
    "PhraseSet",
    "SpeechAdaptation",
)
