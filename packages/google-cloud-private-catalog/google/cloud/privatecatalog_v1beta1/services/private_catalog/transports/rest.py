# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.privatecatalog_v1beta1.types import private_catalog

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import PrivateCatalogTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class PrivateCatalogRestInterceptor:
    """Interceptor for PrivateCatalog.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PrivateCatalogRestTransport.

    .. code-block:: python
        class MyCustomPrivateCatalogInterceptor(PrivateCatalogRestInterceptor):
            def pre_search_catalogs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_catalogs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_products(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_products(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PrivateCatalogRestTransport(interceptor=MyCustomPrivateCatalogInterceptor())
        client = PrivateCatalogClient(transport=transport)


    """

    def pre_search_catalogs(
        self,
        request: private_catalog.SearchCatalogsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[private_catalog.SearchCatalogsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_catalogs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivateCatalog server.
        """
        return request, metadata

    def post_search_catalogs(
        self, response: private_catalog.SearchCatalogsResponse
    ) -> private_catalog.SearchCatalogsResponse:
        """Post-rpc interceptor for search_catalogs

        Override in a subclass to manipulate the response
        after it is returned by the PrivateCatalog server but before
        it is returned to user code.
        """
        return response

    def pre_search_products(
        self,
        request: private_catalog.SearchProductsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[private_catalog.SearchProductsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_products

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivateCatalog server.
        """
        return request, metadata

    def post_search_products(
        self, response: private_catalog.SearchProductsResponse
    ) -> private_catalog.SearchProductsResponse:
        """Post-rpc interceptor for search_products

        Override in a subclass to manipulate the response
        after it is returned by the PrivateCatalog server but before
        it is returned to user code.
        """
        return response

    def pre_search_versions(
        self,
        request: private_catalog.SearchVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[private_catalog.SearchVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PrivateCatalog server.
        """
        return request, metadata

    def post_search_versions(
        self, response: private_catalog.SearchVersionsResponse
    ) -> private_catalog.SearchVersionsResponse:
        """Post-rpc interceptor for search_versions

        Override in a subclass to manipulate the response
        after it is returned by the PrivateCatalog server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PrivateCatalogRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PrivateCatalogRestInterceptor


class PrivateCatalogRestTransport(PrivateCatalogTransport):
    """REST backend transport for PrivateCatalog.

    ``PrivateCatalog`` allows catalog consumers to retrieve ``Catalog``,
    ``Product`` and ``Version`` resources under a target resource
    context.

    ``Catalog`` is computed based on the [Association][]s linked to the
    target resource and its ancestors. Each association's
    [google.cloud.privatecatalogproducer.v1beta.Catalog][] is
    transformed into a ``Catalog``. If multiple associations have the
    same parent [google.cloud.privatecatalogproducer.v1beta.Catalog][],
    they are de-duplicated into one ``Catalog``. Users must have
    ``cloudprivatecatalog.catalogTargets.get`` IAM permission on the
    resource context in order to access catalogs. ``Catalog`` contains
    the resource name and a subset of data of the original
    [google.cloud.privatecatalogproducer.v1beta.Catalog][].

    ``Product`` is child resource of the catalog. A ``Product`` contains
    the resource name and a subset of the data of the original
    [google.cloud.privatecatalogproducer.v1beta.Product][].

    ``Version`` is child resource of the product. A ``Version`` contains
    the resource name and a subset of the data of the original
    [google.cloud.privatecatalogproducer.v1beta.Version][].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudprivatecatalog.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[PrivateCatalogRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudprivatecatalog.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or PrivateCatalogRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _SearchCatalogs(PrivateCatalogRestStub):
        def __hash__(self):
            return hash("SearchCatalogs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: private_catalog.SearchCatalogsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> private_catalog.SearchCatalogsResponse:
            r"""Call the search catalogs method over HTTP.

            Args:
                request (~.private_catalog.SearchCatalogsRequest):
                    The request object. Request message for
                [PrivateCatalog.SearchCatalogs][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchCatalogs].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.private_catalog.SearchCatalogsResponse:
                    Response message for
                [PrivateCatalog.SearchCatalogs][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchCatalogs].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=projects/*}/catalogs:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=organizations/*}/catalogs:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=folders/*}/catalogs:search",
                },
            ]
            request, metadata = self._interceptor.pre_search_catalogs(request, metadata)
            pb_request = private_catalog.SearchCatalogsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = private_catalog.SearchCatalogsResponse()
            pb_resp = private_catalog.SearchCatalogsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_catalogs(resp)
            return resp

    class _SearchProducts(PrivateCatalogRestStub):
        def __hash__(self):
            return hash("SearchProducts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: private_catalog.SearchProductsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> private_catalog.SearchProductsResponse:
            r"""Call the search products method over HTTP.

            Args:
                request (~.private_catalog.SearchProductsRequest):
                    The request object. Request message for
                [PrivateCatalog.SearchProducts][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchProducts].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.private_catalog.SearchProductsResponse:
                    Response message for
                [PrivateCatalog.SearchProducts][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchProducts].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=projects/*}/products:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=organizations/*}/products:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=folders/*}/products:search",
                },
            ]
            request, metadata = self._interceptor.pre_search_products(request, metadata)
            pb_request = private_catalog.SearchProductsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = private_catalog.SearchProductsResponse()
            pb_resp = private_catalog.SearchProductsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_products(resp)
            return resp

    class _SearchVersions(PrivateCatalogRestStub):
        def __hash__(self):
            return hash("SearchVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "query": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: private_catalog.SearchVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> private_catalog.SearchVersionsResponse:
            r"""Call the search versions method over HTTP.

            Args:
                request (~.private_catalog.SearchVersionsRequest):
                    The request object. Request message for
                [PrivateCatalog.SearchVersions][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.private_catalog.SearchVersionsResponse:
                    Response message for
                [PrivateCatalog.SearchVersions][google.cloud.privatecatalog.v1beta1.PrivateCatalog.SearchVersions].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=projects/*}/versions:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=organizations/*}/versions:search",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{resource=folders/*}/versions:search",
                },
            ]
            request, metadata = self._interceptor.pre_search_versions(request, metadata)
            pb_request = private_catalog.SearchVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = private_catalog.SearchVersionsResponse()
            pb_resp = private_catalog.SearchVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_versions(resp)
            return resp

    @property
    def search_catalogs(
        self,
    ) -> Callable[
        [private_catalog.SearchCatalogsRequest], private_catalog.SearchCatalogsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchCatalogs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_products(
        self,
    ) -> Callable[
        [private_catalog.SearchProductsRequest], private_catalog.SearchProductsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchProducts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_versions(
        self,
    ) -> Callable[
        [private_catalog.SearchVersionsRequest], private_catalog.SearchVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("PrivateCatalogRestTransport",)
