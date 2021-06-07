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

from google.cloud.compute_v1.services.security_policies import pagers
from google.cloud.compute_v1.types import compute
from .transports.base import SecurityPoliciesTransport, DEFAULT_CLIENT_INFO
from .transports.rest import SecurityPoliciesRestTransport


class SecurityPoliciesClientMeta(type):
    """Metaclass for the SecurityPolicies client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SecurityPoliciesTransport]]
    _transport_registry["rest"] = SecurityPoliciesRestTransport

    def get_transport_class(cls, label: str = None,) -> Type[SecurityPoliciesTransport]:
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


class SecurityPoliciesClient(metaclass=SecurityPoliciesClientMeta):
    """The SecurityPolicies API."""

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
            SecurityPoliciesClient: The constructed client.
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
            SecurityPoliciesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SecurityPoliciesTransport:
        """Returns the transport used by the client instance.

        Returns:
            SecurityPoliciesTransport: The transport used by the client
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
        transport: Union[str, SecurityPoliciesTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the security policies client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, SecurityPoliciesTransport]): The
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
        if isinstance(transport, SecurityPoliciesTransport):
            # transport is a SecurityPoliciesTransport instance.
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

    def add_rule(
        self,
        request: compute.AddRuleSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        security_policy_rule_resource: compute.SecurityPolicyRule = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Inserts a rule into a security policy.

        Args:
            request (google.cloud.compute_v1.types.AddRuleSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.AddRule. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to
                update.

                This corresponds to the ``security_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy_rule_resource (google.cloud.compute_v1.types.SecurityPolicyRule):
                The body resource for this request
                This corresponds to the ``security_policy_rule_resource`` field
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
            [project, security_policy, security_policy_rule_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.AddRuleSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.AddRuleSecurityPolicyRequest):
            request = compute.AddRuleSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy
            if security_policy_rule_resource is not None:
                request.security_policy_rule_resource = security_policy_rule_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete(
        self,
        request: compute.DeleteSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified policy.

        Args:
            request (google.cloud.compute_v1.types.DeleteSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.Delete. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to
                delete.

                This corresponds to the ``security_policy`` field
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
        has_flattened_params = any([project, security_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.DeleteSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.DeleteSecurityPolicyRequest):
            request = compute.DeleteSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get(
        self,
        request: compute.GetSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SecurityPolicy:
        r"""List all of the ordered rules present in a single
        specified policy.

        Args:
            request (google.cloud.compute_v1.types.GetSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.Get. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to get.
                This corresponds to the ``security_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.SecurityPolicy:
                Represents a Google Cloud Armor security policy
                resource.

                   Only external backend services that use load
                   balancers can reference a security policy. For more
                   information, see Google Cloud Armor security policy
                   overview. (== resource_for
                   {$api_version}.securityPolicies ==)

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, security_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetSecurityPolicyRequest):
            request = compute.GetSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_rule(
        self,
        request: compute.GetRuleSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SecurityPolicyRule:
        r"""Gets a rule at the specified priority.

        Args:
            request (google.cloud.compute_v1.types.GetRuleSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.GetRule. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to which
                the queried rule belongs.

                This corresponds to the ``security_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.SecurityPolicyRule:
                Represents a rule that describes one
                or more match conditions along with the
                action to be taken when traffic matches
                this condition (allow or deny).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, security_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.GetRuleSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.GetRuleSecurityPolicyRequest):
            request = compute.GetRuleSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def insert(
        self,
        request: compute.InsertSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy_resource: compute.SecurityPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates a new policy in the specified project using
        the data included in the request.

        Args:
            request (google.cloud.compute_v1.types.InsertSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.Insert. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy_resource (google.cloud.compute_v1.types.SecurityPolicy):
                The body resource for this request
                This corresponds to the ``security_policy_resource`` field
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
        has_flattened_params = any([project, security_policy_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.InsertSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.InsertSecurityPolicyRequest):
            request = compute.InsertSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy_resource is not None:
                request.security_policy_resource = security_policy_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list(
        self,
        request: compute.ListSecurityPoliciesRequest = None,
        *,
        project: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""List all the policies that have been configured for
        the specified project.

        Args:
            request (google.cloud.compute_v1.types.ListSecurityPoliciesRequest):
                The request object. A request message for
                SecurityPolicies.List. See the method description for
                details.
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
            google.cloud.compute_v1.services.security_policies.pagers.ListPager:
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
        # in a compute.ListSecurityPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.ListSecurityPoliciesRequest):
            request = compute.ListSecurityPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

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

    def list_preconfigured_expression_sets(
        self,
        request: compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest = None,
        *,
        project: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SecurityPoliciesListPreconfiguredExpressionSetsResponse:
        r"""Gets the current list of preconfigured Web
        Application Firewall (WAF) expressions.

        Args:
            request (google.cloud.compute_v1.types.ListPreconfiguredExpressionSetsSecurityPoliciesRequest):
                The request object. A request message for
                SecurityPolicies.ListPreconfiguredExpressionSets. See
                the method description for details.
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
            google.cloud.compute_v1.types.SecurityPoliciesListPreconfiguredExpressionSetsResponse:

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
        # in a compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest
        ):
            request = compute.ListPreconfiguredExpressionSetsSecurityPoliciesRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_preconfigured_expression_sets
        ]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def patch(
        self,
        request: compute.PatchSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        security_policy_resource: compute.SecurityPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Patches the specified policy with the data included
        in the request. This cannot be used to be update the
        rules in the policy. Please use the per rule methods
        like addRule, patchRule, and removeRule instead.

        Args:
            request (google.cloud.compute_v1.types.PatchSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.Patch. See the method description for
                details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to
                update.

                This corresponds to the ``security_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy_resource (google.cloud.compute_v1.types.SecurityPolicy):
                The body resource for this request
                This corresponds to the ``security_policy_resource`` field
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
        has_flattened_params = any([project, security_policy, security_policy_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.PatchSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.PatchSecurityPolicyRequest):
            request = compute.PatchSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy
            if security_policy_resource is not None:
                request.security_policy_resource = security_policy_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def patch_rule(
        self,
        request: compute.PatchRuleSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        security_policy_rule_resource: compute.SecurityPolicyRule = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Patches a rule at the specified priority.

        Args:
            request (google.cloud.compute_v1.types.PatchRuleSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.PatchRule. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to
                update.

                This corresponds to the ``security_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy_rule_resource (google.cloud.compute_v1.types.SecurityPolicyRule):
                The body resource for this request
                This corresponds to the ``security_policy_rule_resource`` field
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
            [project, security_policy, security_policy_rule_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.PatchRuleSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.PatchRuleSecurityPolicyRequest):
            request = compute.PatchRuleSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy
            if security_policy_rule_resource is not None:
                request.security_policy_rule_resource = security_policy_rule_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch_rule]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def remove_rule(
        self,
        request: compute.RemoveRuleSecurityPolicyRequest = None,
        *,
        project: str = None,
        security_policy: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes a rule at the specified priority.

        Args:
            request (google.cloud.compute_v1.types.RemoveRuleSecurityPolicyRequest):
                The request object. A request message for
                SecurityPolicies.RemoveRule. See the method description
                for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            security_policy (str):
                Name of the security policy to
                update.

                This corresponds to the ``security_policy`` field
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
        has_flattened_params = any([project, security_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a compute.RemoveRuleSecurityPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, compute.RemoveRuleSecurityPolicyRequest):
            request = compute.RemoveRuleSecurityPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if security_policy is not None:
                request.security_policy = security_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_rule]

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


__all__ = ("SecurityPoliciesClient",)
