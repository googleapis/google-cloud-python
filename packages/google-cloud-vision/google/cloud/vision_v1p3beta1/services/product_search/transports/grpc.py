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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.vision_v1p3beta1.types import product_search_service

from .base import DEFAULT_CLIENT_INFO, ProductSearchTransport

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
                    "serviceName": "google.cloud.vision.v1p3beta1.ProductSearch",
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
                    "serviceName": "google.cloud.vision.v1p3beta1.ProductSearch",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class ProductSearchGrpcTransport(ProductSearchTransport):
    """gRPC backend transport for ProductSearch.

    Manages Products and ProductSets of reference images for use in
    product search. It uses the following resource model:

    -  The API has a collection of
       [ProductSet][google.cloud.vision.v1p3beta1.ProductSet] resources,
       named ``projects/*/locations/*/productSets/*``, which acts as a
       way to put different products into groups to limit
       identification.

    In parallel,

    -  The API has a collection of
       [Product][google.cloud.vision.v1p3beta1.Product] resources, named
       ``projects/*/locations/*/products/*``

    -  Each [Product][google.cloud.vision.v1p3beta1.Product] has a
       collection of
       [ReferenceImage][google.cloud.vision.v1p3beta1.ReferenceImage]
       resources, named
       ``projects/*/locations/*/products/*/referenceImages/*``

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
        host: str = "vision.googleapis.com",
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
                 The hostname to connect to (default: 'vision.googleapis.com').
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
        host: str = "vision.googleapis.com",
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
    def create_product_set(
        self,
    ) -> Callable[
        [product_search_service.CreateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        r"""Return a callable for the create product set method over gRPC.

        Creates and returns a new ProductSet resource.

        Possible errors:

        -  Returns INVALID_ARGUMENT if display_name is missing, or is
           longer than 4096 characters.

        Returns:
            Callable[[~.CreateProductSetRequest],
                    ~.ProductSet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_product_set" not in self._stubs:
            self._stubs["create_product_set"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/CreateProductSet",
                request_serializer=product_search_service.CreateProductSetRequest.serialize,
                response_deserializer=product_search_service.ProductSet.deserialize,
            )
        return self._stubs["create_product_set"]

    @property
    def list_product_sets(
        self,
    ) -> Callable[
        [product_search_service.ListProductSetsRequest],
        product_search_service.ListProductSetsResponse,
    ]:
        r"""Return a callable for the list product sets method over gRPC.

        Lists ProductSets in an unspecified order.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100, or
           less than 1.

        Returns:
            Callable[[~.ListProductSetsRequest],
                    ~.ListProductSetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_product_sets" not in self._stubs:
            self._stubs["list_product_sets"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/ListProductSets",
                request_serializer=product_search_service.ListProductSetsRequest.serialize,
                response_deserializer=product_search_service.ListProductSetsResponse.deserialize,
            )
        return self._stubs["list_product_sets"]

    @property
    def get_product_set(
        self,
    ) -> Callable[
        [product_search_service.GetProductSetRequest], product_search_service.ProductSet
    ]:
        r"""Return a callable for the get product set method over gRPC.

        Gets information associated with a ProductSet.

        Possible errors:

        -  Returns NOT_FOUND if the ProductSet does not exist.

        Returns:
            Callable[[~.GetProductSetRequest],
                    ~.ProductSet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_product_set" not in self._stubs:
            self._stubs["get_product_set"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/GetProductSet",
                request_serializer=product_search_service.GetProductSetRequest.serialize,
                response_deserializer=product_search_service.ProductSet.deserialize,
            )
        return self._stubs["get_product_set"]

    @property
    def update_product_set(
        self,
    ) -> Callable[
        [product_search_service.UpdateProductSetRequest],
        product_search_service.ProductSet,
    ]:
        r"""Return a callable for the update product set method over gRPC.

        Makes changes to a ProductSet resource. Only display_name can be
        updated currently.

        Possible errors:

        -  Returns NOT_FOUND if the ProductSet does not exist.
        -  Returns INVALID_ARGUMENT if display_name is present in
           update_mask but missing from the request or longer than 4096
           characters.

        Returns:
            Callable[[~.UpdateProductSetRequest],
                    ~.ProductSet]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_product_set" not in self._stubs:
            self._stubs["update_product_set"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/UpdateProductSet",
                request_serializer=product_search_service.UpdateProductSetRequest.serialize,
                response_deserializer=product_search_service.ProductSet.deserialize,
            )
        return self._stubs["update_product_set"]

    @property
    def delete_product_set(
        self,
    ) -> Callable[[product_search_service.DeleteProductSetRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete product set method over gRPC.

        Permanently deletes a ProductSet. All Products and
        ReferenceImages in the ProductSet will be deleted.

        The actual image files are not deleted from Google Cloud
        Storage.

        Possible errors:

        -  Returns NOT_FOUND if the ProductSet does not exist.

        Returns:
            Callable[[~.DeleteProductSetRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_product_set" not in self._stubs:
            self._stubs["delete_product_set"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/DeleteProductSet",
                request_serializer=product_search_service.DeleteProductSetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_product_set"]

    @property
    def create_product(
        self,
    ) -> Callable[
        [product_search_service.CreateProductRequest], product_search_service.Product
    ]:
        r"""Return a callable for the create product method over gRPC.

        Creates and returns a new product resource.

        Possible errors:

        -  Returns INVALID_ARGUMENT if display_name is missing or longer
           than 4096 characters.
        -  Returns INVALID_ARGUMENT if description is longer than 4096
           characters.
        -  Returns INVALID_ARGUMENT if product_category is missing or
           invalid.

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
            self._stubs["create_product"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/CreateProduct",
                request_serializer=product_search_service.CreateProductRequest.serialize,
                response_deserializer=product_search_service.Product.deserialize,
            )
        return self._stubs["create_product"]

    @property
    def list_products(
        self,
    ) -> Callable[
        [product_search_service.ListProductsRequest],
        product_search_service.ListProductsResponse,
    ]:
        r"""Return a callable for the list products method over gRPC.

        Lists products in an unspecified order.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100 or
           less than 1.

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
            self._stubs["list_products"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/ListProducts",
                request_serializer=product_search_service.ListProductsRequest.serialize,
                response_deserializer=product_search_service.ListProductsResponse.deserialize,
            )
        return self._stubs["list_products"]

    @property
    def get_product(
        self,
    ) -> Callable[
        [product_search_service.GetProductRequest], product_search_service.Product
    ]:
        r"""Return a callable for the get product method over gRPC.

        Gets information associated with a Product.

        Possible errors:

        -  Returns NOT_FOUND if the Product does not exist.

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
            self._stubs["get_product"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/GetProduct",
                request_serializer=product_search_service.GetProductRequest.serialize,
                response_deserializer=product_search_service.Product.deserialize,
            )
        return self._stubs["get_product"]

    @property
    def update_product(
        self,
    ) -> Callable[
        [product_search_service.UpdateProductRequest], product_search_service.Product
    ]:
        r"""Return a callable for the update product method over gRPC.

        Makes changes to a Product resource. Only display_name,
        description and labels can be updated right now.

        If labels are updated, the change will not be reflected in
        queries until the next index time.

        Possible errors:

        -  Returns NOT_FOUND if the Product does not exist.
        -  Returns INVALID_ARGUMENT if display_name is present in
           update_mask but is missing from the request or longer than
           4096 characters.
        -  Returns INVALID_ARGUMENT if description is present in
           update_mask but is longer than 4096 characters.
        -  Returns INVALID_ARGUMENT if product_category is present in
           update_mask.

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
            self._stubs["update_product"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/UpdateProduct",
                request_serializer=product_search_service.UpdateProductRequest.serialize,
                response_deserializer=product_search_service.Product.deserialize,
            )
        return self._stubs["update_product"]

    @property
    def delete_product(
        self,
    ) -> Callable[[product_search_service.DeleteProductRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete product method over gRPC.

        Permanently deletes a product and its reference images.

        Metadata of the product and all its images will be deleted right
        away, but search queries against ProductSets containing the
        product may still work until all related caches are refreshed.

        Possible errors:

        -  Returns NOT_FOUND if the product does not exist.

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
            self._stubs["delete_product"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/DeleteProduct",
                request_serializer=product_search_service.DeleteProductRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_product"]

    @property
    def create_reference_image(
        self,
    ) -> Callable[
        [product_search_service.CreateReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        r"""Return a callable for the create reference image method over gRPC.

        Creates and returns a new ReferenceImage resource.

        The ``bounding_poly`` field is optional. If ``bounding_poly`` is
        not specified, the system will try to detect regions of interest
        in the image that are compatible with the product_category on
        the parent product. If it is specified, detection is ALWAYS
        skipped. The system converts polygons into non-rotated
        rectangles.

        Note that the pipeline will resize the image if the image
        resolution is too large to process (above 50MP).

        Possible errors:

        -  Returns INVALID_ARGUMENT if the image_uri is missing or
           longer than 4096 characters.
        -  Returns INVALID_ARGUMENT if the product does not exist.
        -  Returns INVALID_ARGUMENT if bounding_poly is not provided,
           and nothing compatible with the parent product's
           product_category is detected.
        -  Returns INVALID_ARGUMENT if bounding_poly contains more than
           10 polygons.

        Returns:
            Callable[[~.CreateReferenceImageRequest],
                    ~.ReferenceImage]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_reference_image" not in self._stubs:
            self._stubs["create_reference_image"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/CreateReferenceImage",
                request_serializer=product_search_service.CreateReferenceImageRequest.serialize,
                response_deserializer=product_search_service.ReferenceImage.deserialize,
            )
        return self._stubs["create_reference_image"]

    @property
    def delete_reference_image(
        self,
    ) -> Callable[
        [product_search_service.DeleteReferenceImageRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the delete reference image method over gRPC.

        Permanently deletes a reference image.

        The image metadata will be deleted right away, but search
        queries against ProductSets containing the image may still work
        until all related caches are refreshed.

        The actual image files are not deleted from Google Cloud
        Storage.

        Possible errors:

        -  Returns NOT_FOUND if the reference image does not exist.

        Returns:
            Callable[[~.DeleteReferenceImageRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_reference_image" not in self._stubs:
            self._stubs["delete_reference_image"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/DeleteReferenceImage",
                request_serializer=product_search_service.DeleteReferenceImageRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_reference_image"]

    @property
    def list_reference_images(
        self,
    ) -> Callable[
        [product_search_service.ListReferenceImagesRequest],
        product_search_service.ListReferenceImagesResponse,
    ]:
        r"""Return a callable for the list reference images method over gRPC.

        Lists reference images.

        Possible errors:

        -  Returns NOT_FOUND if the parent product does not exist.
        -  Returns INVALID_ARGUMENT if the page_size is greater than
           100, or less than 1.

        Returns:
            Callable[[~.ListReferenceImagesRequest],
                    ~.ListReferenceImagesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_reference_images" not in self._stubs:
            self._stubs["list_reference_images"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/ListReferenceImages",
                request_serializer=product_search_service.ListReferenceImagesRequest.serialize,
                response_deserializer=product_search_service.ListReferenceImagesResponse.deserialize,
            )
        return self._stubs["list_reference_images"]

    @property
    def get_reference_image(
        self,
    ) -> Callable[
        [product_search_service.GetReferenceImageRequest],
        product_search_service.ReferenceImage,
    ]:
        r"""Return a callable for the get reference image method over gRPC.

        Gets information associated with a ReferenceImage.

        Possible errors:

        -  Returns NOT_FOUND if the specified image does not exist.

        Returns:
            Callable[[~.GetReferenceImageRequest],
                    ~.ReferenceImage]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_reference_image" not in self._stubs:
            self._stubs["get_reference_image"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/GetReferenceImage",
                request_serializer=product_search_service.GetReferenceImageRequest.serialize,
                response_deserializer=product_search_service.ReferenceImage.deserialize,
            )
        return self._stubs["get_reference_image"]

    @property
    def add_product_to_product_set(
        self,
    ) -> Callable[
        [product_search_service.AddProductToProductSetRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the add product to product set method over gRPC.

        Adds a Product to the specified ProductSet. If the Product is
        already present, no change is made.

        One Product can be added to at most 100 ProductSets.

        Possible errors:

        -  Returns NOT_FOUND if the Product or the ProductSet doesn't
           exist.

        Returns:
            Callable[[~.AddProductToProductSetRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_product_to_product_set" not in self._stubs:
            self._stubs[
                "add_product_to_product_set"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/AddProductToProductSet",
                request_serializer=product_search_service.AddProductToProductSetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["add_product_to_product_set"]

    @property
    def remove_product_from_product_set(
        self,
    ) -> Callable[
        [product_search_service.RemoveProductFromProductSetRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the remove product from product
        set method over gRPC.

        Removes a Product from the specified ProductSet.

        Possible errors:

        -  Returns NOT_FOUND If the Product is not found under the
           ProductSet.

        Returns:
            Callable[[~.RemoveProductFromProductSetRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "remove_product_from_product_set" not in self._stubs:
            self._stubs[
                "remove_product_from_product_set"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/RemoveProductFromProductSet",
                request_serializer=product_search_service.RemoveProductFromProductSetRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["remove_product_from_product_set"]

    @property
    def list_products_in_product_set(
        self,
    ) -> Callable[
        [product_search_service.ListProductsInProductSetRequest],
        product_search_service.ListProductsInProductSetResponse,
    ]:
        r"""Return a callable for the list products in product set method over gRPC.

        Lists the Products in a ProductSet, in an unspecified order. If
        the ProductSet does not exist, the products field of the
        response will be empty.

        Possible errors:

        -  Returns INVALID_ARGUMENT if page_size is greater than 100 or
           less than 1.

        Returns:
            Callable[[~.ListProductsInProductSetRequest],
                    ~.ListProductsInProductSetResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_products_in_product_set" not in self._stubs:
            self._stubs[
                "list_products_in_product_set"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/ListProductsInProductSet",
                request_serializer=product_search_service.ListProductsInProductSetRequest.serialize,
                response_deserializer=product_search_service.ListProductsInProductSetResponse.deserialize,
            )
        return self._stubs["list_products_in_product_set"]

    @property
    def import_product_sets(
        self,
    ) -> Callable[
        [product_search_service.ImportProductSetsRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the import product sets method over gRPC.

        Asynchronous API that imports a list of reference images to
        specified product sets based on a list of image information.

        The [google.longrunning.Operation][google.longrunning.Operation]
        API can be used to keep track of the progress and results of the
        request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress) ``Operation.response``
        contains ``ImportProductSetsResponse``. (results)

        The input source of this method is a csv file on Google Cloud
        Storage. For the format of the csv file please see
        [ImportProductSetsGcsSource.csv_file_uri][google.cloud.vision.v1p3beta1.ImportProductSetsGcsSource.csv_file_uri].

        Returns:
            Callable[[~.ImportProductSetsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_product_sets" not in self._stubs:
            self._stubs["import_product_sets"] = self._logged_channel.unary_unary(
                "/google.cloud.vision.v1p3beta1.ProductSearch/ImportProductSets",
                request_serializer=product_search_service.ImportProductSetsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_product_sets"]

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("ProductSearchGrpcTransport",)
