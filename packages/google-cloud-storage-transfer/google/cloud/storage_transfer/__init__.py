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

from google.cloud.storage_transfer_v1.services.storage_transfer_service.client import (
    StorageTransferServiceClient,
)
from google.cloud.storage_transfer_v1.services.storage_transfer_service.async_client import (
    StorageTransferServiceAsyncClient,
)

from google.cloud.storage_transfer_v1.types.transfer import CreateTransferJobRequest
from google.cloud.storage_transfer_v1.types.transfer import (
    GetGoogleServiceAccountRequest,
)
from google.cloud.storage_transfer_v1.types.transfer import GetTransferJobRequest
from google.cloud.storage_transfer_v1.types.transfer import ListTransferJobsRequest
from google.cloud.storage_transfer_v1.types.transfer import ListTransferJobsResponse
from google.cloud.storage_transfer_v1.types.transfer import (
    PauseTransferOperationRequest,
)
from google.cloud.storage_transfer_v1.types.transfer import (
    ResumeTransferOperationRequest,
)
from google.cloud.storage_transfer_v1.types.transfer import RunTransferJobRequest
from google.cloud.storage_transfer_v1.types.transfer import UpdateTransferJobRequest
from google.cloud.storage_transfer_v1.types.transfer_types import AwsAccessKey
from google.cloud.storage_transfer_v1.types.transfer_types import AwsS3Data
from google.cloud.storage_transfer_v1.types.transfer_types import AzureBlobStorageData
from google.cloud.storage_transfer_v1.types.transfer_types import AzureCredentials
from google.cloud.storage_transfer_v1.types.transfer_types import ErrorLogEntry
from google.cloud.storage_transfer_v1.types.transfer_types import ErrorSummary
from google.cloud.storage_transfer_v1.types.transfer_types import GcsData
from google.cloud.storage_transfer_v1.types.transfer_types import GoogleServiceAccount
from google.cloud.storage_transfer_v1.types.transfer_types import HttpData
from google.cloud.storage_transfer_v1.types.transfer_types import NotificationConfig
from google.cloud.storage_transfer_v1.types.transfer_types import ObjectConditions
from google.cloud.storage_transfer_v1.types.transfer_types import Schedule
from google.cloud.storage_transfer_v1.types.transfer_types import TransferCounters
from google.cloud.storage_transfer_v1.types.transfer_types import TransferJob
from google.cloud.storage_transfer_v1.types.transfer_types import TransferOperation
from google.cloud.storage_transfer_v1.types.transfer_types import TransferOptions
from google.cloud.storage_transfer_v1.types.transfer_types import TransferSpec

__all__ = (
    "StorageTransferServiceClient",
    "StorageTransferServiceAsyncClient",
    "CreateTransferJobRequest",
    "GetGoogleServiceAccountRequest",
    "GetTransferJobRequest",
    "ListTransferJobsRequest",
    "ListTransferJobsResponse",
    "PauseTransferOperationRequest",
    "ResumeTransferOperationRequest",
    "RunTransferJobRequest",
    "UpdateTransferJobRequest",
    "AwsAccessKey",
    "AwsS3Data",
    "AzureBlobStorageData",
    "AzureCredentials",
    "ErrorLogEntry",
    "ErrorSummary",
    "GcsData",
    "GoogleServiceAccount",
    "HttpData",
    "NotificationConfig",
    "ObjectConditions",
    "Schedule",
    "TransferCounters",
    "TransferJob",
    "TransferOperation",
    "TransferOptions",
    "TransferSpec",
)
