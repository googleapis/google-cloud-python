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

from google.cloud.dataplex_v1.types import data_taxonomy
from google.cloud.dataplex_v1.types import data_taxonomy as gcd_data_taxonomy

from .base import DEFAULT_CLIENT_INFO, DataTaxonomyServiceTransport

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
                    "serviceName": "google.cloud.dataplex.v1.DataTaxonomyService",
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
                    "serviceName": "google.cloud.dataplex.v1.DataTaxonomyService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class DataTaxonomyServiceGrpcTransport(DataTaxonomyServiceTransport):
    """gRPC backend transport for DataTaxonomyService.

    DataTaxonomyService enables attribute-based governance. The
    resources currently offered include DataTaxonomy and
    DataAttribute.

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
        host: str = "dataplex.googleapis.com",
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
                 The hostname to connect to (default: 'dataplex.googleapis.com').
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
        host: str = "dataplex.googleapis.com",
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
    def create_data_taxonomy(
        self,
    ) -> Callable[
        [gcd_data_taxonomy.CreateDataTaxonomyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create data taxonomy method over gRPC.

        Create a DataTaxonomy resource.

        Returns:
            Callable[[~.CreateDataTaxonomyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_taxonomy" not in self._stubs:
            self._stubs["create_data_taxonomy"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/CreateDataTaxonomy",
                request_serializer=gcd_data_taxonomy.CreateDataTaxonomyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_data_taxonomy"]

    @property
    def update_data_taxonomy(
        self,
    ) -> Callable[
        [gcd_data_taxonomy.UpdateDataTaxonomyRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update data taxonomy method over gRPC.

        Updates a DataTaxonomy resource.

        Returns:
            Callable[[~.UpdateDataTaxonomyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_taxonomy" not in self._stubs:
            self._stubs["update_data_taxonomy"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/UpdateDataTaxonomy",
                request_serializer=gcd_data_taxonomy.UpdateDataTaxonomyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_data_taxonomy"]

    @property
    def delete_data_taxonomy(
        self,
    ) -> Callable[[data_taxonomy.DeleteDataTaxonomyRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete data taxonomy method over gRPC.

        Deletes a DataTaxonomy resource. All attributes
        within the DataTaxonomy must be deleted before the
        DataTaxonomy can be deleted.

        Returns:
            Callable[[~.DeleteDataTaxonomyRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_taxonomy" not in self._stubs:
            self._stubs["delete_data_taxonomy"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/DeleteDataTaxonomy",
                request_serializer=data_taxonomy.DeleteDataTaxonomyRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_data_taxonomy"]

    @property
    def list_data_taxonomies(
        self,
    ) -> Callable[
        [data_taxonomy.ListDataTaxonomiesRequest],
        data_taxonomy.ListDataTaxonomiesResponse,
    ]:
        r"""Return a callable for the list data taxonomies method over gRPC.

        Lists DataTaxonomy resources in a project and
        location.

        Returns:
            Callable[[~.ListDataTaxonomiesRequest],
                    ~.ListDataTaxonomiesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_taxonomies" not in self._stubs:
            self._stubs["list_data_taxonomies"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/ListDataTaxonomies",
                request_serializer=data_taxonomy.ListDataTaxonomiesRequest.serialize,
                response_deserializer=data_taxonomy.ListDataTaxonomiesResponse.deserialize,
            )
        return self._stubs["list_data_taxonomies"]

    @property
    def get_data_taxonomy(
        self,
    ) -> Callable[[data_taxonomy.GetDataTaxonomyRequest], data_taxonomy.DataTaxonomy]:
        r"""Return a callable for the get data taxonomy method over gRPC.

        Retrieves a DataTaxonomy resource.

        Returns:
            Callable[[~.GetDataTaxonomyRequest],
                    ~.DataTaxonomy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_taxonomy" not in self._stubs:
            self._stubs["get_data_taxonomy"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/GetDataTaxonomy",
                request_serializer=data_taxonomy.GetDataTaxonomyRequest.serialize,
                response_deserializer=data_taxonomy.DataTaxonomy.deserialize,
            )
        return self._stubs["get_data_taxonomy"]

    @property
    def create_data_attribute_binding(
        self,
    ) -> Callable[
        [data_taxonomy.CreateDataAttributeBindingRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the create data attribute binding method over gRPC.

        Create a DataAttributeBinding resource.

        Returns:
            Callable[[~.CreateDataAttributeBindingRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_attribute_binding" not in self._stubs:
            self._stubs[
                "create_data_attribute_binding"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/CreateDataAttributeBinding",
                request_serializer=data_taxonomy.CreateDataAttributeBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_data_attribute_binding"]

    @property
    def update_data_attribute_binding(
        self,
    ) -> Callable[
        [data_taxonomy.UpdateDataAttributeBindingRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the update data attribute binding method over gRPC.

        Updates a DataAttributeBinding resource.

        Returns:
            Callable[[~.UpdateDataAttributeBindingRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_attribute_binding" not in self._stubs:
            self._stubs[
                "update_data_attribute_binding"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/UpdateDataAttributeBinding",
                request_serializer=data_taxonomy.UpdateDataAttributeBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_data_attribute_binding"]

    @property
    def delete_data_attribute_binding(
        self,
    ) -> Callable[
        [data_taxonomy.DeleteDataAttributeBindingRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the delete data attribute binding method over gRPC.

        Deletes a DataAttributeBinding resource. All
        attributes within the DataAttributeBinding must be
        deleted before the DataAttributeBinding can be deleted.

        Returns:
            Callable[[~.DeleteDataAttributeBindingRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_attribute_binding" not in self._stubs:
            self._stubs[
                "delete_data_attribute_binding"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/DeleteDataAttributeBinding",
                request_serializer=data_taxonomy.DeleteDataAttributeBindingRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_data_attribute_binding"]

    @property
    def list_data_attribute_bindings(
        self,
    ) -> Callable[
        [data_taxonomy.ListDataAttributeBindingsRequest],
        data_taxonomy.ListDataAttributeBindingsResponse,
    ]:
        r"""Return a callable for the list data attribute bindings method over gRPC.

        Lists DataAttributeBinding resources in a project and
        location.

        Returns:
            Callable[[~.ListDataAttributeBindingsRequest],
                    ~.ListDataAttributeBindingsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_attribute_bindings" not in self._stubs:
            self._stubs[
                "list_data_attribute_bindings"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/ListDataAttributeBindings",
                request_serializer=data_taxonomy.ListDataAttributeBindingsRequest.serialize,
                response_deserializer=data_taxonomy.ListDataAttributeBindingsResponse.deserialize,
            )
        return self._stubs["list_data_attribute_bindings"]

    @property
    def get_data_attribute_binding(
        self,
    ) -> Callable[
        [data_taxonomy.GetDataAttributeBindingRequest],
        data_taxonomy.DataAttributeBinding,
    ]:
        r"""Return a callable for the get data attribute binding method over gRPC.

        Retrieves a DataAttributeBinding resource.

        Returns:
            Callable[[~.GetDataAttributeBindingRequest],
                    ~.DataAttributeBinding]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_attribute_binding" not in self._stubs:
            self._stubs[
                "get_data_attribute_binding"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/GetDataAttributeBinding",
                request_serializer=data_taxonomy.GetDataAttributeBindingRequest.serialize,
                response_deserializer=data_taxonomy.DataAttributeBinding.deserialize,
            )
        return self._stubs["get_data_attribute_binding"]

    @property
    def create_data_attribute(
        self,
    ) -> Callable[[data_taxonomy.CreateDataAttributeRequest], operations_pb2.Operation]:
        r"""Return a callable for the create data attribute method over gRPC.

        Create a DataAttribute resource.

        Returns:
            Callable[[~.CreateDataAttributeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_attribute" not in self._stubs:
            self._stubs["create_data_attribute"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/CreateDataAttribute",
                request_serializer=data_taxonomy.CreateDataAttributeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_data_attribute"]

    @property
    def update_data_attribute(
        self,
    ) -> Callable[[data_taxonomy.UpdateDataAttributeRequest], operations_pb2.Operation]:
        r"""Return a callable for the update data attribute method over gRPC.

        Updates a DataAttribute resource.

        Returns:
            Callable[[~.UpdateDataAttributeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_attribute" not in self._stubs:
            self._stubs["update_data_attribute"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/UpdateDataAttribute",
                request_serializer=data_taxonomy.UpdateDataAttributeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_data_attribute"]

    @property
    def delete_data_attribute(
        self,
    ) -> Callable[[data_taxonomy.DeleteDataAttributeRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete data attribute method over gRPC.

        Deletes a Data Attribute resource.

        Returns:
            Callable[[~.DeleteDataAttributeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_attribute" not in self._stubs:
            self._stubs["delete_data_attribute"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/DeleteDataAttribute",
                request_serializer=data_taxonomy.DeleteDataAttributeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_data_attribute"]

    @property
    def list_data_attributes(
        self,
    ) -> Callable[
        [data_taxonomy.ListDataAttributesRequest],
        data_taxonomy.ListDataAttributesResponse,
    ]:
        r"""Return a callable for the list data attributes method over gRPC.

        Lists Data Attribute resources in a DataTaxonomy.

        Returns:
            Callable[[~.ListDataAttributesRequest],
                    ~.ListDataAttributesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_attributes" not in self._stubs:
            self._stubs["list_data_attributes"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/ListDataAttributes",
                request_serializer=data_taxonomy.ListDataAttributesRequest.serialize,
                response_deserializer=data_taxonomy.ListDataAttributesResponse.deserialize,
            )
        return self._stubs["list_data_attributes"]

    @property
    def get_data_attribute(
        self,
    ) -> Callable[[data_taxonomy.GetDataAttributeRequest], data_taxonomy.DataAttribute]:
        r"""Return a callable for the get data attribute method over gRPC.

        Retrieves a Data Attribute resource.

        Returns:
            Callable[[~.GetDataAttributeRequest],
                    ~.DataAttribute]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_attribute" not in self._stubs:
            self._stubs["get_data_attribute"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataTaxonomyService/GetDataAttribute",
                request_serializer=data_taxonomy.GetDataAttributeRequest.serialize,
                response_deserializer=data_taxonomy.DataAttribute.deserialize,
            )
        return self._stubs["get_data_attribute"]

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
    def kind(self) -> str:
        return "grpc"


__all__ = ("DataTaxonomyServiceGrpcTransport",)
