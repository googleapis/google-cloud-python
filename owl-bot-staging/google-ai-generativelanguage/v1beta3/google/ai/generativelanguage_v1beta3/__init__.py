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
from google.ai.generativelanguage_v1beta3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.discuss_service import DiscussServiceClient
from .services.discuss_service import DiscussServiceAsyncClient
from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient
from .services.permission_service import PermissionServiceClient
from .services.permission_service import PermissionServiceAsyncClient
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
from .types.model_service import CreateTunedModelMetadata
from .types.model_service import CreateTunedModelRequest
from .types.model_service import DeleteTunedModelRequest
from .types.model_service import GetModelRequest
from .types.model_service import GetTunedModelRequest
from .types.model_service import ListModelsRequest
from .types.model_service import ListModelsResponse
from .types.model_service import ListTunedModelsRequest
from .types.model_service import ListTunedModelsResponse
from .types.model_service import UpdateTunedModelRequest
from .types.permission import Permission
from .types.permission_service import CreatePermissionRequest
from .types.permission_service import DeletePermissionRequest
from .types.permission_service import GetPermissionRequest
from .types.permission_service import ListPermissionsRequest
from .types.permission_service import ListPermissionsResponse
from .types.permission_service import TransferOwnershipRequest
from .types.permission_service import TransferOwnershipResponse
from .types.permission_service import UpdatePermissionRequest
from .types.safety import ContentFilter
from .types.safety import SafetyFeedback
from .types.safety import SafetyRating
from .types.safety import SafetySetting
from .types.safety import HarmCategory
from .types.text_service import BatchEmbedTextRequest
from .types.text_service import BatchEmbedTextResponse
from .types.text_service import CountTextTokensRequest
from .types.text_service import CountTextTokensResponse
from .types.text_service import Embedding
from .types.text_service import EmbedTextRequest
from .types.text_service import EmbedTextResponse
from .types.text_service import GenerateTextRequest
from .types.text_service import GenerateTextResponse
from .types.text_service import TextCompletion
from .types.text_service import TextPrompt
from .types.tuned_model import Dataset
from .types.tuned_model import Hyperparameters
from .types.tuned_model import TunedModel
from .types.tuned_model import TunedModelSource
from .types.tuned_model import TuningExample
from .types.tuned_model import TuningExamples
from .types.tuned_model import TuningSnapshot
from .types.tuned_model import TuningTask

__all__ = (
    'DiscussServiceAsyncClient',
    'ModelServiceAsyncClient',
    'PermissionServiceAsyncClient',
    'TextServiceAsyncClient',
'BatchEmbedTextRequest',
'BatchEmbedTextResponse',
'CitationMetadata',
'CitationSource',
'ContentFilter',
'CountMessageTokensRequest',
'CountMessageTokensResponse',
'CountTextTokensRequest',
'CountTextTokensResponse',
'CreatePermissionRequest',
'CreateTunedModelMetadata',
'CreateTunedModelRequest',
'Dataset',
'DeletePermissionRequest',
'DeleteTunedModelRequest',
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
'GetPermissionRequest',
'GetTunedModelRequest',
'HarmCategory',
'Hyperparameters',
'ListModelsRequest',
'ListModelsResponse',
'ListPermissionsRequest',
'ListPermissionsResponse',
'ListTunedModelsRequest',
'ListTunedModelsResponse',
'Message',
'MessagePrompt',
'Model',
'ModelServiceClient',
'Permission',
'PermissionServiceClient',
'SafetyFeedback',
'SafetyRating',
'SafetySetting',
'TextCompletion',
'TextPrompt',
'TextServiceClient',
'TransferOwnershipRequest',
'TransferOwnershipResponse',
'TunedModel',
'TunedModelSource',
'TuningExample',
'TuningExamples',
'TuningSnapshot',
'TuningTask',
'UpdatePermissionRequest',
'UpdateTunedModelRequest',
)
