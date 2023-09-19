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
from google.ai.generativelanguage import gapic_version as package_version

__version__ = package_version.__version__


from google.ai.generativelanguage_v1beta3.services.discuss_service.client import DiscussServiceClient
from google.ai.generativelanguage_v1beta3.services.discuss_service.async_client import DiscussServiceAsyncClient
from google.ai.generativelanguage_v1beta3.services.model_service.client import ModelServiceClient
from google.ai.generativelanguage_v1beta3.services.model_service.async_client import ModelServiceAsyncClient
from google.ai.generativelanguage_v1beta3.services.permission_service.client import PermissionServiceClient
from google.ai.generativelanguage_v1beta3.services.permission_service.async_client import PermissionServiceAsyncClient
from google.ai.generativelanguage_v1beta3.services.text_service.client import TextServiceClient
from google.ai.generativelanguage_v1beta3.services.text_service.async_client import TextServiceAsyncClient

from google.ai.generativelanguage_v1beta3.types.citation import CitationMetadata
from google.ai.generativelanguage_v1beta3.types.citation import CitationSource
from google.ai.generativelanguage_v1beta3.types.discuss_service import CountMessageTokensRequest
from google.ai.generativelanguage_v1beta3.types.discuss_service import CountMessageTokensResponse
from google.ai.generativelanguage_v1beta3.types.discuss_service import Example
from google.ai.generativelanguage_v1beta3.types.discuss_service import GenerateMessageRequest
from google.ai.generativelanguage_v1beta3.types.discuss_service import GenerateMessageResponse
from google.ai.generativelanguage_v1beta3.types.discuss_service import Message
from google.ai.generativelanguage_v1beta3.types.discuss_service import MessagePrompt
from google.ai.generativelanguage_v1beta3.types.model import Model
from google.ai.generativelanguage_v1beta3.types.model_service import CreateTunedModelMetadata
from google.ai.generativelanguage_v1beta3.types.model_service import CreateTunedModelRequest
from google.ai.generativelanguage_v1beta3.types.model_service import DeleteTunedModelRequest
from google.ai.generativelanguage_v1beta3.types.model_service import GetModelRequest
from google.ai.generativelanguage_v1beta3.types.model_service import GetTunedModelRequest
from google.ai.generativelanguage_v1beta3.types.model_service import ListModelsRequest
from google.ai.generativelanguage_v1beta3.types.model_service import ListModelsResponse
from google.ai.generativelanguage_v1beta3.types.model_service import ListTunedModelsRequest
from google.ai.generativelanguage_v1beta3.types.model_service import ListTunedModelsResponse
from google.ai.generativelanguage_v1beta3.types.model_service import UpdateTunedModelRequest
from google.ai.generativelanguage_v1beta3.types.permission import Permission
from google.ai.generativelanguage_v1beta3.types.permission_service import CreatePermissionRequest
from google.ai.generativelanguage_v1beta3.types.permission_service import DeletePermissionRequest
from google.ai.generativelanguage_v1beta3.types.permission_service import GetPermissionRequest
from google.ai.generativelanguage_v1beta3.types.permission_service import ListPermissionsRequest
from google.ai.generativelanguage_v1beta3.types.permission_service import ListPermissionsResponse
from google.ai.generativelanguage_v1beta3.types.permission_service import TransferOwnershipRequest
from google.ai.generativelanguage_v1beta3.types.permission_service import TransferOwnershipResponse
from google.ai.generativelanguage_v1beta3.types.permission_service import UpdatePermissionRequest
from google.ai.generativelanguage_v1beta3.types.safety import ContentFilter
from google.ai.generativelanguage_v1beta3.types.safety import SafetyFeedback
from google.ai.generativelanguage_v1beta3.types.safety import SafetyRating
from google.ai.generativelanguage_v1beta3.types.safety import SafetySetting
from google.ai.generativelanguage_v1beta3.types.safety import HarmCategory
from google.ai.generativelanguage_v1beta3.types.text_service import BatchEmbedTextRequest
from google.ai.generativelanguage_v1beta3.types.text_service import BatchEmbedTextResponse
from google.ai.generativelanguage_v1beta3.types.text_service import CountTextTokensRequest
from google.ai.generativelanguage_v1beta3.types.text_service import CountTextTokensResponse
from google.ai.generativelanguage_v1beta3.types.text_service import Embedding
from google.ai.generativelanguage_v1beta3.types.text_service import EmbedTextRequest
from google.ai.generativelanguage_v1beta3.types.text_service import EmbedTextResponse
from google.ai.generativelanguage_v1beta3.types.text_service import GenerateTextRequest
from google.ai.generativelanguage_v1beta3.types.text_service import GenerateTextResponse
from google.ai.generativelanguage_v1beta3.types.text_service import TextCompletion
from google.ai.generativelanguage_v1beta3.types.text_service import TextPrompt
from google.ai.generativelanguage_v1beta3.types.tuned_model import Dataset
from google.ai.generativelanguage_v1beta3.types.tuned_model import Hyperparameters
from google.ai.generativelanguage_v1beta3.types.tuned_model import TunedModel
from google.ai.generativelanguage_v1beta3.types.tuned_model import TunedModelSource
from google.ai.generativelanguage_v1beta3.types.tuned_model import TuningExample
from google.ai.generativelanguage_v1beta3.types.tuned_model import TuningExamples
from google.ai.generativelanguage_v1beta3.types.tuned_model import TuningSnapshot
from google.ai.generativelanguage_v1beta3.types.tuned_model import TuningTask

__all__ = ('DiscussServiceClient',
    'DiscussServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'PermissionServiceClient',
    'PermissionServiceAsyncClient',
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
    'CreateTunedModelMetadata',
    'CreateTunedModelRequest',
    'DeleteTunedModelRequest',
    'GetModelRequest',
    'GetTunedModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'ListTunedModelsRequest',
    'ListTunedModelsResponse',
    'UpdateTunedModelRequest',
    'Permission',
    'CreatePermissionRequest',
    'DeletePermissionRequest',
    'GetPermissionRequest',
    'ListPermissionsRequest',
    'ListPermissionsResponse',
    'TransferOwnershipRequest',
    'TransferOwnershipResponse',
    'UpdatePermissionRequest',
    'ContentFilter',
    'SafetyFeedback',
    'SafetyRating',
    'SafetySetting',
    'HarmCategory',
    'BatchEmbedTextRequest',
    'BatchEmbedTextResponse',
    'CountTextTokensRequest',
    'CountTextTokensResponse',
    'Embedding',
    'EmbedTextRequest',
    'EmbedTextResponse',
    'GenerateTextRequest',
    'GenerateTextResponse',
    'TextCompletion',
    'TextPrompt',
    'Dataset',
    'Hyperparameters',
    'TunedModel',
    'TunedModelSource',
    'TuningExample',
    'TuningExamples',
    'TuningSnapshot',
    'TuningTask',
)
