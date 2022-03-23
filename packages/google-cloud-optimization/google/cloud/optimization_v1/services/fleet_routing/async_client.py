# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from collections import OrderedDict
import functools
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.optimization_v1.types import async_model
from google.cloud.optimization_v1.types import fleet_routing
from .transports.base import FleetRoutingTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import FleetRoutingGrpcAsyncIOTransport
from .client import FleetRoutingClient


class FleetRoutingAsyncClient:
    """A service for optimizing vehicle tours.

    Validity of certain types of fields:

    -  ``google.protobuf.Timestamp``

       -  Times are in Unix time: seconds since
          1970-01-01T00:00:00+00:00.
       -  seconds must be in [0, 253402300799], i.e. in
          [1970-01-01T00:00:00+00:00, 9999-12-31T23:59:59+00:00].
       -  nanos must be unset or set to 0.

    -  ``google.protobuf.Duration``

       -  seconds must be in [0, 253402300799], i.e. in
          [1970-01-01T00:00:00+00:00, 9999-12-31T23:59:59+00:00].
       -  nanos must be unset or set to 0.

    -  ``google.type.LatLng``

       -  latitude must be in [-90.0, 90.0].
       -  longitude must be in [-180.0, 180.0].
       -  at least one of latitude and longitude must be non-zero.
    """

    _client: FleetRoutingClient

    DEFAULT_ENDPOINT = FleetRoutingClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = FleetRoutingClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        FleetRoutingClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        FleetRoutingClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(FleetRoutingClient.common_folder_path)
    parse_common_folder_path = staticmethod(FleetRoutingClient.parse_common_folder_path)
    common_organization_path = staticmethod(FleetRoutingClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        FleetRoutingClient.parse_common_organization_path
    )
    common_project_path = staticmethod(FleetRoutingClient.common_project_path)
    parse_common_project_path = staticmethod(
        FleetRoutingClient.parse_common_project_path
    )
    common_location_path = staticmethod(FleetRoutingClient.common_location_path)
    parse_common_location_path = staticmethod(
        FleetRoutingClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FleetRoutingAsyncClient: The constructed client.
        """
        return FleetRoutingClient.from_service_account_info.__func__(FleetRoutingAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FleetRoutingAsyncClient: The constructed client.
        """
        return FleetRoutingClient.from_service_account_file.__func__(FleetRoutingAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return FleetRoutingClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> FleetRoutingTransport:
        """Returns the transport used by the client instance.

        Returns:
            FleetRoutingTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(FleetRoutingClient).get_transport_class, type(FleetRoutingClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, FleetRoutingTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the fleet routing client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FleetRoutingTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = FleetRoutingClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def optimize_tours(
        self,
        request: Union[fleet_routing.OptimizeToursRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> fleet_routing.OptimizeToursResponse:
        r"""Sends an ``OptimizeToursRequest`` containing a ``ShipmentModel``
        and returns an ``OptimizeToursResponse`` containing
        ``ShipmentRoute``\ s, which are a set of routes to be performed
        by vehicles minimizing the overall cost.

        A ``ShipmentModel`` model consists mainly of ``Shipment``\ s
        that need to be carried out and ``Vehicle``\ s that can be used
        to transport the ``Shipment``\ s. The ``ShipmentRoute``\ s
        assign ``Shipment``\ s to ``Vehicle``\ s. More specifically,
        they assign a series of ``Visit``\ s to each vehicle, where a
        ``Visit`` corresponds to a ``VisitRequest``, which is a pickup
        or delivery for a ``Shipment``.

        The goal is to provide an assignment of ``ShipmentRoute``\ s to
        ``Vehicle``\ s that minimizes the total cost where cost has many
        components defined in the ``ShipmentModel``.


        .. code-block:: python

            from google.cloud import optimization_v1

            def sample_optimize_tours():
                # Create a client
                client = optimization_v1.FleetRoutingClient()

                # Initialize request argument(s)
                request = optimization_v1.OptimizeToursRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.optimize_tours(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.optimization_v1.types.OptimizeToursRequest, dict]):
                The request object. Request to be given to a tour
                optimization solver which defines the shipment model to
                solve as well as optimization parameters.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.optimization_v1.types.OptimizeToursResponse:
                Response after solving a tour
                optimization problem containing the
                routes followed by each vehicle, the
                shipments which have been skipped and
                the overall cost of the solution.

        """
        # Create or coerce a protobuf request object.
        request = fleet_routing.OptimizeToursRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.optimize_tours,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=3600.0,
            ),
            default_timeout=3600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def batch_optimize_tours(
        self,
        request: Union[fleet_routing.BatchOptimizeToursRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Optimizes vehicle tours for one or more ``OptimizeToursRequest``
        messages as a batch.

        This method is a Long Running Operation (LRO). The inputs for
        optimization (``OptimizeToursRequest`` messages) and outputs
        (``OptimizeToursResponse`` messages) are read/written from/to
        Cloud Storage in user-specified format. Like the
        ``OptimizeTours`` method, each ``OptimizeToursRequest`` contains
        a ``ShipmentModel`` and returns an ``OptimizeToursResponse``
        containing ``ShipmentRoute``\ s, which are a set of routes to be
        performed by vehicles minimizing the overall cost.


        .. code-block:: python

            from google.cloud import optimization_v1

            def sample_batch_optimize_tours():
                # Create a client
                client = optimization_v1.FleetRoutingClient()

                # Initialize request argument(s)
                model_configs = optimization_v1.AsyncModelConfig()
                model_configs.input_config.gcs_source.uri = "uri_value"
                model_configs.output_config.gcs_destination.uri = "uri_value"

                request = optimization_v1.BatchOptimizeToursRequest(
                    parent="parent_value",
                    model_configs=model_configs,
                )

                # Make the request
                operation = client.batch_optimize_tours(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.optimization_v1.types.BatchOptimizeToursRequest, dict]):
                The request object. Request to batch optimize tours as
                an asynchronous operation. Each input file should
                contain one `OptimizeToursRequest`, and each output file
                will contain one `OptimizeToursResponse`. The request
                contains information to read/write and parse the files.
                All the input and output files should be under the same
                project.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.optimization_v1.types.BatchOptimizeToursResponse` Response to a BatchOptimizeToursRequest. This is returned in
                   the LRO Operation after the operation is complete.

        """
        # Create or coerce a protobuf request object.
        request = fleet_routing.BatchOptimizeToursRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_optimize_tours,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            fleet_routing.BatchOptimizeToursResponse,
            metadata_type=async_model.AsyncModelMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-optimization",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FleetRoutingAsyncClient",)
