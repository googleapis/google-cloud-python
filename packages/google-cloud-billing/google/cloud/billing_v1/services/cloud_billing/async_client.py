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

from google.cloud.billing_v1.services.cloud_billing import pagers
from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from .transports.base import CloudBillingTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudBillingGrpcAsyncIOTransport
from .client import CloudBillingClient


class CloudBillingAsyncClient:
    """Retrieves GCP Console billing accounts and associates them
    with projects.
    """

    _client: CloudBillingClient

    DEFAULT_ENDPOINT = CloudBillingClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudBillingClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        CloudBillingClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudBillingClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudBillingClient.common_folder_path)
    parse_common_folder_path = staticmethod(CloudBillingClient.parse_common_folder_path)
    common_organization_path = staticmethod(CloudBillingClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        CloudBillingClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudBillingClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudBillingClient.parse_common_project_path
    )
    common_location_path = staticmethod(CloudBillingClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudBillingClient.parse_common_location_path
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
            CloudBillingAsyncClient: The constructed client.
        """
        return CloudBillingClient.from_service_account_info.__func__(CloudBillingAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CloudBillingAsyncClient: The constructed client.
        """
        return CloudBillingClient.from_service_account_file.__func__(CloudBillingAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudBillingTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudBillingTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudBillingClient).get_transport_class, type(CloudBillingClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudBillingTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud billing client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudBillingTransport]): The
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
        self._client = CloudBillingClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_billing_account(
        self,
        request: cloud_billing.GetBillingAccountRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Gets information about a billing account. The current
        authenticated user must be a `viewer of the billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`google.cloud.billing_v1.types.GetBillingAccountRequest`):
                The request object. Request message for
                `GetBillingAccount`.
            name (:class:`str`):
                Required. The resource name of the billing account to
                retrieve. For example,
                ``billingAccounts/012345-567890-ABCDEF``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.types.BillingAccount:
                A billing account in [GCP Console](\ https://console.cloud.google.com/).
                   You can assign a billing account to one or more
                   projects.

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

        request = cloud_billing.GetBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_billing_account,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

    async def list_billing_accounts(
        self,
        request: cloud_billing.ListBillingAccountsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBillingAccountsAsyncPager:
        r"""Lists the billing accounts that the current authenticated user
        has permission to
        `view <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`google.cloud.billing_v1.types.ListBillingAccountsRequest`):
                The request object. Request message for
                `ListBillingAccounts`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.services.cloud_billing.pagers.ListBillingAccountsAsyncPager:
                Response message for ListBillingAccounts.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = cloud_billing.ListBillingAccountsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_billing_accounts,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBillingAccountsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_billing_account(
        self,
        request: cloud_billing.UpdateBillingAccountRequest = None,
        *,
        name: str = None,
        account: cloud_billing.BillingAccount = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Updates a billing account's fields. Currently the only field
        that can be edited is ``display_name``. The current
        authenticated user must have the ``billing.accounts.update`` IAM
        permission, which is typically given to the
        `administrator <https://cloud.google.com/billing/docs/how-to/billing-access>`__
        of the billing account.

        Args:
            request (:class:`google.cloud.billing_v1.types.UpdateBillingAccountRequest`):
                The request object. Request message for
                `UpdateBillingAccount`.
            name (:class:`str`):
                Required. The name of the billing
                account resource to be updated.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            account (:class:`google.cloud.billing_v1.types.BillingAccount`):
                Required. The billing account
                resource to replace the resource on the
                server.

                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.types.BillingAccount:
                A billing account in [GCP Console](\ https://console.cloud.google.com/).
                   You can assign a billing account to one or more
                   projects.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, account])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.UpdateBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if account is not None:
            request.account = account

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_billing_account,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

    async def create_billing_account(
        self,
        request: cloud_billing.CreateBillingAccountRequest = None,
        *,
        billing_account: cloud_billing.BillingAccount = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Creates a billing account. This method can only be used to
        create `billing
        subaccounts <https://cloud.google.com/billing/docs/concepts>`__
        by GCP resellers. When creating a subaccount, the current
        authenticated user must have the ``billing.accounts.update`` IAM
        permission on the master account, which is typically given to
        billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.
        This method will return an error if the master account has not
        been provisioned as a reseller account.

        Args:
            request (:class:`google.cloud.billing_v1.types.CreateBillingAccountRequest`):
                The request object. Request message for
                `CreateBillingAccount`.
            billing_account (:class:`google.cloud.billing_v1.types.BillingAccount`):
                Required. The billing account
                resource to create. Currently
                CreateBillingAccount only supports
                subaccount creation, so any created
                billing accounts must be under a
                provided master billing account.

                This corresponds to the ``billing_account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.types.BillingAccount:
                A billing account in [GCP Console](\ https://console.cloud.google.com/).
                   You can assign a billing account to one or more
                   projects.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([billing_account])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.CreateBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if billing_account is not None:
            request.billing_account = billing_account

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_billing_account,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_project_billing_info(
        self,
        request: cloud_billing.ListProjectBillingInfoRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProjectBillingInfoAsyncPager:
        r"""Lists the projects associated with a billing account. The
        current authenticated user must have the
        ``billing.resourceAssociations.list`` IAM permission, which is
        often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`google.cloud.billing_v1.types.ListProjectBillingInfoRequest`):
                The request object. Request message for
                `ListProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the billing account
                associated with the projects that you want to list. For
                example, ``billingAccounts/012345-567890-ABCDEF``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.services.cloud_billing.pagers.ListProjectBillingInfoAsyncPager:
                Request message for ListProjectBillingInfoResponse.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = cloud_billing.ListProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_project_billing_info,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListProjectBillingInfoAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_project_billing_info(
        self,
        request: cloud_billing.GetProjectBillingInfoRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.ProjectBillingInfo:
        r"""Gets the billing information for a project. The current
        authenticated user must have `permission to view the
        project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__.

        Args:
            request (:class:`google.cloud.billing_v1.types.GetProjectBillingInfoRequest`):
                The request object. Request message for
                `GetProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the project for which
                billing information is retrieved. For example,
                ``projects/tokyo-rain-123``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.types.ProjectBillingInfo:
                Encapsulation of billing information
                for a GCP Console project. A project has
                at most one associated billing account
                at a time (but a billing account can be
                assigned to multiple projects).

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

        request = cloud_billing.GetProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_project_billing_info,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

    async def update_project_billing_info(
        self,
        request: cloud_billing.UpdateProjectBillingInfoRequest = None,
        *,
        name: str = None,
        project_billing_info: cloud_billing.ProjectBillingInfo = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.ProjectBillingInfo:
        r"""Sets or updates the billing account associated with a project.
        You specify the new billing account by setting the
        ``billing_account_name`` in the ``ProjectBillingInfo`` resource
        to the resource name of a billing account. Associating a project
        with an open billing account enables billing on the project and
        allows charges for resource usage. If the project already had a
        billing account, this method changes the billing account used
        for resource usage charges.

        *Note:* Incurred charges that have not yet been reported in the
        transaction history of the GCP Console might be billed to the
        new billing account, even if the charge occurred before the new
        billing account was assigned to the project.

        The current authenticated user must have ownership privileges
        for both the
        `project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__
        and the `billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        You can disable billing on the project by setting the
        ``billing_account_name`` field to empty. This action
        disassociates the current billing account from the project. Any
        billable activity of your in-use services will stop, and your
        application could stop functioning as expected. Any unbilled
        charges to date will be billed to the previously associated
        account. The current authenticated user must be either an owner
        of the project or an owner of the billing account for the
        project.

        Note that associating a project with a *closed* billing account
        will have much the same effect as disabling billing on the
        project: any paid resources used by the project will be shut
        down. Thus, unless you wish to disable billing, you should
        always call this method with the name of an *open* billing
        account.

        Args:
            request (:class:`google.cloud.billing_v1.types.UpdateProjectBillingInfoRequest`):
                The request object. Request message for
                `UpdateProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the project associated
                with the billing information that you want to update.
                For example, ``projects/tokyo-rain-123``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            project_billing_info (:class:`google.cloud.billing_v1.types.ProjectBillingInfo`):
                The new billing information for the project. Read-only
                fields are ignored; thus, you can leave empty all fields
                except ``billing_account_name``.

                This corresponds to the ``project_billing_info`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.billing_v1.types.ProjectBillingInfo:
                Encapsulation of billing information
                for a GCP Console project. A project has
                at most one associated billing account
                at a time (but a billing account can be
                assigned to multiple projects).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, project_billing_info])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.UpdateProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if project_billing_info is not None:
            request.project_billing_info = project_billing_info

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_project_billing_info,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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

    async def get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a billing account. The caller
        must have the ``billing.accounts.getIamPolicy`` permission on
        the account, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`google.iam.v1.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.GetIamPolicyRequest(resource=resource,)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy for a billing account. Replaces
        any existing policy. The caller must have the
        ``billing.accounts.setIamPolicy`` permission on the account,
        which is often given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`google.iam.v1.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.SetIamPolicyRequest(resource=resource,)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the access control policy for a billing
        account. This method takes the resource and a set of
        permissions as input and returns the subset of the input
        permissions that the caller is allowed for that
        resource.

        Args:
            request (:class:`google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (:class:`Sequence[str]`):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            request = iam_policy_pb2.TestIamPermissionsRequest(
                resource=resource, permissions=permissions,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
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
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-billing",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudBillingAsyncClient",)
