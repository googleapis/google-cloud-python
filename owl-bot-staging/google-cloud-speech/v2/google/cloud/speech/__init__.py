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


from google.cloud.speech_v2.services.speech.client import SpeechClient
from google.cloud.speech_v2.services.speech.async_client import SpeechAsyncClient

from google.cloud.speech_v2.types.cloud_speech import AutoDetectDecodingConfig
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeFileMetadata
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeFileResult
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeMetadata
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeRequest
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeResponse
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeResults
from google.cloud.speech_v2.types.cloud_speech import BatchRecognizeTranscriptionMetadata
from google.cloud.speech_v2.types.cloud_speech import CloudStorageResult
from google.cloud.speech_v2.types.cloud_speech import Config
from google.cloud.speech_v2.types.cloud_speech import CreateCustomClassRequest
from google.cloud.speech_v2.types.cloud_speech import CreatePhraseSetRequest
from google.cloud.speech_v2.types.cloud_speech import CreateRecognizerRequest
from google.cloud.speech_v2.types.cloud_speech import CustomClass
from google.cloud.speech_v2.types.cloud_speech import DeleteCustomClassRequest
from google.cloud.speech_v2.types.cloud_speech import DeletePhraseSetRequest
from google.cloud.speech_v2.types.cloud_speech import DeleteRecognizerRequest
from google.cloud.speech_v2.types.cloud_speech import ExplicitDecodingConfig
from google.cloud.speech_v2.types.cloud_speech import GcsOutputConfig
from google.cloud.speech_v2.types.cloud_speech import GetConfigRequest
from google.cloud.speech_v2.types.cloud_speech import GetCustomClassRequest
from google.cloud.speech_v2.types.cloud_speech import GetPhraseSetRequest
from google.cloud.speech_v2.types.cloud_speech import GetRecognizerRequest
from google.cloud.speech_v2.types.cloud_speech import InlineOutputConfig
from google.cloud.speech_v2.types.cloud_speech import InlineResult
from google.cloud.speech_v2.types.cloud_speech import ListCustomClassesRequest
from google.cloud.speech_v2.types.cloud_speech import ListCustomClassesResponse
from google.cloud.speech_v2.types.cloud_speech import ListPhraseSetsRequest
from google.cloud.speech_v2.types.cloud_speech import ListPhraseSetsResponse
from google.cloud.speech_v2.types.cloud_speech import ListRecognizersRequest
from google.cloud.speech_v2.types.cloud_speech import ListRecognizersResponse
from google.cloud.speech_v2.types.cloud_speech import OperationMetadata
from google.cloud.speech_v2.types.cloud_speech import PhraseSet
from google.cloud.speech_v2.types.cloud_speech import RecognitionConfig
from google.cloud.speech_v2.types.cloud_speech import RecognitionFeatures
from google.cloud.speech_v2.types.cloud_speech import RecognitionOutputConfig
from google.cloud.speech_v2.types.cloud_speech import RecognitionResponseMetadata
from google.cloud.speech_v2.types.cloud_speech import Recognizer
from google.cloud.speech_v2.types.cloud_speech import RecognizeRequest
from google.cloud.speech_v2.types.cloud_speech import RecognizeResponse
from google.cloud.speech_v2.types.cloud_speech import SpeakerDiarizationConfig
from google.cloud.speech_v2.types.cloud_speech import SpeechAdaptation
from google.cloud.speech_v2.types.cloud_speech import SpeechRecognitionAlternative
from google.cloud.speech_v2.types.cloud_speech import SpeechRecognitionResult
from google.cloud.speech_v2.types.cloud_speech import StreamingRecognitionConfig
from google.cloud.speech_v2.types.cloud_speech import StreamingRecognitionFeatures
from google.cloud.speech_v2.types.cloud_speech import StreamingRecognitionResult
from google.cloud.speech_v2.types.cloud_speech import StreamingRecognizeRequest
from google.cloud.speech_v2.types.cloud_speech import StreamingRecognizeResponse
from google.cloud.speech_v2.types.cloud_speech import TranscriptNormalization
from google.cloud.speech_v2.types.cloud_speech import UndeleteCustomClassRequest
from google.cloud.speech_v2.types.cloud_speech import UndeletePhraseSetRequest
from google.cloud.speech_v2.types.cloud_speech import UndeleteRecognizerRequest
from google.cloud.speech_v2.types.cloud_speech import UpdateConfigRequest
from google.cloud.speech_v2.types.cloud_speech import UpdateCustomClassRequest
from google.cloud.speech_v2.types.cloud_speech import UpdatePhraseSetRequest
from google.cloud.speech_v2.types.cloud_speech import UpdateRecognizerRequest
from google.cloud.speech_v2.types.cloud_speech import WordInfo

__all__ = ('SpeechClient',
    'SpeechAsyncClient',
    'AutoDetectDecodingConfig',
    'BatchRecognizeFileMetadata',
    'BatchRecognizeFileResult',
    'BatchRecognizeMetadata',
    'BatchRecognizeRequest',
    'BatchRecognizeResponse',
    'BatchRecognizeResults',
    'BatchRecognizeTranscriptionMetadata',
    'CloudStorageResult',
    'Config',
    'CreateCustomClassRequest',
    'CreatePhraseSetRequest',
    'CreateRecognizerRequest',
    'CustomClass',
    'DeleteCustomClassRequest',
    'DeletePhraseSetRequest',
    'DeleteRecognizerRequest',
    'ExplicitDecodingConfig',
    'GcsOutputConfig',
    'GetConfigRequest',
    'GetCustomClassRequest',
    'GetPhraseSetRequest',
    'GetRecognizerRequest',
    'InlineOutputConfig',
    'InlineResult',
    'ListCustomClassesRequest',
    'ListCustomClassesResponse',
    'ListPhraseSetsRequest',
    'ListPhraseSetsResponse',
    'ListRecognizersRequest',
    'ListRecognizersResponse',
    'OperationMetadata',
    'PhraseSet',
    'RecognitionConfig',
    'RecognitionFeatures',
    'RecognitionOutputConfig',
    'RecognitionResponseMetadata',
    'Recognizer',
    'RecognizeRequest',
    'RecognizeResponse',
    'SpeakerDiarizationConfig',
    'SpeechAdaptation',
    'SpeechRecognitionAlternative',
    'SpeechRecognitionResult',
    'StreamingRecognitionConfig',
    'StreamingRecognitionFeatures',
    'StreamingRecognitionResult',
    'StreamingRecognizeRequest',
    'StreamingRecognizeResponse',
    'TranscriptNormalization',
    'UndeleteCustomClassRequest',
    'UndeletePhraseSetRequest',
    'UndeleteRecognizerRequest',
    'UpdateConfigRequest',
    'UpdateCustomClassRequest',
    'UpdatePhraseSetRequest',
    'UpdateRecognizerRequest',
    'WordInfo',
)
