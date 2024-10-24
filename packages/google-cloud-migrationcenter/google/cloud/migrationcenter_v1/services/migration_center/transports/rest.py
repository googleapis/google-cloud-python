# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.migrationcenter_v1.types import migrationcenter

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMigrationCenterRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class MigrationCenterRestInterceptor:
    """Interceptor for MigrationCenter.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MigrationCenterRestTransport.

    .. code-block:: python
        class MyCustomMigrationCenterInterceptor(MigrationCenterRestInterceptor):
            def pre_add_assets_to_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_assets_to_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_aggregate_assets_values(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregate_assets_values(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_update_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_import_data_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_import_data_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_preference_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_preference_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_import_data_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_import_data_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_preference_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_preference_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_error_frame(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_error_frame(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_import_data_file(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_import_data_file(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_preference_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_preference_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_report_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_report_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_error_frames(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_error_frames(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_import_data_files(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_import_data_files(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_import_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_import_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_preference_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_preference_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_report_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_report_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_reports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_reports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_assets_from_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_assets_from_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_report_asset_frames(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_report_asset_frames(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_preference_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_preference_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_validate_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_validate_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MigrationCenterRestTransport(interceptor=MyCustomMigrationCenterInterceptor())
        client = MigrationCenterClient(transport=transport)


    """

    def pre_add_assets_to_group(
        self,
        request: migrationcenter.AddAssetsToGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.AddAssetsToGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_assets_to_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_add_assets_to_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_assets_to_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_aggregate_assets_values(
        self,
        request: migrationcenter.AggregateAssetsValuesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.AggregateAssetsValuesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for aggregate_assets_values

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_aggregate_assets_values(
        self, response: migrationcenter.AggregateAssetsValuesResponse
    ) -> migrationcenter.AggregateAssetsValuesResponse:
        """Post-rpc interceptor for aggregate_assets_values

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_assets(
        self,
        request: migrationcenter.BatchDeleteAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.BatchDeleteAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def pre_batch_update_assets(
        self,
        request: migrationcenter.BatchUpdateAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.BatchUpdateAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_batch_update_assets(
        self, response: migrationcenter.BatchUpdateAssetsResponse
    ) -> migrationcenter.BatchUpdateAssetsResponse:
        """Post-rpc interceptor for batch_update_assets

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_group(
        self,
        request: migrationcenter.CreateGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_import_data_file(
        self,
        request: migrationcenter.CreateImportDataFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateImportDataFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_import_data_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_import_data_file(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_import_data_file

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_import_job(
        self,
        request: migrationcenter.CreateImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_import_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_preference_set(
        self,
        request: migrationcenter.CreatePreferenceSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreatePreferenceSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_preference_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_preference_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_preference_set

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_report(
        self,
        request: migrationcenter.CreateReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_report(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_report

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_report_config(
        self,
        request: migrationcenter.CreateReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_report_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_report_config

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_source(
        self,
        request: migrationcenter.CreateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.CreateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_create_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_source

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_asset(
        self,
        request: migrationcenter.DeleteAssetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def pre_delete_group(
        self,
        request: migrationcenter.DeleteGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_import_data_file(
        self,
        request: migrationcenter.DeleteImportDataFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteImportDataFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_import_data_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_import_data_file(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_import_data_file

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_import_job(
        self,
        request: migrationcenter.DeleteImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_import_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_preference_set(
        self,
        request: migrationcenter.DeletePreferenceSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeletePreferenceSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_preference_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_preference_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_preference_set

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_report(
        self,
        request: migrationcenter.DeleteReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_report(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_report

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_report_config(
        self,
        request: migrationcenter.DeleteReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_report_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_report_config

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_source(
        self,
        request: migrationcenter.DeleteSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.DeleteSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_source

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_asset(
        self,
        request: migrationcenter.GetAssetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_asset(self, response: migrationcenter.Asset) -> migrationcenter.Asset:
        """Post-rpc interceptor for get_asset

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_error_frame(
        self,
        request: migrationcenter.GetErrorFrameRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetErrorFrameRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_error_frame

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_error_frame(
        self, response: migrationcenter.ErrorFrame
    ) -> migrationcenter.ErrorFrame:
        """Post-rpc interceptor for get_error_frame

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_group(
        self,
        request: migrationcenter.GetGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_group(self, response: migrationcenter.Group) -> migrationcenter.Group:
        """Post-rpc interceptor for get_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_import_data_file(
        self,
        request: migrationcenter.GetImportDataFileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetImportDataFileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_import_data_file

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_import_data_file(
        self, response: migrationcenter.ImportDataFile
    ) -> migrationcenter.ImportDataFile:
        """Post-rpc interceptor for get_import_data_file

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_import_job(
        self,
        request: migrationcenter.GetImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_import_job(
        self, response: migrationcenter.ImportJob
    ) -> migrationcenter.ImportJob:
        """Post-rpc interceptor for get_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_preference_set(
        self,
        request: migrationcenter.GetPreferenceSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetPreferenceSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_preference_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_preference_set(
        self, response: migrationcenter.PreferenceSet
    ) -> migrationcenter.PreferenceSet:
        """Post-rpc interceptor for get_preference_set

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_report(
        self,
        request: migrationcenter.GetReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_report(
        self, response: migrationcenter.Report
    ) -> migrationcenter.Report:
        """Post-rpc interceptor for get_report

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_report_config(
        self,
        request: migrationcenter.GetReportConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetReportConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_report_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_report_config(
        self, response: migrationcenter.ReportConfig
    ) -> migrationcenter.ReportConfig:
        """Post-rpc interceptor for get_report_config

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_settings(
        self,
        request: migrationcenter.GetSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_settings(
        self, response: migrationcenter.Settings
    ) -> migrationcenter.Settings:
        """Post-rpc interceptor for get_settings

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_source(
        self,
        request: migrationcenter.GetSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.GetSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_source(
        self, response: migrationcenter.Source
    ) -> migrationcenter.Source:
        """Post-rpc interceptor for get_source

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_assets(
        self,
        request: migrationcenter.ListAssetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_assets(
        self, response: migrationcenter.ListAssetsResponse
    ) -> migrationcenter.ListAssetsResponse:
        """Post-rpc interceptor for list_assets

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_error_frames(
        self,
        request: migrationcenter.ListErrorFramesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListErrorFramesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_error_frames

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_error_frames(
        self, response: migrationcenter.ListErrorFramesResponse
    ) -> migrationcenter.ListErrorFramesResponse:
        """Post-rpc interceptor for list_error_frames

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_groups(
        self,
        request: migrationcenter.ListGroupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_groups(
        self, response: migrationcenter.ListGroupsResponse
    ) -> migrationcenter.ListGroupsResponse:
        """Post-rpc interceptor for list_groups

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_import_data_files(
        self,
        request: migrationcenter.ListImportDataFilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListImportDataFilesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_import_data_files

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_import_data_files(
        self, response: migrationcenter.ListImportDataFilesResponse
    ) -> migrationcenter.ListImportDataFilesResponse:
        """Post-rpc interceptor for list_import_data_files

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_import_jobs(
        self,
        request: migrationcenter.ListImportJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListImportJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_import_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_import_jobs(
        self, response: migrationcenter.ListImportJobsResponse
    ) -> migrationcenter.ListImportJobsResponse:
        """Post-rpc interceptor for list_import_jobs

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_preference_sets(
        self,
        request: migrationcenter.ListPreferenceSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListPreferenceSetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_preference_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_preference_sets(
        self, response: migrationcenter.ListPreferenceSetsResponse
    ) -> migrationcenter.ListPreferenceSetsResponse:
        """Post-rpc interceptor for list_preference_sets

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_report_configs(
        self,
        request: migrationcenter.ListReportConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListReportConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_report_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_report_configs(
        self, response: migrationcenter.ListReportConfigsResponse
    ) -> migrationcenter.ListReportConfigsResponse:
        """Post-rpc interceptor for list_report_configs

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_reports(
        self,
        request: migrationcenter.ListReportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListReportsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_reports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_reports(
        self, response: migrationcenter.ListReportsResponse
    ) -> migrationcenter.ListReportsResponse:
        """Post-rpc interceptor for list_reports

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_sources(
        self,
        request: migrationcenter.ListSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ListSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_sources(
        self, response: migrationcenter.ListSourcesResponse
    ) -> migrationcenter.ListSourcesResponse:
        """Post-rpc interceptor for list_sources

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_remove_assets_from_group(
        self,
        request: migrationcenter.RemoveAssetsFromGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.RemoveAssetsFromGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_assets_from_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_remove_assets_from_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_assets_from_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_report_asset_frames(
        self,
        request: migrationcenter.ReportAssetFramesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ReportAssetFramesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for report_asset_frames

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_report_asset_frames(
        self, response: migrationcenter.ReportAssetFramesResponse
    ) -> migrationcenter.ReportAssetFramesResponse:
        """Post-rpc interceptor for report_asset_frames

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_run_import_job(
        self,
        request: migrationcenter.RunImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.RunImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_run_import_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for run_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_asset(
        self,
        request: migrationcenter.UpdateAssetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdateAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_asset(
        self, response: migrationcenter.Asset
    ) -> migrationcenter.Asset:
        """Post-rpc interceptor for update_asset

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_group(
        self,
        request: migrationcenter.UpdateGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdateGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_group

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_import_job(
        self,
        request: migrationcenter.UpdateImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdateImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_import_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_preference_set(
        self,
        request: migrationcenter.UpdatePreferenceSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdatePreferenceSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_preference_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_preference_set(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_preference_set

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_settings(
        self,
        request: migrationcenter.UpdateSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdateSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_settings(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_settings

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_source(
        self,
        request: migrationcenter.UpdateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.UpdateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_update_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_source

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_validate_import_job(
        self,
        request: migrationcenter.ValidateImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[migrationcenter.ValidateImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for validate_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_validate_import_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for validate_import_job

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MigrationCenter server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the MigrationCenter server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MigrationCenterRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MigrationCenterRestInterceptor


class MigrationCenterRestTransport(_BaseMigrationCenterRestTransport):
    """REST backend synchronous transport for MigrationCenter.

    Service describing handlers for resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "migrationcenter.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MigrationCenterRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'migrationcenter.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or MigrationCenterRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AddAssetsToGroup(
        _BaseMigrationCenterRestTransport._BaseAddAssetsToGroup, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.AddAssetsToGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.AddAssetsToGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add assets to group method over HTTP.

            Args:
                request (~.migrationcenter.AddAssetsToGroupRequest):
                    The request object. A request to add assets to a group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseAddAssetsToGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_assets_to_group(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseAddAssetsToGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseAddAssetsToGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseAddAssetsToGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._AddAssetsToGroup._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_add_assets_to_group(resp)
            return resp

    class _AggregateAssetsValues(
        _BaseMigrationCenterRestTransport._BaseAggregateAssetsValues,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.AggregateAssetsValues")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.AggregateAssetsValuesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.AggregateAssetsValuesResponse:
            r"""Call the aggregate assets values method over HTTP.

            Args:
                request (~.migrationcenter.AggregateAssetsValuesRequest):
                    The request object. A request to aggregate one or more
                values.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.AggregateAssetsValuesResponse:
                    A response to a request to aggregated
                assets values.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseAggregateAssetsValues._get_http_options()
            )
            request, metadata = self._interceptor.pre_aggregate_assets_values(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseAggregateAssetsValues._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseAggregateAssetsValues._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseAggregateAssetsValues._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                MigrationCenterRestTransport._AggregateAssetsValues._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.AggregateAssetsValuesResponse()
            pb_resp = migrationcenter.AggregateAssetsValuesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregate_assets_values(resp)
            return resp

    class _BatchDeleteAssets(
        _BaseMigrationCenterRestTransport._BaseBatchDeleteAssets,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.BatchDeleteAssets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.BatchDeleteAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the batch delete assets method over HTTP.

            Args:
                request (~.migrationcenter.BatchDeleteAssetsRequest):
                    The request object. A request to delete a list of  asset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseBatchDeleteAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_delete_assets(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseBatchDeleteAssets._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseBatchDeleteAssets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseBatchDeleteAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._BatchDeleteAssets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _BatchUpdateAssets(
        _BaseMigrationCenterRestTransport._BaseBatchUpdateAssets,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.BatchUpdateAssets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.BatchUpdateAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.BatchUpdateAssetsResponse:
            r"""Call the batch update assets method over HTTP.

            Args:
                request (~.migrationcenter.BatchUpdateAssetsRequest):
                    The request object. A request to update a list of assets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.BatchUpdateAssetsResponse:
                    Response for updating a list of
                assets.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseBatchUpdateAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_batch_update_assets(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseBatchUpdateAssets._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseBatchUpdateAssets._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseBatchUpdateAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._BatchUpdateAssets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.BatchUpdateAssetsResponse()
            pb_resp = migrationcenter.BatchUpdateAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_assets(resp)
            return resp

    class _CreateGroup(
        _BaseMigrationCenterRestTransport._BaseCreateGroup, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create group method over HTTP.

            Args:
                request (~.migrationcenter.CreateGroupRequest):
                    The request object. A request to create a group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_group(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateGroup._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_group(resp)
            return resp

    class _CreateImportDataFile(
        _BaseMigrationCenterRestTransport._BaseCreateImportDataFile,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateImportDataFile")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateImportDataFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create import data file method over HTTP.

            Args:
                request (~.migrationcenter.CreateImportDataFileRequest):
                    The request object. A request to create an ``ImportDataFile`` resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateImportDataFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_import_data_file(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateImportDataFile._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateImportDataFile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateImportDataFile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateImportDataFile._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_import_data_file(resp)
            return resp

    class _CreateImportJob(
        _BaseMigrationCenterRestTransport._BaseCreateImportJob, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create import job method over HTTP.

            Args:
                request (~.migrationcenter.CreateImportJobRequest):
                    The request object. A request to create an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_import_job(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateImportJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateImportJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_import_job(resp)
            return resp

    class _CreatePreferenceSet(
        _BaseMigrationCenterRestTransport._BaseCreatePreferenceSet,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreatePreferenceSet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreatePreferenceSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create preference set method over HTTP.

            Args:
                request (~.migrationcenter.CreatePreferenceSetRequest):
                    The request object. A request to create a preference set.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreatePreferenceSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_preference_set(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreatePreferenceSet._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreatePreferenceSet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreatePreferenceSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreatePreferenceSet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_preference_set(resp)
            return resp

    class _CreateReport(
        _BaseMigrationCenterRestTransport._BaseCreateReport, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateReport")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create report method over HTTP.

            Args:
                request (~.migrationcenter.CreateReportRequest):
                    The request object. Message for creating a Report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_report(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateReport._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_report(resp)
            return resp

    class _CreateReportConfig(
        _BaseMigrationCenterRestTransport._BaseCreateReportConfig,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateReportConfig")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create report config method over HTTP.

            Args:
                request (~.migrationcenter.CreateReportConfigRequest):
                    The request object. A request to create a ``ReportConfig`` resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_report_config(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateReportConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateReportConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateReportConfig._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_report_config(resp)
            return resp

    class _CreateSource(
        _BaseMigrationCenterRestTransport._BaseCreateSource, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CreateSource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.CreateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create source method over HTTP.

            Args:
                request (~.migrationcenter.CreateSourceRequest):
                    The request object. A request to create a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCreateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_source(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCreateSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCreateSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCreateSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CreateSource._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_source(resp)
            return resp

    class _DeleteAsset(
        _BaseMigrationCenterRestTransport._BaseDeleteAsset, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete asset method over HTTP.

            Args:
                request (~.migrationcenter.DeleteAssetRequest):
                    The request object. A request to delete an asset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_asset(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteAsset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteGroup(
        _BaseMigrationCenterRestTransport._BaseDeleteGroup, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete group method over HTTP.

            Args:
                request (~.migrationcenter.DeleteGroupRequest):
                    The request object. A request to delete a group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_group(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteGroup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteGroup._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_group(resp)
            return resp

    class _DeleteImportDataFile(
        _BaseMigrationCenterRestTransport._BaseDeleteImportDataFile,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteImportDataFile")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteImportDataFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete import data file method over HTTP.

            Args:
                request (~.migrationcenter.DeleteImportDataFileRequest):
                    The request object. A request to delete an ``ImportDataFile`` resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteImportDataFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_import_data_file(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteImportDataFile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteImportDataFile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteImportDataFile._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_import_data_file(resp)
            return resp

    class _DeleteImportJob(
        _BaseMigrationCenterRestTransport._BaseDeleteImportJob, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete import job method over HTTP.

            Args:
                request (~.migrationcenter.DeleteImportJobRequest):
                    The request object. A request to delete an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_import_job(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteImportJob._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_import_job(resp)
            return resp

    class _DeletePreferenceSet(
        _BaseMigrationCenterRestTransport._BaseDeletePreferenceSet,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeletePreferenceSet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeletePreferenceSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete preference set method over HTTP.

            Args:
                request (~.migrationcenter.DeletePreferenceSetRequest):
                    The request object. A request to delete a preference set.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeletePreferenceSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_preference_set(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeletePreferenceSet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeletePreferenceSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeletePreferenceSet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_preference_set(resp)
            return resp

    class _DeleteReport(
        _BaseMigrationCenterRestTransport._BaseDeleteReport, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteReport")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete report method over HTTP.

            Args:
                request (~.migrationcenter.DeleteReportRequest):
                    The request object. A request to delete a Report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_report(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteReport._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_report(resp)
            return resp

    class _DeleteReportConfig(
        _BaseMigrationCenterRestTransport._BaseDeleteReportConfig,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteReportConfig")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete report config method over HTTP.

            Args:
                request (~.migrationcenter.DeleteReportConfigRequest):
                    The request object. A request to delete a ReportConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_report_config(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteReportConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteReportConfig._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_report_config(resp)
            return resp

    class _DeleteSource(
        _BaseMigrationCenterRestTransport._BaseDeleteSource, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteSource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.DeleteSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete source method over HTTP.

            Args:
                request (~.migrationcenter.DeleteSourceRequest):
                    The request object. A request to delete a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_source(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteSource._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_source(resp)
            return resp

    class _GetAsset(
        _BaseMigrationCenterRestTransport._BaseGetAsset, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Asset:
            r"""Call the get asset method over HTTP.

            Args:
                request (~.migrationcenter.GetAssetRequest):
                    The request object. Message for getting a Asset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Asset:
                    An asset represents a resource in
                your environment. Asset types include
                virtual machines and databases.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_asset(request, metadata)
            transcoded_request = (
                _BaseMigrationCenterRestTransport._BaseGetAsset._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseMigrationCenterRestTransport._BaseGetAsset._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = MigrationCenterRestTransport._GetAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Asset()
            pb_resp = migrationcenter.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_asset(resp)
            return resp

    class _GetErrorFrame(
        _BaseMigrationCenterRestTransport._BaseGetErrorFrame, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetErrorFrame")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetErrorFrameRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ErrorFrame:
            r"""Call the get error frame method over HTTP.

            Args:
                request (~.migrationcenter.GetErrorFrameRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ErrorFrame:
                    Message representing a frame which
                failed to be processed due to an error.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetErrorFrame._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_error_frame(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetErrorFrame._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetErrorFrame._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetErrorFrame._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ErrorFrame()
            pb_resp = migrationcenter.ErrorFrame.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_error_frame(resp)
            return resp

    class _GetGroup(
        _BaseMigrationCenterRestTransport._BaseGetGroup, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Group:
            r"""Call the get group method over HTTP.

            Args:
                request (~.migrationcenter.GetGroupRequest):
                    The request object. A request to get a group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Group:
                    A resource that represents an asset
                group. The purpose of an asset group is
                to bundle a set of assets that have
                something in common, while allowing
                users to add annotations to the group.
                An asset can belong to multiple groups.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_group(request, metadata)
            transcoded_request = (
                _BaseMigrationCenterRestTransport._BaseGetGroup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseMigrationCenterRestTransport._BaseGetGroup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = MigrationCenterRestTransport._GetGroup._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Group()
            pb_resp = migrationcenter.Group.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_group(resp)
            return resp

    class _GetImportDataFile(
        _BaseMigrationCenterRestTransport._BaseGetImportDataFile,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetImportDataFile")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetImportDataFileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ImportDataFile:
            r"""Call the get import data file method over HTTP.

            Args:
                request (~.migrationcenter.GetImportDataFileRequest):
                    The request object. A request to get an import data file.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ImportDataFile:
                    A resource that represents a payload
                file in an import job.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetImportDataFile._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_import_data_file(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetImportDataFile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetImportDataFile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetImportDataFile._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ImportDataFile()
            pb_resp = migrationcenter.ImportDataFile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_import_data_file(resp)
            return resp

    class _GetImportJob(
        _BaseMigrationCenterRestTransport._BaseGetImportJob, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ImportJob:
            r"""Call the get import job method over HTTP.

            Args:
                request (~.migrationcenter.GetImportJobRequest):
                    The request object. A request to get an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ImportJob:
                    A resource that represents the
                background job that imports asset
                frames.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_import_job(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetImportJob._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ImportJob()
            pb_resp = migrationcenter.ImportJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_import_job(resp)
            return resp

    class _GetPreferenceSet(
        _BaseMigrationCenterRestTransport._BaseGetPreferenceSet, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetPreferenceSet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetPreferenceSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.PreferenceSet:
            r"""Call the get preference set method over HTTP.

            Args:
                request (~.migrationcenter.GetPreferenceSetRequest):
                    The request object. A request to get a preference set.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.PreferenceSet:
                    The preferences that apply to all
                assets in a given context.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetPreferenceSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_preference_set(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetPreferenceSet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetPreferenceSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetPreferenceSet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.PreferenceSet()
            pb_resp = migrationcenter.PreferenceSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_preference_set(resp)
            return resp

    class _GetReport(
        _BaseMigrationCenterRestTransport._BaseGetReport, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetReport")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Report:
            r"""Call the get report method over HTTP.

            Args:
                request (~.migrationcenter.GetReportRequest):
                    The request object. A request to get a Report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Report:
                    Report represents a point-in-time
                rendering of the ReportConfig results.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_report(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseMigrationCenterRestTransport._BaseGetReport._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = MigrationCenterRestTransport._GetReport._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Report()
            pb_resp = migrationcenter.Report.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_report(resp)
            return resp

    class _GetReportConfig(
        _BaseMigrationCenterRestTransport._BaseGetReportConfig, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetReportConfig")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetReportConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ReportConfig:
            r"""Call the get report config method over HTTP.

            Args:
                request (~.migrationcenter.GetReportConfigRequest):
                    The request object. A request to get a ``ReportConfig`` resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ReportConfig:
                    The groups and associated preference
                sets on which we can generate reports.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetReportConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_report_config(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetReportConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetReportConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetReportConfig._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ReportConfig()
            pb_resp = migrationcenter.ReportConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_report_config(resp)
            return resp

    class _GetSettings(
        _BaseMigrationCenterRestTransport._BaseGetSettings, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetSettings")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Settings:
            r"""Call the get settings method over HTTP.

            Args:
                request (~.migrationcenter.GetSettingsRequest):
                    The request object. A request to get the settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Settings:
                    Describes the Migration Center
                settings related to the project.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_settings(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetSettings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetSettings._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Settings()
            pb_resp = migrationcenter.Settings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_settings(resp)
            return resp

    class _GetSource(
        _BaseMigrationCenterRestTransport._BaseGetSource, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetSource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.GetSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Source:
            r"""Call the get source method over HTTP.

            Args:
                request (~.migrationcenter.GetSourceRequest):
                    The request object. A request to get a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Source:
                    Source represents an object from
                which asset information is streamed to
                Migration Center.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_source(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetSource._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseMigrationCenterRestTransport._BaseGetSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = MigrationCenterRestTransport._GetSource._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Source()
            pb_resp = migrationcenter.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_source(resp)
            return resp

    class _ListAssets(
        _BaseMigrationCenterRestTransport._BaseListAssets, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListAssets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListAssetsResponse:
            r"""Call the list assets method over HTTP.

            Args:
                request (~.migrationcenter.ListAssetsRequest):
                    The request object. Message for requesting a list of
                assets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListAssetsResponse:
                    Response message for listing assets.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_assets(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListAssets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListAssets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListAssetsResponse()
            pb_resp = migrationcenter.ListAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_assets(resp)
            return resp

    class _ListErrorFrames(
        _BaseMigrationCenterRestTransport._BaseListErrorFrames, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListErrorFrames")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListErrorFramesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListErrorFramesResponse:
            r"""Call the list error frames method over HTTP.

            Args:
                request (~.migrationcenter.ListErrorFramesRequest):
                    The request object. A request to list error frames for a
                source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListErrorFramesResponse:
                    A response for listing error frames.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListErrorFrames._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_error_frames(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListErrorFrames._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListErrorFrames._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListErrorFrames._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListErrorFramesResponse()
            pb_resp = migrationcenter.ListErrorFramesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_error_frames(resp)
            return resp

    class _ListGroups(
        _BaseMigrationCenterRestTransport._BaseListGroups, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListGroups")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListGroupsResponse:
            r"""Call the list groups method over HTTP.

            Args:
                request (~.migrationcenter.ListGroupsRequest):
                    The request object. A request to list groups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListGroupsResponse:
                    A response for listing groups.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListGroups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_groups(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListGroups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListGroups._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListGroups._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListGroupsResponse()
            pb_resp = migrationcenter.ListGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_groups(resp)
            return resp

    class _ListImportDataFiles(
        _BaseMigrationCenterRestTransport._BaseListImportDataFiles,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListImportDataFiles")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListImportDataFilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListImportDataFilesResponse:
            r"""Call the list import data files method over HTTP.

            Args:
                request (~.migrationcenter.ListImportDataFilesRequest):
                    The request object. A request to list import data files
                of an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListImportDataFilesResponse:
                    Response for listing payload files of
                an import job.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListImportDataFiles._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_import_data_files(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListImportDataFiles._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListImportDataFiles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListImportDataFiles._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListImportDataFilesResponse()
            pb_resp = migrationcenter.ListImportDataFilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_import_data_files(resp)
            return resp

    class _ListImportJobs(
        _BaseMigrationCenterRestTransport._BaseListImportJobs, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListImportJobs")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListImportJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListImportJobsResponse:
            r"""Call the list import jobs method over HTTP.

            Args:
                request (~.migrationcenter.ListImportJobsRequest):
                    The request object. A request to list import jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListImportJobsResponse:
                    A response for listing import jobs.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListImportJobs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_import_jobs(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListImportJobs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListImportJobs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListImportJobs._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListImportJobsResponse()
            pb_resp = migrationcenter.ListImportJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_import_jobs(resp)
            return resp

    class _ListPreferenceSets(
        _BaseMigrationCenterRestTransport._BaseListPreferenceSets,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListPreferenceSets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListPreferenceSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListPreferenceSetsResponse:
            r"""Call the list preference sets method over HTTP.

            Args:
                request (~.migrationcenter.ListPreferenceSetsRequest):
                    The request object. Request for listing preference sets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListPreferenceSetsResponse:
                    Response message for listing
                preference sets.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListPreferenceSets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_preference_sets(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListPreferenceSets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListPreferenceSets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListPreferenceSets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListPreferenceSetsResponse()
            pb_resp = migrationcenter.ListPreferenceSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_preference_sets(resp)
            return resp

    class _ListReportConfigs(
        _BaseMigrationCenterRestTransport._BaseListReportConfigs,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListReportConfigs")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListReportConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListReportConfigsResponse:
            r"""Call the list report configs method over HTTP.

            Args:
                request (~.migrationcenter.ListReportConfigsRequest):
                    The request object. A request to get a list of ``ReportConfig`` resources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListReportConfigsResponse:
                    Response message for listing report
                configs.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListReportConfigs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_report_configs(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListReportConfigs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListReportConfigs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListReportConfigs._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListReportConfigsResponse()
            pb_resp = migrationcenter.ListReportConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_report_configs(resp)
            return resp

    class _ListReports(
        _BaseMigrationCenterRestTransport._BaseListReports, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListReports")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListReportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListReportsResponse:
            r"""Call the list reports method over HTTP.

            Args:
                request (~.migrationcenter.ListReportsRequest):
                    The request object. A request for a list of Reports.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListReportsResponse:
                    Response message for listing Reports.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListReports._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_reports(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListReports._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListReports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListReports._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListReportsResponse()
            pb_resp = migrationcenter.ListReportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_reports(resp)
            return resp

    class _ListSources(
        _BaseMigrationCenterRestTransport._BaseListSources, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListSources")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ListSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ListSourcesResponse:
            r"""Call the list sources method over HTTP.

            Args:
                request (~.migrationcenter.ListSourcesRequest):
                    The request object. A request for a list of sources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ListSourcesResponse:
                    Response message for listing sources.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_sources(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListSources._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListSources._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListSources._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ListSourcesResponse()
            pb_resp = migrationcenter.ListSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sources(resp)
            return resp

    class _RemoveAssetsFromGroup(
        _BaseMigrationCenterRestTransport._BaseRemoveAssetsFromGroup,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.RemoveAssetsFromGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.RemoveAssetsFromGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove assets from group method over HTTP.

            Args:
                request (~.migrationcenter.RemoveAssetsFromGroupRequest):
                    The request object. A request to remove assets from a
                group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseRemoveAssetsFromGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_assets_from_group(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseRemoveAssetsFromGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseRemoveAssetsFromGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseRemoveAssetsFromGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                MigrationCenterRestTransport._RemoveAssetsFromGroup._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_remove_assets_from_group(resp)
            return resp

    class _ReportAssetFrames(
        _BaseMigrationCenterRestTransport._BaseReportAssetFrames,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ReportAssetFrames")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ReportAssetFramesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.ReportAssetFramesResponse:
            r"""Call the report asset frames method over HTTP.

            Args:
                request (~.migrationcenter.ReportAssetFramesRequest):
                    The request object. A request to report a set of asset
                frames.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.ReportAssetFramesResponse:
                    A response to a call to ``ReportAssetFrame``.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseReportAssetFrames._get_http_options()
            )
            request, metadata = self._interceptor.pre_report_asset_frames(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseReportAssetFrames._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseReportAssetFrames._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseReportAssetFrames._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ReportAssetFrames._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.ReportAssetFramesResponse()
            pb_resp = migrationcenter.ReportAssetFramesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_report_asset_frames(resp)
            return resp

    class _RunImportJob(
        _BaseMigrationCenterRestTransport._BaseRunImportJob, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.RunImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.RunImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the run import job method over HTTP.

            Args:
                request (~.migrationcenter.RunImportJobRequest):
                    The request object. A request to run an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseRunImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_import_job(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseRunImportJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseRunImportJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseRunImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._RunImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_import_job(resp)
            return resp

    class _UpdateAsset(
        _BaseMigrationCenterRestTransport._BaseUpdateAsset, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdateAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdateAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> migrationcenter.Asset:
            r"""Call the update asset method over HTTP.

            Args:
                request (~.migrationcenter.UpdateAssetRequest):
                    The request object. A request to update an asset.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.migrationcenter.Asset:
                    An asset represents a resource in
                your environment. Asset types include
                virtual machines and databases.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdateAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_asset(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdateAsset._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdateAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdateAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdateAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = migrationcenter.Asset()
            pb_resp = migrationcenter.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_asset(resp)
            return resp

    class _UpdateGroup(
        _BaseMigrationCenterRestTransport._BaseUpdateGroup, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdateGroup")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdateGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update group method over HTTP.

            Args:
                request (~.migrationcenter.UpdateGroupRequest):
                    The request object. A request to update a group.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdateGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_group(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdateGroup._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdateGroup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdateGroup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdateGroup._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_group(resp)
            return resp

    class _UpdateImportJob(
        _BaseMigrationCenterRestTransport._BaseUpdateImportJob, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdateImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdateImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update import job method over HTTP.

            Args:
                request (~.migrationcenter.UpdateImportJobRequest):
                    The request object. A request to update an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdateImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_import_job(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdateImportJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdateImportJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdateImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdateImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_import_job(resp)
            return resp

    class _UpdatePreferenceSet(
        _BaseMigrationCenterRestTransport._BaseUpdatePreferenceSet,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdatePreferenceSet")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdatePreferenceSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update preference set method over HTTP.

            Args:
                request (~.migrationcenter.UpdatePreferenceSetRequest):
                    The request object. A request to update a preference set.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdatePreferenceSet._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_preference_set(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdatePreferenceSet._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdatePreferenceSet._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdatePreferenceSet._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdatePreferenceSet._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_preference_set(resp)
            return resp

    class _UpdateSettings(
        _BaseMigrationCenterRestTransport._BaseUpdateSettings, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdateSettings")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdateSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update settings method over HTTP.

            Args:
                request (~.migrationcenter.UpdateSettingsRequest):
                    The request object. A request to update the settings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdateSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_settings(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdateSettings._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdateSettings._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdateSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdateSettings._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_settings(resp)
            return resp

    class _UpdateSource(
        _BaseMigrationCenterRestTransport._BaseUpdateSource, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.UpdateSource")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.UpdateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update source method over HTTP.

            Args:
                request (~.migrationcenter.UpdateSourceRequest):
                    The request object. A request to update a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseUpdateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_source(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseUpdateSource._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseUpdateSource._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseUpdateSource._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._UpdateSource._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_source(resp)
            return resp

    class _ValidateImportJob(
        _BaseMigrationCenterRestTransport._BaseValidateImportJob,
        MigrationCenterRestStub,
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ValidateImportJob")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: migrationcenter.ValidateImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the validate import job method over HTTP.

            Args:
                request (~.migrationcenter.ValidateImportJobRequest):
                    The request object. A request to validate an import job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseValidateImportJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_validate_import_job(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseValidateImportJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseValidateImportJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseValidateImportJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ValidateImportJob._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_validate_import_job(resp)
            return resp

    @property
    def add_assets_to_group(
        self,
    ) -> Callable[[migrationcenter.AddAssetsToGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddAssetsToGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def aggregate_assets_values(
        self,
    ) -> Callable[
        [migrationcenter.AggregateAssetsValuesRequest],
        migrationcenter.AggregateAssetsValuesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregateAssetsValues(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_assets(
        self,
    ) -> Callable[[migrationcenter.BatchDeleteAssetsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_assets(
        self,
    ) -> Callable[
        [migrationcenter.BatchUpdateAssetsRequest],
        migrationcenter.BatchUpdateAssetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_group(
        self,
    ) -> Callable[[migrationcenter.CreateGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_import_data_file(
        self,
    ) -> Callable[
        [migrationcenter.CreateImportDataFileRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateImportDataFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_import_job(
        self,
    ) -> Callable[[migrationcenter.CreateImportJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_preference_set(
        self,
    ) -> Callable[
        [migrationcenter.CreatePreferenceSetRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePreferenceSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_report(
        self,
    ) -> Callable[[migrationcenter.CreateReportRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_report_config(
        self,
    ) -> Callable[
        [migrationcenter.CreateReportConfigRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_source(
        self,
    ) -> Callable[[migrationcenter.CreateSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_asset(
        self,
    ) -> Callable[[migrationcenter.DeleteAssetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_group(
        self,
    ) -> Callable[[migrationcenter.DeleteGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_import_data_file(
        self,
    ) -> Callable[
        [migrationcenter.DeleteImportDataFileRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteImportDataFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_import_job(
        self,
    ) -> Callable[[migrationcenter.DeleteImportJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_preference_set(
        self,
    ) -> Callable[
        [migrationcenter.DeletePreferenceSetRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePreferenceSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_report(
        self,
    ) -> Callable[[migrationcenter.DeleteReportRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_report_config(
        self,
    ) -> Callable[
        [migrationcenter.DeleteReportConfigRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_source(
        self,
    ) -> Callable[[migrationcenter.DeleteSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_asset(
        self,
    ) -> Callable[[migrationcenter.GetAssetRequest], migrationcenter.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_error_frame(
        self,
    ) -> Callable[[migrationcenter.GetErrorFrameRequest], migrationcenter.ErrorFrame]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetErrorFrame(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_group(
        self,
    ) -> Callable[[migrationcenter.GetGroupRequest], migrationcenter.Group]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_import_data_file(
        self,
    ) -> Callable[
        [migrationcenter.GetImportDataFileRequest], migrationcenter.ImportDataFile
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetImportDataFile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_import_job(
        self,
    ) -> Callable[[migrationcenter.GetImportJobRequest], migrationcenter.ImportJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_preference_set(
        self,
    ) -> Callable[
        [migrationcenter.GetPreferenceSetRequest], migrationcenter.PreferenceSet
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPreferenceSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_report(
        self,
    ) -> Callable[[migrationcenter.GetReportRequest], migrationcenter.Report]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_report_config(
        self,
    ) -> Callable[
        [migrationcenter.GetReportConfigRequest], migrationcenter.ReportConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReportConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_settings(
        self,
    ) -> Callable[[migrationcenter.GetSettingsRequest], migrationcenter.Settings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_source(
        self,
    ) -> Callable[[migrationcenter.GetSourceRequest], migrationcenter.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_assets(
        self,
    ) -> Callable[
        [migrationcenter.ListAssetsRequest], migrationcenter.ListAssetsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_error_frames(
        self,
    ) -> Callable[
        [migrationcenter.ListErrorFramesRequest],
        migrationcenter.ListErrorFramesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListErrorFrames(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_groups(
        self,
    ) -> Callable[
        [migrationcenter.ListGroupsRequest], migrationcenter.ListGroupsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_import_data_files(
        self,
    ) -> Callable[
        [migrationcenter.ListImportDataFilesRequest],
        migrationcenter.ListImportDataFilesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListImportDataFiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_import_jobs(
        self,
    ) -> Callable[
        [migrationcenter.ListImportJobsRequest], migrationcenter.ListImportJobsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListImportJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_preference_sets(
        self,
    ) -> Callable[
        [migrationcenter.ListPreferenceSetsRequest],
        migrationcenter.ListPreferenceSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPreferenceSets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_report_configs(
        self,
    ) -> Callable[
        [migrationcenter.ListReportConfigsRequest],
        migrationcenter.ListReportConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReportConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_reports(
        self,
    ) -> Callable[
        [migrationcenter.ListReportsRequest], migrationcenter.ListReportsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sources(
        self,
    ) -> Callable[
        [migrationcenter.ListSourcesRequest], migrationcenter.ListSourcesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_assets_from_group(
        self,
    ) -> Callable[
        [migrationcenter.RemoveAssetsFromGroupRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveAssetsFromGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def report_asset_frames(
        self,
    ) -> Callable[
        [migrationcenter.ReportAssetFramesRequest],
        migrationcenter.ReportAssetFramesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReportAssetFrames(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_import_job(
        self,
    ) -> Callable[[migrationcenter.RunImportJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_asset(
        self,
    ) -> Callable[[migrationcenter.UpdateAssetRequest], migrationcenter.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_group(
        self,
    ) -> Callable[[migrationcenter.UpdateGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_import_job(
        self,
    ) -> Callable[[migrationcenter.UpdateImportJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_preference_set(
        self,
    ) -> Callable[
        [migrationcenter.UpdatePreferenceSetRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePreferenceSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_settings(
        self,
    ) -> Callable[[migrationcenter.UpdateSettingsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_source(
        self,
    ) -> Callable[[migrationcenter.UpdateSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def validate_import_job(
        self,
    ) -> Callable[[migrationcenter.ValidateImportJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ValidateImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseMigrationCenterRestTransport._BaseGetLocation, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseMigrationCenterRestTransport._BaseListLocations, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseMigrationCenterRestTransport._BaseCancelOperation, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseMigrationCenterRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseMigrationCenterRestTransport._BaseDeleteOperation, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseMigrationCenterRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._DeleteOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseMigrationCenterRestTransport._BaseGetOperation, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseMigrationCenterRestTransport._BaseListOperations, MigrationCenterRestStub
    ):
        def __hash__(self):
            return hash("MigrationCenterRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseMigrationCenterRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseMigrationCenterRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMigrationCenterRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = MigrationCenterRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MigrationCenterRestTransport",)
