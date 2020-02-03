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


import google.api_core.grpc_helpers
from google.api_core import operations_v1

from google.cloud.vision_v1p4beta1.proto import product_search_service_pb2_grpc


class ProductSearchGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.vision.v1p4beta1 ProductSearch API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-vision",
    )

    def __init__(
        self, channel=None, credentials=None, address="vision.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "product_search_stub": product_search_service_pb2_grpc.ProductSearchStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="vision.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.create_product_set`.

        Creates and returns a new ProductSet resource.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if display\_name is missing, or is longer
           than 4096 characters.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].CreateProductSet

    @property
    def list_product_sets(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.list_product_sets`.

        Lists ProductSets in an unspecified order.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100, or less
           than 1.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].ListProductSets

    @property
    def get_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.get_product_set`.

        Gets information associated with a ProductSet.

        Possible errors:

        -  Returns NOT\_FOUND if the ProductSet does not exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].GetProductSet

    @property
    def update_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.update_product_set`.

        Makes changes to a ProductSet resource. Only display\_name can be
        updated currently.

        Possible errors:

        -  Returns NOT\_FOUND if the ProductSet does not exist.
        -  Returns INVALID\_ARGUMENT if display\_name is present in update\_mask
           but missing from the request or longer than 4096 characters.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].UpdateProductSet

    @property
    def delete_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.delete_product_set`.

        Permanently deletes a ProductSet. Products and ReferenceImages in the
        ProductSet are not deleted.

        The actual image files are not deleted from Google Cloud Storage.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].DeleteProductSet

    @property
    def create_product(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.create_product`.

        Creates and returns a new product resource.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if display\_name is missing or longer than
           4096 characters.
        -  Returns INVALID\_ARGUMENT if description is longer than 4096
           characters.
        -  Returns INVALID\_ARGUMENT if product\_category is missing or invalid.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].CreateProduct

    @property
    def list_products(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.list_products`.

        Lists products in an unspecified order.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100 or less
           than 1.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].ListProducts

    @property
    def get_product(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.get_product`.

        Gets information associated with a Product.

        Possible errors:

        -  Returns NOT\_FOUND if the Product does not exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].GetProduct

    @property
    def update_product(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.update_product`.

        Makes changes to a Product resource. Only the ``display_name``,
        ``description``, and ``labels`` fields can be updated right now.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].UpdateProduct

    @property
    def delete_product(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.delete_product`.

        Permanently deletes a product and its reference images.

        Metadata of the product and all its images will be deleted right away, but
        search queries against ProductSets containing the product may still work
        until all related caches are refreshed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].DeleteProduct

    @property
    def create_reference_image(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.create_reference_image`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].CreateReferenceImage

    @property
    def delete_reference_image(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.delete_reference_image`.

        Permanently deletes a reference image.

        The image metadata will be deleted right away, but search queries
        against ProductSets containing the image may still work until all related
        caches are refreshed.

        The actual image files are not deleted from Google Cloud Storage.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].DeleteReferenceImage

    @property
    def list_reference_images(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.list_reference_images`.

        Lists reference images.

        Possible errors:

        -  Returns NOT\_FOUND if the parent product does not exist.
        -  Returns INVALID\_ARGUMENT if the page\_size is greater than 100, or
           less than 1.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].ListReferenceImages

    @property
    def get_reference_image(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.get_reference_image`.

        Gets information associated with a ReferenceImage.

        Possible errors:

        -  Returns NOT\_FOUND if the specified image does not exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].GetReferenceImage

    @property
    def add_product_to_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.add_product_to_product_set`.

        Adds a Product to the specified ProductSet. If the Product is already
        present, no change is made.

        One Product can be added to at most 100 ProductSets.

        Possible errors:

        -  Returns NOT\_FOUND if the Product or the ProductSet doesn't exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].AddProductToProductSet

    @property
    def remove_product_from_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.remove_product_from_product_set`.

        Removes a Product from the specified ProductSet.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].RemoveProductFromProductSet

    @property
    def list_products_in_product_set(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.list_products_in_product_set`.

        Lists the Products in a ProductSet, in an unspecified order. If the
        ProductSet does not exist, the products field of the response will be
        empty.

        Possible errors:

        -  Returns INVALID\_ARGUMENT if page\_size is greater than 100 or less
           than 1.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].ListProductsInProductSet

    @property
    def import_product_sets(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.import_product_sets`.

        Asynchronous API that imports a list of reference images to specified
        product sets based on a list of image information.

        The ``google.longrunning.Operation`` API can be used to keep track of
        the progress and results of the request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress) ``Operation.response`` contains
        ``ImportProductSetsResponse``. (results)

        The input source of this method is a csv file on Google Cloud Storage.
        For the format of the csv file please see
        ``ImportProductSetsGcsSource.csv_file_uri``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].ImportProductSets

    @property
    def purge_products(self):
        """Return the gRPC stub for :meth:`ProductSearchClient.purge_products`.

        Asynchronous API to delete all Products in a ProductSet or all Products
        that are in no ProductSet.

        If a Product is a member of the specified ProductSet in addition to
        other ProductSets, the Product will still be deleted.

        It is recommended to not delete the specified ProductSet until after
        this operation has completed. It is also recommended to not add any of
        the Products involved in the batch delete to a new ProductSet while this
        operation is running because those Products may still end up deleted.

        It's not possible to undo the PurgeProducts operation. Therefore, it is
        recommended to keep the csv files used in ImportProductSets (if that was
        how you originally built the Product Set) before starting PurgeProducts,
        in case you need to re-import the data after deletion.

        If the plan is to purge all of the Products from a ProductSet and then
        re-use the empty ProductSet to re-import new Products into the empty
        ProductSet, you must wait until the PurgeProducts operation has finished
        for that ProductSet.

        The ``google.longrunning.Operation`` API can be used to keep track of
        the progress and results of the request. ``Operation.metadata`` contains
        ``BatchOperationMetadata``. (progress)

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["product_search_stub"].PurgeProducts
