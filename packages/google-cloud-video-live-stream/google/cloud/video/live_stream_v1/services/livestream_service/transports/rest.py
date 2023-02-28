# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.video.live_stream_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import LivestreamServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class LivestreamServiceRestInterceptor:
    """Interceptor for LivestreamService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LivestreamServiceRestTransport.

    .. code-block:: python
        class MyCustomLivestreamServiceInterceptor(LivestreamServiceRestInterceptor):
            def pre_create_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_channels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_channels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_inputs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_inputs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_input(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LivestreamServiceRestTransport(interceptor=MyCustomLivestreamServiceInterceptor())
        client = LivestreamServiceClient(transport=transport)


    """

    def pre_create_channel(
        self, request: service.CreateChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_event(
        self, request: service.CreateEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_event(self, response: resources.Event) -> resources.Event:
        """Post-rpc interceptor for create_event

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_input(
        self, request: service.CreateInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_channel(
        self, request: service.DeleteChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_event(
        self, request: service.DeleteEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def pre_delete_input(
        self, request: service.DeleteInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_channel(
        self, request: service.GetChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_channel(self, response: resources.Channel) -> resources.Channel:
        """Post-rpc interceptor for get_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_event(
        self, request: service.GetEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_event(self, response: resources.Event) -> resources.Event:
        """Post-rpc interceptor for get_event

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_input(
        self, request: service.GetInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_input(self, response: resources.Input) -> resources.Input:
        """Post-rpc interceptor for get_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_channels(
        self, request: service.ListChannelsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListChannelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_channels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_channels(
        self, response: service.ListChannelsResponse
    ) -> service.ListChannelsResponse:
        """Post-rpc interceptor for list_channels

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_events(
        self, request: service.ListEventsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_events(
        self, response: service.ListEventsResponse
    ) -> service.ListEventsResponse:
        """Post-rpc interceptor for list_events

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_inputs(
        self, request: service.ListInputsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListInputsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_inputs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_inputs(
        self, response: service.ListInputsResponse
    ) -> service.ListInputsResponse:
        """Post-rpc interceptor for list_inputs

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_start_channel(
        self, request: service.StartChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.StartChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_start_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_stop_channel(
        self, request: service.StopChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.StopChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_stop_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_update_channel(
        self, request: service.UpdateChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_update_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_update_input(
        self, request: service.UpdateInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_update_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LivestreamServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LivestreamServiceRestInterceptor


class LivestreamServiceRestTransport(LivestreamServiceTransport):
    """REST backend transport for LivestreamService.

    Using Live Stream API, you can generate live streams in the
    various renditions and streaming formats. The streaming format
    include HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming
    over HTTP (DASH). You can send a source stream in the various
    ways, including Real-Time Messaging Protocol (RTMP) and Secure
    Reliable Transport (SRT).

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "livestream.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LivestreamServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or LivestreamServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("CreateChannel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "channelId": "",
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
            request: service.CreateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create channel method over HTTP.

            Args:
                request (~.service.CreateChannelRequest):
                    The request object. Request message for
                "LivestreamService.CreateChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/channels",
                    "body": "channel",
                },
            ]
            request, metadata = self._interceptor.pre_create_channel(request, metadata)
            pb_request = service.CreateChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_channel(resp)
            return resp

    class _CreateEvent(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("CreateEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "eventId": "",
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
            request: service.CreateEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Event:
            r"""Call the create event method over HTTP.

            Args:
                request (~.service.CreateEventRequest):
                    The request object. Request message for
                "LivestreamService.CreateEvent".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Event:
                    Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/channels/*}/events",
                    "body": "event",
                },
            ]
            request, metadata = self._interceptor.pre_create_event(request, metadata)
            pb_request = service.CreateEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Event()
            pb_resp = resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_event(resp)
            return resp

    class _CreateInput(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("CreateInput")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "inputId": "",
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
            request: service.CreateInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create input method over HTTP.

            Args:
                request (~.service.CreateInputRequest):
                    The request object. Request message for
                "LivestreamService.CreateInput".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/inputs",
                    "body": "input",
                },
            ]
            request, metadata = self._interceptor.pre_create_input(request, metadata)
            pb_request = service.CreateInputRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_input(resp)
            return resp

    class _DeleteChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("DeleteChannel")

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
            request: service.DeleteChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete channel method over HTTP.

            Args:
                request (~.service.DeleteChannelRequest):
                    The request object. Request message for
                "LivestreamService.DeleteChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_channel(request, metadata)
            pb_request = service.DeleteChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_channel(resp)
            return resp

    class _DeleteEvent(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("DeleteEvent")

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
            request: service.DeleteEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete event method over HTTP.

            Args:
                request (~.service.DeleteEventRequest):
                    The request object. Request message for
                "LivestreamService.DeleteEvent".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*/events/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_event(request, metadata)
            pb_request = service.DeleteEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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

    class _DeleteInput(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("DeleteInput")

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
            request: service.DeleteInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete input method over HTTP.

            Args:
                request (~.service.DeleteInputRequest):
                    The request object. Request message for
                "LivestreamService.DeleteInput".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/inputs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_input(request, metadata)
            pb_request = service.DeleteInputRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_input(resp)
            return resp

    class _GetChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("GetChannel")

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
            request: service.GetChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Channel:
            r"""Call the get channel method over HTTP.

            Args:
                request (~.service.GetChannelRequest):
                    The request object. Request message for
                "LivestreamService.GetChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Channel:
                    Channel resource represents the
                processor that does a user-defined
                "streaming" operation, which includes
                getting an input stream through an
                input, transcoding it to multiple
                renditions, and publishing output live
                streams in certain formats (for example,
                HLS or DASH) to the specified location.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_channel(request, metadata)
            pb_request = service.GetChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Channel()
            pb_resp = resources.Channel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_channel(resp)
            return resp

    class _GetEvent(LivestreamServiceRestStub):
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
            request: service.GetEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Event:
            r"""Call the get event method over HTTP.

            Args:
                request (~.service.GetEventRequest):
                    The request object. Request message for
                "LivestreamService.GetEvent".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Event:
                    Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*/events/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_event(request, metadata)
            pb_request = service.GetEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Event()
            pb_resp = resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event(resp)
            return resp

    class _GetInput(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("GetInput")

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
            request: service.GetInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Input:
            r"""Call the get input method over HTTP.

            Args:
                request (~.service.GetInputRequest):
                    The request object. Request message for
                "LivestreamService.GetInput".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Input:
                    Input resource represents the
                endpoint from which the channel ingests
                the input stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/inputs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_input(request, metadata)
            pb_request = service.GetInputRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Input()
            pb_resp = resources.Input.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_input(resp)
            return resp

    class _ListChannels(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("ListChannels")

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
            request: service.ListChannelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListChannelsResponse:
            r"""Call the list channels method over HTTP.

            Args:
                request (~.service.ListChannelsRequest):
                    The request object. Request message for
                "LivestreamService.ListChannels".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListChannelsResponse:
                    Response message for
                "LivestreamService.ListChannels".

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/channels",
                },
            ]
            request, metadata = self._interceptor.pre_list_channels(request, metadata)
            pb_request = service.ListChannelsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListChannelsResponse()
            pb_resp = service.ListChannelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_channels(resp)
            return resp

    class _ListEvents(LivestreamServiceRestStub):
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
            request: service.ListEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListEventsResponse:
            r"""Call the list events method over HTTP.

            Args:
                request (~.service.ListEventsRequest):
                    The request object. Request message for
                "LivestreamService.ListEvents".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListEventsResponse:
                    Response message for
                "LivestreamService.ListEvents".

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/channels/*}/events",
                },
            ]
            request, metadata = self._interceptor.pre_list_events(request, metadata)
            pb_request = service.ListEventsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListEventsResponse()
            pb_resp = service.ListEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_events(resp)
            return resp

    class _ListInputs(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("ListInputs")

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
            request: service.ListInputsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListInputsResponse:
            r"""Call the list inputs method over HTTP.

            Args:
                request (~.service.ListInputsRequest):
                    The request object. Request message for
                "LivestreamService.ListInputs".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListInputsResponse:
                    Response message for
                "LivestreamService.ListInputs".

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/inputs",
                },
            ]
            request, metadata = self._interceptor.pre_list_inputs(request, metadata)
            pb_request = service.ListInputsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListInputsResponse()
            pb_resp = service.ListInputsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_inputs(resp)
            return resp

    class _StartChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("StartChannel")

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
            request: service.StartChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start channel method over HTTP.

            Args:
                request (~.service.StartChannelRequest):
                    The request object. Request message for
                "LivestreamService.StartChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*}:start",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_start_channel(request, metadata)
            pb_request = service.StartChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_channel(resp)
            return resp

    class _StopChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("StopChannel")

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
            request: service.StopChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop channel method over HTTP.

            Args:
                request (~.service.StopChannelRequest):
                    The request object. Request message for
                "LivestreamService.StopChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/channels/*}:stop",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stop_channel(request, metadata)
            pb_request = service.StopChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_stop_channel(resp)
            return resp

    class _UpdateChannel(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("UpdateChannel")

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
            request: service.UpdateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update channel method over HTTP.

            Args:
                request (~.service.UpdateChannelRequest):
                    The request object. Request message for
                "LivestreamService.UpdateChannel".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{channel.name=projects/*/locations/*/channels/*}",
                    "body": "channel",
                },
            ]
            request, metadata = self._interceptor.pre_update_channel(request, metadata)
            pb_request = service.UpdateChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_channel(resp)
            return resp

    class _UpdateInput(LivestreamServiceRestStub):
        def __hash__(self):
            return hash("UpdateInput")

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
            request: service.UpdateInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update input method over HTTP.

            Args:
                request (~.service.UpdateInputRequest):
                    The request object. Request message for
                "LivestreamService.UpdateInput".

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{input.name=projects/*/locations/*/inputs/*}",
                    "body": "input",
                },
            ]
            request, metadata = self._interceptor.pre_update_input(request, metadata)
            pb_request = service.UpdateInputRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_input(resp)
            return resp

    @property
    def create_channel_(
        self,
    ) -> Callable[[service.CreateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_event(self) -> Callable[[service.CreateEventRequest], resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_input(
        self,
    ) -> Callable[[service.CreateInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_channel(
        self,
    ) -> Callable[[service.DeleteChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_event(self) -> Callable[[service.DeleteEventRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_input(
        self,
    ) -> Callable[[service.DeleteInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_channel(self) -> Callable[[service.GetChannelRequest], resources.Channel]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_event(self) -> Callable[[service.GetEventRequest], resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_input(self) -> Callable[[service.GetInputRequest], resources.Input]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_channels(
        self,
    ) -> Callable[[service.ListChannelsRequest], service.ListChannelsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChannels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_events(
        self,
    ) -> Callable[[service.ListEventsRequest], service.ListEventsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_inputs(
        self,
    ) -> Callable[[service.ListInputsRequest], service.ListInputsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInputs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_channel(
        self,
    ) -> Callable[[service.StartChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_channel(
        self,
    ) -> Callable[[service.StopChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_channel(
        self,
    ) -> Callable[[service.UpdateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_input(
        self,
    ) -> Callable[[service.UpdateInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LivestreamServiceRestTransport",)
