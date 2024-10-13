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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.datacatalog_v1beta1.types import policytagmanager

from .base import DEFAULT_CLIENT_INFO, PolicyTagManagerTransport
from .grpc import PolicyTagManagerGrpcTransport


class PolicyTagManagerGrpcAsyncIOTransport(PolicyTagManagerTransport):
    """gRPC AsyncIO backend transport for PolicyTagManager.

    The policy tag manager API service allows clients to manage
    their taxonomies and policy tags.

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
        host: str = "datacatalog.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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
        host: str = "datacatalog.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'datacatalog.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
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

        if isinstance(channel, aio.Channel):
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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def create_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.CreateTaxonomyRequest], Awaitable[policytagmanager.Taxonomy]
    ]:
        r"""Return a callable for the create taxonomy method over gRPC.

        Creates a taxonomy in the specified project.

        Returns:
            Callable[[~.CreateTaxonomyRequest],
                    Awaitable[~.Taxonomy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_taxonomy" not in self._stubs:
            self._stubs["create_taxonomy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/CreateTaxonomy",
                request_serializer=policytagmanager.CreateTaxonomyRequest.serialize,
                response_deserializer=policytagmanager.Taxonomy.deserialize,
            )
        return self._stubs["create_taxonomy"]

    @property
    def delete_taxonomy(
        self,
    ) -> Callable[[policytagmanager.DeleteTaxonomyRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete taxonomy method over gRPC.

        Deletes a taxonomy. This operation will also delete
        all policy tags in this taxonomy along with their
        associated policies.

        Returns:
            Callable[[~.DeleteTaxonomyRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_taxonomy" not in self._stubs:
            self._stubs["delete_taxonomy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/DeleteTaxonomy",
                request_serializer=policytagmanager.DeleteTaxonomyRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_taxonomy"]

    @property
    def update_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.UpdateTaxonomyRequest], Awaitable[policytagmanager.Taxonomy]
    ]:
        r"""Return a callable for the update taxonomy method over gRPC.

        Updates a taxonomy.

        Returns:
            Callable[[~.UpdateTaxonomyRequest],
                    Awaitable[~.Taxonomy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_taxonomy" not in self._stubs:
            self._stubs["update_taxonomy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/UpdateTaxonomy",
                request_serializer=policytagmanager.UpdateTaxonomyRequest.serialize,
                response_deserializer=policytagmanager.Taxonomy.deserialize,
            )
        return self._stubs["update_taxonomy"]

    @property
    def list_taxonomies(
        self,
    ) -> Callable[
        [policytagmanager.ListTaxonomiesRequest],
        Awaitable[policytagmanager.ListTaxonomiesResponse],
    ]:
        r"""Return a callable for the list taxonomies method over gRPC.

        Lists all taxonomies in a project in a particular
        location that the caller has permission to view.

        Returns:
            Callable[[~.ListTaxonomiesRequest],
                    Awaitable[~.ListTaxonomiesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_taxonomies" not in self._stubs:
            self._stubs["list_taxonomies"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/ListTaxonomies",
                request_serializer=policytagmanager.ListTaxonomiesRequest.serialize,
                response_deserializer=policytagmanager.ListTaxonomiesResponse.deserialize,
            )
        return self._stubs["list_taxonomies"]

    @property
    def get_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.GetTaxonomyRequest], Awaitable[policytagmanager.Taxonomy]
    ]:
        r"""Return a callable for the get taxonomy method over gRPC.

        Gets a taxonomy.

        Returns:
            Callable[[~.GetTaxonomyRequest],
                    Awaitable[~.Taxonomy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_taxonomy" not in self._stubs:
            self._stubs["get_taxonomy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/GetTaxonomy",
                request_serializer=policytagmanager.GetTaxonomyRequest.serialize,
                response_deserializer=policytagmanager.Taxonomy.deserialize,
            )
        return self._stubs["get_taxonomy"]

    @property
    def create_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.CreatePolicyTagRequest], Awaitable[policytagmanager.PolicyTag]
    ]:
        r"""Return a callable for the create policy tag method over gRPC.

        Creates a policy tag in the specified taxonomy.

        Returns:
            Callable[[~.CreatePolicyTagRequest],
                    Awaitable[~.PolicyTag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_policy_tag" not in self._stubs:
            self._stubs["create_policy_tag"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/CreatePolicyTag",
                request_serializer=policytagmanager.CreatePolicyTagRequest.serialize,
                response_deserializer=policytagmanager.PolicyTag.deserialize,
            )
        return self._stubs["create_policy_tag"]

    @property
    def delete_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.DeletePolicyTagRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete policy tag method over gRPC.

        Deletes a policy tag. Also deletes all of its
        descendant policy tags.

        Returns:
            Callable[[~.DeletePolicyTagRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_policy_tag" not in self._stubs:
            self._stubs["delete_policy_tag"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/DeletePolicyTag",
                request_serializer=policytagmanager.DeletePolicyTagRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_policy_tag"]

    @property
    def update_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.UpdatePolicyTagRequest], Awaitable[policytagmanager.PolicyTag]
    ]:
        r"""Return a callable for the update policy tag method over gRPC.

        Updates a policy tag.

        Returns:
            Callable[[~.UpdatePolicyTagRequest],
                    Awaitable[~.PolicyTag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_policy_tag" not in self._stubs:
            self._stubs["update_policy_tag"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/UpdatePolicyTag",
                request_serializer=policytagmanager.UpdatePolicyTagRequest.serialize,
                response_deserializer=policytagmanager.PolicyTag.deserialize,
            )
        return self._stubs["update_policy_tag"]

    @property
    def list_policy_tags(
        self,
    ) -> Callable[
        [policytagmanager.ListPolicyTagsRequest],
        Awaitable[policytagmanager.ListPolicyTagsResponse],
    ]:
        r"""Return a callable for the list policy tags method over gRPC.

        Lists all policy tags in a taxonomy.

        Returns:
            Callable[[~.ListPolicyTagsRequest],
                    Awaitable[~.ListPolicyTagsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_policy_tags" not in self._stubs:
            self._stubs["list_policy_tags"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/ListPolicyTags",
                request_serializer=policytagmanager.ListPolicyTagsRequest.serialize,
                response_deserializer=policytagmanager.ListPolicyTagsResponse.deserialize,
            )
        return self._stubs["list_policy_tags"]

    @property
    def get_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.GetPolicyTagRequest], Awaitable[policytagmanager.PolicyTag]
    ]:
        r"""Return a callable for the get policy tag method over gRPC.

        Gets a policy tag.

        Returns:
            Callable[[~.GetPolicyTagRequest],
                    Awaitable[~.PolicyTag]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_policy_tag" not in self._stubs:
            self._stubs["get_policy_tag"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/GetPolicyTag",
                request_serializer=policytagmanager.GetPolicyTagRequest.serialize,
                response_deserializer=policytagmanager.PolicyTag.deserialize,
            )
        return self._stubs["get_policy_tag"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM policy for a taxonomy or a policy tag.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the IAM policy for a taxonomy or a policy tag.

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns the permissions that a caller has on the
        specified taxonomy or policy tag.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.cloud.datacatalog.v1beta1.PolicyTagManager/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_taxonomy: self._wrap_method(
                self.create_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_taxonomy: self._wrap_method(
                self.delete_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_taxonomy: self._wrap_method(
                self.update_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_taxonomies: self._wrap_method(
                self.list_taxonomies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_taxonomy: self._wrap_method(
                self.get_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_policy_tag: self._wrap_method(
                self.create_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_policy_tag: self._wrap_method(
                self.delete_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_policy_tag: self._wrap_method(
                self.update_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_policy_tags: self._wrap_method(
                self.list_policy_tags,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_policy_tag: self._wrap_method(
                self.get_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("PolicyTagManagerGrpcAsyncIOTransport",)
