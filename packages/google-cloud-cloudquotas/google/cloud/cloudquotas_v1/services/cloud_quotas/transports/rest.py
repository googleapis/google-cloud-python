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


from google.cloud.cloudquotas_v1.types import cloudquotas, resources

from .base import CloudQuotasTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CloudQuotasRestInterceptor:
    """Interceptor for CloudQuotas.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudQuotasRestTransport.

    .. code-block:: python
        class MyCustomCloudQuotasInterceptor(CloudQuotasRestInterceptor):
            def pre_create_quota_preference(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_quota_preference(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_quota_info(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_quota_info(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_quota_preference(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_quota_preference(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_quota_infos(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_quota_infos(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_quota_preferences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_quota_preferences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_quota_preference(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_quota_preference(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudQuotasRestTransport(interceptor=MyCustomCloudQuotasInterceptor())
        client = CloudQuotasClient(transport=transport)


    """

    def pre_create_quota_preference(
        self,
        request: cloudquotas.CreateQuotaPreferenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.CreateQuotaPreferenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_quota_preference

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_create_quota_preference(
        self, response: resources.QuotaPreference
    ) -> resources.QuotaPreference:
        """Post-rpc interceptor for create_quota_preference

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response

    def pre_get_quota_info(
        self,
        request: cloudquotas.GetQuotaInfoRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.GetQuotaInfoRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_quota_info

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_get_quota_info(self, response: resources.QuotaInfo) -> resources.QuotaInfo:
        """Post-rpc interceptor for get_quota_info

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response

    def pre_get_quota_preference(
        self,
        request: cloudquotas.GetQuotaPreferenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.GetQuotaPreferenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_quota_preference

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_get_quota_preference(
        self, response: resources.QuotaPreference
    ) -> resources.QuotaPreference:
        """Post-rpc interceptor for get_quota_preference

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response

    def pre_list_quota_infos(
        self,
        request: cloudquotas.ListQuotaInfosRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.ListQuotaInfosRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_quota_infos

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_list_quota_infos(
        self, response: cloudquotas.ListQuotaInfosResponse
    ) -> cloudquotas.ListQuotaInfosResponse:
        """Post-rpc interceptor for list_quota_infos

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response

    def pre_list_quota_preferences(
        self,
        request: cloudquotas.ListQuotaPreferencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.ListQuotaPreferencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_quota_preferences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_list_quota_preferences(
        self, response: cloudquotas.ListQuotaPreferencesResponse
    ) -> cloudquotas.ListQuotaPreferencesResponse:
        """Post-rpc interceptor for list_quota_preferences

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response

    def pre_update_quota_preference(
        self,
        request: cloudquotas.UpdateQuotaPreferenceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudquotas.UpdateQuotaPreferenceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_quota_preference

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudQuotas server.
        """
        return request, metadata

    def post_update_quota_preference(
        self, response: resources.QuotaPreference
    ) -> resources.QuotaPreference:
        """Post-rpc interceptor for update_quota_preference

        Override in a subclass to manipulate the response
        after it is returned by the CloudQuotas server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudQuotasRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudQuotasRestInterceptor


class CloudQuotasRestTransport(CloudQuotasTransport):
    """REST backend transport for CloudQuotas.

    The Cloud Quotas API is an infrastructure service for Google
    Cloud that lets service consumers list and manage their resource
    usage limits.

    - List/Get the metadata and current status of the quotas for a
      service.
    - Create/Update quota preferencess that declare the preferred
      quota values.
    - Check the status of a quota preference request.
    - List/Get pending and historical quota preference.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudquotas.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudQuotasRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudquotas.googleapis.com').
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
        self._interceptor = interceptor or CloudQuotasRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateQuotaPreference(CloudQuotasRestStub):
        def __hash__(self):
            return hash("CreateQuotaPreference")

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
            request: cloudquotas.CreateQuotaPreferenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.QuotaPreference:
            r"""Call the create quota preference method over HTTP.

            Args:
                request (~.cloudquotas.CreateQuotaPreferenceRequest):
                    The request object. Message for creating a
                QuotaPreference
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.QuotaPreference:
                    QuotaPreference represents the
                preferred quota configuration specified
                for a project, folder or organization.
                There is only one QuotaPreference
                resource for a quota value targeting a
                unique set of dimensions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/quotaPreferences",
                    "body": "quota_preference",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=folders/*/locations/*}/quotaPreferences",
                    "body": "quota_preference",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=organizations/*/locations/*}/quotaPreferences",
                    "body": "quota_preference",
                },
            ]
            request, metadata = self._interceptor.pre_create_quota_preference(
                request, metadata
            )
            pb_request = cloudquotas.CreateQuotaPreferenceRequest.pb(request)
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
            resp = resources.QuotaPreference()
            pb_resp = resources.QuotaPreference.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_quota_preference(resp)
            return resp

    class _GetQuotaInfo(CloudQuotasRestStub):
        def __hash__(self):
            return hash("GetQuotaInfo")

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
            request: cloudquotas.GetQuotaInfoRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.QuotaInfo:
            r"""Call the get quota info method over HTTP.

            Args:
                request (~.cloudquotas.GetQuotaInfoRequest):
                    The request object. Message for getting a QuotaInfo
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.QuotaInfo:
                    QuotaInfo represents information
                about a particular quota for a given
                project, folder or organization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/services/*/quotaInfos/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/services/*/quotaInfos/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/services/*/quotaInfos/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_quota_info(request, metadata)
            pb_request = cloudquotas.GetQuotaInfoRequest.pb(request)
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
            resp = resources.QuotaInfo()
            pb_resp = resources.QuotaInfo.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_quota_info(resp)
            return resp

    class _GetQuotaPreference(CloudQuotasRestStub):
        def __hash__(self):
            return hash("GetQuotaPreference")

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
            request: cloudquotas.GetQuotaPreferenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.QuotaPreference:
            r"""Call the get quota preference method over HTTP.

            Args:
                request (~.cloudquotas.GetQuotaPreferenceRequest):
                    The request object. Message for getting a QuotaPreference
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.QuotaPreference:
                    QuotaPreference represents the
                preferred quota configuration specified
                for a project, folder or organization.
                There is only one QuotaPreference
                resource for a quota value targeting a
                unique set of dimensions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/quotaPreferences/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=organizations/*/locations/*/quotaPreferences/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=folders/*/locations/*/quotaPreferences/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_quota_preference(
                request, metadata
            )
            pb_request = cloudquotas.GetQuotaPreferenceRequest.pb(request)
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
            resp = resources.QuotaPreference()
            pb_resp = resources.QuotaPreference.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_quota_preference(resp)
            return resp

    class _ListQuotaInfos(CloudQuotasRestStub):
        def __hash__(self):
            return hash("ListQuotaInfos")

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
            request: cloudquotas.ListQuotaInfosRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudquotas.ListQuotaInfosResponse:
            r"""Call the list quota infos method over HTTP.

            Args:
                request (~.cloudquotas.ListQuotaInfosRequest):
                    The request object. Message for requesting list of
                QuotaInfos
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudquotas.ListQuotaInfosResponse:
                    Message for response to listing
                QuotaInfos

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/services/*}/quotaInfos",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*/services/*}/quotaInfos",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*/services/*}/quotaInfos",
                },
            ]
            request, metadata = self._interceptor.pre_list_quota_infos(
                request, metadata
            )
            pb_request = cloudquotas.ListQuotaInfosRequest.pb(request)
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
            resp = cloudquotas.ListQuotaInfosResponse()
            pb_resp = cloudquotas.ListQuotaInfosResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_quota_infos(resp)
            return resp

    class _ListQuotaPreferences(CloudQuotasRestStub):
        def __hash__(self):
            return hash("ListQuotaPreferences")

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
            request: cloudquotas.ListQuotaPreferencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudquotas.ListQuotaPreferencesResponse:
            r"""Call the list quota preferences method over HTTP.

            Args:
                request (~.cloudquotas.ListQuotaPreferencesRequest):
                    The request object. Message for requesting list of
                QuotaPreferences
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudquotas.ListQuotaPreferencesResponse:
                    Message for response to listing
                QuotaPreferences

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/quotaPreferences",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=folders/*/locations/*}/quotaPreferences",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=organizations/*/locations/*}/quotaPreferences",
                },
            ]
            request, metadata = self._interceptor.pre_list_quota_preferences(
                request, metadata
            )
            pb_request = cloudquotas.ListQuotaPreferencesRequest.pb(request)
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
            resp = cloudquotas.ListQuotaPreferencesResponse()
            pb_resp = cloudquotas.ListQuotaPreferencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_quota_preferences(resp)
            return resp

    class _UpdateQuotaPreference(CloudQuotasRestStub):
        def __hash__(self):
            return hash("UpdateQuotaPreference")

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
            request: cloudquotas.UpdateQuotaPreferenceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.QuotaPreference:
            r"""Call the update quota preference method over HTTP.

            Args:
                request (~.cloudquotas.UpdateQuotaPreferenceRequest):
                    The request object. Message for updating a
                QuotaPreference
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.QuotaPreference:
                    QuotaPreference represents the
                preferred quota configuration specified
                for a project, folder or organization.
                There is only one QuotaPreference
                resource for a quota value targeting a
                unique set of dimensions.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{quota_preference.name=projects/*/locations/*/quotaPreferences/*}",
                    "body": "quota_preference",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{quota_preference.name=folders/*/locations/*/quotaPreferences/*}",
                    "body": "quota_preference",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{quota_preference.name=organizations/*/locations/*/quotaPreferences/*}",
                    "body": "quota_preference",
                },
            ]
            request, metadata = self._interceptor.pre_update_quota_preference(
                request, metadata
            )
            pb_request = cloudquotas.UpdateQuotaPreferenceRequest.pb(request)
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
            resp = resources.QuotaPreference()
            pb_resp = resources.QuotaPreference.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_quota_preference(resp)
            return resp

    @property
    def create_quota_preference(
        self,
    ) -> Callable[
        [cloudquotas.CreateQuotaPreferenceRequest], resources.QuotaPreference
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateQuotaPreference(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_quota_info(
        self,
    ) -> Callable[[cloudquotas.GetQuotaInfoRequest], resources.QuotaInfo]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetQuotaInfo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_quota_preference(
        self,
    ) -> Callable[[cloudquotas.GetQuotaPreferenceRequest], resources.QuotaPreference]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetQuotaPreference(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_quota_infos(
        self,
    ) -> Callable[
        [cloudquotas.ListQuotaInfosRequest], cloudquotas.ListQuotaInfosResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListQuotaInfos(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_quota_preferences(
        self,
    ) -> Callable[
        [cloudquotas.ListQuotaPreferencesRequest],
        cloudquotas.ListQuotaPreferencesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListQuotaPreferences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_quota_preference(
        self,
    ) -> Callable[
        [cloudquotas.UpdateQuotaPreferenceRequest], resources.QuotaPreference
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateQuotaPreference(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudQuotasRestTransport",)
