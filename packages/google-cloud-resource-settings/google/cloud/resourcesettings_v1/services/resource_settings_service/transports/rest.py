# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.resourcesettings_v1.types import resource_settings

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import ResourceSettingsServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
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


class ResourceSettingsServiceRestTransport(ResourceSettingsServiceTransport):
    """REST backend transport for ResourceSettingsService.

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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ResourceSettingsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetSetting(ResourceSettingsServiceRestStub):
        def __hash__(self):
            return hash("GetSetting")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/settings/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/settings/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/settings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_setting(request, metadata)
            pb_request = resource_settings.GetSettingRequest.pb(request)
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
            resp = resource_settings.Setting()
            pb_resp = resource_settings.Setting.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_setting(resp)
            return resp

    class _ListSettings(ResourceSettingsServiceRestStub):
        def __hash__(self):
            return hash("ListSettings")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*}/settings",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*}/settings",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/settings",
                },
            ]
            request, metadata = self._interceptor.pre_list_settings(request, metadata)
            pb_request = resource_settings.ListSettingsRequest.pb(request)
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
            resp = resource_settings.ListSettingsResponse()
            pb_resp = resource_settings.ListSettingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_settings(resp)
            return resp

    class _UpdateSetting(ResourceSettingsServiceRestStub):
        def __hash__(self):
            return hash("UpdateSetting")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{setting.name=organizations/*/settings/*}",
                    "body": "setting",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{setting.name=folders/*/settings/*}",
                    "body": "setting",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{setting.name=projects/*/settings/*}",
                    "body": "setting",
                },
            ]
            request, metadata = self._interceptor.pre_update_setting(request, metadata)
            pb_request = resource_settings.UpdateSettingRequest.pb(request)
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
