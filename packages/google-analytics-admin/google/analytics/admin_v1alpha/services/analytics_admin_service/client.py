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

from google.analytics.admin_v1alpha.services.analytics_admin_service import pagers
from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import resources
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore

from .transports.base import AnalyticsAdminServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import AnalyticsAdminServiceGrpcTransport
from .transports.grpc_asyncio import AnalyticsAdminServiceGrpcAsyncIOTransport


class AnalyticsAdminServiceClientMeta(type):
    """Metaclass for the AnalyticsAdminService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[AnalyticsAdminServiceTransport]]
    _transport_registry["grpc"] = AnalyticsAdminServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = AnalyticsAdminServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[AnalyticsAdminServiceTransport]:
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


class AnalyticsAdminServiceClient(metaclass=AnalyticsAdminServiceClientMeta):
    """Service Interface for the Analytics Admin API (GA4)."""

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

    DEFAULT_ENDPOINT = "analyticsadmin.googleapis.com"
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

    @property
    def transport(self) -> AnalyticsAdminServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            AnalyticsAdminServiceTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def account_path(account: str,) -> str:
        """Return a fully-qualified account string."""
        return "accounts/{account}".format(account=account,)

    @staticmethod
    def parse_account_path(path: str) -> Dict[str, str]:
        """Parse a account path into its component segments."""
        m = re.match(r"^accounts/(?P<account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def account_summary_path(account_summary: str,) -> str:
        """Return a fully-qualified account_summary string."""
        return "accountSummaries/{account_summary}".format(
            account_summary=account_summary,
        )

    @staticmethod
    def parse_account_summary_path(path: str) -> Dict[str, str]:
        """Parse a account_summary path into its component segments."""
        m = re.match(r"^accountSummaries/(?P<account_summary>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def android_app_data_stream_path(
        property: str, android_app_data_stream: str,
    ) -> str:
        """Return a fully-qualified android_app_data_stream string."""
        return "properties/{property}/androidAppDataStreams/{android_app_data_stream}".format(
            property=property, android_app_data_stream=android_app_data_stream,
        )

    @staticmethod
    def parse_android_app_data_stream_path(path: str) -> Dict[str, str]:
        """Parse a android_app_data_stream path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/androidAppDataStreams/(?P<android_app_data_stream>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_sharing_settings_path(account: str,) -> str:
        """Return a fully-qualified data_sharing_settings string."""
        return "accounts/{account}/dataSharingSettings".format(account=account,)

    @staticmethod
    def parse_data_sharing_settings_path(path: str) -> Dict[str, str]:
        """Parse a data_sharing_settings path into its component segments."""
        m = re.match(r"^accounts/(?P<account>.+?)/dataSharingSettings$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def enhanced_measurement_settings_path(property: str, web_data_stream: str,) -> str:
        """Return a fully-qualified enhanced_measurement_settings string."""
        return "properties/{property}/webDataStreams/{web_data_stream}/enhancedMeasurementSettings".format(
            property=property, web_data_stream=web_data_stream,
        )

    @staticmethod
    def parse_enhanced_measurement_settings_path(path: str) -> Dict[str, str]:
        """Parse a enhanced_measurement_settings path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/webDataStreams/(?P<web_data_stream>.+?)/enhancedMeasurementSettings$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def firebase_link_path(property: str, firebase_link: str,) -> str:
        """Return a fully-qualified firebase_link string."""
        return "properties/{property}/firebaseLinks/{firebase_link}".format(
            property=property, firebase_link=firebase_link,
        )

    @staticmethod
    def parse_firebase_link_path(path: str) -> Dict[str, str]:
        """Parse a firebase_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/firebaseLinks/(?P<firebase_link>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def global_site_tag_path(property: str,) -> str:
        """Return a fully-qualified global_site_tag string."""
        return "properties/{property}/globalSiteTag".format(property=property,)

    @staticmethod
    def parse_global_site_tag_path(path: str) -> Dict[str, str]:
        """Parse a global_site_tag path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)/globalSiteTag$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def google_ads_link_path(property: str, google_ads_link: str,) -> str:
        """Return a fully-qualified google_ads_link string."""
        return "properties/{property}/googleAdsLinks/{google_ads_link}".format(
            property=property, google_ads_link=google_ads_link,
        )

    @staticmethod
    def parse_google_ads_link_path(path: str) -> Dict[str, str]:
        """Parse a google_ads_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/googleAdsLinks/(?P<google_ads_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ios_app_data_stream_path(property: str, ios_app_data_stream: str,) -> str:
        """Return a fully-qualified ios_app_data_stream string."""
        return "properties/{property}/iosAppDataStreams/{ios_app_data_stream}".format(
            property=property, ios_app_data_stream=ios_app_data_stream,
        )

    @staticmethod
    def parse_ios_app_data_stream_path(path: str) -> Dict[str, str]:
        """Parse a ios_app_data_stream path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/iosAppDataStreams/(?P<ios_app_data_stream>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def property_path(property: str,) -> str:
        """Return a fully-qualified property string."""
        return "properties/{property}".format(property=property,)

    @staticmethod
    def parse_property_path(path: str) -> Dict[str, str]:
        """Parse a property path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def user_link_path(account: str, user_link: str,) -> str:
        """Return a fully-qualified user_link string."""
        return "accounts/{account}/userLinks/{user_link}".format(
            account=account, user_link=user_link,
        )

    @staticmethod
    def parse_user_link_path(path: str) -> Dict[str, str]:
        """Parse a user_link path into its component segments."""
        m = re.match(r"^accounts/(?P<account>.+?)/userLinks/(?P<user_link>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def web_data_stream_path(property: str, web_data_stream: str,) -> str:
        """Return a fully-qualified web_data_stream string."""
        return "properties/{property}/webDataStreams/{web_data_stream}".format(
            property=property, web_data_stream=web_data_stream,
        )

    @staticmethod
    def parse_web_data_stream_path(path: str) -> Dict[str, str]:
        """Parse a web_data_stream path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/webDataStreams/(?P<web_data_stream>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
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
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
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
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, AnalyticsAdminServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the analytics admin service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AnalyticsAdminServiceTransport]): The
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
        if isinstance(transport, AnalyticsAdminServiceTransport):
            # transport is a AnalyticsAdminServiceTransport instance.
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

    def get_account(
        self,
        request: analytics_admin.GetAccountRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Lookup for a single Account.
        Throws "Target not found" if no such account found, or
        if caller does not have permissions to access it.

        Args:
            request (:class:`~.analytics_admin.GetAccountRequest`):
                The request object. Request message for GetAccount RPC.
            name (:class:`str`):
                Required. The name of the account to
                lookup. Format: accounts/{account}
                Example: "accounts/100".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Account:
                A resource message representing a
                Google Analytics account.

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
        # in a analytics_admin.GetAccountRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetAccountRequest):
            request = analytics_admin.GetAccountRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_accounts(
        self,
        request: analytics_admin.ListAccountsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountsPager:
        r"""Returns all accounts accessible by the caller.
        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        Args:
            request (:class:`~.analytics_admin.ListAccountsRequest`):
                The request object. Request message for ListAccounts
                RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListAccountsPager:
                Request message for ListAccounts RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.ListAccountsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListAccountsRequest):
            request = analytics_admin.ListAccountsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_accounts]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAccountsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_account(
        self,
        request: analytics_admin.DeleteAccountRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Marks target Account as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        accounts. However, they can be restored using the Trash
        Can UI.
        If the accounts are not restored before the expiration
        time, the account and all child resources (eg:
        Properties, GoogleAdsLinks, Streams, UserLinks) will be
        permanently purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found.

        Args:
            request (:class:`~.analytics_admin.DeleteAccountRequest`):
                The request object. Request message for DeleteAccount
                RPC.
            name (:class:`str`):
                Required. The name of the Account to
                soft-delete. Format: accounts/{account}
                Example: "accounts/100".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteAccountRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteAccountRequest):
            request = analytics_admin.DeleteAccountRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_account(
        self,
        request: analytics_admin.UpdateAccountRequest = None,
        *,
        account: resources.Account = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Updates an account.

        Args:
            request (:class:`~.analytics_admin.UpdateAccountRequest`):
                The request object. Request message for UpdateAccount
                RPC.
            account (:class:`~.resources.Account`):
                Required. The account to update. The account's ``name``
                field is used to identify the account.
                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Account:
                A resource message representing a
                Google Analytics account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([account, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateAccountRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateAccountRequest):
            request = analytics_admin.UpdateAccountRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if account is not None:
                request.account = account
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("account.name", request.account.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def provision_account_ticket(
        self,
        request: analytics_admin.ProvisionAccountTicketRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ProvisionAccountTicketResponse:
        r"""Requests a ticket for creating an account.

        Args:
            request (:class:`~.analytics_admin.ProvisionAccountTicketRequest`):
                The request object. Request message for
                ProvisionAccountTicket RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_admin.ProvisionAccountTicketResponse:
                Response message for
                ProvisionAccountTicket RPC.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.ProvisionAccountTicketRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ProvisionAccountTicketRequest):
            request = analytics_admin.ProvisionAccountTicketRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.provision_account_ticket]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_account_summaries(
        self,
        request: analytics_admin.ListAccountSummariesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountSummariesPager:
        r"""Returns summaries of all accounts accessible by the
        caller.

        Args:
            request (:class:`~.analytics_admin.ListAccountSummariesRequest`):
                The request object. Request message for
                ListAccountSummaries RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListAccountSummariesPager:
                Response message for
                ListAccountSummaries RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.ListAccountSummariesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListAccountSummariesRequest):
            request = analytics_admin.ListAccountSummariesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_account_summaries]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAccountSummariesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_property(
        self,
        request: analytics_admin.GetPropertyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Lookup for a single "GA4" Property.
        Throws "Target not found" if no such property found, if
        property is not of the type "GA4", or if caller does not
        have permissions to access it.

        Args:
            request (:class:`~.analytics_admin.GetPropertyRequest`):
                The request object. Request message for GetProperty RPC.
            name (:class:`str`):
                Required. The name of the property to lookup. Format:
                properties/{property_id} Example: "properties/1000".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Property:
                A resource message representing a
                Google Analytics GA4 property.

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
        # in a analytics_admin.GetPropertyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetPropertyRequest):
            request = analytics_admin.GetPropertyRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_properties(
        self,
        request: analytics_admin.ListPropertiesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPropertiesPager:
        r"""Returns child Properties under the specified parent
        Account.
        Only "GA4" properties will be returned.
        Properties will be excluded if the caller does not have
        access. Soft-deleted (ie: "trashed") properties are
        excluded by default. Returns an empty list if no
        relevant properties are found.

        Args:
            request (:class:`~.analytics_admin.ListPropertiesRequest`):
                The request object. Request message for ListProperties
                RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListPropertiesPager:
                Response message for ListProperties
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.ListPropertiesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListPropertiesRequest):
            request = analytics_admin.ListPropertiesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_properties]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPropertiesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_property(
        self,
        request: analytics_admin.CreatePropertyRequest = None,
        *,
        property: resources.Property = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Creates an "GA4" property with the specified location
        and attributes.

        Args:
            request (:class:`~.analytics_admin.CreatePropertyRequest`):
                The request object. Request message for CreateProperty
                RPC.
            property (:class:`~.resources.Property`):
                Required. The property to create.
                Note: the supplied property must specify
                its parent.
                This corresponds to the ``property`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([property])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreatePropertyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreatePropertyRequest):
            request = analytics_admin.CreatePropertyRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if property is not None:
                request.property = property

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_property]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_property(
        self,
        request: analytics_admin.DeletePropertyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Marks target Property as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        properties. However, they can be restored using the
        Trash Can UI.
        If the properties are not restored before the expiration
        time, the Property and all child resources (eg:
        GoogleAdsLinks, Streams, UserLinks) will be permanently
        purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found, or is not
        an GA4 Property.

        Args:
            request (:class:`~.analytics_admin.DeletePropertyRequest`):
                The request object. Request message for DeleteProperty
                RPC.
            name (:class:`str`):
                Required. The name of the Property to soft-delete.
                Format: properties/{property_id} Example:
                "properties/1000".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeletePropertyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeletePropertyRequest):
            request = analytics_admin.DeletePropertyRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_property(
        self,
        request: analytics_admin.UpdatePropertyRequest = None,
        *,
        property: resources.Property = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Updates a property.

        Args:
            request (:class:`~.analytics_admin.UpdatePropertyRequest`):
                The request object. Request message for UpdateProperty
                RPC.
            property (:class:`~.resources.Property`):
                Required. The property to update. The property's
                ``name`` field is used to identify the property to be
                updated.
                This corresponds to the ``property`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([property, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdatePropertyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdatePropertyRequest):
            request = analytics_admin.UpdatePropertyRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if property is not None:
                request.property = property
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("property.name", request.property.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_user_link(
        self,
        request: analytics_admin.GetUserLinkRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Gets information about a user's link to an account or
        property.

        Args:
            request (:class:`~.analytics_admin.GetUserLinkRequest`):
                The request object. Request message for GetUserLink RPC.
            name (:class:`str`):
                Required. Example format:
                accounts/1234/userLinks/5678
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

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
        # in a analytics_admin.GetUserLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetUserLinkRequest):
            request = analytics_admin.GetUserLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_user_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_get_user_links(
        self,
        request: analytics_admin.BatchGetUserLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchGetUserLinksResponse:
        r"""Gets information about multiple users' links to an
        account or property.

        Args:
            request (:class:`~.analytics_admin.BatchGetUserLinksRequest`):
                The request object. Request message for
                BatchGetUserLinks RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_admin.BatchGetUserLinksResponse:
                Response message for
                BatchGetUserLinks RPC.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.BatchGetUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.BatchGetUserLinksRequest):
            request = analytics_admin.BatchGetUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_get_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_user_links(
        self,
        request: analytics_admin.ListUserLinksRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUserLinksPager:
        r"""Lists all user links on an account or property.

        Args:
            request (:class:`~.analytics_admin.ListUserLinksRequest`):
                The request object. Request message for ListUserLinks
                RPC.
            parent (:class:`str`):
                Required. Example format:
                accounts/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListUserLinksPager:
                Response message for ListUserLinks
                RPC.
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
        # in a analytics_admin.ListUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListUserLinksRequest):
            request = analytics_admin.ListUserLinksRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListUserLinksPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def audit_user_links(
        self,
        request: analytics_admin.AuditUserLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AuditUserLinksPager:
        r"""Lists all user links on an account or property,
        including implicit ones that come from effective
        permissions granted by groups or organization admin
        roles.

        If a returned user link does not have direct
        permissions, they cannot be removed from the account or
        property directly with the DeleteUserLink command. They
        have to be removed from the group/etc that gives them
        permissions, which is currently only usable/discoverable
        in the GA or GMP UIs.

        Args:
            request (:class:`~.analytics_admin.AuditUserLinksRequest`):
                The request object. Request message for AuditUserLinks
                RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.AuditUserLinksPager:
                Response message for AuditUserLinks
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.AuditUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.AuditUserLinksRequest):
            request = analytics_admin.AuditUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.audit_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.AuditUserLinksPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_user_link(
        self,
        request: analytics_admin.CreateUserLinkRequest = None,
        *,
        parent: str = None,
        user_link: resources.UserLink = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Creates a user link on an account or property.
        If the user with the specified email already has
        permissions on the account or property, then the user's
        existing permissions will be unioned with the
        permissions specified in the new UserLink.

        Args:
            request (:class:`~.analytics_admin.CreateUserLinkRequest`):
                The request object. Request message for CreateUserLink
                RPC.
                Users can have multiple email addresses associated with
                their Google account, and one of these email addresses
                is the "primary" email address. Any of the email
                addresses associated with a Google account may be used
                for a new UserLink, but the returned UserLink will
                always contain the "primary" email address. As a result,
                the input and output email address for this request may
                differ.
            parent (:class:`str`):
                Required. Example format:
                accounts/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            user_link (:class:`~.resources.UserLink`):
                Required. The user link to create.
                This corresponds to the ``user_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, user_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateUserLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateUserLinkRequest):
            request = analytics_admin.CreateUserLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if user_link is not None:
                request.user_link = user_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_user_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_create_user_links(
        self,
        request: analytics_admin.BatchCreateUserLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchCreateUserLinksResponse:
        r"""Creates information about multiple users' links to an
        account or property.
        This method is transactional. If any UserLink cannot be
        created, none of the UserLinks will be created.

        Args:
            request (:class:`~.analytics_admin.BatchCreateUserLinksRequest`):
                The request object. Request message for
                BatchCreateUserLinks RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_admin.BatchCreateUserLinksResponse:
                Response message for
                BatchCreateUserLinks RPC.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.BatchCreateUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.BatchCreateUserLinksRequest):
            request = analytics_admin.BatchCreateUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_user_link(
        self,
        request: analytics_admin.UpdateUserLinkRequest = None,
        *,
        user_link: resources.UserLink = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Updates a user link on an account or property.

        Args:
            request (:class:`~.analytics_admin.UpdateUserLinkRequest`):
                The request object. Request message for UpdateUserLink
                RPC.
            user_link (:class:`~.resources.UserLink`):
                Required. The user link to update.
                This corresponds to the ``user_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([user_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateUserLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateUserLinkRequest):
            request = analytics_admin.UpdateUserLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if user_link is not None:
                request.user_link = user_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_user_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("user_link.name", request.user_link.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_update_user_links(
        self,
        request: analytics_admin.BatchUpdateUserLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchUpdateUserLinksResponse:
        r"""Updates information about multiple users' links to an
        account or property.

        Args:
            request (:class:`~.analytics_admin.BatchUpdateUserLinksRequest`):
                The request object. Request message for
                BatchUpdateUserLinks RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_admin.BatchUpdateUserLinksResponse:
                Response message for
                BatchUpdateUserLinks RPC.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.BatchUpdateUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.BatchUpdateUserLinksRequest):
            request = analytics_admin.BatchUpdateUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_update_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_user_link(
        self,
        request: analytics_admin.DeleteUserLinkRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a user link on an account or property.

        Args:
            request (:class:`~.analytics_admin.DeleteUserLinkRequest`):
                The request object. Request message for DeleteUserLink
                RPC.
            name (:class:`str`):
                Required. Example format:
                accounts/1234/userLinks/5678
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteUserLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteUserLinkRequest):
            request = analytics_admin.DeleteUserLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_user_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def batch_delete_user_links(
        self,
        request: analytics_admin.BatchDeleteUserLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes information about multiple users' links to an
        account or property.

        Args:
            request (:class:`~.analytics_admin.BatchDeleteUserLinksRequest`):
                The request object. Request message for
                BatchDeleteUserLinks RPC.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.BatchDeleteUserLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.BatchDeleteUserLinksRequest):
            request = analytics_admin.BatchDeleteUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_delete_user_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_web_data_stream(
        self,
        request: analytics_admin.GetWebDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.WebDataStream:
        r"""Lookup for a single WebDataStream
        Throws "Target not found" if no such web data stream
        found, or if the caller does not have permissions to
        access it.

        Args:
            request (:class:`~.analytics_admin.GetWebDataStreamRequest`):
                The request object. Request message for GetWebDataStream
                RPC.
            name (:class:`str`):
                Required. The name of the web data stream to lookup.
                Format:
                properties/{property_id}/webDataStreams/{stream_id}
                Example: "properties/123/webDataStreams/456".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.WebDataStream:
                A resource message representing a
                Google Analytics web stream.

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
        # in a analytics_admin.GetWebDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetWebDataStreamRequest):
            request = analytics_admin.GetWebDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_web_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_web_data_stream(
        self,
        request: analytics_admin.DeleteWebDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a web stream on a property.

        Args:
            request (:class:`~.analytics_admin.DeleteWebDataStreamRequest`):
                The request object. Request message for
                DeleteWebDataStream RPC.
            name (:class:`str`):
                Required. The name of the web data stream to delete.
                Format:
                properties/{property_id}/webDataStreams/{stream_id}
                Example: "properties/123/webDataStreams/456".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteWebDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteWebDataStreamRequest):
            request = analytics_admin.DeleteWebDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_web_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_web_data_stream(
        self,
        request: analytics_admin.UpdateWebDataStreamRequest = None,
        *,
        web_data_stream: resources.WebDataStream = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.WebDataStream:
        r"""Updates a web stream on a property.

        Args:
            request (:class:`~.analytics_admin.UpdateWebDataStreamRequest`):
                The request object. Request message for
                UpdateWebDataStream RPC.
            web_data_stream (:class:`~.resources.WebDataStream`):
                Required. The web stream to update. The ``name`` field
                is used to identify the web stream to be updated.
                This corresponds to the ``web_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.WebDataStream:
                A resource message representing a
                Google Analytics web stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([web_data_stream, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateWebDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateWebDataStreamRequest):
            request = analytics_admin.UpdateWebDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if web_data_stream is not None:
                request.web_data_stream = web_data_stream
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_web_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("web_data_stream.name", request.web_data_stream.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_web_data_stream(
        self,
        request: analytics_admin.CreateWebDataStreamRequest = None,
        *,
        parent: str = None,
        web_data_stream: resources.WebDataStream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.WebDataStream:
        r"""Creates a web stream with the specified location and
        attributes.

        Args:
            request (:class:`~.analytics_admin.CreateWebDataStreamRequest`):
                The request object. Request message for
                CreateWebDataStream RPC.
            parent (:class:`str`):
                Required. The parent resource where
                this web data stream will be created.
                Format: properties/123
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            web_data_stream (:class:`~.resources.WebDataStream`):
                Required. The web stream to create.
                This corresponds to the ``web_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.WebDataStream:
                A resource message representing a
                Google Analytics web stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, web_data_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateWebDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateWebDataStreamRequest):
            request = analytics_admin.CreateWebDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if web_data_stream is not None:
                request.web_data_stream = web_data_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_web_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_web_data_streams(
        self,
        request: analytics_admin.ListWebDataStreamsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWebDataStreamsPager:
        r"""Returns child web data streams under the specified
        parent property.
        Web data streams will be excluded if the caller does not
        have access. Returns an empty list if no relevant web
        data streams are found.

        Args:
            request (:class:`~.analytics_admin.ListWebDataStreamsRequest`):
                The request object. Request message for
                ListWebDataStreams RPC.
            parent (:class:`str`):
                Required. The name of the parent
                property. For example, to list results
                of web streams under the property with
                Id 123: "properties/123".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListWebDataStreamsPager:
                Request message for
                ListWebDataStreams RPC.
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
        # in a analytics_admin.ListWebDataStreamsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListWebDataStreamsRequest):
            request = analytics_admin.ListWebDataStreamsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_web_data_streams]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListWebDataStreamsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_ios_app_data_stream(
        self,
        request: analytics_admin.GetIosAppDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IosAppDataStream:
        r"""Lookup for a single IosAppDataStream
        Throws "Target not found" if no such iOS app data stream
        found, or if the caller does not have permissions to
        access it.

        Args:
            request (:class:`~.analytics_admin.GetIosAppDataStreamRequest`):
                The request object. Request message for
                GetIosAppDataStream RPC.
            name (:class:`str`):
                Required. The name of the iOS app data stream to lookup.
                Format:
                properties/{property_id}/iosAppDataStreams/{stream_id}
                Example: "properties/123/iosAppDataStreams/456".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.IosAppDataStream:
                A resource message representing a
                Google Analytics IOS app stream.

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
        # in a analytics_admin.GetIosAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetIosAppDataStreamRequest):
            request = analytics_admin.GetIosAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_ios_app_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_ios_app_data_stream(
        self,
        request: analytics_admin.DeleteIosAppDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an iOS app stream on a property.

        Args:
            request (:class:`~.analytics_admin.DeleteIosAppDataStreamRequest`):
                The request object. Request message for
                DeleteIosAppDataStream RPC.
            name (:class:`str`):
                Required. The name of the iOS app data stream to delete.
                Format:
                properties/{property_id}/iosAppDataStreams/{stream_id}
                Example: "properties/123/iosAppDataStreams/456".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteIosAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteIosAppDataStreamRequest):
            request = analytics_admin.DeleteIosAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_ios_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_ios_app_data_stream(
        self,
        request: analytics_admin.UpdateIosAppDataStreamRequest = None,
        *,
        ios_app_data_stream: resources.IosAppDataStream = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IosAppDataStream:
        r"""Updates an iOS app stream on a property.

        Args:
            request (:class:`~.analytics_admin.UpdateIosAppDataStreamRequest`):
                The request object. Request message for
                UpdateIosAppDataStream RPC.
            ios_app_data_stream (:class:`~.resources.IosAppDataStream`):
                Required. The iOS app stream to update. The ``name``
                field is used to identify the iOS app stream to be
                updated.
                This corresponds to the ``ios_app_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.IosAppDataStream:
                A resource message representing a
                Google Analytics IOS app stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([ios_app_data_stream, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateIosAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateIosAppDataStreamRequest):
            request = analytics_admin.UpdateIosAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if ios_app_data_stream is not None:
                request.ios_app_data_stream = ios_app_data_stream
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_ios_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("ios_app_data_stream.name", request.ios_app_data_stream.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_ios_app_data_stream(
        self,
        request: analytics_admin.CreateIosAppDataStreamRequest = None,
        *,
        parent: str = None,
        ios_app_data_stream: resources.IosAppDataStream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IosAppDataStream:
        r"""Creates an iOS app data stream with the specified
        location and attributes.

        Args:
            request (:class:`~.analytics_admin.CreateIosAppDataStreamRequest`):
                The request object. Request message for
                CreateIosAppDataStream RPC.
            parent (:class:`str`):
                Required. The parent resource where
                this ios app data stream will be
                created. Format: properties/123
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ios_app_data_stream (:class:`~.resources.IosAppDataStream`):
                Required. The iOS app data stream to
                create.
                This corresponds to the ``ios_app_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.IosAppDataStream:
                A resource message representing a
                Google Analytics IOS app stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, ios_app_data_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateIosAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateIosAppDataStreamRequest):
            request = analytics_admin.CreateIosAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if ios_app_data_stream is not None:
                request.ios_app_data_stream = ios_app_data_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_ios_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_ios_app_data_streams(
        self,
        request: analytics_admin.ListIosAppDataStreamsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIosAppDataStreamsPager:
        r"""Returns child iOS app data streams under the
        specified parent property.
        iOS app data streams will be excluded if the caller does
        not have access. Returns an empty list if no relevant
        iOS app data streams are found.

        Args:
            request (:class:`~.analytics_admin.ListIosAppDataStreamsRequest`):
                The request object. Request message for
                ListIosAppDataStreams RPC.
            parent (:class:`str`):
                Required. The name of the parent
                property. For example, to list results
                of app streams under the property with
                Id 123: "properties/123".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListIosAppDataStreamsPager:
                Request message for
                ListIosAppDataStreams RPC.
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
        # in a analytics_admin.ListIosAppDataStreamsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListIosAppDataStreamsRequest):
            request = analytics_admin.ListIosAppDataStreamsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_ios_app_data_streams
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
        response = pagers.ListIosAppDataStreamsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_android_app_data_stream(
        self,
        request: analytics_admin.GetAndroidAppDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AndroidAppDataStream:
        r"""Lookup for a single AndroidAppDataStream
        Throws "Target not found" if no such android app data
        stream found, or if the caller does not have permissions
        to access it.

        Args:
            request (:class:`~.analytics_admin.GetAndroidAppDataStreamRequest`):
                The request object. Request message for
                GetAndroidAppDataStream RPC.
            name (:class:`str`):
                Required. The name of the android app data stream to
                lookup. Format:
                properties/{property_id}/androidAppDataStreams/{stream_id}
                Example: "properties/123/androidAppDataStreams/456".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.AndroidAppDataStream:
                A resource message representing a
                Google Analytics Android app stream.

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
        # in a analytics_admin.GetAndroidAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetAndroidAppDataStreamRequest):
            request = analytics_admin.GetAndroidAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_android_app_data_stream
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

    def delete_android_app_data_stream(
        self,
        request: analytics_admin.DeleteAndroidAppDataStreamRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an android app stream on a property.

        Args:
            request (:class:`~.analytics_admin.DeleteAndroidAppDataStreamRequest`):
                The request object. Request message for
                DeleteAndroidAppDataStream RPC.
            name (:class:`str`):
                Required. The name of the android app data stream to
                delete. Format:
                properties/{property_id}/androidAppDataStreams/{stream_id}
                Example: "properties/123/androidAppDataStreams/456".
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteAndroidAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteAndroidAppDataStreamRequest):
            request = analytics_admin.DeleteAndroidAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_android_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_android_app_data_stream(
        self,
        request: analytics_admin.UpdateAndroidAppDataStreamRequest = None,
        *,
        android_app_data_stream: resources.AndroidAppDataStream = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AndroidAppDataStream:
        r"""Updates an android app stream on a property.

        Args:
            request (:class:`~.analytics_admin.UpdateAndroidAppDataStreamRequest`):
                The request object. Request message for
                UpdateAndroidAppDataStream RPC.
            android_app_data_stream (:class:`~.resources.AndroidAppDataStream`):
                Required. The android app stream to update. The ``name``
                field is used to identify the android app stream to be
                updated.
                This corresponds to the ``android_app_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.AndroidAppDataStream:
                A resource message representing a
                Google Analytics Android app stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([android_app_data_stream, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateAndroidAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateAndroidAppDataStreamRequest):
            request = analytics_admin.UpdateAndroidAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if android_app_data_stream is not None:
                request.android_app_data_stream = android_app_data_stream
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_android_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "android_app_data_stream.name",
                        request.android_app_data_stream.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_android_app_data_stream(
        self,
        request: analytics_admin.CreateAndroidAppDataStreamRequest = None,
        *,
        parent: str = None,
        android_app_data_stream: resources.AndroidAppDataStream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AndroidAppDataStream:
        r"""Creates an android app stream with the specified
        location and attributes.

        Args:
            request (:class:`~.analytics_admin.CreateAndroidAppDataStreamRequest`):
                The request object. Request message for
                CreateAndroidAppDataStream RPC.
            parent (:class:`str`):
                Required. The parent resource where
                this android app data stream will be
                created. Format: properties/123
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            android_app_data_stream (:class:`~.resources.AndroidAppDataStream`):
                Required. The android app stream to
                create.
                This corresponds to the ``android_app_data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.AndroidAppDataStream:
                A resource message representing a
                Google Analytics Android app stream.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, android_app_data_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateAndroidAppDataStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateAndroidAppDataStreamRequest):
            request = analytics_admin.CreateAndroidAppDataStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if android_app_data_stream is not None:
                request.android_app_data_stream = android_app_data_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_android_app_data_stream
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_android_app_data_streams(
        self,
        request: analytics_admin.ListAndroidAppDataStreamsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAndroidAppDataStreamsPager:
        r"""Returns child android app streams under the specified
        parent property.
        Android app streams will be excluded if the caller does
        not have access. Returns an empty list if no relevant
        android app streams are found.

        Args:
            request (:class:`~.analytics_admin.ListAndroidAppDataStreamsRequest`):
                The request object. Request message for
                ListAndroidAppDataStreams RPC.
            parent (:class:`str`):
                Required. The name of the parent
                property. For example, to limit results
                to app streams under the property with
                Id 123: "properties/123".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListAndroidAppDataStreamsPager:
                Request message for
                ListAndroidDataStreams RPC.
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
        # in a analytics_admin.ListAndroidAppDataStreamsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListAndroidAppDataStreamsRequest):
            request = analytics_admin.ListAndroidAppDataStreamsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_android_app_data_streams
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
        response = pagers.ListAndroidAppDataStreamsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_enhanced_measurement_settings(
        self,
        request: analytics_admin.GetEnhancedMeasurementSettingsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.EnhancedMeasurementSettings:
        r"""Returns the singleton enhanced measurement settings
        for this web stream. Note that the stream must enable
        enhanced measurement for these settings to take effect.

        Args:
            request (:class:`~.analytics_admin.GetEnhancedMeasurementSettingsRequest`):
                The request object. Request message for
                GetEnhancedMeasurementSettings RPC.
            name (:class:`str`):
                Required. The name of the settings to lookup. Format:

                properties/{property_id}/webDataStreams/{stream_id}/enhancedMeasurementSettings
                Example:
                "properties/1000/webDataStreams/2000/enhancedMeasurementSettings".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.EnhancedMeasurementSettings:
                Singleton resource under a
                WebDataStream, configuring measurement
                of additional site interactions and
                content.

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
        # in a analytics_admin.GetEnhancedMeasurementSettingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, analytics_admin.GetEnhancedMeasurementSettingsRequest
        ):
            request = analytics_admin.GetEnhancedMeasurementSettingsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_enhanced_measurement_settings
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

    def update_enhanced_measurement_settings(
        self,
        request: analytics_admin.UpdateEnhancedMeasurementSettingsRequest = None,
        *,
        enhanced_measurement_settings: resources.EnhancedMeasurementSettings = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.EnhancedMeasurementSettings:
        r"""Updates the singleton enhanced measurement settings
        for this web stream. Note that the stream must enable
        enhanced measurement for these settings to take effect.

        Args:
            request (:class:`~.analytics_admin.UpdateEnhancedMeasurementSettingsRequest`):
                The request object. Request message for
                UpdateEnhancedMeasurementSettings RPC.
            enhanced_measurement_settings (:class:`~.resources.EnhancedMeasurementSettings`):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.
                This corresponds to the ``enhanced_measurement_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.EnhancedMeasurementSettings:
                Singleton resource under a
                WebDataStream, configuring measurement
                of additional site interactions and
                content.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([enhanced_measurement_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateEnhancedMeasurementSettingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, analytics_admin.UpdateEnhancedMeasurementSettingsRequest
        ):
            request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if enhanced_measurement_settings is not None:
                request.enhanced_measurement_settings = enhanced_measurement_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_enhanced_measurement_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "enhanced_measurement_settings.name",
                        request.enhanced_measurement_settings.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_firebase_link(
        self,
        request: analytics_admin.CreateFirebaseLinkRequest = None,
        *,
        parent: str = None,
        firebase_link: resources.FirebaseLink = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.FirebaseLink:
        r"""Creates a FirebaseLink.
        Properties can have at most one FirebaseLink.

        Args:
            request (:class:`~.analytics_admin.CreateFirebaseLinkRequest`):
                The request object. Request message for
                CreateFirebaseLink RPC
            parent (:class:`str`):
                Required. Format: properties/{property_id} Example:
                properties/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firebase_link (:class:`~.resources.FirebaseLink`):
                Required. The Firebase link to
                create.
                This corresponds to the ``firebase_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.FirebaseLink:
                A link between an GA4 property and a
                Firebase project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, firebase_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateFirebaseLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateFirebaseLinkRequest):
            request = analytics_admin.CreateFirebaseLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if firebase_link is not None:
                request.firebase_link = firebase_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_firebase_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_firebase_link(
        self,
        request: analytics_admin.UpdateFirebaseLinkRequest = None,
        *,
        firebase_link: resources.FirebaseLink = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.FirebaseLink:
        r"""Updates a FirebaseLink on a property

        Args:
            request (:class:`~.analytics_admin.UpdateFirebaseLinkRequest`):
                The request object. Request message for
                UpdateFirebaseLink RPC
            firebase_link (:class:`~.resources.FirebaseLink`):
                Required. The Firebase link to
                update.
                This corresponds to the ``firebase_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.FirebaseLink:
                A link between an GA4 property and a
                Firebase project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([firebase_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateFirebaseLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateFirebaseLinkRequest):
            request = analytics_admin.UpdateFirebaseLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if firebase_link is not None:
                request.firebase_link = firebase_link
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_firebase_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("firebase_link.name", request.firebase_link.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_firebase_link(
        self,
        request: analytics_admin.DeleteFirebaseLinkRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a FirebaseLink on a property

        Args:
            request (:class:`~.analytics_admin.DeleteFirebaseLinkRequest`):
                The request object. Request message for
                DeleteFirebaseLink RPC
            name (:class:`str`):
                Required. Format:
                properties/{property_id}/firebaseLinks/{firebase_link_id}
                Example: properties/1234/firebaseLinks/5678
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteFirebaseLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteFirebaseLinkRequest):
            request = analytics_admin.DeleteFirebaseLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_firebase_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def list_firebase_links(
        self,
        request: analytics_admin.ListFirebaseLinksRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ListFirebaseLinksResponse:
        r"""Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        Args:
            request (:class:`~.analytics_admin.ListFirebaseLinksRequest`):
                The request object. Request message for
                ListFirebaseLinks RPC
            parent (:class:`str`):
                Required. Format: properties/{property_id} Example:
                properties/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.analytics_admin.ListFirebaseLinksResponse:
                Response message for
                ListFirebaseLinks RPC

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
        # in a analytics_admin.ListFirebaseLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListFirebaseLinksRequest):
            request = analytics_admin.ListFirebaseLinksRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_firebase_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_global_site_tag(
        self,
        request: analytics_admin.GetGlobalSiteTagRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GlobalSiteTag:
        r"""Returns the Site Tag for the specified web stream.
        Site Tags are immutable singletons.

        Args:
            request (:class:`~.analytics_admin.GetGlobalSiteTagRequest`):
                The request object. Request message for GetGlobalSiteTag
                RPC.
            name (:class:`str`):
                Required. The name of the site tag to lookup. Note that
                site tags are singletons and do not have unique IDs.
                Format:
                properties/{property_id}/webDataStreams/{stream_id}/globalSiteTag
                Example:
                "properties/123/webDataStreams/456/globalSiteTag".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.GlobalSiteTag:
                Read-only resource with the tag for
                sending data from a website to a
                WebDataStream.

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
        # in a analytics_admin.GetGlobalSiteTagRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetGlobalSiteTagRequest):
            request = analytics_admin.GetGlobalSiteTagRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_global_site_tag]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_google_ads_link(
        self,
        request: analytics_admin.CreateGoogleAdsLinkRequest = None,
        *,
        parent: str = None,
        google_ads_link: resources.GoogleAdsLink = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Creates a GoogleAdsLink.

        Args:
            request (:class:`~.analytics_admin.CreateGoogleAdsLinkRequest`):
                The request object. Request message for
                CreateGoogleAdsLink RPC
            parent (:class:`str`):
                Required. Example format:
                properties/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            google_ads_link (:class:`~.resources.GoogleAdsLink`):
                Required. The GoogleAdsLink to
                create.
                This corresponds to the ``google_ads_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.GoogleAdsLink:
                A link between an GA4 property and a
                Google Ads account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, google_ads_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.CreateGoogleAdsLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.CreateGoogleAdsLinkRequest):
            request = analytics_admin.CreateGoogleAdsLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if google_ads_link is not None:
                request.google_ads_link = google_ads_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_google_ads_link(
        self,
        request: analytics_admin.UpdateGoogleAdsLinkRequest = None,
        *,
        google_ads_link: resources.GoogleAdsLink = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Updates a GoogleAdsLink on a property

        Args:
            request (:class:`~.analytics_admin.UpdateGoogleAdsLinkRequest`):
                The request object. Request message for
                UpdateGoogleAdsLink RPC
            google_ads_link (:class:`~.resources.GoogleAdsLink`):
                The GoogleAdsLink to update
                This corresponds to the ``google_ads_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.GoogleAdsLink:
                A link between an GA4 property and a
                Google Ads account.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([google_ads_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.UpdateGoogleAdsLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.UpdateGoogleAdsLinkRequest):
            request = analytics_admin.UpdateGoogleAdsLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if google_ads_link is not None:
                request.google_ads_link = google_ads_link
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("google_ads_link.name", request.google_ads_link.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_google_ads_link(
        self,
        request: analytics_admin.DeleteGoogleAdsLinkRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a GoogleAdsLink on a property

        Args:
            request (:class:`~.analytics_admin.DeleteGoogleAdsLinkRequest`):
                The request object. Request message for
                DeleteGoogleAdsLink RPC.
            name (:class:`str`):
                Required. Example format:
                properties/1234/googleAdsLinks/5678
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

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_admin.DeleteGoogleAdsLinkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.DeleteGoogleAdsLinkRequest):
            request = analytics_admin.DeleteGoogleAdsLinkRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def list_google_ads_links(
        self,
        request: analytics_admin.ListGoogleAdsLinksRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGoogleAdsLinksPager:
        r"""Lists GoogleAdsLinks on a property.

        Args:
            request (:class:`~.analytics_admin.ListGoogleAdsLinksRequest`):
                The request object. Request message for
                ListGoogleAdsLinks RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListGoogleAdsLinksPager:
                Response message for
                ListGoogleAdsLinks RPC.
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
        # in a analytics_admin.ListGoogleAdsLinksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.ListGoogleAdsLinksRequest):
            request = analytics_admin.ListGoogleAdsLinksRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_google_ads_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListGoogleAdsLinksPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_data_sharing_settings(
        self,
        request: analytics_admin.GetDataSharingSettingsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataSharingSettings:
        r"""Get data sharing settings on an account.
        Data sharing settings are singletons.

        Args:
            request (:class:`~.analytics_admin.GetDataSharingSettingsRequest`):
                The request object. Request message for
                GetDataSharingSettings RPC.
            name (:class:`str`):
                Required. The name of the settings to
                lookup. Format:
                accounts/{account}/dataSharingSettings
                Example:
                "accounts/1000/dataSharingSettings".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.DataSharingSettings:
                A resource message representing data
                sharing settings of a Google Analytics
                account.

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
        # in a analytics_admin.GetDataSharingSettingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_admin.GetDataSharingSettingsRequest):
            request = analytics_admin.GetDataSharingSettingsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_data_sharing_settings
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-analytics-admin",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AnalyticsAdminServiceClient",)
