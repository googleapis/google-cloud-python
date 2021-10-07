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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.network_security_v1beta1.services.network_security import pagers
from google.cloud.network_security_v1beta1.types import authorization_policy
from google.cloud.network_security_v1beta1.types import (
    authorization_policy as gcn_authorization_policy,
)
from google.cloud.network_security_v1beta1.types import client_tls_policy
from google.cloud.network_security_v1beta1.types import (
    client_tls_policy as gcn_client_tls_policy,
)
from google.cloud.network_security_v1beta1.types import common
from google.cloud.network_security_v1beta1.types import server_tls_policy
from google.cloud.network_security_v1beta1.types import (
    server_tls_policy as gcn_server_tls_policy,
)
from google.cloud.network_security_v1beta1.types import tls
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import NetworkSecurityTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import NetworkSecurityGrpcTransport
from .transports.grpc_asyncio import NetworkSecurityGrpcAsyncIOTransport


class NetworkSecurityClientMeta(type):
    """Metaclass for the NetworkSecurity client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[NetworkSecurityTransport]]
    _transport_registry["grpc"] = NetworkSecurityGrpcTransport
    _transport_registry["grpc_asyncio"] = NetworkSecurityGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[NetworkSecurityTransport]:
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


class NetworkSecurityClient(metaclass=NetworkSecurityClientMeta):
    """"""

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

    DEFAULT_ENDPOINT = "networksecurity.googleapis.com"
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
            NetworkSecurityClient: The constructed client.
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
            NetworkSecurityClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> NetworkSecurityTransport:
        """Returns the transport used by the client instance.

        Returns:
            NetworkSecurityTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def authorization_policy_path(
        project: str, location: str, authorization_policy: str,
    ) -> str:
        """Returns a fully-qualified authorization_policy string."""
        return "projects/{project}/locations/{location}/authorizationPolicies/{authorization_policy}".format(
            project=project,
            location=location,
            authorization_policy=authorization_policy,
        )

    @staticmethod
    def parse_authorization_policy_path(path: str) -> Dict[str, str]:
        """Parses a authorization_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/authorizationPolicies/(?P<authorization_policy>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def client_tls_policy_path(
        project: str, location: str, client_tls_policy: str,
    ) -> str:
        """Returns a fully-qualified client_tls_policy string."""
        return "projects/{project}/locations/{location}/clientTlsPolicies/{client_tls_policy}".format(
            project=project, location=location, client_tls_policy=client_tls_policy,
        )

    @staticmethod
    def parse_client_tls_policy_path(path: str) -> Dict[str, str]:
        """Parses a client_tls_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/clientTlsPolicies/(?P<client_tls_policy>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def server_tls_policy_path(
        project: str, location: str, server_tls_policy: str,
    ) -> str:
        """Returns a fully-qualified server_tls_policy string."""
        return "projects/{project}/locations/{location}/serverTlsPolicies/{server_tls_policy}".format(
            project=project, location=location, server_tls_policy=server_tls_policy,
        )

    @staticmethod
    def parse_server_tls_policy_path(path: str) -> Dict[str, str]:
        """Parses a server_tls_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/serverTlsPolicies/(?P<server_tls_policy>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

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
        transport: Union[str, NetworkSecurityTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the network security client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, NetworkSecurityTransport]): The
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
        if isinstance(transport, NetworkSecurityTransport):
            # transport is a NetworkSecurityTransport instance.
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
                always_use_jwt_access=True,
            )

    def list_authorization_policies(
        self,
        request: Union[
            authorization_policy.ListAuthorizationPoliciesRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAuthorizationPoliciesPager:
        r"""Lists AuthorizationPolicies in a given project and
        location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.ListAuthorizationPoliciesRequest, dict]):
                The request object. Request used with the
                ListAuthorizationPolicies method.
            parent (str):
                Required. The project and location from which the
                AuthorizationPolicies should be listed, specified in the
                format ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.services.network_security.pagers.ListAuthorizationPoliciesPager:
                Response returned by the
                ListAuthorizationPolicies method.
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

        # Minor optimization to avoid making a copy if the user passes
        # in a authorization_policy.ListAuthorizationPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, authorization_policy.ListAuthorizationPoliciesRequest
        ):
            request = authorization_policy.ListAuthorizationPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_authorization_policies
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAuthorizationPoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_authorization_policy(
        self,
        request: Union[authorization_policy.GetAuthorizationPolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> authorization_policy.AuthorizationPolicy:
        r"""Gets details of a single AuthorizationPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.GetAuthorizationPolicyRequest, dict]):
                The request object. Request used by the
                GetAuthorizationPolicy method.
            name (str):
                Required. A name of the AuthorizationPolicy to get. Must
                be in the format
                ``projects/{project}/locations/{location}/authorizationPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.types.AuthorizationPolicy:
                AuthorizationPolicy is a resource
                that specifies how a server should
                authorize incoming connections. This
                resource in itself does not change the
                configuration unless it's attached to a
                target https proxy or endpoint config
                selector resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a authorization_policy.GetAuthorizationPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, authorization_policy.GetAuthorizationPolicyRequest):
            request = authorization_policy.GetAuthorizationPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_authorization_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_authorization_policy(
        self,
        request: Union[
            gcn_authorization_policy.CreateAuthorizationPolicyRequest, dict
        ] = None,
        *,
        parent: str = None,
        authorization_policy: gcn_authorization_policy.AuthorizationPolicy = None,
        authorization_policy_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new AuthorizationPolicy in a given project
        and location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.CreateAuthorizationPolicyRequest, dict]):
                The request object. Request used by the
                CreateAuthorizationPolicy method.
            parent (str):
                Required. The parent resource of the
                AuthorizationPolicy. Must be in the format
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            authorization_policy (google.cloud.network_security_v1beta1.types.AuthorizationPolicy):
                Required. AuthorizationPolicy
                resource to be created.

                This corresponds to the ``authorization_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            authorization_policy_id (str):
                Required. Short name of the AuthorizationPolicy resource
                to be created. This value should be 1-63 characters
                long, containing only letters, numbers, hyphens, and
                underscores, and should not start with a number. E.g.
                "authz_policy".

                This corresponds to the ``authorization_policy_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.AuthorizationPolicy` AuthorizationPolicy is a resource that specifies how a server
                   should authorize incoming connections. This resource
                   in itself does not change the configuration unless
                   it's attached to a target https proxy or endpoint
                   config selector resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, authorization_policy, authorization_policy_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_authorization_policy.CreateAuthorizationPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcn_authorization_policy.CreateAuthorizationPolicyRequest
        ):
            request = gcn_authorization_policy.CreateAuthorizationPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if authorization_policy is not None:
                request.authorization_policy = authorization_policy
            if authorization_policy_id is not None:
                request.authorization_policy_id = authorization_policy_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_authorization_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_authorization_policy.AuthorizationPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_authorization_policy(
        self,
        request: Union[
            gcn_authorization_policy.UpdateAuthorizationPolicyRequest, dict
        ] = None,
        *,
        authorization_policy: gcn_authorization_policy.AuthorizationPolicy = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single
        AuthorizationPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.UpdateAuthorizationPolicyRequest, dict]):
                The request object. Request used by the
                UpdateAuthorizationPolicy method.
            authorization_policy (google.cloud.network_security_v1beta1.types.AuthorizationPolicy):
                Required. Updated AuthorizationPolicy
                resource.

                This corresponds to the ``authorization_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Field mask is used to specify the fields to be
                overwritten in the AuthorizationPolicy resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.AuthorizationPolicy` AuthorizationPolicy is a resource that specifies how a server
                   should authorize incoming connections. This resource
                   in itself does not change the configuration unless
                   it's attached to a target https proxy or endpoint
                   config selector resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([authorization_policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_authorization_policy.UpdateAuthorizationPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcn_authorization_policy.UpdateAuthorizationPolicyRequest
        ):
            request = gcn_authorization_policy.UpdateAuthorizationPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if authorization_policy is not None:
                request.authorization_policy = authorization_policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_authorization_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("authorization_policy.name", request.authorization_policy.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_authorization_policy.AuthorizationPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_authorization_policy(
        self,
        request: Union[
            authorization_policy.DeleteAuthorizationPolicyRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single AuthorizationPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.DeleteAuthorizationPolicyRequest, dict]):
                The request object. Request used by the
                DeleteAuthorizationPolicy method.
            name (str):
                Required. A name of the AuthorizationPolicy to delete.
                Must be in the format
                ``projects/{project}/locations/{location}/authorizationPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a authorization_policy.DeleteAuthorizationPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, authorization_policy.DeleteAuthorizationPolicyRequest
        ):
            request = authorization_policy.DeleteAuthorizationPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_authorization_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_server_tls_policies(
        self,
        request: Union[server_tls_policy.ListServerTlsPoliciesRequest, dict] = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServerTlsPoliciesPager:
        r"""Lists ServerTlsPolicies in a given project and
        location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.ListServerTlsPoliciesRequest, dict]):
                The request object. Request used by the
                ListServerTlsPolicies method.
            parent (str):
                Required. The project and location from which the
                ServerTlsPolicies should be listed, specified in the
                format ``projects/*/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.services.network_security.pagers.ListServerTlsPoliciesPager:
                Response returned by the
                ListServerTlsPolicies method.
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

        # Minor optimization to avoid making a copy if the user passes
        # in a server_tls_policy.ListServerTlsPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, server_tls_policy.ListServerTlsPoliciesRequest):
            request = server_tls_policy.ListServerTlsPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_server_tls_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServerTlsPoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_server_tls_policy(
        self,
        request: Union[server_tls_policy.GetServerTlsPolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> server_tls_policy.ServerTlsPolicy:
        r"""Gets details of a single ServerTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.GetServerTlsPolicyRequest, dict]):
                The request object. Request used by the
                GetServerTlsPolicy method.
            name (str):
                Required. A name of the ServerTlsPolicy to get. Must be
                in the format
                ``projects/*/locations/{location}/serverTlsPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.types.ServerTlsPolicy:
                ServerTlsPolicy is a resource that
                specifies how a server should
                authenticate incoming requests. This
                resource itself does not affect
                configuration unless it is attached to a
                target https proxy or endpoint config
                selector resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a server_tls_policy.GetServerTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, server_tls_policy.GetServerTlsPolicyRequest):
            request = server_tls_policy.GetServerTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_server_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_server_tls_policy(
        self,
        request: Union[gcn_server_tls_policy.CreateServerTlsPolicyRequest, dict] = None,
        *,
        parent: str = None,
        server_tls_policy: gcn_server_tls_policy.ServerTlsPolicy = None,
        server_tls_policy_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new ServerTlsPolicy in a given project and
        location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.CreateServerTlsPolicyRequest, dict]):
                The request object. Request used by the
                CreateServerTlsPolicy method.
            parent (str):
                Required. The parent resource of the ServerTlsPolicy.
                Must be in the format
                ``projects/*/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            server_tls_policy (google.cloud.network_security_v1beta1.types.ServerTlsPolicy):
                Required. ServerTlsPolicy resource to
                be created.

                This corresponds to the ``server_tls_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            server_tls_policy_id (str):
                Required. Short name of the ServerTlsPolicy resource to
                be created. This value should be 1-63 characters long,
                containing only letters, numbers, hyphens, and
                underscores, and should not start with a number. E.g.
                "server_mtls_policy".

                This corresponds to the ``server_tls_policy_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.ServerTlsPolicy` ServerTlsPolicy is a resource that specifies how a server should authenticate
                   incoming requests. This resource itself does not
                   affect configuration unless it is attached to a
                   target https proxy or endpoint config selector
                   resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, server_tls_policy, server_tls_policy_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_server_tls_policy.CreateServerTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcn_server_tls_policy.CreateServerTlsPolicyRequest):
            request = gcn_server_tls_policy.CreateServerTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if server_tls_policy is not None:
                request.server_tls_policy = server_tls_policy
            if server_tls_policy_id is not None:
                request.server_tls_policy_id = server_tls_policy_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_server_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_server_tls_policy.ServerTlsPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_server_tls_policy(
        self,
        request: Union[gcn_server_tls_policy.UpdateServerTlsPolicyRequest, dict] = None,
        *,
        server_tls_policy: gcn_server_tls_policy.ServerTlsPolicy = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single ServerTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.UpdateServerTlsPolicyRequest, dict]):
                The request object. Request used by
                UpdateServerTlsPolicy method.
            server_tls_policy (google.cloud.network_security_v1beta1.types.ServerTlsPolicy):
                Required. Updated ServerTlsPolicy
                resource.

                This corresponds to the ``server_tls_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Field mask is used to specify the fields to be
                overwritten in the ServerTlsPolicy resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.ServerTlsPolicy` ServerTlsPolicy is a resource that specifies how a server should authenticate
                   incoming requests. This resource itself does not
                   affect configuration unless it is attached to a
                   target https proxy or endpoint config selector
                   resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([server_tls_policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_server_tls_policy.UpdateServerTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcn_server_tls_policy.UpdateServerTlsPolicyRequest):
            request = gcn_server_tls_policy.UpdateServerTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if server_tls_policy is not None:
                request.server_tls_policy = server_tls_policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_server_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("server_tls_policy.name", request.server_tls_policy.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_server_tls_policy.ServerTlsPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_server_tls_policy(
        self,
        request: Union[server_tls_policy.DeleteServerTlsPolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single ServerTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.DeleteServerTlsPolicyRequest, dict]):
                The request object. Request used by the
                DeleteServerTlsPolicy method.
            name (str):
                Required. A name of the ServerTlsPolicy to delete. Must
                be in the format
                ``projects/*/locations/{location}/serverTlsPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a server_tls_policy.DeleteServerTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, server_tls_policy.DeleteServerTlsPolicyRequest):
            request = server_tls_policy.DeleteServerTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_server_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_client_tls_policies(
        self,
        request: Union[client_tls_policy.ListClientTlsPoliciesRequest, dict] = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListClientTlsPoliciesPager:
        r"""Lists ClientTlsPolicies in a given project and
        location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.ListClientTlsPoliciesRequest, dict]):
                The request object. Request used by the
                ListClientTlsPolicies method.
            parent (str):
                Required. The project and location from which the
                ClientTlsPolicies should be listed, specified in the
                format ``projects/*/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.services.network_security.pagers.ListClientTlsPoliciesPager:
                Response returned by the
                ListClientTlsPolicies method.
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

        # Minor optimization to avoid making a copy if the user passes
        # in a client_tls_policy.ListClientTlsPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, client_tls_policy.ListClientTlsPoliciesRequest):
            request = client_tls_policy.ListClientTlsPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_client_tls_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListClientTlsPoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_client_tls_policy(
        self,
        request: Union[client_tls_policy.GetClientTlsPolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> client_tls_policy.ClientTlsPolicy:
        r"""Gets details of a single ClientTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.GetClientTlsPolicyRequest, dict]):
                The request object. Request used by the
                GetClientTlsPolicy method.
            name (str):
                Required. A name of the ClientTlsPolicy to get. Must be
                in the format
                ``projects/*/locations/{location}/clientTlsPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.network_security_v1beta1.types.ClientTlsPolicy:
                ClientTlsPolicy is a resource that
                specifies how a client should
                authenticate connections to backends of
                a service. This resource itself does not
                affect configuration unless it is
                attached to a backend service resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a client_tls_policy.GetClientTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, client_tls_policy.GetClientTlsPolicyRequest):
            request = client_tls_policy.GetClientTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_client_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_client_tls_policy(
        self,
        request: Union[gcn_client_tls_policy.CreateClientTlsPolicyRequest, dict] = None,
        *,
        parent: str = None,
        client_tls_policy: gcn_client_tls_policy.ClientTlsPolicy = None,
        client_tls_policy_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new ClientTlsPolicy in a given project and
        location.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.CreateClientTlsPolicyRequest, dict]):
                The request object. Request used by the
                CreateClientTlsPolicy method.
            parent (str):
                Required. The parent resource of the ClientTlsPolicy.
                Must be in the format
                ``projects/*/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            client_tls_policy (google.cloud.network_security_v1beta1.types.ClientTlsPolicy):
                Required. ClientTlsPolicy resource to
                be created.

                This corresponds to the ``client_tls_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            client_tls_policy_id (str):
                Required. Short name of the ClientTlsPolicy resource to
                be created. This value should be 1-63 characters long,
                containing only letters, numbers, hyphens, and
                underscores, and should not start with a number. E.g.
                "client_mtls_policy".

                This corresponds to the ``client_tls_policy_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.ClientTlsPolicy` ClientTlsPolicy is a resource that specifies how a client should authenticate
                   connections to backends of a service. This resource
                   itself does not affect configuration unless it is
                   attached to a backend service resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, client_tls_policy, client_tls_policy_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_client_tls_policy.CreateClientTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcn_client_tls_policy.CreateClientTlsPolicyRequest):
            request = gcn_client_tls_policy.CreateClientTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if client_tls_policy is not None:
                request.client_tls_policy = client_tls_policy
            if client_tls_policy_id is not None:
                request.client_tls_policy_id = client_tls_policy_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_client_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_client_tls_policy.ClientTlsPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_client_tls_policy(
        self,
        request: Union[gcn_client_tls_policy.UpdateClientTlsPolicyRequest, dict] = None,
        *,
        client_tls_policy: gcn_client_tls_policy.ClientTlsPolicy = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single ClientTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.UpdateClientTlsPolicyRequest, dict]):
                The request object. Request used by
                UpdateClientTlsPolicy method.
            client_tls_policy (google.cloud.network_security_v1beta1.types.ClientTlsPolicy):
                Required. Updated ClientTlsPolicy
                resource.

                This corresponds to the ``client_tls_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Field mask is used to specify the fields to be
                overwritten in the ClientTlsPolicy resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.network_security_v1beta1.types.ClientTlsPolicy` ClientTlsPolicy is a resource that specifies how a client should authenticate
                   connections to backends of a service. This resource
                   itself does not affect configuration unless it is
                   attached to a backend service resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([client_tls_policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcn_client_tls_policy.UpdateClientTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcn_client_tls_policy.UpdateClientTlsPolicyRequest):
            request = gcn_client_tls_policy.UpdateClientTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if client_tls_policy is not None:
                request.client_tls_policy = client_tls_policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_client_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("client_tls_policy.name", request.client_tls_policy.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcn_client_tls_policy.ClientTlsPolicy,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_client_tls_policy(
        self,
        request: Union[client_tls_policy.DeleteClientTlsPolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single ClientTlsPolicy.

        Args:
            request (Union[google.cloud.network_security_v1beta1.types.DeleteClientTlsPolicyRequest, dict]):
                The request object. Request used by the
                DeleteClientTlsPolicy method.
            name (str):
                Required. A name of the ClientTlsPolicy to delete. Must
                be in the format
                ``projects/*/locations/{location}/clientTlsPolicies/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a client_tls_policy.DeleteClientTlsPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, client_tls_policy.DeleteClientTlsPolicyRequest):
            request = client_tls_policy.DeleteClientTlsPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_client_tls_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=common.OperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-network-security",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("NetworkSecurityClient",)
