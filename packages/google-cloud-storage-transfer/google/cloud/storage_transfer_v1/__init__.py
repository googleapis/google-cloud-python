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

from .services.storage_transfer_service import StorageTransferServiceClient
from .services.storage_transfer_service import StorageTransferServiceAsyncClient

from .types.transfer import CreateAgentPoolRequest
from .types.transfer import CreateTransferJobRequest
from .types.transfer import DeleteAgentPoolRequest
from .types.transfer import GetAgentPoolRequest
from .types.transfer import GetGoogleServiceAccountRequest
from .types.transfer import GetTransferJobRequest
from .types.transfer import ListAgentPoolsRequest
from .types.transfer import ListAgentPoolsResponse
from .types.transfer import ListTransferJobsRequest
from .types.transfer import ListTransferJobsResponse
from .types.transfer import PauseTransferOperationRequest
from .types.transfer import ResumeTransferOperationRequest
from .types.transfer import RunTransferJobRequest
from .types.transfer import UpdateAgentPoolRequest
from .types.transfer import UpdateTransferJobRequest
from .types.transfer_types import AgentPool
from .types.transfer_types import AwsAccessKey
from .types.transfer_types import AwsS3Data
from .types.transfer_types import AzureBlobStorageData
from .types.transfer_types import AzureCredentials
from .types.transfer_types import ErrorLogEntry
from .types.transfer_types import ErrorSummary
from .types.transfer_types import GcsData
from .types.transfer_types import GoogleServiceAccount
from .types.transfer_types import HttpData
from .types.transfer_types import LoggingConfig
from .types.transfer_types import MetadataOptions
from .types.transfer_types import NotificationConfig
from .types.transfer_types import ObjectConditions
from .types.transfer_types import PosixFilesystem
from .types.transfer_types import Schedule
from .types.transfer_types import TransferCounters
from .types.transfer_types import TransferJob
from .types.transfer_types import TransferManifest
from .types.transfer_types import TransferOperation
from .types.transfer_types import TransferOptions
from .types.transfer_types import TransferSpec

__all__ = (
    "StorageTransferServiceAsyncClient",
    "AgentPool",
    "AwsAccessKey",
    "AwsS3Data",
    "AzureBlobStorageData",
    "AzureCredentials",
    "CreateAgentPoolRequest",
    "CreateTransferJobRequest",
    "DeleteAgentPoolRequest",
    "ErrorLogEntry",
    "ErrorSummary",
    "GcsData",
    "GetAgentPoolRequest",
    "GetGoogleServiceAccountRequest",
    "GetTransferJobRequest",
    "GoogleServiceAccount",
    "HttpData",
    "ListAgentPoolsRequest",
    "ListAgentPoolsResponse",
    "ListTransferJobsRequest",
    "ListTransferJobsResponse",
    "LoggingConfig",
    "MetadataOptions",
    "NotificationConfig",
    "ObjectConditions",
    "PauseTransferOperationRequest",
    "PosixFilesystem",
    "ResumeTransferOperationRequest",
    "RunTransferJobRequest",
    "Schedule",
    "StorageTransferServiceClient",
    "TransferCounters",
    "TransferJob",
    "TransferManifest",
    "TransferOperation",
    "TransferOptions",
    "TransferSpec",
    "UpdateAgentPoolRequest",
    "UpdateTransferJobRequest",
)
