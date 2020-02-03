# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.cloud.vision.v1p3beta1 ProductSearch API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
from google.api_core import operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.vision_v1p3beta1.gapic import enums
from google.cloud.vision_v1p3beta1.gapic import product_search_client_config
from google.cloud.vision_v1p3beta1.gapic.transports import product_search_grpc_transport
from google.cloud.vision_v1p3beta1.proto import product_search_service_pb2
from google.cloud.vision_v1p3beta1.proto import product_search_service_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-vision").version


class ProductSearchClient(object):
    """
    Manages Products and ProductSets of reference images for use in product
    search. It uses the following resource model:

    -  The API has a collection of ``ProductSet`` resources, named
       ``projects/*/locations/*/productSets/*``, which acts as a way to put
       different products into groups to limit identification.

    In parallel,

    -  The API has a collection of ``Product`` resources, named
       ``projects/*/locations/*/products/*``

    -  Each ``Product`` has a collection of ``ReferenceImage`` resources,
       named ``projects/*/locations/*/products/*/referenceImages/*``
    """

    SERVICE_ADDRESS = "vision.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.vision.v1p3beta1.ProductSearch"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ProductSearchClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def product_path(cls, project, location, product):
        """Return a fully-qualified product string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/products/{product}",
            project=project,
            location=location,
            product=product,
        )

    @classmethod
    def product_set_path(cls, project, location, product_set):
        """Return a fully-qualified product_set string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/productSets/{product_set}",
            project=project,
            location=location,
            product_set=product_set,
        )

    @classmethod
    def reference_image_path(cls, project, location, product, reference_image):
        """Return a fully-qualified reference_image string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/products/{product}/referenceImages/{reference_image}",
            project=project,
            location=location,
            product=product,
            reference_image=reference_image,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.ProductSearchGrpcTransport,
                    Callable[[~.Credentials, type], ~.ProductSearchGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = product_search_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=product_search_grpc_transport.ProductSearchGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = product_search_grpc_transport.ProductSearchGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_product_set(
        self,
        parent,
        product_set,
        product_set_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates and returns a new ProductSet resource.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if display\_name is missing, or is longer
           than 4096 characters.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `product_set`:
            >>> product_set = {}
            >>>
            >>> # TODO: Initialize `product_set_id`:
            >>> product_set_id = ''
            >>>
            >>> response = client.create_product_set(parent, product_set, product_set_id)

        Args:
            parent (str): Required. The project in which the ProductSet should be created.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
            product_set (Union[dict, ~google.cloud.vision_v1p3beta1.types.ProductSet]): Required. The ProductSet to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.ProductSet`
            product_set_id (str): A user-supplied resource id for this ProductSet. If set, the server will
                attempt to use this value as the resource id. If it is already in use,
                an error is returned with code ALREADY\_EXISTS. Must be at most 128
                characters long. It cannot contain the character ``/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.ProductSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_product_set,
                default_retry=self._method_configs["CreateProductSet"].retry,
                default_timeout=self._method_configs["CreateProductSet"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.CreateProductSetRequest(
            parent=parent, product_set=product_set, product_set_id=product_set_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_product_sets(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists ProductSets in an unspecified order.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100, or less
           than 1.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_product_sets(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_product_sets(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project from which ProductSets should be listed.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.vision_v1p3beta1.types.ProductSet` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_product_sets" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_product_sets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_product_sets,
                default_retry=self._method_configs["ListProductSets"].retry,
                default_timeout=self._method_configs["ListProductSets"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.ListProductSetsRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_product_sets"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="product_sets",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_product_set(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets information associated with a ProductSet.

        Possible errors:

        -  Returns NOT\_FOUND if the ProductSet does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_set_path('[PROJECT]', '[LOCATION]', '[PRODUCT_SET]')
            >>>
            >>> response = client.get_product_set(name)

        Args:
            name (str): Required. Resource name of the ProductSet to get.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.ProductSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_product_set,
                default_retry=self._method_configs["GetProductSet"].retry,
                default_timeout=self._method_configs["GetProductSet"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.GetProductSetRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_product_set(
        self,
        product_set,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Makes changes to a ProductSet resource. Only display\_name can be
        updated currently.

        Possible errors:

        -  Returns NOT\_FOUND if the ProductSet does not exist.
        -  Returns INVALID\_ARGUMENT if display\_name is present in update\_mask
           but missing from the request or longer than 4096 characters.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> # TODO: Initialize `product_set`:
            >>> product_set = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_product_set(product_set, update_mask)

        Args:
            product_set (Union[dict, ~google.cloud.vision_v1p3beta1.types.ProductSet]): Required. The ProductSet resource which replaces the one on the server.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.ProductSet`
            update_mask (Union[dict, ~google.cloud.vision_v1p3beta1.types.FieldMask]): The ``FieldMask`` that specifies which fields to update. If update\_mask
                isn't specified, all mutable fields are to be updated. Valid mask path
                is ``display_name``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.ProductSet` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_product_set,
                default_retry=self._method_configs["UpdateProductSet"].retry,
                default_timeout=self._method_configs["UpdateProductSet"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.UpdateProductSetRequest(
            product_set=product_set, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("product_set.name", product_set.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_product_set(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently deletes a ProductSet. All Products and ReferenceImages in
        the ProductSet will be deleted.

        The actual image files are not deleted from Google Cloud Storage.

        Possible errors:

        -  Returns NOT\_FOUND if the ProductSet does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_set_path('[PROJECT]', '[LOCATION]', '[PRODUCT_SET]')
            >>>
            >>> client.delete_product_set(name)

        Args:
            name (str): Required. Resource name of the ProductSet to delete.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_product_set,
                default_retry=self._method_configs["DeleteProductSet"].retry,
                default_timeout=self._method_configs["DeleteProductSet"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.DeleteProductSetRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_product(
        self,
        parent,
        product,
        product_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates and returns a new product resource.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if display\_name is missing or longer than
           4096 characters.
        -  Returns INVALID\_ARGUMENT if description is longer than 4096
           characters.
        -  Returns INVALID\_ARGUMENT if product\_category is missing or invalid.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `product`:
            >>> product = {}
            >>>
            >>> # TODO: Initialize `product_id`:
            >>> product_id = ''
            >>>
            >>> response = client.create_product(parent, product, product_id)

        Args:
            parent (str): Required. The project in which the Product should be created.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
            product (Union[dict, ~google.cloud.vision_v1p3beta1.types.Product]): Required. The product to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.Product`
            product_id (str): A user-supplied resource id for this Product. If set, the server will
                attempt to use this value as the resource id. If it is already in use,
                an error is returned with code ALREADY\_EXISTS. Must be at most 128
                characters long. It cannot contain the character ``/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.Product` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_product" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_product"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_product,
                default_retry=self._method_configs["CreateProduct"].retry,
                default_timeout=self._method_configs["CreateProduct"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.CreateProductRequest(
            parent=parent, product=product, product_id=product_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_product"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_products(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists products in an unspecified order.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100 or less
           than 1.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_products(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_products(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The project OR ProductSet from which Products should be
                listed.

                Format: ``projects/PROJECT_ID/locations/LOC_ID``
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.vision_v1p3beta1.types.Product` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_products" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_products"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_products,
                default_retry=self._method_configs["ListProducts"].retry,
                default_timeout=self._method_configs["ListProducts"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.ListProductsRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_products"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="products",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_product(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets information associated with a Product.

        Possible errors:

        -  Returns NOT\_FOUND if the Product does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_path('[PROJECT]', '[LOCATION]', '[PRODUCT]')
            >>>
            >>> response = client.get_product(name)

        Args:
            name (str): Required. Resource name of the Product to get.

                Format is: ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.Product` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_product" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_product"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_product,
                default_retry=self._method_configs["GetProduct"].retry,
                default_timeout=self._method_configs["GetProduct"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.GetProductRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_product"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_product(
        self,
        product,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Makes changes to a Product resource. Only display\_name, description and
        labels can be updated right now.

        If labels are updated, the change will not be reflected in queries until
        the next index time.

        Possible errors:

        -  Returns NOT\_FOUND if the Product does not exist.
        -  Returns INVALID\_ARGUMENT if display\_name is present in update\_mask
           but is missing from the request or longer than 4096 characters.
        -  Returns INVALID\_ARGUMENT if description is present in update\_mask
           but is longer than 4096 characters.
        -  Returns INVALID\_ARGUMENT if product\_category is present in
           update\_mask.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> # TODO: Initialize `product`:
            >>> product = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_product(product, update_mask)

        Args:
            product (Union[dict, ~google.cloud.vision_v1p3beta1.types.Product]): Required. The Product resource which replaces the one on the server.
                product.name is immutable.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.Product`
            update_mask (Union[dict, ~google.cloud.vision_v1p3beta1.types.FieldMask]): The ``FieldMask`` that specifies which fields to update. If update\_mask
                isn't specified, all mutable fields are to be updated. Valid mask paths
                include ``product_labels``, ``display_name``, and ``description``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.Product` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_product" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_product"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_product,
                default_retry=self._method_configs["UpdateProduct"].retry,
                default_timeout=self._method_configs["UpdateProduct"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.UpdateProductRequest(
            product=product, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("product.name", product.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_product"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_product(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently deletes a product and its reference images.

        Metadata of the product and all its images will be deleted right away,
        but search queries against ProductSets containing the product may still
        work until all related caches are refreshed.

        Possible errors:

        -  Returns NOT\_FOUND if the product does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_path('[PROJECT]', '[LOCATION]', '[PRODUCT]')
            >>>
            >>> client.delete_product(name)

        Args:
            name (str): Required. Resource name of product to delete.

                Format is: ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_product" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_product"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_product,
                default_retry=self._method_configs["DeleteProduct"].retry,
                default_timeout=self._method_configs["DeleteProduct"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.DeleteProductRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_product"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_reference_image(
        self,
        parent,
        reference_image,
        reference_image_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates and returns a new ReferenceImage resource.

        The ``bounding_poly`` field is optional. If ``bounding_poly`` is not
        specified, the system will try to detect regions of interest in the
        image that are compatible with the product\_category on the parent
        product. If it is specified, detection is ALWAYS skipped. The system
        converts polygons into non-rotated rectangles.

        Note that the pipeline will resize the image if the image resolution is
        too large to process (above 50MP).

        Possible errors:

        -  Returns INVALID\_ARGUMENT if the image\_uri is missing or longer than
           4096 characters.
        -  Returns INVALID\_ARGUMENT if the product does not exist.
        -  Returns INVALID\_ARGUMENT if bounding\_poly is not provided, and
           nothing compatible with the parent product's product\_category is
           detected.
        -  Returns INVALID\_ARGUMENT if bounding\_poly contains more than 10
           polygons.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.product_path('[PROJECT]', '[LOCATION]', '[PRODUCT]')
            >>>
            >>> # TODO: Initialize `reference_image`:
            >>> reference_image = {}
            >>>
            >>> # TODO: Initialize `reference_image_id`:
            >>> reference_image_id = ''
            >>>
            >>> response = client.create_reference_image(parent, reference_image, reference_image_id)

        Args:
            parent (str): Required. Resource name of the product in which to create the reference
                image.

                Format is ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.
            reference_image (Union[dict, ~google.cloud.vision_v1p3beta1.types.ReferenceImage]): Required. The reference image to create.
                If an image ID is specified, it is ignored.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.ReferenceImage`
            reference_image_id (str): A user-supplied resource id for the ReferenceImage to be added. If set,
                the server will attempt to use this value as the resource id. If it is
                already in use, an error is returned with code ALREADY\_EXISTS. Must be
                at most 128 characters long. It cannot contain the character ``/``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.ReferenceImage` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_reference_image" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_reference_image"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_reference_image,
                default_retry=self._method_configs["CreateReferenceImage"].retry,
                default_timeout=self._method_configs["CreateReferenceImage"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.CreateReferenceImageRequest(
            parent=parent,
            reference_image=reference_image,
            reference_image_id=reference_image_id,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_reference_image"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_reference_image(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently deletes a reference image.

        The image metadata will be deleted right away, but search queries
        against ProductSets containing the image may still work until all
        related caches are refreshed.

        The actual image files are not deleted from Google Cloud Storage.

        Possible errors:

        -  Returns NOT\_FOUND if the reference image does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.reference_image_path('[PROJECT]', '[LOCATION]', '[PRODUCT]', '[REFERENCE_IMAGE]')
            >>>
            >>> client.delete_reference_image(name)

        Args:
            name (str): Required. The resource name of the reference image to delete.

                Format is:

                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_reference_image" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_reference_image"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_reference_image,
                default_retry=self._method_configs["DeleteReferenceImage"].retry,
                default_timeout=self._method_configs["DeleteReferenceImage"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.DeleteReferenceImageRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_reference_image"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_reference_images(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists reference images.

        Possible errors:

        -  Returns NOT\_FOUND if the parent product does not exist.
        -  Returns INVALID\_ARGUMENT if the page\_size is greater than 100, or
           less than 1.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.product_path('[PROJECT]', '[LOCATION]', '[PRODUCT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_reference_images(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_reference_images(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. Resource name of the product containing the reference images.

                Format is ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.vision_v1p3beta1.types.ReferenceImage` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_reference_images" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_reference_images"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_reference_images,
                default_retry=self._method_configs["ListReferenceImages"].retry,
                default_timeout=self._method_configs["ListReferenceImages"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.ListReferenceImagesRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_reference_images"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="reference_images",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_reference_image(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets information associated with a ReferenceImage.

        Possible errors:

        -  Returns NOT\_FOUND if the specified image does not exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.reference_image_path('[PROJECT]', '[LOCATION]', '[PRODUCT]', '[REFERENCE_IMAGE]')
            >>>
            >>> response = client.get_reference_image(name)

        Args:
            name (str): Required. The resource name of the ReferenceImage to get.

                Format is:

                ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID/referenceImages/IMAGE_ID``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types.ReferenceImage` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_reference_image" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_reference_image"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_reference_image,
                default_retry=self._method_configs["GetReferenceImage"].retry,
                default_timeout=self._method_configs["GetReferenceImage"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.GetReferenceImageRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_reference_image"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def add_product_to_product_set(
        self,
        name,
        product,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Adds a Product to the specified ProductSet. If the Product is already
        present, no change is made.

        One Product can be added to at most 100 ProductSets.

        Possible errors:

        -  Returns NOT\_FOUND if the Product or the ProductSet doesn't exist.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_set_path('[PROJECT]', '[LOCATION]', '[PRODUCT_SET]')
            >>>
            >>> # TODO: Initialize `product`:
            >>> product = ''
            >>>
            >>> client.add_product_to_product_set(name, product)

        Args:
            name (str): Required. The resource name for the ProductSet to modify.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
            product (str): Required. The resource name for the Product to be added to this
                ProductSet.

                Format is: ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "add_product_to_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "add_product_to_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.add_product_to_product_set,
                default_retry=self._method_configs["AddProductToProductSet"].retry,
                default_timeout=self._method_configs["AddProductToProductSet"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.AddProductToProductSetRequest(
            name=name, product=product
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["add_product_to_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def remove_product_from_product_set(
        self,
        name,
        product,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Removes a Product from the specified ProductSet.

        Possible errors:

        -  Returns NOT\_FOUND If the Product is not found under the ProductSet.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_set_path('[PROJECT]', '[LOCATION]', '[PRODUCT_SET]')
            >>>
            >>> # TODO: Initialize `product`:
            >>> product = ''
            >>>
            >>> client.remove_product_from_product_set(name, product)

        Args:
            name (str): Required. The resource name for the ProductSet to modify.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
            product (str): Required. The resource name for the Product to be removed from this
                ProductSet.

                Format is: ``projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID``
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "remove_product_from_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "remove_product_from_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.remove_product_from_product_set,
                default_retry=self._method_configs["RemoveProductFromProductSet"].retry,
                default_timeout=self._method_configs[
                    "RemoveProductFromProductSet"
                ].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.RemoveProductFromProductSetRequest(
            name=name, product=product
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["remove_product_from_product_set"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_products_in_product_set(
        self,
        name,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the Products in a ProductSet, in an unspecified order. If the
        ProductSet does not exist, the products field of the response will be
        empty.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100 or less
           than 1.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> name = client.product_set_path('[PROJECT]', '[LOCATION]', '[PRODUCT_SET]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_products_in_product_set(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_products_in_product_set(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): Required. The ProductSet resource for which to retrieve Products.

                Format is:
                ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.vision_v1p3beta1.types.Product` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_products_in_product_set" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_products_in_product_set"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_products_in_product_set,
                default_retry=self._method_configs["ListProductsInProductSet"].retry,
                default_timeout=self._method_configs[
                    "ListProductsInProductSet"
                ].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.ListProductsInProductSetRequest(
            name=name, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_products_in_product_set"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="products",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def import_product_sets(
        self,
        parent,
        input_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Asynchronous API that imports a list of reference images to specified
        product sets based on a list of image information.

        The ``google.longrunning.Operation`` API can be used to keep track of
        the progress and results of the request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress) ``Operation.response`` contains
        ``ImportProductSetsResponse``. (results)

        The input source of this method is a csv file on Google Cloud Storage.
        For the format of the csv file please see
        ``ImportProductSetsGcsSource.csv_file_uri``.

        Example:
            >>> from google.cloud import vision_v1p3beta1
            >>>
            >>> client = vision_v1p3beta1.ProductSearchClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `input_config`:
            >>> input_config = {}
            >>>
            >>> response = client.import_product_sets(parent, input_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The project in which the ProductSets should be imported.

                Format is ``projects/PROJECT_ID/locations/LOC_ID``.
            input_config (Union[dict, ~google.cloud.vision_v1p3beta1.types.ImportProductSetsInputConfig]): Required. The input content for the list of requests.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1p3beta1.types.ImportProductSetsInputConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1p3beta1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "import_product_sets" not in self._inner_api_calls:
            self._inner_api_calls[
                "import_product_sets"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.import_product_sets,
                default_retry=self._method_configs["ImportProductSets"].retry,
                default_timeout=self._method_configs["ImportProductSets"].timeout,
                client_info=self._client_info,
            )

        request = product_search_service_pb2.ImportProductSetsRequest(
            parent=parent, input_config=input_config
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["import_product_sets"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            product_search_service_pb2.ImportProductSetsResponse,
            metadata_type=product_search_service_pb2.BatchOperationMetadata,
        )
