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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.errorreporting_v1beta1.types import error_stats_service

from .base import (
    ErrorStatsServiceTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ErrorStatsServiceRestInterceptor:
    """Interceptor for ErrorStatsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ErrorStatsServiceRestTransport.

    .. code-block:: python
        class MyCustomErrorStatsServiceInterceptor(ErrorStatsServiceRestInterceptor):
            def pre_delete_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_group_stats(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_group_stats(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ErrorStatsServiceRestTransport(interceptor=MyCustomErrorStatsServiceInterceptor())
        client = ErrorStatsServiceClient(transport=transport)


    """

    def pre_delete_events(
        self,
        request: error_stats_service.DeleteEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[error_stats_service.DeleteEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ErrorStatsService server.
        """
        return request, metadata

    def post_delete_events(
        self, response: error_stats_service.DeleteEventsResponse
    ) -> error_stats_service.DeleteEventsResponse:
        """Post-rpc interceptor for delete_events

        Override in a subclass to manipulate the response
        after it is returned by the ErrorStatsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_events(
        self,
        request: error_stats_service.ListEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[error_stats_service.ListEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ErrorStatsService server.
        """
        return request, metadata

    def post_list_events(
        self, response: error_stats_service.ListEventsResponse
    ) -> error_stats_service.ListEventsResponse:
        """Post-rpc interceptor for list_events

        Override in a subclass to manipulate the response
        after it is returned by the ErrorStatsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_group_stats(
        self,
        request: error_stats_service.ListGroupStatsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[error_stats_service.ListGroupStatsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_group_stats

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ErrorStatsService server.
        """
        return request, metadata

    def post_list_group_stats(
        self, response: error_stats_service.ListGroupStatsResponse
    ) -> error_stats_service.ListGroupStatsResponse:
        """Post-rpc interceptor for list_group_stats

        Override in a subclass to manipulate the response
        after it is returned by the ErrorStatsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ErrorStatsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ErrorStatsServiceRestInterceptor


class ErrorStatsServiceRestTransport(ErrorStatsServiceTransport):
    """REST backend transport for ErrorStatsService.

    An API for retrieving and managing error statistics as well
    as data for individual events.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "clouderrorreporting.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ErrorStatsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'clouderrorreporting.googleapis.com').
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
        self._interceptor = interceptor or ErrorStatsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _DeleteEvents(ErrorStatsServiceRestStub):
        def __hash__(self):
            return hash("DeleteEvents")

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
            request: error_stats_service.DeleteEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> error_stats_service.DeleteEventsResponse:
            r"""Call the delete events method over HTTP.

            Args:
                request (~.error_stats_service.DeleteEventsRequest):
                    The request object. Deletes all events in the project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.error_stats_service.DeleteEventsResponse:
                    Response message for deleting error
                events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta1/{project_name=projects/*}/events",
                },
                {
                    "method": "delete",
                    "uri": "/v1beta1/{project_name=projects/*/locations/*}/events",
                },
            ]
            request, metadata = self._interceptor.pre_delete_events(request, metadata)
            pb_request = error_stats_service.DeleteEventsRequest.pb(request)
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
            resp = error_stats_service.DeleteEventsResponse()
            pb_resp = error_stats_service.DeleteEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_events(resp)
            return resp

    class _ListEvents(ErrorStatsServiceRestStub):
        def __hash__(self):
            return hash("ListEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "groupId": "",
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
            request: error_stats_service.ListEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> error_stats_service.ListEventsResponse:
            r"""Call the list events method over HTTP.

            Args:
                request (~.error_stats_service.ListEventsRequest):
                    The request object. Specifies a set of error events to
                return.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.error_stats_service.ListEventsResponse:
                    Contains a set of requested error
                events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{project_name=projects/*}/events",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{project_name=projects/*/locations/*}/events",
                },
            ]
            request, metadata = self._interceptor.pre_list_events(request, metadata)
            pb_request = error_stats_service.ListEventsRequest.pb(request)
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
            resp = error_stats_service.ListEventsResponse()
            pb_resp = error_stats_service.ListEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_events(resp)
            return resp

    class _ListGroupStats(ErrorStatsServiceRestStub):
        def __hash__(self):
            return hash("ListGroupStats")

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
            request: error_stats_service.ListGroupStatsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> error_stats_service.ListGroupStatsResponse:
            r"""Call the list group stats method over HTTP.

            Args:
                request (~.error_stats_service.ListGroupStatsRequest):
                    The request object. Specifies a set of ``ErrorGroupStats`` to return.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.error_stats_service.ListGroupStatsResponse:
                    Contains a set of requested error
                group stats.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta1/{project_name=projects/*}/groupStats",
                },
                {
                    "method": "get",
                    "uri": "/v1beta1/{project_name=projects/*/locations/*}/groupStats",
                },
            ]
            request, metadata = self._interceptor.pre_list_group_stats(
                request, metadata
            )
            pb_request = error_stats_service.ListGroupStatsRequest.pb(request)
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
            resp = error_stats_service.ListGroupStatsResponse()
            pb_resp = error_stats_service.ListGroupStatsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_group_stats(resp)
            return resp

    @property
    def delete_events(
        self,
    ) -> Callable[
        [error_stats_service.DeleteEventsRequest],
        error_stats_service.DeleteEventsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_events(
        self,
    ) -> Callable[
        [error_stats_service.ListEventsRequest], error_stats_service.ListEventsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_group_stats(
        self,
    ) -> Callable[
        [error_stats_service.ListGroupStatsRequest],
        error_stats_service.ListGroupStatsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGroupStats(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ErrorStatsServiceRestTransport",)
