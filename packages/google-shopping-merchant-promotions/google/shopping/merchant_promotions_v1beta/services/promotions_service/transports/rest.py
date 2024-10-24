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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.shopping.merchant_promotions_v1beta.types import promotions

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BasePromotionsServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class PromotionsServiceRestInterceptor:
    """Interceptor for PromotionsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PromotionsServiceRestTransport.

    .. code-block:: python
        class MyCustomPromotionsServiceInterceptor(PromotionsServiceRestInterceptor):
            def pre_get_promotion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_promotion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert_promotion(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert_promotion(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_promotions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_promotions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PromotionsServiceRestTransport(interceptor=MyCustomPromotionsServiceInterceptor())
        client = PromotionsServiceClient(transport=transport)


    """

    def pre_get_promotion(
        self,
        request: promotions.GetPromotionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[promotions.GetPromotionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_promotion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PromotionsService server.
        """
        return request, metadata

    def post_get_promotion(
        self, response: promotions.Promotion
    ) -> promotions.Promotion:
        """Post-rpc interceptor for get_promotion

        Override in a subclass to manipulate the response
        after it is returned by the PromotionsService server but before
        it is returned to user code.
        """
        return response

    def pre_insert_promotion(
        self,
        request: promotions.InsertPromotionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[promotions.InsertPromotionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for insert_promotion

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PromotionsService server.
        """
        return request, metadata

    def post_insert_promotion(
        self, response: promotions.Promotion
    ) -> promotions.Promotion:
        """Post-rpc interceptor for insert_promotion

        Override in a subclass to manipulate the response
        after it is returned by the PromotionsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_promotions(
        self,
        request: promotions.ListPromotionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[promotions.ListPromotionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_promotions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the PromotionsService server.
        """
        return request, metadata

    def post_list_promotions(
        self, response: promotions.ListPromotionsResponse
    ) -> promotions.ListPromotionsResponse:
        """Post-rpc interceptor for list_promotions

        Override in a subclass to manipulate the response
        after it is returned by the PromotionsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PromotionsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PromotionsServiceRestInterceptor


class PromotionsServiceRestTransport(_BasePromotionsServiceRestTransport):
    """REST backend synchronous transport for PromotionsService.

    Service to manage promotions for products.

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
        interceptor: Optional[PromotionsServiceRestInterceptor] = None,
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
        self._interceptor = interceptor or PromotionsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetPromotion(
        _BasePromotionsServiceRestTransport._BaseGetPromotion, PromotionsServiceRestStub
    ):
        def __hash__(self):
            return hash("PromotionsServiceRestTransport.GetPromotion")

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
            request: promotions.GetPromotionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> promotions.Promotion:
            r"""Call the get promotion method over HTTP.

            Args:
                request (~.promotions.GetPromotionRequest):
                    The request object. Request message for the ``GetPromotion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.promotions.Promotion:
                    Represents a promotion. See the following articles for
                more details.

                Required promotion input attributes to pass data
                validation checks are primarily defined below:

                -  `Promotions data
                   specification <https://support.google.com/merchants/answer/2906014>`__
                -  `Local promotions data
                   specification <https://support.google.com/merchants/answer/10146130>`__

                After inserting, updating a promotion input, it may take
                several minutes before the final promotion can be
                retrieved.

            """

            http_options = (
                _BasePromotionsServiceRestTransport._BaseGetPromotion._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_promotion(request, metadata)
            transcoded_request = _BasePromotionsServiceRestTransport._BaseGetPromotion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePromotionsServiceRestTransport._BaseGetPromotion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PromotionsServiceRestTransport._GetPromotion._get_response(
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
            resp = promotions.Promotion()
            pb_resp = promotions.Promotion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_promotion(resp)
            return resp

    class _InsertPromotion(
        _BasePromotionsServiceRestTransport._BaseInsertPromotion,
        PromotionsServiceRestStub,
    ):
        def __hash__(self):
            return hash("PromotionsServiceRestTransport.InsertPromotion")

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
            request: promotions.InsertPromotionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> promotions.Promotion:
            r"""Call the insert promotion method over HTTP.

            Args:
                request (~.promotions.InsertPromotionRequest):
                    The request object. Request message for the ``InsertPromotion`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.promotions.Promotion:
                    Represents a promotion. See the following articles for
                more details.

                Required promotion input attributes to pass data
                validation checks are primarily defined below:

                -  `Promotions data
                   specification <https://support.google.com/merchants/answer/2906014>`__
                -  `Local promotions data
                   specification <https://support.google.com/merchants/answer/10146130>`__

                After inserting, updating a promotion input, it may take
                several minutes before the final promotion can be
                retrieved.

            """

            http_options = (
                _BasePromotionsServiceRestTransport._BaseInsertPromotion._get_http_options()
            )
            request, metadata = self._interceptor.pre_insert_promotion(
                request, metadata
            )
            transcoded_request = _BasePromotionsServiceRestTransport._BaseInsertPromotion._get_transcoded_request(
                http_options, request
            )

            body = _BasePromotionsServiceRestTransport._BaseInsertPromotion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BasePromotionsServiceRestTransport._BaseInsertPromotion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PromotionsServiceRestTransport._InsertPromotion._get_response(
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
            resp = promotions.Promotion()
            pb_resp = promotions.Promotion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_insert_promotion(resp)
            return resp

    class _ListPromotions(
        _BasePromotionsServiceRestTransport._BaseListPromotions,
        PromotionsServiceRestStub,
    ):
        def __hash__(self):
            return hash("PromotionsServiceRestTransport.ListPromotions")

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
            request: promotions.ListPromotionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> promotions.ListPromotionsResponse:
            r"""Call the list promotions method over HTTP.

            Args:
                request (~.promotions.ListPromotionsRequest):
                    The request object. Request message for the ``ListPromotions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.promotions.ListPromotionsResponse:
                    Response message for the ``ListPromotions`` method.
            """

            http_options = (
                _BasePromotionsServiceRestTransport._BaseListPromotions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_promotions(request, metadata)
            transcoded_request = _BasePromotionsServiceRestTransport._BaseListPromotions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BasePromotionsServiceRestTransport._BaseListPromotions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = PromotionsServiceRestTransport._ListPromotions._get_response(
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
            resp = promotions.ListPromotionsResponse()
            pb_resp = promotions.ListPromotionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_promotions(resp)
            return resp

    @property
    def get_promotion(
        self,
    ) -> Callable[[promotions.GetPromotionRequest], promotions.Promotion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPromotion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert_promotion(
        self,
    ) -> Callable[[promotions.InsertPromotionRequest], promotions.Promotion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._InsertPromotion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_promotions(
        self,
    ) -> Callable[
        [promotions.ListPromotionsRequest], promotions.ListPromotionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPromotions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("PromotionsServiceRestTransport",)
