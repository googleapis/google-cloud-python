# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.ads.marketingplatform_admin_v1alpha.types import (
    marketingplatform_admin,
    resources,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseMarketingplatformAdminServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class MarketingplatformAdminServiceRestInterceptor:
    """Interceptor for MarketingplatformAdminService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MarketingplatformAdminServiceRestTransport.

    .. code-block:: python
        class MyCustomMarketingplatformAdminServiceInterceptor(MarketingplatformAdminServiceRestInterceptor):
            def pre_create_analytics_account_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_analytics_account_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_analytics_account_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_organization(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_organization(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_analytics_account_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_analytics_account_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_property_service_level(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_property_service_level(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MarketingplatformAdminServiceRestTransport(interceptor=MyCustomMarketingplatformAdminServiceInterceptor())
        client = MarketingplatformAdminServiceClient(transport=transport)


    """

    def pre_create_analytics_account_link(
        self,
        request: marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_analytics_account_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MarketingplatformAdminService server.
        """
        return request, metadata

    def post_create_analytics_account_link(
        self, response: resources.AnalyticsAccountLink
    ) -> resources.AnalyticsAccountLink:
        """Post-rpc interceptor for create_analytics_account_link

        DEPRECATED. Please use the `post_create_analytics_account_link_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the MarketingplatformAdminService server but before
        it is returned to user code. This `post_create_analytics_account_link` interceptor runs
        before the `post_create_analytics_account_link_with_metadata` interceptor.
        """
        return response

    def post_create_analytics_account_link_with_metadata(
        self,
        response: resources.AnalyticsAccountLink,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[resources.AnalyticsAccountLink, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for create_analytics_account_link

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the MarketingplatformAdminService server but before it is returned to user code.

        We recommend only using this `post_create_analytics_account_link_with_metadata`
        interceptor in new development instead of the `post_create_analytics_account_link` interceptor.
        When both interceptors are used, this `post_create_analytics_account_link_with_metadata` interceptor runs after the
        `post_create_analytics_account_link` interceptor. The (possibly modified) response returned by
        `post_create_analytics_account_link` will be passed to
        `post_create_analytics_account_link_with_metadata`.
        """
        return response, metadata

    def pre_delete_analytics_account_link(
        self,
        request: marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete_analytics_account_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MarketingplatformAdminService server.
        """
        return request, metadata

    def pre_get_organization(
        self,
        request: marketingplatform_admin.GetOrganizationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.GetOrganizationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get_organization

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MarketingplatformAdminService server.
        """
        return request, metadata

    def post_get_organization(
        self, response: resources.Organization
    ) -> resources.Organization:
        """Post-rpc interceptor for get_organization

        DEPRECATED. Please use the `post_get_organization_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the MarketingplatformAdminService server but before
        it is returned to user code. This `post_get_organization` interceptor runs
        before the `post_get_organization_with_metadata` interceptor.
        """
        return response

    def post_get_organization_with_metadata(
        self,
        response: resources.Organization,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[resources.Organization, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get_organization

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the MarketingplatformAdminService server but before it is returned to user code.

        We recommend only using this `post_get_organization_with_metadata`
        interceptor in new development instead of the `post_get_organization` interceptor.
        When both interceptors are used, this `post_get_organization_with_metadata` interceptor runs after the
        `post_get_organization` interceptor. The (possibly modified) response returned by
        `post_get_organization` will be passed to
        `post_get_organization_with_metadata`.
        """
        return response, metadata

    def pre_list_analytics_account_links(
        self,
        request: marketingplatform_admin.ListAnalyticsAccountLinksRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.ListAnalyticsAccountLinksRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_analytics_account_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MarketingplatformAdminService server.
        """
        return request, metadata

    def post_list_analytics_account_links(
        self, response: marketingplatform_admin.ListAnalyticsAccountLinksResponse
    ) -> marketingplatform_admin.ListAnalyticsAccountLinksResponse:
        """Post-rpc interceptor for list_analytics_account_links

        DEPRECATED. Please use the `post_list_analytics_account_links_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the MarketingplatformAdminService server but before
        it is returned to user code. This `post_list_analytics_account_links` interceptor runs
        before the `post_list_analytics_account_links_with_metadata` interceptor.
        """
        return response

    def post_list_analytics_account_links_with_metadata(
        self,
        response: marketingplatform_admin.ListAnalyticsAccountLinksResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.ListAnalyticsAccountLinksResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_analytics_account_links

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the MarketingplatformAdminService server but before it is returned to user code.

        We recommend only using this `post_list_analytics_account_links_with_metadata`
        interceptor in new development instead of the `post_list_analytics_account_links` interceptor.
        When both interceptors are used, this `post_list_analytics_account_links_with_metadata` interceptor runs after the
        `post_list_analytics_account_links` interceptor. The (possibly modified) response returned by
        `post_list_analytics_account_links` will be passed to
        `post_list_analytics_account_links_with_metadata`.
        """
        return response, metadata

    def pre_set_property_service_level(
        self,
        request: marketingplatform_admin.SetPropertyServiceLevelRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.SetPropertyServiceLevelRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for set_property_service_level

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MarketingplatformAdminService server.
        """
        return request, metadata

    def post_set_property_service_level(
        self, response: marketingplatform_admin.SetPropertyServiceLevelResponse
    ) -> marketingplatform_admin.SetPropertyServiceLevelResponse:
        """Post-rpc interceptor for set_property_service_level

        DEPRECATED. Please use the `post_set_property_service_level_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the MarketingplatformAdminService server but before
        it is returned to user code. This `post_set_property_service_level` interceptor runs
        before the `post_set_property_service_level_with_metadata` interceptor.
        """
        return response

    def post_set_property_service_level_with_metadata(
        self,
        response: marketingplatform_admin.SetPropertyServiceLevelResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        marketingplatform_admin.SetPropertyServiceLevelResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for set_property_service_level

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the MarketingplatformAdminService server but before it is returned to user code.

        We recommend only using this `post_set_property_service_level_with_metadata`
        interceptor in new development instead of the `post_set_property_service_level` interceptor.
        When both interceptors are used, this `post_set_property_service_level_with_metadata` interceptor runs after the
        `post_set_property_service_level` interceptor. The (possibly modified) response returned by
        `post_set_property_service_level` will be passed to
        `post_set_property_service_level_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class MarketingplatformAdminServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MarketingplatformAdminServiceRestInterceptor


class MarketingplatformAdminServiceRestTransport(
    _BaseMarketingplatformAdminServiceRestTransport
):
    """REST backend synchronous transport for MarketingplatformAdminService.

    Service Interface for the Google Marketing Platform Admin
    API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "marketingplatformadmin.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[MarketingplatformAdminServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'marketingplatformadmin.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided. This argument will be
                removed in the next major version of this library.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = (
            interceptor or MarketingplatformAdminServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _CreateAnalyticsAccountLink(
        _BaseMarketingplatformAdminServiceRestTransport._BaseCreateAnalyticsAccountLink,
        MarketingplatformAdminServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MarketingplatformAdminServiceRestTransport.CreateAnalyticsAccountLink"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: marketingplatform_admin.CreateAnalyticsAccountLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.AnalyticsAccountLink:
            r"""Call the create analytics account
            link method over HTTP.

                Args:
                    request (~.marketingplatform_admin.CreateAnalyticsAccountLinkRequest):
                        The request object. Request message for
                    CreateAnalyticsAccountLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.resources.AnalyticsAccountLink:
                        A resource message representing the
                    link between a Google Analytics account
                    and a Google Marketing Platform
                    organization.

            """

            http_options = (
                _BaseMarketingplatformAdminServiceRestTransport._BaseCreateAnalyticsAccountLink._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_analytics_account_link(
                request, metadata
            )
            transcoded_request = _BaseMarketingplatformAdminServiceRestTransport._BaseCreateAnalyticsAccountLink._get_transcoded_request(
                http_options, request
            )

            body = _BaseMarketingplatformAdminServiceRestTransport._BaseCreateAnalyticsAccountLink._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMarketingplatformAdminServiceRestTransport._BaseCreateAnalyticsAccountLink._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.CreateAnalyticsAccountLink",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "CreateAnalyticsAccountLink",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MarketingplatformAdminServiceRestTransport._CreateAnalyticsAccountLink._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.AnalyticsAccountLink()
            pb_resp = resources.AnalyticsAccountLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_analytics_account_link(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            (
                resp,
                _,
            ) = self._interceptor.post_create_analytics_account_link_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.AnalyticsAccountLink.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.create_analytics_account_link",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "CreateAnalyticsAccountLink",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteAnalyticsAccountLink(
        _BaseMarketingplatformAdminServiceRestTransport._BaseDeleteAnalyticsAccountLink,
        MarketingplatformAdminServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MarketingplatformAdminServiceRestTransport.DeleteAnalyticsAccountLink"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: marketingplatform_admin.DeleteAnalyticsAccountLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete analytics account
            link method over HTTP.

                Args:
                    request (~.marketingplatform_admin.DeleteAnalyticsAccountLinkRequest):
                        The request object. Request message for
                    DeleteAnalyticsAccountLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.
            """

            http_options = (
                _BaseMarketingplatformAdminServiceRestTransport._BaseDeleteAnalyticsAccountLink._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_analytics_account_link(
                request, metadata
            )
            transcoded_request = _BaseMarketingplatformAdminServiceRestTransport._BaseDeleteAnalyticsAccountLink._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMarketingplatformAdminServiceRestTransport._BaseDeleteAnalyticsAccountLink._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.DeleteAnalyticsAccountLink",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "DeleteAnalyticsAccountLink",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MarketingplatformAdminServiceRestTransport._DeleteAnalyticsAccountLink._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetOrganization(
        _BaseMarketingplatformAdminServiceRestTransport._BaseGetOrganization,
        MarketingplatformAdminServiceRestStub,
    ):
        def __hash__(self):
            return hash("MarketingplatformAdminServiceRestTransport.GetOrganization")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: marketingplatform_admin.GetOrganizationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resources.Organization:
            r"""Call the get organization method over HTTP.

            Args:
                request (~.marketingplatform_admin.GetOrganizationRequest):
                    The request object. Request message for GetOrganization
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.resources.Organization:
                    A resource message representing a
                Google Marketing Platform organization.

            """

            http_options = (
                _BaseMarketingplatformAdminServiceRestTransport._BaseGetOrganization._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_organization(
                request, metadata
            )
            transcoded_request = _BaseMarketingplatformAdminServiceRestTransport._BaseGetOrganization._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMarketingplatformAdminServiceRestTransport._BaseGetOrganization._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.GetOrganization",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "GetOrganization",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MarketingplatformAdminServiceRestTransport._GetOrganization._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Organization()
            pb_resp = resources.Organization.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_organization(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_organization_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = resources.Organization.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.get_organization",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "GetOrganization",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListAnalyticsAccountLinks(
        _BaseMarketingplatformAdminServiceRestTransport._BaseListAnalyticsAccountLinks,
        MarketingplatformAdminServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MarketingplatformAdminServiceRestTransport.ListAnalyticsAccountLinks"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: marketingplatform_admin.ListAnalyticsAccountLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> marketingplatform_admin.ListAnalyticsAccountLinksResponse:
            r"""Call the list analytics account
            links method over HTTP.

                Args:
                    request (~.marketingplatform_admin.ListAnalyticsAccountLinksRequest):
                        The request object. Request message for
                    ListAnalyticsAccountLinks RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.marketingplatform_admin.ListAnalyticsAccountLinksResponse:
                        Response message for
                    ListAnalyticsAccountLinks RPC.

            """

            http_options = (
                _BaseMarketingplatformAdminServiceRestTransport._BaseListAnalyticsAccountLinks._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_analytics_account_links(
                request, metadata
            )
            transcoded_request = _BaseMarketingplatformAdminServiceRestTransport._BaseListAnalyticsAccountLinks._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseMarketingplatformAdminServiceRestTransport._BaseListAnalyticsAccountLinks._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.ListAnalyticsAccountLinks",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "ListAnalyticsAccountLinks",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MarketingplatformAdminServiceRestTransport._ListAnalyticsAccountLinks._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = marketingplatform_admin.ListAnalyticsAccountLinksResponse()
            pb_resp = marketingplatform_admin.ListAnalyticsAccountLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_analytics_account_links(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_analytics_account_links_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = marketingplatform_admin.ListAnalyticsAccountLinksResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.list_analytics_account_links",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "ListAnalyticsAccountLinks",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SetPropertyServiceLevel(
        _BaseMarketingplatformAdminServiceRestTransport._BaseSetPropertyServiceLevel,
        MarketingplatformAdminServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "MarketingplatformAdminServiceRestTransport.SetPropertyServiceLevel"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: marketingplatform_admin.SetPropertyServiceLevelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> marketingplatform_admin.SetPropertyServiceLevelResponse:
            r"""Call the set property service
            level method over HTTP.

                Args:
                    request (~.marketingplatform_admin.SetPropertyServiceLevelRequest):
                        The request object. Request message for
                    SetPropertyServiceLevel RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.marketingplatform_admin.SetPropertyServiceLevelResponse:
                        Response message for
                    SetPropertyServiceLevel RPC.

            """

            http_options = (
                _BaseMarketingplatformAdminServiceRestTransport._BaseSetPropertyServiceLevel._get_http_options()
            )

            request, metadata = self._interceptor.pre_set_property_service_level(
                request, metadata
            )
            transcoded_request = _BaseMarketingplatformAdminServiceRestTransport._BaseSetPropertyServiceLevel._get_transcoded_request(
                http_options, request
            )

            body = _BaseMarketingplatformAdminServiceRestTransport._BaseSetPropertyServiceLevel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseMarketingplatformAdminServiceRestTransport._BaseSetPropertyServiceLevel._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.SetPropertyServiceLevel",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "SetPropertyServiceLevel",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = MarketingplatformAdminServiceRestTransport._SetPropertyServiceLevel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = marketingplatform_admin.SetPropertyServiceLevelResponse()
            pb_resp = marketingplatform_admin.SetPropertyServiceLevelResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_set_property_service_level(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_set_property_service_level_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        marketingplatform_admin.SetPropertyServiceLevelResponse.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.marketingplatform.admin_v1alpha.MarketingplatformAdminServiceClient.set_property_service_level",
                    extra={
                        "serviceName": "google.marketingplatform.admin.v1alpha.MarketingplatformAdminService",
                        "rpcName": "SetPropertyServiceLevel",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_analytics_account_link(
        self,
    ) -> Callable[
        [marketingplatform_admin.CreateAnalyticsAccountLinkRequest],
        resources.AnalyticsAccountLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAnalyticsAccountLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_analytics_account_link(
        self,
    ) -> Callable[
        [marketingplatform_admin.DeleteAnalyticsAccountLinkRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAnalyticsAccountLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_organization(
        self,
    ) -> Callable[
        [marketingplatform_admin.GetOrganizationRequest], resources.Organization
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrganization(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_analytics_account_links(
        self,
    ) -> Callable[
        [marketingplatform_admin.ListAnalyticsAccountLinksRequest],
        marketingplatform_admin.ListAnalyticsAccountLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAnalyticsAccountLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_property_service_level(
        self,
    ) -> Callable[
        [marketingplatform_admin.SetPropertyServiceLevelRequest],
        marketingplatform_admin.SetPropertyServiceLevelResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetPropertyServiceLevel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("MarketingplatformAdminServiceRestTransport",)
