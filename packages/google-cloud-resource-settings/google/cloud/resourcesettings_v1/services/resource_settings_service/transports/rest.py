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

from google.cloud.resourcesettings_v1.types import resource_settings

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseResourceSettingsServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ResourceSettingsServiceRestInterceptor:
    """Interceptor for ResourceSettingsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ResourceSettingsServiceRestTransport.

    .. code-block:: python
        class MyCustomResourceSettingsServiceInterceptor(ResourceSettingsServiceRestInterceptor):
            def pre_get_setting(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_setting(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_setting(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_setting(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ResourceSettingsServiceRestTransport(interceptor=MyCustomResourceSettingsServiceInterceptor())
        client = ResourceSettingsServiceClient(transport=transport)


    """

    def pre_get_setting(
        self,
        request: resource_settings.GetSettingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[resource_settings.GetSettingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_setting

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ResourceSettingsService server.
        """
        return request, metadata

    def post_get_setting(
        self, response: resource_settings.Setting
    ) -> resource_settings.Setting:
        """Post-rpc interceptor for get_setting

        Override in a subclass to manipulate the response
        after it is returned by the ResourceSettingsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_settings(
        self,
        request: resource_settings.ListSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[resource_settings.ListSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ResourceSettingsService server.
        """
        return request, metadata

    def post_list_settings(
        self, response: resource_settings.ListSettingsResponse
    ) -> resource_settings.ListSettingsResponse:
        """Post-rpc interceptor for list_settings

        Override in a subclass to manipulate the response
        after it is returned by the ResourceSettingsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_setting(
        self,
        request: resource_settings.UpdateSettingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[resource_settings.UpdateSettingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_setting

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ResourceSettingsService server.
        """
        return request, metadata

    def post_update_setting(
        self, response: resource_settings.Setting
    ) -> resource_settings.Setting:
        """Post-rpc interceptor for update_setting

        Override in a subclass to manipulate the response
        after it is returned by the ResourceSettingsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ResourceSettingsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ResourceSettingsServiceRestInterceptor


class ResourceSettingsServiceRestTransport(_BaseResourceSettingsServiceRestTransport):
    """REST backend synchronous transport for ResourceSettingsService.

    An interface to interact with resource settings and setting values
    throughout the resource hierarchy.

    Services may surface a number of settings for users to control how
    their resources behave. Values of settings applied on a given Cloud
    resource are evaluated hierarchically and inherited by all
    descendants of that resource.

    For all requests, returns a ``google.rpc.Status`` with
    ``google.rpc.Code.PERMISSION_DENIED`` if the IAM check fails or the
    ``parent`` resource is not in a Cloud Organization. For all
    requests, returns a ``google.rpc.Status`` with
    ``google.rpc.Code.INVALID_ARGUMENT`` if the request is malformed.
    (== deprecation_description Resource Settings is deprecated. As of
    November 7, 2023, no organizations will be onboarded for any of the
    enabled settings, and the service will be shut down on October 1,
    2024. ==)

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "resourcesettings.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ResourceSettingsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'resourcesettings.googleapis.com').
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
        self._interceptor = interceptor or ResourceSettingsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetSetting(
        _BaseResourceSettingsServiceRestTransport._BaseGetSetting,
        ResourceSettingsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ResourceSettingsServiceRestTransport.GetSetting")

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
            request: resource_settings.GetSettingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource_settings.Setting:
            r"""Call the get setting method over HTTP.

            Args:
                request (~.resource_settings.GetSettingRequest):
                    The request object. The request for GetSetting.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource_settings.Setting:
                    The schema for settings.
            """

            http_options = (
                _BaseResourceSettingsServiceRestTransport._BaseGetSetting._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_setting(request, metadata)
            transcoded_request = _BaseResourceSettingsServiceRestTransport._BaseGetSetting._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseResourceSettingsServiceRestTransport._BaseGetSetting._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ResourceSettingsServiceRestTransport._GetSetting._get_response(
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
            resp = resource_settings.Setting()
            pb_resp = resource_settings.Setting.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_setting(resp)
            return resp

    class _ListSettings(
        _BaseResourceSettingsServiceRestTransport._BaseListSettings,
        ResourceSettingsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ResourceSettingsServiceRestTransport.ListSettings")

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
            request: resource_settings.ListSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource_settings.ListSettingsResponse:
            r"""Call the list settings method over HTTP.

            Args:
                request (~.resource_settings.ListSettingsRequest):
                    The request object. The request for ListSettings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource_settings.ListSettingsResponse:
                    The response from ListSettings.
            """

            http_options = (
                _BaseResourceSettingsServiceRestTransport._BaseListSettings._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_settings(request, metadata)
            transcoded_request = _BaseResourceSettingsServiceRestTransport._BaseListSettings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseResourceSettingsServiceRestTransport._BaseListSettings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ResourceSettingsServiceRestTransport._ListSettings._get_response(
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
            resp = resource_settings.ListSettingsResponse()
            pb_resp = resource_settings.ListSettingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_settings(resp)
            return resp

    class _UpdateSetting(
        _BaseResourceSettingsServiceRestTransport._BaseUpdateSetting,
        ResourceSettingsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ResourceSettingsServiceRestTransport.UpdateSetting")

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
            request: resource_settings.UpdateSettingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource_settings.Setting:
            r"""Call the update setting method over HTTP.

            Args:
                request (~.resource_settings.UpdateSettingRequest):
                    The request object. The request for UpdateSetting.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource_settings.Setting:
                    The schema for settings.
            """

            http_options = (
                _BaseResourceSettingsServiceRestTransport._BaseUpdateSetting._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_setting(request, metadata)
            transcoded_request = _BaseResourceSettingsServiceRestTransport._BaseUpdateSetting._get_transcoded_request(
                http_options, request
            )

            body = _BaseResourceSettingsServiceRestTransport._BaseUpdateSetting._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseResourceSettingsServiceRestTransport._BaseUpdateSetting._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ResourceSettingsServiceRestTransport._UpdateSetting._get_response(
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
            resp = resource_settings.Setting()
            pb_resp = resource_settings.Setting.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_setting(resp)
            return resp

    @property
    def get_setting(
        self,
    ) -> Callable[[resource_settings.GetSettingRequest], resource_settings.Setting]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSetting(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_settings(
        self,
    ) -> Callable[
        [resource_settings.ListSettingsRequest], resource_settings.ListSettingsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_setting(
        self,
    ) -> Callable[[resource_settings.UpdateSettingRequest], resource_settings.Setting]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSetting(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ResourceSettingsServiceRestTransport",)
