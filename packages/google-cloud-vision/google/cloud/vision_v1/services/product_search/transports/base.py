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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.vision_v1.types import product_search_service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-vision",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ProductSearchTransport(abc.ABC):
    """Abstract transport class for ProductSearch."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-vision",
    )

    def __init__(
        self,
        *,
        host: str = "vision.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_product_set: gapic_v1.method.wrap_method(
                self.create_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_product_sets: gapic_v1.method.wrap_method(
                self.list_product_sets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_product_set: gapic_v1.method.wrap_method(
                self.get_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.update_product_set: gapic_v1.method.wrap_method(
                self.update_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_product_set: gapic_v1.method.wrap_method(
                self.delete_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.create_product: gapic_v1.method.wrap_method(
                self.create_product,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_products: gapic_v1.method.wrap_method(
                self.list_products,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_product: gapic_v1.method.wrap_method(
                self.get_product,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.update_product: gapic_v1.method.wrap_method(
                self.update_product,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_product: gapic_v1.method.wrap_method(
                self.delete_product,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.create_reference_image: gapic_v1.method.wrap_method(
                self.create_reference_image,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_reference_image: gapic_v1.method.wrap_method(
                self.delete_reference_image,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_reference_images: gapic_v1.method.wrap_method(
                self.list_reference_images,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_reference_image: gapic_v1.method.wrap_method(
                self.get_reference_image,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.add_product_to_product_set: gapic_v1.method.wrap_method(
                self.add_product_to_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.remove_product_from_product_set: gapic_v1.method.wrap_method(
                self.remove_product_from_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_products_in_product_set: gapic_v1.method.wrap_method(
                self.list_products_in_product_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.import_product_sets: gapic_v1.method.wrap_method(
                self.import_product_sets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.purge_products: gapic_v1.method.wrap_method(
                self.purge_products,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(),
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.CreateProductSetRequest],
        typing.Union[
            product_search_service.ProductSet,
            typing.Awaitable[product_search_service.ProductSet],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_product_sets(
        self,
    ) -> typing.Callable[
        [product_search_service.ListProductSetsRequest],
        typing.Union[
            product_search_service.ListProductSetsResponse,
            typing.Awaitable[product_search_service.ListProductSetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.GetProductSetRequest],
        typing.Union[
            product_search_service.ProductSet,
            typing.Awaitable[product_search_service.ProductSet],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.UpdateProductSetRequest],
        typing.Union[
            product_search_service.ProductSet,
            typing.Awaitable[product_search_service.ProductSet],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.DeleteProductSetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_product(
        self,
    ) -> typing.Callable[
        [product_search_service.CreateProductRequest],
        typing.Union[
            product_search_service.Product,
            typing.Awaitable[product_search_service.Product],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_products(
        self,
    ) -> typing.Callable[
        [product_search_service.ListProductsRequest],
        typing.Union[
            product_search_service.ListProductsResponse,
            typing.Awaitable[product_search_service.ListProductsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_product(
        self,
    ) -> typing.Callable[
        [product_search_service.GetProductRequest],
        typing.Union[
            product_search_service.Product,
            typing.Awaitable[product_search_service.Product],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_product(
        self,
    ) -> typing.Callable[
        [product_search_service.UpdateProductRequest],
        typing.Union[
            product_search_service.Product,
            typing.Awaitable[product_search_service.Product],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_product(
        self,
    ) -> typing.Callable[
        [product_search_service.DeleteProductRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_reference_image(
        self,
    ) -> typing.Callable[
        [product_search_service.CreateReferenceImageRequest],
        typing.Union[
            product_search_service.ReferenceImage,
            typing.Awaitable[product_search_service.ReferenceImage],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_reference_image(
        self,
    ) -> typing.Callable[
        [product_search_service.DeleteReferenceImageRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_reference_images(
        self,
    ) -> typing.Callable[
        [product_search_service.ListReferenceImagesRequest],
        typing.Union[
            product_search_service.ListReferenceImagesResponse,
            typing.Awaitable[product_search_service.ListReferenceImagesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_reference_image(
        self,
    ) -> typing.Callable[
        [product_search_service.GetReferenceImageRequest],
        typing.Union[
            product_search_service.ReferenceImage,
            typing.Awaitable[product_search_service.ReferenceImage],
        ],
    ]:
        raise NotImplementedError()

    @property
    def add_product_to_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.AddProductToProductSetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def remove_product_from_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.RemoveProductFromProductSetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_products_in_product_set(
        self,
    ) -> typing.Callable[
        [product_search_service.ListProductsInProductSetRequest],
        typing.Union[
            product_search_service.ListProductsInProductSetResponse,
            typing.Awaitable[product_search_service.ListProductsInProductSetResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def import_product_sets(
        self,
    ) -> typing.Callable[
        [product_search_service.ImportProductSetsRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def purge_products(
        self,
    ) -> typing.Callable[
        [product_search_service.PurgeProductsRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("ProductSearchTransport",)
