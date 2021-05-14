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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.orgpolicy_v2.services.org_policy import pagers
from google.cloud.orgpolicy_v2.types import constraint
from google.cloud.orgpolicy_v2.types import orgpolicy
from .transports.base import OrgPolicyTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import OrgPolicyGrpcAsyncIOTransport
from .client import OrgPolicyClient


class OrgPolicyAsyncClient:
    """An interface for managing organization policies.

    The Cloud Org Policy service provides a simple mechanism for
    organizations to restrict the allowed configurations across their
    entire Cloud Resource hierarchy.

    You can use a ``policy`` to configure restrictions in Cloud
    resources. For example, you can enforce a ``policy`` that restricts
    which Google Cloud Platform APIs can be activated in a certain part
    of your resource hierarchy, or prevents serial port access to VM
    instances in a particular folder.

    ``Policies`` are inherited down through the resource hierarchy. A
    ``policy`` applied to a parent resource automatically applies to all
    its child resources unless overridden with a ``policy`` lower in the
    hierarchy.

    A ``constraint`` defines an aspect of a resource's configuration
    that can be controlled by an organization's policy administrator.
    ``Policies`` are a collection of ``constraints`` that defines their
    allowable configuration on a particular resource and its child
    resources.
    """

    _client: OrgPolicyClient

    DEFAULT_ENDPOINT = OrgPolicyClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = OrgPolicyClient.DEFAULT_MTLS_ENDPOINT

    constraint_path = staticmethod(OrgPolicyClient.constraint_path)
    parse_constraint_path = staticmethod(OrgPolicyClient.parse_constraint_path)
    policy_path = staticmethod(OrgPolicyClient.policy_path)
    parse_policy_path = staticmethod(OrgPolicyClient.parse_policy_path)
    common_billing_account_path = staticmethod(
        OrgPolicyClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        OrgPolicyClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(OrgPolicyClient.common_folder_path)
    parse_common_folder_path = staticmethod(OrgPolicyClient.parse_common_folder_path)
    common_organization_path = staticmethod(OrgPolicyClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        OrgPolicyClient.parse_common_organization_path
    )
    common_project_path = staticmethod(OrgPolicyClient.common_project_path)
    parse_common_project_path = staticmethod(OrgPolicyClient.parse_common_project_path)
    common_location_path = staticmethod(OrgPolicyClient.common_location_path)
    parse_common_location_path = staticmethod(
        OrgPolicyClient.parse_common_location_path
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
            OrgPolicyAsyncClient: The constructed client.
        """
        return OrgPolicyClient.from_service_account_info.__func__(OrgPolicyAsyncClient, info, *args, **kwargs)  # type: ignore

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
            OrgPolicyAsyncClient: The constructed client.
        """
        return OrgPolicyClient.from_service_account_file.__func__(OrgPolicyAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OrgPolicyTransport:
        """Returns the transport used by the client instance.

        Returns:
            OrgPolicyTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(OrgPolicyClient).get_transport_class, type(OrgPolicyClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, OrgPolicyTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the org policy client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.OrgPolicyTransport]): The
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
        self._client = OrgPolicyClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_constraints(
        self,
        request: orgpolicy.ListConstraintsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConstraintsAsyncPager:
        r"""Lists ``Constraints`` that could be applied on the specified
        resource.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.ListConstraintsRequest`):
                The request object. The request sent to the
                [ListConstraints]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints]
                method.
            parent (:class:`str`):
                Required. The Cloud resource that parents the
                constraint. Must be in one of the following forms:

                -  ``projects/{project_number}``
                -  ``projects/{project_id}``
                -  ``folders/{folder_id}``
                -  ``organizations/{organization_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.services.org_policy.pagers.ListConstraintsAsyncPager:
                The response returned from the [ListConstraints]
                   [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = orgpolicy.ListConstraintsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_constraints,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListConstraintsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_policies(
        self,
        request: orgpolicy.ListPoliciesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPoliciesAsyncPager:
        r"""Retrieves all of the ``Policies`` that exist on a particular
        resource.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.ListPoliciesRequest`):
                The request object. The request sent to the
                [ListPolicies]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies]
                method.
            parent (:class:`str`):
                Required. The target Cloud resource that parents the set
                of constraints and policies that will be returned from
                this call. Must be in one of the following forms:

                -  ``projects/{project_number}``
                -  ``projects/{project_id}``
                -  ``folders/{folder_id}``
                -  ``organizations/{organization_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.services.org_policy.pagers.ListPoliciesAsyncPager:
                The response returned from the [ListPolicies]
                   [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies]
                   method. It will be empty if no Policies are set on
                   the resource.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = orgpolicy.ListPoliciesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_policies,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListPoliciesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_policy(
        self,
        request: orgpolicy.GetPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> orgpolicy.Policy:
        r"""Gets a ``Policy`` on a resource.

        If no ``Policy`` is set on the resource, NOT_FOUND is returned.
        The ``etag`` value can be used with ``UpdatePolicy()`` to update
        a ``Policy`` during read-modify-write.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.GetPolicyRequest`):
                The request object. The request sent to the [GetPolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.GetPolicy] method.
            name (:class:`str`):
                Required. Resource name of the policy. See ``Policy``
                for naming requirements.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.types.Policy:
                Defines a Cloud Organization Policy which is used to specify Constraints
                   for configurations of Cloud Platform resources.

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

        request = orgpolicy.GetPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_effective_policy(
        self,
        request: orgpolicy.GetEffectivePolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> orgpolicy.Policy:
        r"""Gets the effective ``Policy`` on a resource. This is the result
        of merging ``Policies`` in the resource hierarchy and evaluating
        conditions. The returned ``Policy`` will not have an ``etag`` or
        ``condition`` set because it is a computed ``Policy`` across
        multiple resources. Subtrees of Resource Manager resource
        hierarchy with 'under:' prefix will not be expanded.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.GetEffectivePolicyRequest`):
                The request object. The request sent to the
                [GetEffectivePolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.GetEffectivePolicy]
                method.
            name (:class:`str`):
                Required. The effective policy to compute. See
                ``Policy`` for naming rules.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.types.Policy:
                Defines a Cloud Organization Policy which is used to specify Constraints
                   for configurations of Cloud Platform resources.

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

        request = orgpolicy.GetEffectivePolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_effective_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_policy(
        self,
        request: orgpolicy.CreatePolicyRequest = None,
        *,
        parent: str = None,
        policy: orgpolicy.Policy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> orgpolicy.Policy:
        r"""Creates a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint does not exist.
        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ALREADY_EXISTS`` if the policy already exists
        on the given Cloud resource.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.CreatePolicyRequest`):
                The request object. The request sent to the
                [CreatePolicyRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.CreatePolicy]
                method.
            parent (:class:`str`):
                Required. The Cloud resource that will parent the new
                Policy. Must be in one of the following forms:

                -  ``projects/{project_number}``
                -  ``projects/{project_id}``
                -  ``folders/{folder_id}``
                -  ``organizations/{organization_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            policy (:class:`google.cloud.orgpolicy_v2.types.Policy`):
                Required. ``Policy`` to create.
                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.types.Policy:
                Defines a Cloud Organization Policy which is used to specify Constraints
                   for configurations of Cloud Platform resources.

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

        request = orgpolicy.CreatePolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if policy is not None:
            request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_policy(
        self,
        request: orgpolicy.UpdatePolicyRequest = None,
        *,
        policy: orgpolicy.Policy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> orgpolicy.Policy:
        r"""Updates a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint or the policy do
        not exist. Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.ABORTED`` if the etag supplied in the request
        does not match the persisted etag of the policy

        Note: the supplied policy will perform a full overwrite of all
        fields.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.UpdatePolicyRequest`):
                The request object. The request sent to the
                [UpdatePolicyRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.UpdatePolicy]
                method.
            policy (:class:`google.cloud.orgpolicy_v2.types.Policy`):
                Required. ``Policy`` to update.
                This corresponds to the ``policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.orgpolicy_v2.types.Policy:
                Defines a Cloud Organization Policy which is used to specify Constraints
                   for configurations of Cloud Platform resources.

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

        request = orgpolicy.UpdatePolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if policy is not None:
            request.policy = policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
                (("policy.name", request.policy.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_policy(
        self,
        request: orgpolicy.DeletePolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a Policy.

        Returns a ``google.rpc.Status`` with
        ``google.rpc.Code.NOT_FOUND`` if the constraint or Org Policy
        does not exist.

        Args:
            request (:class:`google.cloud.orgpolicy_v2.types.DeletePolicyRequest`):
                The request object. The request sent to the
                [DeletePolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.DeletePolicy]
                method.
            name (:class:`str`):
                Required. Name of the policy to delete. See ``Policy``
                for naming rules.

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

        request = orgpolicy.DeletePolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-org-policy",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("OrgPolicyAsyncClient",)
