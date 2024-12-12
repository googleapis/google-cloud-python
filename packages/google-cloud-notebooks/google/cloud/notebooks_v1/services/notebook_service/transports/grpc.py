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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.notebooks_v1.types import (
    environment,
    execution,
    instance,
    schedule,
    service,
)

from .base import DEFAULT_CLIENT_INFO, NotebookServiceTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.notebooks.v1.NotebookService",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.notebooks.v1.NotebookService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class NotebookServiceGrpcTransport(NotebookServiceTransport):
    """gRPC backend transport for NotebookService.

    API v1 service for Cloud AI Platform Notebooks.

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
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'notebooks.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
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

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "notebooks.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
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
        """Return the channel designed to connect to this service."""
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
                self._logged_channel
            )

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
            self._stubs["list_instances"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ListInstances",
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
            self._stubs["get_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/GetInstance",
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
            self._stubs["create_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/CreateInstance",
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
            self._stubs["register_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/RegisterInstance",
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
            self._stubs["set_instance_accelerator"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/SetInstanceAccelerator",
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
            self._stubs["set_instance_machine_type"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/SetInstanceMachineType",
                request_serializer=service.SetInstanceMachineTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_instance_machine_type"]

    @property
    def update_instance_config(
        self,
    ) -> Callable[[service.UpdateInstanceConfigRequest], operations_pb2.Operation]:
        r"""Return a callable for the update instance config method over gRPC.

        Update Notebook Instance configurations.

        Returns:
            Callable[[~.UpdateInstanceConfigRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance_config" not in self._stubs:
            self._stubs["update_instance_config"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/UpdateInstanceConfig",
                request_serializer=service.UpdateInstanceConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_instance_config"]

    @property
    def update_shielded_instance_config(
        self,
    ) -> Callable[
        [service.UpdateShieldedInstanceConfigRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update shielded instance
        config method over gRPC.

        Updates the Shielded instance configuration of a
        single Instance.

        Returns:
            Callable[[~.UpdateShieldedInstanceConfigRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_shielded_instance_config" not in self._stubs:
            self._stubs[
                "update_shielded_instance_config"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/UpdateShieldedInstanceConfig",
                request_serializer=service.UpdateShieldedInstanceConfigRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_shielded_instance_config"]

    @property
    def set_instance_labels(
        self,
    ) -> Callable[[service.SetInstanceLabelsRequest], operations_pb2.Operation]:
        r"""Return a callable for the set instance labels method over gRPC.

        Replaces all the labels of an Instance.

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
            self._stubs["set_instance_labels"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/SetInstanceLabels",
                request_serializer=service.SetInstanceLabelsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_instance_labels"]

    @property
    def update_instance_metadata_items(
        self,
    ) -> Callable[
        [service.UpdateInstanceMetadataItemsRequest],
        service.UpdateInstanceMetadataItemsResponse,
    ]:
        r"""Return a callable for the update instance metadata items method over gRPC.

        Add/update metadata items for an instance.

        Returns:
            Callable[[~.UpdateInstanceMetadataItemsRequest],
                    ~.UpdateInstanceMetadataItemsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance_metadata_items" not in self._stubs:
            self._stubs[
                "update_instance_metadata_items"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/UpdateInstanceMetadataItems",
                request_serializer=service.UpdateInstanceMetadataItemsRequest.serialize,
                response_deserializer=service.UpdateInstanceMetadataItemsResponse.deserialize,
            )
        return self._stubs["update_instance_metadata_items"]

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
            self._stubs["delete_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/DeleteInstance",
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
            self._stubs["start_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/StartInstance",
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
            self._stubs["stop_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/StopInstance",
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
            self._stubs["reset_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ResetInstance",
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
            self._stubs["report_instance_info"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ReportInstanceInfo",
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
            self._stubs["is_instance_upgradeable"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/IsInstanceUpgradeable",
                request_serializer=service.IsInstanceUpgradeableRequest.serialize,
                response_deserializer=service.IsInstanceUpgradeableResponse.deserialize,
            )
        return self._stubs["is_instance_upgradeable"]

    @property
    def get_instance_health(
        self,
    ) -> Callable[
        [service.GetInstanceHealthRequest], service.GetInstanceHealthResponse
    ]:
        r"""Return a callable for the get instance health method over gRPC.

        Check if a notebook instance is healthy.

        Returns:
            Callable[[~.GetInstanceHealthRequest],
                    ~.GetInstanceHealthResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance_health" not in self._stubs:
            self._stubs["get_instance_health"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/GetInstanceHealth",
                request_serializer=service.GetInstanceHealthRequest.serialize,
                response_deserializer=service.GetInstanceHealthResponse.deserialize,
            )
        return self._stubs["get_instance_health"]

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
            self._stubs["upgrade_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/UpgradeInstance",
                request_serializer=service.UpgradeInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_instance"]

    @property
    def rollback_instance(
        self,
    ) -> Callable[[service.RollbackInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the rollback instance method over gRPC.

        Rollbacks a notebook instance to the previous
        version.

        Returns:
            Callable[[~.RollbackInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rollback_instance" not in self._stubs:
            self._stubs["rollback_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/RollbackInstance",
                request_serializer=service.RollbackInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["rollback_instance"]

    @property
    def diagnose_instance(
        self,
    ) -> Callable[[service.DiagnoseInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the diagnose instance method over gRPC.

        Creates a Diagnostic File and runs Diagnostic Tool
        given an Instance.

        Returns:
            Callable[[~.DiagnoseInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "diagnose_instance" not in self._stubs:
            self._stubs["diagnose_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/DiagnoseInstance",
                request_serializer=service.DiagnoseInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["diagnose_instance"]

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
            self._stubs["upgrade_instance_internal"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/UpgradeInstanceInternal",
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
            self._stubs["list_environments"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ListEnvironments",
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
            self._stubs["get_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/GetEnvironment",
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
            self._stubs["create_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/CreateEnvironment",
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
            self._stubs["delete_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/DeleteEnvironment",
                request_serializer=service.DeleteEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_environment"]

    @property
    def list_schedules(
        self,
    ) -> Callable[[service.ListSchedulesRequest], service.ListSchedulesResponse]:
        r"""Return a callable for the list schedules method over gRPC.

        Lists schedules in a given project and location.

        Returns:
            Callable[[~.ListSchedulesRequest],
                    ~.ListSchedulesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_schedules" not in self._stubs:
            self._stubs["list_schedules"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ListSchedules",
                request_serializer=service.ListSchedulesRequest.serialize,
                response_deserializer=service.ListSchedulesResponse.deserialize,
            )
        return self._stubs["list_schedules"]

    @property
    def get_schedule(self) -> Callable[[service.GetScheduleRequest], schedule.Schedule]:
        r"""Return a callable for the get schedule method over gRPC.

        Gets details of schedule

        Returns:
            Callable[[~.GetScheduleRequest],
                    ~.Schedule]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_schedule" not in self._stubs:
            self._stubs["get_schedule"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/GetSchedule",
                request_serializer=service.GetScheduleRequest.serialize,
                response_deserializer=schedule.Schedule.deserialize,
            )
        return self._stubs["get_schedule"]

    @property
    def delete_schedule(
        self,
    ) -> Callable[[service.DeleteScheduleRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete schedule method over gRPC.

        Deletes schedule and all underlying jobs

        Returns:
            Callable[[~.DeleteScheduleRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_schedule" not in self._stubs:
            self._stubs["delete_schedule"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/DeleteSchedule",
                request_serializer=service.DeleteScheduleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_schedule"]

    @property
    def create_schedule(
        self,
    ) -> Callable[[service.CreateScheduleRequest], operations_pb2.Operation]:
        r"""Return a callable for the create schedule method over gRPC.

        Creates a new Scheduled Notebook in a given project
        and location.

        Returns:
            Callable[[~.CreateScheduleRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_schedule" not in self._stubs:
            self._stubs["create_schedule"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/CreateSchedule",
                request_serializer=service.CreateScheduleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_schedule"]

    @property
    def trigger_schedule(
        self,
    ) -> Callable[[service.TriggerScheduleRequest], operations_pb2.Operation]:
        r"""Return a callable for the trigger schedule method over gRPC.

        Triggers execution of an existing schedule.

        Returns:
            Callable[[~.TriggerScheduleRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "trigger_schedule" not in self._stubs:
            self._stubs["trigger_schedule"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/TriggerSchedule",
                request_serializer=service.TriggerScheduleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["trigger_schedule"]

    @property
    def list_executions(
        self,
    ) -> Callable[[service.ListExecutionsRequest], service.ListExecutionsResponse]:
        r"""Return a callable for the list executions method over gRPC.

        Lists executions in a given project and location

        Returns:
            Callable[[~.ListExecutionsRequest],
                    ~.ListExecutionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_executions" not in self._stubs:
            self._stubs["list_executions"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/ListExecutions",
                request_serializer=service.ListExecutionsRequest.serialize,
                response_deserializer=service.ListExecutionsResponse.deserialize,
            )
        return self._stubs["list_executions"]

    @property
    def get_execution(
        self,
    ) -> Callable[[service.GetExecutionRequest], execution.Execution]:
        r"""Return a callable for the get execution method over gRPC.

        Gets details of executions

        Returns:
            Callable[[~.GetExecutionRequest],
                    ~.Execution]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_execution" not in self._stubs:
            self._stubs["get_execution"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/GetExecution",
                request_serializer=service.GetExecutionRequest.serialize,
                response_deserializer=execution.Execution.deserialize,
            )
        return self._stubs["get_execution"]

    @property
    def delete_execution(
        self,
    ) -> Callable[[service.DeleteExecutionRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete execution method over gRPC.

        Deletes execution

        Returns:
            Callable[[~.DeleteExecutionRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_execution" not in self._stubs:
            self._stubs["delete_execution"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/DeleteExecution",
                request_serializer=service.DeleteExecutionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_execution"]

    @property
    def create_execution(
        self,
    ) -> Callable[[service.CreateExecutionRequest], operations_pb2.Operation]:
        r"""Return a callable for the create execution method over gRPC.

        Creates a new Execution in a given project and
        location.

        Returns:
            Callable[[~.CreateExecutionRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_execution" not in self._stubs:
            self._stubs["create_execution"] = self._logged_channel.unary_unary(
                "/google.cloud.notebooks.v1.NotebookService/CreateExecution",
                request_serializer=service.CreateExecutionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_execution"]

    def close(self):
        self._logged_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self._logged_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("NotebookServiceGrpcTransport",)
