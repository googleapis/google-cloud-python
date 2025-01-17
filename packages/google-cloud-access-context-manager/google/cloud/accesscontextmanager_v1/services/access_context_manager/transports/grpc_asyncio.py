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
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.accesscontextmanager_v1.types import (
    access_context_manager,
    access_level,
    access_policy,
    gcp_user_access_binding,
    service_perimeter,
)

from .base import DEFAULT_CLIENT_INFO, AccessContextManagerTransport
from .grpc import AccessContextManagerGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
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
                    "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
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
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.identity.accesscontextmanager.v1.AccessContextManager",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class AccessContextManagerGrpcAsyncIOTransport(AccessContextManagerTransport):
    """gRPC AsyncIO backend transport for AccessContextManager.

    API for setting [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter] for
    Google Cloud projects. Each organization has one [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] that contains
    the [access levels]
    [google.identity.accesscontextmanager.v1.AccessLevel] and [service
    perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter]. This
    [access policy]
    [google.identity.accesscontextmanager.v1.AccessPolicy] is applicable
    to all resources in the organization. AccessPolicies

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
        host: str = "accesscontextmanager.googleapis.com",
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
        host: str = "accesscontextmanager.googleapis.com",
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
                 The hostname to connect to (default: 'accesscontextmanager.googleapis.com').
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
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
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
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def list_access_policies(
        self,
    ) -> Callable[
        [access_context_manager.ListAccessPoliciesRequest],
        Awaitable[access_context_manager.ListAccessPoliciesResponse],
    ]:
        r"""Return a callable for the list access policies method over gRPC.

        Lists all [access policies]
        [google.identity.accesscontextmanager.v1.AccessPolicy] in an
        organization.

        Returns:
            Callable[[~.ListAccessPoliciesRequest],
                    Awaitable[~.ListAccessPoliciesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_access_policies" not in self._stubs:
            self._stubs["list_access_policies"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ListAccessPolicies",
                request_serializer=access_context_manager.ListAccessPoliciesRequest.serialize,
                response_deserializer=access_context_manager.ListAccessPoliciesResponse.deserialize,
            )
        return self._stubs["list_access_policies"]

    @property
    def get_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.GetAccessPolicyRequest],
        Awaitable[access_policy.AccessPolicy],
    ]:
        r"""Return a callable for the get access policy method over gRPC.

        Returns an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] based on
        the name.

        Returns:
            Callable[[~.GetAccessPolicyRequest],
                    Awaitable[~.AccessPolicy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_access_policy" not in self._stubs:
            self._stubs["get_access_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/GetAccessPolicy",
                request_serializer=access_context_manager.GetAccessPolicyRequest.serialize,
                response_deserializer=access_policy.AccessPolicy.deserialize,
            )
        return self._stubs["get_access_policy"]

    @property
    def create_access_policy(
        self,
    ) -> Callable[[access_policy.AccessPolicy], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the create access policy method over gRPC.

        Creates an access policy. This method fails if the organization
        already has an access policy. The long-running operation has a
        successful status after the access policy propagates to
        long-lasting storage. Syntactic and basic semantic errors are
        returned in ``metadata`` as a BadRequest proto.

        Returns:
            Callable[[~.AccessPolicy],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_access_policy" not in self._stubs:
            self._stubs["create_access_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/CreateAccessPolicy",
                request_serializer=access_policy.AccessPolicy.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_access_policy"]

    @property
    def update_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.UpdateAccessPolicyRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update access policy method over gRPC.

        Updates an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy]. The
        long-running operation from this RPC has a successful status
        after the changes to the [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] propagate
        to long-lasting storage.

        Returns:
            Callable[[~.UpdateAccessPolicyRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_access_policy" not in self._stubs:
            self._stubs["update_access_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/UpdateAccessPolicy",
                request_serializer=access_context_manager.UpdateAccessPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_access_policy"]

    @property
    def delete_access_policy(
        self,
    ) -> Callable[
        [access_context_manager.DeleteAccessPolicyRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete access policy method over gRPC.

        Deletes an [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] based on
        the resource name. The long-running operation has a successful
        status after the [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] is
        removed from long-lasting storage.

        Returns:
            Callable[[~.DeleteAccessPolicyRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_access_policy" not in self._stubs:
            self._stubs["delete_access_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/DeleteAccessPolicy",
                request_serializer=access_context_manager.DeleteAccessPolicyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_access_policy"]

    @property
    def list_access_levels(
        self,
    ) -> Callable[
        [access_context_manager.ListAccessLevelsRequest],
        Awaitable[access_context_manager.ListAccessLevelsResponse],
    ]:
        r"""Return a callable for the list access levels method over gRPC.

        Lists all [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] for an
        access policy.

        Returns:
            Callable[[~.ListAccessLevelsRequest],
                    Awaitable[~.ListAccessLevelsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_access_levels" not in self._stubs:
            self._stubs["list_access_levels"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ListAccessLevels",
                request_serializer=access_context_manager.ListAccessLevelsRequest.serialize,
                response_deserializer=access_context_manager.ListAccessLevelsResponse.deserialize,
            )
        return self._stubs["list_access_levels"]

    @property
    def get_access_level(
        self,
    ) -> Callable[
        [access_context_manager.GetAccessLevelRequest],
        Awaitable[access_level.AccessLevel],
    ]:
        r"""Return a callable for the get access level method over gRPC.

        Gets an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] based on
        the resource name.

        Returns:
            Callable[[~.GetAccessLevelRequest],
                    Awaitable[~.AccessLevel]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_access_level" not in self._stubs:
            self._stubs["get_access_level"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/GetAccessLevel",
                request_serializer=access_context_manager.GetAccessLevelRequest.serialize,
                response_deserializer=access_level.AccessLevel.deserialize,
            )
        return self._stubs["get_access_level"]

    @property
    def create_access_level(
        self,
    ) -> Callable[
        [access_context_manager.CreateAccessLevelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create access level method over gRPC.

        Creates an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel]. The
        long-running operation from this RPC has a successful status
        after the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] propagates
        to long-lasting storage. If [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contain
        errors, an error response is returned for the first error
        encountered.

        Returns:
            Callable[[~.CreateAccessLevelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_access_level" not in self._stubs:
            self._stubs["create_access_level"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/CreateAccessLevel",
                request_serializer=access_context_manager.CreateAccessLevelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_access_level"]

    @property
    def update_access_level(
        self,
    ) -> Callable[
        [access_context_manager.UpdateAccessLevelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update access level method over gRPC.

        Updates an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel]. The
        long-running operation from this RPC has a successful status
        after the changes to the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] propagate
        to long-lasting storage. If [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contain
        errors, an error response is returned for the first error
        encountered.

        Returns:
            Callable[[~.UpdateAccessLevelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_access_level" not in self._stubs:
            self._stubs["update_access_level"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/UpdateAccessLevel",
                request_serializer=access_context_manager.UpdateAccessLevelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_access_level"]

    @property
    def delete_access_level(
        self,
    ) -> Callable[
        [access_context_manager.DeleteAccessLevelRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete access level method over gRPC.

        Deletes an [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] based on
        the resource name. The long-running operation from this RPC has
        a successful status after the [access level]
        [google.identity.accesscontextmanager.v1.AccessLevel] has been
        removed from long-lasting storage.

        Returns:
            Callable[[~.DeleteAccessLevelRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_access_level" not in self._stubs:
            self._stubs["delete_access_level"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/DeleteAccessLevel",
                request_serializer=access_context_manager.DeleteAccessLevelRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_access_level"]

    @property
    def replace_access_levels(
        self,
    ) -> Callable[
        [access_context_manager.ReplaceAccessLevelsRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the replace access levels method over gRPC.

        Replaces all existing [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] in an
        [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] with the
        [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] provided.
        This is done atomically. The long-running operation from this
        RPC has a successful status after all replacements propagate to
        long-lasting storage. If the replacement contains errors, an
        error response is returned for the first error encountered. Upon
        error, the replacement is cancelled, and existing [access
        levels] [google.identity.accesscontextmanager.v1.AccessLevel]
        are not affected. The Operation.response field contains
        ReplaceAccessLevelsResponse. Removing [access levels]
        [google.identity.accesscontextmanager.v1.AccessLevel] contained
        in existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        result in an error.

        Returns:
            Callable[[~.ReplaceAccessLevelsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "replace_access_levels" not in self._stubs:
            self._stubs["replace_access_levels"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ReplaceAccessLevels",
                request_serializer=access_context_manager.ReplaceAccessLevelsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["replace_access_levels"]

    @property
    def list_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.ListServicePerimetersRequest],
        Awaitable[access_context_manager.ListServicePerimetersResponse],
    ]:
        r"""Return a callable for the list service perimeters method over gRPC.

        Lists all [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] for
        an access policy.

        Returns:
            Callable[[~.ListServicePerimetersRequest],
                    Awaitable[~.ListServicePerimetersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_service_perimeters" not in self._stubs:
            self._stubs["list_service_perimeters"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ListServicePerimeters",
                request_serializer=access_context_manager.ListServicePerimetersRequest.serialize,
                response_deserializer=access_context_manager.ListServicePerimetersResponse.deserialize,
            )
        return self._stubs["list_service_perimeters"]

    @property
    def get_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.GetServicePerimeterRequest],
        Awaitable[service_perimeter.ServicePerimeter],
    ]:
        r"""Return a callable for the get service perimeter method over gRPC.

        Gets a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] based
        on the resource name.

        Returns:
            Callable[[~.GetServicePerimeterRequest],
                    Awaitable[~.ServicePerimeter]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service_perimeter" not in self._stubs:
            self._stubs["get_service_perimeter"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/GetServicePerimeter",
                request_serializer=access_context_manager.GetServicePerimeterRequest.serialize,
                response_deserializer=service_perimeter.ServicePerimeter.deserialize,
            )
        return self._stubs["get_service_perimeter"]

    @property
    def create_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.CreateServicePerimeterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create service perimeter method over gRPC.

        Creates a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]. The
        long-running operation from this RPC has a successful status
        after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        propagates to long-lasting storage. If a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        contains errors, an error response is returned for the first
        error encountered.

        Returns:
            Callable[[~.CreateServicePerimeterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service_perimeter" not in self._stubs:
            self._stubs["create_service_perimeter"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/CreateServicePerimeter",
                request_serializer=access_context_manager.CreateServicePerimeterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_service_perimeter"]

    @property
    def update_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.UpdateServicePerimeterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update service perimeter method over gRPC.

        Updates a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]. The
        long-running operation from this RPC has a successful status
        after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        propagates to long-lasting storage. If a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        contains errors, an error response is returned for the first
        error encountered.

        Returns:
            Callable[[~.UpdateServicePerimeterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service_perimeter" not in self._stubs:
            self._stubs["update_service_perimeter"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/UpdateServicePerimeter",
                request_serializer=access_context_manager.UpdateServicePerimeterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_service_perimeter"]

    @property
    def delete_service_perimeter(
        self,
    ) -> Callable[
        [access_context_manager.DeleteServicePerimeterRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete service perimeter method over gRPC.

        Deletes a [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] based
        on the resource name. The long-running operation from this RPC
        has a successful status after the [service perimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] is
        removed from long-lasting storage.

        Returns:
            Callable[[~.DeleteServicePerimeterRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service_perimeter" not in self._stubs:
            self._stubs["delete_service_perimeter"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/DeleteServicePerimeter",
                request_serializer=access_context_manager.DeleteServicePerimeterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_service_perimeter"]

    @property
    def replace_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.ReplaceServicePerimetersRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the replace service perimeters method over gRPC.

        Replace all existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] in an
        [access policy]
        [google.identity.accesscontextmanager.v1.AccessPolicy] with the
        [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter]
        provided. This is done atomically. The long-running operation
        from this RPC has a successful status after all replacements
        propagate to long-lasting storage. Replacements containing
        errors result in an error response for the first error
        encountered. Upon an error, replacement are cancelled and
        existing [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] are
        not affected. The Operation.response field contains
        ReplaceServicePerimetersResponse.

        Returns:
            Callable[[~.ReplaceServicePerimetersRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "replace_service_perimeters" not in self._stubs:
            self._stubs[
                "replace_service_perimeters"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ReplaceServicePerimeters",
                request_serializer=access_context_manager.ReplaceServicePerimetersRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["replace_service_perimeters"]

    @property
    def commit_service_perimeters(
        self,
    ) -> Callable[
        [access_context_manager.CommitServicePerimetersRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the commit service perimeters method over gRPC.

        Commits the dry-run specification for all the [service
        perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] in an
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy]. A
        commit operation on a service perimeter involves copying its
        ``spec`` field to the ``status`` field of the service perimeter.
        Only [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] with
        ``use_explicit_dry_run_spec`` field set to true are affected by
        a commit operation. The long-running operation from this RPC has
        a successful status after the dry-run specifications for all the
        [service perimeters]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] have
        been committed. If a commit fails, it causes the long-running
        operation to return an error response and the entire commit
        operation is cancelled. When successful, the Operation.response
        field contains CommitServicePerimetersResponse. The ``dry_run``
        and the ``spec`` fields are cleared after a successful commit
        operation.

        Returns:
            Callable[[~.CommitServicePerimetersRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "commit_service_perimeters" not in self._stubs:
            self._stubs["commit_service_perimeters"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/CommitServicePerimeters",
                request_serializer=access_context_manager.CommitServicePerimetersRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["commit_service_perimeters"]

    @property
    def list_gcp_user_access_bindings(
        self,
    ) -> Callable[
        [access_context_manager.ListGcpUserAccessBindingsRequest],
        Awaitable[access_context_manager.ListGcpUserAccessBindingsResponse],
    ]:
        r"""Return a callable for the list gcp user access bindings method over gRPC.

        Lists all [GcpUserAccessBindings]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        for a Google Cloud organization.

        Returns:
            Callable[[~.ListGcpUserAccessBindingsRequest],
                    Awaitable[~.ListGcpUserAccessBindingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_gcp_user_access_bindings" not in self._stubs:
            self._stubs[
                "list_gcp_user_access_bindings"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/ListGcpUserAccessBindings",
                request_serializer=access_context_manager.ListGcpUserAccessBindingsRequest.serialize,
                response_deserializer=access_context_manager.ListGcpUserAccessBindingsResponse.deserialize,
            )
        return self._stubs["list_gcp_user_access_bindings"]

    @property
    def get_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.GetGcpUserAccessBindingRequest],
        Awaitable[gcp_user_access_binding.GcpUserAccessBinding],
    ]:
        r"""Return a callable for the get gcp user access binding method over gRPC.

        Gets the [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        with the given name.

        Returns:
            Callable[[~.GetGcpUserAccessBindingRequest],
                    Awaitable[~.GcpUserAccessBinding]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_gcp_user_access_binding" not in self._stubs:
            self._stubs[
                "get_gcp_user_access_binding"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/GetGcpUserAccessBinding",
                request_serializer=access_context_manager.GetGcpUserAccessBindingRequest.serialize,
                response_deserializer=gcp_user_access_binding.GcpUserAccessBinding.deserialize,
            )
        return self._stubs["get_gcp_user_access_binding"]

    @property
    def create_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.CreateGcpUserAccessBindingRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create gcp user access binding method over gRPC.

        Creates a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        If the client specifies a [name]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding.name],
        the server ignores it. Fails if a resource already exists with
        the same [group_key]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding.group_key].
        Completion of this long-running operation does not necessarily
        signify that the new binding is deployed onto all affected
        users, which may take more time.

        Returns:
            Callable[[~.CreateGcpUserAccessBindingRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_gcp_user_access_binding" not in self._stubs:
            self._stubs[
                "create_gcp_user_access_binding"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/CreateGcpUserAccessBinding",
                request_serializer=access_context_manager.CreateGcpUserAccessBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_gcp_user_access_binding"]

    @property
    def update_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.UpdateGcpUserAccessBindingRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the update gcp user access binding method over gRPC.

        Updates a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        Completion of this long-running operation does not necessarily
        signify that the changed binding is deployed onto all affected
        users, which may take more time.

        Returns:
            Callable[[~.UpdateGcpUserAccessBindingRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_gcp_user_access_binding" not in self._stubs:
            self._stubs[
                "update_gcp_user_access_binding"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/UpdateGcpUserAccessBinding",
                request_serializer=access_context_manager.UpdateGcpUserAccessBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_gcp_user_access_binding"]

    @property
    def delete_gcp_user_access_binding(
        self,
    ) -> Callable[
        [access_context_manager.DeleteGcpUserAccessBindingRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete gcp user access binding method over gRPC.

        Deletes a [GcpUserAccessBinding]
        [google.identity.accesscontextmanager.v1.GcpUserAccessBinding].
        Completion of this long-running operation does not necessarily
        signify that the binding deletion is deployed onto all affected
        users, which may take more time.

        Returns:
            Callable[[~.DeleteGcpUserAccessBindingRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_gcp_user_access_binding" not in self._stubs:
            self._stubs[
                "delete_gcp_user_access_binding"
            ] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/DeleteGcpUserAccessBinding",
                request_serializer=access_context_manager.DeleteGcpUserAccessBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_gcp_user_access_binding"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the IAM policy for the specified Access Context Manager
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].
        This method replaces the existing IAM policy on the access
        policy. The IAM policy controls the set of users who can perform
        specific operations on the Access Context Manager [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].

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
            self._stubs["set_iam_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM policy for the specified Access Context Manager
        [access
        policy][google.identity.accesscontextmanager.v1.AccessPolicy].

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
            self._stubs["get_iam_policy"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns the IAM permissions that the caller has on the specified
        Access Context Manager resource. The resource can be an
        [AccessPolicy][google.identity.accesscontextmanager.v1.AccessPolicy],
        [AccessLevel][google.identity.accesscontextmanager.v1.AccessLevel],
        or
        [ServicePerimeter][google.identity.accesscontextmanager.v1.ServicePerimeter
        ]. This method does not support other resources.

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
            self._stubs["test_iam_permissions"] = self._logged_channel.unary_unary(
                "/google.identity.accesscontextmanager.v1.AccessContextManager/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_access_policies: self._wrap_method(
                self.list_access_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_access_policy: self._wrap_method(
                self.get_access_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_access_policy: self._wrap_method(
                self.create_access_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_access_policy: self._wrap_method(
                self.update_access_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_access_policy: self._wrap_method(
                self.delete_access_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_access_levels: self._wrap_method(
                self.list_access_levels,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_access_level: self._wrap_method(
                self.get_access_level,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_access_level: self._wrap_method(
                self.create_access_level,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_access_level: self._wrap_method(
                self.update_access_level,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_access_level: self._wrap_method(
                self.delete_access_level,
                default_timeout=None,
                client_info=client_info,
            ),
            self.replace_access_levels: self._wrap_method(
                self.replace_access_levels,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_service_perimeters: self._wrap_method(
                self.list_service_perimeters,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_perimeter: self._wrap_method(
                self.get_service_perimeter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service_perimeter: self._wrap_method(
                self.create_service_perimeter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_service_perimeter: self._wrap_method(
                self.update_service_perimeter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_service_perimeter: self._wrap_method(
                self.delete_service_perimeter,
                default_timeout=None,
                client_info=client_info,
            ),
            self.replace_service_perimeters: self._wrap_method(
                self.replace_service_perimeters,
                default_timeout=None,
                client_info=client_info,
            ),
            self.commit_service_perimeters: self._wrap_method(
                self.commit_service_perimeters,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_gcp_user_access_bindings: self._wrap_method(
                self.list_gcp_user_access_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_gcp_user_access_binding: self._wrap_method(
                self.get_gcp_user_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_gcp_user_access_binding: self._wrap_method(
                self.create_gcp_user_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_gcp_user_access_binding: self._wrap_method(
                self.update_gcp_user_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_gcp_user_access_binding: self._wrap_method(
                self.delete_gcp_user_access_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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


__all__ = ("AccessContextManagerGrpcAsyncIOTransport",)
