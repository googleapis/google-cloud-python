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


from google.cloud.support_v2.types import case
from google.cloud.support_v2.types import case as gcs_case
from google.cloud.support_v2.types import case_service

from .base import CaseServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CaseServiceRestInterceptor:
    """Interceptor for CaseService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CaseServiceRestTransport.

    .. code-block:: python
        class MyCustomCaseServiceInterceptor(CaseServiceRestInterceptor):
            def pre_close_case(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_close_case(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_case(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_case(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_escalate_case(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_escalate_case(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_case(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_case(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_case_classifications(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_case_classifications(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_cases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_cases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_case(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_case(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CaseServiceRestTransport(interceptor=MyCustomCaseServiceInterceptor())
        client = CaseServiceClient(transport=transport)


    """

    def pre_close_case(
        self,
        request: case_service.CloseCaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.CloseCaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for close_case

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_close_case(self, response: case.Case) -> case.Case:
        """Post-rpc interceptor for close_case

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_create_case(
        self,
        request: case_service.CreateCaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.CreateCaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_case

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_create_case(self, response: gcs_case.Case) -> gcs_case.Case:
        """Post-rpc interceptor for create_case

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_escalate_case(
        self,
        request: case_service.EscalateCaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.EscalateCaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for escalate_case

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_escalate_case(self, response: case.Case) -> case.Case:
        """Post-rpc interceptor for escalate_case

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_get_case(
        self, request: case_service.GetCaseRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[case_service.GetCaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_case

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_get_case(self, response: case.Case) -> case.Case:
        """Post-rpc interceptor for get_case

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_list_cases(
        self,
        request: case_service.ListCasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.ListCasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_cases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_list_cases(
        self, response: case_service.ListCasesResponse
    ) -> case_service.ListCasesResponse:
        """Post-rpc interceptor for list_cases

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_search_case_classifications(
        self,
        request: case_service.SearchCaseClassificationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        case_service.SearchCaseClassificationsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_case_classifications

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_search_case_classifications(
        self, response: case_service.SearchCaseClassificationsResponse
    ) -> case_service.SearchCaseClassificationsResponse:
        """Post-rpc interceptor for search_case_classifications

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_search_cases(
        self,
        request: case_service.SearchCasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.SearchCasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_cases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_search_cases(
        self, response: case_service.SearchCasesResponse
    ) -> case_service.SearchCasesResponse:
        """Post-rpc interceptor for search_cases

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response

    def pre_update_case(
        self,
        request: case_service.UpdateCaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[case_service.UpdateCaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_case

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CaseService server.
        """
        return request, metadata

    def post_update_case(self, response: gcs_case.Case) -> gcs_case.Case:
        """Post-rpc interceptor for update_case

        Override in a subclass to manipulate the response
        after it is returned by the CaseService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CaseServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CaseServiceRestInterceptor


class CaseServiceRestTransport(CaseServiceTransport):
    """REST backend transport for CaseService.

    A service to manage Google Cloud support cases.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudsupport.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CaseServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudsupport.googleapis.com').
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
        self._interceptor = interceptor or CaseServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CloseCase(CaseServiceRestStub):
        def __hash__(self):
            return hash("CloseCase")

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
            request: case_service.CloseCaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case.Case:
            r"""Call the close case method over HTTP.

            Args:
                request (~.case_service.CloseCaseRequest):
                    The request object. The request message for the CloseCase
                endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.case.Case:
                    A support case.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/cases/*}:close",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/cases/*}:close",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_close_case(request, metadata)
            pb_request = case_service.CloseCaseRequest.pb(request)
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
            resp = case.Case()
            pb_resp = case.Case.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_close_case(resp)
            return resp

    class _CreateCase(CaseServiceRestStub):
        def __hash__(self):
            return hash("CreateCase")

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
            request: case_service.CreateCaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_case.Case:
            r"""Call the create case method over HTTP.

            Args:
                request (~.case_service.CreateCaseRequest):
                    The request object. The request message for the
                CreateCase endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_case.Case:
                    A support case.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/cases",
                    "body": "case",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/cases",
                    "body": "case",
                },
            ]
            request, metadata = self._interceptor.pre_create_case(request, metadata)
            pb_request = case_service.CreateCaseRequest.pb(request)
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
            resp = gcs_case.Case()
            pb_resp = gcs_case.Case.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_case(resp)
            return resp

    class _EscalateCase(CaseServiceRestStub):
        def __hash__(self):
            return hash("EscalateCase")

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
            request: case_service.EscalateCaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case.Case:
            r"""Call the escalate case method over HTTP.

            Args:
                request (~.case_service.EscalateCaseRequest):
                    The request object. The request message for the
                EscalateCase endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.case.Case:
                    A support case.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/cases/*}:escalate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/cases/*}:escalate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_escalate_case(request, metadata)
            pb_request = case_service.EscalateCaseRequest.pb(request)
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
            resp = case.Case()
            pb_resp = case.Case.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_escalate_case(resp)
            return resp

    class _GetCase(CaseServiceRestStub):
        def __hash__(self):
            return hash("GetCase")

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
            request: case_service.GetCaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case.Case:
            r"""Call the get case method over HTTP.

            Args:
                request (~.case_service.GetCaseRequest):
                    The request object. The request message for the GetCase
                endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.case.Case:
                    A support case.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/cases/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/cases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_case(request, metadata)
            pb_request = case_service.GetCaseRequest.pb(request)
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
            resp = case.Case()
            pb_resp = case.Case.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_case(resp)
            return resp

    class _ListCases(CaseServiceRestStub):
        def __hash__(self):
            return hash("ListCases")

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
            request: case_service.ListCasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case_service.ListCasesResponse:
            r"""Call the list cases method over HTTP.

            Args:
                request (~.case_service.ListCasesRequest):
                    The request object. The request message for the ListCases
                endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.case_service.ListCasesResponse:
                    The response message for the
                ListCases endpoint.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/cases",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/cases",
                },
            ]
            request, metadata = self._interceptor.pre_list_cases(request, metadata)
            pb_request = case_service.ListCasesRequest.pb(request)
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
            resp = case_service.ListCasesResponse()
            pb_resp = case_service.ListCasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_cases(resp)
            return resp

    class _SearchCaseClassifications(CaseServiceRestStub):
        def __hash__(self):
            return hash("SearchCaseClassifications")

        def __call__(
            self,
            request: case_service.SearchCaseClassificationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case_service.SearchCaseClassificationsResponse:
            r"""Call the search case
            classifications method over HTTP.

                Args:
                    request (~.case_service.SearchCaseClassificationsRequest):
                        The request object. The request message for
                    SearchCaseClassifications endpoint.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.case_service.SearchCaseClassificationsResponse:
                        The response message for
                    SearchCaseClassifications endpoint.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/caseClassifications:search",
                },
            ]
            request, metadata = self._interceptor.pre_search_case_classifications(
                request, metadata
            )
            pb_request = case_service.SearchCaseClassificationsRequest.pb(request)
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
            resp = case_service.SearchCaseClassificationsResponse()
            pb_resp = case_service.SearchCaseClassificationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_case_classifications(resp)
            return resp

    class _SearchCases(CaseServiceRestStub):
        def __hash__(self):
            return hash("SearchCases")

        def __call__(
            self,
            request: case_service.SearchCasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> case_service.SearchCasesResponse:
            r"""Call the search cases method over HTTP.

            Args:
                request (~.case_service.SearchCasesRequest):
                    The request object. The request message for the
                SearchCases endpoint.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.case_service.SearchCasesResponse:
                    The response message for the
                SearchCases endpoint.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/cases:search",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/cases:search",
                },
            ]
            request, metadata = self._interceptor.pre_search_cases(request, metadata)
            pb_request = case_service.SearchCasesRequest.pb(request)
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
            resp = case_service.SearchCasesResponse()
            pb_resp = case_service.SearchCasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_cases(resp)
            return resp

    class _UpdateCase(CaseServiceRestStub):
        def __hash__(self):
            return hash("UpdateCase")

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
            request: case_service.UpdateCaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_case.Case:
            r"""Call the update case method over HTTP.

            Args:
                request (~.case_service.UpdateCaseRequest):
                    The request object. The request message for the
                UpdateCase endpoint
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_case.Case:
                    A support case.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{case.name=projects/*/cases/*}",
                    "body": "case",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{case.name=organizations/*/cases/*}",
                    "body": "case",
                },
            ]
            request, metadata = self._interceptor.pre_update_case(request, metadata)
            pb_request = case_service.UpdateCaseRequest.pb(request)
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
            resp = gcs_case.Case()
            pb_resp = gcs_case.Case.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_case(resp)
            return resp

    @property
    def close_case(self) -> Callable[[case_service.CloseCaseRequest], case.Case]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CloseCase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_case(self) -> Callable[[case_service.CreateCaseRequest], gcs_case.Case]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def escalate_case(self) -> Callable[[case_service.EscalateCaseRequest], case.Case]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EscalateCase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_case(self) -> Callable[[case_service.GetCaseRequest], case.Case]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cases(
        self,
    ) -> Callable[[case_service.ListCasesRequest], case_service.ListCasesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_case_classifications(
        self,
    ) -> Callable[
        [case_service.SearchCaseClassificationsRequest],
        case_service.SearchCaseClassificationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchCaseClassifications(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_cases(
        self,
    ) -> Callable[[case_service.SearchCasesRequest], case_service.SearchCasesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchCases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_case(self) -> Callable[[case_service.UpdateCaseRequest], gcs_case.Case]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCase(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CaseServiceRestTransport",)
