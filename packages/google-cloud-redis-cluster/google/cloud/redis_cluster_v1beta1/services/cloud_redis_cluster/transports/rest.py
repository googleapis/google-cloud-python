# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.redis_cluster_v1beta1.types import cloud_redis_cluster

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCloudRedisClusterRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CloudRedisClusterRestInterceptor:
    """Interceptor for CloudRedisCluster.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudRedisClusterRestTransport.

    .. code-block:: python
        class MyCustomCloudRedisClusterInterceptor(CloudRedisClusterRestInterceptor):
            def pre_backup_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_backup_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_collections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_collections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reschedule_cluster_maintenance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reschedule_cluster_maintenance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudRedisClusterRestTransport(interceptor=MyCustomCloudRedisClusterInterceptor())
        client = CloudRedisClusterClient(transport=transport)


    """

    def pre_backup_cluster(
        self,
        request: cloud_redis_cluster.BackupClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.BackupClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for backup_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_backup_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for backup_cluster

        DEPRECATED. Please use the `post_backup_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_backup_cluster` interceptor runs
        before the `post_backup_cluster_with_metadata` interceptor.
        """
        return response

    def post_backup_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for backup_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_backup_cluster_with_metadata`
        interceptor in new development instead of the `post_backup_cluster` interceptor.
        When both interceptors are used, this `post_backup_cluster_with_metadata` interceptor runs after the
        `post_backup_cluster` interceptor. The (possibly modified) response returned by
        `post_backup_cluster` will be passed to
        `post_backup_cluster_with_metadata`.
        """
        return response, metadata

    def pre_create_cluster(
        self,
        request: cloud_redis_cluster.CreateClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.CreateClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cluster

        DEPRECATED. Please use the `post_create_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_create_cluster` interceptor runs
        before the `post_create_cluster_with_metadata` interceptor.
        """
        return response

    def post_create_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_create_cluster_with_metadata`
        interceptor in new development instead of the `post_create_cluster` interceptor.
        When both interceptors are used, this `post_create_cluster_with_metadata` interceptor runs after the
        `post_create_cluster` interceptor. The (possibly modified) response returned by
        `post_create_cluster` will be passed to
        `post_create_cluster_with_metadata`.
        """
        return response, metadata

    def pre_delete_backup(
        self,
        request: cloud_redis_cluster.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.DeleteBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        DEPRECATED. Please use the `post_delete_backup_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_delete_backup` interceptor runs
        before the `post_delete_backup_with_metadata` interceptor.
        """
        return response

    def post_delete_backup_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_delete_backup_with_metadata`
        interceptor in new development instead of the `post_delete_backup` interceptor.
        When both interceptors are used, this `post_delete_backup_with_metadata` interceptor runs after the
        `post_delete_backup` interceptor. The (possibly modified) response returned by
        `post_delete_backup` will be passed to
        `post_delete_backup_with_metadata`.
        """
        return response, metadata

    def pre_delete_cluster(
        self,
        request: cloud_redis_cluster.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.DeleteClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_delete_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cluster

        DEPRECATED. Please use the `post_delete_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_delete_cluster` interceptor runs
        before the `post_delete_cluster_with_metadata` interceptor.
        """
        return response

    def post_delete_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_delete_cluster_with_metadata`
        interceptor in new development instead of the `post_delete_cluster` interceptor.
        When both interceptors are used, this `post_delete_cluster_with_metadata` interceptor runs after the
        `post_delete_cluster` interceptor. The (possibly modified) response returned by
        `post_delete_cluster` will be passed to
        `post_delete_cluster_with_metadata`.
        """
        return response, metadata

    def pre_export_backup(
        self,
        request: cloud_redis_cluster.ExportBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ExportBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for export_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_export_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_backup

        DEPRECATED. Please use the `post_export_backup_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_export_backup` interceptor runs
        before the `post_export_backup_with_metadata` interceptor.
        """
        return response

    def post_export_backup_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for export_backup

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_export_backup_with_metadata`
        interceptor in new development instead of the `post_export_backup` interceptor.
        When both interceptors are used, this `post_export_backup_with_metadata` interceptor runs after the
        `post_export_backup` interceptor. The (possibly modified) response returned by
        `post_export_backup` will be passed to
        `post_export_backup_with_metadata`.
        """
        return response, metadata

    def pre_get_backup(
        self,
        request: cloud_redis_cluster.GetBackupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.GetBackupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_backup(
        self, response: cloud_redis_cluster.Backup
    ) -> cloud_redis_cluster.Backup:
        """Post-rpc interceptor for get_backup

        DEPRECATED. Please use the `post_get_backup_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_get_backup` interceptor runs
        before the `post_get_backup_with_metadata` interceptor.
        """
        return response

    def post_get_backup_with_metadata(
        self,
        response: cloud_redis_cluster.Backup,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[cloud_redis_cluster.Backup, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_backup

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_get_backup_with_metadata`
        interceptor in new development instead of the `post_get_backup` interceptor.
        When both interceptors are used, this `post_get_backup_with_metadata` interceptor runs after the
        `post_get_backup` interceptor. The (possibly modified) response returned by
        `post_get_backup` will be passed to
        `post_get_backup_with_metadata`.
        """
        return response, metadata

    def pre_get_backup_collection(
        self,
        request: cloud_redis_cluster.GetBackupCollectionRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.GetBackupCollectionRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_backup_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_backup_collection(
        self, response: cloud_redis_cluster.BackupCollection
    ) -> cloud_redis_cluster.BackupCollection:
        """Post-rpc interceptor for get_backup_collection

        DEPRECATED. Please use the `post_get_backup_collection_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_get_backup_collection` interceptor runs
        before the `post_get_backup_collection_with_metadata` interceptor.
        """
        return response

    def post_get_backup_collection_with_metadata(
        self,
        response: cloud_redis_cluster.BackupCollection,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.BackupCollection, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get_backup_collection

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_get_backup_collection_with_metadata`
        interceptor in new development instead of the `post_get_backup_collection` interceptor.
        When both interceptors are used, this `post_get_backup_collection_with_metadata` interceptor runs after the
        `post_get_backup_collection` interceptor. The (possibly modified) response returned by
        `post_get_backup_collection` will be passed to
        `post_get_backup_collection_with_metadata`.
        """
        return response, metadata

    def pre_get_cluster(
        self,
        request: cloud_redis_cluster.GetClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.GetClusterRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_cluster(
        self, response: cloud_redis_cluster.Cluster
    ) -> cloud_redis_cluster.Cluster:
        """Post-rpc interceptor for get_cluster

        DEPRECATED. Please use the `post_get_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_get_cluster` interceptor runs
        before the `post_get_cluster_with_metadata` interceptor.
        """
        return response

    def post_get_cluster_with_metadata(
        self,
        response: cloud_redis_cluster.Cluster,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[cloud_redis_cluster.Cluster, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_get_cluster_with_metadata`
        interceptor in new development instead of the `post_get_cluster` interceptor.
        When both interceptors are used, this `post_get_cluster_with_metadata` interceptor runs after the
        `post_get_cluster` interceptor. The (possibly modified) response returned by
        `post_get_cluster` will be passed to
        `post_get_cluster_with_metadata`.
        """
        return response, metadata

    def pre_get_cluster_certificate_authority(
        self,
        request: cloud_redis_cluster.GetClusterCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.GetClusterCertificateAuthorityRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_cluster_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_cluster_certificate_authority(
        self, response: cloud_redis_cluster.CertificateAuthority
    ) -> cloud_redis_cluster.CertificateAuthority:
        """Post-rpc interceptor for get_cluster_certificate_authority

        DEPRECATED. Please use the `post_get_cluster_certificate_authority_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_get_cluster_certificate_authority` interceptor runs
        before the `post_get_cluster_certificate_authority_with_metadata` interceptor.
        """
        return response

    def post_get_cluster_certificate_authority_with_metadata(
        self,
        response: cloud_redis_cluster.CertificateAuthority,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.CertificateAuthority,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for get_cluster_certificate_authority

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_get_cluster_certificate_authority_with_metadata`
        interceptor in new development instead of the `post_get_cluster_certificate_authority` interceptor.
        When both interceptors are used, this `post_get_cluster_certificate_authority_with_metadata` interceptor runs after the
        `post_get_cluster_certificate_authority` interceptor. The (possibly modified) response returned by
        `post_get_cluster_certificate_authority` will be passed to
        `post_get_cluster_certificate_authority_with_metadata`.
        """
        return response, metadata

    def pre_list_backup_collections(
        self,
        request: cloud_redis_cluster.ListBackupCollectionsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListBackupCollectionsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_backup_collections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_list_backup_collections(
        self, response: cloud_redis_cluster.ListBackupCollectionsResponse
    ) -> cloud_redis_cluster.ListBackupCollectionsResponse:
        """Post-rpc interceptor for list_backup_collections

        DEPRECATED. Please use the `post_list_backup_collections_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_list_backup_collections` interceptor runs
        before the `post_list_backup_collections_with_metadata` interceptor.
        """
        return response

    def post_list_backup_collections_with_metadata(
        self,
        response: cloud_redis_cluster.ListBackupCollectionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListBackupCollectionsResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_backup_collections

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_list_backup_collections_with_metadata`
        interceptor in new development instead of the `post_list_backup_collections` interceptor.
        When both interceptors are used, this `post_list_backup_collections_with_metadata` interceptor runs after the
        `post_list_backup_collections` interceptor. The (possibly modified) response returned by
        `post_list_backup_collections` will be passed to
        `post_list_backup_collections_with_metadata`.
        """
        return response, metadata

    def pre_list_backups(
        self,
        request: cloud_redis_cluster.ListBackupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListBackupsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_list_backups(
        self, response: cloud_redis_cluster.ListBackupsResponse
    ) -> cloud_redis_cluster.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        DEPRECATED. Please use the `post_list_backups_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_list_backups` interceptor runs
        before the `post_list_backups_with_metadata` interceptor.
        """
        return response

    def post_list_backups_with_metadata(
        self,
        response: cloud_redis_cluster.ListBackupsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListBackupsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list_backups

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_list_backups_with_metadata`
        interceptor in new development instead of the `post_list_backups` interceptor.
        When both interceptors are used, this `post_list_backups_with_metadata` interceptor runs after the
        `post_list_backups` interceptor. The (possibly modified) response returned by
        `post_list_backups` will be passed to
        `post_list_backups_with_metadata`.
        """
        return response, metadata

    def pre_list_clusters(
        self,
        request: cloud_redis_cluster.ListClustersRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListClustersRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: cloud_redis_cluster.ListClustersResponse
    ) -> cloud_redis_cluster.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        DEPRECATED. Please use the `post_list_clusters_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_list_clusters` interceptor runs
        before the `post_list_clusters_with_metadata` interceptor.
        """
        return response

    def post_list_clusters_with_metadata(
        self,
        response: cloud_redis_cluster.ListClustersResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.ListClustersResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_list_clusters_with_metadata`
        interceptor in new development instead of the `post_list_clusters` interceptor.
        When both interceptors are used, this `post_list_clusters_with_metadata` interceptor runs after the
        `post_list_clusters` interceptor. The (possibly modified) response returned by
        `post_list_clusters` will be passed to
        `post_list_clusters_with_metadata`.
        """
        return response, metadata

    def pre_reschedule_cluster_maintenance(
        self,
        request: cloud_redis_cluster.RescheduleClusterMaintenanceRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.RescheduleClusterMaintenanceRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for reschedule_cluster_maintenance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_reschedule_cluster_maintenance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reschedule_cluster_maintenance

        DEPRECATED. Please use the `post_reschedule_cluster_maintenance_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_reschedule_cluster_maintenance` interceptor runs
        before the `post_reschedule_cluster_maintenance_with_metadata` interceptor.
        """
        return response

    def post_reschedule_cluster_maintenance_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for reschedule_cluster_maintenance

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_reschedule_cluster_maintenance_with_metadata`
        interceptor in new development instead of the `post_reschedule_cluster_maintenance` interceptor.
        When both interceptors are used, this `post_reschedule_cluster_maintenance_with_metadata` interceptor runs after the
        `post_reschedule_cluster_maintenance` interceptor. The (possibly modified) response returned by
        `post_reschedule_cluster_maintenance` will be passed to
        `post_reschedule_cluster_maintenance_with_metadata`.
        """
        return response, metadata

    def pre_update_cluster(
        self,
        request: cloud_redis_cluster.UpdateClusterRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        cloud_redis_cluster.UpdateClusterRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_cluster

        DEPRECATED. Please use the `post_update_cluster_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code. This `post_update_cluster` interceptor runs
        before the `post_update_cluster_with_metadata` interceptor.
        """
        return response

    def post_update_cluster_with_metadata(
        self,
        response: operations_pb2.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[operations_pb2.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the CloudRedisCluster server but before it is returned to user code.

        We recommend only using this `post_update_cluster_with_metadata`
        interceptor in new development instead of the `post_update_cluster` interceptor.
        When both interceptors are used, this `post_update_cluster_with_metadata` interceptor runs after the
        `post_update_cluster` interceptor. The (possibly modified) response returned by
        `post_update_cluster` will be passed to
        `post_update_cluster_with_metadata`.
        """
        return response, metadata

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.GetLocationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        locations_pb2.ListLocationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.CancelOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.ListOperationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudRedisCluster server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CloudRedisCluster server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudRedisClusterRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudRedisClusterRestInterceptor


class CloudRedisClusterRestTransport(_BaseCloudRedisClusterRestTransport):
    """REST backend synchronous transport for CloudRedisCluster.

    Configures and manages Cloud Memorystore for Redis clusters

    Google Cloud Memorystore for Redis Cluster

    The ``redis.googleapis.com`` service implements the Google Cloud
    Memorystore for Redis API and defines the following resource model
    for managing Redis clusters:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of Redis clusters, named:
       ``/clusters/*``
    -  As such, Redis clusters are resources of the form:
       ``/projects/{project_id}/locations/{location_id}/clusters/{instance_id}``

    Note that location_id must be a GCP ``region``; for example:

    -  ``projects/redpepper-1290/locations/us-central1/clusters/my-redis``

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "redis.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudRedisClusterRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'redis.googleapis.com').
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
        self._interceptor = interceptor or CloudRedisClusterRestInterceptor()
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
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BackupCluster(
        _BaseCloudRedisClusterRestTransport._BaseBackupCluster,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.BackupCluster")

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
            request: cloud_redis_cluster.BackupClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the backup cluster method over HTTP.

            Args:
                request (~.cloud_redis_cluster.BackupClusterRequest):
                    The request object. Request for [BackupCluster].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseBackupCluster._get_http_options()
            )

            request, metadata = self._interceptor.pre_backup_cluster(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseBackupCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudRedisClusterRestTransport._BaseBackupCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseBackupCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.BackupCluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "BackupCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._BackupCluster._get_response(
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

            resp = self._interceptor.post_backup_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_backup_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.backup_cluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "BackupCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateCluster(
        _BaseCloudRedisClusterRestTransport._BaseCreateCluster,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.CreateCluster")

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
            request: cloud_redis_cluster.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.cloud_redis_cluster.CreateClusterRequest):
                    The request object. Request for [CreateCluster][CloudRedis.CreateCluster].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseCreateCluster._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseCreateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudRedisClusterRestTransport._BaseCreateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseCreateCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.CreateCluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "CreateCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._CreateCluster._get_response(
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

            resp = self._interceptor.post_create_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_create_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.create_cluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "CreateCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteBackup(
        _BaseCloudRedisClusterRestTransport._BaseDeleteBackup, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.DeleteBackup")

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
            request: cloud_redis_cluster.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.cloud_redis_cluster.DeleteBackupRequest):
                    The request object. Request for [DeleteBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseDeleteBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseDeleteBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseDeleteBackup._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.DeleteBackup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "DeleteBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._DeleteBackup._get_response(
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
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_backup_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.delete_backup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "DeleteBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteCluster(
        _BaseCloudRedisClusterRestTransport._BaseDeleteCluster,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.DeleteCluster")

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
            request: cloud_redis_cluster.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.cloud_redis_cluster.DeleteClusterRequest):
                    The request object. Request for [DeleteCluster][CloudRedis.DeleteCluster].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseDeleteCluster._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseDeleteCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseDeleteCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.DeleteCluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "DeleteCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._DeleteCluster._get_response(
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

            resp = self._interceptor.post_delete_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.delete_cluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "DeleteCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ExportBackup(
        _BaseCloudRedisClusterRestTransport._BaseExportBackup, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ExportBackup")

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
            request: cloud_redis_cluster.ExportBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export backup method over HTTP.

            Args:
                request (~.cloud_redis_cluster.ExportBackupRequest):
                    The request object. Request for [ExportBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseExportBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_export_backup(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseExportBackup._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudRedisClusterRestTransport._BaseExportBackup._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseExportBackup._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ExportBackup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ExportBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._ExportBackup._get_response(
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

            resp = self._interceptor.post_export_backup(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_export_backup_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.export_backup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ExportBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackup(
        _BaseCloudRedisClusterRestTransport._BaseGetBackup, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetBackup")

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
            request: cloud_redis_cluster.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.cloud_redis_cluster.GetBackupRequest):
                    The request object. Request for [GetBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.Backup:
                    Backup of a cluster.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetBackup._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetBackup._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetBackup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetBackup",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._GetBackup._get_response(
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
            resp = cloud_redis_cluster.Backup()
            pb_resp = cloud_redis_cluster.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_backup_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.Backup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.get_backup",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetBackup",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetBackupCollection(
        _BaseCloudRedisClusterRestTransport._BaseGetBackupCollection,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetBackupCollection")

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
            request: cloud_redis_cluster.GetBackupCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.BackupCollection:
            r"""Call the get backup collection method over HTTP.

            Args:
                request (~.cloud_redis_cluster.GetBackupCollectionRequest):
                    The request object. Request for [GetBackupCollection].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.BackupCollection:
                    BackupCollection of a cluster.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetBackupCollection._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_backup_collection(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetBackupCollection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetBackupCollection._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetBackupCollection",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetBackupCollection",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                CloudRedisClusterRestTransport._GetBackupCollection._get_response(
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
            resp = cloud_redis_cluster.BackupCollection()
            pb_resp = cloud_redis_cluster.BackupCollection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_backup_collection(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_backup_collection_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.BackupCollection.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.get_backup_collection",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetBackupCollection",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetCluster(
        _BaseCloudRedisClusterRestTransport._BaseGetCluster, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetCluster")

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
            request: cloud_redis_cluster.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.cloud_redis_cluster.GetClusterRequest):
                    The request object. Request for [GetCluster][CloudRedis.GetCluster].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.Cluster:
                    A cluster instance.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetCluster._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetCluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._GetCluster._get_response(
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
            resp = cloud_redis_cluster.Cluster()
            pb_resp = cloud_redis_cluster.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.Cluster.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.get_cluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetClusterCertificateAuthority(
        _BaseCloudRedisClusterRestTransport._BaseGetClusterCertificateAuthority,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetClusterCertificateAuthority")

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
            request: cloud_redis_cluster.GetClusterCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.CertificateAuthority:
            r"""Call the get cluster certificate
            authority method over HTTP.

                Args:
                    request (~.cloud_redis_cluster.GetClusterCertificateAuthorityRequest):
                        The request object. Request for
                    [GetClusterCertificateAuthorityRequest][CloudRedis.GetClusterCertificateAuthorityRequest].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.cloud_redis_cluster.CertificateAuthority:
                        Redis cluster certificate authority
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetClusterCertificateAuthority._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_cluster_certificate_authority(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetClusterCertificateAuthority._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetClusterCertificateAuthority._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetClusterCertificateAuthority",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetClusterCertificateAuthority",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._GetClusterCertificateAuthority._get_response(
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
            resp = cloud_redis_cluster.CertificateAuthority()
            pb_resp = cloud_redis_cluster.CertificateAuthority.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_cluster_certificate_authority(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_get_cluster_certificate_authority_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.CertificateAuthority.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.get_cluster_certificate_authority",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetClusterCertificateAuthority",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackupCollections(
        _BaseCloudRedisClusterRestTransport._BaseListBackupCollections,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ListBackupCollections")

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
            request: cloud_redis_cluster.ListBackupCollectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.ListBackupCollectionsResponse:
            r"""Call the list backup collections method over HTTP.

            Args:
                request (~.cloud_redis_cluster.ListBackupCollectionsRequest):
                    The request object. Request for [ListBackupCollections]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.ListBackupCollectionsResponse:
                    Response for [ListBackupCollections].
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseListBackupCollections._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backup_collections(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseListBackupCollections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseListBackupCollections._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ListBackupCollections",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListBackupCollections",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                CloudRedisClusterRestTransport._ListBackupCollections._get_response(
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
            resp = cloud_redis_cluster.ListBackupCollectionsResponse()
            pb_resp = cloud_redis_cluster.ListBackupCollectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backup_collections(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_backup_collections_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        cloud_redis_cluster.ListBackupCollectionsResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.list_backup_collections",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListBackupCollections",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListBackups(
        _BaseCloudRedisClusterRestTransport._BaseListBackups, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ListBackups")

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
            request: cloud_redis_cluster.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.cloud_redis_cluster.ListBackupsRequest):
                    The request object. Request for [ListBackups].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.ListBackupsResponse:
                    Response for [ListBackups].
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseListBackups._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseListBackups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseListBackups._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ListBackups",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListBackups",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._ListBackups._get_response(
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
            resp = cloud_redis_cluster.ListBackupsResponse()
            pb_resp = cloud_redis_cluster.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_backups(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_backups_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.ListBackupsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.list_backups",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListBackups",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListClusters(
        _BaseCloudRedisClusterRestTransport._BaseListClusters, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ListClusters")

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
            request: cloud_redis_cluster.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> cloud_redis_cluster.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.cloud_redis_cluster.ListClustersRequest):
                    The request object. Request for [ListClusters][CloudRedis.ListClusters].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.cloud_redis_cluster.ListClustersResponse:
                    Response for [ListClusters][CloudRedis.ListClusters].
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseListClusters._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseListClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseListClusters._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ListClusters",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListClusters",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._ListClusters._get_response(
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
            resp = cloud_redis_cluster.ListClustersResponse()
            pb_resp = cloud_redis_cluster.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_clusters(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_clusters_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = cloud_redis_cluster.ListClustersResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.list_clusters",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListClusters",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _RescheduleClusterMaintenance(
        _BaseCloudRedisClusterRestTransport._BaseRescheduleClusterMaintenance,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.RescheduleClusterMaintenance")

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
            request: cloud_redis_cluster.RescheduleClusterMaintenanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reschedule cluster
            maintenance method over HTTP.

                Args:
                    request (~.cloud_redis_cluster.RescheduleClusterMaintenanceRequest):
                        The request object. Request for rescheduling a cluster
                    maintenance.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseRescheduleClusterMaintenance._get_http_options()
            )

            request, metadata = self._interceptor.pre_reschedule_cluster_maintenance(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseRescheduleClusterMaintenance._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudRedisClusterRestTransport._BaseRescheduleClusterMaintenance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseRescheduleClusterMaintenance._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.RescheduleClusterMaintenance",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "RescheduleClusterMaintenance",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._RescheduleClusterMaintenance._get_response(
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

            resp = self._interceptor.post_reschedule_cluster_maintenance(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_reschedule_cluster_maintenance_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.reschedule_cluster_maintenance",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "RescheduleClusterMaintenance",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateCluster(
        _BaseCloudRedisClusterRestTransport._BaseUpdateCluster,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.UpdateCluster")

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
            request: cloud_redis_cluster.UpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.cloud_redis_cluster.UpdateClusterRequest):
                    The request object. Request for [UpdateCluster][CloudRedis.UpdateCluster].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseUpdateCluster._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseUpdateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseCloudRedisClusterRestTransport._BaseUpdateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseUpdateCluster._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.UpdateCluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "UpdateCluster",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._UpdateCluster._get_response(
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

            resp = self._interceptor.post_update_cluster(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_update_cluster_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.update_cluster",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "UpdateCluster",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def backup_cluster(
        self,
    ) -> Callable[[cloud_redis_cluster.BackupClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BackupCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_cluster(
        self,
    ) -> Callable[[cloud_redis_cluster.CreateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[cloud_redis_cluster.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[cloud_redis_cluster.DeleteClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_backup(
        self,
    ) -> Callable[[cloud_redis_cluster.ExportBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(
        self,
    ) -> Callable[[cloud_redis_cluster.GetBackupRequest], cloud_redis_cluster.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_collection(
        self,
    ) -> Callable[
        [cloud_redis_cluster.GetBackupCollectionRequest],
        cloud_redis_cluster.BackupCollection,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[cloud_redis_cluster.GetClusterRequest], cloud_redis_cluster.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster_certificate_authority(
        self,
    ) -> Callable[
        [cloud_redis_cluster.GetClusterCertificateAuthorityRequest],
        cloud_redis_cluster.CertificateAuthority,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetClusterCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_collections(
        self,
    ) -> Callable[
        [cloud_redis_cluster.ListBackupCollectionsRequest],
        cloud_redis_cluster.ListBackupCollectionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupCollections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[
        [cloud_redis_cluster.ListBackupsRequest],
        cloud_redis_cluster.ListBackupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [cloud_redis_cluster.ListClustersRequest],
        cloud_redis_cluster.ListClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reschedule_cluster_maintenance(
        self,
    ) -> Callable[
        [cloud_redis_cluster.RescheduleClusterMaintenanceRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RescheduleClusterMaintenance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(
        self,
    ) -> Callable[[cloud_redis_cluster.UpdateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseCloudRedisClusterRestTransport._BaseGetLocation, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetLocation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetLocation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetLocation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._GetLocation._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterAsyncClient.GetLocation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetLocation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseCloudRedisClusterRestTransport._BaseListLocations,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ListLocations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseListLocations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListLocations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._ListLocations._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterAsyncClient.ListLocations",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListLocations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseCloudRedisClusterRestTransport._BaseCancelOperation,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseCancelOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.CancelOperation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "CancelOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseCloudRedisClusterRestTransport._BaseDeleteOperation,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.DeleteOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseDeleteOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.DeleteOperation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "DeleteOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._DeleteOperation._get_response(
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
        _BaseCloudRedisClusterRestTransport._BaseGetOperation, CloudRedisClusterRestStub
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._GetOperation._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseCloudRedisClusterRestTransport._BaseListOperations,
        CloudRedisClusterRestStub,
    ):
        def __hash__(self):
            return hash("CloudRedisClusterRestTransport.ListOperations")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseCloudRedisClusterRestTransport._BaseListOperations._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseCloudRedisClusterRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudRedisClusterRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.redis.cluster_v1beta1.CloudRedisClusterClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListOperations",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = CloudRedisClusterRestTransport._ListOperations._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.redis.cluster_v1beta1.CloudRedisClusterAsyncClient.ListOperations",
                    extra={
                        "serviceName": "google.cloud.redis.cluster.v1beta1.CloudRedisCluster",
                        "rpcName": "ListOperations",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudRedisClusterRestTransport",)
