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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import gapic_v1

from google.protobuf import json_format

from requests import __version__ as requests_version
import dataclasses
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings


from google.cloud.bigtable_v2.types import bigtable


from .rest_base import _BaseBigtableRestTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class BigtableRestInterceptor:
    """Interceptor for Bigtable.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BigtableRestTransport.

    .. code-block:: python
        class MyCustomBigtableInterceptor(BigtableRestInterceptor):
            def pre_check_and_mutate_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_and_mutate_row(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_execute_query(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_execute_query(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_initial_change_stream_partitions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_initial_change_stream_partitions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mutate_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mutate_row(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mutate_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mutate_rows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_ping_and_warm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_ping_and_warm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_read_change_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_read_change_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_read_modify_write_row(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_read_modify_write_row(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_read_rows(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_read_rows(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_sample_row_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_sample_row_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BigtableRestTransport(interceptor=MyCustomBigtableInterceptor())
        client = BigtableClient(transport=transport)


    """

    def pre_check_and_mutate_row(
        self,
        request: bigtable.CheckAndMutateRowRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable.CheckAndMutateRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for check_and_mutate_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_check_and_mutate_row(
        self, response: bigtable.CheckAndMutateRowResponse
    ) -> bigtable.CheckAndMutateRowResponse:
        """Post-rpc interceptor for check_and_mutate_row

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_execute_query(
        self, request: bigtable.ExecuteQueryRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[bigtable.ExecuteQueryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for execute_query

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_execute_query(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for execute_query

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_generate_initial_change_stream_partitions(
        self,
        request: bigtable.GenerateInitialChangeStreamPartitionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable.GenerateInitialChangeStreamPartitionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_initial_change_stream_partitions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_generate_initial_change_stream_partitions(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for generate_initial_change_stream_partitions

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_mutate_row(
        self, request: bigtable.MutateRowRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[bigtable.MutateRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for mutate_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_mutate_row(
        self, response: bigtable.MutateRowResponse
    ) -> bigtable.MutateRowResponse:
        """Post-rpc interceptor for mutate_row

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_mutate_rows(
        self, request: bigtable.MutateRowsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[bigtable.MutateRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for mutate_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_mutate_rows(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for mutate_rows

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_ping_and_warm(
        self, request: bigtable.PingAndWarmRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[bigtable.PingAndWarmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for ping_and_warm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_ping_and_warm(
        self, response: bigtable.PingAndWarmResponse
    ) -> bigtable.PingAndWarmResponse:
        """Post-rpc interceptor for ping_and_warm

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_read_change_stream(
        self,
        request: bigtable.ReadChangeStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable.ReadChangeStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for read_change_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_read_change_stream(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for read_change_stream

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_read_modify_write_row(
        self,
        request: bigtable.ReadModifyWriteRowRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable.ReadModifyWriteRowRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for read_modify_write_row

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_read_modify_write_row(
        self, response: bigtable.ReadModifyWriteRowResponse
    ) -> bigtable.ReadModifyWriteRowResponse:
        """Post-rpc interceptor for read_modify_write_row

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_read_rows(
        self, request: bigtable.ReadRowsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[bigtable.ReadRowsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for read_rows

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_read_rows(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for read_rows

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response

    def pre_sample_row_keys(
        self,
        request: bigtable.SampleRowKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable.SampleRowKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for sample_row_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Bigtable server.
        """
        return request, metadata

    def post_sample_row_keys(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        """Post-rpc interceptor for sample_row_keys

        Override in a subclass to manipulate the response
        after it is returned by the Bigtable server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BigtableRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BigtableRestInterceptor


class BigtableRestTransport(_BaseBigtableRestTransport):
    """REST backend synchronous transport for Bigtable.

    Service for reading from and writing to existing Bigtable
    tables.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "bigtable.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BigtableRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigtable.googleapis.com').
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
        self._interceptor = interceptor or BigtableRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CheckAndMutateRow(
        _BaseBigtableRestTransport._BaseCheckAndMutateRow, BigtableRestStub
    ):
        def __hash__(self):
            return hash("BigtableRestTransport.CheckAndMutateRow")

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
            request: bigtable.CheckAndMutateRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable.CheckAndMutateRowResponse:
            r"""Call the check and mutate row method over HTTP.

            Args:
                request (~.bigtable.CheckAndMutateRowRequest):
                    The request object. Request message for
                Bigtable.CheckAndMutateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.CheckAndMutateRowResponse:
                    Response message for
                Bigtable.CheckAndMutateRow.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseCheckAndMutateRow._get_http_options()
            )
            request, metadata = self._interceptor.pre_check_and_mutate_row(
                request, metadata
            )
            transcoded_request = _BaseBigtableRestTransport._BaseCheckAndMutateRow._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableRestTransport._BaseCheckAndMutateRow._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableRestTransport._BaseCheckAndMutateRow._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableRestTransport._CheckAndMutateRow._get_response(
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
            resp = bigtable.CheckAndMutateRowResponse()
            pb_resp = bigtable.CheckAndMutateRowResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_and_mutate_row(resp)
            return resp

    class _ExecuteQuery(_BaseBigtableRestTransport._BaseExecuteQuery, BigtableRestStub):
        def __hash__(self):
            return hash("BigtableRestTransport.ExecuteQuery")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.ExecuteQueryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the execute query method over HTTP.

            Args:
                request (~.bigtable.ExecuteQueryRequest):
                    The request object. Request message for
                Bigtable.ExecuteQuery
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.ExecuteQueryResponse:
                    Response message for
                Bigtable.ExecuteQuery

            """

            http_options = (
                _BaseBigtableRestTransport._BaseExecuteQuery._get_http_options()
            )
            request, metadata = self._interceptor.pre_execute_query(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BaseExecuteQuery._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBigtableRestTransport._BaseExecuteQuery._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseExecuteQuery._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._ExecuteQuery._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, bigtable.ExecuteQueryResponse
            )
            resp = self._interceptor.post_execute_query(resp)
            return resp

    class _GenerateInitialChangeStreamPartitions(
        _BaseBigtableRestTransport._BaseGenerateInitialChangeStreamPartitions,
        BigtableRestStub,
    ):
        def __hash__(self):
            return hash("BigtableRestTransport.GenerateInitialChangeStreamPartitions")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.GenerateInitialChangeStreamPartitionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the generate initial change
            stream partitions method over HTTP.

                Args:
                    request (~.bigtable.GenerateInitialChangeStreamPartitionsRequest):
                        The request object. NOTE: This API is intended to be used
                    by Apache Beam BigtableIO. Request
                    message for
                    Bigtable.GenerateInitialChangeStreamPartitions.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.bigtable.GenerateInitialChangeStreamPartitionsResponse:
                        NOTE: This API is intended to be used
                    by Apache Beam BigtableIO. Response
                    message for
                    Bigtable.GenerateInitialChangeStreamPartitions.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseGenerateInitialChangeStreamPartitions._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_generate_initial_change_stream_partitions(
                request, metadata
            )
            transcoded_request = _BaseBigtableRestTransport._BaseGenerateInitialChangeStreamPartitions._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableRestTransport._BaseGenerateInitialChangeStreamPartitions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableRestTransport._BaseGenerateInitialChangeStreamPartitions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableRestTransport._GenerateInitialChangeStreamPartitions._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, bigtable.GenerateInitialChangeStreamPartitionsResponse
            )
            resp = self._interceptor.post_generate_initial_change_stream_partitions(
                resp
            )
            return resp

    class _MutateRow(_BaseBigtableRestTransport._BaseMutateRow, BigtableRestStub):
        def __hash__(self):
            return hash("BigtableRestTransport.MutateRow")

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
            request: bigtable.MutateRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable.MutateRowResponse:
            r"""Call the mutate row method over HTTP.

            Args:
                request (~.bigtable.MutateRowRequest):
                    The request object. Request message for
                Bigtable.MutateRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.MutateRowResponse:
                    Response message for
                Bigtable.MutateRow.

            """

            http_options = _BaseBigtableRestTransport._BaseMutateRow._get_http_options()
            request, metadata = self._interceptor.pre_mutate_row(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BaseMutateRow._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBigtableRestTransport._BaseMutateRow._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseMutateRow._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._MutateRow._get_response(
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
            resp = bigtable.MutateRowResponse()
            pb_resp = bigtable.MutateRowResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mutate_row(resp)
            return resp

    class _MutateRows(_BaseBigtableRestTransport._BaseMutateRows, BigtableRestStub):
        def __hash__(self):
            return hash("BigtableRestTransport.MutateRows")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.MutateRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the mutate rows method over HTTP.

            Args:
                request (~.bigtable.MutateRowsRequest):
                    The request object. Request message for
                BigtableService.MutateRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.MutateRowsResponse:
                    Response message for
                BigtableService.MutateRows.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseMutateRows._get_http_options()
            )
            request, metadata = self._interceptor.pre_mutate_rows(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BaseMutateRows._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBigtableRestTransport._BaseMutateRows._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseMutateRows._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._MutateRows._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, bigtable.MutateRowsResponse
            )
            resp = self._interceptor.post_mutate_rows(resp)
            return resp

    class _PingAndWarm(_BaseBigtableRestTransport._BasePingAndWarm, BigtableRestStub):
        def __hash__(self):
            return hash("BigtableRestTransport.PingAndWarm")

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
            request: bigtable.PingAndWarmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable.PingAndWarmResponse:
            r"""Call the ping and warm method over HTTP.

            Args:
                request (~.bigtable.PingAndWarmRequest):
                    The request object. Request message for client connection
                keep-alive and warming.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.PingAndWarmResponse:
                    Response message for
                Bigtable.PingAndWarm connection
                keepalive and warming.

            """

            http_options = (
                _BaseBigtableRestTransport._BasePingAndWarm._get_http_options()
            )
            request, metadata = self._interceptor.pre_ping_and_warm(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BasePingAndWarm._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBigtableRestTransport._BasePingAndWarm._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BasePingAndWarm._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._PingAndWarm._get_response(
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
            resp = bigtable.PingAndWarmResponse()
            pb_resp = bigtable.PingAndWarmResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_ping_and_warm(resp)
            return resp

    class _ReadChangeStream(
        _BaseBigtableRestTransport._BaseReadChangeStream, BigtableRestStub
    ):
        def __hash__(self):
            return hash("BigtableRestTransport.ReadChangeStream")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.ReadChangeStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the read change stream method over HTTP.

            Args:
                request (~.bigtable.ReadChangeStreamRequest):
                    The request object. NOTE: This API is intended to be used
                by Apache Beam BigtableIO. Request
                message for Bigtable.ReadChangeStream.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.ReadChangeStreamResponse:
                    NOTE: This API is intended to be used
                by Apache Beam BigtableIO. Response
                message for Bigtable.ReadChangeStream.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseReadChangeStream._get_http_options()
            )
            request, metadata = self._interceptor.pre_read_change_stream(
                request, metadata
            )
            transcoded_request = _BaseBigtableRestTransport._BaseReadChangeStream._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBigtableRestTransport._BaseReadChangeStream._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseReadChangeStream._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._ReadChangeStream._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, bigtable.ReadChangeStreamResponse
            )
            resp = self._interceptor.post_read_change_stream(resp)
            return resp

    class _ReadModifyWriteRow(
        _BaseBigtableRestTransport._BaseReadModifyWriteRow, BigtableRestStub
    ):
        def __hash__(self):
            return hash("BigtableRestTransport.ReadModifyWriteRow")

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
            request: bigtable.ReadModifyWriteRowRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable.ReadModifyWriteRowResponse:
            r"""Call the read modify write row method over HTTP.

            Args:
                request (~.bigtable.ReadModifyWriteRowRequest):
                    The request object. Request message for
                Bigtable.ReadModifyWriteRow.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.ReadModifyWriteRowResponse:
                    Response message for
                Bigtable.ReadModifyWriteRow.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseReadModifyWriteRow._get_http_options()
            )
            request, metadata = self._interceptor.pre_read_modify_write_row(
                request, metadata
            )
            transcoded_request = _BaseBigtableRestTransport._BaseReadModifyWriteRow._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableRestTransport._BaseReadModifyWriteRow._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableRestTransport._BaseReadModifyWriteRow._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableRestTransport._ReadModifyWriteRow._get_response(
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
            resp = bigtable.ReadModifyWriteRowResponse()
            pb_resp = bigtable.ReadModifyWriteRowResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_read_modify_write_row(resp)
            return resp

    class _ReadRows(_BaseBigtableRestTransport._BaseReadRows, BigtableRestStub):
        def __hash__(self):
            return hash("BigtableRestTransport.ReadRows")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.ReadRowsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the read rows method over HTTP.

            Args:
                request (~.bigtable.ReadRowsRequest):
                    The request object. Request message for
                Bigtable.ReadRows.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.ReadRowsResponse:
                    Response message for
                Bigtable.ReadRows.

            """

            http_options = _BaseBigtableRestTransport._BaseReadRows._get_http_options()
            request, metadata = self._interceptor.pre_read_rows(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BaseReadRows._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseBigtableRestTransport._BaseReadRows._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseReadRows._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._ReadRows._get_response(
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
            resp = rest_streaming.ResponseIterator(response, bigtable.ReadRowsResponse)
            resp = self._interceptor.post_read_rows(resp)
            return resp

    class _SampleRowKeys(
        _BaseBigtableRestTransport._BaseSampleRowKeys, BigtableRestStub
    ):
        def __hash__(self):
            return hash("BigtableRestTransport.SampleRowKeys")

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
                stream=True,
            )
            return response

        def __call__(
            self,
            request: bigtable.SampleRowKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the sample row keys method over HTTP.

            Args:
                request (~.bigtable.SampleRowKeysRequest):
                    The request object. Request message for
                Bigtable.SampleRowKeys.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable.SampleRowKeysResponse:
                    Response message for
                Bigtable.SampleRowKeys.

            """

            http_options = (
                _BaseBigtableRestTransport._BaseSampleRowKeys._get_http_options()
            )
            request, metadata = self._interceptor.pre_sample_row_keys(request, metadata)
            transcoded_request = (
                _BaseBigtableRestTransport._BaseSampleRowKeys._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBigtableRestTransport._BaseSampleRowKeys._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BigtableRestTransport._SampleRowKeys._get_response(
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
            resp = rest_streaming.ResponseIterator(
                response, bigtable.SampleRowKeysResponse
            )
            resp = self._interceptor.post_sample_row_keys(resp)
            return resp

    @property
    def check_and_mutate_row(
        self,
    ) -> Callable[
        [bigtable.CheckAndMutateRowRequest], bigtable.CheckAndMutateRowResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckAndMutateRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def execute_query(
        self,
    ) -> Callable[[bigtable.ExecuteQueryRequest], bigtable.ExecuteQueryResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExecuteQuery(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_initial_change_stream_partitions(
        self,
    ) -> Callable[
        [bigtable.GenerateInitialChangeStreamPartitionsRequest],
        bigtable.GenerateInitialChangeStreamPartitionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateInitialChangeStreamPartitions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mutate_row(
        self,
    ) -> Callable[[bigtable.MutateRowRequest], bigtable.MutateRowResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MutateRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mutate_rows(
        self,
    ) -> Callable[[bigtable.MutateRowsRequest], bigtable.MutateRowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MutateRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def ping_and_warm(
        self,
    ) -> Callable[[bigtable.PingAndWarmRequest], bigtable.PingAndWarmResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PingAndWarm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def read_change_stream(
        self,
    ) -> Callable[
        [bigtable.ReadChangeStreamRequest], bigtable.ReadChangeStreamResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReadChangeStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def read_modify_write_row(
        self,
    ) -> Callable[
        [bigtable.ReadModifyWriteRowRequest], bigtable.ReadModifyWriteRowResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReadModifyWriteRow(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def read_rows(
        self,
    ) -> Callable[[bigtable.ReadRowsRequest], bigtable.ReadRowsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReadRows(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def sample_row_keys(
        self,
    ) -> Callable[[bigtable.SampleRowKeysRequest], bigtable.SampleRowKeysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SampleRowKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BigtableRestTransport",)
