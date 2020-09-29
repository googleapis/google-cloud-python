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
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.security.privateca_v1beta1.services.certificate_authority_service import (
    pagers,
)
from google.cloud.security.privateca_v1beta1.types import resources
from google.cloud.security.privateca_v1beta1.types import service
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import CertificateAuthorityServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import CertificateAuthorityServiceGrpcTransport
from .transports.grpc_asyncio import CertificateAuthorityServiceGrpcAsyncIOTransport


class CertificateAuthorityServiceClientMeta(type):
    """Metaclass for the CertificateAuthorityService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[CertificateAuthorityServiceTransport]]
    _transport_registry["grpc"] = CertificateAuthorityServiceGrpcTransport
    _transport_registry[
        "grpc_asyncio"
    ] = CertificateAuthorityServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[CertificateAuthorityServiceTransport]:
        """Return an appropriate transport class.

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


class CertificateAuthorityServiceClient(
    metaclass=CertificateAuthorityServiceClientMeta
):
    """[Certificate Authority
    Service][google.cloud.security.privateca.v1beta1.CertificateAuthorityService]
    manages private certificate authorities and issued certificates.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
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

    DEFAULT_ENDPOINT = "privateca.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def certificate_path(
        project: str, location: str, certificate_authority: str, certificate: str,
    ) -> str:
        """Return a fully-qualified certificate string."""
        return "projects/{project}/locations/{location}/certificateAuthorities/{certificate_authority}/certificates/{certificate}".format(
            project=project,
            location=location,
            certificate_authority=certificate_authority,
            certificate=certificate,
        )

    @staticmethod
    def parse_certificate_path(path: str) -> Dict[str, str]:
        """Parse a certificate path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateAuthorities/(?P<certificate_authority>.+?)/certificates/(?P<certificate>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_authority_path(
        project: str, location: str, certificate_authority: str,
    ) -> str:
        """Return a fully-qualified certificate_authority string."""
        return "projects/{project}/locations/{location}/certificateAuthorities/{certificate_authority}".format(
            project=project,
            location=location,
            certificate_authority=certificate_authority,
        )

    @staticmethod
    def parse_certificate_authority_path(path: str) -> Dict[str, str]:
        """Parse a certificate_authority path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateAuthorities/(?P<certificate_authority>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_revocation_list_path(
        project: str,
        location: str,
        certificate_authority: str,
        certificate_revocation_list: str,
    ) -> str:
        """Return a fully-qualified certificate_revocation_list string."""
        return "projects/{project}/locations/{location}/certificateAuthorities/{certificate_authority}/certificateRevocationLists/{certificate_revocation_list}".format(
            project=project,
            location=location,
            certificate_authority=certificate_authority,
            certificate_revocation_list=certificate_revocation_list,
        )

    @staticmethod
    def parse_certificate_revocation_list_path(path: str) -> Dict[str, str]:
        """Parse a certificate_revocation_list path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateAuthorities/(?P<certificate_authority>.+?)/certificateRevocationLists/(?P<certificate_revocation_list>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def reusable_config_path(project: str, location: str, reusable_config: str,) -> str:
        """Return a fully-qualified reusable_config string."""
        return "projects/{project}/locations/{location}/reusableConfigs/{reusable_config}".format(
            project=project, location=location, reusable_config=reusable_config,
        )

    @staticmethod
    def parse_reusable_config_path(path: str) -> Dict[str, str]:
        """Parse a reusable_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/reusableConfigs/(?P<reusable_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, CertificateAuthorityServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the certificate authority service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CertificateAuthorityServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (client_options_lib.ClientOptions): Custom options for the
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

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

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
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, CertificateAuthorityServiceTransport):
            # transport is a CertificateAuthorityServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_certificate(
        self,
        request: service.CreateCertificateRequest = None,
        *,
        parent: str = None,
        certificate: resources.Certificate = None,
        certificate_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Certificate:
        r"""Create a new
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
        in a given Project, Location from a particular
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.CreateCertificateRequest`):
                The request object. Request message for
                [CertificateAuthorityService.CreateCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateCertificate].
            parent (:class:`str`):
                Required. The resource name of the location and
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                associated with the
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate],
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate (:class:`~.resources.Certificate`):
                Required. A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                with initial field values.
                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_id (:class:`str`):
                Optional. It must be unique within a location and match
                the regular expression ``[a-zA-Z0-9-]{1,63}``. This
                field is required when using a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the Enterprise
                [CertificateAuthority.Tier][google.cloud.security.privateca.v1beta1.CertificateAuthority.Tier],
                but is optional and its value is ignored otherwise.
                This corresponds to the ``certificate_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Certificate:
                A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, certificate, certificate_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateCertificateRequest):
            request = service.CreateCertificateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if certificate is not None:
                request.certificate = certificate
            if certificate_id is not None:
                request.certificate_id = certificate_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_certificate(
        self,
        request: service.GetCertificateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Certificate:
        r"""Returns a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Args:
            request (:class:`~.service.GetCertificateRequest`):
                The request object. Request message for
                [CertificateAuthorityService.GetCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificate].
            name (:class:`str`):
                Required. The
                [name][google.cloud.security.privateca.v1beta1.Certificate.name]
                of the
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                to get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Certificate:
                A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

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
        # in a service.GetCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetCertificateRequest):
            request = service.GetCertificateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_certificates(
        self,
        request: service.ListCertificatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificatesPager:
        r"""Lists
        [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

        Args:
            request (:class:`~.service.ListCertificatesRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificates].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate],
                in the format
                ``projects/*/locations/*/certificateauthorities/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListCertificatesPager:
                Response message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificates].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListCertificatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListCertificatesRequest):
            request = service.ListCertificatesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_certificates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCertificatesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def revoke_certificate(
        self,
        request: service.RevokeCertificateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Certificate:
        r"""Revoke a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Args:
            request (:class:`~.service.RevokeCertificateRequest`):
                The request object. Request message for
                [CertificateAuthorityService.RevokeCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.RevokeCertificate].
            name (:class:`str`):
                Required. The resource name for this
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*/certificates/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Certificate:
                A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

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
        # in a service.RevokeCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.RevokeCertificateRequest):
            request = service.RevokeCertificateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.revoke_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_certificate(
        self,
        request: service.UpdateCertificateRequest = None,
        *,
        certificate: resources.Certificate = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Certificate:
        r"""Update a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Args:
            request (:class:`~.service.UpdateCertificateRequest`):
                The request object. Request message for
                [CertificateAuthorityService.UpdateCertificate][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificate].
            certificate (:class:`~.resources.Certificate`):
                Required.
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                with updated values.
                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. A list of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Certificate:
                A
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpdateCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpdateCertificateRequest):
            request = service.UpdateCertificateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if certificate is not None:
                request.certificate = certificate
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate.name", request.certificate.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def activate_certificate_authority(
        self,
        request: service.ActivateCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Activate a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        After the parent Certificate Authority signs a certificate
        signing request from
        [FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr],
        this method can complete the activation process.

        Args:
            request (:class:`~.service.ActivateCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ActivateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ActivateCertificateAuthority].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.ActivateCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ActivateCertificateAuthorityRequest):
            request = service.ActivateCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.activate_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_certificate_authority(
        self,
        request: service.CreateCertificateAuthorityRequest = None,
        *,
        parent: str = None,
        certificate_authority: resources.CertificateAuthority = None,
        certificate_authority_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a new
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        in a given Project and Location.

        Args:
            request (:class:`~.service.CreateCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.CreateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateCertificateAuthority].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [CertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthority],
                in the format ``projects/*/locations/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_authority (:class:`~.resources.CertificateAuthority`):
                Required. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                with initial field values.
                This corresponds to the ``certificate_authority`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_authority_id (:class:`str`):
                Required. It must be unique within a location and match
                the regular expression ``[a-zA-Z0-9-]{1,63}``
                This corresponds to the ``certificate_authority_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, certificate_authority, certificate_authority_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateCertificateAuthorityRequest):
            request = service.CreateCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if certificate_authority is not None:
                request.certificate_authority = certificate_authority
            if certificate_authority_id is not None:
                request.certificate_authority_id = certificate_authority_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def disable_certificate_authority(
        self,
        request: service.DisableCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Disable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.DisableCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.DisableCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.DisableCertificateAuthority].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.DisableCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.DisableCertificateAuthorityRequest):
            request = service.DisableCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.disable_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def enable_certificate_authority(
        self,
        request: service.EnableCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Enable a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.EnableCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.EnableCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.EnableCertificateAuthority].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.EnableCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.EnableCertificateAuthorityRequest):
            request = service.EnableCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.enable_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def fetch_certificate_authority_csr(
        self,
        request: service.FetchCertificateAuthorityCsrRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.FetchCertificateAuthorityCsrResponse:
        r"""Fetch a certificate signing request (CSR) from a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is in state
        [PENDING_ACTIVATION][google.cloud.security.privateca.v1beta1.CertificateAuthority.State.PENDING_ACTIVATION]
        and is of type
        [SUBORDINATE][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type.SUBORDINATE].
        The CSR must then be signed by the desired parent Certificate
        Authority, which could be another
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        resource, or could be an on-prem certificate authority. See also
        [ActivateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ActivateCertificateAuthority].

        Args:
            request (:class:`~.service.FetchCertificateAuthorityCsrRequest`):
                The request object. Request message for
                [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.service.FetchCertificateAuthorityCsrResponse:
                Response message for
                [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.FetchCertificateAuthorityCsr].

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
        # in a service.FetchCertificateAuthorityCsrRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.FetchCertificateAuthorityCsrRequest):
            request = service.FetchCertificateAuthorityCsrRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.fetch_certificate_authority_csr
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_certificate_authority(
        self,
        request: service.GetCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CertificateAuthority:
        r"""Returns a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.GetCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.GetCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificateAuthority].
            name (:class:`str`):
                Required. The
                [name][google.cloud.security.privateca.v1beta1.CertificateAuthority.name]
                of the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                to get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.CertificateAuthority:
                A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.GetCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetCertificateAuthorityRequest):
            request = service.GetCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_certificate_authority
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_certificate_authorities(
        self,
        request: service.ListCertificateAuthoritiesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateAuthoritiesPager:
        r"""Lists
        [CertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.ListCertificateAuthoritiesRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateAuthorities].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [CertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthority],
                in the format ``projects/*/locations/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListCertificateAuthoritiesPager:
                Response message for
                [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateAuthorities].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListCertificateAuthoritiesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListCertificateAuthoritiesRequest):
            request = service.ListCertificateAuthoritiesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_certificate_authorities
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
        response = pagers.ListCertificateAuthoritiesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def restore_certificate_authority(
        self,
        request: service.RestoreCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Restore a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        that is scheduled for deletion.

        Args:
            request (:class:`~.service.RestoreCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.RestoreCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.RestoreCertificateAuthority].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.RestoreCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.RestoreCertificateAuthorityRequest):
            request = service.RestoreCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.restore_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def schedule_delete_certificate_authority(
        self,
        request: service.ScheduleDeleteCertificateAuthorityRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Schedule a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        for deletion.

        Args:
            request (:class:`~.service.ScheduleDeleteCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ScheduleDeleteCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ScheduleDeleteCertificateAuthority].
            name (:class:`str`):
                Required. The resource name for this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

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
        # in a service.ScheduleDeleteCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ScheduleDeleteCertificateAuthorityRequest):
            request = service.ScheduleDeleteCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.schedule_delete_certificate_authority
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
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_certificate_authority(
        self,
        request: service.UpdateCertificateAuthorityRequest = None,
        *,
        certificate_authority: resources.CertificateAuthority = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.UpdateCertificateAuthorityRequest`):
                The request object. Request message for
                [CertificateAuthorityService.UpdateCertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificateAuthority].
            certificate_authority (:class:`~.resources.CertificateAuthority`):
                Required.
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                with updated values.
                This corresponds to the ``certificate_authority`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. A list of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateAuthority``: A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_authority, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpdateCertificateAuthorityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpdateCertificateAuthorityRequest):
            request = service.UpdateCertificateAuthorityRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if certificate_authority is not None:
                request.certificate_authority = certificate_authority
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_certificate_authority
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate_authority.name", request.certificate_authority.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.CertificateAuthority,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_certificate_revocation_list(
        self,
        request: service.CreateCertificateRevocationListRequest = None,
        *,
        parent: str = None,
        certificate_revocation_list: resources.CertificateRevocationList = None,
        certificate_revocation_list_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a new
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
        in a given Project, Location for a particular
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Args:
            request (:class:`~.service.CreateCertificateRevocationListRequest`):
                The request object. Request message for
                [CertificateAuthorityService.CreateCertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateCertificateRevocationList].
            parent (:class:`str`):
                Required. The resource name of the location and
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                associated with the
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList],
                in the format
                ``projects/*/locations/*/certificateAuthorities/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_revocation_list (:class:`~.resources.CertificateRevocationList`):
                Required. A
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                with initial field values.
                This corresponds to the ``certificate_revocation_list`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_revocation_list_id (:class:`str`):
                Required. It must be unique within a location and match
                the regular expression ``[a-zA-Z0-9-]{1,63}``
                This corresponds to the ``certificate_revocation_list_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateRevocationList``: A
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                corresponds to a signed X.509 certificate Revocation
                List (CRL). A CRL contains the serial numbers of
                certificates that should no longer be trusted.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, certificate_revocation_list, certificate_revocation_list_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateCertificateRevocationListRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateCertificateRevocationListRequest):
            request = service.CreateCertificateRevocationListRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if certificate_revocation_list is not None:
                request.certificate_revocation_list = certificate_revocation_list
            if certificate_revocation_list_id is not None:
                request.certificate_revocation_list_id = certificate_revocation_list_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_certificate_revocation_list
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
            resources.CertificateRevocationList,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_certificate_revocation_list(
        self,
        request: service.GetCertificateRevocationListRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CertificateRevocationList:
        r"""Returns a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Args:
            request (:class:`~.service.GetCertificateRevocationListRequest`):
                The request object. Request message for
                [CertificateAuthorityService.GetCertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetCertificateRevocationList].
            name (:class:`str`):
                Required. The
                [name][google.cloud.security.privateca.v1beta1.CertificateRevocationList.name]
                of the
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                to get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.CertificateRevocationList:
                A
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                corresponds to a signed X.509 certificate Revocation
                List (CRL). A CRL contains the serial numbers of
                certificates that should no longer be trusted.

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
        # in a service.GetCertificateRevocationListRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetCertificateRevocationListRequest):
            request = service.GetCertificateRevocationListRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_certificate_revocation_list
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_certificate_revocation_lists(
        self,
        request: service.ListCertificateRevocationListsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateRevocationListsPager:
        r"""Lists
        [CertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Args:
            request (:class:`~.service.ListCertificateRevocationListsRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateRevocationLists].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [CertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateRevocationList],
                in the format
                ``projects/*/locations/*/certificateauthorities/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListCertificateRevocationListsPager:
                Response message for
                [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListCertificateRevocationLists].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListCertificateRevocationListsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListCertificateRevocationListsRequest):
            request = service.ListCertificateRevocationListsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_certificate_revocation_lists
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
        response = pagers.ListCertificateRevocationListsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_certificate_revocation_list(
        self,
        request: service.UpdateCertificateRevocationListRequest = None,
        *,
        certificate_revocation_list: resources.CertificateRevocationList = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].

        Args:
            request (:class:`~.service.UpdateCertificateRevocationListRequest`):
                The request object. Request message for
                [CertificateAuthorityService.UpdateCertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateCertificateRevocationList].
            certificate_revocation_list (:class:`~.resources.CertificateRevocationList`):
                Required.
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                with updated values.
                This corresponds to the ``certificate_revocation_list`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. A list of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.CertificateRevocationList``: A
                [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
                corresponds to a signed X.509 certificate Revocation
                List (CRL). A CRL contains the serial numbers of
                certificates that should no longer be trusted.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_revocation_list, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpdateCertificateRevocationListRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpdateCertificateRevocationListRequest):
            request = service.UpdateCertificateRevocationListRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if certificate_revocation_list is not None:
                request.certificate_revocation_list = certificate_revocation_list
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_certificate_revocation_list
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "certificate_revocation_list.name",
                        request.certificate_revocation_list.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.CertificateRevocationList,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_reusable_config(
        self,
        request: service.CreateReusableConfigRequest = None,
        *,
        parent: str = None,
        reusable_config: resources.ReusableConfig = None,
        reusable_config_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a new
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
        in a given Project and Location.

        Args:
            request (:class:`~.service.CreateReusableConfigRequest`):
                The request object. Request message for
                [CertificateAuthorityService.CreateReusableConfig][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.CreateReusableConfig].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig],
                in the format ``projects/*/locations/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reusable_config (:class:`~.resources.ReusableConfig`):
                Required. A
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                with initial field values.
                This corresponds to the ``reusable_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reusable_config_id (:class:`str`):
                Required. It must be unique within a location and match
                the regular expression ``[a-zA-Z0-9-]{1,63}``
                This corresponds to the ``reusable_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.ReusableConfig``: A
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                refers to a managed
                [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
                Those, in turn, are used to describe certain fields of
                an X.509 certificate, such as the key usage fields,
                fields specific to CA certificates, certificate policy
                extensions and custom extensions.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, reusable_config, reusable_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateReusableConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateReusableConfigRequest):
            request = service.CreateReusableConfigRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if reusable_config is not None:
                request.reusable_config = reusable_config
            if reusable_config_id is not None:
                request.reusable_config_id = reusable_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_reusable_config]

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
            resources.ReusableConfig,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_reusable_config(
        self,
        request: service.DeleteReusableConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""DeleteReusableConfig deletes a
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Args:
            request (:class:`~.service.DeleteReusableConfigRequest`):
                The request object. Request message for
                [CertificateAuthorityService.DeleteReusableConfig][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.DeleteReusableConfig].
            name (:class:`str`):
                Required. The resource name for this
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                in the format
                ``projects/*/locations/*/reusableConfigs/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

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
        # in a service.DeleteReusableConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.DeleteReusableConfigRequest):
            request = service.DeleteReusableConfigRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_reusable_config]

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
            empty.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_reusable_config(
        self,
        request: service.GetReusableConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ReusableConfig:
        r"""Returns a
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Args:
            request (:class:`~.service.GetReusableConfigRequest`):
                The request object. Request message for
                [CertificateAuthorityService.GetReusableConfig][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.GetReusableConfig].
            name (:class:`str`):
                Required. The [name][ReusableConfigs.name] of the
                [ReusableConfigs][] to get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.ReusableConfig:
                A
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                refers to a managed
                [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
                Those, in turn, are used to describe certain fields of
                an X.509 certificate, such as the key usage fields,
                fields specific to CA certificates, certificate policy
                extensions and custom extensions.

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
        # in a service.GetReusableConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetReusableConfigRequest):
            request = service.GetReusableConfigRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_reusable_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_reusable_configs(
        self,
        request: service.ListReusableConfigsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReusableConfigsPager:
        r"""Lists
        [ReusableConfigs][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Args:
            request (:class:`~.service.ListReusableConfigsRequest`):
                The request object. Request message for
                [CertificateAuthorityService.ListReusableConfigs][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListReusableConfigs].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [ReusableConfigs][google.cloud.security.privateca.v1beta1.ReusableConfig],
                in the format ``projects/*/locations/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListReusableConfigsPager:
                Response message for
                [CertificateAuthorityService.ListReusableConfigs][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.ListReusableConfigs].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListReusableConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListReusableConfigsRequest):
            request = service.ListReusableConfigsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_reusable_configs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListReusableConfigsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_reusable_config(
        self,
        request: service.UpdateReusableConfigRequest = None,
        *,
        reusable_config: resources.ReusableConfig = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update a
        [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig].

        Args:
            request (:class:`~.service.UpdateReusableConfigRequest`):
                The request object. Request message for
                [CertificateAuthorityService.UpdateReusableConfig][google.cloud.security.privateca.v1beta1.CertificateAuthorityService.UpdateReusableConfig].
            reusable_config (:class:`~.resources.ReusableConfig`):
                Required.
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                with updated values.
                This corresponds to the ``reusable_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. A list of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.resources.ReusableConfig``: A
                [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
                refers to a managed
                [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
                Those, in turn, are used to describe certain fields of
                an X.509 certificate, such as the key usage fields,
                fields specific to CA certificates, certificate policy
                extensions and custom extensions.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([reusable_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpdateReusableConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpdateReusableConfigRequest):
            request = service.UpdateReusableConfigRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if reusable_config is not None:
                request.reusable_config = reusable_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_reusable_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("reusable_config.name", request.reusable_config.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.ReusableConfig,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-security-private-ca",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CertificateAuthorityServiceClient",)
