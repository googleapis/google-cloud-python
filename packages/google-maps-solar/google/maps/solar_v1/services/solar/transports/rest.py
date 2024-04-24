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


from google.api import httpbody_pb2  # type: ignore

from google.maps.solar_v1.types import solar_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import SolarTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SolarRestInterceptor:
    """Interceptor for Solar.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SolarRestTransport.

    .. code-block:: python
        class MyCustomSolarInterceptor(SolarRestInterceptor):
            def pre_find_closest_building_insights(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_find_closest_building_insights(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_layers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_layers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_geo_tiff(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_geo_tiff(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SolarRestTransport(interceptor=MyCustomSolarInterceptor())
        client = SolarClient(transport=transport)


    """

    def pre_find_closest_building_insights(
        self,
        request: solar_service.FindClosestBuildingInsightsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        solar_service.FindClosestBuildingInsightsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for find_closest_building_insights

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Solar server.
        """
        return request, metadata

    def post_find_closest_building_insights(
        self, response: solar_service.BuildingInsights
    ) -> solar_service.BuildingInsights:
        """Post-rpc interceptor for find_closest_building_insights

        Override in a subclass to manipulate the response
        after it is returned by the Solar server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_layers(
        self,
        request: solar_service.GetDataLayersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[solar_service.GetDataLayersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_layers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Solar server.
        """
        return request, metadata

    def post_get_data_layers(
        self, response: solar_service.DataLayers
    ) -> solar_service.DataLayers:
        """Post-rpc interceptor for get_data_layers

        Override in a subclass to manipulate the response
        after it is returned by the Solar server but before
        it is returned to user code.
        """
        return response

    def pre_get_geo_tiff(
        self,
        request: solar_service.GetGeoTiffRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[solar_service.GetGeoTiffRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_geo_tiff

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Solar server.
        """
        return request, metadata

    def post_get_geo_tiff(
        self, response: httpbody_pb2.HttpBody
    ) -> httpbody_pb2.HttpBody:
        """Post-rpc interceptor for get_geo_tiff

        Override in a subclass to manipulate the response
        after it is returned by the Solar server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SolarRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SolarRestInterceptor


class SolarRestTransport(SolarTransport):
    """REST backend transport for Solar.

    Service definition for the Solar API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "solar.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SolarRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'solar.googleapis.com').
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
        self._interceptor = interceptor or SolarRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _FindClosestBuildingInsights(SolarRestStub):
        def __hash__(self):
            return hash("FindClosestBuildingInsights")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "location": {},
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
            request: solar_service.FindClosestBuildingInsightsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> solar_service.BuildingInsights:
            r"""Call the find closest building
            insights method over HTTP.

                Args:
                    request (~.solar_service.FindClosestBuildingInsightsRequest):
                        The request object. Request message for
                    ``Solar.FindClosestBuildingInsights``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.solar_service.BuildingInsights:
                        Response message for
                    ``Solar.FindClosestBuildingInsights``. Information about
                    the location, dimensions, and solar potential of a
                    building.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/buildingInsights:findClosest",
                },
            ]
            request, metadata = self._interceptor.pre_find_closest_building_insights(
                request, metadata
            )
            pb_request = solar_service.FindClosestBuildingInsightsRequest.pb(request)
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
            resp = solar_service.BuildingInsights()
            pb_resp = solar_service.BuildingInsights.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_find_closest_building_insights(resp)
            return resp

    class _GetDataLayers(SolarRestStub):
        def __hash__(self):
            return hash("GetDataLayers")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "location": {},
            "radiusMeters": 0.0,
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
            request: solar_service.GetDataLayersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> solar_service.DataLayers:
            r"""Call the get data layers method over HTTP.

            Args:
                request (~.solar_service.GetDataLayersRequest):
                    The request object. Request message for ``Solar.GetDataLayers``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.solar_service.DataLayers:
                    Information about the solar potential of a region. The
                actual data are contained in a number of GeoTIFF files
                covering the requested region, for which this message
                contains URLs: Each string in the ``DataLayers`` message
                contains a URL from which the corresponding GeoTIFF can
                be fetched. These URLs are valid for a few hours after
                they've been generated. Most of the GeoTIFF files are at
                a resolution of 0.1m/pixel, but the monthly flux file is
                at 0.5m/pixel, and the hourly shade files are at
                1m/pixel. If a ``pixel_size_meters`` value was specified
                in the ``GetDataLayersRequest``, then the minimum
                resolution in the GeoTIFF files will be that value.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/dataLayers:get",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_layers(request, metadata)
            pb_request = solar_service.GetDataLayersRequest.pb(request)
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
            resp = solar_service.DataLayers()
            pb_resp = solar_service.DataLayers.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_layers(resp)
            return resp

    class _GetGeoTiff(SolarRestStub):
        def __hash__(self):
            return hash("GetGeoTiff")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "id": "",
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
            request: solar_service.GetGeoTiffRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> httpbody_pb2.HttpBody:
            r"""Call the get geo tiff method over HTTP.

            Args:
                request (~.solar_service.GetGeoTiffRequest):
                    The request object. Request message for ``Solar.GetGeoTiff``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.httpbody_pb2.HttpBody:
                    Message that represents an arbitrary HTTP body. It
                should only be used for payload formats that can't be
                represented as JSON, such as raw binary or an HTML page.

                This message can be used both in streaming and
                non-streaming API methods in the request as well as the
                response.

                It can be used as a top-level request field, which is
                convenient if one wants to extract parameters from
                either the URL or HTTP template into the request fields
                and also want access to the raw HTTP body.

                Example:

                ::

                    message GetResourceRequest {
                      // A unique request id.
                      string request_id = 1;

                      // The raw HTTP body is bound to this field.
                      google.api.HttpBody http_body = 2;

                    }

                    service ResourceService {
                      rpc GetResource(GetResourceRequest)
                        returns (google.api.HttpBody);
                      rpc UpdateResource(google.api.HttpBody)
                        returns (google.protobuf.Empty);

                    }

                Example with streaming methods:

                ::

                    service CaldavService {
                      rpc GetCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);
                      rpc UpdateCalendar(stream google.api.HttpBody)
                        returns (stream google.api.HttpBody);

                    }

                Use of this type only changes how the request and
                response bodies are handled, all other features will
                continue to work unchanged.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/geoTiff:get",
                },
            ]
            request, metadata = self._interceptor.pre_get_geo_tiff(request, metadata)
            pb_request = solar_service.GetGeoTiffRequest.pb(request)
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
            resp = httpbody_pb2.HttpBody()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_geo_tiff(resp)
            return resp

    @property
    def find_closest_building_insights(
        self,
    ) -> Callable[
        [solar_service.FindClosestBuildingInsightsRequest],
        solar_service.BuildingInsights,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FindClosestBuildingInsights(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_layers(
        self,
    ) -> Callable[[solar_service.GetDataLayersRequest], solar_service.DataLayers]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataLayers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_geo_tiff(
        self,
    ) -> Callable[[solar_service.GetGeoTiffRequest], httpbody_pb2.HttpBody]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGeoTiff(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SolarRestTransport",)
