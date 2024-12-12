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
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.advisorynotifications_v1.types import service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAdvisoryNotificationsServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class AdvisoryNotificationsServiceRestInterceptor:
    """Interceptor for AdvisoryNotificationsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AdvisoryNotificationsServiceRestTransport.

    .. code-block:: python
        class MyCustomAdvisoryNotificationsServiceInterceptor(AdvisoryNotificationsServiceRestInterceptor):
            def pre_get_notification(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_notification(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_notifications(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_notifications(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AdvisoryNotificationsServiceRestTransport(interceptor=MyCustomAdvisoryNotificationsServiceInterceptor())
        client = AdvisoryNotificationsServiceClient(transport=transport)


    """

    def pre_get_notification(
        self,
        request: service.GetNotificationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetNotificationRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_notification

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AdvisoryNotificationsService server.
        """
        return request, metadata

    def post_get_notification(
        self, response: service.Notification
    ) -> service.Notification:
        """Post-rpc interceptor for get_notification

        Override in a subclass to manipulate the response
        after it is returned by the AdvisoryNotificationsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_settings(
        self,
        request: service.GetSettingsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.GetSettingsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AdvisoryNotificationsService server.
        """
        return request, metadata

    def post_get_settings(self, response: service.Settings) -> service.Settings:
        """Post-rpc interceptor for get_settings

        Override in a subclass to manipulate the response
        after it is returned by the AdvisoryNotificationsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_notifications(
        self,
        request: service.ListNotificationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        service.ListNotificationsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for list_notifications

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AdvisoryNotificationsService server.
        """
        return request, metadata

    def post_list_notifications(
        self, response: service.ListNotificationsResponse
    ) -> service.ListNotificationsResponse:
        """Post-rpc interceptor for list_notifications

        Override in a subclass to manipulate the response
        after it is returned by the AdvisoryNotificationsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_settings(
        self,
        request: service.UpdateSettingsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[service.UpdateSettingsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AdvisoryNotificationsService server.
        """
        return request, metadata

    def post_update_settings(self, response: service.Settings) -> service.Settings:
        """Post-rpc interceptor for update_settings

        Override in a subclass to manipulate the response
        after it is returned by the AdvisoryNotificationsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AdvisoryNotificationsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AdvisoryNotificationsServiceRestInterceptor


class AdvisoryNotificationsServiceRestTransport(
    _BaseAdvisoryNotificationsServiceRestTransport
):
    """REST backend synchronous transport for AdvisoryNotificationsService.

    Service to manage Security and Privacy Notifications.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "advisorynotifications.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AdvisoryNotificationsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'advisorynotifications.googleapis.com').
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
        self._interceptor = interceptor or AdvisoryNotificationsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetNotification(
        _BaseAdvisoryNotificationsServiceRestTransport._BaseGetNotification,
        AdvisoryNotificationsServiceRestStub,
    ):
        def __hash__(self):
            return hash("AdvisoryNotificationsServiceRestTransport.GetNotification")

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
            request: service.GetNotificationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Notification:
            r"""Call the get notification method over HTTP.

            Args:
                request (~.service.GetNotificationRequest):
                    The request object. Request for fetching a notification.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Notification:
                    A notification object for notifying
                customers about security and privacy
                issues.

            """

            http_options = (
                _BaseAdvisoryNotificationsServiceRestTransport._BaseGetNotification._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_notification(
                request, metadata
            )
            transcoded_request = _BaseAdvisoryNotificationsServiceRestTransport._BaseGetNotification._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAdvisoryNotificationsServiceRestTransport._BaseGetNotification._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.GetNotification",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "GetNotification",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AdvisoryNotificationsServiceRestTransport._GetNotification._get_response(
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
            resp = service.Notification()
            pb_resp = service.Notification.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_notification(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Notification.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.get_notification",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "GetNotification",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _GetSettings(
        _BaseAdvisoryNotificationsServiceRestTransport._BaseGetSettings,
        AdvisoryNotificationsServiceRestStub,
    ):
        def __hash__(self):
            return hash("AdvisoryNotificationsServiceRestTransport.GetSettings")

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
            request: service.GetSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Settings:
            r"""Call the get settings method over HTTP.

            Args:
                request (~.service.GetSettingsRequest):
                    The request object. Request of GetSettings endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Settings:
                    Settings for Advisory Notifications.
            """

            http_options = (
                _BaseAdvisoryNotificationsServiceRestTransport._BaseGetSettings._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_settings(request, metadata)
            transcoded_request = _BaseAdvisoryNotificationsServiceRestTransport._BaseGetSettings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAdvisoryNotificationsServiceRestTransport._BaseGetSettings._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.GetSettings",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "GetSettings",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AdvisoryNotificationsServiceRestTransport._GetSettings._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.Settings()
            pb_resp = service.Settings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_settings(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Settings.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.get_settings",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "GetSettings",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListNotifications(
        _BaseAdvisoryNotificationsServiceRestTransport._BaseListNotifications,
        AdvisoryNotificationsServiceRestStub,
    ):
        def __hash__(self):
            return hash("AdvisoryNotificationsServiceRestTransport.ListNotifications")

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
            request: service.ListNotificationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.ListNotificationsResponse:
            r"""Call the list notifications method over HTTP.

            Args:
                request (~.service.ListNotificationsRequest):
                    The request object. Request for fetching all
                notifications for a given parent.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.ListNotificationsResponse:
                    Response of ListNotifications
                endpoint.

            """

            http_options = (
                _BaseAdvisoryNotificationsServiceRestTransport._BaseListNotifications._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_notifications(
                request, metadata
            )
            transcoded_request = _BaseAdvisoryNotificationsServiceRestTransport._BaseListNotifications._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAdvisoryNotificationsServiceRestTransport._BaseListNotifications._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.ListNotifications",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "ListNotifications",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = AdvisoryNotificationsServiceRestTransport._ListNotifications._get_response(
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
            resp = service.ListNotificationsResponse()
            pb_resp = service.ListNotificationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_notifications(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.ListNotificationsResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.list_notifications",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "ListNotifications",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateSettings(
        _BaseAdvisoryNotificationsServiceRestTransport._BaseUpdateSettings,
        AdvisoryNotificationsServiceRestStub,
    ):
        def __hash__(self):
            return hash("AdvisoryNotificationsServiceRestTransport.UpdateSettings")

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
            request: service.UpdateSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> service.Settings:
            r"""Call the update settings method over HTTP.

            Args:
                request (~.service.UpdateSettingsRequest):
                    The request object. Request of UpdateSettings endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.service.Settings:
                    Settings for Advisory Notifications.
            """

            http_options = (
                _BaseAdvisoryNotificationsServiceRestTransport._BaseUpdateSettings._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_settings(request, metadata)
            transcoded_request = _BaseAdvisoryNotificationsServiceRestTransport._BaseUpdateSettings._get_transcoded_request(
                http_options, request
            )

            body = _BaseAdvisoryNotificationsServiceRestTransport._BaseUpdateSettings._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAdvisoryNotificationsServiceRestTransport._BaseUpdateSettings._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.UpdateSettings",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "UpdateSettings",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                AdvisoryNotificationsServiceRestTransport._UpdateSettings._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.Settings()
            pb_resp = service.Settings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_settings(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = service.Settings.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.advisorynotifications_v1.AdvisoryNotificationsServiceClient.update_settings",
                    extra={
                        "serviceName": "google.cloud.advisorynotifications.v1.AdvisoryNotificationsService",
                        "rpcName": "UpdateSettings",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get_notification(
        self,
    ) -> Callable[[service.GetNotificationRequest], service.Notification]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNotification(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_settings(self) -> Callable[[service.GetSettingsRequest], service.Settings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_notifications(
        self,
    ) -> Callable[
        [service.ListNotificationsRequest], service.ListNotificationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNotifications(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_settings(
        self,
    ) -> Callable[[service.UpdateSettingsRequest], service.Settings]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AdvisoryNotificationsServiceRestTransport",)
