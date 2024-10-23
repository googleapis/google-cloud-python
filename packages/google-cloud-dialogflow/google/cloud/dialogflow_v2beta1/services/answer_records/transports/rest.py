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
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.dialogflow_v2beta1.types import answer_record as gcd_answer_record
from google.cloud.dialogflow_v2beta1.types import answer_record

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAnswerRecordsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class AnswerRecordsRestInterceptor:
    """Interceptor for AnswerRecords.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AnswerRecordsRestTransport.

    .. code-block:: python
        class MyCustomAnswerRecordsInterceptor(AnswerRecordsRestInterceptor):
            def pre_get_answer_record(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_answer_record(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_answer_records(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_answer_records(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_answer_record(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_answer_record(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AnswerRecordsRestTransport(interceptor=MyCustomAnswerRecordsInterceptor())
        client = AnswerRecordsClient(transport=transport)


    """

    def pre_get_answer_record(
        self,
        request: answer_record.GetAnswerRecordRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[answer_record.GetAnswerRecordRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_answer_record

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_get_answer_record(
        self, response: answer_record.AnswerRecord
    ) -> answer_record.AnswerRecord:
        """Post-rpc interceptor for get_answer_record

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
        it is returned to user code.
        """
        return response

    def pre_list_answer_records(
        self,
        request: answer_record.ListAnswerRecordsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[answer_record.ListAnswerRecordsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_answer_records

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_list_answer_records(
        self, response: answer_record.ListAnswerRecordsResponse
    ) -> answer_record.ListAnswerRecordsResponse:
        """Post-rpc interceptor for list_answer_records

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
        it is returned to user code.
        """
        return response

    def pre_update_answer_record(
        self,
        request: gcd_answer_record.UpdateAnswerRecordRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcd_answer_record.UpdateAnswerRecordRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_answer_record

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_update_answer_record(
        self, response: gcd_answer_record.AnswerRecord
    ) -> gcd_answer_record.AnswerRecord:
        """Post-rpc interceptor for update_answer_record

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
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
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
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
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
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
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
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
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
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
        before they are sent to the AnswerRecords server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AnswerRecords server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AnswerRecordsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AnswerRecordsRestInterceptor


class AnswerRecordsRestTransport(_BaseAnswerRecordsRestTransport):
    """REST backend synchronous transport for AnswerRecords.

    Service for managing
    [AnswerRecords][google.cloud.dialogflow.v2beta1.AnswerRecord].

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
        interceptor: Optional[AnswerRecordsRestInterceptor] = None,
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
        self._interceptor = interceptor or AnswerRecordsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetAnswerRecord(
        _BaseAnswerRecordsRestTransport._BaseGetAnswerRecord, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.GetAnswerRecord")

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
            request: answer_record.GetAnswerRecordRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> answer_record.AnswerRecord:
            r"""Call the get answer record method over HTTP.

            Args:
                request (~.answer_record.GetAnswerRecordRequest):
                    The request object. Request message for
                [AnswerRecords.GetAnswerRecord][google.cloud.dialogflow.v2beta1.AnswerRecords.GetAnswerRecord].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.answer_record.AnswerRecord:
                    Answer records are records to manage answer history and
                feedbacks for Dialogflow.

                Currently, answer record includes:

                -  human agent assistant article suggestion
                -  human agent assistant faq article

                It doesn't include:

                -  ``DetectIntent`` intent matching
                -  ``DetectIntent`` knowledge

                Answer records are not related to the conversation
                history in the Dialogflow Console. A Record is generated
                even when the end-user disables conversation history in
                the console. Records are created when there's a human
                agent assistant suggestion generated.

                A typical workflow for customers provide feedback to an
                answer is:

                1. For human agent assistant, customers get suggestion
                   via ListSuggestions API. Together with the answers,
                   [AnswerRecord.name][google.cloud.dialogflow.v2beta1.AnswerRecord.name]
                   are returned to the customers.
                2. The customer uses the
                   [AnswerRecord.name][google.cloud.dialogflow.v2beta1.AnswerRecord.name]
                   to call the [UpdateAnswerRecord][] method to send
                   feedback about a specific answer that they believe is
                   wrong.

            """

            http_options = (
                _BaseAnswerRecordsRestTransport._BaseGetAnswerRecord._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_answer_record(
                request, metadata
            )
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseGetAnswerRecord._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseGetAnswerRecord._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._GetAnswerRecord._get_response(
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
            resp = answer_record.AnswerRecord()
            pb_resp = answer_record.AnswerRecord.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_answer_record(resp)
            return resp

    class _ListAnswerRecords(
        _BaseAnswerRecordsRestTransport._BaseListAnswerRecords, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.ListAnswerRecords")

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
            request: answer_record.ListAnswerRecordsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> answer_record.ListAnswerRecordsResponse:
            r"""Call the list answer records method over HTTP.

            Args:
                request (~.answer_record.ListAnswerRecordsRequest):
                    The request object. Request message for
                [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2beta1.AnswerRecords.ListAnswerRecords].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.answer_record.ListAnswerRecordsResponse:
                    Response message for
                [AnswerRecords.ListAnswerRecords][google.cloud.dialogflow.v2beta1.AnswerRecords.ListAnswerRecords].

            """

            http_options = (
                _BaseAnswerRecordsRestTransport._BaseListAnswerRecords._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_answer_records(
                request, metadata
            )
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseListAnswerRecords._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseListAnswerRecords._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._ListAnswerRecords._get_response(
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
            resp = answer_record.ListAnswerRecordsResponse()
            pb_resp = answer_record.ListAnswerRecordsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_answer_records(resp)
            return resp

    class _UpdateAnswerRecord(
        _BaseAnswerRecordsRestTransport._BaseUpdateAnswerRecord, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.UpdateAnswerRecord")

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
            request: gcd_answer_record.UpdateAnswerRecordRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_answer_record.AnswerRecord:
            r"""Call the update answer record method over HTTP.

            Args:
                request (~.gcd_answer_record.UpdateAnswerRecordRequest):
                    The request object. Request message for
                [AnswerRecords.UpdateAnswerRecord][google.cloud.dialogflow.v2beta1.AnswerRecords.UpdateAnswerRecord].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcd_answer_record.AnswerRecord:
                    Answer records are records to manage answer history and
                feedbacks for Dialogflow.

                Currently, answer record includes:

                -  human agent assistant article suggestion
                -  human agent assistant faq article

                It doesn't include:

                -  ``DetectIntent`` intent matching
                -  ``DetectIntent`` knowledge

                Answer records are not related to the conversation
                history in the Dialogflow Console. A Record is generated
                even when the end-user disables conversation history in
                the console. Records are created when there's a human
                agent assistant suggestion generated.

                A typical workflow for customers provide feedback to an
                answer is:

                1. For human agent assistant, customers get suggestion
                   via ListSuggestions API. Together with the answers,
                   [AnswerRecord.name][google.cloud.dialogflow.v2beta1.AnswerRecord.name]
                   are returned to the customers.
                2. The customer uses the
                   [AnswerRecord.name][google.cloud.dialogflow.v2beta1.AnswerRecord.name]
                   to call the [UpdateAnswerRecord][] method to send
                   feedback about a specific answer that they believe is
                   wrong.

            """

            http_options = (
                _BaseAnswerRecordsRestTransport._BaseUpdateAnswerRecord._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_answer_record(
                request, metadata
            )
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseUpdateAnswerRecord._get_transcoded_request(
                http_options, request
            )

            body = _BaseAnswerRecordsRestTransport._BaseUpdateAnswerRecord._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseUpdateAnswerRecord._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._UpdateAnswerRecord._get_response(
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
            resp = gcd_answer_record.AnswerRecord()
            pb_resp = gcd_answer_record.AnswerRecord.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_answer_record(resp)
            return resp

    @property
    def get_answer_record(
        self,
    ) -> Callable[[answer_record.GetAnswerRecordRequest], answer_record.AnswerRecord]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAnswerRecord(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_answer_records(
        self,
    ) -> Callable[
        [answer_record.ListAnswerRecordsRequest],
        answer_record.ListAnswerRecordsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAnswerRecords(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_answer_record(
        self,
    ) -> Callable[
        [gcd_answer_record.UpdateAnswerRecordRequest], gcd_answer_record.AnswerRecord
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAnswerRecord(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseAnswerRecordsRestTransport._BaseGetLocation, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.GetLocation")

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
                _BaseAnswerRecordsRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseAnswerRecordsRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = AnswerRecordsRestTransport._GetLocation._get_response(
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
        _BaseAnswerRecordsRestTransport._BaseListLocations, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.ListLocations")

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
                _BaseAnswerRecordsRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._ListLocations._get_response(
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
        _BaseAnswerRecordsRestTransport._BaseCancelOperation, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.CancelOperation")

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
                _BaseAnswerRecordsRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._CancelOperation._get_response(
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

    class _GetOperation(
        _BaseAnswerRecordsRestTransport._BaseGetOperation, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.GetOperation")

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
                _BaseAnswerRecordsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._GetOperation._get_response(
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
        _BaseAnswerRecordsRestTransport._BaseListOperations, AnswerRecordsRestStub
    ):
        def __hash__(self):
            return hash("AnswerRecordsRestTransport.ListOperations")

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
                _BaseAnswerRecordsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseAnswerRecordsRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAnswerRecordsRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AnswerRecordsRestTransport._ListOperations._get_response(
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


__all__ = ("AnswerRecordsRestTransport",)
