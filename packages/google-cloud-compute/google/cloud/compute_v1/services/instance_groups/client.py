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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.compute_v1.services.instance_groups import pagers
from google.cloud.compute_v1.types import compute
from .transports.base import InstanceGroupsTransport, DEFAULT_CLIENT_INFO
from .transports.rest import InstanceGroupsRestTransport


class InstanceGroupsClientMeta(type):
    """Metaclass for the InstanceGroups client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[InstanceGroupsTransport]]
    _transport_registry["rest"] = InstanceGroupsRestTransport

    def get_transport_class(cls, label: str = None,) -> Type[InstanceGroupsTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class InstanceGroupsClient(metaclass=InstanceGroupsClientMeta):
    """The InstanceGroups API."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "compute.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            InstanceGroupsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            InstanceGroupsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> InstanceGroupsTransport:
        """Returns the transport used by the client instance.

        Returns:
            InstanceGroupsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, InstanceGroupsTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the instance groups client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, InstanceGroupsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, InstanceGroupsTransport):
            # transport is a InstanceGroupsTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def add_instances(
        self,
        request: compute.AddInstancesInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_add_instances_request_resource: compute.InstanceGroupsAddInstancesRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Adds a list of instances to the specified instance
        group. All of the instances in the instance group must
        be in the same network/subnetwork. Read  Adding
        instances for more information.

        Args:
            request (google.cloud.compute_v1.types.AddInstancesInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.AddInstances. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                you are adding instances.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_add_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsAddInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_add_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource.

                   Google Compute Engine has three Operation resources:

                   -  [Global](/compute/docs/reference/rest/{$api_version}/globalOperations)
                      \*
                      [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations)
                      \*
                      [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations)

                   You can use an operation resource to manage
                   asynchronous API requests. For more information, read
                   Handling API responses.

                   Operations can be global, regional or zonal. - For
                   global operations, use the globalOperations resource.
                   - For regional operations, use the regionOperations
                   resource. - For zonal operations, use the
                   zonalOperations resource.

                   For more information, read Global, Regional, and
                   Zonal Resources. (== resource_for
                   {$api_version}.globalOperations ==) (== resource_for
                   {$api_version}.regionOperations ==) (== resource_for
                   {$api_version}.zoneOperations ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_add_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddInstancesInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddInstancesInstanceGroupRequest):
            request = compute.AddInstancesInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_add_instances_request_resource is not None:
                request.instance_groups_add_instances_request_resource = (
                    instance_groups_add_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def aggregated_list(
        self,
        request: compute.AggregatedListInstanceGroupsRequest = None,
        *,
        project: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AggregatedListPager:
        r"""Retrieves the list of instance groups and sorts them
        by zone.

        Args:
            request (google.cloud.compute_v1.types.AggregatedListInstanceGroupsRequest):
                The request object. A request message for
                InstanceGroups.AggregatedList. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.AggregatedListPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AggregatedListInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AggregatedListInstanceGroupsRequest):
            request = compute.AggregatedListInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.aggregated_list]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.AggregatedListPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete(
        self,
        request: compute.DeleteInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified instance group. The instances
        in the group are not deleted. Note that instance group
        must not belong to a backend service. Read  Deleting an
        instance group for more information.

        Args:
            request (google.cloud.compute_v1.types.DeleteInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.Delete. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group to
                delete.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource.

                   Google Compute Engine has three Operation resources:

                   -  [Global](/compute/docs/reference/rest/{$api_version}/globalOperations)
                      \*
                      [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations)
                      \*
                      [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations)

                   You can use an operation resource to manage
                   asynchronous API requests. For more information, read
                   Handling API responses.

                   Operations can be global, regional or zonal. - For
                   global operations, use the globalOperations resource.
                   - For regional operations, use the regionOperations
                   resource. - For zonal operations, use the
                   zonalOperations resource.

                   For more information, read Global, Regional, and
                   Zonal Resources. (== resource_for
                   {$api_version}.globalOperations ==) (== resource_for
                   {$api_version}.regionOperations ==) (== resource_for
                   {$api_version}.zoneOperations ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteInstanceGroupRequest):
            request = compute.DeleteInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get(
        self,
        request: compute.GetInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstanceGroup:
        r"""Returns the specified zonal instance group. Get a
        list of available zonal instance groups by making a
        list() request.  For managed instance groups, use the
        instanceGroupManagers or regionInstanceGroupManagers
        methods instead.

        Args:
            request (google.cloud.compute_v1.types.GetInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.Get. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group.
                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.InstanceGroup:
                Represents an Instance Group resource.

                   Instance Groups can be used to configure a target for
                   load balancing.

                   Instance groups can either be managed or unmanaged.

                   To create managed instance groups, use the
                   instanceGroupManager or regionInstanceGroupManager
                   resource instead.

                   Use zonal unmanaged instance groups if you need to
                   apply load balancing to groups of heterogeneous
                   instances or if you need to manage the instances
                   yourself. You cannot create regional unmanaged
                   instance groups.

                   For more information, read Instance groups.

                   (== resource_for {$api_version}.instanceGroups ==)
                   (== resource_for {$api_version}.regionInstanceGroups
                   ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetInstanceGroupRequest):
            request = compute.GetInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def insert(
        self,
        request: compute.InsertInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group_resource: compute.InstanceGroup = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates an instance group in the specified project
        using the parameters that are included in the request.

        Args:
            request (google.cloud.compute_v1.types.InsertInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.Insert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where you want
                to create the instance group.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_resource (google.cloud.compute_v1.types.InstanceGroup):
                The body resource for this request
                This corresponds to the ``instance_group_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource.

                   Google Compute Engine has three Operation resources:

                   -  [Global](/compute/docs/reference/rest/{$api_version}/globalOperations)
                      \*
                      [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations)
                      \*
                      [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations)

                   You can use an operation resource to manage
                   asynchronous API requests. For more information, read
                   Handling API responses.

                   Operations can be global, regional or zonal. - For
                   global operations, use the globalOperations resource.
                   - For regional operations, use the regionOperations
                   resource. - For zonal operations, use the
                   zonalOperations resource.

                   For more information, read Global, Regional, and
                   Zonal Resources. (== resource_for
                   {$api_version}.globalOperations ==) (== resource_for
                   {$api_version}.regionOperations ==) (== resource_for
                   {$api_version}.zoneOperations ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, instance_group_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertInstanceGroupRequest):
            request = compute.InsertInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group_resource is not None:
                request.instance_group_resource = instance_group_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list(
        self,
        request: compute.ListInstanceGroupsRequest = None,
        *,
        project: str = None,
        zone: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Retrieves the list of zonal instance group resources
        contained within the specified zone.
        For managed instance groups, use the
        instanceGroupManagers or regionInstanceGroupManagers
        methods instead.

        Args:
            request (google.cloud.compute_v1.types.ListInstanceGroupsRequest):
                The request object. A request message for
                InstanceGroups.List. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.ListPager:
                A list of InstanceGroup resources.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListInstanceGroupsRequest):
            request = compute.ListInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_instances(
        self,
        request: compute.ListInstancesInstanceGroupsRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_list_instances_request_resource: compute.InstanceGroupsListInstancesRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesPager:
        r"""Lists the instances in the specified instance group.
        The orderBy query parameter is not supported.

        Args:
            request (google.cloud.compute_v1.types.ListInstancesInstanceGroupsRequest):
                The request object. A request message for
                InstanceGroups.ListInstances. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group from
                which you want to generate a list of
                included instances.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_list_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsListInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_list_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.instance_groups.pagers.ListInstancesPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_list_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListInstancesInstanceGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListInstancesInstanceGroupsRequest):
            request = compute.ListInstancesInstanceGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_list_instances_request_resource is not None:
                request.instance_groups_list_instances_request_resource = (
                    instance_groups_list_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInstancesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_instances(
        self,
        request: compute.RemoveInstancesInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_remove_instances_request_resource: compute.InstanceGroupsRemoveInstancesRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Removes one or more instances from the specified
        instance group, but does not delete those instances.  If
        the group is part of a backend service that has enabled
        connection draining, it can take up to 60 seconds after
        the connection draining duration before the VM instance
        is removed or deleted.

        Args:
            request (google.cloud.compute_v1.types.RemoveInstancesInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.RemoveInstances. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                the specified instances will be removed.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_remove_instances_request_resource (google.cloud.compute_v1.types.InstanceGroupsRemoveInstancesRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_remove_instances_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource.

                   Google Compute Engine has three Operation resources:

                   -  [Global](/compute/docs/reference/rest/{$api_version}/globalOperations)
                      \*
                      [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations)
                      \*
                      [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations)

                   You can use an operation resource to manage
                   asynchronous API requests. For more information, read
                   Handling API responses.

                   Operations can be global, regional or zonal. - For
                   global operations, use the globalOperations resource.
                   - For regional operations, use the regionOperations
                   resource. - For zonal operations, use the
                   zonalOperations resource.

                   For more information, read Global, Regional, and
                   Zonal Resources. (== resource_for
                   {$api_version}.globalOperations ==) (== resource_for
                   {$api_version}.regionOperations ==) (== resource_for
                   {$api_version}.zoneOperations ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_remove_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveInstancesInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveInstancesInstanceGroupRequest):
            request = compute.RemoveInstancesInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_remove_instances_request_resource is not None:
                request.instance_groups_remove_instances_request_resource = (
                    instance_groups_remove_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_instances]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def set_named_ports(
        self,
        request: compute.SetNamedPortsInstanceGroupRequest = None,
        *,
        project: str = None,
        zone: str = None,
        instance_group: str = None,
        instance_groups_set_named_ports_request_resource: compute.InstanceGroupsSetNamedPortsRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the named ports for the specified instance
        group.

        Args:
            request (google.cloud.compute_v1.types.SetNamedPortsInstanceGroupRequest):
                The request object. A request message for
                InstanceGroups.SetNamedPorts. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone where the
                instance group is located.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group (str):
                The name of the instance group where
                the named ports are updated.

                This corresponds to the ``instance_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_groups_set_named_ports_request_resource (google.cloud.compute_v1.types.InstanceGroupsSetNamedPortsRequest):
                The body resource for this request
                This corresponds to the ``instance_groups_set_named_ports_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Operation:
                Represents an Operation resource.

                   Google Compute Engine has three Operation resources:

                   -  [Global](/compute/docs/reference/rest/{$api_version}/globalOperations)
                      \*
                      [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations)
                      \*
                      [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations)

                   You can use an operation resource to manage
                   asynchronous API requests. For more information, read
                   Handling API responses.

                   Operations can be global, regional or zonal. - For
                   global operations, use the globalOperations resource.
                   - For regional operations, use the regionOperations
                   resource. - For zonal operations, use the
                   zonalOperations resource.

                   For more information, read Global, Regional, and
                   Zonal Resources. (== resource_for
                   {$api_version}.globalOperations ==) (== resource_for
                   {$api_version}.regionOperations ==) (== resource_for
                   {$api_version}.zoneOperations ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                project,
                zone,
                instance_group,
                instance_groups_set_named_ports_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetNamedPortsInstanceGroupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetNamedPortsInstanceGroupRequest):
            request = compute.SetNamedPortsInstanceGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if instance_group is not None:
                request.instance_group = instance_group
            if instance_groups_set_named_ports_request_resource is not None:
                request.instance_groups_set_named_ports_request_resource = (
                    instance_groups_set_named_ports_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_named_ports]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("InstanceGroupsClient",)
