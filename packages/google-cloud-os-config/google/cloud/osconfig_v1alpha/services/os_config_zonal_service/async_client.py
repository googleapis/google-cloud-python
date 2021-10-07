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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service import pagers
from google.cloud.osconfig_v1alpha.types import config_common
from google.cloud.osconfig_v1alpha.types import instance_os_policies_compliance
from google.cloud.osconfig_v1alpha.types import inventory
from google.cloud.osconfig_v1alpha.types import os_policy
from google.cloud.osconfig_v1alpha.types import os_policy_assignments
from google.cloud.osconfig_v1alpha.types import vulnerability
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import OsConfigZonalServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import OsConfigZonalServiceGrpcAsyncIOTransport
from .client import OsConfigZonalServiceClient


class OsConfigZonalServiceAsyncClient:
    """Zonal OS Config API
    The OS Config service is the server-side component that allows
    users to manage package installations and patch jobs for Compute
    Engine VM instances.
    """

    _client: OsConfigZonalServiceClient

    DEFAULT_ENDPOINT = OsConfigZonalServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = OsConfigZonalServiceClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(OsConfigZonalServiceClient.instance_path)
    parse_instance_path = staticmethod(OsConfigZonalServiceClient.parse_instance_path)
    instance_os_policies_compliance_path = staticmethod(
        OsConfigZonalServiceClient.instance_os_policies_compliance_path
    )
    parse_instance_os_policies_compliance_path = staticmethod(
        OsConfigZonalServiceClient.parse_instance_os_policies_compliance_path
    )
    inventory_path = staticmethod(OsConfigZonalServiceClient.inventory_path)
    parse_inventory_path = staticmethod(OsConfigZonalServiceClient.parse_inventory_path)
    os_policy_assignment_path = staticmethod(
        OsConfigZonalServiceClient.os_policy_assignment_path
    )
    parse_os_policy_assignment_path = staticmethod(
        OsConfigZonalServiceClient.parse_os_policy_assignment_path
    )
    vulnerability_report_path = staticmethod(
        OsConfigZonalServiceClient.vulnerability_report_path
    )
    parse_vulnerability_report_path = staticmethod(
        OsConfigZonalServiceClient.parse_vulnerability_report_path
    )
    common_billing_account_path = staticmethod(
        OsConfigZonalServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        OsConfigZonalServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(OsConfigZonalServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        OsConfigZonalServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        OsConfigZonalServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        OsConfigZonalServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(OsConfigZonalServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        OsConfigZonalServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(OsConfigZonalServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        OsConfigZonalServiceClient.parse_common_location_path
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
            OsConfigZonalServiceAsyncClient: The constructed client.
        """
        return OsConfigZonalServiceClient.from_service_account_info.__func__(OsConfigZonalServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            OsConfigZonalServiceAsyncClient: The constructed client.
        """
        return OsConfigZonalServiceClient.from_service_account_file.__func__(OsConfigZonalServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OsConfigZonalServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            OsConfigZonalServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(OsConfigZonalServiceClient).get_transport_class,
        type(OsConfigZonalServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, OsConfigZonalServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the os config zonal service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.OsConfigZonalServiceTransport]): The
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
        self._client = OsConfigZonalServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_os_policy_assignment(
        self,
        request: os_policy_assignments.CreateOSPolicyAssignmentRequest = None,
        *,
        parent: str = None,
        os_policy_assignment: os_policy_assignments.OSPolicyAssignment = None,
        os_policy_assignment_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create an OS policy assignment.

        This method also creates the first revision of the OS policy
        assignment.

        This method returns a long running operation (LRO) that contains
        the rollout details. The rollout can be cancelled by cancelling
        the LRO.

        For more information, see `Method:
        projects.locations.osPolicyAssignments.operations.cancel <https://cloud.google.com/compute/docs/osconfig/rest/v1alpha/projects.locations.osPolicyAssignments.operations/cancel>`__.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.CreateOSPolicyAssignmentRequest`):
                The request object. A request message to create an OS
                policy assignment
            parent (:class:`str`):
                Required. The parent resource name in
                the form:
                projects/{project}/locations/{location}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            os_policy_assignment (:class:`google.cloud.osconfig_v1alpha.types.OSPolicyAssignment`):
                Required. The OS policy assignment to
                be created.

                This corresponds to the ``os_policy_assignment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            os_policy_assignment_id (:class:`str`):
                Required. The logical name of the OS policy assignment
                in the project with the following restrictions:

                -  Must contain only lowercase letters, numbers, and
                   hyphens.
                -  Must start with a letter.
                -  Must be between 1-63 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the project.


                This corresponds to the ``os_policy_assignment_id`` field
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

                The result type for the operation will be :class:`google.cloud.osconfig_v1alpha.types.OSPolicyAssignment` OS policy assignment is an API resource that is used to
                   apply a set of OS policies to a dynamically targeted
                   group of Compute Engine VM instances.

                   An OS policy is used to define the desired state
                   configuration for a Compute Engine VM instance
                   through a set of configuration resources that provide
                   capabilities such as installing or removing software
                   packages, or executing a script.

                   For more information, see [OS policy and OS policy
                   assignment](\ https://cloud.google.com/compute/docs/os-configuration-management/working-with-os-policies).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, os_policy_assignment, os_policy_assignment_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = os_policy_assignments.CreateOSPolicyAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if os_policy_assignment is not None:
            request.os_policy_assignment = os_policy_assignment
        if os_policy_assignment_id is not None:
            request.os_policy_assignment_id = os_policy_assignment_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_os_policy_assignment,
            default_timeout=None,
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
            os_policy_assignments.OSPolicyAssignment,
            metadata_type=os_policy_assignments.OSPolicyAssignmentOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_os_policy_assignment(
        self,
        request: os_policy_assignments.UpdateOSPolicyAssignmentRequest = None,
        *,
        os_policy_assignment: os_policy_assignments.OSPolicyAssignment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update an existing OS policy assignment.

        This method creates a new revision of the OS policy assignment.

        This method returns a long running operation (LRO) that contains
        the rollout details. The rollout can be cancelled by cancelling
        the LRO.

        For more information, see `Method:
        projects.locations.osPolicyAssignments.operations.cancel <https://cloud.google.com/compute/docs/osconfig/rest/v1alpha/projects.locations.osPolicyAssignments.operations/cancel>`__.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.UpdateOSPolicyAssignmentRequest`):
                The request object. A request message to update an OS
                policy assignment
            os_policy_assignment (:class:`google.cloud.osconfig_v1alpha.types.OSPolicyAssignment`):
                Required. The updated OS policy
                assignment.

                This corresponds to the ``os_policy_assignment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Field mask that controls
                which fields of the assignment should be
                updated.

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be :class:`google.cloud.osconfig_v1alpha.types.OSPolicyAssignment` OS policy assignment is an API resource that is used to
                   apply a set of OS policies to a dynamically targeted
                   group of Compute Engine VM instances.

                   An OS policy is used to define the desired state
                   configuration for a Compute Engine VM instance
                   through a set of configuration resources that provide
                   capabilities such as installing or removing software
                   packages, or executing a script.

                   For more information, see [OS policy and OS policy
                   assignment](\ https://cloud.google.com/compute/docs/os-configuration-management/working-with-os-policies).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([os_policy_assignment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = os_policy_assignments.UpdateOSPolicyAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if os_policy_assignment is not None:
            request.os_policy_assignment = os_policy_assignment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_os_policy_assignment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("os_policy_assignment.name", request.os_policy_assignment.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            os_policy_assignments.OSPolicyAssignment,
            metadata_type=os_policy_assignments.OSPolicyAssignmentOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_os_policy_assignment(
        self,
        request: os_policy_assignments.GetOSPolicyAssignmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> os_policy_assignments.OSPolicyAssignment:
        r"""Retrieve an existing OS policy assignment.

        This method always returns the latest revision. In order to
        retrieve a previous revision of the assignment, also provide the
        revision ID in the ``name`` parameter.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.GetOSPolicyAssignmentRequest`):
                The request object. A request message to get an OS
                policy assignment
            name (:class:`str`):
                Required. The resource name of OS policy assignment.

                Format:
                ``projects/{project}/locations/{location}/osPolicyAssignments/{os_policy_assignment}@{revisionId}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.types.OSPolicyAssignment:
                OS policy assignment is an API resource that is used to
                   apply a set of OS policies to a dynamically targeted
                   group of Compute Engine VM instances.

                   An OS policy is used to define the desired state
                   configuration for a Compute Engine VM instance
                   through a set of configuration resources that provide
                   capabilities such as installing or removing software
                   packages, or executing a script.

                   For more information, see [OS policy and OS policy
                   assignment](\ https://cloud.google.com/compute/docs/os-configuration-management/working-with-os-policies).

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

        request = os_policy_assignments.GetOSPolicyAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_os_policy_assignment,
            default_timeout=None,
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

    async def list_os_policy_assignments(
        self,
        request: os_policy_assignments.ListOSPolicyAssignmentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOSPolicyAssignmentsAsyncPager:
        r"""List the OS policy assignments under the parent
        resource.
        For each OS policy assignment, the latest revision is
        returned.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.ListOSPolicyAssignmentsRequest`):
                The request object. A request message to list OS policy
                assignments for a parent resource
            parent (:class:`str`):
                Required. The parent resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.services.os_config_zonal_service.pagers.ListOSPolicyAssignmentsAsyncPager:
                A response message for listing all
                assignments under given parent.
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

        request = os_policy_assignments.ListOSPolicyAssignmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_os_policy_assignments,
            default_timeout=None,
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
        response = pagers.ListOSPolicyAssignmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_os_policy_assignment_revisions(
        self,
        request: os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOSPolicyAssignmentRevisionsAsyncPager:
        r"""List the OS policy assignment revisions for a given
        OS policy assignment.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.ListOSPolicyAssignmentRevisionsRequest`):
                The request object. A request message to list revisions
                for a OS policy assignment
            name (:class:`str`):
                Required. The name of the OS policy
                assignment to list revisions for.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.services.os_config_zonal_service.pagers.ListOSPolicyAssignmentRevisionsAsyncPager:
                A response message for listing all
                revisions for a OS policy assignment.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_os_policy_assignment_revisions,
            default_timeout=None,
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
        response = pagers.ListOSPolicyAssignmentRevisionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_os_policy_assignment(
        self,
        request: os_policy_assignments.DeleteOSPolicyAssignmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Delete the OS policy assignment.

        This method creates a new revision of the OS policy assignment.

        This method returns a long running operation (LRO) that contains
        the rollout details. The rollout can be cancelled by cancelling
        the LRO.

        If the LRO completes and is not cancelled, all revisions
        associated with the OS policy assignment are deleted.

        For more information, see `Method:
        projects.locations.osPolicyAssignments.operations.cancel <https://cloud.google.com/compute/docs/osconfig/rest/v1alpha/projects.locations.osPolicyAssignments.operations/cancel>`__.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.DeleteOSPolicyAssignmentRequest`):
                The request object. A request message for deleting a OS
                policy assignment.
            name (:class:`str`):
                Required. The name of the OS policy
                assignment to be deleted

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

                   The JSON representation for Empty is empty JSON
                   object {}.

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

        request = os_policy_assignments.DeleteOSPolicyAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_os_policy_assignment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=os_policy_assignments.OSPolicyAssignmentOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_instance_os_policies_compliance(
        self,
        request: instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance_os_policies_compliance.InstanceOSPoliciesCompliance:
        r"""Get OS policies compliance data for the specified
        Compute Engine VM instance.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.GetInstanceOSPoliciesComplianceRequest`):
                The request object. A request message for getting OS
                policies compliance data for the given Compute Engine VM
                instance.
            name (:class:`str`):
                Required. API resource name for instance OS policies
                compliance resource.

                Format:
                ``projects/{project}/locations/{location}/instanceOSPoliciesCompliances/{instance}``

                For ``{project}``, either Compute Engine project-number
                or project-id can be provided. For ``{instance}``,
                either Compute Engine VM instance-id or instance-name
                can be provided.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.types.InstanceOSPoliciesCompliance:
                This API resource represents the OS policies compliance data for a Compute
                   Engine virtual machine (VM) instance at a given point
                   in time.

                   A Compute Engine VM can have multiple OS policy
                   assignments, and each assignment can have multiple OS
                   policies. As a result, multiple OS policies could be
                   applied to a single VM.

                   You can use this API resource to determine both the
                   compliance state of your VM as well as the compliance
                   state of an individual OS policy.

                   For more information, see [View
                   compliance](\ https://cloud.google.com/compute/docs/os-configuration-management/view-compliance).

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

        request = instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance_os_policies_compliance,
            default_timeout=None,
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

    async def list_instance_os_policies_compliances(
        self,
        request: instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstanceOSPoliciesCompliancesAsyncPager:
        r"""List OS policies compliance data for all Compute
        Engine VM instances in the specified zone.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.ListInstanceOSPoliciesCompliancesRequest`):
                The request object. A request message for listing OS
                policies compliance data for all Compute Engine VMs in
                the given location.
            parent (:class:`str`):
                Required. The parent resource name.

                Format: ``projects/{project}/locations/{location}``

                For ``{project}``, either Compute Engine project-number
                or project-id can be provided.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.services.os_config_zonal_service.pagers.ListInstanceOSPoliciesCompliancesAsyncPager:
                A response message for listing OS
                policies compliance data for all Compute
                Engine VMs in the given location.
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

        request = instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instance_os_policies_compliances,
            default_timeout=None,
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
        response = pagers.ListInstanceOSPoliciesCompliancesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_inventory(
        self,
        request: inventory.GetInventoryRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> inventory.Inventory:
        r"""Get inventory data for the specified VM instance. If the VM has
        no associated inventory, the message ``NOT_FOUND`` is returned.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.GetInventoryRequest`):
                The request object. A request message for getting
                inventory data for the specified VM.
            name (:class:`str`):
                Required. API resource name for inventory resource.

                Format:
                ``projects/{project}/locations/{location}/instances/{instance}/inventory``

                For ``{project}``, either ``project-number`` or
                ``project-id`` can be provided. For ``{instance}``,
                either Compute Engine ``instance-id`` or
                ``instance-name`` can be provided.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.types.Inventory:
                This API resource represents the available inventory data for a
                   Compute Engine virtual machine (VM) instance at a
                   given point in time.

                   You can use this API resource to determine the
                   inventory data of your VM.

                   For more information, see [Information provided by OS
                   inventory
                   management](\ https://cloud.google.com/compute/docs/instances/os-inventory-management#data-collected).

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

        request = inventory.GetInventoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_inventory,
            default_timeout=None,
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

    async def list_inventories(
        self,
        request: inventory.ListInventoriesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInventoriesAsyncPager:
        r"""List inventory data for all VM instances in the
        specified zone.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.ListInventoriesRequest`):
                The request object. A request message for listing
                inventory data for all VMs in the specified location.
            parent (:class:`str`):
                Required. The parent resource name.

                Format:
                ``projects/{project}/locations/{location}/instances/{instance}``

                For ``{project}``, either ``project-number`` or
                ``project-id`` can be provided. For ``{instance}``, only
                hyphen or dash character is supported to list
                inventories across VMs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.services.os_config_zonal_service.pagers.ListInventoriesAsyncPager:
                A response message for listing
                inventory data for all VMs in a
                specified location.
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

        request = inventory.ListInventoriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_inventories,
            default_timeout=None,
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
        response = pagers.ListInventoriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_vulnerability_report(
        self,
        request: vulnerability.GetVulnerabilityReportRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> vulnerability.VulnerabilityReport:
        r"""Gets the vulnerability report for the specified VM
        instance. Only VMs with inventory data have
        vulnerability reports associated with them.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.GetVulnerabilityReportRequest`):
                The request object. A request message for getting the
                vulnerability report for the specified VM.
            name (:class:`str`):
                Required. API resource name for vulnerability resource.

                Format:
                ``projects/{project}/locations/{location}/instances/{instance}/vulnerabilityReport``

                For ``{project}``, either ``project-number`` or
                ``project-id`` can be provided. For ``{instance}``,
                either Compute Engine ``instance-id`` or
                ``instance-name`` can be provided.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.types.VulnerabilityReport:
                This API resource represents the vulnerability report for a specified
                   Compute Engine virtual machine (VM) instance at a
                   given point in time.

                   For more information, see [Vulnerability
                   reports](\ https://cloud.google.com/compute/docs/instances/os-inventory-management#vulnerability-reports).

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

        request = vulnerability.GetVulnerabilityReportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_vulnerability_report,
            default_timeout=None,
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

    async def list_vulnerability_reports(
        self,
        request: vulnerability.ListVulnerabilityReportsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVulnerabilityReportsAsyncPager:
        r"""List vulnerability reports for all VM instances in
        the specified zone.

        Args:
            request (:class:`google.cloud.osconfig_v1alpha.types.ListVulnerabilityReportsRequest`):
                The request object. A request message for listing
                vulnerability reports for all VM instances in the
                specified location.
            parent (:class:`str`):
                Required. The parent resource name.

                Format:
                ``projects/{project}/locations/{location}/instances/{instance}``

                For ``{project}``, either ``project-number`` or
                ``project-id`` can be provided. For ``{instance}``, only
                ``-`` character is supported to list vulnerability
                reports across VMs.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1alpha.services.os_config_zonal_service.pagers.ListVulnerabilityReportsAsyncPager:
                A response message for listing
                vulnerability reports for all VM
                instances in the specified location.
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

        request = vulnerability.ListVulnerabilityReportsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_vulnerability_reports,
            default_timeout=None,
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
        response = pagers.ListVulnerabilityReportsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-os-config",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("OsConfigZonalServiceAsyncClient",)
