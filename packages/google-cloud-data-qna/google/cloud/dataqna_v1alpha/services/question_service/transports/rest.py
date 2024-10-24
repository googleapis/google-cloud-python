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

from google.cloud.dataqna_v1alpha.types import user_feedback as gcd_user_feedback
from google.cloud.dataqna_v1alpha.types import question
from google.cloud.dataqna_v1alpha.types import question as gcd_question
from google.cloud.dataqna_v1alpha.types import question_service
from google.cloud.dataqna_v1alpha.types import user_feedback

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseQuestionServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class QuestionServiceRestInterceptor:
    """Interceptor for QuestionService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the QuestionServiceRestTransport.

    .. code-block:: python
        class MyCustomQuestionServiceInterceptor(QuestionServiceRestInterceptor):
            def pre_create_question(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_question(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_execute_question(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_execute_question(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_question(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_question(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_user_feedback(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_user_feedback(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_user_feedback(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_user_feedback(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = QuestionServiceRestTransport(interceptor=MyCustomQuestionServiceInterceptor())
        client = QuestionServiceClient(transport=transport)


    """

    def pre_create_question(
        self,
        request: question_service.CreateQuestionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[question_service.CreateQuestionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_question

        Override in a subclass to manipulate the request or metadata
        before they are sent to the QuestionService server.
        """
        return request, metadata

    def post_create_question(
        self, response: gcd_question.Question
    ) -> gcd_question.Question:
        """Post-rpc interceptor for create_question

        Override in a subclass to manipulate the response
        after it is returned by the QuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_execute_question(
        self,
        request: question_service.ExecuteQuestionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[question_service.ExecuteQuestionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for execute_question

        Override in a subclass to manipulate the request or metadata
        before they are sent to the QuestionService server.
        """
        return request, metadata

    def post_execute_question(self, response: question.Question) -> question.Question:
        """Post-rpc interceptor for execute_question

        Override in a subclass to manipulate the response
        after it is returned by the QuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_get_question(
        self,
        request: question_service.GetQuestionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[question_service.GetQuestionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_question

        Override in a subclass to manipulate the request or metadata
        before they are sent to the QuestionService server.
        """
        return request, metadata

    def post_get_question(self, response: question.Question) -> question.Question:
        """Post-rpc interceptor for get_question

        Override in a subclass to manipulate the response
        after it is returned by the QuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_get_user_feedback(
        self,
        request: question_service.GetUserFeedbackRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[question_service.GetUserFeedbackRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_user_feedback

        Override in a subclass to manipulate the request or metadata
        before they are sent to the QuestionService server.
        """
        return request, metadata

    def post_get_user_feedback(
        self, response: user_feedback.UserFeedback
    ) -> user_feedback.UserFeedback:
        """Post-rpc interceptor for get_user_feedback

        Override in a subclass to manipulate the response
        after it is returned by the QuestionService server but before
        it is returned to user code.
        """
        return response

    def pre_update_user_feedback(
        self,
        request: question_service.UpdateUserFeedbackRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[question_service.UpdateUserFeedbackRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_user_feedback

        Override in a subclass to manipulate the request or metadata
        before they are sent to the QuestionService server.
        """
        return request, metadata

    def post_update_user_feedback(
        self, response: gcd_user_feedback.UserFeedback
    ) -> gcd_user_feedback.UserFeedback:
        """Post-rpc interceptor for update_user_feedback

        Override in a subclass to manipulate the response
        after it is returned by the QuestionService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class QuestionServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: QuestionServiceRestInterceptor


class QuestionServiceRestTransport(_BaseQuestionServiceRestTransport):
    """REST backend synchronous transport for QuestionService.

    Service to interpret natural language queries. The service allows to
    create ``Question`` resources that are interpreted and are filled
    with one or more interpretations if the question could be
    interpreted. Once a ``Question`` resource is created and has at
    least one interpretation, an interpretation can be chosen for
    execution, which triggers a query to the backend (for BigQuery, it
    will create a job). Upon successful execution of that
    interpretation, backend specific information will be returned so
    that the client can retrieve the results from the backend.

    The ``Question`` resources are named
    ``projects/*/locations/*/questions/*``.

    The ``Question`` resource has a singletion sub-resource
    ``UserFeedback`` named
    ``projects/*/locations/*/questions/*/userFeedback``, which allows
    access to user feedback.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "dataqna.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[QuestionServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'dataqna.googleapis.com').
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
        self._interceptor = interceptor or QuestionServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateQuestion(
        _BaseQuestionServiceRestTransport._BaseCreateQuestion, QuestionServiceRestStub
    ):
        def __hash__(self):
            return hash("QuestionServiceRestTransport.CreateQuestion")

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
            request: question_service.CreateQuestionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_question.Question:
            r"""Call the create question method over HTTP.

            Args:
                request (~.question_service.CreateQuestionRequest):
                    The request object. Request to create a question
                resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_question.Question:
                    The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

            """

            http_options = (
                _BaseQuestionServiceRestTransport._BaseCreateQuestion._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_question(request, metadata)
            transcoded_request = _BaseQuestionServiceRestTransport._BaseCreateQuestion._get_transcoded_request(
                http_options, request
            )

            body = _BaseQuestionServiceRestTransport._BaseCreateQuestion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseQuestionServiceRestTransport._BaseCreateQuestion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = QuestionServiceRestTransport._CreateQuestion._get_response(
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
            resp = gcd_question.Question()
            pb_resp = gcd_question.Question.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_question(resp)
            return resp

    class _ExecuteQuestion(
        _BaseQuestionServiceRestTransport._BaseExecuteQuestion, QuestionServiceRestStub
    ):
        def __hash__(self):
            return hash("QuestionServiceRestTransport.ExecuteQuestion")

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
            request: question_service.ExecuteQuestionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> question.Question:
            r"""Call the execute question method over HTTP.

            Args:
                request (~.question_service.ExecuteQuestionRequest):
                    The request object. Request to execute an interpretation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.question.Question:
                    The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

            """

            http_options = (
                _BaseQuestionServiceRestTransport._BaseExecuteQuestion._get_http_options()
            )
            request, metadata = self._interceptor.pre_execute_question(
                request, metadata
            )
            transcoded_request = _BaseQuestionServiceRestTransport._BaseExecuteQuestion._get_transcoded_request(
                http_options, request
            )

            body = _BaseQuestionServiceRestTransport._BaseExecuteQuestion._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseQuestionServiceRestTransport._BaseExecuteQuestion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = QuestionServiceRestTransport._ExecuteQuestion._get_response(
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
            resp = question.Question()
            pb_resp = question.Question.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_execute_question(resp)
            return resp

    class _GetQuestion(
        _BaseQuestionServiceRestTransport._BaseGetQuestion, QuestionServiceRestStub
    ):
        def __hash__(self):
            return hash("QuestionServiceRestTransport.GetQuestion")

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
            request: question_service.GetQuestionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> question.Question:
            r"""Call the get question method over HTTP.

            Args:
                request (~.question_service.GetQuestionRequest):
                    The request object. A request to get a previously created
                question.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.question.Question:
                    The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

            """

            http_options = (
                _BaseQuestionServiceRestTransport._BaseGetQuestion._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_question(request, metadata)
            transcoded_request = _BaseQuestionServiceRestTransport._BaseGetQuestion._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseQuestionServiceRestTransport._BaseGetQuestion._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = QuestionServiceRestTransport._GetQuestion._get_response(
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
            resp = question.Question()
            pb_resp = question.Question.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_question(resp)
            return resp

    class _GetUserFeedback(
        _BaseQuestionServiceRestTransport._BaseGetUserFeedback, QuestionServiceRestStub
    ):
        def __hash__(self):
            return hash("QuestionServiceRestTransport.GetUserFeedback")

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
            request: question_service.GetUserFeedbackRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> user_feedback.UserFeedback:
            r"""Call the get user feedback method over HTTP.

            Args:
                request (~.question_service.GetUserFeedbackRequest):
                    The request object. Request to get user feedback.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.user_feedback.UserFeedback:
                    Feedback provided by a user.
            """

            http_options = (
                _BaseQuestionServiceRestTransport._BaseGetUserFeedback._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_user_feedback(
                request, metadata
            )
            transcoded_request = _BaseQuestionServiceRestTransport._BaseGetUserFeedback._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseQuestionServiceRestTransport._BaseGetUserFeedback._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = QuestionServiceRestTransport._GetUserFeedback._get_response(
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
            resp = user_feedback.UserFeedback()
            pb_resp = user_feedback.UserFeedback.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_user_feedback(resp)
            return resp

    class _UpdateUserFeedback(
        _BaseQuestionServiceRestTransport._BaseUpdateUserFeedback,
        QuestionServiceRestStub,
    ):
        def __hash__(self):
            return hash("QuestionServiceRestTransport.UpdateUserFeedback")

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
            request: question_service.UpdateUserFeedbackRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_user_feedback.UserFeedback:
            r"""Call the update user feedback method over HTTP.

            Args:
                request (~.question_service.UpdateUserFeedbackRequest):
                    The request object. Request to updates user feedback.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_user_feedback.UserFeedback:
                    Feedback provided by a user.
            """

            http_options = (
                _BaseQuestionServiceRestTransport._BaseUpdateUserFeedback._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_user_feedback(
                request, metadata
            )
            transcoded_request = _BaseQuestionServiceRestTransport._BaseUpdateUserFeedback._get_transcoded_request(
                http_options, request
            )

            body = _BaseQuestionServiceRestTransport._BaseUpdateUserFeedback._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseQuestionServiceRestTransport._BaseUpdateUserFeedback._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = QuestionServiceRestTransport._UpdateUserFeedback._get_response(
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
            resp = gcd_user_feedback.UserFeedback()
            pb_resp = gcd_user_feedback.UserFeedback.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_user_feedback(resp)
            return resp

    @property
    def create_question(
        self,
    ) -> Callable[[question_service.CreateQuestionRequest], gcd_question.Question]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateQuestion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def execute_question(
        self,
    ) -> Callable[[question_service.ExecuteQuestionRequest], question.Question]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExecuteQuestion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_question(
        self,
    ) -> Callable[[question_service.GetQuestionRequest], question.Question]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetQuestion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_user_feedback(
        self,
    ) -> Callable[
        [question_service.GetUserFeedbackRequest], user_feedback.UserFeedback
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetUserFeedback(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_user_feedback(
        self,
    ) -> Callable[
        [question_service.UpdateUserFeedbackRequest], gcd_user_feedback.UserFeedback
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateUserFeedback(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("QuestionServiceRestTransport",)
