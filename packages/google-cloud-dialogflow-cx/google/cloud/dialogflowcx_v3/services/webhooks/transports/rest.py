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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflowcx_v3.types import webhook
from google.cloud.dialogflowcx_v3.types import webhook as gcdc_webhook

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseWebhooksRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class WebhooksRestInterceptor:
    """Interceptor for Webhooks.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the WebhooksRestTransport.

    .. code-block:: python
        class MyCustomWebhooksInterceptor(WebhooksRestInterceptor):
            def pre_create_webhook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_webhook(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_webhook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_webhook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_webhook(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_webhooks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_webhooks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_webhook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_webhook(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = WebhooksRestTransport(interceptor=MyCustomWebhooksInterceptor())
        client = WebhooksClient(transport=transport)


    """

    def pre_create_webhook(
        self,
        request: gcdc_webhook.CreateWebhookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_webhook.CreateWebhookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_webhook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_create_webhook(
        self, response: gcdc_webhook.Webhook
    ) -> gcdc_webhook.Webhook:
        """Post-rpc interceptor for create_webhook

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response

    def pre_delete_webhook(
        self, request: webhook.DeleteWebhookRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[webhook.DeleteWebhookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_webhook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def pre_get_webhook(
        self, request: webhook.GetWebhookRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[webhook.GetWebhookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_webhook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_get_webhook(self, response: webhook.Webhook) -> webhook.Webhook:
        """Post-rpc interceptor for get_webhook

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response

    def pre_list_webhooks(
        self, request: webhook.ListWebhooksRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[webhook.ListWebhooksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_webhooks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_list_webhooks(
        self, response: webhook.ListWebhooksResponse
    ) -> webhook.ListWebhooksResponse:
        """Post-rpc interceptor for list_webhooks

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response

    def pre_update_webhook(
        self,
        request: gcdc_webhook.UpdateWebhookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcdc_webhook.UpdateWebhookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_webhook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_update_webhook(
        self, response: gcdc_webhook.Webhook
    ) -> gcdc_webhook.Webhook:
        """Post-rpc interceptor for update_webhook

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
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
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
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
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
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
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Webhooks server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Webhooks server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class WebhooksRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: WebhooksRestInterceptor


class WebhooksRestTransport(_BaseWebhooksRestTransport):
    """REST backend synchronous transport for Webhooks.

    Service for managing
    [Webhooks][google.cloud.dialogflow.cx.v3.Webhook].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[WebhooksRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
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
        self._interceptor = interceptor or WebhooksRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateWebhook(
        _BaseWebhooksRestTransport._BaseCreateWebhook, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.CreateWebhook")

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
            request: gcdc_webhook.CreateWebhookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_webhook.Webhook:
            r"""Call the create webhook method over HTTP.

            Args:
                request (~.gcdc_webhook.CreateWebhookRequest):
                    The request object. The request message for
                [Webhooks.CreateWebhook][google.cloud.dialogflow.cx.v3.Webhooks.CreateWebhook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_webhook.Webhook:
                    Webhooks host the developer's
                business logic. During a session,
                webhooks allow the developer to use the
                data extracted by Dialogflow's natural
                language processing to generate dynamic
                responses, validate collected data, or
                trigger actions on the backend.

            """

            http_options = (
                _BaseWebhooksRestTransport._BaseCreateWebhook._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_webhook(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseCreateWebhook._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWebhooksRestTransport._BaseCreateWebhook._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseCreateWebhook._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._CreateWebhook._get_response(
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
            resp = gcdc_webhook.Webhook()
            pb_resp = gcdc_webhook.Webhook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_webhook(resp)
            return resp

    class _DeleteWebhook(
        _BaseWebhooksRestTransport._BaseDeleteWebhook, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.DeleteWebhook")

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
            request: webhook.DeleteWebhookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete webhook method over HTTP.

            Args:
                request (~.webhook.DeleteWebhookRequest):
                    The request object. The request message for
                [Webhooks.DeleteWebhook][google.cloud.dialogflow.cx.v3.Webhooks.DeleteWebhook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWebhooksRestTransport._BaseDeleteWebhook._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_webhook(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseDeleteWebhook._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseDeleteWebhook._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._DeleteWebhook._get_response(
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

    class _GetWebhook(_BaseWebhooksRestTransport._BaseGetWebhook, WebhooksRestStub):
        def __hash__(self):
            return hash("WebhooksRestTransport.GetWebhook")

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
            request: webhook.GetWebhookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> webhook.Webhook:
            r"""Call the get webhook method over HTTP.

            Args:
                request (~.webhook.GetWebhookRequest):
                    The request object. The request message for
                [Webhooks.GetWebhook][google.cloud.dialogflow.cx.v3.Webhooks.GetWebhook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.webhook.Webhook:
                    Webhooks host the developer's
                business logic. During a session,
                webhooks allow the developer to use the
                data extracted by Dialogflow's natural
                language processing to generate dynamic
                responses, validate collected data, or
                trigger actions on the backend.

            """

            http_options = (
                _BaseWebhooksRestTransport._BaseGetWebhook._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_webhook(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseGetWebhook._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseGetWebhook._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._GetWebhook._get_response(
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
            resp = webhook.Webhook()
            pb_resp = webhook.Webhook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_webhook(resp)
            return resp

    class _ListWebhooks(_BaseWebhooksRestTransport._BaseListWebhooks, WebhooksRestStub):
        def __hash__(self):
            return hash("WebhooksRestTransport.ListWebhooks")

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
            request: webhook.ListWebhooksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> webhook.ListWebhooksResponse:
            r"""Call the list webhooks method over HTTP.

            Args:
                request (~.webhook.ListWebhooksRequest):
                    The request object. The request message for
                [Webhooks.ListWebhooks][google.cloud.dialogflow.cx.v3.Webhooks.ListWebhooks].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.webhook.ListWebhooksResponse:
                    The response message for
                [Webhooks.ListWebhooks][google.cloud.dialogflow.cx.v3.Webhooks.ListWebhooks].

            """

            http_options = (
                _BaseWebhooksRestTransport._BaseListWebhooks._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_webhooks(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseListWebhooks._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseListWebhooks._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._ListWebhooks._get_response(
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
            resp = webhook.ListWebhooksResponse()
            pb_resp = webhook.ListWebhooksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_webhooks(resp)
            return resp

    class _UpdateWebhook(
        _BaseWebhooksRestTransport._BaseUpdateWebhook, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.UpdateWebhook")

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
            request: gcdc_webhook.UpdateWebhookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcdc_webhook.Webhook:
            r"""Call the update webhook method over HTTP.

            Args:
                request (~.gcdc_webhook.UpdateWebhookRequest):
                    The request object. The request message for
                [Webhooks.UpdateWebhook][google.cloud.dialogflow.cx.v3.Webhooks.UpdateWebhook].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcdc_webhook.Webhook:
                    Webhooks host the developer's
                business logic. During a session,
                webhooks allow the developer to use the
                data extracted by Dialogflow's natural
                language processing to generate dynamic
                responses, validate collected data, or
                trigger actions on the backend.

            """

            http_options = (
                _BaseWebhooksRestTransport._BaseUpdateWebhook._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_webhook(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseUpdateWebhook._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseWebhooksRestTransport._BaseUpdateWebhook._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseUpdateWebhook._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._UpdateWebhook._get_response(
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
            resp = gcdc_webhook.Webhook()
            pb_resp = gcdc_webhook.Webhook.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_webhook(resp)
            return resp

    @property
    def create_webhook(
        self,
    ) -> Callable[[gcdc_webhook.CreateWebhookRequest], gcdc_webhook.Webhook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWebhook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_webhook(
        self,
    ) -> Callable[[webhook.DeleteWebhookRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWebhook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_webhook(self) -> Callable[[webhook.GetWebhookRequest], webhook.Webhook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWebhook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_webhooks(
        self,
    ) -> Callable[[webhook.ListWebhooksRequest], webhook.ListWebhooksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWebhooks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_webhook(
        self,
    ) -> Callable[[gcdc_webhook.UpdateWebhookRequest], gcdc_webhook.Webhook]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWebhook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseWebhooksRestTransport._BaseGetLocation, WebhooksRestStub):
        def __hash__(self):
            return hash("WebhooksRestTransport.GetLocation")

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

            http_options = (
                _BaseWebhooksRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._GetLocation._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseWebhooksRestTransport._BaseListLocations, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.ListLocations")

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

            http_options = (
                _BaseWebhooksRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._ListLocations._get_response(
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

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseWebhooksRestTransport._BaseCancelOperation, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseWebhooksRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(_BaseWebhooksRestTransport._BaseGetOperation, WebhooksRestStub):
        def __hash__(self):
            return hash("WebhooksRestTransport.GetOperation")

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

            http_options = (
                _BaseWebhooksRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._GetOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseWebhooksRestTransport._BaseListOperations, WebhooksRestStub
    ):
        def __hash__(self):
            return hash("WebhooksRestTransport.ListOperations")

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
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseWebhooksRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseWebhooksRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseWebhooksRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = WebhooksRestTransport._ListOperations._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("WebhooksRestTransport",)
