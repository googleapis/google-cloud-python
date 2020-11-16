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

from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dataproc_v1.services.autoscaling_policy_service import pagers
from google.cloud.dataproc_v1.types import autoscaling_policies

from .transports.base import AutoscalingPolicyServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AutoscalingPolicyServiceGrpcAsyncIOTransport
from .client import AutoscalingPolicyServiceClient


class AutoscalingPolicyServiceAsyncClient:
    """The API interface for managing autoscaling policies in the
    Dataproc API.
    """

    _client: AutoscalingPolicyServiceClient

    DEFAULT_ENDPOINT = AutoscalingPolicyServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AutoscalingPolicyServiceClient.DEFAULT_MTLS_ENDPOINT

    autoscaling_policy_path = staticmethod(
        AutoscalingPolicyServiceClient.autoscaling_policy_path
    )
    parse_autoscaling_policy_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_autoscaling_policy_path
    )

    common_billing_account_path = staticmethod(
        AutoscalingPolicyServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_common_billing_account_path
    )

    common_folder_path = staticmethod(AutoscalingPolicyServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_common_folder_path
    )

    common_organization_path = staticmethod(
        AutoscalingPolicyServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_common_organization_path
    )

    common_project_path = staticmethod(
        AutoscalingPolicyServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_common_project_path
    )

    common_location_path = staticmethod(
        AutoscalingPolicyServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        AutoscalingPolicyServiceClient.parse_common_location_path
    )

    from_service_account_file = AutoscalingPolicyServiceClient.from_service_account_file
    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AutoscalingPolicyServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            AutoscalingPolicyServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AutoscalingPolicyServiceClient).get_transport_class,
        type(AutoscalingPolicyServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, AutoscalingPolicyServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the autoscaling policy service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AutoscalingPolicyServiceTransport]): The
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

        self._client = AutoscalingPolicyServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_autoscaling_policy(
        self,
        request: autoscaling_policies.CreateAutoscalingPolicyRequest = None,
        *,
        parent: str = None,
        policy: autoscaling_policies.AutoscalingPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> autoscaling_policies.AutoscalingPolicy:
        r"""Creates new autoscaling policy.

        Args:
            request (:class:`~.autoscaling_policies.CreateAutoscalingPolicyRequest`):
                The request object. A request to create an autoscaling
                policy.
            parent (:class:`str`):
                Required. The "resource name" of the region or location,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.autoscalingPolicies.create``,
                   the resource name of the region has the following
                   format: ``projects/{project_id}/regions/{region}``

                -  For
                   ``projects.locations.autoscalingPolicies.create``,
                   the resource name of the location has the following
                   format:
                   ``projects/{project_id}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            policy (:class:`~.autoscaling_policies.AutoscalingPolicy`):
                Required. The autoscaling policy to
                create.
                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.autoscaling_policies.AutoscalingPolicy:
                Describes an autoscaling policy for
                Dataproc cluster autoscaler.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = autoscaling_policies.CreateAutoscalingPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if policy is not None:
            request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_autoscaling_policy,
            default_timeout=600.0,
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

    async def update_autoscaling_policy(
        self,
        request: autoscaling_policies.UpdateAutoscalingPolicyRequest = None,
        *,
        policy: autoscaling_policies.AutoscalingPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> autoscaling_policies.AutoscalingPolicy:
        r"""Updates (replaces) autoscaling policy.

        Disabled check for update_mask, because all updates will be full
        replacements.

        Args:
            request (:class:`~.autoscaling_policies.UpdateAutoscalingPolicyRequest`):
                The request object. A request to update an autoscaling
                policy.
            policy (:class:`~.autoscaling_policies.AutoscalingPolicy`):
                Required. The updated autoscaling
                policy.
                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.autoscaling_policies.AutoscalingPolicy:
                Describes an autoscaling policy for
                Dataproc cluster autoscaler.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = autoscaling_policies.UpdateAutoscalingPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if policy is not None:
            request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_autoscaling_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("policy.name", request.policy.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_autoscaling_policy(
        self,
        request: autoscaling_policies.GetAutoscalingPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> autoscaling_policies.AutoscalingPolicy:
        r"""Retrieves autoscaling policy.

        Args:
            request (:class:`~.autoscaling_policies.GetAutoscalingPolicyRequest`):
                The request object. A request to fetch an autoscaling
                policy.
            name (:class:`str`):
                Required. The "resource name" of the autoscaling policy,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.autoscalingPolicies.get``, the
                   resource name of the policy has the following format:
                   ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``

                -  For ``projects.locations.autoscalingPolicies.get``,
                   the resource name of the policy has the following
                   format:
                   ``projects/{project_id}/locations/{location}/autoscalingPolicies/{policy_id}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.autoscaling_policies.AutoscalingPolicy:
                Describes an autoscaling policy for
                Dataproc cluster autoscaler.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = autoscaling_policies.GetAutoscalingPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_autoscaling_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_autoscaling_policies(
        self,
        request: autoscaling_policies.ListAutoscalingPoliciesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAutoscalingPoliciesAsyncPager:
        r"""Lists autoscaling policies in the project.

        Args:
            request (:class:`~.autoscaling_policies.ListAutoscalingPoliciesRequest`):
                The request object. A request to list autoscaling
                policies in a project.
            parent (:class:`str`):
                Required. The "resource name" of the region or location,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.autoscalingPolicies.list``,
                   the resource name of the region has the following
                   format: ``projects/{project_id}/regions/{region}``

                -  For ``projects.locations.autoscalingPolicies.list``,
                   the resource name of the location has the following
                   format:
                   ``projects/{project_id}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListAutoscalingPoliciesAsyncPager:
                A response to a request to list
                autoscaling policies in a project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = autoscaling_policies.ListAutoscalingPoliciesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_autoscaling_policies,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAutoscalingPoliciesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_autoscaling_policy(
        self,
        request: autoscaling_policies.DeleteAutoscalingPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an autoscaling policy. It is an error to
        delete an autoscaling policy that is in use by one or
        more clusters.

        Args:
            request (:class:`~.autoscaling_policies.DeleteAutoscalingPolicyRequest`):
                The request object. A request to delete an autoscaling
                policy.
                Autoscaling policies in use by one or more clusters will
                not be deleted.
            name (:class:`str`):
                Required. The "resource name" of the autoscaling policy,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.autoscalingPolicies.delete``,
                   the resource name of the policy has the following
                   format:
                   ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``

                -  For
                   ``projects.locations.autoscalingPolicies.delete``,
                   the resource name of the policy has the following
                   format:
                   ``projects/{project_id}/locations/{location}/autoscalingPolicies/{policy_id}``
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = autoscaling_policies.DeleteAutoscalingPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_autoscaling_policy,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AutoscalingPolicyServiceAsyncClient",)
