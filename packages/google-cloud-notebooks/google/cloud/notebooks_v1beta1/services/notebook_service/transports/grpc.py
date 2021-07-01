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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.notebooks_v1beta1.types import environment
from google.cloud.notebooks_v1beta1.types import instance
from google.cloud.notebooks_v1beta1.types import service
from google.longrunning import operations_pb2  # type: ignore
from .base import NotebookServiceTransport, DEFAULT_CLIENT_INFO


class NotebookServiceGrpcTransport(NotebookServiceTransport):
    """gRPC backend transport for NotebookService.

    API v1beta1 service for Cloud AI Platform Notebooks.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "notebooks.googleapis.com",
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
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
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
        self._operations_client = None

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
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
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
    def create_channel(
        cls,
        host: str = "notebooks.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
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
            **kwargs,
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
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def list_instances(
        self,
    ) -> Callable[[service.ListInstancesRequest], service.ListInstancesResponse]:
        r"""Return a callable for the list instances method over gRPC.

        Lists instances in a given project and location.

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
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/ListInstances",
                request_serializer=service.ListInstancesRequest.serialize,
                response_deserializer=service.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(self) -> Callable[[service.GetInstanceRequest], instance.Instance]:
        r"""Return a callable for the get instance method over gRPC.

        Gets details of a single Instance.

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
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/GetInstance",
                request_serializer=service.GetInstanceRequest.serialize,
                response_deserializer=instance.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self,
    ) -> Callable[[service.CreateInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the create instance method over gRPC.

        Creates a new Instance in a given project and
        location.

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
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/CreateInstance",
                request_serializer=service.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def register_instance(
        self,
    ) -> Callable[[service.RegisterInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the register instance method over gRPC.

        Registers an existing legacy notebook instance to the
        Notebooks API server. Legacy instances are instances
        created with the legacy Compute Engine calls. They are
        not manageable by the Notebooks API out of the box. This
        call makes these instances manageable by the Notebooks
        API.

        Returns:
            Callable[[~.RegisterInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "register_instance" not in self._stubs:
            self._stubs["register_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/RegisterInstance",
                request_serializer=service.RegisterInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["register_instance"]

    @property
    def set_instance_accelerator(
        self,
    ) -> Callable[[service.SetInstanceAcceleratorRequest], operations_pb2.Operation]:
        r"""Return a callable for the set instance accelerator method over gRPC.

        Updates the guest accelerators of a single Instance.

        Returns:
            Callable[[~.SetInstanceAcceleratorRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_instance_accelerator" not in self._stubs:
            self._stubs["set_instance_accelerator"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/SetInstanceAccelerator",
                request_serializer=service.SetInstanceAcceleratorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_instance_accelerator"]

    @property
    def set_instance_machine_type(
        self,
    ) -> Callable[[service.SetInstanceMachineTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the set instance machine type method over gRPC.

        Updates the machine type of a single Instance.

        Returns:
            Callable[[~.SetInstanceMachineTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_instance_machine_type" not in self._stubs:
            self._stubs["set_instance_machine_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/SetInstanceMachineType",
                request_serializer=service.SetInstanceMachineTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_instance_machine_type"]

    @property
    def set_instance_labels(
        self,
    ) -> Callable[[service.SetInstanceLabelsRequest], operations_pb2.Operation]:
        r"""Return a callable for the set instance labels method over gRPC.

        Updates the labels of an Instance.

        Returns:
            Callable[[~.SetInstanceLabelsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_instance_labels" not in self._stubs:
            self._stubs["set_instance_labels"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/SetInstanceLabels",
                request_serializer=service.SetInstanceLabelsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_instance_labels"]

    @property
    def delete_instance(
        self,
    ) -> Callable[[service.DeleteInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes a single Instance.

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
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/DeleteInstance",
                request_serializer=service.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def start_instance(
        self,
    ) -> Callable[[service.StartInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the start instance method over gRPC.

        Starts a notebook instance.

        Returns:
            Callable[[~.StartInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_instance" not in self._stubs:
            self._stubs["start_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/StartInstance",
                request_serializer=service.StartInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_instance"]

    @property
    def stop_instance(
        self,
    ) -> Callable[[service.StopInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the stop instance method over gRPC.

        Stops a notebook instance.

        Returns:
            Callable[[~.StopInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_instance" not in self._stubs:
            self._stubs["stop_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/StopInstance",
                request_serializer=service.StopInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_instance"]

    @property
    def reset_instance(
        self,
    ) -> Callable[[service.ResetInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the reset instance method over gRPC.

        Resets a notebook instance.

        Returns:
            Callable[[~.ResetInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_instance" not in self._stubs:
            self._stubs["reset_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/ResetInstance",
                request_serializer=service.ResetInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reset_instance"]

    @property
    def report_instance_info(
        self,
    ) -> Callable[[service.ReportInstanceInfoRequest], operations_pb2.Operation]:
        r"""Return a callable for the report instance info method over gRPC.

        Allows notebook instances to
        report their latest instance information to the
        Notebooks API server. The server will merge the reported
        information to the instance metadata store. Do not use
        this method directly.

        Returns:
            Callable[[~.ReportInstanceInfoRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "report_instance_info" not in self._stubs:
            self._stubs["report_instance_info"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/ReportInstanceInfo",
                request_serializer=service.ReportInstanceInfoRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["report_instance_info"]

    @property
    def is_instance_upgradeable(
        self,
    ) -> Callable[
        [service.IsInstanceUpgradeableRequest], service.IsInstanceUpgradeableResponse
    ]:
        r"""Return a callable for the is instance upgradeable method over gRPC.

        Check if a notebook instance is upgradable.

        Returns:
            Callable[[~.IsInstanceUpgradeableRequest],
                    ~.IsInstanceUpgradeableResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "is_instance_upgradeable" not in self._stubs:
            self._stubs["is_instance_upgradeable"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/IsInstanceUpgradeable",
                request_serializer=service.IsInstanceUpgradeableRequest.serialize,
                response_deserializer=service.IsInstanceUpgradeableResponse.deserialize,
            )
        return self._stubs["is_instance_upgradeable"]

    @property
    def upgrade_instance(
        self,
    ) -> Callable[[service.UpgradeInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the upgrade instance method over gRPC.

        Upgrades a notebook instance to the latest version.

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
        if "upgrade_instance" not in self._stubs:
            self._stubs["upgrade_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/UpgradeInstance",
                request_serializer=service.UpgradeInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_instance"]

    @property
    def upgrade_instance_internal(
        self,
    ) -> Callable[[service.UpgradeInstanceInternalRequest], operations_pb2.Operation]:
        r"""Return a callable for the upgrade instance internal method over gRPC.

        Allows notebook instances to
        call this endpoint to upgrade themselves. Do not use
        this method directly.

        Returns:
            Callable[[~.UpgradeInstanceInternalRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upgrade_instance_internal" not in self._stubs:
            self._stubs["upgrade_instance_internal"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/UpgradeInstanceInternal",
                request_serializer=service.UpgradeInstanceInternalRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_instance_internal"]

    @property
    def list_environments(
        self,
    ) -> Callable[[service.ListEnvironmentsRequest], service.ListEnvironmentsResponse]:
        r"""Return a callable for the list environments method over gRPC.

        Lists environments in a project.

        Returns:
            Callable[[~.ListEnvironmentsRequest],
                    ~.ListEnvironmentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_environments" not in self._stubs:
            self._stubs["list_environments"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/ListEnvironments",
                request_serializer=service.ListEnvironmentsRequest.serialize,
                response_deserializer=service.ListEnvironmentsResponse.deserialize,
            )
        return self._stubs["list_environments"]

    @property
    def get_environment(
        self,
    ) -> Callable[[service.GetEnvironmentRequest], environment.Environment]:
        r"""Return a callable for the get environment method over gRPC.

        Gets details of a single Environment.

        Returns:
            Callable[[~.GetEnvironmentRequest],
                    ~.Environment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_environment" not in self._stubs:
            self._stubs["get_environment"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/GetEnvironment",
                request_serializer=service.GetEnvironmentRequest.serialize,
                response_deserializer=environment.Environment.deserialize,
            )
        return self._stubs["get_environment"]

    @property
    def create_environment(
        self,
    ) -> Callable[[service.CreateEnvironmentRequest], operations_pb2.Operation]:
        r"""Return a callable for the create environment method over gRPC.

        Creates a new Environment.

        Returns:
            Callable[[~.CreateEnvironmentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_environment" not in self._stubs:
            self._stubs["create_environment"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/CreateEnvironment",
                request_serializer=service.CreateEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_environment"]

    @property
    def delete_environment(
        self,
    ) -> Callable[[service.DeleteEnvironmentRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete environment method over gRPC.

        Deletes a single Environment.

        Returns:
            Callable[[~.DeleteEnvironmentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_environment" not in self._stubs:
            self._stubs["delete_environment"] = self.grpc_channel.unary_unary(
                "/google.cloud.notebooks.v1beta1.NotebookService/DeleteEnvironment",
                request_serializer=service.DeleteEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_environment"]


__all__ = ("NotebookServiceGrpcTransport",)
