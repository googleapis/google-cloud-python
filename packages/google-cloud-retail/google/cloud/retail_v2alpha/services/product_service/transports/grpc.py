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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.retail_v2alpha.types import export_config, import_config
from google.cloud.retail_v2alpha.types import product
from google.cloud.retail_v2alpha.types import product as gcr_product
from google.cloud.retail_v2alpha.types import product_service, purge_config

from .base import DEFAULT_CLIENT_INFO, ProductServiceTransport


class ProductServiceGrpcTransport(ProductServiceTransport):
    """gRPC backend transport for ProductService.

    Service for ingesting [Product][google.cloud.retail.v2alpha.Product]
    information of the customer's website.

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
        host: str = "retail.googleapis.com",
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
                 The hostname to connect to (default: 'retail.googleapis.com').
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

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "retail.googleapis.com",
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
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def create_product(
        self,
    ) -> Callable[[product_service.CreateProductRequest], gcr_product.Product]:
        r"""Return a callable for the create product method over gRPC.

        Creates a [Product][google.cloud.retail.v2alpha.Product].

        Returns:
            Callable[[~.CreateProductRequest],
                    ~.Product]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_product" not in self._stubs:
            self._stubs["create_product"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/CreateProduct",
                request_serializer=product_service.CreateProductRequest.serialize,
                response_deserializer=gcr_product.Product.deserialize,
            )
        return self._stubs["create_product"]

    @property
    def get_product(
        self,
    ) -> Callable[[product_service.GetProductRequest], product.Product]:
        r"""Return a callable for the get product method over gRPC.

        Gets a [Product][google.cloud.retail.v2alpha.Product].

        Returns:
            Callable[[~.GetProductRequest],
                    ~.Product]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_product" not in self._stubs:
            self._stubs["get_product"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/GetProduct",
                request_serializer=product_service.GetProductRequest.serialize,
                response_deserializer=product.Product.deserialize,
            )
        return self._stubs["get_product"]

    @property
    def list_products(
        self,
    ) -> Callable[
        [product_service.ListProductsRequest], product_service.ListProductsResponse
    ]:
        r"""Return a callable for the list products method over gRPC.

        Gets a list of [Product][google.cloud.retail.v2alpha.Product]s.

        Returns:
            Callable[[~.ListProductsRequest],
                    ~.ListProductsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_products" not in self._stubs:
            self._stubs["list_products"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/ListProducts",
                request_serializer=product_service.ListProductsRequest.serialize,
                response_deserializer=product_service.ListProductsResponse.deserialize,
            )
        return self._stubs["list_products"]

    @property
    def update_product(
        self,
    ) -> Callable[[product_service.UpdateProductRequest], gcr_product.Product]:
        r"""Return a callable for the update product method over gRPC.

        Updates a [Product][google.cloud.retail.v2alpha.Product].

        Returns:
            Callable[[~.UpdateProductRequest],
                    ~.Product]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_product" not in self._stubs:
            self._stubs["update_product"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/UpdateProduct",
                request_serializer=product_service.UpdateProductRequest.serialize,
                response_deserializer=gcr_product.Product.deserialize,
            )
        return self._stubs["update_product"]

    @property
    def delete_product(
        self,
    ) -> Callable[[product_service.DeleteProductRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete product method over gRPC.

        Deletes a [Product][google.cloud.retail.v2alpha.Product].

        Returns:
            Callable[[~.DeleteProductRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_product" not in self._stubs:
            self._stubs["delete_product"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/DeleteProduct",
                request_serializer=product_service.DeleteProductRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_product"]

    @property
    def purge_products(
        self,
    ) -> Callable[[purge_config.PurgeProductsRequest], operations_pb2.Operation]:
        r"""Return a callable for the purge products method over gRPC.

        Permanently deletes all selected
        [Product][google.cloud.retail.v2alpha.Product]s under a branch.

        This process is asynchronous. If the request is valid, the
        removal will be enqueued and processed offline. Depending on the
        number of [Product][google.cloud.retail.v2alpha.Product]s, this
        operation could take hours to complete. Before the operation
        completes, some [Product][google.cloud.retail.v2alpha.Product]s
        may still be returned by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Depending on the number of
        [Product][google.cloud.retail.v2alpha.Product]s, this operation
        could take hours to complete. To get a sample of
        [Product][google.cloud.retail.v2alpha.Product]s that would be
        deleted, set
        [PurgeProductsRequest.force][google.cloud.retail.v2alpha.PurgeProductsRequest.force]
        to false.

        Returns:
            Callable[[~.PurgeProductsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "purge_products" not in self._stubs:
            self._stubs["purge_products"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/PurgeProducts",
                request_serializer=purge_config.PurgeProductsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["purge_products"]

    @property
    def import_products(
        self,
    ) -> Callable[[import_config.ImportProductsRequest], operations_pb2.Operation]:
        r"""Return a callable for the import products method over gRPC.

        Bulk import of multiple
        [Product][google.cloud.retail.v2alpha.Product]s.

        Request processing may be synchronous. Non-existing items are
        created.

        Note that it is possible for a subset of the
        [Product][google.cloud.retail.v2alpha.Product]s to be
        successfully updated.

        Returns:
            Callable[[~.ImportProductsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_products" not in self._stubs:
            self._stubs["import_products"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/ImportProducts",
                request_serializer=import_config.ImportProductsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_products"]

    @property
    def export_products(
        self,
    ) -> Callable[[export_config.ExportProductsRequest], operations_pb2.Operation]:
        r"""Return a callable for the export products method over gRPC.

        Exports multiple
        [Product][google.cloud.retail.v2alpha.Product]s.

        Returns:
            Callable[[~.ExportProductsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_products" not in self._stubs:
            self._stubs["export_products"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/ExportProducts",
                request_serializer=export_config.ExportProductsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_products"]

    @property
    def set_inventory(
        self,
    ) -> Callable[[product_service.SetInventoryRequest], operations_pb2.Operation]:
        r"""Return a callable for the set inventory method over gRPC.

        Updates inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] while respecting
        the last update timestamps of each inventory field.

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update is enqueued and processed downstream. As a consequence,
        when a response is returned, updates are not immediately
        manifested in the [Product][google.cloud.retail.v2alpha.Product]
        queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        When inventory is updated with
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct],
        the specified inventory field value(s) overwrite any existing
        value(s) while ignoring the last update time for this field.
        Furthermore, the last update times for the specified inventory
        fields are overwritten by the times of the
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        or
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        request.

        If no inventory fields are set in
        [CreateProductRequest.product][google.cloud.retail.v2alpha.CreateProductRequest.product],
        then any pre-existing inventory information for this product is
        used.

        If no inventory fields are set in
        [SetInventoryRequest.set_mask][google.cloud.retail.v2alpha.SetInventoryRequest.set_mask],
        then any existing inventory information is preserved.

        Pre-existing inventory information can only be updated with
        [ProductService.SetInventory][google.cloud.retail.v2alpha.ProductService.SetInventory],
        [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces],
        and
        [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces].

        The returned [Operation][google.longrunning.Operation]s is
        obsolete after one day, and the
        [GetOperation][google.longrunning.Operations.GetOperation] API
        returns ``NOT_FOUND`` afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates are not marked as
        [done][google.longrunning.Operation.done] until they are
        obsolete.

        Returns:
            Callable[[~.SetInventoryRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_inventory" not in self._stubs:
            self._stubs["set_inventory"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/SetInventory",
                request_serializer=product_service.SetInventoryRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_inventory"]

    @property
    def add_fulfillment_places(
        self,
    ) -> Callable[
        [product_service.AddFulfillmentPlacesRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the add fulfillment places method over gRPC.

        We recommend that you use the
        [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
        method instead of the
        [ProductService.AddFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.AddFulfillmentPlaces]
        method.
        [ProductService.AddLocalInventories][google.cloud.retail.v2alpha.ProductService.AddLocalInventories]
        achieves the same results but provides more fine-grained control
        over ingesting local inventory data.

        Incrementally adds place IDs to
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2alpha.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the added place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        Returns:
            Callable[[~.AddFulfillmentPlacesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_fulfillment_places" not in self._stubs:
            self._stubs["add_fulfillment_places"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/AddFulfillmentPlaces",
                request_serializer=product_service.AddFulfillmentPlacesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["add_fulfillment_places"]

    @property
    def remove_fulfillment_places(
        self,
    ) -> Callable[
        [product_service.RemoveFulfillmentPlacesRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the remove fulfillment places method over gRPC.

        We recommend that you use the
        [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
        method instead of the
        [ProductService.RemoveFulfillmentPlaces][google.cloud.retail.v2alpha.ProductService.RemoveFulfillmentPlaces]
        method.
        [ProductService.RemoveLocalInventories][google.cloud.retail.v2alpha.ProductService.RemoveLocalInventories]
        achieves the same results but provides more fine-grained control
        over ingesting local inventory data.

        Incrementally removes place IDs from a
        [Product.fulfillment_info.place_ids][google.cloud.retail.v2alpha.FulfillmentInfo.place_ids].

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating fulfillment information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, the removed place IDs
        are not immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        Returns:
            Callable[[~.RemoveFulfillmentPlacesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_fulfillment_places" not in self._stubs:
            self._stubs["remove_fulfillment_places"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/RemoveFulfillmentPlaces",
                request_serializer=product_service.RemoveFulfillmentPlacesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["remove_fulfillment_places"]

    @property
    def add_local_inventories(
        self,
    ) -> Callable[
        [product_service.AddLocalInventoriesRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the add local inventories method over gRPC.

        Updates local inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] at a list of
        places, while respecting the last update timestamps of each
        inventory field.

        This process is asynchronous and does not require the
        [Product][google.cloud.retail.v2alpha.Product] to exist before
        updating inventory information. If the request is valid, the
        update will be enqueued and processed downstream. As a
        consequence, when a response is returned, updates are not
        immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Local inventory information can only be modified using this
        method.
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        has no effect on local inventories.

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        Returns:
            Callable[[~.AddLocalInventoriesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_local_inventories" not in self._stubs:
            self._stubs["add_local_inventories"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/AddLocalInventories",
                request_serializer=product_service.AddLocalInventoriesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["add_local_inventories"]

    @property
    def remove_local_inventories(
        self,
    ) -> Callable[
        [product_service.RemoveLocalInventoriesRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the remove local inventories method over gRPC.

        Remove local inventory information for a
        [Product][google.cloud.retail.v2alpha.Product] at a list of
        places at a removal timestamp.

        This process is asynchronous. If the request is valid, the
        removal will be enqueued and processed downstream. As a
        consequence, when a response is returned, removals are not
        immediately manifested in the
        [Product][google.cloud.retail.v2alpha.Product] queried by
        [ProductService.GetProduct][google.cloud.retail.v2alpha.ProductService.GetProduct]
        or
        [ProductService.ListProducts][google.cloud.retail.v2alpha.ProductService.ListProducts].

        Local inventory information can only be removed using this
        method.
        [ProductService.CreateProduct][google.cloud.retail.v2alpha.ProductService.CreateProduct]
        and
        [ProductService.UpdateProduct][google.cloud.retail.v2alpha.ProductService.UpdateProduct]
        has no effect on local inventories.

        The returned [Operation][google.longrunning.Operation]s will be
        obsolete after 1 day, and
        [GetOperation][google.longrunning.Operations.GetOperation] API
        will return NOT_FOUND afterwards.

        If conflicting updates are issued, the
        [Operation][google.longrunning.Operation]s associated with the
        stale updates will not be marked as
        [done][google.longrunning.Operation.done] until being obsolete.

        Returns:
            Callable[[~.RemoveLocalInventoriesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_local_inventories" not in self._stubs:
            self._stubs["remove_local_inventories"] = self.grpc_channel.unary_unary(
                "/google.cloud.retail.v2alpha.ProductService/RemoveLocalInventories",
                request_serializer=product_service.RemoveLocalInventoriesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["remove_local_inventories"]

    def close(self):
        self.grpc_channel.close()

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
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
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
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("ProductServiceGrpcTransport",)
