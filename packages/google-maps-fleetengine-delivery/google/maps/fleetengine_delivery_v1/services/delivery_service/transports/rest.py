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


from google.maps.fleetengine_delivery_v1.types import (
    delivery_api,
    delivery_vehicles,
    task_tracking_info,
    tasks,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DeliveryServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DeliveryServiceRestInterceptor:
    """Interceptor for DeliveryService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DeliveryServiceRestTransport.

    .. code-block:: python
        class MyCustomDeliveryServiceInterceptor(DeliveryServiceRestInterceptor):
            def pre_batch_create_tasks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_tasks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_delivery_vehicle(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_delivery_vehicle(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_task(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_delivery_vehicle(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_delivery_vehicle(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_task(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_task_tracking_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_task_tracking_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_delivery_vehicles(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_delivery_vehicles(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tasks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tasks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_delivery_vehicle(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_delivery_vehicle(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_task(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_task(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DeliveryServiceRestTransport(interceptor=MyCustomDeliveryServiceInterceptor())
        client = DeliveryServiceClient(transport=transport)


    """

    def pre_batch_create_tasks(
        self,
        request: delivery_api.BatchCreateTasksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.BatchCreateTasksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_tasks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_batch_create_tasks(
        self, response: delivery_api.BatchCreateTasksResponse
    ) -> delivery_api.BatchCreateTasksResponse:
        """Post-rpc interceptor for batch_create_tasks

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_create_delivery_vehicle(
        self,
        request: delivery_api.CreateDeliveryVehicleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.CreateDeliveryVehicleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_delivery_vehicle

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_create_delivery_vehicle(
        self, response: delivery_vehicles.DeliveryVehicle
    ) -> delivery_vehicles.DeliveryVehicle:
        """Post-rpc interceptor for create_delivery_vehicle

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_create_task(
        self,
        request: delivery_api.CreateTaskRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.CreateTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_create_task(self, response: tasks.Task) -> tasks.Task:
        """Post-rpc interceptor for create_task

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_get_delivery_vehicle(
        self,
        request: delivery_api.GetDeliveryVehicleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.GetDeliveryVehicleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_delivery_vehicle

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_get_delivery_vehicle(
        self, response: delivery_vehicles.DeliveryVehicle
    ) -> delivery_vehicles.DeliveryVehicle:
        """Post-rpc interceptor for get_delivery_vehicle

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_get_task(
        self, request: delivery_api.GetTaskRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[delivery_api.GetTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_get_task(self, response: tasks.Task) -> tasks.Task:
        """Post-rpc interceptor for get_task

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_get_task_tracking_info(
        self,
        request: delivery_api.GetTaskTrackingInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.GetTaskTrackingInfoRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_task_tracking_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_get_task_tracking_info(
        self, response: task_tracking_info.TaskTrackingInfo
    ) -> task_tracking_info.TaskTrackingInfo:
        """Post-rpc interceptor for get_task_tracking_info

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_list_delivery_vehicles(
        self,
        request: delivery_api.ListDeliveryVehiclesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.ListDeliveryVehiclesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_delivery_vehicles

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_list_delivery_vehicles(
        self, response: delivery_api.ListDeliveryVehiclesResponse
    ) -> delivery_api.ListDeliveryVehiclesResponse:
        """Post-rpc interceptor for list_delivery_vehicles

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_list_tasks(
        self,
        request: delivery_api.ListTasksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.ListTasksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tasks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_list_tasks(
        self, response: delivery_api.ListTasksResponse
    ) -> delivery_api.ListTasksResponse:
        """Post-rpc interceptor for list_tasks

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_update_delivery_vehicle(
        self,
        request: delivery_api.UpdateDeliveryVehicleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.UpdateDeliveryVehicleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_delivery_vehicle

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_update_delivery_vehicle(
        self, response: delivery_vehicles.DeliveryVehicle
    ) -> delivery_vehicles.DeliveryVehicle:
        """Post-rpc interceptor for update_delivery_vehicle

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response

    def pre_update_task(
        self,
        request: delivery_api.UpdateTaskRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[delivery_api.UpdateTaskRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_task

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeliveryService server.
        """
        return request, metadata

    def post_update_task(self, response: tasks.Task) -> tasks.Task:
        """Post-rpc interceptor for update_task

        Override in a subclass to manipulate the response
        after it is returned by the DeliveryService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DeliveryServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DeliveryServiceRestInterceptor


class DeliveryServiceRestTransport(DeliveryServiceTransport):
    """REST backend transport for DeliveryService.

    The Last Mile Delivery service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "fleetengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DeliveryServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'fleetengine.googleapis.com').
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
        self._interceptor = interceptor or DeliveryServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchCreateTasks(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("BatchCreateTasks")

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
            request: delivery_api.BatchCreateTasksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_api.BatchCreateTasksResponse:
            r"""Call the batch create tasks method over HTTP.

            Args:
                request (~.delivery_api.BatchCreateTasksRequest):
                    The request object. The ``BatchCreateTask`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_api.BatchCreateTasksResponse:
                    The ``BatchCreateTask`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=providers/*}/tasks:batchCreate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_create_tasks(
                request, metadata
            )
            pb_request = delivery_api.BatchCreateTasksRequest.pb(request)
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
            resp = delivery_api.BatchCreateTasksResponse()
            pb_resp = delivery_api.BatchCreateTasksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_tasks(resp)
            return resp

    class _CreateDeliveryVehicle(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("CreateDeliveryVehicle")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "deliveryVehicleId": "",
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
            request: delivery_api.CreateDeliveryVehicleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_vehicles.DeliveryVehicle:
            r"""Call the create delivery vehicle method over HTTP.

            Args:
                request (~.delivery_api.CreateDeliveryVehicleRequest):
                    The request object. The ``CreateDeliveryVehicle`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_vehicles.DeliveryVehicle:
                    The ``DeliveryVehicle`` message. A delivery vehicle
                transports shipments from a depot to a delivery
                location, and from a pickup location to the depot. In
                some cases, delivery vehicles also transport shipments
                directly from the pickup location to the delivery
                location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``DeliveryVehicle.current_route_segment`` field in the
                gRPC API and the ``DeliveryVehicle.currentRouteSegment``
                field in the REST API refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=providers/*}/deliveryVehicles",
                    "body": "delivery_vehicle",
                },
            ]
            request, metadata = self._interceptor.pre_create_delivery_vehicle(
                request, metadata
            )
            pb_request = delivery_api.CreateDeliveryVehicleRequest.pb(request)
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
            resp = delivery_vehicles.DeliveryVehicle()
            pb_resp = delivery_vehicles.DeliveryVehicle.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_delivery_vehicle(resp)
            return resp

    class _CreateTask(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("CreateTask")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "taskId": "",
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
            request: delivery_api.CreateTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tasks.Task:
            r"""Call the create task method over HTTP.

            Args:
                request (~.delivery_api.CreateTaskRequest):
                    The request object. The ``CreateTask`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tasks.Task:
                    A Task in the Delivery API represents a single action to
                track. In general, there is a distinction between
                shipment-related Tasks and break Tasks. A shipment can
                have multiple Tasks associated with it. For example,
                there could be one Task for the pickup, and one for the
                drop-off or transfer. Also, different Tasks for a given
                shipment can be handled by different vehicles. For
                example, one vehicle could handle the pickup, driving
                the shipment to the hub, while another vehicle drives
                the same shipment from the hub to the drop-off location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``Task.journey_sharing_info`` field in the gRPC API and
                the ``Task.journeySharingInfo`` field in the REST API
                refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=providers/*}/tasks",
                    "body": "task",
                },
            ]
            request, metadata = self._interceptor.pre_create_task(request, metadata)
            pb_request = delivery_api.CreateTaskRequest.pb(request)
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
            resp = tasks.Task()
            pb_resp = tasks.Task.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_task(resp)
            return resp

    class _GetDeliveryVehicle(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("GetDeliveryVehicle")

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
            request: delivery_api.GetDeliveryVehicleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_vehicles.DeliveryVehicle:
            r"""Call the get delivery vehicle method over HTTP.

            Args:
                request (~.delivery_api.GetDeliveryVehicleRequest):
                    The request object. The ``GetDeliveryVehicle`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_vehicles.DeliveryVehicle:
                    The ``DeliveryVehicle`` message. A delivery vehicle
                transports shipments from a depot to a delivery
                location, and from a pickup location to the depot. In
                some cases, delivery vehicles also transport shipments
                directly from the pickup location to the delivery
                location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``DeliveryVehicle.current_route_segment`` field in the
                gRPC API and the ``DeliveryVehicle.currentRouteSegment``
                field in the REST API refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=providers/*/deliveryVehicles/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_delivery_vehicle(
                request, metadata
            )
            pb_request = delivery_api.GetDeliveryVehicleRequest.pb(request)
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
            resp = delivery_vehicles.DeliveryVehicle()
            pb_resp = delivery_vehicles.DeliveryVehicle.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_delivery_vehicle(resp)
            return resp

    class _GetTask(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("GetTask")

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
            request: delivery_api.GetTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tasks.Task:
            r"""Call the get task method over HTTP.

            Args:
                request (~.delivery_api.GetTaskRequest):
                    The request object. The ``GetTask`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tasks.Task:
                    A Task in the Delivery API represents a single action to
                track. In general, there is a distinction between
                shipment-related Tasks and break Tasks. A shipment can
                have multiple Tasks associated with it. For example,
                there could be one Task for the pickup, and one for the
                drop-off or transfer. Also, different Tasks for a given
                shipment can be handled by different vehicles. For
                example, one vehicle could handle the pickup, driving
                the shipment to the hub, while another vehicle drives
                the same shipment from the hub to the drop-off location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``Task.journey_sharing_info`` field in the gRPC API and
                the ``Task.journeySharingInfo`` field in the REST API
                refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=providers/*/tasks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_task(request, metadata)
            pb_request = delivery_api.GetTaskRequest.pb(request)
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
            resp = tasks.Task()
            pb_resp = tasks.Task.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_task(resp)
            return resp

    class _GetTaskTrackingInfo(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("GetTaskTrackingInfo")

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
            request: delivery_api.GetTaskTrackingInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> task_tracking_info.TaskTrackingInfo:
            r"""Call the get task tracking info method over HTTP.

            Args:
                request (~.delivery_api.GetTaskTrackingInfoRequest):
                    The request object. The ``GetTaskTrackingInfoRequest`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.task_tracking_info.TaskTrackingInfo:
                    The ``TaskTrackingInfo`` message. The message contains
                task tracking information which will be used for
                display. If a tracking ID is associated with multiple
                Tasks, Fleet Engine uses a heuristic to decide which
                Task's TaskTrackingInfo to select.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=providers/*/taskTrackingInfo/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_task_tracking_info(
                request, metadata
            )
            pb_request = delivery_api.GetTaskTrackingInfoRequest.pb(request)
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
            resp = task_tracking_info.TaskTrackingInfo()
            pb_resp = task_tracking_info.TaskTrackingInfo.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_task_tracking_info(resp)
            return resp

    class _ListDeliveryVehicles(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("ListDeliveryVehicles")

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
            request: delivery_api.ListDeliveryVehiclesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_api.ListDeliveryVehiclesResponse:
            r"""Call the list delivery vehicles method over HTTP.

            Args:
                request (~.delivery_api.ListDeliveryVehiclesRequest):
                    The request object. The ``ListDeliveryVehicles`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_api.ListDeliveryVehiclesResponse:
                    The ``ListDeliveryVehicles`` response message.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=providers/*}/deliveryVehicles",
                },
            ]
            request, metadata = self._interceptor.pre_list_delivery_vehicles(
                request, metadata
            )
            pb_request = delivery_api.ListDeliveryVehiclesRequest.pb(request)
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
            resp = delivery_api.ListDeliveryVehiclesResponse()
            pb_resp = delivery_api.ListDeliveryVehiclesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_delivery_vehicles(resp)
            return resp

    class _ListTasks(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("ListTasks")

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
            request: delivery_api.ListTasksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_api.ListTasksResponse:
            r"""Call the list tasks method over HTTP.

            Args:
                request (~.delivery_api.ListTasksRequest):
                    The request object. The ``ListTasks`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_api.ListTasksResponse:
                    The ``ListTasks`` response that contains the set of
                Tasks that meet the filter criteria in the
                ``ListTasksRequest``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=providers/*}/tasks",
                },
            ]
            request, metadata = self._interceptor.pre_list_tasks(request, metadata)
            pb_request = delivery_api.ListTasksRequest.pb(request)
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
            resp = delivery_api.ListTasksResponse()
            pb_resp = delivery_api.ListTasksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tasks(resp)
            return resp

    class _UpdateDeliveryVehicle(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("UpdateDeliveryVehicle")

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
            request: delivery_api.UpdateDeliveryVehicleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> delivery_vehicles.DeliveryVehicle:
            r"""Call the update delivery vehicle method over HTTP.

            Args:
                request (~.delivery_api.UpdateDeliveryVehicleRequest):
                    The request object. The ``UpdateDeliveryVehicle`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.delivery_vehicles.DeliveryVehicle:
                    The ``DeliveryVehicle`` message. A delivery vehicle
                transports shipments from a depot to a delivery
                location, and from a pickup location to the depot. In
                some cases, delivery vehicles also transport shipments
                directly from the pickup location to the delivery
                location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``DeliveryVehicle.current_route_segment`` field in the
                gRPC API and the ``DeliveryVehicle.currentRouteSegment``
                field in the REST API refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{delivery_vehicle.name=providers/*/deliveryVehicles/*}",
                    "body": "delivery_vehicle",
                },
            ]
            request, metadata = self._interceptor.pre_update_delivery_vehicle(
                request, metadata
            )
            pb_request = delivery_api.UpdateDeliveryVehicleRequest.pb(request)
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
            resp = delivery_vehicles.DeliveryVehicle()
            pb_resp = delivery_vehicles.DeliveryVehicle.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_delivery_vehicle(resp)
            return resp

    class _UpdateTask(DeliveryServiceRestStub):
        def __hash__(self):
            return hash("UpdateTask")

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
            request: delivery_api.UpdateTaskRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> tasks.Task:
            r"""Call the update task method over HTTP.

            Args:
                request (~.delivery_api.UpdateTaskRequest):
                    The request object. The ``UpdateTask`` request message.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.tasks.Task:
                    A Task in the Delivery API represents a single action to
                track. In general, there is a distinction between
                shipment-related Tasks and break Tasks. A shipment can
                have multiple Tasks associated with it. For example,
                there could be one Task for the pickup, and one for the
                drop-off or transfer. Also, different Tasks for a given
                shipment can be handled by different vehicles. For
                example, one vehicle could handle the pickup, driving
                the shipment to the hub, while another vehicle drives
                the same shipment from the hub to the drop-off location.

                Note: gRPC and REST APIs use different field naming
                conventions. For example, the
                ``Task.journey_sharing_info`` field in the gRPC API and
                the ``Task.journeySharingInfo`` field in the REST API
                refer to the same field.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{task.name=providers/*/tasks/*}",
                    "body": "task",
                },
            ]
            request, metadata = self._interceptor.pre_update_task(request, metadata)
            pb_request = delivery_api.UpdateTaskRequest.pb(request)
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
            resp = tasks.Task()
            pb_resp = tasks.Task.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_task(resp)
            return resp

    @property
    def batch_create_tasks(
        self,
    ) -> Callable[
        [delivery_api.BatchCreateTasksRequest], delivery_api.BatchCreateTasksResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateTasks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_delivery_vehicle(
        self,
    ) -> Callable[
        [delivery_api.CreateDeliveryVehicleRequest], delivery_vehicles.DeliveryVehicle
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeliveryVehicle(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_task(self) -> Callable[[delivery_api.CreateTaskRequest], tasks.Task]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_delivery_vehicle(
        self,
    ) -> Callable[
        [delivery_api.GetDeliveryVehicleRequest], delivery_vehicles.DeliveryVehicle
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeliveryVehicle(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_task(self) -> Callable[[delivery_api.GetTaskRequest], tasks.Task]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_task_tracking_info(
        self,
    ) -> Callable[
        [delivery_api.GetTaskTrackingInfoRequest], task_tracking_info.TaskTrackingInfo
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTaskTrackingInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_delivery_vehicles(
        self,
    ) -> Callable[
        [delivery_api.ListDeliveryVehiclesRequest],
        delivery_api.ListDeliveryVehiclesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeliveryVehicles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tasks(
        self,
    ) -> Callable[[delivery_api.ListTasksRequest], delivery_api.ListTasksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTasks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_delivery_vehicle(
        self,
    ) -> Callable[
        [delivery_api.UpdateDeliveryVehicleRequest], delivery_vehicles.DeliveryVehicle
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeliveryVehicle(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_task(self) -> Callable[[delivery_api.UpdateTaskRequest], tasks.Task]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTask(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DeliveryServiceRestTransport",)
