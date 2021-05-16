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

from google.cloud.accessapproval_v1.services.access_approval import pagers
from google.cloud.accessapproval_v1.types import accessapproval
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import AccessApprovalTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AccessApprovalGrpcAsyncIOTransport
from .client import AccessApprovalClient


class AccessApprovalAsyncClient:
    """This API allows a customer to manage accesses to cloud resources by
    Google personnel. It defines the following resource model:

    -  The API has a collection of
       [ApprovalRequest][google.cloud.accessapproval.v1.ApprovalRequest]
       resources, named ``approvalRequests/{approval_request_id}``
    -  The API has top-level settings per Project/Folder/Organization,
       named ``accessApprovalSettings``

    The service also periodically emails a list of recipients, defined
    at the Project/Folder/Organization level in the
    accessApprovalSettings, when there is a pending ApprovalRequest for
    them to act on. The ApprovalRequests can also optionally be
    published to a Cloud Pub/Sub topic owned by the customer (for Beta,
    the Pub/Sub setup is managed manually).

    ApprovalRequests can be approved or dismissed. Google personel can
    only access the indicated resource or resources if the request is
    approved (subject to some exclusions:
    https://cloud.google.com/access-approval/docs/overview#exclusions).

    Note: Using Access Approval functionality will mean that Google may
    not be able to meet the SLAs for your chosen products, as any
    support response times may be dramatically increased. As such the
    SLAs do not apply to any service disruption to the extent impacted
    by Customer's use of Access Approval. Do not enable Access Approval
    for projects where you may require high service availability and
    rapid response by Google Cloud Support.

    After a request is approved or dismissed, no further action may be
    taken on it. Requests with the requested_expiration in the past or
    with no activity for 14 days are considered dismissed. When an
    approval expires, the request is considered dismissed.

    If a request is not approved or dismissed, we call it pending.
    """

    _client: AccessApprovalClient

    DEFAULT_ENDPOINT = AccessApprovalClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AccessApprovalClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        AccessApprovalClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AccessApprovalClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AccessApprovalClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AccessApprovalClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AccessApprovalClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AccessApprovalClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AccessApprovalClient.common_project_path)
    parse_common_project_path = staticmethod(
        AccessApprovalClient.parse_common_project_path
    )
    common_location_path = staticmethod(AccessApprovalClient.common_location_path)
    parse_common_location_path = staticmethod(
        AccessApprovalClient.parse_common_location_path
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
            AccessApprovalAsyncClient: The constructed client.
        """
        return AccessApprovalClient.from_service_account_info.__func__(AccessApprovalAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AccessApprovalAsyncClient: The constructed client.
        """
        return AccessApprovalClient.from_service_account_file.__func__(AccessApprovalAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AccessApprovalTransport:
        """Returns the transport used by the client instance.

        Returns:
            AccessApprovalTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AccessApprovalClient).get_transport_class, type(AccessApprovalClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AccessApprovalTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the access approval client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AccessApprovalTransport]): The
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
        self._client = AccessApprovalClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_approval_requests(
        self,
        request: accessapproval.ListApprovalRequestsMessage = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApprovalRequestsAsyncPager:
        r"""Lists approval requests associated with a project,
        folder, or organization. Approval requests can be
        filtered by state (pending, active, dismissed). The
        order is reverse chronological.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.ListApprovalRequestsMessage`):
                The request object. Request to list approval requests.
            parent (:class:`str`):
                The parent resource. This may be
                "projects/{project_id}", "folders/{folder_id}", or
                "organizations/{organization_id}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.services.access_approval.pagers.ListApprovalRequestsAsyncPager:
                Response to listing of
                ApprovalRequest objects.
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

        request = accessapproval.ListApprovalRequestsMessage(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_approval_requests,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        response = pagers.ListApprovalRequestsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_approval_request(
        self,
        request: accessapproval.GetApprovalRequestMessage = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accessapproval.ApprovalRequest:
        r"""Gets an approval request. Returns NOT_FOUND if the request does
        not exist.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.GetApprovalRequestMessage`):
                The request object. Request to get an approval request.
            name (:class:`str`):
                Name of the approval request to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.types.ApprovalRequest:
                A request for the customer to approve
                access to a resource.

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

        request = accessapproval.GetApprovalRequestMessage(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_approval_request,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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

    async def approve_approval_request(
        self,
        request: accessapproval.ApproveApprovalRequestMessage = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accessapproval.ApprovalRequest:
        r"""Approves a request and returns the updated ApprovalRequest.

        Returns NOT_FOUND if the request does not exist. Returns
        FAILED_PRECONDITION if the request exists but is not in a
        pending state.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.ApproveApprovalRequestMessage`):
                The request object. Request to approve an
                ApprovalRequest.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.types.ApprovalRequest:
                A request for the customer to approve
                access to a resource.

        """
        # Create or coerce a protobuf request object.
        request = accessapproval.ApproveApprovalRequestMessage(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.approve_approval_request,
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

    async def dismiss_approval_request(
        self,
        request: accessapproval.DismissApprovalRequestMessage = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accessapproval.ApprovalRequest:
        r"""Dismisses a request. Returns the updated ApprovalRequest.

        NOTE: This does not deny access to the resource if another
        request has been made and approved. It is equivalent in effect
        to ignoring the request altogether.

        Returns NOT_FOUND if the request does not exist.

        Returns FAILED_PRECONDITION if the request exists but is not in
        a pending state.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.DismissApprovalRequestMessage`):
                The request object. Request to dismiss an approval
                request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.types.ApprovalRequest:
                A request for the customer to approve
                access to a resource.

        """
        # Create or coerce a protobuf request object.
        request = accessapproval.DismissApprovalRequestMessage(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.dismiss_approval_request,
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

    async def get_access_approval_settings(
        self,
        request: accessapproval.GetAccessApprovalSettingsMessage = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accessapproval.AccessApprovalSettings:
        r"""Gets the settings associated with a project, folder,
        or organization.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.GetAccessApprovalSettingsMessage`):
                The request object. Request to get access approval
                settings.
            name (:class:`str`):
                Name of the AccessApprovalSettings to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.types.AccessApprovalSettings:
                Settings on a
                Project/Folder/Organization related to
                Access Approval.

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

        request = accessapproval.GetAccessApprovalSettingsMessage(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_access_approval_settings,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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

    async def update_access_approval_settings(
        self,
        request: accessapproval.UpdateAccessApprovalSettingsMessage = None,
        *,
        settings: accessapproval.AccessApprovalSettings = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accessapproval.AccessApprovalSettings:
        r"""Updates the settings associated with a project, folder, or
        organization. Settings to update are determined by the value of
        field_mask.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.UpdateAccessApprovalSettingsMessage`):
                The request object. Request to update access approval
                settings.
            settings (:class:`google.cloud.accessapproval_v1.types.AccessApprovalSettings`):
                The new AccessApprovalSettings.
                This corresponds to the ``settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The update mask applies to the settings. Only the top
                level fields of AccessApprovalSettings
                (notification_emails & enrolled_services) are supported.
                For each field, if it is included, the currently stored
                value will be entirely overwritten with the value of the
                field passed in this request.

                For the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
                If this field is left unset, only the
                notification_emails field will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.accessapproval_v1.types.AccessApprovalSettings:
                Settings on a
                Project/Folder/Organization related to
                Access Approval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = accessapproval.UpdateAccessApprovalSettingsMessage(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if settings is not None:
            request.settings = settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_access_approval_settings,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("settings.name", request.settings.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_access_approval_settings(
        self,
        request: accessapproval.DeleteAccessApprovalSettingsMessage = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the settings associated with a project,
        folder, or organization. This will have the effect of
        disabling Access Approval for the project, folder, or
        organization, but only if all ancestors also have Access
        Approval disabled. If Access Approval is enabled at a
        higher level of the hierarchy, then Access Approval will
        still be enabled at this level as the settings are
        inherited.

        Args:
            request (:class:`google.cloud.accessapproval_v1.types.DeleteAccessApprovalSettingsMessage`):
                The request object. Request to delete access approval
                settings.
            name (:class:`str`):
                Name of the AccessApprovalSettings to
                delete.

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

        request = accessapproval.DeleteAccessApprovalSettingsMessage(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_access_approval_settings,
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
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-access-approval",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AccessApprovalAsyncClient",)
