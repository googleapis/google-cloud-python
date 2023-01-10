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

from google.cloud.contentwarehouse_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.longrunning import operations_pb2

from google.cloud.contentwarehouse_v1.services.rule_set_service import pagers
from google.cloud.contentwarehouse_v1.types import rule_engine, ruleset_service_request

from .client import RuleSetServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, RuleSetServiceTransport
from .transports.grpc_asyncio import RuleSetServiceGrpcAsyncIOTransport


class RuleSetServiceAsyncClient:
    """Service to manage customer specific RuleSets."""

    _client: RuleSetServiceClient

    DEFAULT_ENDPOINT = RuleSetServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = RuleSetServiceClient.DEFAULT_MTLS_ENDPOINT

    document_path = staticmethod(RuleSetServiceClient.document_path)
    parse_document_path = staticmethod(RuleSetServiceClient.parse_document_path)
    location_path = staticmethod(RuleSetServiceClient.location_path)
    parse_location_path = staticmethod(RuleSetServiceClient.parse_location_path)
    rule_set_path = staticmethod(RuleSetServiceClient.rule_set_path)
    parse_rule_set_path = staticmethod(RuleSetServiceClient.parse_rule_set_path)
    common_billing_account_path = staticmethod(
        RuleSetServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        RuleSetServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(RuleSetServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        RuleSetServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        RuleSetServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        RuleSetServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(RuleSetServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        RuleSetServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(RuleSetServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        RuleSetServiceClient.parse_common_location_path
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
            RuleSetServiceAsyncClient: The constructed client.
        """
        return RuleSetServiceClient.from_service_account_info.__func__(RuleSetServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            RuleSetServiceAsyncClient: The constructed client.
        """
        return RuleSetServiceClient.from_service_account_file.__func__(RuleSetServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return RuleSetServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> RuleSetServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            RuleSetServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(RuleSetServiceClient).get_transport_class, type(RuleSetServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, RuleSetServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the rule set service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RuleSetServiceTransport]): The
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
        self._client = RuleSetServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_rule_set(
        self,
        request: Optional[
            Union[ruleset_service_request.CreateRuleSetRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        rule_set: Optional[rule_engine.RuleSet] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> rule_engine.RuleSet:
        r"""Creates a ruleset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_create_rule_set():
                # Create a client
                client = contentwarehouse_v1.RuleSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.CreateRuleSetRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_rule_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.CreateRuleSetRequest, dict]]):
                The request object. Request message for
                RuleSetService.CreateRuleSet.
            parent (:class:`str`):
                Required. The parent name. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rule_set (:class:`google.cloud.contentwarehouse_v1.types.RuleSet`):
                Required. The rule set to create.
                This corresponds to the ``rule_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.RuleSet:
                Represents a set of rules from a
                single customer.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, rule_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ruleset_service_request.CreateRuleSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if rule_set is not None:
            request.rule_set = rule_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_rule_set,
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

    async def get_rule_set(
        self,
        request: Optional[
            Union[ruleset_service_request.GetRuleSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> rule_engine.RuleSet:
        r"""Gets a ruleset. Returns NOT_FOUND if the ruleset does not exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_get_rule_set():
                # Create a client
                client = contentwarehouse_v1.RuleSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.GetRuleSetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_rule_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.GetRuleSetRequest, dict]]):
                The request object. Request message for
                RuleSetService.GetRuleSet.
            name (:class:`str`):
                Required. The name of the rule set to retrieve. Format:
                projects/{project_number}/locations/{location}/ruleSets/{rule_set_id}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.RuleSet:
                Represents a set of rules from a
                single customer.

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

        request = ruleset_service_request.GetRuleSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_rule_set,
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

    async def update_rule_set(
        self,
        request: Optional[
            Union[ruleset_service_request.UpdateRuleSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        rule_set: Optional[rule_engine.RuleSet] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> rule_engine.RuleSet:
        r"""Updates a ruleset. Returns INVALID_ARGUMENT if the name of the
        ruleset is non-empty and does not equal the existing name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_update_rule_set():
                # Create a client
                client = contentwarehouse_v1.RuleSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.UpdateRuleSetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.update_rule_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.UpdateRuleSetRequest, dict]]):
                The request object. Request message for
                RuleSetService.UpdateRuleSet.
            name (:class:`str`):
                Required. The name of the rule set to update. Format:
                projects/{project_number}/locations/{location}/ruleSets/{rule_set_id}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rule_set (:class:`google.cloud.contentwarehouse_v1.types.RuleSet`):
                Required. The rule set to update.
                This corresponds to the ``rule_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.RuleSet:
                Represents a set of rules from a
                single customer.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, rule_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ruleset_service_request.UpdateRuleSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if rule_set is not None:
            request.rule_set = rule_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_rule_set,
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

    async def delete_rule_set(
        self,
        request: Optional[
            Union[ruleset_service_request.DeleteRuleSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ruleset. Returns NOT_FOUND if the document does not
        exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_delete_rule_set():
                # Create a client
                client = contentwarehouse_v1.RuleSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.DeleteRuleSetRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_rule_set(request=request)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.DeleteRuleSetRequest, dict]]):
                The request object. Request message for
                RuleSetService.DeleteRuleSet.
            name (:class:`str`):
                Required. The name of the rule set to delete. Format:
                projects/{project_number}/locations/{location}/ruleSets/{rule_set_id}.

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

        request = ruleset_service_request.DeleteRuleSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_rule_set,
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

    async def list_rule_sets(
        self,
        request: Optional[
            Union[ruleset_service_request.ListRuleSetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRuleSetsAsyncPager:
        r"""Lists rulesets.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_list_rule_sets():
                # Create a client
                client = contentwarehouse_v1.RuleSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.ListRuleSetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_rule_sets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.ListRuleSetsRequest, dict]]):
                The request object. Request message for
                RuleSetService.ListRuleSets.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                document. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.services.rule_set_service.pagers.ListRuleSetsAsyncPager:
                Response message for
                RuleSetService.ListRuleSets.
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

        request = ruleset_service_request.ListRuleSetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_rule_sets,
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
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRuleSetsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("RuleSetServiceAsyncClient",)
