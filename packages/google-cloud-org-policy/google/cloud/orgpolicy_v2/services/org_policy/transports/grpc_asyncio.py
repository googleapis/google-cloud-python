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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.orgpolicy_v2.types import orgpolicy
from google.protobuf import empty_pb2  # type: ignore
from .base import OrgPolicyTransport, DEFAULT_CLIENT_INFO
from .grpc import OrgPolicyGrpcTransport


class OrgPolicyGrpcAsyncIOTransport(OrgPolicyTransport):
    """gRPC AsyncIO backend transport for OrgPolicy.

    An interface for managing organization policies.

    The Cloud Org Policy service provides a simple mechanism for
    organizations to restrict the allowed configurations across their
    entire Cloud Resource hierarchy.

    You can use a ``policy`` to configure restrictions in Cloud
    resources. For example, you can enforce a ``policy`` that restricts
    which Google Cloud Platform APIs can be activated in a certain part
    of your resource hierarchy, or prevents serial port access to VM
    instances in a particular folder.

    ``Policies`` are inherited down through the resource hierarchy. A
    ``policy`` applied to a parent resource automatically applies to all
    its child resources unless overridden with a ``policy`` lower in the
    hierarchy.

    A ``constraint`` defines an aspect of a resource's configuration
    that can be controlled by an organization's policy administrator.
    ``Policies`` are a collection of ``constraints`` that defines their
    allowable configuration on a particular resource and its child
    resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "orgpolicy.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "orgpolicy.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

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

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_constraints(
        self,
    ) -> Callable[
        [orgpolicy.ListConstraintsRequest], Awaitable[orgpolicy.ListConstraintsResponse]
    ]:
        r"""Return a callable for the list constraints method over gRPC.

        Lists ``Constraints`` that could be applied on the specified
        resource.

        Returns:
            Callable[[~.ListConstraintsRequest],
                    Awaitable[~.ListConstraintsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_constraints" not in self._stubs:
            self._stubs["list_constraints"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/ListConstraints",
                request_serializer=orgpolicy.ListConstraintsRequest.serialize,
                response_deserializer=orgpolicy.ListConstraintsResponse.deserialize,
            )
        return self._stubs["list_constraints"]

    @property
    def list_policies(
        self,
    ) -> Callable[
        [orgpolicy.ListPoliciesRequest], Awaitable[orgpolicy.ListPoliciesResponse]
    ]:
        r"""Return a callable for the list policies method over gRPC.

        Retrieves all of the ``Policies`` that exist on a particular
        resource.

        Returns:
            Callable[[~.ListPoliciesRequest],
                    Awaitable[~.ListPoliciesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_policies" not in self._stubs:
            self._stubs["list_policies"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/ListPolicies",
                request_serializer=orgpolicy.ListPoliciesRequest.serialize,
                response_deserializer=orgpolicy.ListPoliciesResponse.deserialize,
            )
        return self._stubs["list_policies"]

    @property
    def get_policy(
        self,
    ) -> Callable[[orgpolicy.GetPolicyRequest], Awaitable[orgpolicy.Policy]]:
        r"""Return a callable for the get policy method over gRPC.

        Gets a ``Policy`` on a resource.

        If no ``Policy`` is set on the resource, NOT_FOUND is returned.
        The ``etag`` value can be used with ``UpdatePolicy()`` to update
        a ``Policy`` during read-modify-write.

        Returns:
            Callable[[~.GetPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_policy" not in self._stubs:
            self._stubs["get_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/GetPolicy",
                request_serializer=orgpolicy.GetPolicyRequest.serialize,
                response_deserializer=orgpolicy.Policy.deserialize,
            )
        return self._stubs["get_policy"]

    @property
    def get_effective_policy(
        self,
    ) -> Callable[[orgpolicy.GetEffectivePolicyRequest], Awaitable[orgpolicy.Policy]]:
        r"""Return a callable for the get effective policy method over gRPC.

        Gets the effective ``Policy`` on a resource. This is the result
        of merging ``Policies`` in the resource hierarchy and evaluating
        conditions. The returned ``Policy`` will not have an ``etag`` or
        ``condition`` set because it is a computed ``Policy`` across
        multiple resources. Subtrees of Resource Manager resource
        hierarchy with 'under:' prefix will not be expanded.

        Returns:
            Callable[[~.GetEffectivePolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_effective_policy" not in self._stubs:
            self._stubs["get_effective_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/GetEffectivePolicy",
                request_serializer=orgpolicy.GetEffectivePolicyRequest.serialize,
                response_deserializer=orgpolicy.Policy.deserialize,
            )
        return self._stubs["get_effective_policy"]

    @property
    def create_policy(
        self,
    ) -> Callable[[orgpolicy.CreatePolicyRequest], Awaitable[orgpolicy.Policy]]:
        r"""Return a callable for the create policy method over gRPC.

        Creates a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint does not exist.
        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ALREADY_EXISTS`` if the policy already exists
        on the given Cloud resource.

        Returns:
            Callable[[~.CreatePolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_policy" not in self._stubs:
            self._stubs["create_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/CreatePolicy",
                request_serializer=orgpolicy.CreatePolicyRequest.serialize,
                response_deserializer=orgpolicy.Policy.deserialize,
            )
        return self._stubs["create_policy"]

    @property
    def update_policy(
        self,
    ) -> Callable[[orgpolicy.UpdatePolicyRequest], Awaitable[orgpolicy.Policy]]:
        r"""Return a callable for the update policy method over gRPC.

        Updates a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint or the policy do
        not exist. Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ABORTED`` if the etag supplied in the request
        does not match the persisted etag of the policy

        Note: the supplied policy will perform a full overwrite of all
        fields.

        Returns:
            Callable[[~.UpdatePolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_policy" not in self._stubs:
            self._stubs["update_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/UpdatePolicy",
                request_serializer=orgpolicy.UpdatePolicyRequest.serialize,
                response_deserializer=orgpolicy.Policy.deserialize,
            )
        return self._stubs["update_policy"]

    @property
    def delete_policy(
        self,
    ) -> Callable[[orgpolicy.DeletePolicyRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete policy method over gRPC.

        Deletes a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint or Org Policy
        does not exist.

        Returns:
            Callable[[~.DeletePolicyRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_policy" not in self._stubs:
            self._stubs["delete_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.orgpolicy.v2.OrgPolicy/DeletePolicy",
                request_serializer=orgpolicy.DeletePolicyRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_policy"]


__all__ = ("OrgPolicyGrpcAsyncIOTransport",)
