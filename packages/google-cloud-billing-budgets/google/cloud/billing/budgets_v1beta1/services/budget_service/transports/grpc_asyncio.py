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

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.billing.budgets_v1beta1.types import budget_model
from google.cloud.billing.budgets_v1beta1.types import budget_service
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import BudgetServiceTransport
from .grpc import BudgetServiceGrpcTransport


class BudgetServiceGrpcAsyncIOTransport(BudgetServiceTransport):
    """gRPC AsyncIO backend transport for BudgetService.

    BudgetService stores Cloud Billing budgets, which define a
    budget plan and rules to execute as we track spend against that
    plan.

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
        host: str = "billingbudgets.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        **kwargs
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            **kwargs
        )

    def __init__(
        self,
        *,
        host: str = "billingbudgets.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None
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
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_budget(
        self,
    ) -> Callable[[budget_service.CreateBudgetRequest], Awaitable[budget_model.Budget]]:
        r"""Return a callable for the create budget method over gRPC.

        Creates a new budget. See
        <a href="https://cloud.google.com/billing/quotas">Quotas
        and limits</a> for more information on the limits of the
        number of budgets you can create.

        Returns:
            Callable[[~.CreateBudgetRequest],
                    Awaitable[~.Budget]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_budget" not in self._stubs:
            self._stubs["create_budget"] = self.grpc_channel.unary_unary(
                "/google.cloud.billing.budgets.v1beta1.BudgetService/CreateBudget",
                request_serializer=budget_service.CreateBudgetRequest.serialize,
                response_deserializer=budget_model.Budget.deserialize,
            )
        return self._stubs["create_budget"]

    @property
    def update_budget(
        self,
    ) -> Callable[[budget_service.UpdateBudgetRequest], Awaitable[budget_model.Budget]]:
        r"""Return a callable for the update budget method over gRPC.

        Updates a budget and returns the updated budget.
        WARNING: There are some fields exposed on the Google
        Cloud Console that aren't available on this API. Budget
        fields that are not exposed in this API will not be
        changed by this method.

        Returns:
            Callable[[~.UpdateBudgetRequest],
                    Awaitable[~.Budget]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_budget" not in self._stubs:
            self._stubs["update_budget"] = self.grpc_channel.unary_unary(
                "/google.cloud.billing.budgets.v1beta1.BudgetService/UpdateBudget",
                request_serializer=budget_service.UpdateBudgetRequest.serialize,
                response_deserializer=budget_model.Budget.deserialize,
            )
        return self._stubs["update_budget"]

    @property
    def get_budget(
        self,
    ) -> Callable[[budget_service.GetBudgetRequest], Awaitable[budget_model.Budget]]:
        r"""Return a callable for the get budget method over gRPC.

        Returns a budget.
        WARNING: There are some fields exposed on the Google
        Cloud Console that aren't available on this API. When
        reading from the API, you will not see these fields in
        the return value, though they may have been set in the
        Cloud Console.

        Returns:
            Callable[[~.GetBudgetRequest],
                    Awaitable[~.Budget]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_budget" not in self._stubs:
            self._stubs["get_budget"] = self.grpc_channel.unary_unary(
                "/google.cloud.billing.budgets.v1beta1.BudgetService/GetBudget",
                request_serializer=budget_service.GetBudgetRequest.serialize,
                response_deserializer=budget_model.Budget.deserialize,
            )
        return self._stubs["get_budget"]

    @property
    def list_budgets(
        self,
    ) -> Callable[
        [budget_service.ListBudgetsRequest],
        Awaitable[budget_service.ListBudgetsResponse],
    ]:
        r"""Return a callable for the list budgets method over gRPC.

        Returns a list of budgets for a billing account.
        WARNING: There are some fields exposed on the Google
        Cloud Console that aren't available on this API. When
        reading from the API, you will not see these fields in
        the return value, though they may have been set in the
        Cloud Console.

        Returns:
            Callable[[~.ListBudgetsRequest],
                    Awaitable[~.ListBudgetsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_budgets" not in self._stubs:
            self._stubs["list_budgets"] = self.grpc_channel.unary_unary(
                "/google.cloud.billing.budgets.v1beta1.BudgetService/ListBudgets",
                request_serializer=budget_service.ListBudgetsRequest.serialize,
                response_deserializer=budget_service.ListBudgetsResponse.deserialize,
            )
        return self._stubs["list_budgets"]

    @property
    def delete_budget(
        self,
    ) -> Callable[[budget_service.DeleteBudgetRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete budget method over gRPC.

        Deletes a budget. Returns successfully if already
        deleted.

        Returns:
            Callable[[~.DeleteBudgetRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_budget" not in self._stubs:
            self._stubs["delete_budget"] = self.grpc_channel.unary_unary(
                "/google.cloud.billing.budgets.v1beta1.BudgetService/DeleteBudget",
                request_serializer=budget_service.DeleteBudgetRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_budget"]


__all__ = ("BudgetServiceGrpcAsyncIOTransport",)
