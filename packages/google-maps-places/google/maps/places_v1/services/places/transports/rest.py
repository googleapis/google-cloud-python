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


from google.maps.places_v1.types import place, places_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import PlacesTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class PlacesRestInterceptor:
    """Interceptor for Places.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the PlacesRestTransport.

    .. code-block:: python
        class MyCustomPlacesInterceptor(PlacesRestInterceptor):
            def pre_autocomplete_places(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_autocomplete_places(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_photo_media(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_photo_media(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_place(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_place(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_nearby(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_nearby(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_text(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_text(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = PlacesRestTransport(interceptor=MyCustomPlacesInterceptor())
        client = PlacesClient(transport=transport)


    """

    def pre_autocomplete_places(
        self,
        request: places_service.AutocompletePlacesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[places_service.AutocompletePlacesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for autocomplete_places

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Places server.
        """
        return request, metadata

    def post_autocomplete_places(
        self, response: places_service.AutocompletePlacesResponse
    ) -> places_service.AutocompletePlacesResponse:
        """Post-rpc interceptor for autocomplete_places

        Override in a subclass to manipulate the response
        after it is returned by the Places server but before
        it is returned to user code.
        """
        return response

    def pre_get_photo_media(
        self,
        request: places_service.GetPhotoMediaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[places_service.GetPhotoMediaRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_photo_media

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Places server.
        """
        return request, metadata

    def post_get_photo_media(
        self, response: places_service.PhotoMedia
    ) -> places_service.PhotoMedia:
        """Post-rpc interceptor for get_photo_media

        Override in a subclass to manipulate the response
        after it is returned by the Places server but before
        it is returned to user code.
        """
        return response

    def pre_get_place(
        self,
        request: places_service.GetPlaceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[places_service.GetPlaceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_place

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Places server.
        """
        return request, metadata

    def post_get_place(self, response: place.Place) -> place.Place:
        """Post-rpc interceptor for get_place

        Override in a subclass to manipulate the response
        after it is returned by the Places server but before
        it is returned to user code.
        """
        return response

    def pre_search_nearby(
        self,
        request: places_service.SearchNearbyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[places_service.SearchNearbyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_nearby

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Places server.
        """
        return request, metadata

    def post_search_nearby(
        self, response: places_service.SearchNearbyResponse
    ) -> places_service.SearchNearbyResponse:
        """Post-rpc interceptor for search_nearby

        Override in a subclass to manipulate the response
        after it is returned by the Places server but before
        it is returned to user code.
        """
        return response

    def pre_search_text(
        self,
        request: places_service.SearchTextRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[places_service.SearchTextRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_text

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Places server.
        """
        return request, metadata

    def post_search_text(
        self, response: places_service.SearchTextResponse
    ) -> places_service.SearchTextResponse:
        """Post-rpc interceptor for search_text

        Override in a subclass to manipulate the response
        after it is returned by the Places server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class PlacesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: PlacesRestInterceptor


class PlacesRestTransport(PlacesTransport):
    """REST backend transport for Places.

    Service definition for the Places API. Note: every request (except
    for Autocomplete requests) requires a field mask set outside of the
    request proto (``all/*``, is not assumed). The field mask can be set
    via the HTTP header ``X-Goog-FieldMask``. See:
    https://developers.google.com/maps/documentation/places/web-service/choose-fields

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "places.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[PlacesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'places.googleapis.com').
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
        self._interceptor = interceptor or PlacesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AutocompletePlaces(PlacesRestStub):
        def __hash__(self):
            return hash("AutocompletePlaces")

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
            request: places_service.AutocompletePlacesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> places_service.AutocompletePlacesResponse:
            r"""Call the autocomplete places method over HTTP.

            Args:
                request (~.places_service.AutocompletePlacesRequest):
                    The request object. Request proto for AutocompletePlaces.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.places_service.AutocompletePlacesResponse:
                    Response proto for
                AutocompletePlaces.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/places:autocomplete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_autocomplete_places(
                request, metadata
            )
            pb_request = places_service.AutocompletePlacesRequest.pb(request)
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
            resp = places_service.AutocompletePlacesResponse()
            pb_resp = places_service.AutocompletePlacesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_autocomplete_places(resp)
            return resp

    class _GetPhotoMedia(PlacesRestStub):
        def __hash__(self):
            return hash("GetPhotoMedia")

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
            request: places_service.GetPhotoMediaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> places_service.PhotoMedia:
            r"""Call the get photo media method over HTTP.

            Args:
                request (~.places_service.GetPhotoMediaRequest):
                    The request object. Request for fetching a photo of a
                place using a photo resource name.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.places_service.PhotoMedia:
                    A photo media from Places API.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=places/*/photos/*/media}",
                },
            ]
            request, metadata = self._interceptor.pre_get_photo_media(request, metadata)
            pb_request = places_service.GetPhotoMediaRequest.pb(request)
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
            resp = places_service.PhotoMedia()
            pb_resp = places_service.PhotoMedia.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_photo_media(resp)
            return resp

    class _GetPlace(PlacesRestStub):
        def __hash__(self):
            return hash("GetPlace")

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
            request: places_service.GetPlaceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> place.Place:
            r"""Call the get place method over HTTP.

            Args:
                request (~.places_service.GetPlaceRequest):
                    The request object. Request for fetching a Place based on its resource name,
                which is a string in the ``places/{place_id}`` format.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.place.Place:
                    All the information representing a
                Place.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=places/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_place(request, metadata)
            pb_request = places_service.GetPlaceRequest.pb(request)
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
            resp = place.Place()
            pb_resp = place.Place.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_place(resp)
            return resp

    class _SearchNearby(PlacesRestStub):
        def __hash__(self):
            return hash("SearchNearby")

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
            request: places_service.SearchNearbyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> places_service.SearchNearbyResponse:
            r"""Call the search nearby method over HTTP.

            Args:
                request (~.places_service.SearchNearbyRequest):
                    The request object. Request proto for Search Nearby.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.places_service.SearchNearbyResponse:
                    Response proto for Search Nearby.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/places:searchNearby",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_nearby(request, metadata)
            pb_request = places_service.SearchNearbyRequest.pb(request)
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
            resp = places_service.SearchNearbyResponse()
            pb_resp = places_service.SearchNearbyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_nearby(resp)
            return resp

    class _SearchText(PlacesRestStub):
        def __hash__(self):
            return hash("SearchText")

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
            request: places_service.SearchTextRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> places_service.SearchTextResponse:
            r"""Call the search text method over HTTP.

            Args:
                request (~.places_service.SearchTextRequest):
                    The request object. Request proto for SearchText.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.places_service.SearchTextResponse:
                    Response proto for SearchText.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/places:searchText",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_text(request, metadata)
            pb_request = places_service.SearchTextRequest.pb(request)
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
            resp = places_service.SearchTextResponse()
            pb_resp = places_service.SearchTextResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_text(resp)
            return resp

    @property
    def autocomplete_places(
        self,
    ) -> Callable[
        [places_service.AutocompletePlacesRequest],
        places_service.AutocompletePlacesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AutocompletePlaces(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_photo_media(
        self,
    ) -> Callable[[places_service.GetPhotoMediaRequest], places_service.PhotoMedia]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPhotoMedia(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_place(self) -> Callable[[places_service.GetPlaceRequest], place.Place]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPlace(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_nearby(
        self,
    ) -> Callable[
        [places_service.SearchNearbyRequest], places_service.SearchNearbyResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchNearby(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_text(
        self,
    ) -> Callable[
        [places_service.SearchTextRequest], places_service.SearchTextResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchText(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("PlacesRestTransport",)
