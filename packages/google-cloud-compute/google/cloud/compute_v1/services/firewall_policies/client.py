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

from google.cloud.compute_v1.services.firewall_policies import pagers
from google.cloud.compute_v1.types import compute
from .transports.base import FirewallPoliciesTransport, DEFAULT_CLIENT_INFO
from .transports.rest import FirewallPoliciesRestTransport


class FirewallPoliciesClientMeta(type):
    """Metaclass for the FirewallPolicies client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[FirewallPoliciesTransport]]
    _transport_registry["rest"] = FirewallPoliciesRestTransport

    def get_transport_class(cls, label: str = None,) -> Type[FirewallPoliciesTransport]:
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


class FirewallPoliciesClient(metaclass=FirewallPoliciesClientMeta):
    """The FirewallPolicies API."""

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
            FirewallPoliciesClient: The constructed client.
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
            FirewallPoliciesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FirewallPoliciesTransport:
        """Returns the transport used by the client instance.

        Returns:
            FirewallPoliciesTransport: The transport used by the client
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
        transport: Union[str, FirewallPoliciesTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the firewall policies client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, FirewallPoliciesTransport]): The
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
        if isinstance(transport, FirewallPoliciesTransport):
            # transport is a FirewallPoliciesTransport instance.
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

    def add_association(
        self,
        request: compute.AddAssociationFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        firewall_policy_association_resource: compute.FirewallPolicyAssociation = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Inserts an association for the specified firewall
        policy.

        Args:
            request (google.cloud.compute_v1.types.AddAssociationFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.AddAssociation. See the method
                description for details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firewall_policy_association_resource (google.cloud.compute_v1.types.FirewallPolicyAssociation):
                The body resource for this request
                This corresponds to the ``firewall_policy_association_resource`` field
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
            [firewall_policy, firewall_policy_association_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddAssociationFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddAssociationFirewallPolicyRequest):
            request = compute.AddAssociationFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy
            if firewall_policy_association_resource is not None:
                request.firewall_policy_association_resource = (
                    firewall_policy_association_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_association]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def add_rule(
        self,
        request: compute.AddRuleFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        firewall_policy_rule_resource: compute.FirewallPolicyRule = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Inserts a rule into a firewall policy.

        Args:
            request (google.cloud.compute_v1.types.AddRuleFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.AddRule. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firewall_policy_rule_resource (google.cloud.compute_v1.types.FirewallPolicyRule):
                The body resource for this request
                This corresponds to the ``firewall_policy_rule_resource`` field
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
        has_flattened_params = any([firewall_policy, firewall_policy_rule_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddRuleFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddRuleFirewallPolicyRequest):
            request = compute.AddRuleFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy
            if firewall_policy_rule_resource is not None:
                request.firewall_policy_rule_resource = firewall_policy_rule_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def clone_rules(
        self,
        request: compute.CloneRulesFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Copies rules to the specified firewall policy.

        Args:
            request (google.cloud.compute_v1.types.CloneRulesFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.CloneRules. See the method description
                for details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
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
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.CloneRulesFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.CloneRulesFirewallPolicyRequest):
            request = compute.CloneRulesFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.clone_rules]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete(
        self,
        request: compute.DeleteFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified policy.

        Args:
            request (google.cloud.compute_v1.types.DeleteFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.Delete. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to
                delete.

                This corresponds to the ``firewall_policy`` field
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
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteFirewallPolicyRequest):
            request = compute.DeleteFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get(
        self,
        request: compute.GetFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.FirewallPolicy:
        r"""Returns the specified firewall policy.

        Args:
            request (google.cloud.compute_v1.types.GetFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.Get. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to get.
                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.FirewallPolicy:
                Represents a Firewall Policy resource. (== resource_for
                {$api_version}.firewallPolicies ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetFirewallPolicyRequest):
            request = compute.GetFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_association(
        self,
        request: compute.GetAssociationFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.FirewallPolicyAssociation:
        r"""Gets an association with the specified name.

        Args:
            request (google.cloud.compute_v1.types.GetAssociationFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.GetAssociation. See the method
                description for details.
            firewall_policy (str):
                Name of the firewall policy to which
                the queried rule belongs.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.FirewallPolicyAssociation:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetAssociationFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetAssociationFirewallPolicyRequest):
            request = compute.GetAssociationFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_association]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: compute.GetIamPolicyFirewallPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Gets the access control policy for a resource. May be
        empty if no such policy or resource exists.

        Args:
            request (google.cloud.compute_v1.types.GetIamPolicyFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.GetIamPolicy. See the method
                description for details.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions; each role can be an IAM predefined role
                   or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   { "bindings": [ { "role":
                   "roles/resourcemanager.organizationAdmin", "members":
                   [ "user:mike@example.com",
                   "group:admins@example.com", "domain:google.com",
                   "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                   ] }, { "role":
                   "roles/resourcemanager.organizationViewer",
                   "members": [ "user:eve@example.com" ], "condition": {
                   "title": "expirable access", "description": "Does not
                   grant access after Sep 2020", "expression":
                   "request.time <
                   timestamp('2020-10-01T00:00:00.000Z')", } } ],
                   "etag": "BwWWja0YfJA=", "version": 3 }

                   **YAML example:**

                   bindings: - members: - user:\ mike@example.com -
                   group:\ admins@example.com - domain:google.com -
                   serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                   role: roles/resourcemanager.organizationAdmin -
                   members: - user:\ eve@example.com role:
                   roles/resourcemanager.organizationViewer condition:
                   title: expirable access description: Does not grant
                   access after Sep 2020 expression: request.time <
                   timestamp('2020-10-01T00:00:00.000Z') - etag:
                   BwWWja0YfJA= - version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

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

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetIamPolicyFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetIamPolicyFirewallPolicyRequest):
            request = compute.GetIamPolicyFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_rule(
        self,
        request: compute.GetRuleFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.FirewallPolicyRule:
        r"""Gets a rule of the specified priority.

        Args:
            request (google.cloud.compute_v1.types.GetRuleFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.GetRule. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to which
                the queried rule belongs.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.FirewallPolicyRule:
                Represents a rule that describes one
                or more match conditions along with the
                action to be taken when traffic matches
                this condition (allow or deny).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetRuleFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetRuleFirewallPolicyRequest):
            request = compute.GetRuleFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def insert(
        self,
        request: compute.InsertFirewallPolicyRequest = None,
        *,
        firewall_policy_resource: compute.FirewallPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates a new policy in the specified project using
        the data included in the request.

        Args:
            request (google.cloud.compute_v1.types.InsertFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.Insert. See the method description for
                details.
            firewall_policy_resource (google.cloud.compute_v1.types.FirewallPolicy):
                The body resource for this request
                This corresponds to the ``firewall_policy_resource`` field
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
        has_flattened_params = any([firewall_policy_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertFirewallPolicyRequest):
            request = compute.InsertFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy_resource is not None:
                request.firewall_policy_resource = firewall_policy_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list(
        self,
        request: compute.ListFirewallPoliciesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Lists all the policies that have been configured for
        the specified project.

        Args:
            request (google.cloud.compute_v1.types.ListFirewallPoliciesRequest):
                The request object. A request message for
                FirewallPolicies.List. See the method description for
                details.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.firewall_policies.pagers.ListPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListFirewallPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListFirewallPoliciesRequest):
            request = compute.ListFirewallPoliciesRequest(request)

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

    def list_associations(
        self,
        request: compute.ListAssociationsFirewallPolicyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.FirewallPoliciesListAssociationsResponse:
        r"""Lists associations of a specified target, i.e.,
        organization or folder.

        Args:
            request (google.cloud.compute_v1.types.ListAssociationsFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.ListAssociations. See the method
                description for details.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.FirewallPoliciesListAssociationsResponse:

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a compute.ListAssociationsFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListAssociationsFirewallPolicyRequest):
            request = compute.ListAssociationsFirewallPolicyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_associations]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def move(
        self,
        request: compute.MoveFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Moves the specified firewall policy.

        Args:
            request (google.cloud.compute_v1.types.MoveFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.Move. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
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
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.MoveFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.MoveFirewallPolicyRequest):
            request = compute.MoveFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.move]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def patch(
        self,
        request: compute.PatchFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        firewall_policy_resource: compute.FirewallPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Patches the specified policy with the data included
        in the request.

        Args:
            request (google.cloud.compute_v1.types.PatchFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.Patch. See the method description for
                details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firewall_policy_resource (google.cloud.compute_v1.types.FirewallPolicy):
                The body resource for this request
                This corresponds to the ``firewall_policy_resource`` field
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
        has_flattened_params = any([firewall_policy, firewall_policy_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.PatchFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.PatchFirewallPolicyRequest):
            request = compute.PatchFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy
            if firewall_policy_resource is not None:
                request.firewall_policy_resource = firewall_policy_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def patch_rule(
        self,
        request: compute.PatchRuleFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        firewall_policy_rule_resource: compute.FirewallPolicyRule = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Patches a rule of the specified priority.

        Args:
            request (google.cloud.compute_v1.types.PatchRuleFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.PatchRule. See the method description
                for details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firewall_policy_rule_resource (google.cloud.compute_v1.types.FirewallPolicyRule):
                The body resource for this request
                This corresponds to the ``firewall_policy_rule_resource`` field
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
        has_flattened_params = any([firewall_policy, firewall_policy_rule_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.PatchRuleFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.PatchRuleFirewallPolicyRequest):
            request = compute.PatchRuleFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy
            if firewall_policy_rule_resource is not None:
                request.firewall_policy_rule_resource = firewall_policy_rule_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def remove_association(
        self,
        request: compute.RemoveAssociationFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Removes an association for the specified firewall
        policy.

        Args:
            request (google.cloud.compute_v1.types.RemoveAssociationFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.RemoveAssociation. See the method
                description for details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
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
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveAssociationFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveAssociationFirewallPolicyRequest):
            request = compute.RemoveAssociationFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_association]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def remove_rule(
        self,
        request: compute.RemoveRuleFirewallPolicyRequest = None,
        *,
        firewall_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes a rule of the specified priority.

        Args:
            request (google.cloud.compute_v1.types.RemoveRuleFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.RemoveRule. See the method description
                for details.
            firewall_policy (str):
                Name of the firewall policy to
                update.

                This corresponds to the ``firewall_policy`` field
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
        has_flattened_params = any([firewall_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveRuleFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveRuleFirewallPolicyRequest):
            request = compute.RemoveRuleFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if firewall_policy is not None:
                request.firewall_policy = firewall_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: compute.SetIamPolicyFirewallPolicyRequest = None,
        *,
        resource: str = None,
        global_organization_set_policy_request_resource: compute.GlobalOrganizationSetPolicyRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Sets the access control policy on the specified
        resource. Replaces any existing policy.

        Args:
            request (google.cloud.compute_v1.types.SetIamPolicyFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.SetIamPolicy. See the method
                description for details.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            global_organization_set_policy_request_resource (google.cloud.compute_v1.types.GlobalOrganizationSetPolicyRequest):
                The body resource for this request
                This corresponds to the ``global_organization_set_policy_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions; each role can be an IAM predefined role
                   or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   { "bindings": [ { "role":
                   "roles/resourcemanager.organizationAdmin", "members":
                   [ "user:mike@example.com",
                   "group:admins@example.com", "domain:google.com",
                   "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                   ] }, { "role":
                   "roles/resourcemanager.organizationViewer",
                   "members": [ "user:eve@example.com" ], "condition": {
                   "title": "expirable access", "description": "Does not
                   grant access after Sep 2020", "expression":
                   "request.time <
                   timestamp('2020-10-01T00:00:00.000Z')", } } ],
                   "etag": "BwWWja0YfJA=", "version": 3 }

                   **YAML example:**

                   bindings: - members: - user:\ mike@example.com -
                   group:\ admins@example.com - domain:google.com -
                   serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                   role: roles/resourcemanager.organizationAdmin -
                   members: - user:\ eve@example.com role:
                   roles/resourcemanager.organizationViewer condition:
                   title: expirable access description: Does not grant
                   access after Sep 2020 expression: request.time <
                   timestamp('2020-10-01T00:00:00.000Z') - etag:
                   BwWWja0YfJA= - version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [resource, global_organization_set_policy_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.SetIamPolicyFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.SetIamPolicyFirewallPolicyRequest):
            request = compute.SetIamPolicyFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if resource is not None:
                request.resource = resource
            if global_organization_set_policy_request_resource is not None:
                request.global_organization_set_policy_request_resource = (
                    global_organization_set_policy_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: compute.TestIamPermissionsFirewallPolicyRequest = None,
        *,
        resource: str = None,
        test_permissions_request_resource: compute.TestPermissionsRequest = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TestPermissionsResponse:
        r"""Returns permissions that a caller has on the
        specified resource.

        Args:
            request (google.cloud.compute_v1.types.TestIamPermissionsFirewallPolicyRequest):
                The request object. A request message for
                FirewallPolicies.TestIamPermissions. See the method
                description for details.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            test_permissions_request_resource (google.cloud.compute_v1.types.TestPermissionsRequest):
                The body resource for this request
                This corresponds to the ``test_permissions_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.TestPermissionsResponse:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, test_permissions_request_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.TestIamPermissionsFirewallPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.TestIamPermissionsFirewallPolicyRequest):
            request = compute.TestIamPermissionsFirewallPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if resource is not None:
                request.resource = resource
            if test_permissions_request_resource is not None:
                request.test_permissions_request_resource = (
                    test_permissions_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

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


__all__ = ("FirewallPoliciesClient",)
