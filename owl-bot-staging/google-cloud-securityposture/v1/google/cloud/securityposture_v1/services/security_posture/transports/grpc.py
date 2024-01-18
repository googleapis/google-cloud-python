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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.location import locations_pb2 # type: ignore
from google.cloud.securityposture_v1.types import securityposture
from google.longrunning import operations_pb2 # type: ignore
from .base import SecurityPostureTransport, DEFAULT_CLIENT_INFO


class SecurityPostureGrpcTransport(SecurityPostureTransport):
    """gRPC backend transport for SecurityPosture.

    Service describing handlers for resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'securityposture.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: Optional[grpc.Channel] = None,
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
                       host: str = 'securityposture.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
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
    def list_postures(self) -> Callable[
            [securityposture.ListPosturesRequest],
            securityposture.ListPosturesResponse]:
        r"""Return a callable for the list postures method over gRPC.

        (-- This option restricts the visibility of the API to only
        projects that will (-- be labeled as ``PREVIEW`` or
        ``GOOGLE_INTERNAL`` by the service. (-- option
        (google.api.api_visibility).restriction =
        "PREVIEW,GOOGLE_INTERNAL"; Postures Lists Postures in a given
        organization and location. In case a posture has multiple
        revisions, the latest revision as per UpdateTime will be
        returned.

        Returns:
            Callable[[~.ListPosturesRequest],
                    ~.ListPosturesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_postures' not in self._stubs:
            self._stubs['list_postures'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/ListPostures',
                request_serializer=securityposture.ListPosturesRequest.serialize,
                response_deserializer=securityposture.ListPosturesResponse.deserialize,
            )
        return self._stubs['list_postures']

    @property
    def list_posture_revisions(self) -> Callable[
            [securityposture.ListPostureRevisionsRequest],
            securityposture.ListPostureRevisionsResponse]:
        r"""Return a callable for the list posture revisions method over gRPC.

        Lists revisions of a Posture in a given organization
        and location.

        Returns:
            Callable[[~.ListPostureRevisionsRequest],
                    ~.ListPostureRevisionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_posture_revisions' not in self._stubs:
            self._stubs['list_posture_revisions'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/ListPostureRevisions',
                request_serializer=securityposture.ListPostureRevisionsRequest.serialize,
                response_deserializer=securityposture.ListPostureRevisionsResponse.deserialize,
            )
        return self._stubs['list_posture_revisions']

    @property
    def get_posture(self) -> Callable[
            [securityposture.GetPostureRequest],
            securityposture.Posture]:
        r"""Return a callable for the get posture method over gRPC.

        Gets a posture in a given organization and location. User must
        provide revision_id to retrieve a specific revision of the
        resource. NOT_FOUND error is returned if the revision_id or the
        Posture name does not exist. In case revision_id is not provided
        then the latest Posture revision by UpdateTime is returned.

        Returns:
            Callable[[~.GetPostureRequest],
                    ~.Posture]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_posture' not in self._stubs:
            self._stubs['get_posture'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/GetPosture',
                request_serializer=securityposture.GetPostureRequest.serialize,
                response_deserializer=securityposture.Posture.deserialize,
            )
        return self._stubs['get_posture']

    @property
    def create_posture(self) -> Callable[
            [securityposture.CreatePostureRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create posture method over gRPC.

        Creates a new Posture resource. If a Posture with the specified
        name already exists in the specified organization and location,
        the long running operation returns a
        [ALREADY_EXISTS][google.rpc.Code.ALREADY_EXISTS] error.

        Returns:
            Callable[[~.CreatePostureRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_posture' not in self._stubs:
            self._stubs['create_posture'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/CreatePosture',
                request_serializer=securityposture.CreatePostureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_posture']

    @property
    def update_posture(self) -> Callable[
            [securityposture.UpdatePostureRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update posture method over gRPC.

        Updates an existing Posture. A new revision of the posture will
        be created if the revision to be updated is currently deployed
        on a workload. Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the Posture does not exist.
        Returns a ``google.rpc.Status`` with ``google.rpc.Code.ABORTED``
        if the etag supplied in the request does not match the persisted
        etag of the Posture. Updatable fields are state, description and
        policy_sets. State update operation cannot be clubbed with
        update of description and policy_sets. An ACTIVE posture can be
        updated to both DRAFT or DEPRECATED states. Postures in DRAFT or
        DEPRECATED states can only be updated to ACTIVE state.

        Returns:
            Callable[[~.UpdatePostureRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_posture' not in self._stubs:
            self._stubs['update_posture'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/UpdatePosture',
                request_serializer=securityposture.UpdatePostureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_posture']

    @property
    def delete_posture(self) -> Callable[
            [securityposture.DeletePostureRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete posture method over gRPC.

        Deletes all the revisions of a resource.
        A posture can only be deleted when none of the revisions
        are deployed to any workload.

        Returns:
            Callable[[~.DeletePostureRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_posture' not in self._stubs:
            self._stubs['delete_posture'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/DeletePosture',
                request_serializer=securityposture.DeletePostureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_posture']

    @property
    def extract_posture(self) -> Callable[
            [securityposture.ExtractPostureRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the extract posture method over gRPC.

        Extracts existing policies on a workload as a posture. If a
        Posture on the given workload already exists, the long running
        operation returns a
        [ALREADY_EXISTS][google.rpc.Code.ALREADY_EXISTS] error.

        Returns:
            Callable[[~.ExtractPostureRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'extract_posture' not in self._stubs:
            self._stubs['extract_posture'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/ExtractPosture',
                request_serializer=securityposture.ExtractPostureRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['extract_posture']

    @property
    def list_posture_deployments(self) -> Callable[
            [securityposture.ListPostureDeploymentsRequest],
            securityposture.ListPostureDeploymentsResponse]:
        r"""Return a callable for the list posture deployments method over gRPC.

        PostureDeployments
        Lists PostureDeployments in a given project and
        location.

        Returns:
            Callable[[~.ListPostureDeploymentsRequest],
                    ~.ListPostureDeploymentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_posture_deployments' not in self._stubs:
            self._stubs['list_posture_deployments'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/ListPostureDeployments',
                request_serializer=securityposture.ListPostureDeploymentsRequest.serialize,
                response_deserializer=securityposture.ListPostureDeploymentsResponse.deserialize,
            )
        return self._stubs['list_posture_deployments']

    @property
    def get_posture_deployment(self) -> Callable[
            [securityposture.GetPostureDeploymentRequest],
            securityposture.PostureDeployment]:
        r"""Return a callable for the get posture deployment method over gRPC.

        Gets details of a single PostureDeployment.

        Returns:
            Callable[[~.GetPostureDeploymentRequest],
                    ~.PostureDeployment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_posture_deployment' not in self._stubs:
            self._stubs['get_posture_deployment'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/GetPostureDeployment',
                request_serializer=securityposture.GetPostureDeploymentRequest.serialize,
                response_deserializer=securityposture.PostureDeployment.deserialize,
            )
        return self._stubs['get_posture_deployment']

    @property
    def create_posture_deployment(self) -> Callable[
            [securityposture.CreatePostureDeploymentRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create posture deployment method over gRPC.

        Creates a new PostureDeployment in a given project
        and location.

        Returns:
            Callable[[~.CreatePostureDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_posture_deployment' not in self._stubs:
            self._stubs['create_posture_deployment'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/CreatePostureDeployment',
                request_serializer=securityposture.CreatePostureDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_posture_deployment']

    @property
    def update_posture_deployment(self) -> Callable[
            [securityposture.UpdatePostureDeploymentRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update posture deployment method over gRPC.

        Updates the parameters of a single PostureDeployment.

        Returns:
            Callable[[~.UpdatePostureDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_posture_deployment' not in self._stubs:
            self._stubs['update_posture_deployment'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/UpdatePostureDeployment',
                request_serializer=securityposture.UpdatePostureDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_posture_deployment']

    @property
    def delete_posture_deployment(self) -> Callable[
            [securityposture.DeletePostureDeploymentRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete posture deployment method over gRPC.

        Deletes a single PostureDeployment.

        Returns:
            Callable[[~.DeletePostureDeploymentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_posture_deployment' not in self._stubs:
            self._stubs['delete_posture_deployment'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/DeletePostureDeployment',
                request_serializer=securityposture.DeletePostureDeploymentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_posture_deployment']

    @property
    def list_posture_templates(self) -> Callable[
            [securityposture.ListPostureTemplatesRequest],
            securityposture.ListPostureTemplatesResponse]:
        r"""Return a callable for the list posture templates method over gRPC.

        PostureTemplates
        Lists all the PostureTemplates available to the user.

        Returns:
            Callable[[~.ListPostureTemplatesRequest],
                    ~.ListPostureTemplatesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_posture_templates' not in self._stubs:
            self._stubs['list_posture_templates'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/ListPostureTemplates',
                request_serializer=securityposture.ListPostureTemplatesRequest.serialize,
                response_deserializer=securityposture.ListPostureTemplatesResponse.deserialize,
            )
        return self._stubs['list_posture_templates']

    @property
    def get_posture_template(self) -> Callable[
            [securityposture.GetPostureTemplateRequest],
            securityposture.PostureTemplate]:
        r"""Return a callable for the get posture template method over gRPC.

        Gets a PostureTemplate. User must provide revision_id to
        retrieve a specific revision of the resource. NOT_FOUND error is
        returned if the revision_id or the PostureTemplate name does not
        exist. In case revision_id is not provided then the
        PostureTemplate with latest revision_id is returned.

        Returns:
            Callable[[~.GetPostureTemplateRequest],
                    ~.PostureTemplate]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_posture_template' not in self._stubs:
            self._stubs['get_posture_template'] = self.grpc_channel.unary_unary(
                '/google.cloud.securityposture.v1.SecurityPosture/GetPostureTemplate',
                request_serializer=securityposture.GetPostureTemplateRequest.serialize,
                response_deserializer=securityposture.PostureTemplate.deserialize,
            )
        return self._stubs['get_posture_template']

    def close(self):
        self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[[operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse]:
        r"""Return a callable for the list_operations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[[locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = (
    'SecurityPostureGrpcTransport',
)
