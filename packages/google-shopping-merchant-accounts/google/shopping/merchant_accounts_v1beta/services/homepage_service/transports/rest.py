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


from google.shopping.merchant_accounts_v1beta.types import homepage as gsma_homepage
from google.shopping.merchant_accounts_v1beta.types import homepage

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import HomepageServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class HomepageServiceRestInterceptor:
    """Interceptor for HomepageService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the HomepageServiceRestTransport.

    .. code-block:: python
        class MyCustomHomepageServiceInterceptor(HomepageServiceRestInterceptor):
            def pre_claim_homepage(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_claim_homepage(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_homepage(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_homepage(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_unclaim_homepage(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_unclaim_homepage(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_homepage(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_homepage(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = HomepageServiceRestTransport(interceptor=MyCustomHomepageServiceInterceptor())
        client = HomepageServiceClient(transport=transport)


    """

    def pre_claim_homepage(
        self,
        request: homepage.ClaimHomepageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[homepage.ClaimHomepageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for claim_homepage

        Override in a subclass to manipulate the request or metadata
        before they are sent to the HomepageService server.
        """
        return request, metadata

    def post_claim_homepage(self, response: homepage.Homepage) -> homepage.Homepage:
        """Post-rpc interceptor for claim_homepage

        Override in a subclass to manipulate the response
        after it is returned by the HomepageService server but before
        it is returned to user code.
        """
        return response

    def pre_get_homepage(
        self, request: homepage.GetHomepageRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[homepage.GetHomepageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_homepage

        Override in a subclass to manipulate the request or metadata
        before they are sent to the HomepageService server.
        """
        return request, metadata

    def post_get_homepage(self, response: homepage.Homepage) -> homepage.Homepage:
        """Post-rpc interceptor for get_homepage

        Override in a subclass to manipulate the response
        after it is returned by the HomepageService server but before
        it is returned to user code.
        """
        return response

    def pre_unclaim_homepage(
        self,
        request: homepage.UnclaimHomepageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[homepage.UnclaimHomepageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for unclaim_homepage

        Override in a subclass to manipulate the request or metadata
        before they are sent to the HomepageService server.
        """
        return request, metadata

    def post_unclaim_homepage(self, response: homepage.Homepage) -> homepage.Homepage:
        """Post-rpc interceptor for unclaim_homepage

        Override in a subclass to manipulate the response
        after it is returned by the HomepageService server but before
        it is returned to user code.
        """
        return response

    def pre_update_homepage(
        self,
        request: gsma_homepage.UpdateHomepageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gsma_homepage.UpdateHomepageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_homepage

        Override in a subclass to manipulate the request or metadata
        before they are sent to the HomepageService server.
        """
        return request, metadata

    def post_update_homepage(
        self, response: gsma_homepage.Homepage
    ) -> gsma_homepage.Homepage:
        """Post-rpc interceptor for update_homepage

        Override in a subclass to manipulate the response
        after it is returned by the HomepageService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class HomepageServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: HomepageServiceRestInterceptor


class HomepageServiceRestTransport(HomepageServiceTransport):
    """REST backend transport for HomepageService.

    Service to support an API for a store's homepage.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "merchantapi.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[HomepageServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'merchantapi.googleapis.com').
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
        self._interceptor = interceptor or HomepageServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _ClaimHomepage(HomepageServiceRestStub):
        def __hash__(self):
            return hash("ClaimHomepage")

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
            request: homepage.ClaimHomepageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> homepage.Homepage:
            r"""Call the claim homepage method over HTTP.

            Args:
                request (~.homepage.ClaimHomepageRequest):
                    The request object. Request message for the ``ClaimHomepage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.homepage.Homepage:
                    A store's homepage.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/accounts/v1beta/{name=accounts/*/homepage}:claim",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_claim_homepage(request, metadata)
            pb_request = homepage.ClaimHomepageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = homepage.Homepage()
            pb_resp = homepage.Homepage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_claim_homepage(resp)
            return resp

    class _GetHomepage(HomepageServiceRestStub):
        def __hash__(self):
            return hash("GetHomepage")

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
            request: homepage.GetHomepageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> homepage.Homepage:
            r"""Call the get homepage method over HTTP.

            Args:
                request (~.homepage.GetHomepageRequest):
                    The request object. Request message for the ``GetHomepage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.homepage.Homepage:
                    A store's homepage.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/accounts/v1beta/{name=accounts/*/homepage}",
                },
            ]
            request, metadata = self._interceptor.pre_get_homepage(request, metadata)
            pb_request = homepage.GetHomepageRequest.pb(request)
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
            resp = homepage.Homepage()
            pb_resp = homepage.Homepage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_homepage(resp)
            return resp

    class _UnclaimHomepage(HomepageServiceRestStub):
        def __hash__(self):
            return hash("UnclaimHomepage")

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
            request: homepage.UnclaimHomepageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> homepage.Homepage:
            r"""Call the unclaim homepage method over HTTP.

            Args:
                request (~.homepage.UnclaimHomepageRequest):
                    The request object. Request message for the ``UnclaimHomepage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.homepage.Homepage:
                    A store's homepage.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/accounts/v1beta/{name=accounts/*/homepage}:unclaim",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_unclaim_homepage(
                request, metadata
            )
            pb_request = homepage.UnclaimHomepageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = homepage.Homepage()
            pb_resp = homepage.Homepage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_unclaim_homepage(resp)
            return resp

    class _UpdateHomepage(HomepageServiceRestStub):
        def __hash__(self):
            return hash("UpdateHomepage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: gsma_homepage.UpdateHomepageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gsma_homepage.Homepage:
            r"""Call the update homepage method over HTTP.

            Args:
                request (~.gsma_homepage.UpdateHomepageRequest):
                    The request object. Request message for the ``UpdateHomepage`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gsma_homepage.Homepage:
                    A store's homepage.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/accounts/v1beta/{homepage.name=accounts/*/homepage}",
                    "body": "homepage",
                },
            ]
            request, metadata = self._interceptor.pre_update_homepage(request, metadata)
            pb_request = gsma_homepage.UpdateHomepageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gsma_homepage.Homepage()
            pb_resp = gsma_homepage.Homepage.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_homepage(resp)
            return resp

    @property
    def claim_homepage(
        self,
    ) -> Callable[[homepage.ClaimHomepageRequest], homepage.Homepage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ClaimHomepage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_homepage(
        self,
    ) -> Callable[[homepage.GetHomepageRequest], homepage.Homepage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetHomepage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def unclaim_homepage(
        self,
    ) -> Callable[[homepage.UnclaimHomepageRequest], homepage.Homepage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UnclaimHomepage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_homepage(
        self,
    ) -> Callable[[gsma_homepage.UpdateHomepageRequest], gsma_homepage.Homepage]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateHomepage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("HomepageServiceRestTransport",)
