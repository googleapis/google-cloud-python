# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.network_management_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.network_management_v1.services.reachability_service import pagers
from google.cloud.network_management_v1.types import connectivity_test, reachability

from .client import ReachabilityServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ReachabilityServiceTransport
from .transports.grpc_asyncio import ReachabilityServiceGrpcAsyncIOTransport


class ReachabilityServiceAsyncClient:
    """The Reachability service in the Google Cloud Network
    Management API provides services that analyze the reachability
    within a single Google Virtual Private Cloud (VPC) network,
    between peered VPC networks, between VPC and on-premises
    networks, or between VPC networks and internet hosts. A
    reachability analysis is based on Google Cloud network
    configurations.

    You can use the analysis results to verify these configurations
    and to troubleshoot connectivity issues.
    """

    _client: ReachabilityServiceClient

    DEFAULT_ENDPOINT = ReachabilityServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ReachabilityServiceClient.DEFAULT_MTLS_ENDPOINT

    connectivity_test_path = staticmethod(
        ReachabilityServiceClient.connectivity_test_path
    )
    parse_connectivity_test_path = staticmethod(
        ReachabilityServiceClient.parse_connectivity_test_path
    )
    common_billing_account_path = staticmethod(
        ReachabilityServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ReachabilityServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ReachabilityServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ReachabilityServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ReachabilityServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ReachabilityServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ReachabilityServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ReachabilityServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ReachabilityServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ReachabilityServiceClient.parse_common_location_path
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
            ReachabilityServiceAsyncClient: The constructed client.
        """
        return ReachabilityServiceClient.from_service_account_info.__func__(ReachabilityServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ReachabilityServiceAsyncClient: The constructed client.
        """
        return ReachabilityServiceClient.from_service_account_file.__func__(ReachabilityServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        default mTLS endpoint; if the environment variable is "never", use the default API
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
        return ReachabilityServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ReachabilityServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ReachabilityServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ReachabilityServiceClient).get_transport_class,
        type(ReachabilityServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ReachabilityServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the reachability service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ReachabilityServiceTransport]): The
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
        self._client = ReachabilityServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_connectivity_tests(
        self,
        request: Optional[
            Union[reachability.ListConnectivityTestsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConnectivityTestsAsyncPager:
        r"""Lists all Connectivity Tests owned by a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_list_connectivity_tests():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                request = network_management_v1.ListConnectivityTestsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_connectivity_tests(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.ListConnectivityTestsRequest, dict]]):
                The request object. Request for the ``ListConnectivityTests`` method.
            parent (:class:`str`):
                Required. The parent resource of the Connectivity Tests:
                ``projects/{project_id}/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_management_v1.services.reachability_service.pagers.ListConnectivityTestsAsyncPager:
                Response for the ListConnectivityTests method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reachability.ListConnectivityTestsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_connectivity_tests,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListConnectivityTestsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_connectivity_test(
        self,
        request: Optional[Union[reachability.GetConnectivityTestRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> connectivity_test.ConnectivityTest:
        r"""Gets the details of a specific Connectivity Test.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_get_connectivity_test():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                request = network_management_v1.GetConnectivityTestRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_connectivity_test(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.GetConnectivityTestRequest, dict]]):
                The request object. Request for the ``GetConnectivityTest`` method.
            name (:class:`str`):
                Required. ``ConnectivityTest`` resource name using the
                form:
                ``projects/{project_id}/locations/global/connectivityTests/{test_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_management_v1.types.ConnectivityTest:
                A Connectivity Test for a network
                reachability analysis.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reachability.GetConnectivityTestRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_connectivity_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_connectivity_test(
        self,
        request: Optional[
            Union[reachability.CreateConnectivityTestRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        test_id: Optional[str] = None,
        resource: Optional[connectivity_test.ConnectivityTest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Connectivity Test. After you create a test, the
        reachability analysis is performed as part of the long running
        operation, which completes when the analysis completes.

        If the endpoint specifications in ``ConnectivityTest`` are
        invalid (for example, containing non-existent resources in the
        network, or you don't have read permissions to the network
        configurations of listed projects), then the reachability result
        returns a value of ``UNKNOWN``.

        If the endpoint specifications in ``ConnectivityTest`` are
        incomplete, the reachability result returns a value of
        AMBIGUOUS. For more information, see the Connectivity Test
        documentation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_create_connectivity_test():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                resource = network_management_v1.ConnectivityTest()
                resource.name = "name_value"

                request = network_management_v1.CreateConnectivityTestRequest(
                    parent="parent_value",
                    test_id="test_id_value",
                    resource=resource,
                )

                # Make the request
                operation = client.create_connectivity_test(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.CreateConnectivityTestRequest, dict]]):
                The request object. Request for the ``CreateConnectivityTest`` method.
            parent (:class:`str`):
                Required. The parent resource of the Connectivity Test
                to create: ``projects/{project_id}/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            test_id (:class:`str`):
                Required. The logical name of the Connectivity Test in
                your project with the following restrictions:

                -  Must contain only lowercase letters, numbers, and
                   hyphens.
                -  Must start with a letter.
                -  Must be between 1-40 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the customer project

                This corresponds to the ``test_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.network_management_v1.types.ConnectivityTest`):
                Required. A ``ConnectivityTest`` resource
                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.network_management_v1.types.ConnectivityTest`
                A Connectivity Test for a network reachability analysis.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, test_id, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reachability.CreateConnectivityTestRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if test_id is not None:
            request.test_id = test_id
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_connectivity_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            connectivity_test.ConnectivityTest,
            metadata_type=reachability.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_connectivity_test(
        self,
        request: Optional[
            Union[reachability.UpdateConnectivityTestRequest, dict]
        ] = None,
        *,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        resource: Optional[connectivity_test.ConnectivityTest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the configuration of an existing ``ConnectivityTest``.
        After you update a test, the reachability analysis is performed
        as part of the long running operation, which completes when the
        analysis completes. The Reachability state in the test resource
        is updated with the new result.

        If the endpoint specifications in ``ConnectivityTest`` are
        invalid (for example, they contain non-existent resources in the
        network, or the user does not have read permissions to the
        network configurations of listed projects), then the
        reachability result returns a value of UNKNOWN.

        If the endpoint specifications in ``ConnectivityTest`` are
        incomplete, the reachability result returns a value of
        ``AMBIGUOUS``. See the documentation in ``ConnectivityTest`` for
        for more details.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_update_connectivity_test():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                resource = network_management_v1.ConnectivityTest()
                resource.name = "name_value"

                request = network_management_v1.UpdateConnectivityTestRequest(
                    resource=resource,
                )

                # Make the request
                operation = client.update_connectivity_test(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.UpdateConnectivityTestRequest, dict]]):
                The request object. Request for the ``UpdateConnectivityTest`` method.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.
                At least one path must be supplied in
                this field.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.network_management_v1.types.ConnectivityTest`):
                Required. Only fields specified in update_mask are
                updated.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.network_management_v1.types.ConnectivityTest`
                A Connectivity Test for a network reachability analysis.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reachability.UpdateConnectivityTestRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_connectivity_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource.name", request.resource.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            connectivity_test.ConnectivityTest,
            metadata_type=reachability.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def rerun_connectivity_test(
        self,
        request: Optional[
            Union[reachability.RerunConnectivityTestRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Rerun an existing ``ConnectivityTest``. After the user triggers
        the rerun, the reachability analysis is performed as part of the
        long running operation, which completes when the analysis
        completes.

        Even though the test configuration remains the same, the
        reachability result may change due to underlying network
        configuration changes.

        If the endpoint specifications in ``ConnectivityTest`` become
        invalid (for example, specified resources are deleted in the
        network, or you lost read permissions to the network
        configurations of listed projects), then the reachability result
        returns a value of ``UNKNOWN``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_rerun_connectivity_test():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                request = network_management_v1.RerunConnectivityTestRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.rerun_connectivity_test(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.RerunConnectivityTestRequest, dict]]):
                The request object. Request for the ``RerunConnectivityTest`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.network_management_v1.types.ConnectivityTest`
                A Connectivity Test for a network reachability analysis.

        """
        # Create or coerce a protobuf request object.
        request = reachability.RerunConnectivityTestRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rerun_connectivity_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            connectivity_test.ConnectivityTest,
            metadata_type=reachability.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_connectivity_test(
        self,
        request: Optional[
            Union[reachability.DeleteConnectivityTestRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a specific ``ConnectivityTest``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import network_management_v1

            async def sample_delete_connectivity_test():
                # Create a client
                client = network_management_v1.ReachabilityServiceAsyncClient()

                # Initialize request argument(s)
                request = network_management_v1.DeleteConnectivityTestRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_connectivity_test(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.network_management_v1.types.DeleteConnectivityTestRequest, dict]]):
                The request object. Request for the ``DeleteConnectivityTest`` method.
            name (:class:`str`):
                Required. Connectivity Test resource name using the
                form:
                ``projects/{project_id}/locations/global/connectivityTests/{test_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reachability.DeleteConnectivityTestRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_connectivity_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=reachability.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "ReachabilityServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ReachabilityServiceAsyncClient",)
