# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.client import (
    DataTransferServiceClient,
)
from google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.async_client import (
    DataTransferServiceAsyncClient,
)

from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    CheckValidCredsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    CheckValidCredsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    CreateTransferConfigRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import DataSource
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import DataSourceParameter
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    DeleteTransferConfigRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    DeleteTransferRunRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    GetDataSourceRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    GetTransferConfigRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    GetTransferRunRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListDataSourcesRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListDataSourcesResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferConfigsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferConfigsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferLogsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferLogsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferRunsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ListTransferRunsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ScheduleTransferRunsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    ScheduleTransferRunsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    StartManualTransferRunsRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    StartManualTransferRunsResponse,
)
from google.cloud.bigquery_datatransfer_v1.types.datatransfer import (
    UpdateTransferConfigRequest,
)
from google.cloud.bigquery_datatransfer_v1.types.transfer import EmailPreferences
from google.cloud.bigquery_datatransfer_v1.types.transfer import ScheduleOptions
from google.cloud.bigquery_datatransfer_v1.types.transfer import TransferConfig
from google.cloud.bigquery_datatransfer_v1.types.transfer import TransferMessage
from google.cloud.bigquery_datatransfer_v1.types.transfer import TransferRun
from google.cloud.bigquery_datatransfer_v1.types.transfer import TransferState
from google.cloud.bigquery_datatransfer_v1.types.transfer import TransferType

__all__ = (
    "DataTransferServiceClient",
    "DataTransferServiceAsyncClient",
    "CheckValidCredsRequest",
    "CheckValidCredsResponse",
    "CreateTransferConfigRequest",
    "DataSource",
    "DataSourceParameter",
    "DeleteTransferConfigRequest",
    "DeleteTransferRunRequest",
    "GetDataSourceRequest",
    "GetTransferConfigRequest",
    "GetTransferRunRequest",
    "ListDataSourcesRequest",
    "ListDataSourcesResponse",
    "ListTransferConfigsRequest",
    "ListTransferConfigsResponse",
    "ListTransferLogsRequest",
    "ListTransferLogsResponse",
    "ListTransferRunsRequest",
    "ListTransferRunsResponse",
    "ScheduleTransferRunsRequest",
    "ScheduleTransferRunsResponse",
    "StartManualTransferRunsRequest",
    "StartManualTransferRunsResponse",
    "UpdateTransferConfigRequest",
    "EmailPreferences",
    "ScheduleOptions",
    "TransferConfig",
    "TransferMessage",
    "TransferRun",
    "TransferState",
    "TransferType",
)
