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

from google.api import httpbody_pb2  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.apigee_registry_v1.types import registry_models, registry_service

from .base import DEFAULT_CLIENT_INFO, RegistryTransport
from .grpc import RegistryGrpcTransport

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
                    "serviceName": "google.cloud.apigeeregistry.v1.Registry",
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
                    "serviceName": "google.cloud.apigeeregistry.v1.Registry",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class RegistryGrpcAsyncIOTransport(RegistryTransport):
    """gRPC AsyncIO backend transport for Registry.

    The Registry service allows teams to manage descriptions of
    APIs.

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
        host: str = "apigeeregistry.googleapis.com",
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
        host: str = "apigeeregistry.googleapis.com",
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
                 The hostname to connect to (default: 'apigeeregistry.googleapis.com').
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
    def list_apis(
        self,
    ) -> Callable[
        [registry_service.ListApisRequest], Awaitable[registry_service.ListApisResponse]
    ]:
        r"""Return a callable for the list apis method over gRPC.

        Returns matching APIs.

        Returns:
            Callable[[~.ListApisRequest],
                    Awaitable[~.ListApisResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_apis" not in self._stubs:
            self._stubs["list_apis"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApis",
                request_serializer=registry_service.ListApisRequest.serialize,
                response_deserializer=registry_service.ListApisResponse.deserialize,
            )
        return self._stubs["list_apis"]

    @property
    def get_api(
        self,
    ) -> Callable[[registry_service.GetApiRequest], Awaitable[registry_models.Api]]:
        r"""Return a callable for the get api method over gRPC.

        Returns a specified API.

        Returns:
            Callable[[~.GetApiRequest],
                    Awaitable[~.Api]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api" not in self._stubs:
            self._stubs["get_api"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetApi",
                request_serializer=registry_service.GetApiRequest.serialize,
                response_deserializer=registry_models.Api.deserialize,
            )
        return self._stubs["get_api"]

    @property
    def create_api(
        self,
    ) -> Callable[[registry_service.CreateApiRequest], Awaitable[registry_models.Api]]:
        r"""Return a callable for the create api method over gRPC.

        Creates a specified API.

        Returns:
            Callable[[~.CreateApiRequest],
                    Awaitable[~.Api]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api" not in self._stubs:
            self._stubs["create_api"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/CreateApi",
                request_serializer=registry_service.CreateApiRequest.serialize,
                response_deserializer=registry_models.Api.deserialize,
            )
        return self._stubs["create_api"]

    @property
    def update_api(
        self,
    ) -> Callable[[registry_service.UpdateApiRequest], Awaitable[registry_models.Api]]:
        r"""Return a callable for the update api method over gRPC.

        Used to modify a specified API.

        Returns:
            Callable[[~.UpdateApiRequest],
                    Awaitable[~.Api]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api" not in self._stubs:
            self._stubs["update_api"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/UpdateApi",
                request_serializer=registry_service.UpdateApiRequest.serialize,
                response_deserializer=registry_models.Api.deserialize,
            )
        return self._stubs["update_api"]

    @property
    def delete_api(
        self,
    ) -> Callable[[registry_service.DeleteApiRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete api method over gRPC.

        Removes a specified API and all of the resources that
        it owns.

        Returns:
            Callable[[~.DeleteApiRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api" not in self._stubs:
            self._stubs["delete_api"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApi",
                request_serializer=registry_service.DeleteApiRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_api"]

    @property
    def list_api_versions(
        self,
    ) -> Callable[
        [registry_service.ListApiVersionsRequest],
        Awaitable[registry_service.ListApiVersionsResponse],
    ]:
        r"""Return a callable for the list api versions method over gRPC.

        Returns matching versions.

        Returns:
            Callable[[~.ListApiVersionsRequest],
                    Awaitable[~.ListApiVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_versions" not in self._stubs:
            self._stubs["list_api_versions"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApiVersions",
                request_serializer=registry_service.ListApiVersionsRequest.serialize,
                response_deserializer=registry_service.ListApiVersionsResponse.deserialize,
            )
        return self._stubs["list_api_versions"]

    @property
    def get_api_version(
        self,
    ) -> Callable[
        [registry_service.GetApiVersionRequest], Awaitable[registry_models.ApiVersion]
    ]:
        r"""Return a callable for the get api version method over gRPC.

        Returns a specified version.

        Returns:
            Callable[[~.GetApiVersionRequest],
                    Awaitable[~.ApiVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api_version" not in self._stubs:
            self._stubs["get_api_version"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetApiVersion",
                request_serializer=registry_service.GetApiVersionRequest.serialize,
                response_deserializer=registry_models.ApiVersion.deserialize,
            )
        return self._stubs["get_api_version"]

    @property
    def create_api_version(
        self,
    ) -> Callable[
        [registry_service.CreateApiVersionRequest],
        Awaitable[registry_models.ApiVersion],
    ]:
        r"""Return a callable for the create api version method over gRPC.

        Creates a specified version.

        Returns:
            Callable[[~.CreateApiVersionRequest],
                    Awaitable[~.ApiVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api_version" not in self._stubs:
            self._stubs["create_api_version"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/CreateApiVersion",
                request_serializer=registry_service.CreateApiVersionRequest.serialize,
                response_deserializer=registry_models.ApiVersion.deserialize,
            )
        return self._stubs["create_api_version"]

    @property
    def update_api_version(
        self,
    ) -> Callable[
        [registry_service.UpdateApiVersionRequest],
        Awaitable[registry_models.ApiVersion],
    ]:
        r"""Return a callable for the update api version method over gRPC.

        Used to modify a specified version.

        Returns:
            Callable[[~.UpdateApiVersionRequest],
                    Awaitable[~.ApiVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api_version" not in self._stubs:
            self._stubs["update_api_version"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/UpdateApiVersion",
                request_serializer=registry_service.UpdateApiVersionRequest.serialize,
                response_deserializer=registry_models.ApiVersion.deserialize,
            )
        return self._stubs["update_api_version"]

    @property
    def delete_api_version(
        self,
    ) -> Callable[
        [registry_service.DeleteApiVersionRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete api version method over gRPC.

        Removes a specified version and all of the resources
        that it owns.

        Returns:
            Callable[[~.DeleteApiVersionRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_version" not in self._stubs:
            self._stubs["delete_api_version"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApiVersion",
                request_serializer=registry_service.DeleteApiVersionRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_api_version"]

    @property
    def list_api_specs(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecsRequest],
        Awaitable[registry_service.ListApiSpecsResponse],
    ]:
        r"""Return a callable for the list api specs method over gRPC.

        Returns matching specs.

        Returns:
            Callable[[~.ListApiSpecsRequest],
                    Awaitable[~.ListApiSpecsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_specs" not in self._stubs:
            self._stubs["list_api_specs"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApiSpecs",
                request_serializer=registry_service.ListApiSpecsRequest.serialize,
                response_deserializer=registry_service.ListApiSpecsResponse.deserialize,
            )
        return self._stubs["list_api_specs"]

    @property
    def get_api_spec(
        self,
    ) -> Callable[
        [registry_service.GetApiSpecRequest], Awaitable[registry_models.ApiSpec]
    ]:
        r"""Return a callable for the get api spec method over gRPC.

        Returns a specified spec.

        Returns:
            Callable[[~.GetApiSpecRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api_spec" not in self._stubs:
            self._stubs["get_api_spec"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetApiSpec",
                request_serializer=registry_service.GetApiSpecRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["get_api_spec"]

    @property
    def get_api_spec_contents(
        self,
    ) -> Callable[
        [registry_service.GetApiSpecContentsRequest], Awaitable[httpbody_pb2.HttpBody]
    ]:
        r"""Return a callable for the get api spec contents method over gRPC.

        Returns the contents of a specified spec. If specs are stored
        with GZip compression, the default behavior is to return the
        spec uncompressed (the mime_type response field indicates the
        exact format returned).

        Returns:
            Callable[[~.GetApiSpecContentsRequest],
                    Awaitable[~.HttpBody]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api_spec_contents" not in self._stubs:
            self._stubs["get_api_spec_contents"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetApiSpecContents",
                request_serializer=registry_service.GetApiSpecContentsRequest.serialize,
                response_deserializer=httpbody_pb2.HttpBody.FromString,
            )
        return self._stubs["get_api_spec_contents"]

    @property
    def create_api_spec(
        self,
    ) -> Callable[
        [registry_service.CreateApiSpecRequest], Awaitable[registry_models.ApiSpec]
    ]:
        r"""Return a callable for the create api spec method over gRPC.

        Creates a specified spec.

        Returns:
            Callable[[~.CreateApiSpecRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api_spec" not in self._stubs:
            self._stubs["create_api_spec"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/CreateApiSpec",
                request_serializer=registry_service.CreateApiSpecRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["create_api_spec"]

    @property
    def update_api_spec(
        self,
    ) -> Callable[
        [registry_service.UpdateApiSpecRequest], Awaitable[registry_models.ApiSpec]
    ]:
        r"""Return a callable for the update api spec method over gRPC.

        Used to modify a specified spec.

        Returns:
            Callable[[~.UpdateApiSpecRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api_spec" not in self._stubs:
            self._stubs["update_api_spec"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/UpdateApiSpec",
                request_serializer=registry_service.UpdateApiSpecRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["update_api_spec"]

    @property
    def delete_api_spec(
        self,
    ) -> Callable[[registry_service.DeleteApiSpecRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete api spec method over gRPC.

        Removes a specified spec, all revisions, and all
        child resources (e.g., artifacts).

        Returns:
            Callable[[~.DeleteApiSpecRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_spec" not in self._stubs:
            self._stubs["delete_api_spec"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApiSpec",
                request_serializer=registry_service.DeleteApiSpecRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_api_spec"]

    @property
    def tag_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiSpecRevisionRequest], Awaitable[registry_models.ApiSpec]
    ]:
        r"""Return a callable for the tag api spec revision method over gRPC.

        Adds a tag to a specified revision of a spec.

        Returns:
            Callable[[~.TagApiSpecRevisionRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "tag_api_spec_revision" not in self._stubs:
            self._stubs["tag_api_spec_revision"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/TagApiSpecRevision",
                request_serializer=registry_service.TagApiSpecRevisionRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["tag_api_spec_revision"]

    @property
    def list_api_spec_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecRevisionsRequest],
        Awaitable[registry_service.ListApiSpecRevisionsResponse],
    ]:
        r"""Return a callable for the list api spec revisions method over gRPC.

        Lists all revisions of a spec.
        Revisions are returned in descending order of revision
        creation time.

        Returns:
            Callable[[~.ListApiSpecRevisionsRequest],
                    Awaitable[~.ListApiSpecRevisionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_spec_revisions" not in self._stubs:
            self._stubs["list_api_spec_revisions"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApiSpecRevisions",
                request_serializer=registry_service.ListApiSpecRevisionsRequest.serialize,
                response_deserializer=registry_service.ListApiSpecRevisionsResponse.deserialize,
            )
        return self._stubs["list_api_spec_revisions"]

    @property
    def rollback_api_spec(
        self,
    ) -> Callable[
        [registry_service.RollbackApiSpecRequest], Awaitable[registry_models.ApiSpec]
    ]:
        r"""Return a callable for the rollback api spec method over gRPC.

        Sets the current revision to a specified prior
        revision. Note that this creates a new revision with a
        new revision ID.

        Returns:
            Callable[[~.RollbackApiSpecRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rollback_api_spec" not in self._stubs:
            self._stubs["rollback_api_spec"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/RollbackApiSpec",
                request_serializer=registry_service.RollbackApiSpecRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["rollback_api_spec"]

    @property
    def delete_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiSpecRevisionRequest],
        Awaitable[registry_models.ApiSpec],
    ]:
        r"""Return a callable for the delete api spec revision method over gRPC.

        Deletes a revision of a spec.

        Returns:
            Callable[[~.DeleteApiSpecRevisionRequest],
                    Awaitable[~.ApiSpec]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_spec_revision" not in self._stubs:
            self._stubs["delete_api_spec_revision"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApiSpecRevision",
                request_serializer=registry_service.DeleteApiSpecRevisionRequest.serialize,
                response_deserializer=registry_models.ApiSpec.deserialize,
            )
        return self._stubs["delete_api_spec_revision"]

    @property
    def list_api_deployments(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentsRequest],
        Awaitable[registry_service.ListApiDeploymentsResponse],
    ]:
        r"""Return a callable for the list api deployments method over gRPC.

        Returns matching deployments.

        Returns:
            Callable[[~.ListApiDeploymentsRequest],
                    Awaitable[~.ListApiDeploymentsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_deployments" not in self._stubs:
            self._stubs["list_api_deployments"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApiDeployments",
                request_serializer=registry_service.ListApiDeploymentsRequest.serialize,
                response_deserializer=registry_service.ListApiDeploymentsResponse.deserialize,
            )
        return self._stubs["list_api_deployments"]

    @property
    def get_api_deployment(
        self,
    ) -> Callable[
        [registry_service.GetApiDeploymentRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the get api deployment method over gRPC.

        Returns a specified deployment.

        Returns:
            Callable[[~.GetApiDeploymentRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_api_deployment" not in self._stubs:
            self._stubs["get_api_deployment"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetApiDeployment",
                request_serializer=registry_service.GetApiDeploymentRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["get_api_deployment"]

    @property
    def create_api_deployment(
        self,
    ) -> Callable[
        [registry_service.CreateApiDeploymentRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the create api deployment method over gRPC.

        Creates a specified deployment.

        Returns:
            Callable[[~.CreateApiDeploymentRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_api_deployment" not in self._stubs:
            self._stubs["create_api_deployment"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/CreateApiDeployment",
                request_serializer=registry_service.CreateApiDeploymentRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["create_api_deployment"]

    @property
    def update_api_deployment(
        self,
    ) -> Callable[
        [registry_service.UpdateApiDeploymentRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the update api deployment method over gRPC.

        Used to modify a specified deployment.

        Returns:
            Callable[[~.UpdateApiDeploymentRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_api_deployment" not in self._stubs:
            self._stubs["update_api_deployment"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/UpdateApiDeployment",
                request_serializer=registry_service.UpdateApiDeploymentRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["update_api_deployment"]

    @property
    def delete_api_deployment(
        self,
    ) -> Callable[
        [registry_service.DeleteApiDeploymentRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete api deployment method over gRPC.

        Removes a specified deployment, all revisions, and
        all child resources (e.g., artifacts).

        Returns:
            Callable[[~.DeleteApiDeploymentRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_deployment" not in self._stubs:
            self._stubs["delete_api_deployment"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApiDeployment",
                request_serializer=registry_service.DeleteApiDeploymentRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_api_deployment"]

    @property
    def tag_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiDeploymentRevisionRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the tag api deployment revision method over gRPC.

        Adds a tag to a specified revision of a
        deployment.

        Returns:
            Callable[[~.TagApiDeploymentRevisionRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "tag_api_deployment_revision" not in self._stubs:
            self._stubs[
                "tag_api_deployment_revision"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/TagApiDeploymentRevision",
                request_serializer=registry_service.TagApiDeploymentRevisionRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["tag_api_deployment_revision"]

    @property
    def list_api_deployment_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentRevisionsRequest],
        Awaitable[registry_service.ListApiDeploymentRevisionsResponse],
    ]:
        r"""Return a callable for the list api deployment revisions method over gRPC.

        Lists all revisions of a deployment.
        Revisions are returned in descending order of revision
        creation time.

        Returns:
            Callable[[~.ListApiDeploymentRevisionsRequest],
                    Awaitable[~.ListApiDeploymentRevisionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_api_deployment_revisions" not in self._stubs:
            self._stubs[
                "list_api_deployment_revisions"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListApiDeploymentRevisions",
                request_serializer=registry_service.ListApiDeploymentRevisionsRequest.serialize,
                response_deserializer=registry_service.ListApiDeploymentRevisionsResponse.deserialize,
            )
        return self._stubs["list_api_deployment_revisions"]

    @property
    def rollback_api_deployment(
        self,
    ) -> Callable[
        [registry_service.RollbackApiDeploymentRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the rollback api deployment method over gRPC.

        Sets the current revision to a specified prior
        revision. Note that this creates a new revision with a
        new revision ID.

        Returns:
            Callable[[~.RollbackApiDeploymentRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rollback_api_deployment" not in self._stubs:
            self._stubs["rollback_api_deployment"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/RollbackApiDeployment",
                request_serializer=registry_service.RollbackApiDeploymentRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["rollback_api_deployment"]

    @property
    def delete_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiDeploymentRevisionRequest],
        Awaitable[registry_models.ApiDeployment],
    ]:
        r"""Return a callable for the delete api deployment revision method over gRPC.

        Deletes a revision of a deployment.

        Returns:
            Callable[[~.DeleteApiDeploymentRevisionRequest],
                    Awaitable[~.ApiDeployment]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_api_deployment_revision" not in self._stubs:
            self._stubs[
                "delete_api_deployment_revision"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteApiDeploymentRevision",
                request_serializer=registry_service.DeleteApiDeploymentRevisionRequest.serialize,
                response_deserializer=registry_models.ApiDeployment.deserialize,
            )
        return self._stubs["delete_api_deployment_revision"]

    @property
    def list_artifacts(
        self,
    ) -> Callable[
        [registry_service.ListArtifactsRequest],
        Awaitable[registry_service.ListArtifactsResponse],
    ]:
        r"""Return a callable for the list artifacts method over gRPC.

        Returns matching artifacts.

        Returns:
            Callable[[~.ListArtifactsRequest],
                    Awaitable[~.ListArtifactsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_artifacts" not in self._stubs:
            self._stubs["list_artifacts"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ListArtifacts",
                request_serializer=registry_service.ListArtifactsRequest.serialize,
                response_deserializer=registry_service.ListArtifactsResponse.deserialize,
            )
        return self._stubs["list_artifacts"]

    @property
    def get_artifact(
        self,
    ) -> Callable[
        [registry_service.GetArtifactRequest], Awaitable[registry_models.Artifact]
    ]:
        r"""Return a callable for the get artifact method over gRPC.

        Returns a specified artifact.

        Returns:
            Callable[[~.GetArtifactRequest],
                    Awaitable[~.Artifact]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_artifact" not in self._stubs:
            self._stubs["get_artifact"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetArtifact",
                request_serializer=registry_service.GetArtifactRequest.serialize,
                response_deserializer=registry_models.Artifact.deserialize,
            )
        return self._stubs["get_artifact"]

    @property
    def get_artifact_contents(
        self,
    ) -> Callable[
        [registry_service.GetArtifactContentsRequest], Awaitable[httpbody_pb2.HttpBody]
    ]:
        r"""Return a callable for the get artifact contents method over gRPC.

        Returns the contents of a specified artifact. If artifacts are
        stored with GZip compression, the default behavior is to return
        the artifact uncompressed (the mime_type response field
        indicates the exact format returned).

        Returns:
            Callable[[~.GetArtifactContentsRequest],
                    Awaitable[~.HttpBody]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_artifact_contents" not in self._stubs:
            self._stubs["get_artifact_contents"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/GetArtifactContents",
                request_serializer=registry_service.GetArtifactContentsRequest.serialize,
                response_deserializer=httpbody_pb2.HttpBody.FromString,
            )
        return self._stubs["get_artifact_contents"]

    @property
    def create_artifact(
        self,
    ) -> Callable[
        [registry_service.CreateArtifactRequest], Awaitable[registry_models.Artifact]
    ]:
        r"""Return a callable for the create artifact method over gRPC.

        Creates a specified artifact.

        Returns:
            Callable[[~.CreateArtifactRequest],
                    Awaitable[~.Artifact]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_artifact" not in self._stubs:
            self._stubs["create_artifact"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/CreateArtifact",
                request_serializer=registry_service.CreateArtifactRequest.serialize,
                response_deserializer=registry_models.Artifact.deserialize,
            )
        return self._stubs["create_artifact"]

    @property
    def replace_artifact(
        self,
    ) -> Callable[
        [registry_service.ReplaceArtifactRequest], Awaitable[registry_models.Artifact]
    ]:
        r"""Return a callable for the replace artifact method over gRPC.

        Used to replace a specified artifact.

        Returns:
            Callable[[~.ReplaceArtifactRequest],
                    Awaitable[~.Artifact]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "replace_artifact" not in self._stubs:
            self._stubs["replace_artifact"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/ReplaceArtifact",
                request_serializer=registry_service.ReplaceArtifactRequest.serialize,
                response_deserializer=registry_models.Artifact.deserialize,
            )
        return self._stubs["replace_artifact"]

    @property
    def delete_artifact(
        self,
    ) -> Callable[[registry_service.DeleteArtifactRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete artifact method over gRPC.

        Removes a specified artifact.

        Returns:
            Callable[[~.DeleteArtifactRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_artifact" not in self._stubs:
            self._stubs["delete_artifact"] = self._logged_channel.unary_unary(
                "/google.cloud.apigeeregistry.v1.Registry/DeleteArtifact",
                request_serializer=registry_service.DeleteArtifactRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_artifact"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_apis: self._wrap_method(
                self.list_apis,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api: self._wrap_method(
                self.get_api,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api: self._wrap_method(
                self.create_api,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api: self._wrap_method(
                self.update_api,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api: self._wrap_method(
                self.delete_api,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_versions: self._wrap_method(
                self.list_api_versions,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_version: self._wrap_method(
                self.get_api_version,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_version: self._wrap_method(
                self.create_api_version,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_version: self._wrap_method(
                self.update_api_version,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_version: self._wrap_method(
                self.delete_api_version,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_specs: self._wrap_method(
                self.list_api_specs,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_spec: self._wrap_method(
                self.get_api_spec,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_spec_contents: self._wrap_method(
                self.get_api_spec_contents,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_spec: self._wrap_method(
                self.create_api_spec,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_spec: self._wrap_method(
                self.update_api_spec,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_spec: self._wrap_method(
                self.delete_api_spec,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.tag_api_spec_revision: self._wrap_method(
                self.tag_api_spec_revision,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_spec_revisions: self._wrap_method(
                self.list_api_spec_revisions,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.rollback_api_spec: self._wrap_method(
                self.rollback_api_spec,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_spec_revision: self._wrap_method(
                self.delete_api_spec_revision,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_deployments: self._wrap_method(
                self.list_api_deployments,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_deployment: self._wrap_method(
                self.get_api_deployment,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_deployment: self._wrap_method(
                self.create_api_deployment,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_deployment: self._wrap_method(
                self.update_api_deployment,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_deployment: self._wrap_method(
                self.delete_api_deployment,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.tag_api_deployment_revision: self._wrap_method(
                self.tag_api_deployment_revision,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_deployment_revisions: self._wrap_method(
                self.list_api_deployment_revisions,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.rollback_api_deployment: self._wrap_method(
                self.rollback_api_deployment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_deployment_revision: self._wrap_method(
                self.delete_api_deployment_revision,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_artifacts: self._wrap_method(
                self.list_artifacts,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_artifact: self._wrap_method(
                self.get_artifact,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_artifact_contents: self._wrap_method(
                self.get_artifact_contents,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_artifact: self._wrap_method(
                self.create_artifact,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.replace_artifact: self._wrap_method(
                self.replace_artifact,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_artifact: self._wrap_method(
                self.delete_artifact,
                default_retry=retries.AsyncRetry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
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
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
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


__all__ = ("RegistryGrpcAsyncIOTransport",)
