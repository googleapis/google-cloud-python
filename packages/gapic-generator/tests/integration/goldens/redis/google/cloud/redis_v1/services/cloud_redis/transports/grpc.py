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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.redis_v1.types import cloud_redis
from google.longrunning import operations_pb2  # type: ignore
from .base import CloudRedisTransport, DEFAULT_CLIENT_INFO


class CloudRedisGrpcTransport(CloudRedisTransport):
    """gRPC backend transport for CloudRedis.

    Configures and manages Cloud Memorystore for Redis instances

    Google Cloud Memorystore for Redis v1

    The ``redis.googleapis.com`` service implements the Google Cloud
    Memorystore for Redis API and defines the following resource model
    for managing Redis instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of Redis instances, named:
       ``/instances/*``
    -  As such, Redis instances are resources of the form:
       ``/projects/{project_id}/locations/{location_id}/instances/{instance_id}``

    Note that location_id must be referring to a GCP ``region``; for
    example:

    -  ``projects/redpepper-1290/locations/us-central1/instances/my-redis``

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'redis.googleapis.com',
            credentials: ga_credentials.Credentials = None,
            credentials_file: str = None,
            scopes: Sequence[str] = None,
            channel: grpc.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
            ssl_channel_credentials: grpc.ChannelCredentials = None,
            client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(cls,
                       host: str = 'redis.googleapis.com',
                       credentials: ga_credentials.Credentials = None,
                       credentials_file: str = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_instances(self) -> Callable[
            [cloud_redis.ListInstancesRequest],
            cloud_redis.ListInstancesResponse]:
        r"""Return a callable for the list instances method over gRPC.

        Lists all Redis instances owned by a project in either the
        specified location (region) or all locations.

        The location should have the following format:

        -  ``projects/{project_id}/locations/{location_id}``

        If ``location_id`` is specified as ``-`` (wildcard), then all
        regions available to the project are queried, and the results
        are aggregated.

        Returns:
            Callable[[~.ListInstancesRequest],
                    ~.ListInstancesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_instances' not in self._stubs:
            self._stubs['list_instances'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/ListInstances',
                request_serializer=cloud_redis.ListInstancesRequest.serialize,
                response_deserializer=cloud_redis.ListInstancesResponse.deserialize,
            )
        return self._stubs['list_instances']

    @property
    def get_instance(self) -> Callable[
            [cloud_redis.GetInstanceRequest],
            cloud_redis.Instance]:
        r"""Return a callable for the get instance method over gRPC.

        Gets the details of a specific Redis instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    ~.Instance]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_instance' not in self._stubs:
            self._stubs['get_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/GetInstance',
                request_serializer=cloud_redis.GetInstanceRequest.serialize,
                response_deserializer=cloud_redis.Instance.deserialize,
            )
        return self._stubs['get_instance']

    @property
    def create_instance(self) -> Callable[
            [cloud_redis.CreateInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create instance method over gRPC.

        Creates a Redis instance based on the specified tier and memory
        size.

        By default, the instance is accessible from the project's
        `default network <https://cloud.google.com/vpc/docs/vpc>`__.

        The creation is executed asynchronously and callers may check
        the returned operation to track its progress. Once the operation
        is completed the Redis instance will be fully functional.
        Completed longrunning.Operation will contain the new instance
        object in the response field.

        The returned operation is automatically deleted after a few
        hours, so there is no need to call DeleteOperation.

        Returns:
            Callable[[~.CreateInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_instance' not in self._stubs:
            self._stubs['create_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/CreateInstance',
                request_serializer=cloud_redis.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_instance']

    @property
    def update_instance(self) -> Callable[
            [cloud_redis.UpdateInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update instance method over gRPC.

        Updates the metadata and configuration of a specific
        Redis instance.
        Completed longrunning.Operation will contain the new
        instance object in the response field. The returned
        operation is automatically deleted after a few hours, so
        there is no need to call DeleteOperation.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_instance' not in self._stubs:
            self._stubs['update_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/UpdateInstance',
                request_serializer=cloud_redis.UpdateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_instance']

    @property
    def upgrade_instance(self) -> Callable[
            [cloud_redis.UpgradeInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the upgrade instance method over gRPC.

        Upgrades Redis instance to the newer Redis version
        specified in the request.

        Returns:
            Callable[[~.UpgradeInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'upgrade_instance' not in self._stubs:
            self._stubs['upgrade_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/UpgradeInstance',
                request_serializer=cloud_redis.UpgradeInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['upgrade_instance']

    @property
    def import_instance(self) -> Callable[
            [cloud_redis.ImportInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the import instance method over gRPC.

        Import a Redis RDB snapshot file from Cloud Storage
        into a Redis instance.
        Redis may stop serving during this operation. Instance
        state will be IMPORTING for entire operation. When
        complete, the instance will contain only data from the
        imported file.

        The returned operation is automatically deleted after a
        few hours, so there is no need to call DeleteOperation.

        Returns:
            Callable[[~.ImportInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'import_instance' not in self._stubs:
            self._stubs['import_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/ImportInstance',
                request_serializer=cloud_redis.ImportInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['import_instance']

    @property
    def export_instance(self) -> Callable[
            [cloud_redis.ExportInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the export instance method over gRPC.

        Export Redis instance data into a Redis RDB format
        file in Cloud Storage.
        Redis will continue serving during this operation.
        The returned operation is automatically deleted after a
        few hours, so there is no need to call DeleteOperation.

        Returns:
            Callable[[~.ExportInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'export_instance' not in self._stubs:
            self._stubs['export_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/ExportInstance',
                request_serializer=cloud_redis.ExportInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['export_instance']

    @property
    def failover_instance(self) -> Callable[
            [cloud_redis.FailoverInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the failover instance method over gRPC.

        Initiates a failover of the master node to current
        replica node for a specific STANDARD tier Cloud
        Memorystore for Redis instance.

        Returns:
            Callable[[~.FailoverInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'failover_instance' not in self._stubs:
            self._stubs['failover_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/FailoverInstance',
                request_serializer=cloud_redis.FailoverInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['failover_instance']

    @property
    def delete_instance(self) -> Callable[
            [cloud_redis.DeleteInstanceRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes a specific Redis instance.  Instance stops
        serving and data is deleted.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_instance' not in self._stubs:
            self._stubs['delete_instance'] = self.grpc_channel.unary_unary(
                '/google.cloud.redis.v1.CloudRedis/DeleteInstance',
                request_serializer=cloud_redis.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_instance']

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = (
    'CloudRedisGrpcTransport',
)
