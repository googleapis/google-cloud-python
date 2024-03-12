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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.apps.events_subscriptions_v1.types import (
    subscription_resource,
    subscriptions_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import SubscriptionsServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SubscriptionsServiceRestInterceptor:
    """Interceptor for SubscriptionsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SubscriptionsServiceRestTransport.

    .. code-block:: python
        class MyCustomSubscriptionsServiceInterceptor(SubscriptionsServiceRestInterceptor):
            def pre_create_subscription(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_subscription(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_subscription(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_subscription(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_subscription(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_subscription(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_subscriptions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_subscriptions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reactivate_subscription(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reactivate_subscription(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_subscription(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_subscription(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SubscriptionsServiceRestTransport(interceptor=MyCustomSubscriptionsServiceInterceptor())
        client = SubscriptionsServiceClient(transport=transport)


    """

    def pre_create_subscription(
        self,
        request: subscriptions_service.CreateSubscriptionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        subscriptions_service.CreateSubscriptionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_subscription

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_create_subscription(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_subscription

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_subscription(
        self,
        request: subscriptions_service.DeleteSubscriptionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        subscriptions_service.DeleteSubscriptionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_subscription

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_delete_subscription(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_subscription

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_subscription(
        self,
        request: subscriptions_service.GetSubscriptionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[subscriptions_service.GetSubscriptionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_subscription

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_get_subscription(
        self, response: subscription_resource.Subscription
    ) -> subscription_resource.Subscription:
        """Post-rpc interceptor for get_subscription

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_subscriptions(
        self,
        request: subscriptions_service.ListSubscriptionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        subscriptions_service.ListSubscriptionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_subscriptions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_list_subscriptions(
        self, response: subscriptions_service.ListSubscriptionsResponse
    ) -> subscriptions_service.ListSubscriptionsResponse:
        """Post-rpc interceptor for list_subscriptions

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_reactivate_subscription(
        self,
        request: subscriptions_service.ReactivateSubscriptionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        subscriptions_service.ReactivateSubscriptionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for reactivate_subscription

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_reactivate_subscription(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reactivate_subscription

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_subscription(
        self,
        request: subscriptions_service.UpdateSubscriptionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        subscriptions_service.UpdateSubscriptionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_subscription

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_update_subscription(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_subscription

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SubscriptionsService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SubscriptionsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SubscriptionsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SubscriptionsServiceRestInterceptor


class SubscriptionsServiceRestTransport(SubscriptionsServiceTransport):
    """REST backend transport for SubscriptionsService.

    A service that manages subscriptions to Google Workspace
    events.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "workspaceevents.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SubscriptionsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'workspaceevents.googleapis.com').
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
        self._interceptor = interceptor or SubscriptionsServiceRestInterceptor()
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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=operations/**}",
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

    class _CreateSubscription(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("CreateSubscription")

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
            request: subscriptions_service.CreateSubscriptionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create subscription method over HTTP.

            Args:
                request (~.subscriptions_service.CreateSubscriptionRequest):
                    The request object. The request message for
                [SubscriptionsService.CreateSubscription][google.apps.events.subscriptions.v1.SubscriptionsService.CreateSubscription].
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
                    "uri": "/v1/subscriptions",
                    "body": "subscription",
                },
            ]
            request, metadata = self._interceptor.pre_create_subscription(
                request, metadata
            )
            pb_request = subscriptions_service.CreateSubscriptionRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_subscription(resp)
            return resp

    class _DeleteSubscription(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("DeleteSubscription")

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
            request: subscriptions_service.DeleteSubscriptionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete subscription method over HTTP.

            Args:
                request (~.subscriptions_service.DeleteSubscriptionRequest):
                    The request object. The request message for
                [SubscriptionsService.DeleteSubscription][google.apps.events.subscriptions.v1.SubscriptionsService.DeleteSubscription].
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
                    "uri": "/v1/{name=subscriptions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_subscription(
                request, metadata
            )
            pb_request = subscriptions_service.DeleteSubscriptionRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_subscription(resp)
            return resp

    class _GetSubscription(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("GetSubscription")

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
            request: subscriptions_service.GetSubscriptionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> subscription_resource.Subscription:
            r"""Call the get subscription method over HTTP.

            Args:
                request (~.subscriptions_service.GetSubscriptionRequest):
                    The request object. The request message for
                [SubscriptionsService.GetSubscription][google.apps.events.subscriptions.v1.SubscriptionsService.GetSubscription].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.subscription_resource.Subscription:
                    A subscription to receive events about a Google
                Workspace resource. To learn more about subscriptions,
                see the `Google Workspace Events API
                overview <https://developers.google.com/workspace/events>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=subscriptions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_subscription(
                request, metadata
            )
            pb_request = subscriptions_service.GetSubscriptionRequest.pb(request)
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
            resp = subscription_resource.Subscription()
            pb_resp = subscription_resource.Subscription.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_subscription(resp)
            return resp

    class _ListSubscriptions(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("ListSubscriptions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "filter": "",
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
            request: subscriptions_service.ListSubscriptionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> subscriptions_service.ListSubscriptionsResponse:
            r"""Call the list subscriptions method over HTTP.

            Args:
                request (~.subscriptions_service.ListSubscriptionsRequest):
                    The request object. The request message for
                [SubscriptionsService.ListSubscriptions][google.apps.events.subscriptions.v1.SubscriptionsService.ListSubscriptions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.subscriptions_service.ListSubscriptionsResponse:
                    The response message for
                [SubscriptionsService.ListSubscriptions][google.apps.events.subscriptions.v1.SubscriptionsService.ListSubscriptions].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/subscriptions",
                },
            ]
            request, metadata = self._interceptor.pre_list_subscriptions(
                request, metadata
            )
            pb_request = subscriptions_service.ListSubscriptionsRequest.pb(request)
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
            resp = subscriptions_service.ListSubscriptionsResponse()
            pb_resp = subscriptions_service.ListSubscriptionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_subscriptions(resp)
            return resp

    class _ReactivateSubscription(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("ReactivateSubscription")

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
            request: subscriptions_service.ReactivateSubscriptionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reactivate subscription method over HTTP.

            Args:
                request (~.subscriptions_service.ReactivateSubscriptionRequest):
                    The request object. The request message for
                [SubscriptionsService.ReactivateSubscription][google.apps.events.subscriptions.v1.SubscriptionsService.ReactivateSubscription].
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
                    "uri": "/v1/{name=subscriptions/*}:reactivate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reactivate_subscription(
                request, metadata
            )
            pb_request = subscriptions_service.ReactivateSubscriptionRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_reactivate_subscription(resp)
            return resp

    class _UpdateSubscription(SubscriptionsServiceRestStub):
        def __hash__(self):
            return hash("UpdateSubscription")

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
            request: subscriptions_service.UpdateSubscriptionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update subscription method over HTTP.

            Args:
                request (~.subscriptions_service.UpdateSubscriptionRequest):
                    The request object. The request message for
                [SubscriptionsService.UpdateSubscription][google.apps.events.subscriptions.v1.SubscriptionsService.UpdateSubscription].
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
                    "uri": "/v1/{subscription.name=subscriptions/*}",
                    "body": "subscription",
                },
            ]
            request, metadata = self._interceptor.pre_update_subscription(
                request, metadata
            )
            pb_request = subscriptions_service.UpdateSubscriptionRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_subscription(resp)
            return resp

    @property
    def create_subscription(
        self,
    ) -> Callable[
        [subscriptions_service.CreateSubscriptionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSubscription(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_subscription(
        self,
    ) -> Callable[
        [subscriptions_service.DeleteSubscriptionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSubscription(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_subscription(
        self,
    ) -> Callable[
        [subscriptions_service.GetSubscriptionRequest],
        subscription_resource.Subscription,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSubscription(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_subscriptions(
        self,
    ) -> Callable[
        [subscriptions_service.ListSubscriptionsRequest],
        subscriptions_service.ListSubscriptionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSubscriptions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reactivate_subscription(
        self,
    ) -> Callable[
        [subscriptions_service.ReactivateSubscriptionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReactivateSubscription(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_subscription(
        self,
    ) -> Callable[
        [subscriptions_service.UpdateSubscriptionRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSubscription(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(SubscriptionsServiceRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=operations/**}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
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

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("SubscriptionsServiceRestTransport",)
