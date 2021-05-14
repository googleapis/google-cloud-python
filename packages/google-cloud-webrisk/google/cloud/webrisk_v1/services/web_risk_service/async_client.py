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

from google.cloud.webrisk_v1.types import webrisk
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import WebRiskServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import WebRiskServiceGrpcAsyncIOTransport
from .client import WebRiskServiceClient


class WebRiskServiceAsyncClient:
    """Web Risk API defines an interface to detect malicious URLs on
    your website and in client applications.
    """

    _client: WebRiskServiceClient

    DEFAULT_ENDPOINT = WebRiskServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = WebRiskServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        WebRiskServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        WebRiskServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(WebRiskServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        WebRiskServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        WebRiskServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        WebRiskServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(WebRiskServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        WebRiskServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(WebRiskServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        WebRiskServiceClient.parse_common_location_path
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
            WebRiskServiceAsyncClient: The constructed client.
        """
        return WebRiskServiceClient.from_service_account_info.__func__(WebRiskServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            WebRiskServiceAsyncClient: The constructed client.
        """
        return WebRiskServiceClient.from_service_account_file.__func__(WebRiskServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> WebRiskServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            WebRiskServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(WebRiskServiceClient).get_transport_class, type(WebRiskServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, WebRiskServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the web risk service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.WebRiskServiceTransport]): The
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
        self._client = WebRiskServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def compute_threat_list_diff(
        self,
        request: webrisk.ComputeThreatListDiffRequest = None,
        *,
        threat_type: webrisk.ThreatType = None,
        version_token: bytes = None,
        constraints: webrisk.ComputeThreatListDiffRequest.Constraints = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> webrisk.ComputeThreatListDiffResponse:
        r"""Gets the most recent threat list diffs. These diffs
        should be applied to a local database of hashes to keep
        it up-to-date. If the local database is empty or
        excessively out-of-date, a complete snapshot of the
        database will be returned. This Method only updates a
        single ThreatList at a time. To update multiple
        ThreatList databases, this method needs to be called
        once for each list.

        Args:
            request (:class:`google.cloud.webrisk_v1.types.ComputeThreatListDiffRequest`):
                The request object. Describes an API diff request.
            threat_type (:class:`google.cloud.webrisk_v1.types.ThreatType`):
                Required. The threat list to update.
                Only a single ThreatType should be
                specified.

                This corresponds to the ``threat_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            version_token (:class:`bytes`):
                The current version token of the
                client for the requested list (the
                client version that was received from
                the last successful diff). If the client
                does not have a version token (this is
                the first time calling
                ComputeThreatListDiff), this may be left
                empty and a full database snapshot will
                be returned.

                This corresponds to the ``version_token`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            constraints (:class:`google.cloud.webrisk_v1.types.ComputeThreatListDiffRequest.Constraints`):
                Required. The constraints associated
                with this request.

                This corresponds to the ``constraints`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.webrisk_v1.types.ComputeThreatListDiffResponse:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([threat_type, version_token, constraints])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = webrisk.ComputeThreatListDiffRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if threat_type is not None:
            request.threat_type = threat_type
        if version_token is not None:
            request.version_token = version_token
        if constraints is not None:
            request.constraints = constraints

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.compute_threat_list_diff,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def search_uris(
        self,
        request: webrisk.SearchUrisRequest = None,
        *,
        uri: str = None,
        threat_types: Sequence[webrisk.ThreatType] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> webrisk.SearchUrisResponse:
        r"""This method is used to check whether a URI is on a
        given threatList. Multiple threatLists may be searched
        in a single query. The response will list all requested
        threatLists the URI was found to match. If the URI is
        not found on any of the requested ThreatList an empty
        response will be returned.

        Args:
            request (:class:`google.cloud.webrisk_v1.types.SearchUrisRequest`):
                The request object. Request to check URI entries against
                threatLists.
            uri (:class:`str`):
                Required. The URI to be checked for
                matches.

                This corresponds to the ``uri`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            threat_types (:class:`Sequence[google.cloud.webrisk_v1.types.ThreatType]`):
                Required. The ThreatLists to search
                in. Multiple ThreatLists may be
                specified.

                This corresponds to the ``threat_types`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.webrisk_v1.types.SearchUrisResponse:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([uri, threat_types])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = webrisk.SearchUrisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if uri is not None:
            request.uri = uri
        if threat_types:
            request.threat_types.extend(threat_types)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_uris,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def search_hashes(
        self,
        request: webrisk.SearchHashesRequest = None,
        *,
        hash_prefix: bytes = None,
        threat_types: Sequence[webrisk.ThreatType] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> webrisk.SearchHashesResponse:
        r"""Gets the full hashes that match the requested hash
        prefix. This is used after a hash prefix is looked up in
        a threatList and there is a match. The client side
        threatList only holds partial hashes so the client must
        query this method to determine if there is a full hash
        match of a threat.

        Args:
            request (:class:`google.cloud.webrisk_v1.types.SearchHashesRequest`):
                The request object. Request to return full hashes
                matched by the provided hash prefixes.
            hash_prefix (:class:`bytes`):
                A hash prefix, consisting of the most
                significant 4-32 bytes of a SHA256 hash.
                For JSON requests, this field is
                base64-encoded.

                This corresponds to the ``hash_prefix`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            threat_types (:class:`Sequence[google.cloud.webrisk_v1.types.ThreatType]`):
                Required. The ThreatLists to search
                in. Multiple ThreatLists may be
                specified.

                This corresponds to the ``threat_types`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.webrisk_v1.types.SearchHashesResponse:

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([hash_prefix, threat_types])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = webrisk.SearchHashesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if hash_prefix is not None:
            request.hash_prefix = hash_prefix
        if threat_types:
            request.threat_types.extend(threat_types)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_hashes,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_submission(
        self,
        request: webrisk.CreateSubmissionRequest = None,
        *,
        parent: str = None,
        submission: webrisk.Submission = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> webrisk.Submission:
        r"""Creates a Submission of a URI suspected of containing phishing
        content to be reviewed. If the result verifies the existence of
        malicious phishing content, the site will be added to the
        `Google's Social Engineering
        lists <https://support.google.com/webmasters/answer/6350487/>`__
        in order to protect users that could get exposed to this threat
        in the future. Only projects with CREATE_SUBMISSION_USERS
        visibility can use this method.

        Args:
            request (:class:`google.cloud.webrisk_v1.types.CreateSubmissionRequest`):
                The request object. Request to send a potentially phishy
                URI to WebRisk.
            parent (:class:`str`):
                Required. The name of the project that is making the
                submission. This string is in the format
                "projects/{project_number}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            submission (:class:`google.cloud.webrisk_v1.types.Submission`):
                Required. The submission that
                contains the content of the phishing
                report.

                This corresponds to the ``submission`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.webrisk_v1.types.Submission:
                Wraps a URI that might be displaying
                phishing content.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, submission])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = webrisk.CreateSubmissionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if submission is not None:
            request.submission = submission

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_submission,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-webrisk",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("WebRiskServiceAsyncClient",)
