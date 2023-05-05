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
from google.ai.generativelanguage import gapic_version as package_version

__version__ = package_version.__version__


from google.ai.generativelanguage_v1beta2.services.discuss_service.client import DiscussServiceClient
from google.ai.generativelanguage_v1beta2.services.discuss_service.async_client import DiscussServiceAsyncClient
from google.ai.generativelanguage_v1beta2.services.model_service.client import ModelServiceClient
from google.ai.generativelanguage_v1beta2.services.model_service.async_client import ModelServiceAsyncClient
from google.ai.generativelanguage_v1beta2.services.text_service.client import TextServiceClient
from google.ai.generativelanguage_v1beta2.services.text_service.async_client import TextServiceAsyncClient

from google.ai.generativelanguage_v1beta2.types.citation import CitationMetadata
from google.ai.generativelanguage_v1beta2.types.citation import CitationSource
from google.ai.generativelanguage_v1beta2.types.discuss_service import CountMessageTokensRequest
from google.ai.generativelanguage_v1beta2.types.discuss_service import CountMessageTokensResponse
from google.ai.generativelanguage_v1beta2.types.discuss_service import Example
from google.ai.generativelanguage_v1beta2.types.discuss_service import GenerateMessageRequest
from google.ai.generativelanguage_v1beta2.types.discuss_service import GenerateMessageResponse
from google.ai.generativelanguage_v1beta2.types.discuss_service import Message
from google.ai.generativelanguage_v1beta2.types.discuss_service import MessagePrompt
from google.ai.generativelanguage_v1beta2.types.model import Model
from google.ai.generativelanguage_v1beta2.types.model_service import GetModelRequest
from google.ai.generativelanguage_v1beta2.types.model_service import ListModelsRequest
from google.ai.generativelanguage_v1beta2.types.model_service import ListModelsResponse
from google.ai.generativelanguage_v1beta2.types.safety import ContentFilter
from google.ai.generativelanguage_v1beta2.types.safety import SafetyFeedback
from google.ai.generativelanguage_v1beta2.types.safety import SafetyRating
from google.ai.generativelanguage_v1beta2.types.safety import SafetySetting
from google.ai.generativelanguage_v1beta2.types.safety import HarmCategory
from google.ai.generativelanguage_v1beta2.types.text_service import Embedding
from google.ai.generativelanguage_v1beta2.types.text_service import EmbedTextRequest
from google.ai.generativelanguage_v1beta2.types.text_service import EmbedTextResponse
from google.ai.generativelanguage_v1beta2.types.text_service import GenerateTextRequest
from google.ai.generativelanguage_v1beta2.types.text_service import GenerateTextResponse
from google.ai.generativelanguage_v1beta2.types.text_service import TextCompletion
from google.ai.generativelanguage_v1beta2.types.text_service import TextPrompt

__all__ = ('DiscussServiceClient',
    'DiscussServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'TextServiceClient',
    'TextServiceAsyncClient',
    'CitationMetadata',
    'CitationSource',
    'CountMessageTokensRequest',
    'CountMessageTokensResponse',
    'Example',
    'GenerateMessageRequest',
    'GenerateMessageResponse',
    'Message',
    'MessagePrompt',
    'Model',
    'GetModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'ContentFilter',
    'SafetyFeedback',
    'SafetyRating',
    'SafetySetting',
    'HarmCategory',
    'Embedding',
    'EmbedTextRequest',
    'EmbedTextResponse',
    'GenerateTextRequest',
    'GenerateTextResponse',
    'TextCompletion',
    'TextPrompt',
)
