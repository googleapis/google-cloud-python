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

from google.cloud.apigee_registry_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api import httpbody_pb2  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.apigee_registry_v1.services.registry import pagers
from google.cloud.apigee_registry_v1.types import registry_models, registry_service

from .client import RegistryClient
from .transports.base import DEFAULT_CLIENT_INFO, RegistryTransport
from .transports.grpc_asyncio import RegistryGrpcAsyncIOTransport


class RegistryAsyncClient:
    """The Registry service allows teams to manage descriptions of
    APIs.
    """

    _client: RegistryClient

    DEFAULT_ENDPOINT = RegistryClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = RegistryClient.DEFAULT_MTLS_ENDPOINT

    api_path = staticmethod(RegistryClient.api_path)
    parse_api_path = staticmethod(RegistryClient.parse_api_path)
    api_deployment_path = staticmethod(RegistryClient.api_deployment_path)
    parse_api_deployment_path = staticmethod(RegistryClient.parse_api_deployment_path)
    api_spec_path = staticmethod(RegistryClient.api_spec_path)
    parse_api_spec_path = staticmethod(RegistryClient.parse_api_spec_path)
    api_version_path = staticmethod(RegistryClient.api_version_path)
    parse_api_version_path = staticmethod(RegistryClient.parse_api_version_path)
    artifact_path = staticmethod(RegistryClient.artifact_path)
    parse_artifact_path = staticmethod(RegistryClient.parse_artifact_path)
    common_billing_account_path = staticmethod(
        RegistryClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        RegistryClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(RegistryClient.common_folder_path)
    parse_common_folder_path = staticmethod(RegistryClient.parse_common_folder_path)
    common_organization_path = staticmethod(RegistryClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        RegistryClient.parse_common_organization_path
    )
    common_project_path = staticmethod(RegistryClient.common_project_path)
    parse_common_project_path = staticmethod(RegistryClient.parse_common_project_path)
    common_location_path = staticmethod(RegistryClient.common_location_path)
    parse_common_location_path = staticmethod(RegistryClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            RegistryAsyncClient: The constructed client.
        """
        return RegistryClient.from_service_account_info.__func__(RegistryAsyncClient, info, *args, **kwargs)  # type: ignore

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
            RegistryAsyncClient: The constructed client.
        """
        return RegistryClient.from_service_account_file.__func__(RegistryAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return RegistryClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> RegistryTransport:
        """Returns the transport used by the client instance.

        Returns:
            RegistryTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(RegistryClient).get_transport_class, type(RegistryClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, RegistryTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the registry client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RegistryTransport]): The
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
        self._client = RegistryClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_apis(
        self,
        request: Optional[Union[registry_service.ListApisRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApisAsyncPager:
        r"""Returns matching APIs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_apis():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApisRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_apis(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApisRequest, dict]]):
                The request object. Request message for ListApis.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                APIs. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApisAsyncPager:
                Response message for ListApis.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = registry_service.ListApisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_apis,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListApisAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api(
        self,
        request: Optional[Union[registry_service.GetApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Api:
        r"""Returns a specified API.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_api():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetApiRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetApiRequest, dict]]):
                The request object. Request message for GetApi.
            name (:class:`str`):
                Required. The name of the API to retrieve. Format:
                ``projects/*/locations/*/apis/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Api:
                A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

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

        request = registry_service.GetApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def create_api(
        self,
        request: Optional[Union[registry_service.CreateApiRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        api: Optional[registry_models.Api] = None,
        api_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Api:
        r"""Creates a specified API.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_create_api():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.CreateApiRequest(
                    parent="parent_value",
                    api_id="api_id_value",
                )

                # Make the request
                response = await client.create_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.CreateApiRequest, dict]]):
                The request object. Request message for CreateApi.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                APIs. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api (:class:`google.cloud.apigee_registry_v1.types.Api`):
                Required. The API to create.
                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_id (:class:`str`):
                Required. The ID to use for the API, which will become
                the final component of the API's resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                Following AIP-162, IDs must not have the form of a UUID.

                This corresponds to the ``api_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Api:
                A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api, api_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.CreateApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api is not None:
            request.api = api
        if api_id is not None:
            request.api_id = api_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_api(
        self,
        request: Optional[Union[registry_service.UpdateApiRequest, dict]] = None,
        *,
        api: Optional[registry_models.Api] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Api:
        r"""Used to modify a specified API.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_update_api():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.UpdateApiRequest(
                )

                # Make the request
                response = await client.update_api(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.UpdateApiRequest, dict]]):
                The request object. Request message for UpdateApi.
            api (:class:`google.cloud.apigee_registry_v1.types.Api`):
                Required. The API to update.

                The ``name`` field is used to identify the API to
                update. Format: ``projects/*/locations/*/apis/*``

                This corresponds to the ``api`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated. If omitted, all fields
                are updated that are set in the request message (fields
                set to default values are ignored). If an asterisk "*"
                is specified, all fields are updated, including fields
                that are unspecified/default in the request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Api:
                A top-level description of an API.
                Produced by producers and are
                commitments to provide services.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.UpdateApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api is not None:
            request.api = api
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("api.name", request.api.name),)),
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

    async def delete_api(
        self,
        request: Optional[Union[registry_service.DeleteApiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a specified API and all of the resources that
        it owns.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_api(request=request)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiRequest, dict]]):
                The request object. Request message for DeleteApi.
            name (:class:`str`):
                Required. The name of the API to delete. Format:
                ``projects/*/locations/*/apis/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = registry_service.DeleteApiRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_api_versions(
        self,
        request: Optional[Union[registry_service.ListApiVersionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiVersionsAsyncPager:
        r"""Returns matching versions.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_api_versions():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApiVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_api_versions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApiVersionsRequest, dict]]):
                The request object. Request message for ListApiVersions.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                versions. Format: ``projects/*/locations/*/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApiVersionsAsyncPager:
                Response message for ListApiVersions.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = registry_service.ListApiVersionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_versions,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListApiVersionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api_version(
        self,
        request: Optional[Union[registry_service.GetApiVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiVersion:
        r"""Returns a specified version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_api_version():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetApiVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_api_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetApiVersionRequest, dict]]):
                The request object. Request message for GetApiVersion.
            name (:class:`str`):
                Required. The name of the version to retrieve. Format:
                ``projects/*/locations/*/apis/*/versions/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiVersion:
                Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

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

        request = registry_service.GetApiVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api_version,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def create_api_version(
        self,
        request: Optional[Union[registry_service.CreateApiVersionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        api_version: Optional[registry_models.ApiVersion] = None,
        api_version_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiVersion:
        r"""Creates a specified version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_create_api_version():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.CreateApiVersionRequest(
                    parent="parent_value",
                    api_version_id="api_version_id_value",
                )

                # Make the request
                response = await client.create_api_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.CreateApiVersionRequest, dict]]):
                The request object. Request message for CreateApiVersion.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                versions. Format: ``projects/*/locations/*/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_version (:class:`google.cloud.apigee_registry_v1.types.ApiVersion`):
                Required. The version to create.
                This corresponds to the ``api_version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_version_id (:class:`str`):
                Required. The ID to use for the version, which will
                become the final component of the version's resource
                name.

                This value should be 1-63 characters, and valid
                characters are /[a-z][0-9]-/.

                Following AIP-162, IDs must not have the form of a UUID.

                This corresponds to the ``api_version_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiVersion:
                Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api_version, api_version_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.CreateApiVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api_version is not None:
            request.api_version = api_version
        if api_version_id is not None:
            request.api_version_id = api_version_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api_version,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_api_version(
        self,
        request: Optional[Union[registry_service.UpdateApiVersionRequest, dict]] = None,
        *,
        api_version: Optional[registry_models.ApiVersion] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiVersion:
        r"""Used to modify a specified version.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_update_api_version():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.UpdateApiVersionRequest(
                )

                # Make the request
                response = await client.update_api_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.UpdateApiVersionRequest, dict]]):
                The request object. Request message for UpdateApiVersion.
            api_version (:class:`google.cloud.apigee_registry_v1.types.ApiVersion`):
                Required. The version to update.

                The ``name`` field is used to identify the version to
                update. Format:
                ``projects/*/locations/*/apis/*/versions/*``

                This corresponds to the ``api_version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated. If omitted, all fields
                are updated that are set in the request message (fields
                set to default values are ignored). If an asterisk "*"
                is specified, all fields are updated, including fields
                that are unspecified/default in the request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiVersion:
                Describes a particular version of an
                API. ApiVersions are what consumers
                actually use.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api_version, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.UpdateApiVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api_version is not None:
            request.api_version = api_version
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api_version,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("api_version.name", request.api_version.name),)
            ),
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

    async def delete_api_version(
        self,
        request: Optional[Union[registry_service.DeleteApiVersionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a specified version and all of the resources
        that it owns.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api_version():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiVersionRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_api_version(request=request)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiVersionRequest, dict]]):
                The request object. Request message for DeleteApiVersion.
            name (:class:`str`):
                Required. The name of the version to delete. Format:
                ``projects/*/locations/*/apis/*/versions/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = registry_service.DeleteApiVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_version,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_api_specs(
        self,
        request: Optional[Union[registry_service.ListApiSpecsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiSpecsAsyncPager:
        r"""Returns matching specs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_api_specs():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApiSpecsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_api_specs(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApiSpecsRequest, dict]]):
                The request object. Request message for ListApiSpecs.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                specs. Format:
                ``projects/*/locations/*/apis/*/versions/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApiSpecsAsyncPager:
                Response message for ListApiSpecs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = registry_service.ListApiSpecsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_specs,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListApiSpecsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api_spec(
        self,
        request: Optional[Union[registry_service.GetApiSpecRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Returns a specified spec.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_api_spec():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetApiSpecRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_api_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetApiSpecRequest, dict]]):
                The request object. Request message for GetApiSpec.
            name (:class:`str`):
                Required. The name of the spec to retrieve. Format:
                ``projects/*/locations/*/apis/*/versions/*/specs/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

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

        request = registry_service.GetApiSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api_spec,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def get_api_spec_contents(
        self,
        request: Optional[
            Union[registry_service.GetApiSpecContentsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> httpbody_pb2.HttpBody:
        r"""Returns the contents of a specified spec. If specs are stored
        with GZip compression, the default behavior is to return the
        spec uncompressed (the mime_type response field indicates the
        exact format returned).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_api_spec_contents():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetApiSpecContentsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_api_spec_contents(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetApiSpecContentsRequest, dict]]):
                The request object. Request message for
                GetApiSpecContents.
            name (:class:`str`):
                Required. The name of the spec whose contents should be
                retrieved. Format:
                ``projects/*/locations/*/apis/*/versions/*/specs/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.httpbody_pb2.HttpBody:
                Message that represents an arbitrary HTTP body. It should only be used for
                   payload formats that can't be represented as JSON,
                   such as raw binary or an HTML page.

                   This message can be used both in streaming and
                   non-streaming API methods in the request as well as
                   the response.

                   It can be used as a top-level request field, which is
                   convenient if one wants to extract parameters from
                   either the URL or HTTP template into the request
                   fields and also want access to the raw HTTP body.

                   Example:

                      message GetResourceRequest {
                         // A unique request id. string request_id = 1;

                         // The raw HTTP body is bound to this field.
                         google.api.HttpBody http_body = 2;

                      }

                      service ResourceService {
                         rpc GetResource(GetResourceRequest)
                            returns (google.api.HttpBody);

                         rpc UpdateResource(google.api.HttpBody)
                            returns (google.protobuf.Empty);

                      }

                   Example with streaming methods:

                      service CaldavService {
                         rpc GetCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                         rpc UpdateCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                      }

                   Use of this type only changes how the request and
                   response bodies are handled, all other features will
                   continue to work unchanged.

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

        request = registry_service.GetApiSpecContentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api_spec_contents,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def create_api_spec(
        self,
        request: Optional[Union[registry_service.CreateApiSpecRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        api_spec: Optional[registry_models.ApiSpec] = None,
        api_spec_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Creates a specified spec.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_create_api_spec():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.CreateApiSpecRequest(
                    parent="parent_value",
                    api_spec_id="api_spec_id_value",
                )

                # Make the request
                response = await client.create_api_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.CreateApiSpecRequest, dict]]):
                The request object. Request message for CreateApiSpec.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                specs. Format:
                ``projects/*/locations/*/apis/*/versions/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_spec (:class:`google.cloud.apigee_registry_v1.types.ApiSpec`):
                Required. The spec to create.
                This corresponds to the ``api_spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_spec_id (:class:`str`):
                Required. The ID to use for the spec, which will become
                the final component of the spec's resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                Following AIP-162, IDs must not have the form of a UUID.

                This corresponds to the ``api_spec_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api_spec, api_spec_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.CreateApiSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api_spec is not None:
            request.api_spec = api_spec
        if api_spec_id is not None:
            request.api_spec_id = api_spec_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api_spec,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_api_spec(
        self,
        request: Optional[Union[registry_service.UpdateApiSpecRequest, dict]] = None,
        *,
        api_spec: Optional[registry_models.ApiSpec] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Used to modify a specified spec.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_update_api_spec():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.UpdateApiSpecRequest(
                )

                # Make the request
                response = await client.update_api_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.UpdateApiSpecRequest, dict]]):
                The request object. Request message for UpdateApiSpec.
            api_spec (:class:`google.cloud.apigee_registry_v1.types.ApiSpec`):
                Required. The spec to update.

                The ``name`` field is used to identify the spec to
                update. Format:
                ``projects/*/locations/*/apis/*/versions/*/specs/*``

                This corresponds to the ``api_spec`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated. If omitted, all fields
                are updated that are set in the request message (fields
                set to default values are ignored). If an asterisk "*"
                is specified, all fields are updated, including fields
                that are unspecified/default in the request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api_spec, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.UpdateApiSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api_spec is not None:
            request.api_spec = api_spec
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api_spec,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("api_spec.name", request.api_spec.name),)
            ),
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

    async def delete_api_spec(
        self,
        request: Optional[Union[registry_service.DeleteApiSpecRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a specified spec, all revisions, and all
        child resources (e.g., artifacts).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api_spec():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiSpecRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_api_spec(request=request)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiSpecRequest, dict]]):
                The request object. Request message for DeleteApiSpec.
            name (:class:`str`):
                Required. The name of the spec to delete. Format:
                ``projects/*/locations/*/apis/*/versions/*/specs/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = registry_service.DeleteApiSpecRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_spec,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def tag_api_spec_revision(
        self,
        request: Optional[
            Union[registry_service.TagApiSpecRevisionRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Adds a tag to a specified revision of a spec.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_tag_api_spec_revision():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.TagApiSpecRevisionRequest(
                    name="name_value",
                    tag="tag_value",
                )

                # Make the request
                response = await client.tag_api_spec_revision(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.TagApiSpecRevisionRequest, dict]]):
                The request object. Request message for
                TagApiSpecRevision.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.TagApiSpecRevisionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.tag_api_spec_revision,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def list_api_spec_revisions(
        self,
        request: Optional[
            Union[registry_service.ListApiSpecRevisionsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiSpecRevisionsAsyncPager:
        r"""Lists all revisions of a spec.
        Revisions are returned in descending order of revision
        creation time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_api_spec_revisions():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApiSpecRevisionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.list_api_spec_revisions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApiSpecRevisionsRequest, dict]]):
                The request object. Request message for
                ListApiSpecRevisions.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApiSpecRevisionsAsyncPager:
                Response message for
                ListApiSpecRevisionsResponse.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.ListApiSpecRevisionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_spec_revisions,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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
        response = pagers.ListApiSpecRevisionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def rollback_api_spec(
        self,
        request: Optional[Union[registry_service.RollbackApiSpecRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Sets the current revision to a specified prior
        revision. Note that this creates a new revision with a
        new revision ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_rollback_api_spec():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.RollbackApiSpecRequest(
                    name="name_value",
                    revision_id="revision_id_value",
                )

                # Make the request
                response = await client.rollback_api_spec(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.RollbackApiSpecRequest, dict]]):
                The request object. Request message for RollbackApiSpec.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.RollbackApiSpecRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rollback_api_spec,
            default_timeout=60.0,
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

    async def delete_api_spec_revision(
        self,
        request: Optional[
            Union[registry_service.DeleteApiSpecRevisionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiSpec:
        r"""Deletes a revision of a spec.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api_spec_revision():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiSpecRevisionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.delete_api_spec_revision(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiSpecRevisionRequest, dict]]):
                The request object. Request message for
                DeleteApiSpecRevision.
            name (:class:`str`):
                Required. The name of the spec revision to be deleted,
                with a revision ID explicitly included.

                Example:
                ``projects/sample/locations/global/apis/petstore/versions/1.0.0/specs/openapi.yaml@c7cfa2a8``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiSpec:
                Describes a version of an API in a
                structured way. ApiSpecs provide formal
                descriptions that consumers can use to
                use a version. ApiSpec resources are
                intended to be fully-resolved
                descriptions of an ApiVersion. When
                specs consist of multiple files, these
                should be bundled together (e.g., in a
                zip archive) and stored as a unit.
                Multiple specs can exist to provide
                representations in different API
                description formats. Synchronization of
                these representations would be provided
                by tooling and background services.

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

        request = registry_service.DeleteApiSpecRevisionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_spec_revision,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def list_api_deployments(
        self,
        request: Optional[
            Union[registry_service.ListApiDeploymentsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiDeploymentsAsyncPager:
        r"""Returns matching deployments.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_api_deployments():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApiDeploymentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_api_deployments(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApiDeploymentsRequest, dict]]):
                The request object. Request message for
                ListApiDeployments.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                deployments. Format: ``projects/*/locations/*/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApiDeploymentsAsyncPager:
                Response message for
                ListApiDeployments.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = registry_service.ListApiDeploymentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_deployments,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListApiDeploymentsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_api_deployment(
        self,
        request: Optional[Union[registry_service.GetApiDeploymentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Returns a specified deployment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_api_deployment():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetApiDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_api_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetApiDeploymentRequest, dict]]):
                The request object. Request message for GetApiDeployment.
            name (:class:`str`):
                Required. The name of the deployment to retrieve.
                Format: ``projects/*/locations/*/apis/*/deployments/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

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

        request = registry_service.GetApiDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_api_deployment,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def create_api_deployment(
        self,
        request: Optional[
            Union[registry_service.CreateApiDeploymentRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        api_deployment: Optional[registry_models.ApiDeployment] = None,
        api_deployment_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Creates a specified deployment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_create_api_deployment():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.CreateApiDeploymentRequest(
                    parent="parent_value",
                    api_deployment_id="api_deployment_id_value",
                )

                # Make the request
                response = await client.create_api_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.CreateApiDeploymentRequest, dict]]):
                The request object. Request message for
                CreateApiDeployment.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                deployments. Format: ``projects/*/locations/*/apis/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_deployment (:class:`google.cloud.apigee_registry_v1.types.ApiDeployment`):
                Required. The deployment to create.
                This corresponds to the ``api_deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            api_deployment_id (:class:`str`):
                Required. The ID to use for the deployment, which will
                become the final component of the deployment's resource
                name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                Following AIP-162, IDs must not have the form of a UUID.

                This corresponds to the ``api_deployment_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, api_deployment, api_deployment_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.CreateApiDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if api_deployment is not None:
            request.api_deployment = api_deployment
        if api_deployment_id is not None:
            request.api_deployment_id = api_deployment_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_api_deployment,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_api_deployment(
        self,
        request: Optional[
            Union[registry_service.UpdateApiDeploymentRequest, dict]
        ] = None,
        *,
        api_deployment: Optional[registry_models.ApiDeployment] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Used to modify a specified deployment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_update_api_deployment():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.UpdateApiDeploymentRequest(
                )

                # Make the request
                response = await client.update_api_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.UpdateApiDeploymentRequest, dict]]):
                The request object. Request message for
                UpdateApiDeployment.
            api_deployment (:class:`google.cloud.apigee_registry_v1.types.ApiDeployment`):
                Required. The deployment to update.

                The ``name`` field is used to identify the deployment to
                update. Format:
                ``projects/*/locations/*/apis/*/deployments/*``

                This corresponds to the ``api_deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated. If omitted, all fields
                are updated that are set in the request message (fields
                set to default values are ignored). If an asterisk "*"
                is specified, all fields are updated, including fields
                that are unspecified/default in the request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([api_deployment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.UpdateApiDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if api_deployment is not None:
            request.api_deployment = api_deployment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_api_deployment,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("api_deployment.name", request.api_deployment.name),)
            ),
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

    async def delete_api_deployment(
        self,
        request: Optional[
            Union[registry_service.DeleteApiDeploymentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a specified deployment, all revisions, and
        all child resources (e.g., artifacts).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api_deployment():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_api_deployment(request=request)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiDeploymentRequest, dict]]):
                The request object. Request message for
                DeleteApiDeployment.
            name (:class:`str`):
                Required. The name of the deployment to delete. Format:
                ``projects/*/locations/*/apis/*/deployments/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = registry_service.DeleteApiDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_deployment,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def tag_api_deployment_revision(
        self,
        request: Optional[
            Union[registry_service.TagApiDeploymentRevisionRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Adds a tag to a specified revision of a
        deployment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_tag_api_deployment_revision():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.TagApiDeploymentRevisionRequest(
                    name="name_value",
                    tag="tag_value",
                )

                # Make the request
                response = await client.tag_api_deployment_revision(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.TagApiDeploymentRevisionRequest, dict]]):
                The request object. Request message for
                TagApiDeploymentRevision.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.TagApiDeploymentRevisionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.tag_api_deployment_revision,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def list_api_deployment_revisions(
        self,
        request: Optional[
            Union[registry_service.ListApiDeploymentRevisionsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApiDeploymentRevisionsAsyncPager:
        r"""Lists all revisions of a deployment.
        Revisions are returned in descending order of revision
        creation time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_api_deployment_revisions():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListApiDeploymentRevisionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.list_api_deployment_revisions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListApiDeploymentRevisionsRequest, dict]]):
                The request object. Request message for
                ListApiDeploymentRevisions.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListApiDeploymentRevisionsAsyncPager:
                Response message for
                ListApiDeploymentRevisionsResponse.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.ListApiDeploymentRevisionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_api_deployment_revisions,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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
        response = pagers.ListApiDeploymentRevisionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def rollback_api_deployment(
        self,
        request: Optional[
            Union[registry_service.RollbackApiDeploymentRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Sets the current revision to a specified prior
        revision. Note that this creates a new revision with a
        new revision ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_rollback_api_deployment():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.RollbackApiDeploymentRequest(
                    name="name_value",
                    revision_id="revision_id_value",
                )

                # Make the request
                response = await client.rollback_api_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.RollbackApiDeploymentRequest, dict]]):
                The request object. Request message for
                RollbackApiDeployment.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

        """
        # Create or coerce a protobuf request object.
        request = registry_service.RollbackApiDeploymentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rollback_api_deployment,
            default_timeout=60.0,
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

    async def delete_api_deployment_revision(
        self,
        request: Optional[
            Union[registry_service.DeleteApiDeploymentRevisionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.ApiDeployment:
        r"""Deletes a revision of a deployment.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_api_deployment_revision():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteApiDeploymentRevisionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.delete_api_deployment_revision(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteApiDeploymentRevisionRequest, dict]]):
                The request object. Request message for
                DeleteApiDeploymentRevision.
            name (:class:`str`):
                Required. The name of the deployment revision to be
                deleted, with a revision ID explicitly included.

                Example:
                ``projects/sample/locations/global/apis/petstore/deployments/prod@c7cfa2a8``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.ApiDeployment:
                Describes a service running at
                particular address that provides a
                particular version of an API.
                ApiDeployments have revisions which
                correspond to different configurations
                of a single deployment in time. Revision
                identifiers should be updated whenever
                the served API spec or endpoint address
                changes.

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

        request = registry_service.DeleteApiDeploymentRevisionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_api_deployment_revision,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def list_artifacts(
        self,
        request: Optional[Union[registry_service.ListArtifactsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListArtifactsAsyncPager:
        r"""Returns matching artifacts.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_list_artifacts():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ListArtifactsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_artifacts(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ListArtifactsRequest, dict]]):
                The request object. Request message for ListArtifacts.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                artifacts. Format: ``{parent}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.services.registry.pagers.ListArtifactsAsyncPager:
                Response message for ListArtifacts.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = registry_service.ListArtifactsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_artifacts,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListArtifactsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_artifact(
        self,
        request: Optional[Union[registry_service.GetArtifactRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Artifact:
        r"""Returns a specified artifact.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_artifact():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetArtifactRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_artifact(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetArtifactRequest, dict]]):
                The request object. Request message for GetArtifact.
            name (:class:`str`):
                Required. The name of the artifact to retrieve. Format:
                ``{parent}/artifacts/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Artifact:
                Artifacts of resources. Artifacts are unique (single-value) per resource
                   and are used to store metadata that is too large or
                   numerous to be stored directly on the resource. Since
                   artifacts are stored separately from parent
                   resources, they should generally be used for metadata
                   that is needed infrequently, i.e., not for display in
                   primary views of the resource but perhaps displayed
                   or downloaded upon request. The ListArtifacts method
                   allows artifacts to be quickly enumerated and checked
                   for presence without downloading their
                   (potentially-large) contents.

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

        request = registry_service.GetArtifactRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_artifact,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def get_artifact_contents(
        self,
        request: Optional[
            Union[registry_service.GetArtifactContentsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> httpbody_pb2.HttpBody:
        r"""Returns the contents of a specified artifact. If artifacts are
        stored with GZip compression, the default behavior is to return
        the artifact uncompressed (the mime_type response field
        indicates the exact format returned).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_get_artifact_contents():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.GetArtifactContentsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_artifact_contents(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.GetArtifactContentsRequest, dict]]):
                The request object. Request message for
                GetArtifactContents.
            name (:class:`str`):
                Required. The name of the artifact whose contents should
                be retrieved. Format: ``{parent}/artifacts/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.httpbody_pb2.HttpBody:
                Message that represents an arbitrary HTTP body. It should only be used for
                   payload formats that can't be represented as JSON,
                   such as raw binary or an HTML page.

                   This message can be used both in streaming and
                   non-streaming API methods in the request as well as
                   the response.

                   It can be used as a top-level request field, which is
                   convenient if one wants to extract parameters from
                   either the URL or HTTP template into the request
                   fields and also want access to the raw HTTP body.

                   Example:

                      message GetResourceRequest {
                         // A unique request id. string request_id = 1;

                         // The raw HTTP body is bound to this field.
                         google.api.HttpBody http_body = 2;

                      }

                      service ResourceService {
                         rpc GetResource(GetResourceRequest)
                            returns (google.api.HttpBody);

                         rpc UpdateResource(google.api.HttpBody)
                            returns (google.protobuf.Empty);

                      }

                   Example with streaming methods:

                      service CaldavService {
                         rpc GetCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                         rpc UpdateCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                      }

                   Use of this type only changes how the request and
                   response bodies are handled, all other features will
                   continue to work unchanged.

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

        request = registry_service.GetArtifactContentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_artifact_contents,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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

    async def create_artifact(
        self,
        request: Optional[Union[registry_service.CreateArtifactRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        artifact: Optional[registry_models.Artifact] = None,
        artifact_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Artifact:
        r"""Creates a specified artifact.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_create_artifact():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.CreateArtifactRequest(
                    parent="parent_value",
                    artifact_id="artifact_id_value",
                )

                # Make the request
                response = await client.create_artifact(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.CreateArtifactRequest, dict]]):
                The request object. Request message for CreateArtifact.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                artifacts. Format: ``{parent}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            artifact (:class:`google.cloud.apigee_registry_v1.types.Artifact`):
                Required. The artifact to create.
                This corresponds to the ``artifact`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            artifact_id (:class:`str`):
                Required. The ID to use for the artifact, which will
                become the final component of the artifact's resource
                name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                Following AIP-162, IDs must not have the form of a UUID.

                This corresponds to the ``artifact_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Artifact:
                Artifacts of resources. Artifacts are unique (single-value) per resource
                   and are used to store metadata that is too large or
                   numerous to be stored directly on the resource. Since
                   artifacts are stored separately from parent
                   resources, they should generally be used for metadata
                   that is needed infrequently, i.e., not for display in
                   primary views of the resource but perhaps displayed
                   or downloaded upon request. The ListArtifacts method
                   allows artifacts to be quickly enumerated and checked
                   for presence without downloading their
                   (potentially-large) contents.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, artifact, artifact_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.CreateArtifactRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if artifact is not None:
            request.artifact = artifact
        if artifact_id is not None:
            request.artifact_id = artifact_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_artifact,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def replace_artifact(
        self,
        request: Optional[Union[registry_service.ReplaceArtifactRequest, dict]] = None,
        *,
        artifact: Optional[registry_models.Artifact] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> registry_models.Artifact:
        r"""Used to replace a specified artifact.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_replace_artifact():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.ReplaceArtifactRequest(
                )

                # Make the request
                response = await client.replace_artifact(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.ReplaceArtifactRequest, dict]]):
                The request object. Request message for ReplaceArtifact.
            artifact (:class:`google.cloud.apigee_registry_v1.types.Artifact`):
                Required. The artifact to replace.

                The ``name`` field is used to identify the artifact to
                replace. Format: ``{parent}/artifacts/*``

                This corresponds to the ``artifact`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.apigee_registry_v1.types.Artifact:
                Artifacts of resources. Artifacts are unique (single-value) per resource
                   and are used to store metadata that is too large or
                   numerous to be stored directly on the resource. Since
                   artifacts are stored separately from parent
                   resources, they should generally be used for metadata
                   that is needed infrequently, i.e., not for display in
                   primary views of the resource but perhaps displayed
                   or downloaded upon request. The ListArtifacts method
                   allows artifacts to be quickly enumerated and checked
                   for presence without downloading their
                   (potentially-large) contents.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([artifact])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registry_service.ReplaceArtifactRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if artifact is not None:
            request.artifact = artifact

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.replace_artifact,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("artifact.name", request.artifact.name),)
            ),
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

    async def delete_artifact(
        self,
        request: Optional[Union[registry_service.DeleteArtifactRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Removes a specified artifact.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import apigee_registry_v1

            async def sample_delete_artifact():
                # Create a client
                client = apigee_registry_v1.RegistryAsyncClient()

                # Initialize request argument(s)
                request = apigee_registry_v1.DeleteArtifactRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_artifact(request=request)

        Args:
            request (Optional[Union[google.cloud.apigee_registry_v1.types.DeleteArtifactRequest, dict]]):
                The request object. Request message for DeleteArtifact.
            name (:class:`str`):
                Required. The name of the artifact to delete. Format:
                ``{parent}/artifacts/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = registry_service.DeleteArtifactRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_artifact,
            default_retry=retries.Retry(
                initial=0.2,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.Aborted,
                    core_exceptions.Cancelled,
                    core_exceptions.DeadlineExceeded,
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
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.list_operations,
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

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_operation,
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

    async def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def set_iam_policy(
        self,
        request: Optional[iam_policy_pb2.SetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.

        Args:
            request (:class:`~.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    async def get_iam_policy(
        self,
        request: Optional[iam_policy_pb2.GetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does not have a
        policy set.

        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if
                any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    async def test_iam_permissions(
        self,
        request: Optional[iam_policy_pb2.TestIamPermissionsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified IAM permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will return an empty set
        of permissions, not a NOT_FOUND error.

        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    async def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_location,
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

    async def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.list_locations,
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

    async def __aenter__(self) -> "RegistryAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("RegistryAsyncClient",)
