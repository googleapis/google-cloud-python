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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.metastore_v1.types import metastore

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDataprocMetastoreRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DataprocMetastoreRestInterceptor:
    """Interceptor for DataprocMetastore.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataprocMetastoreRestTransport.

    .. code-block:: python
        class MyCustomDataprocMetastoreInterceptor(DataprocMetastoreRestInterceptor):
            def pre_alter_metadata_resource_location(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_alter_metadata_resource_location(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_metadata_import(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_metadata_import(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_metadata_import(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_metadata_import(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_metadata_imports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_metadata_imports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_services(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_services(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_move_table_to_database(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_move_table_to_database(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_query_metadata(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_query_metadata(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_service(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_metadata_import(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_metadata_import(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_service(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_service(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataprocMetastoreRestTransport(interceptor=MyCustomDataprocMetastoreInterceptor())
        client = DataprocMetastoreClient(transport=transport)


    """

    def pre_alter_metadata_resource_location(
        self,
        request: metastore.AlterMetadataResourceLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        metastore.AlterMetadataResourceLocationRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for alter_metadata_resource_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_alter_metadata_resource_location(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for alter_metadata_resource_location

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup(
        self,
        request: metastore.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_create_metadata_import(
        self,
        request: metastore.CreateMetadataImportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.CreateMetadataImportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_metadata_import

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_create_metadata_import(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_metadata_import

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_create_service(
        self,
        request: metastore.CreateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.CreateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_create_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_service

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: metastore.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_delete_service(
        self,
        request: metastore.DeleteServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.DeleteServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_delete_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_service

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_export_metadata(
        self,
        request: metastore.ExportMetadataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.ExportMetadataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_metadata

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_export_metadata(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_metadata

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self, request: metastore.GetBackupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_backup(self, response: metastore.Backup) -> metastore.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_get_metadata_import(
        self,
        request: metastore.GetMetadataImportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.GetMetadataImportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_metadata_import

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_metadata_import(
        self, response: metastore.MetadataImport
    ) -> metastore.MetadataImport:
        """Post-rpc interceptor for get_metadata_import

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_get_service(
        self, request: metastore.GetServiceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.GetServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_service(self, response: metastore.Service) -> metastore.Service:
        """Post-rpc interceptor for get_service

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self, request: metastore.ListBackupsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[metastore.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_list_backups(
        self, response: metastore.ListBackupsResponse
    ) -> metastore.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_list_metadata_imports(
        self,
        request: metastore.ListMetadataImportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.ListMetadataImportsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_metadata_imports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_list_metadata_imports(
        self, response: metastore.ListMetadataImportsResponse
    ) -> metastore.ListMetadataImportsResponse:
        """Post-rpc interceptor for list_metadata_imports

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_list_services(
        self,
        request: metastore.ListServicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.ListServicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_services

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_list_services(
        self, response: metastore.ListServicesResponse
    ) -> metastore.ListServicesResponse:
        """Post-rpc interceptor for list_services

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_move_table_to_database(
        self,
        request: metastore.MoveTableToDatabaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.MoveTableToDatabaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for move_table_to_database

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_move_table_to_database(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for move_table_to_database

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_query_metadata(
        self,
        request: metastore.QueryMetadataRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.QueryMetadataRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for query_metadata

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_query_metadata(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for query_metadata

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_restore_service(
        self,
        request: metastore.RestoreServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.RestoreServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for restore_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_restore_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_service

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_update_metadata_import(
        self,
        request: metastore.UpdateMetadataImportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.UpdateMetadataImportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_metadata_import

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_update_metadata_import(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_metadata_import

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_update_service(
        self,
        request: metastore.UpdateServiceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[metastore.UpdateServiceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_service

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_update_service(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_service

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
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
        before they are sent to the DataprocMetastore server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the DataprocMetastore server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataprocMetastoreRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataprocMetastoreRestInterceptor


class DataprocMetastoreRestTransport(_BaseDataprocMetastoreRestTransport):
    """REST backend synchronous transport for DataprocMetastore.

    Configures and manages metastore services. Metastore services are
    fully managed, highly available, autoscaled, autohealing, OSS-native
    deployments of technical metadata management software. Each
    metastore service exposes a network endpoint through which metadata
    queries are served. Metadata queries can originate from a variety of
    sources, including Apache Hive, Apache Presto, and Apache Spark.

    The Dataproc Metastore API defines the following resource model:

    -  The service works with a collection of Google Cloud projects,
       named: ``/projects/*``

    -  Each project has a collection of available locations, named:
       ``/locations/*`` (a location must refer to a Google Cloud
       ``region``)

    -  Each location has a collection of services, named:
       ``/services/*``

    -  Dataproc Metastore services are resources with names of the form:

       ``/projects/{project_number}/locations/{location_id}/services/{service_id}``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "metastore.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataprocMetastoreRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'metastore.googleapis.com').
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
        self._interceptor = interceptor or DataprocMetastoreRestInterceptor()
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

    class _AlterMetadataResourceLocation(
        _BaseDataprocMetastoreRestTransport._BaseAlterMetadataResourceLocation,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.AlterMetadataResourceLocation")

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
            request: metastore.AlterMetadataResourceLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the alter metadata resource
            location method over HTTP.

                Args:
                    request (~.metastore.AlterMetadataResourceLocationRequest):
                        The request object. Request message for
                    [DataprocMetastore.AlterMetadataResourceLocation][google.cloud.metastore.v1.DataprocMetastore.AlterMetadataResourceLocation].
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
                _BaseDataprocMetastoreRestTransport._BaseAlterMetadataResourceLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_alter_metadata_resource_location(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseAlterMetadataResourceLocation._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseAlterMetadataResourceLocation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseAlterMetadataResourceLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._AlterMetadataResourceLocation._get_response(
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
            resp = self._interceptor.post_alter_metadata_resource_location(resp)
            return resp

    class _CreateBackup(
        _BaseDataprocMetastoreRestTransport._BaseCreateBackup, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.CreateBackup")

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
            request: metastore.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.metastore.CreateBackupRequest):
                    The request object. Request message for
                [DataprocMetastore.CreateBackup][google.cloud.metastore.v1.DataprocMetastore.CreateBackup].
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
                _BaseDataprocMetastoreRestTransport._BaseCreateBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseCreateBackup._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseCreateBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseCreateBackup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._CreateBackup._get_response(
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
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateMetadataImport(
        _BaseDataprocMetastoreRestTransport._BaseCreateMetadataImport,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.CreateMetadataImport")

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
            request: metastore.CreateMetadataImportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create metadata import method over HTTP.

            Args:
                request (~.metastore.CreateMetadataImportRequest):
                    The request object. Request message for
                [DataprocMetastore.CreateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.CreateMetadataImport].
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
                _BaseDataprocMetastoreRestTransport._BaseCreateMetadataImport._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_metadata_import(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseCreateMetadataImport._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseCreateMetadataImport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseCreateMetadataImport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DataprocMetastoreRestTransport._CreateMetadataImport._get_response(
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
            resp = self._interceptor.post_create_metadata_import(resp)
            return resp

    class _CreateService(
        _BaseDataprocMetastoreRestTransport._BaseCreateService,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.CreateService")

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
            request: metastore.CreateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create service method over HTTP.

            Args:
                request (~.metastore.CreateServiceRequest):
                    The request object. Request message for
                [DataprocMetastore.CreateService][google.cloud.metastore.v1.DataprocMetastore.CreateService].
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
                _BaseDataprocMetastoreRestTransport._BaseCreateService._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_service(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseCreateService._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseCreateService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseCreateService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._CreateService._get_response(
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
            resp = self._interceptor.post_create_service(resp)
            return resp

    class _DeleteBackup(
        _BaseDataprocMetastoreRestTransport._BaseDeleteBackup, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.DeleteBackup")

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
            request: metastore.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.metastore.DeleteBackupRequest):
                    The request object. Request message for
                [DataprocMetastore.DeleteBackup][google.cloud.metastore.v1.DataprocMetastore.DeleteBackup].
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
                _BaseDataprocMetastoreRestTransport._BaseDeleteBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseDeleteBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseDeleteBackup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._DeleteBackup._get_response(
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
            resp = self._interceptor.post_delete_backup(resp)
            return resp

    class _DeleteService(
        _BaseDataprocMetastoreRestTransport._BaseDeleteService,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.DeleteService")

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
            request: metastore.DeleteServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete service method over HTTP.

            Args:
                request (~.metastore.DeleteServiceRequest):
                    The request object. Request message for
                [DataprocMetastore.DeleteService][google.cloud.metastore.v1.DataprocMetastore.DeleteService].
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
                _BaseDataprocMetastoreRestTransport._BaseDeleteService._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_service(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseDeleteService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseDeleteService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._DeleteService._get_response(
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
            resp = self._interceptor.post_delete_service(resp)
            return resp

    class _ExportMetadata(
        _BaseDataprocMetastoreRestTransport._BaseExportMetadata,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ExportMetadata")

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
            request: metastore.ExportMetadataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export metadata method over HTTP.

            Args:
                request (~.metastore.ExportMetadataRequest):
                    The request object. Request message for
                [DataprocMetastore.ExportMetadata][google.cloud.metastore.v1.DataprocMetastore.ExportMetadata].
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
                _BaseDataprocMetastoreRestTransport._BaseExportMetadata._get_http_options()
            )
            request, metadata = self._interceptor.pre_export_metadata(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseExportMetadata._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseExportMetadata._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseExportMetadata._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._ExportMetadata._get_response(
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
            resp = self._interceptor.post_export_metadata(resp)
            return resp

    class _GetBackup(
        _BaseDataprocMetastoreRestTransport._BaseGetBackup, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetBackup")

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
            request: metastore.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.metastore.GetBackupRequest):
                    The request object. Request message for
                [DataprocMetastore.GetBackup][google.cloud.metastore.v1.DataprocMetastore.GetBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Backup:
                    The details of a backup resource.
            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseGetBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetBackup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetBackup._get_response(
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
            resp = metastore.Backup()
            pb_resp = metastore.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetMetadataImport(
        _BaseDataprocMetastoreRestTransport._BaseGetMetadataImport,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetMetadataImport")

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
            request: metastore.GetMetadataImportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.MetadataImport:
            r"""Call the get metadata import method over HTTP.

            Args:
                request (~.metastore.GetMetadataImportRequest):
                    The request object. Request message for
                [DataprocMetastore.GetMetadataImport][google.cloud.metastore.v1.DataprocMetastore.GetMetadataImport].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.MetadataImport:
                    A metastore resource that imports
                metadata.

            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseGetMetadataImport._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_metadata_import(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetMetadataImport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetMetadataImport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetMetadataImport._get_response(
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
            resp = metastore.MetadataImport()
            pb_resp = metastore.MetadataImport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_metadata_import(resp)
            return resp

    class _GetService(
        _BaseDataprocMetastoreRestTransport._BaseGetService, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetService")

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
            request: metastore.GetServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.Service:
            r"""Call the get service method over HTTP.

            Args:
                request (~.metastore.GetServiceRequest):
                    The request object. Request message for
                [DataprocMetastore.GetService][google.cloud.metastore.v1.DataprocMetastore.GetService].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.Service:
                    A managed metastore service that
                serves metadata queries.

            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseGetService._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_service(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetService._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetService._get_response(
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
            resp = metastore.Service()
            pb_resp = metastore.Service.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_service(resp)
            return resp

    class _ListBackups(
        _BaseDataprocMetastoreRestTransport._BaseListBackups, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ListBackups")

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
            request: metastore.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.metastore.ListBackupsRequest):
                    The request object. Request message for
                [DataprocMetastore.ListBackups][google.cloud.metastore.v1.DataprocMetastore.ListBackups].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListBackupsResponse:
                    Response message for
                [DataprocMetastore.ListBackups][google.cloud.metastore.v1.DataprocMetastore.ListBackups].

            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseListBackups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseListBackups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseListBackups._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._ListBackups._get_response(
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
            resp = metastore.ListBackupsResponse()
            pb_resp = metastore.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListMetadataImports(
        _BaseDataprocMetastoreRestTransport._BaseListMetadataImports,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ListMetadataImports")

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
            request: metastore.ListMetadataImportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListMetadataImportsResponse:
            r"""Call the list metadata imports method over HTTP.

            Args:
                request (~.metastore.ListMetadataImportsRequest):
                    The request object. Request message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListMetadataImportsResponse:
                    Response message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].

            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseListMetadataImports._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_metadata_imports(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseListMetadataImports._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseListMetadataImports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DataprocMetastoreRestTransport._ListMetadataImports._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = metastore.ListMetadataImportsResponse()
            pb_resp = metastore.ListMetadataImportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_metadata_imports(resp)
            return resp

    class _ListServices(
        _BaseDataprocMetastoreRestTransport._BaseListServices, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ListServices")

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
            request: metastore.ListServicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> metastore.ListServicesResponse:
            r"""Call the list services method over HTTP.

            Args:
                request (~.metastore.ListServicesRequest):
                    The request object. Request message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore.ListServicesResponse:
                    Response message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].

            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseListServices._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_services(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseListServices._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseListServices._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._ListServices._get_response(
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
            resp = metastore.ListServicesResponse()
            pb_resp = metastore.ListServicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_services(resp)
            return resp

    class _MoveTableToDatabase(
        _BaseDataprocMetastoreRestTransport._BaseMoveTableToDatabase,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.MoveTableToDatabase")

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
            request: metastore.MoveTableToDatabaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the move table to database method over HTTP.

            Args:
                request (~.metastore.MoveTableToDatabaseRequest):
                    The request object. Request message for
                [DataprocMetastore.MoveTableToDatabase][google.cloud.metastore.v1.DataprocMetastore.MoveTableToDatabase].
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
                _BaseDataprocMetastoreRestTransport._BaseMoveTableToDatabase._get_http_options()
            )
            request, metadata = self._interceptor.pre_move_table_to_database(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseMoveTableToDatabase._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseMoveTableToDatabase._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseMoveTableToDatabase._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DataprocMetastoreRestTransport._MoveTableToDatabase._get_response(
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
            resp = self._interceptor.post_move_table_to_database(resp)
            return resp

    class _QueryMetadata(
        _BaseDataprocMetastoreRestTransport._BaseQueryMetadata,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.QueryMetadata")

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
            request: metastore.QueryMetadataRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the query metadata method over HTTP.

            Args:
                request (~.metastore.QueryMetadataRequest):
                    The request object. Request message for
                [DataprocMetastore.QueryMetadata][google.cloud.metastore.v1.DataprocMetastore.QueryMetadata].
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
                _BaseDataprocMetastoreRestTransport._BaseQueryMetadata._get_http_options()
            )
            request, metadata = self._interceptor.pre_query_metadata(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseQueryMetadata._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseQueryMetadata._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseQueryMetadata._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._QueryMetadata._get_response(
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
            resp = self._interceptor.post_query_metadata(resp)
            return resp

    class _RestoreService(
        _BaseDataprocMetastoreRestTransport._BaseRestoreService,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.RestoreService")

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
            request: metastore.RestoreServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore service method over HTTP.

            Args:
                request (~.metastore.RestoreServiceRequest):
                    The request object. Request message for [DataprocMetastore.Restore][].
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
                _BaseDataprocMetastoreRestTransport._BaseRestoreService._get_http_options()
            )
            request, metadata = self._interceptor.pre_restore_service(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseRestoreService._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseRestoreService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseRestoreService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._RestoreService._get_response(
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
            resp = self._interceptor.post_restore_service(resp)
            return resp

    class _UpdateMetadataImport(
        _BaseDataprocMetastoreRestTransport._BaseUpdateMetadataImport,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.UpdateMetadataImport")

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
            request: metastore.UpdateMetadataImportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update metadata import method over HTTP.

            Args:
                request (~.metastore.UpdateMetadataImportRequest):
                    The request object. Request message for
                [DataprocMetastore.UpdateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.UpdateMetadataImport].
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
                _BaseDataprocMetastoreRestTransport._BaseUpdateMetadataImport._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_metadata_import(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseUpdateMetadataImport._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseUpdateMetadataImport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseUpdateMetadataImport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                DataprocMetastoreRestTransport._UpdateMetadataImport._get_response(
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
            resp = self._interceptor.post_update_metadata_import(resp)
            return resp

    class _UpdateService(
        _BaseDataprocMetastoreRestTransport._BaseUpdateService,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.UpdateService")

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
            request: metastore.UpdateServiceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update service method over HTTP.

            Args:
                request (~.metastore.UpdateServiceRequest):
                    The request object. Request message for
                [DataprocMetastore.UpdateService][google.cloud.metastore.v1.DataprocMetastore.UpdateService].
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
                _BaseDataprocMetastoreRestTransport._BaseUpdateService._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_service(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseUpdateService._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseUpdateService._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseUpdateService._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._UpdateService._get_response(
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
            resp = self._interceptor.post_update_service(resp)
            return resp

    @property
    def alter_metadata_resource_location(
        self,
    ) -> Callable[
        [metastore.AlterMetadataResourceLocationRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AlterMetadataResourceLocation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup(
        self,
    ) -> Callable[[metastore.CreateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_metadata_import(
        self,
    ) -> Callable[[metastore.CreateMetadataImportRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMetadataImport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_service(
        self,
    ) -> Callable[[metastore.CreateServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[metastore.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_service(
        self,
    ) -> Callable[[metastore.DeleteServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_metadata(
        self,
    ) -> Callable[[metastore.ExportMetadataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportMetadata(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(self) -> Callable[[metastore.GetBackupRequest], metastore.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_metadata_import(
        self,
    ) -> Callable[[metastore.GetMetadataImportRequest], metastore.MetadataImport]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMetadataImport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_service(self) -> Callable[[metastore.GetServiceRequest], metastore.Service]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[[metastore.ListBackupsRequest], metastore.ListBackupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_metadata_imports(
        self,
    ) -> Callable[
        [metastore.ListMetadataImportsRequest], metastore.ListMetadataImportsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMetadataImports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_services(
        self,
    ) -> Callable[[metastore.ListServicesRequest], metastore.ListServicesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListServices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def move_table_to_database(
        self,
    ) -> Callable[[metastore.MoveTableToDatabaseRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MoveTableToDatabase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def query_metadata(
        self,
    ) -> Callable[[metastore.QueryMetadataRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._QueryMetadata(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_service(
        self,
    ) -> Callable[[metastore.RestoreServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_metadata_import(
        self,
    ) -> Callable[[metastore.UpdateMetadataImportRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMetadataImport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_service(
        self,
    ) -> Callable[[metastore.UpdateServiceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateService(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseDataprocMetastoreRestTransport._BaseGetLocation, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetLocation")

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
                _BaseDataprocMetastoreRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetLocation._get_response(
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
        _BaseDataprocMetastoreRestTransport._BaseListLocations,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ListLocations")

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
                _BaseDataprocMetastoreRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._ListLocations._get_response(
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(
        _BaseDataprocMetastoreRestTransport._BaseGetIamPolicy, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(
        _BaseDataprocMetastoreRestTransport._BaseSetIamPolicy, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseDataprocMetastoreRestTransport._BaseTestIamPermissions,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseDataprocMetastoreRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseDataprocMetastoreRestTransport._BaseCancelOperation,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.CancelOperation")

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
                _BaseDataprocMetastoreRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataprocMetastoreRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._CancelOperation._get_response(
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
        _BaseDataprocMetastoreRestTransport._BaseDeleteOperation,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.DeleteOperation")

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
                _BaseDataprocMetastoreRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._DeleteOperation._get_response(
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
        _BaseDataprocMetastoreRestTransport._BaseGetOperation, DataprocMetastoreRestStub
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.GetOperation")

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
                _BaseDataprocMetastoreRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._GetOperation._get_response(
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
        _BaseDataprocMetastoreRestTransport._BaseListOperations,
        DataprocMetastoreRestStub,
    ):
        def __hash__(self):
            return hash("DataprocMetastoreRestTransport.ListOperations")

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
                _BaseDataprocMetastoreRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseDataprocMetastoreRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataprocMetastoreRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataprocMetastoreRestTransport._ListOperations._get_response(
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


__all__ = ("DataprocMetastoreRestTransport",)
