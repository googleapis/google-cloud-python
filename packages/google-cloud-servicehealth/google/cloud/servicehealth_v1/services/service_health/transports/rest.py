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
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.servicehealth_v1.types import event_resources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import ServiceHealthTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ServiceHealthRestInterceptor:
    """Interceptor for ServiceHealth.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ServiceHealthRestTransport.

    .. code-block:: python
        class MyCustomServiceHealthInterceptor(ServiceHealthRestInterceptor):
            def pre_get_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_organization_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_organization_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_organization_impact(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_organization_impact(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_organization_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_organization_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_organization_impacts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_organization_impacts(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ServiceHealthRestTransport(interceptor=MyCustomServiceHealthInterceptor())
        client = ServiceHealthClient(transport=transport)


    """

    def pre_get_event(
        self,
        request: event_resources.GetEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[event_resources.GetEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_get_event(self, response: event_resources.Event) -> event_resources.Event:
        """Post-rpc interceptor for get_event

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_get_organization_event(
        self,
        request: event_resources.GetOrganizationEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[event_resources.GetOrganizationEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_organization_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_get_organization_event(
        self, response: event_resources.OrganizationEvent
    ) -> event_resources.OrganizationEvent:
        """Post-rpc interceptor for get_organization_event

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_get_organization_impact(
        self,
        request: event_resources.GetOrganizationImpactRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[event_resources.GetOrganizationImpactRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_organization_impact

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_get_organization_impact(
        self, response: event_resources.OrganizationImpact
    ) -> event_resources.OrganizationImpact:
        """Post-rpc interceptor for get_organization_impact

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_list_events(
        self,
        request: event_resources.ListEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[event_resources.ListEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_list_events(
        self, response: event_resources.ListEventsResponse
    ) -> event_resources.ListEventsResponse:
        """Post-rpc interceptor for list_events

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_list_organization_events(
        self,
        request: event_resources.ListOrganizationEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        event_resources.ListOrganizationEventsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_organization_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_list_organization_events(
        self, response: event_resources.ListOrganizationEventsResponse
    ) -> event_resources.ListOrganizationEventsResponse:
        """Post-rpc interceptor for list_organization_events

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_list_organization_impacts(
        self,
        request: event_resources.ListOrganizationImpactsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        event_resources.ListOrganizationImpactsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_organization_impacts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_list_organization_impacts(
        self, response: event_resources.ListOrganizationImpactsResponse
    ) -> event_resources.ListOrganizationImpactsResponse:
        """Post-rpc interceptor for list_organization_impacts

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ServiceHealth server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ServiceHealth server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ServiceHealthRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ServiceHealthRestInterceptor


class ServiceHealthRestTransport(ServiceHealthTransport):
    """REST backend transport for ServiceHealth.

    Request service health events relevant to your Google Cloud
    project.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "servicehealth.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ServiceHealthRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'servicehealth.googleapis.com').
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
        self._interceptor = interceptor or ServiceHealthRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetEvent(ServiceHealthRestStub):
        def __hash__(self):
            return hash("GetEvent")

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
            request: event_resources.GetEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.Event:
            r"""Call the get event method over HTTP.

            Args:
                request (~.event_resources.GetEventRequest):
                    The request object. Message for getting an event
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.Event:
                    Represents service health events that
                may affect Google Cloud products. Event
                resource is a read-only view and does
                not allow any modifications. All fields
                are output only.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/events/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_event(request, metadata)
            pb_request = event_resources.GetEventRequest.pb(request)
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
            resp = event_resources.Event()
            pb_resp = event_resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event(resp)
            return resp

    class _GetOrganizationEvent(ServiceHealthRestStub):
        def __hash__(self):
            return hash("GetOrganizationEvent")

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
            request: event_resources.GetOrganizationEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.OrganizationEvent:
            r"""Call the get organization event method over HTTP.

            Args:
                request (~.event_resources.GetOrganizationEventRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.OrganizationEvent:
                    Represents service health events that
                may affect Google Cloud products used
                across the organization. It is a
                read-only view and does not allow any
                modifications.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/organizationEvents/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_organization_event(
                request, metadata
            )
            pb_request = event_resources.GetOrganizationEventRequest.pb(request)
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
            resp = event_resources.OrganizationEvent()
            pb_resp = event_resources.OrganizationEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_organization_event(resp)
            return resp

    class _GetOrganizationImpact(ServiceHealthRestStub):
        def __hash__(self):
            return hash("GetOrganizationImpact")

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
            request: event_resources.GetOrganizationImpactRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.OrganizationImpact:
            r"""Call the get organization impact method over HTTP.

            Args:
                request (~.event_resources.GetOrganizationImpactRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.OrganizationImpact:
                    Represents impact to assets at
                organizational level. It is a read-only
                view and does not allow any
                modifications.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/organizationImpacts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_organization_impact(
                request, metadata
            )
            pb_request = event_resources.GetOrganizationImpactRequest.pb(request)
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
            resp = event_resources.OrganizationImpact()
            pb_resp = event_resources.OrganizationImpact.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_organization_impact(resp)
            return resp

    class _ListEvents(ServiceHealthRestStub):
        def __hash__(self):
            return hash("ListEvents")

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
            request: event_resources.ListEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.ListEventsResponse:
            r"""Call the list events method over HTTP.

            Args:
                request (~.event_resources.ListEventsRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.ListEventsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/events",
                },
            ]
            request, metadata = self._interceptor.pre_list_events(request, metadata)
            pb_request = event_resources.ListEventsRequest.pb(request)
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
            resp = event_resources.ListEventsResponse()
            pb_resp = event_resources.ListEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_events(resp)
            return resp

    class _ListOrganizationEvents(ServiceHealthRestStub):
        def __hash__(self):
            return hash("ListOrganizationEvents")

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
            request: event_resources.ListOrganizationEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.ListOrganizationEventsResponse:
            r"""Call the list organization events method over HTTP.

            Args:
                request (~.event_resources.ListOrganizationEventsRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.ListOrganizationEventsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/organizationEvents",
                },
            ]
            request, metadata = self._interceptor.pre_list_organization_events(
                request, metadata
            )
            pb_request = event_resources.ListOrganizationEventsRequest.pb(request)
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
            resp = event_resources.ListOrganizationEventsResponse()
            pb_resp = event_resources.ListOrganizationEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_organization_events(resp)
            return resp

    class _ListOrganizationImpacts(ServiceHealthRestStub):
        def __hash__(self):
            return hash("ListOrganizationImpacts")

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
            request: event_resources.ListOrganizationImpactsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_resources.ListOrganizationImpactsResponse:
            r"""Call the list organization impacts method over HTTP.

            Args:
                request (~.event_resources.ListOrganizationImpactsRequest):
                    The request object. Message for requesting list of
                OrganizationImpacts
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_resources.ListOrganizationImpactsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/organizationImpacts",
                },
            ]
            request, metadata = self._interceptor.pre_list_organization_impacts(
                request, metadata
            )
            pb_request = event_resources.ListOrganizationImpactsRequest.pb(request)
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
            resp = event_resources.ListOrganizationImpactsResponse()
            pb_resp = event_resources.ListOrganizationImpactsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_organization_impacts(resp)
            return resp

    @property
    def get_event(
        self,
    ) -> Callable[[event_resources.GetEventRequest], event_resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_organization_event(
        self,
    ) -> Callable[
        [event_resources.GetOrganizationEventRequest], event_resources.OrganizationEvent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrganizationEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_organization_impact(
        self,
    ) -> Callable[
        [event_resources.GetOrganizationImpactRequest],
        event_resources.OrganizationImpact,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetOrganizationImpact(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_events(
        self,
    ) -> Callable[
        [event_resources.ListEventsRequest], event_resources.ListEventsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_organization_events(
        self,
    ) -> Callable[
        [event_resources.ListOrganizationEventsRequest],
        event_resources.ListOrganizationEventsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOrganizationEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_organization_impacts(
        self,
    ) -> Callable[
        [event_resources.ListOrganizationImpactsRequest],
        event_resources.ListOrganizationImpactsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOrganizationImpacts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ServiceHealthRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(ServiceHealthRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ServiceHealthRestTransport",)
