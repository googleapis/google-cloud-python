# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import os
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
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.managedidentities_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.managedidentities_v1.services.managed_identities_service import pagers
from google.cloud.managedidentities_v1.types import managed_identities_service, resource

from .transports.base import DEFAULT_CLIENT_INFO, ManagedIdentitiesServiceTransport
from .transports.grpc import ManagedIdentitiesServiceGrpcTransport
from .transports.grpc_asyncio import ManagedIdentitiesServiceGrpcAsyncIOTransport


class ManagedIdentitiesServiceClientMeta(type):
    """Metaclass for the ManagedIdentitiesService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ManagedIdentitiesServiceTransport]]
    _transport_registry["grpc"] = ManagedIdentitiesServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ManagedIdentitiesServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ManagedIdentitiesServiceTransport]:
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


class ManagedIdentitiesServiceClient(metaclass=ManagedIdentitiesServiceClientMeta):
    """API Overview

    The ``managedidentites.googleapis.com`` service implements the
    Google Cloud Managed Identites API for identity services (e.g.
    Microsoft Active Directory).

    The Managed Identities service provides methods to manage
    (create/read/update/delete) domains, reset managed identities admin
    password, add/remove domain controllers in GCP regions and
    add/remove VPC peering.

    Data Model

    The Managed Identities service exposes the following resources:

    -  Locations as global, named as follows:
       ``projects/{project_id}/locations/global``.

    -  Domains, named as follows:
       ``/projects/{project_id}/locations/global/domain/{domain_name}``.

    The ``{domain_name}`` refers to fully qualified domain name in the
    customer project e.g. mydomain.myorganization.com, with the
    following restrictions:

    -  Must contain only lowercase letters, numbers, periods and
       hyphens.
    -  Must start with a letter.
    -  Must contain between 2-64 characters.
    -  Must end with a number or a letter.
    -  Must not start with period.
    -  First segement length (mydomain form example above) shouldn't
       exceed 15 chars.
    -  The last segment cannot be fully numeric.
    -  Must be unique within the customer project.
    """

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

    DEFAULT_ENDPOINT = "managedidentities.googleapis.com"
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
            ManagedIdentitiesServiceClient: The constructed client.
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
            ManagedIdentitiesServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ManagedIdentitiesServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ManagedIdentitiesServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def domain_path(
        project: str,
        location: str,
        domain: str,
    ) -> str:
        """Returns a fully-qualified domain string."""
        return "projects/{project}/locations/{location}/domains/{domain}".format(
            project=project,
            location=location,
            domain=domain,
        )

    @staticmethod
    def parse_domain_path(path: str) -> Dict[str, str]:
        """Parses a domain path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/domains/(?P<domain>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
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
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
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
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, ManagedIdentitiesServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the managed identities service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ManagedIdentitiesServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ManagedIdentitiesServiceTransport):
            # transport is a ManagedIdentitiesServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
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
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

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
                api_audience=client_options.api_audience,
            )

    def create_microsoft_ad_domain(
        self,
        request: Optional[
            Union[managed_identities_service.CreateMicrosoftAdDomainRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        domain_name: Optional[str] = None,
        domain: Optional[resource.Domain] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a Microsoft AD domain.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_create_microsoft_ad_domain():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                domain = managedidentities_v1.Domain()
                domain.name = "name_value"
                domain.reserved_ip_range = "reserved_ip_range_value"
                domain.locations = ['locations_value1', 'locations_value2']

                request = managedidentities_v1.CreateMicrosoftAdDomainRequest(
                    parent="parent_value",
                    domain_name="domain_name_value",
                    domain=domain,
                )

                # Make the request
                operation = client.create_microsoft_ad_domain(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.CreateMicrosoftAdDomainRequest, dict]):
                The request object. Request message for
                [CreateMicrosoftAdDomain][google.cloud.managedidentities.v1.CreateMicrosoftAdDomain]
            parent (str):
                Required. The resource project name and location using
                the form: ``projects/{project_id}/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            domain_name (str):
                Required. The fully qualified domain name. e.g.
                mydomain.myorganization.com, with the following
                restrictions:

                -  Must contain only lowercase letters, numbers, periods
                   and hyphens.
                -  Must start with a letter.
                -  Must contain between 2-64 characters.
                -  Must end with a number or a letter.
                -  Must not start with period.
                -  First segement length (mydomain form example above)
                   shouldn't exceed 15 chars.
                -  The last segment cannot be fully numeric.
                -  Must be unique within the customer project.

                This corresponds to the ``domain_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            domain (google.cloud.managedidentities_v1.types.Domain):
                Required. A Managed Identity domain
                resource.

                This corresponds to the ``domain`` field
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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, domain_name, domain])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.CreateMicrosoftAdDomainRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, managed_identities_service.CreateMicrosoftAdDomainRequest
        ):
            request = managed_identities_service.CreateMicrosoftAdDomainRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if domain_name is not None:
                request.domain_name = domain_name
            if domain is not None:
                request.domain = domain

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_microsoft_ad_domain
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def reset_admin_password(
        self,
        request: Optional[
            Union[managed_identities_service.ResetAdminPasswordRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> managed_identities_service.ResetAdminPasswordResponse:
        r"""Resets a domain's administrator password.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_reset_admin_password():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                request = managedidentities_v1.ResetAdminPasswordRequest(
                    name="name_value",
                )

                # Make the request
                response = client.reset_admin_password(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.ResetAdminPasswordRequest, dict]):
                The request object. Request message for
                [ResetAdminPassword][google.cloud.managedidentities.v1.ResetAdminPassword]
            name (str):
                Required. The domain resource name using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.managedidentities_v1.types.ResetAdminPasswordResponse:
                Response message for
                   [ResetAdminPassword][google.cloud.managedidentities.v1.ResetAdminPassword]

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

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.ResetAdminPasswordRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, managed_identities_service.ResetAdminPasswordRequest
        ):
            request = managed_identities_service.ResetAdminPasswordRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset_admin_password]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_domains(
        self,
        request: Optional[
            Union[managed_identities_service.ListDomainsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDomainsPager:
        r"""Lists domains in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_list_domains():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                request = managedidentities_v1.ListDomainsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_domains(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.ListDomainsRequest, dict]):
                The request object. Request message for
                [ListDomains][google.cloud.managedidentities.v1.ListDomains]
            parent (str):
                Required. The resource name of the domain location using
                the form: ``projects/{project_id}/locations/global``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.managedidentities_v1.services.managed_identities_service.pagers.ListDomainsPager:
                Response message for
                   [ListDomains][google.cloud.managedidentities.v1.ListDomains]

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.ListDomainsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.ListDomainsRequest):
            request = managed_identities_service.ListDomainsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_domains]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDomainsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_domain(
        self,
        request: Optional[
            Union[managed_identities_service.GetDomainRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.Domain:
        r"""Gets information about a domain.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_get_domain():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                request = managedidentities_v1.GetDomainRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_domain(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.GetDomainRequest, dict]):
                The request object. Request message for
                [GetDomain][google.cloud.managedidentities.v1.GetDomain]
            name (str):
                Required. The domain resource name using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.managedidentities_v1.types.Domain:
                Represents a managed Microsoft Active
                Directory domain.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.GetDomainRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.GetDomainRequest):
            request = managed_identities_service.GetDomainRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_domain]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_domain(
        self,
        request: Optional[
            Union[managed_identities_service.UpdateDomainRequest, dict]
        ] = None,
        *,
        domain: Optional[resource.Domain] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the metadata and configuration of a domain.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_update_domain():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                domain = managedidentities_v1.Domain()
                domain.name = "name_value"
                domain.reserved_ip_range = "reserved_ip_range_value"
                domain.locations = ['locations_value1', 'locations_value2']

                request = managedidentities_v1.UpdateDomainRequest(
                    domain=domain,
                )

                # Make the request
                operation = client.update_domain(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.UpdateDomainRequest, dict]):
                The request object. Request message for
                [UpdateDomain][google.cloud.managedidentities.v1.UpdateDomain]
            domain (google.cloud.managedidentities_v1.types.Domain):
                Required. Domain message with updated fields. Only
                supported fields specified in update_mask are updated.

                This corresponds to the ``domain`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field may only include fields from
                [Domain][google.cloud.managedidentities.v1.Domain]:

                -  ``labels``
                -  ``locations``
                -  ``authorized_networks``

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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([domain, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.UpdateDomainRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.UpdateDomainRequest):
            request = managed_identities_service.UpdateDomainRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if domain is not None:
                request.domain = domain
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_domain]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("domain.name", request.domain.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def delete_domain(
        self,
        request: Optional[
            Union[managed_identities_service.DeleteDomainRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a domain.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_delete_domain():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                request = managedidentities_v1.DeleteDomainRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_domain(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.DeleteDomainRequest, dict]):
                The request object. Request message for
                [DeleteDomain][google.cloud.managedidentities.v1.DeleteDomain]
            name (str):
                Required. The domain resource name using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

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

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.DeleteDomainRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.DeleteDomainRequest):
            request = managed_identities_service.DeleteDomainRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_domain]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def attach_trust(
        self,
        request: Optional[
            Union[managed_identities_service.AttachTrustRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        trust: Optional[resource.Trust] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Adds an AD trust to a domain.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_attach_trust():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                trust = managedidentities_v1.Trust()
                trust.target_domain_name = "target_domain_name_value"
                trust.trust_type = "EXTERNAL"
                trust.trust_direction = "BIDIRECTIONAL"
                trust.target_dns_ip_addresses = ['target_dns_ip_addresses_value1', 'target_dns_ip_addresses_value2']
                trust.trust_handshake_secret = "trust_handshake_secret_value"

                request = managedidentities_v1.AttachTrustRequest(
                    name="name_value",
                    trust=trust,
                )

                # Make the request
                operation = client.attach_trust(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.AttachTrustRequest, dict]):
                The request object. Request message for
                [AttachTrust][google.cloud.managedidentities.v1.AttachTrust]
            name (str):
                Required. The resource domain name, project name and
                location using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trust (google.cloud.managedidentities_v1.types.Trust):
                Required. The domain trust resource.
                This corresponds to the ``trust`` field
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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, trust])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.AttachTrustRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.AttachTrustRequest):
            request = managed_identities_service.AttachTrustRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if trust is not None:
                request.trust = trust

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.attach_trust]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def reconfigure_trust(
        self,
        request: Optional[
            Union[managed_identities_service.ReconfigureTrustRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        target_domain_name: Optional[str] = None,
        target_dns_ip_addresses: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the DNS conditional forwarder.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_reconfigure_trust():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                request = managedidentities_v1.ReconfigureTrustRequest(
                    name="name_value",
                    target_domain_name="target_domain_name_value",
                    target_dns_ip_addresses=['target_dns_ip_addresses_value1', 'target_dns_ip_addresses_value2'],
                )

                # Make the request
                operation = client.reconfigure_trust(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.ReconfigureTrustRequest, dict]):
                The request object. Request message for
                [ReconfigureTrust][google.cloud.managedidentities.v1.ReconfigureTrust]
            name (str):
                Required. The resource domain name, project name and
                location using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_domain_name (str):
                Required. The fully-qualified target
                domain name which will be in trust with
                current domain.

                This corresponds to the ``target_domain_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_dns_ip_addresses (MutableSequence[str]):
                Required. The target DNS server IP
                addresses to resolve the remote domain
                involved in the trust.

                This corresponds to the ``target_dns_ip_addresses`` field
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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, target_domain_name, target_dns_ip_addresses])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.ReconfigureTrustRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.ReconfigureTrustRequest):
            request = managed_identities_service.ReconfigureTrustRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if target_domain_name is not None:
                request.target_domain_name = target_domain_name
            if target_dns_ip_addresses is not None:
                request.target_dns_ip_addresses = target_dns_ip_addresses

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reconfigure_trust]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def detach_trust(
        self,
        request: Optional[
            Union[managed_identities_service.DetachTrustRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        trust: Optional[resource.Trust] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Removes an AD trust.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_detach_trust():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                trust = managedidentities_v1.Trust()
                trust.target_domain_name = "target_domain_name_value"
                trust.trust_type = "EXTERNAL"
                trust.trust_direction = "BIDIRECTIONAL"
                trust.target_dns_ip_addresses = ['target_dns_ip_addresses_value1', 'target_dns_ip_addresses_value2']
                trust.trust_handshake_secret = "trust_handshake_secret_value"

                request = managedidentities_v1.DetachTrustRequest(
                    name="name_value",
                    trust=trust,
                )

                # Make the request
                operation = client.detach_trust(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.DetachTrustRequest, dict]):
                The request object. Request message for
                [DetachTrust][google.cloud.managedidentities.v1.DetachTrust]
            name (str):
                Required. The resource domain name, project name, and
                location using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trust (google.cloud.managedidentities_v1.types.Trust):
                Required. The domain trust resource
                to removed.

                This corresponds to the ``trust`` field
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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, trust])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.DetachTrustRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.DetachTrustRequest):
            request = managed_identities_service.DetachTrustRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if trust is not None:
                request.trust = trust

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.detach_trust]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def validate_trust(
        self,
        request: Optional[
            Union[managed_identities_service.ValidateTrustRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        trust: Optional[resource.Trust] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Validates a trust state, that the target domain is
        reachable, and that the target domain is able to accept
        incoming trust requests.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import managedidentities_v1

            def sample_validate_trust():
                # Create a client
                client = managedidentities_v1.ManagedIdentitiesServiceClient()

                # Initialize request argument(s)
                trust = managedidentities_v1.Trust()
                trust.target_domain_name = "target_domain_name_value"
                trust.trust_type = "EXTERNAL"
                trust.trust_direction = "BIDIRECTIONAL"
                trust.target_dns_ip_addresses = ['target_dns_ip_addresses_value1', 'target_dns_ip_addresses_value2']
                trust.trust_handshake_secret = "trust_handshake_secret_value"

                request = managedidentities_v1.ValidateTrustRequest(
                    name="name_value",
                    trust=trust,
                )

                # Make the request
                operation = client.validate_trust(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.managedidentities_v1.types.ValidateTrustRequest, dict]):
                The request object. Request message for
                [ValidateTrust][google.cloud.managedidentities.v1.ValidateTrust]
            name (str):
                Required. The resource domain name, project name, and
                location using the form:
                ``projects/{project_id}/locations/global/domains/{domain_name}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trust (google.cloud.managedidentities_v1.types.Trust):
                Required. The domain trust to
                validate trust state for.

                This corresponds to the ``trust`` field
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

                The result type for the operation will be
                :class:`google.cloud.managedidentities_v1.types.Domain`
                Represents a managed Microsoft Active Directory domain.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, trust])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a managed_identities_service.ValidateTrustRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, managed_identities_service.ValidateTrustRequest):
            request = managed_identities_service.ValidateTrustRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if trust is not None:
                request.trust = trust

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.validate_trust]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resource.Domain,
            metadata_type=managed_identities_service.OpMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ManagedIdentitiesServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ManagedIdentitiesServiceClient",)
