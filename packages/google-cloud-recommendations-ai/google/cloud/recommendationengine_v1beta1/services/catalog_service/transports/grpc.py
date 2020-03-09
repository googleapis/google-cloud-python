# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.recommendationengine_v1beta1.types import catalog
from google.cloud.recommendationengine_v1beta1.types import catalog_service
from google.cloud.recommendationengine_v1beta1.types import import_
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import CatalogServiceTransport


class CatalogServiceGrpcTransport(CatalogServiceTransport):
    """gRPC backend transport for CatalogService.

    Service for ingesting catalog information of the customer's
    website.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "recommendationengine.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @classmethod
    def create_channel(
        cls,
        host: str = "recommendationengine.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def create_catalog_item(
        self
    ) -> Callable[[catalog_service.CreateCatalogItemRequest], catalog.CatalogItem]:
        r"""Return a callable for the create catalog item method over gRPC.

        Creates a catalog item.

        Returns:
            Callable[[~.CreateCatalogItemRequest],
                    ~.CatalogItem]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_catalog_item" not in self._stubs:
            self._stubs["create_catalog_item"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/CreateCatalogItem",
                request_serializer=catalog_service.CreateCatalogItemRequest.serialize,
                response_deserializer=catalog.CatalogItem.deserialize,
            )
        return self._stubs["create_catalog_item"]

    @property
    def get_catalog_item(
        self
    ) -> Callable[[catalog_service.GetCatalogItemRequest], catalog.CatalogItem]:
        r"""Return a callable for the get catalog item method over gRPC.

        Gets a specific catalog item.

        Returns:
            Callable[[~.GetCatalogItemRequest],
                    ~.CatalogItem]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_catalog_item" not in self._stubs:
            self._stubs["get_catalog_item"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/GetCatalogItem",
                request_serializer=catalog_service.GetCatalogItemRequest.serialize,
                response_deserializer=catalog.CatalogItem.deserialize,
            )
        return self._stubs["get_catalog_item"]

    @property
    def list_catalog_items(
        self
    ) -> Callable[
        [catalog_service.ListCatalogItemsRequest],
        catalog_service.ListCatalogItemsResponse,
    ]:
        r"""Return a callable for the list catalog items method over gRPC.

        Gets a list of catalog items.

        Returns:
            Callable[[~.ListCatalogItemsRequest],
                    ~.ListCatalogItemsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_catalog_items" not in self._stubs:
            self._stubs["list_catalog_items"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/ListCatalogItems",
                request_serializer=catalog_service.ListCatalogItemsRequest.serialize,
                response_deserializer=catalog_service.ListCatalogItemsResponse.deserialize,
            )
        return self._stubs["list_catalog_items"]

    @property
    def update_catalog_item(
        self
    ) -> Callable[[catalog_service.UpdateCatalogItemRequest], catalog.CatalogItem]:
        r"""Return a callable for the update catalog item method over gRPC.

        Updates a catalog item. Partial updating is
        supported. Non-existing items will be created.

        Returns:
            Callable[[~.UpdateCatalogItemRequest],
                    ~.CatalogItem]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_catalog_item" not in self._stubs:
            self._stubs["update_catalog_item"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/UpdateCatalogItem",
                request_serializer=catalog_service.UpdateCatalogItemRequest.serialize,
                response_deserializer=catalog.CatalogItem.deserialize,
            )
        return self._stubs["update_catalog_item"]

    @property
    def delete_catalog_item(
        self
    ) -> Callable[[catalog_service.DeleteCatalogItemRequest], empty.Empty]:
        r"""Return a callable for the delete catalog item method over gRPC.

        Deletes a catalog item.

        Returns:
            Callable[[~.DeleteCatalogItemRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_catalog_item" not in self._stubs:
            self._stubs["delete_catalog_item"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/DeleteCatalogItem",
                request_serializer=catalog_service.DeleteCatalogItemRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_catalog_item"]

    @property
    def import_catalog_items(
        self
    ) -> Callable[[import_.ImportCatalogItemsRequest], operations.Operation]:
        r"""Return a callable for the import catalog items method over gRPC.

        Bulk import of multiple catalog items. Request
        processing may be synchronous. No partial updating
        supported. Non-existing items will be created.

        Operation.response is of type ImportResponse. Note that
        it is possible for a subset of the items to be
        successfully updated.

        Returns:
            Callable[[~.ImportCatalogItemsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_catalog_items" not in self._stubs:
            self._stubs["import_catalog_items"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.CatalogService/ImportCatalogItems",
                request_serializer=import_.ImportCatalogItemsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["import_catalog_items"]


__all__ = ("CatalogServiceGrpcTransport",)
