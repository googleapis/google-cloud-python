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


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.retail_v2.types import (
    generative_question,
    generative_question_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import GenerativeQuestionServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class GenerativeQuestionServiceRestInterceptor:
    """Interceptor for GenerativeQuestionService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the GenerativeQuestionServiceRestTransport.

    .. code-block:: python
        class MyCustomGenerativeQuestionServiceInterceptor(GenerativeQuestionServiceRestInterceptor):
            def pre_batch_update_generative_question_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_generative_question_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_generative_questions_feature_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_generative_questions_feature_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_generative_question_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_generative_question_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_generative_question_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_generative_question_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_generative_questions_feature_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_generative_questions_feature_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = GenerativeQuestionServiceRestTransport(interceptor=MyCustomGenerativeQuestionServiceInterceptor())
        client = GenerativeQuestionServiceClient(transport=transport)


    """

    def pre_batch_update_generative_question_configs(
        self,
        request: generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for batch_update_generative_question_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_batch_update_generative_question_configs(
        self,
        response: generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse,
    ) -> generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse:
        """Post-rpc interceptor for batch_update_generative_question_configs

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_get_generative_questions_feature_config(
        self,
        request: generative_question_service.GetGenerativeQuestionsFeatureConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        generative_question_service.GetGenerativeQuestionsFeatureConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_generative_questions_feature_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_get_generative_questions_feature_config(
        self, response: generative_question.GenerativeQuestionsFeatureConfig
    ) -> generative_question.GenerativeQuestionsFeatureConfig:
        """Post-rpc interceptor for get_generative_questions_feature_config

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_list_generative_question_configs(
        self,
        request: generative_question_service.ListGenerativeQuestionConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        generative_question_service.ListGenerativeQuestionConfigsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_generative_question_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_list_generative_question_configs(
        self,
        response: generative_question_service.ListGenerativeQuestionConfigsResponse,
    ) -> generative_question_service.ListGenerativeQuestionConfigsResponse:
        """Post-rpc interceptor for list_generative_question_configs

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_update_generative_question_config(
        self,
        request: generative_question_service.UpdateGenerativeQuestionConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        generative_question_service.UpdateGenerativeQuestionConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_generative_question_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_update_generative_question_config(
        self, response: generative_question.GenerativeQuestionConfig
    ) -> generative_question.GenerativeQuestionConfig:
        """Post-rpc interceptor for update_generative_question_config

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_update_generative_questions_feature_config(
        self,
        request: generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_generative_questions_feature_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_update_generative_questions_feature_config(
        self, response: generative_question.GenerativeQuestionsFeatureConfig
    ) -> generative_question.GenerativeQuestionsFeatureConfig:
        """Post-rpc interceptor for update_generative_questions_feature_config

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
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
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
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
        before they are sent to the GenerativeQuestionService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the GenerativeQuestionService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class GenerativeQuestionServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: GenerativeQuestionServiceRestInterceptor


class GenerativeQuestionServiceRestTransport(GenerativeQuestionServiceTransport):
    """REST backend transport for GenerativeQuestionService.

    Service for managing LLM generated questions in search
    serving.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "retail.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[GenerativeQuestionServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'retail.googleapis.com').
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
        self._interceptor = interceptor or GenerativeQuestionServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchUpdateGenerativeQuestionConfigs(GenerativeQuestionServiceRestStub):
        def __hash__(self):
            return hash("BatchUpdateGenerativeQuestionConfigs")

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
            request: generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse:
            r"""Call the batch update generative
            question configs method over HTTP.

                Args:
                    request (~.generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest):
                        The request object. Request for
                    BatchUpdateGenerativeQuestionConfig
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse:
                        Aggregated response for
                    UpdateGenerativeQuestionConfig method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*/catalogs/*}/generativeQuestion:batchUpdate",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_batch_update_generative_question_configs(
                request, metadata
            )
            pb_request = generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest.pb(
                request
            )
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
            resp = (
                generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse()
            )
            pb_resp = generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_generative_question_configs(resp)
            return resp

    class _GetGenerativeQuestionsFeatureConfig(GenerativeQuestionServiceRestStub):
        def __hash__(self):
            return hash("GetGenerativeQuestionsFeatureConfig")

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
            request: generative_question_service.GetGenerativeQuestionsFeatureConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> generative_question.GenerativeQuestionsFeatureConfig:
            r"""Call the get generative questions
            feature config method over HTTP.

                Args:
                    request (~.generative_question_service.GetGenerativeQuestionsFeatureConfigRequest):
                        The request object. Request for
                    GetGenerativeQuestionsFeatureConfig
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.generative_question.GenerativeQuestionsFeatureConfig:
                        Configuration for overall generative
                    question feature state.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{catalog=projects/*/locations/*/catalogs/*}/generativeQuestionFeature",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_generative_questions_feature_config(
                request, metadata
            )
            pb_request = generative_question_service.GetGenerativeQuestionsFeatureConfigRequest.pb(
                request
            )
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
            resp = generative_question.GenerativeQuestionsFeatureConfig()
            pb_resp = generative_question.GenerativeQuestionsFeatureConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_generative_questions_feature_config(resp)
            return resp

    class _ListGenerativeQuestionConfigs(GenerativeQuestionServiceRestStub):
        def __hash__(self):
            return hash("ListGenerativeQuestionConfigs")

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
            request: generative_question_service.ListGenerativeQuestionConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> generative_question_service.ListGenerativeQuestionConfigsResponse:
            r"""Call the list generative question
            configs method over HTTP.

                Args:
                    request (~.generative_question_service.ListGenerativeQuestionConfigsRequest):
                        The request object. Request for ListQuestions method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.generative_question_service.ListGenerativeQuestionConfigsResponse:
                        Response for ListQuestions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/catalogs/*}/generativeQuestions",
                },
            ]
            request, metadata = self._interceptor.pre_list_generative_question_configs(
                request, metadata
            )
            pb_request = (
                generative_question_service.ListGenerativeQuestionConfigsRequest.pb(
                    request
                )
            )
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
            resp = generative_question_service.ListGenerativeQuestionConfigsResponse()
            pb_resp = (
                generative_question_service.ListGenerativeQuestionConfigsResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_generative_question_configs(resp)
            return resp

    class _UpdateGenerativeQuestionConfig(GenerativeQuestionServiceRestStub):
        def __hash__(self):
            return hash("UpdateGenerativeQuestionConfig")

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
            request: generative_question_service.UpdateGenerativeQuestionConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> generative_question.GenerativeQuestionConfig:
            r"""Call the update generative
            question config method over HTTP.

                Args:
                    request (~.generative_question_service.UpdateGenerativeQuestionConfigRequest):
                        The request object. Request for
                    UpdateGenerativeQuestionConfig method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.generative_question.GenerativeQuestionConfig:
                        Configuration for a single generated
                    question.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{generative_question_config.catalog=projects/*/locations/*/catalogs/*}/generativeQuestion",
                    "body": "generative_question_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_generative_question_config(
                request, metadata
            )
            pb_request = (
                generative_question_service.UpdateGenerativeQuestionConfigRequest.pb(
                    request
                )
            )
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
            resp = generative_question.GenerativeQuestionConfig()
            pb_resp = generative_question.GenerativeQuestionConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_generative_question_config(resp)
            return resp

    class _UpdateGenerativeQuestionsFeatureConfig(GenerativeQuestionServiceRestStub):
        def __hash__(self):
            return hash("UpdateGenerativeQuestionsFeatureConfig")

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
            request: generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> generative_question.GenerativeQuestionsFeatureConfig:
            r"""Call the update generative
            questions feature config method over HTTP.

                Args:
                    request (~.generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest):
                        The request object. Request for
                    UpdateGenerativeQuestionsFeatureConfig
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.generative_question.GenerativeQuestionsFeatureConfig:
                        Configuration for overall generative
                    question feature state.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{generative_questions_feature_config.catalog=projects/*/locations/*/catalogs/*}/generativeQuestionFeature",
                    "body": "generative_questions_feature_config",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_generative_questions_feature_config(
                request, metadata
            )
            pb_request = generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest.pb(
                request
            )
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
            resp = generative_question.GenerativeQuestionsFeatureConfig()
            pb_resp = generative_question.GenerativeQuestionsFeatureConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_generative_questions_feature_config(
                resp
            )
            return resp

    @property
    def batch_update_generative_question_configs(
        self,
    ) -> Callable[
        [generative_question_service.BatchUpdateGenerativeQuestionConfigsRequest],
        generative_question_service.BatchUpdateGenerativeQuestionConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateGenerativeQuestionConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_generative_questions_feature_config(
        self,
    ) -> Callable[
        [generative_question_service.GetGenerativeQuestionsFeatureConfigRequest],
        generative_question.GenerativeQuestionsFeatureConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGenerativeQuestionsFeatureConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_generative_question_configs(
        self,
    ) -> Callable[
        [generative_question_service.ListGenerativeQuestionConfigsRequest],
        generative_question_service.ListGenerativeQuestionConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGenerativeQuestionConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_generative_question_config(
        self,
    ) -> Callable[
        [generative_question_service.UpdateGenerativeQuestionConfigRequest],
        generative_question.GenerativeQuestionConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGenerativeQuestionConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_generative_questions_feature_config(
        self,
    ) -> Callable[
        [generative_question_service.UpdateGenerativeQuestionsFeatureConfigRequest],
        generative_question.GenerativeQuestionsFeatureConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGenerativeQuestionsFeatureConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(GenerativeQuestionServiceRestStub):
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
                    "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/catalogs/*/branches/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/catalogs/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/operations/*}",
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
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(GenerativeQuestionServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/catalogs/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
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

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("GenerativeQuestionServiceRestTransport",)
