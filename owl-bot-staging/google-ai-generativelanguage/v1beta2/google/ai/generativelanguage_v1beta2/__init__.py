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
from google.ai.generativelanguage_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.discuss_service import DiscussServiceClient
from .services.discuss_service import DiscussServiceAsyncClient
from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient
from .services.text_service import TextServiceClient
from .services.text_service import TextServiceAsyncClient

from .types.citation import CitationMetadata
from .types.citation import CitationSource
from .types.discuss_service import CountMessageTokensRequest
from .types.discuss_service import CountMessageTokensResponse
from .types.discuss_service import Example
from .types.discuss_service import GenerateMessageRequest
from .types.discuss_service import GenerateMessageResponse
from .types.discuss_service import Message
from .types.discuss_service import MessagePrompt
from .types.model import Model
from .types.model_service import GetModelRequest
from .types.model_service import ListModelsRequest
from .types.model_service import ListModelsResponse
from .types.safety import ContentFilter
from .types.safety import SafetyFeedback
from .types.safety import SafetyRating
from .types.safety import SafetySetting
from .types.safety import HarmCategory
from .types.text_service import Embedding
from .types.text_service import EmbedTextRequest
from .types.text_service import EmbedTextResponse
from .types.text_service import GenerateTextRequest
from .types.text_service import GenerateTextResponse
from .types.text_service import TextCompletion
from .types.text_service import TextPrompt

__all__ = (
    'DiscussServiceAsyncClient',
    'ModelServiceAsyncClient',
    'TextServiceAsyncClient',
'CitationMetadata',
'CitationSource',
'ContentFilter',
'CountMessageTokensRequest',
'CountMessageTokensResponse',
'DiscussServiceClient',
'EmbedTextRequest',
'EmbedTextResponse',
'Embedding',
'Example',
'GenerateMessageRequest',
'GenerateMessageResponse',
'GenerateTextRequest',
'GenerateTextResponse',
'GetModelRequest',
'HarmCategory',
'ListModelsRequest',
'ListModelsResponse',
'Message',
'MessagePrompt',
'Model',
'ModelServiceClient',
'SafetyFeedback',
'SafetyRating',
'SafetySetting',
'TextCompletion',
'TextPrompt',
'TextServiceClient',
)
