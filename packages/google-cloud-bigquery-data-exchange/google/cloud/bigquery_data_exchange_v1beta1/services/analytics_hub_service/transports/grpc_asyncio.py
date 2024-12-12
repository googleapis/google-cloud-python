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
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.bigquery_data_exchange_v1beta1.types import dataexchange

from .base import DEFAULT_CLIENT_INFO, AnalyticsHubServiceTransport
from .grpc import AnalyticsHubServiceGrpcTransport

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
                    "serviceName": "google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService",
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
                    "serviceName": "google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class AnalyticsHubServiceGrpcAsyncIOTransport(AnalyticsHubServiceTransport):
    """gRPC AsyncIO backend transport for AnalyticsHubService.

    The ``AnalyticsHubService`` API facilitates data sharing within and
    across organizations. It allows data providers to publish listings
    that reference shared datasets. With Analytics Hub, users can
    discover and search for listings that they have access to.
    Subscribers can view and subscribe to listings. When you subscribe
    to a listing, Analytics Hub creates a linked dataset in your
    project.

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
        host: str = "analyticshub.googleapis.com",
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
        host: str = "analyticshub.googleapis.com",
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
                 The hostname to connect to (default: 'analyticshub.googleapis.com').
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
    def list_data_exchanges(
        self,
    ) -> Callable[
        [dataexchange.ListDataExchangesRequest],
        Awaitable[dataexchange.ListDataExchangesResponse],
    ]:
        r"""Return a callable for the list data exchanges method over gRPC.

        Lists all data exchanges in a given project and
        location.

        Returns:
            Callable[[~.ListDataExchangesRequest],
                    Awaitable[~.ListDataExchangesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_exchanges" not in self._stubs:
            self._stubs["list_data_exchanges"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/ListDataExchanges",
                request_serializer=dataexchange.ListDataExchangesRequest.serialize,
                response_deserializer=dataexchange.ListDataExchangesResponse.deserialize,
            )
        return self._stubs["list_data_exchanges"]

    @property
    def list_org_data_exchanges(
        self,
    ) -> Callable[
        [dataexchange.ListOrgDataExchangesRequest],
        Awaitable[dataexchange.ListOrgDataExchangesResponse],
    ]:
        r"""Return a callable for the list org data exchanges method over gRPC.

        Lists all data exchanges from projects in a given
        organization and location.

        Returns:
            Callable[[~.ListOrgDataExchangesRequest],
                    Awaitable[~.ListOrgDataExchangesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_org_data_exchanges" not in self._stubs:
            self._stubs["list_org_data_exchanges"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/ListOrgDataExchanges",
                request_serializer=dataexchange.ListOrgDataExchangesRequest.serialize,
                response_deserializer=dataexchange.ListOrgDataExchangesResponse.deserialize,
            )
        return self._stubs["list_org_data_exchanges"]

    @property
    def get_data_exchange(
        self,
    ) -> Callable[
        [dataexchange.GetDataExchangeRequest], Awaitable[dataexchange.DataExchange]
    ]:
        r"""Return a callable for the get data exchange method over gRPC.

        Gets the details of a data exchange.

        Returns:
            Callable[[~.GetDataExchangeRequest],
                    Awaitable[~.DataExchange]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_data_exchange" not in self._stubs:
            self._stubs["get_data_exchange"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/GetDataExchange",
                request_serializer=dataexchange.GetDataExchangeRequest.serialize,
                response_deserializer=dataexchange.DataExchange.deserialize,
            )
        return self._stubs["get_data_exchange"]

    @property
    def create_data_exchange(
        self,
    ) -> Callable[
        [dataexchange.CreateDataExchangeRequest], Awaitable[dataexchange.DataExchange]
    ]:
        r"""Return a callable for the create data exchange method over gRPC.

        Creates a new data exchange.

        Returns:
            Callable[[~.CreateDataExchangeRequest],
                    Awaitable[~.DataExchange]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_data_exchange" not in self._stubs:
            self._stubs["create_data_exchange"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/CreateDataExchange",
                request_serializer=dataexchange.CreateDataExchangeRequest.serialize,
                response_deserializer=dataexchange.DataExchange.deserialize,
            )
        return self._stubs["create_data_exchange"]

    @property
    def update_data_exchange(
        self,
    ) -> Callable[
        [dataexchange.UpdateDataExchangeRequest], Awaitable[dataexchange.DataExchange]
    ]:
        r"""Return a callable for the update data exchange method over gRPC.

        Updates an existing data exchange.

        Returns:
            Callable[[~.UpdateDataExchangeRequest],
                    Awaitable[~.DataExchange]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_data_exchange" not in self._stubs:
            self._stubs["update_data_exchange"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/UpdateDataExchange",
                request_serializer=dataexchange.UpdateDataExchangeRequest.serialize,
                response_deserializer=dataexchange.DataExchange.deserialize,
            )
        return self._stubs["update_data_exchange"]

    @property
    def delete_data_exchange(
        self,
    ) -> Callable[[dataexchange.DeleteDataExchangeRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete data exchange method over gRPC.

        Deletes an existing data exchange.

        Returns:
            Callable[[~.DeleteDataExchangeRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_data_exchange" not in self._stubs:
            self._stubs["delete_data_exchange"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/DeleteDataExchange",
                request_serializer=dataexchange.DeleteDataExchangeRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_data_exchange"]

    @property
    def list_listings(
        self,
    ) -> Callable[
        [dataexchange.ListListingsRequest], Awaitable[dataexchange.ListListingsResponse]
    ]:
        r"""Return a callable for the list listings method over gRPC.

        Lists all listings in a given project and location.

        Returns:
            Callable[[~.ListListingsRequest],
                    Awaitable[~.ListListingsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_listings" not in self._stubs:
            self._stubs["list_listings"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/ListListings",
                request_serializer=dataexchange.ListListingsRequest.serialize,
                response_deserializer=dataexchange.ListListingsResponse.deserialize,
            )
        return self._stubs["list_listings"]

    @property
    def get_listing(
        self,
    ) -> Callable[[dataexchange.GetListingRequest], Awaitable[dataexchange.Listing]]:
        r"""Return a callable for the get listing method over gRPC.

        Gets the details of a listing.

        Returns:
            Callable[[~.GetListingRequest],
                    Awaitable[~.Listing]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_listing" not in self._stubs:
            self._stubs["get_listing"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/GetListing",
                request_serializer=dataexchange.GetListingRequest.serialize,
                response_deserializer=dataexchange.Listing.deserialize,
            )
        return self._stubs["get_listing"]

    @property
    def create_listing(
        self,
    ) -> Callable[[dataexchange.CreateListingRequest], Awaitable[dataexchange.Listing]]:
        r"""Return a callable for the create listing method over gRPC.

        Creates a new listing.

        Returns:
            Callable[[~.CreateListingRequest],
                    Awaitable[~.Listing]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_listing" not in self._stubs:
            self._stubs["create_listing"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/CreateListing",
                request_serializer=dataexchange.CreateListingRequest.serialize,
                response_deserializer=dataexchange.Listing.deserialize,
            )
        return self._stubs["create_listing"]

    @property
    def update_listing(
        self,
    ) -> Callable[[dataexchange.UpdateListingRequest], Awaitable[dataexchange.Listing]]:
        r"""Return a callable for the update listing method over gRPC.

        Updates an existing listing.

        Returns:
            Callable[[~.UpdateListingRequest],
                    Awaitable[~.Listing]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_listing" not in self._stubs:
            self._stubs["update_listing"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/UpdateListing",
                request_serializer=dataexchange.UpdateListingRequest.serialize,
                response_deserializer=dataexchange.Listing.deserialize,
            )
        return self._stubs["update_listing"]

    @property
    def delete_listing(
        self,
    ) -> Callable[[dataexchange.DeleteListingRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete listing method over gRPC.

        Deletes a listing.

        Returns:
            Callable[[~.DeleteListingRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_listing" not in self._stubs:
            self._stubs["delete_listing"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/DeleteListing",
                request_serializer=dataexchange.DeleteListingRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_listing"]

    @property
    def subscribe_listing(
        self,
    ) -> Callable[
        [dataexchange.SubscribeListingRequest],
        Awaitable[dataexchange.SubscribeListingResponse],
    ]:
        r"""Return a callable for the subscribe listing method over gRPC.

        Subscribes to a listing.

        Currently, with Analytics Hub, you can create listings
        that reference only BigQuery datasets.
        Upon subscription to a listing for a BigQuery dataset,
        Analytics Hub creates a linked dataset in the
        subscriber's project.

        Returns:
            Callable[[~.SubscribeListingRequest],
                    Awaitable[~.SubscribeListingResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "subscribe_listing" not in self._stubs:
            self._stubs["subscribe_listing"] = self._logged_channel.unary_unary(
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/SubscribeListing",
                request_serializer=dataexchange.SubscribeListingRequest.serialize,
                response_deserializer=dataexchange.SubscribeListingResponse.deserialize,
            )
        return self._stubs["subscribe_listing"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM policy.

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
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the IAM policy.

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
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/SetIamPolicy",
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

        Returns the permissions that a caller has.

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
                "/google.cloud.bigquery.dataexchange.v1beta1.AnalyticsHubService/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_data_exchanges: self._wrap_method(
                self.list_data_exchanges,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_org_data_exchanges: self._wrap_method(
                self.list_org_data_exchanges,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_exchange: self._wrap_method(
                self.get_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_data_exchange: self._wrap_method(
                self.create_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_data_exchange: self._wrap_method(
                self.update_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_data_exchange: self._wrap_method(
                self.delete_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_listings: self._wrap_method(
                self.list_listings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_listing: self._wrap_method(
                self.get_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_listing: self._wrap_method(
                self.create_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_listing: self._wrap_method(
                self.update_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_listing: self._wrap_method(
                self.delete_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.subscribe_listing: self._wrap_method(
                self.subscribe_listing,
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


__all__ = ("AnalyticsHubServiceGrpcAsyncIOTransport",)
