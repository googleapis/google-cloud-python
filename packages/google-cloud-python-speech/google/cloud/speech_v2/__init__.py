# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.speech_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.speech import SpeechClient
from .services.speech import SpeechAsyncClient

from .types.cloud_speech import AutoDetectDecodingConfig
from .types.cloud_speech import BatchRecognizeFileMetadata
from .types.cloud_speech import BatchRecognizeFileResult
from .types.cloud_speech import BatchRecognizeMetadata
from .types.cloud_speech import BatchRecognizeRequest
from .types.cloud_speech import BatchRecognizeResponse
from .types.cloud_speech import BatchRecognizeResults
from .types.cloud_speech import BatchRecognizeTranscriptionMetadata
from .types.cloud_speech import Config
from .types.cloud_speech import CreateCustomClassRequest
from .types.cloud_speech import CreatePhraseSetRequest
from .types.cloud_speech import CreateRecognizerRequest
from .types.cloud_speech import CustomClass
from .types.cloud_speech import DeleteCustomClassRequest
from .types.cloud_speech import DeletePhraseSetRequest
from .types.cloud_speech import DeleteRecognizerRequest
from .types.cloud_speech import ExplicitDecodingConfig
from .types.cloud_speech import GcsOutputConfig
from .types.cloud_speech import GetConfigRequest
from .types.cloud_speech import GetCustomClassRequest
from .types.cloud_speech import GetPhraseSetRequest
from .types.cloud_speech import GetRecognizerRequest
from .types.cloud_speech import InlineOutputConfig
from .types.cloud_speech import ListCustomClassesRequest
from .types.cloud_speech import ListCustomClassesResponse
from .types.cloud_speech import ListPhraseSetsRequest
from .types.cloud_speech import ListPhraseSetsResponse
from .types.cloud_speech import ListRecognizersRequest
from .types.cloud_speech import ListRecognizersResponse
from .types.cloud_speech import OperationMetadata
from .types.cloud_speech import PhraseSet
from .types.cloud_speech import RecognitionConfig
from .types.cloud_speech import RecognitionFeatures
from .types.cloud_speech import RecognitionOutputConfig
from .types.cloud_speech import RecognitionResponseMetadata
from .types.cloud_speech import Recognizer
from .types.cloud_speech import RecognizeRequest
from .types.cloud_speech import RecognizeResponse
from .types.cloud_speech import SpeakerDiarizationConfig
from .types.cloud_speech import SpeechAdaptation
from .types.cloud_speech import SpeechRecognitionAlternative
from .types.cloud_speech import SpeechRecognitionResult
from .types.cloud_speech import StreamingRecognitionConfig
from .types.cloud_speech import StreamingRecognitionFeatures
from .types.cloud_speech import StreamingRecognitionResult
from .types.cloud_speech import StreamingRecognizeRequest
from .types.cloud_speech import StreamingRecognizeResponse
from .types.cloud_speech import UndeleteCustomClassRequest
from .types.cloud_speech import UndeletePhraseSetRequest
from .types.cloud_speech import UndeleteRecognizerRequest
from .types.cloud_speech import UpdateConfigRequest
from .types.cloud_speech import UpdateCustomClassRequest
from .types.cloud_speech import UpdatePhraseSetRequest
from .types.cloud_speech import UpdateRecognizerRequest
from .types.cloud_speech import WordInfo

__all__ = (
    "SpeechAsyncClient",
    "AutoDetectDecodingConfig",
    "BatchRecognizeFileMetadata",
    "BatchRecognizeFileResult",
    "BatchRecognizeMetadata",
    "BatchRecognizeRequest",
    "BatchRecognizeResponse",
    "BatchRecognizeResults",
    "BatchRecognizeTranscriptionMetadata",
    "Config",
    "CreateCustomClassRequest",
    "CreatePhraseSetRequest",
    "CreateRecognizerRequest",
    "CustomClass",
    "DeleteCustomClassRequest",
    "DeletePhraseSetRequest",
    "DeleteRecognizerRequest",
    "ExplicitDecodingConfig",
    "GcsOutputConfig",
    "GetConfigRequest",
    "GetCustomClassRequest",
    "GetPhraseSetRequest",
    "GetRecognizerRequest",
    "InlineOutputConfig",
    "ListCustomClassesRequest",
    "ListCustomClassesResponse",
    "ListPhraseSetsRequest",
    "ListPhraseSetsResponse",
    "ListRecognizersRequest",
    "ListRecognizersResponse",
    "OperationMetadata",
    "PhraseSet",
    "RecognitionConfig",
    "RecognitionFeatures",
    "RecognitionOutputConfig",
    "RecognitionResponseMetadata",
    "RecognizeRequest",
    "RecognizeResponse",
    "Recognizer",
    "SpeakerDiarizationConfig",
    "SpeechAdaptation",
    "SpeechClient",
    "SpeechRecognitionAlternative",
    "SpeechRecognitionResult",
    "StreamingRecognitionConfig",
    "StreamingRecognitionFeatures",
    "StreamingRecognitionResult",
    "StreamingRecognizeRequest",
    "StreamingRecognizeResponse",
    "UndeleteCustomClassRequest",
    "UndeletePhraseSetRequest",
    "UndeleteRecognizerRequest",
    "UpdateConfigRequest",
    "UpdateCustomClassRequest",
    "UpdatePhraseSetRequest",
    "UpdateRecognizerRequest",
    "WordInfo",
)
