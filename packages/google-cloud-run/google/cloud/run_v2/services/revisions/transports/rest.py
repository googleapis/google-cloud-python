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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.run_v2.types import revision

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseRevisionsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class RevisionsRestInterceptor:
    """Interceptor for Revisions.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the RevisionsRestTransport.

    .. code-block:: python
        class MyCustomRevisionsInterceptor(RevisionsRestInterceptor):
            def pre_delete_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_revision(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_revision(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_revisions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_revisions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = RevisionsRestTransport(interceptor=MyCustomRevisionsInterceptor())
        client = RevisionsClient(transport=transport)


    """

    def pre_delete_revision(
        self,
        request: revision.DeleteRevisionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[revision.DeleteRevisionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_delete_revision(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_revision

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
        it is returned to user code.
        """
        return response

    def pre_get_revision(
        self, request: revision.GetRevisionRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[revision.GetRevisionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_revision

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_get_revision(self, response: revision.Revision) -> revision.Revision:
        """Post-rpc interceptor for get_revision

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
        it is returned to user code.
        """
        return response

    def pre_list_revisions(
        self,
        request: revision.ListRevisionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[revision.ListRevisionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_revisions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_list_revisions(
        self, response: revision.ListRevisionsResponse
    ) -> revision.ListRevisionsResponse:
        """Post-rpc interceptor for list_revisions

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
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
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
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
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
        it is returned to user code.
        """
        return response

    def pre_wait_operation(
        self,
        request: operations_pb2.WaitOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.WaitOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for wait_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Revisions server.
        """
        return request, metadata

    def post_wait_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for wait_operation

        Override in a subclass to manipulate the response
        after it is returned by the Revisions server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class RevisionsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: RevisionsRestInterceptor


class RevisionsRestTransport(_BaseRevisionsRestTransport):
    """REST backend synchronous transport for Revisions.

    Cloud Run Revision Control Plane API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "run.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[RevisionsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'run.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or RevisionsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=projects/*/locations/*}/operations",
                    },
                ],
                "google.longrunning.Operations.WaitOperation": [
                    {
                        "method": "post",
                        "uri": "/v2/{name=projects/*/locations/*/operations/*}:wait",
                        "body": "*",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _DeleteRevision(
        _BaseRevisionsRestTransport._BaseDeleteRevision, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.DeleteRevision")

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
            request: revision.DeleteRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete revision method over HTTP.

            Args:
                request (~.revision.DeleteRevisionRequest):
                    The request object. Request message for deleting a
                retired Revision. Revision lifecycle is
                usually managed by making changes to the
                parent Service. Only retired revisions
                can be deleted with this API.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseRevisionsRestTransport._BaseDeleteRevision._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_revision(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseDeleteRevision._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseDeleteRevision._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._DeleteRevision._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_revision(resp)
            return resp

    class _GetRevision(_BaseRevisionsRestTransport._BaseGetRevision, RevisionsRestStub):
        def __hash__(self):
            return hash("RevisionsRestTransport.GetRevision")

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
            request: revision.GetRevisionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> revision.Revision:
            r"""Call the get revision method over HTTP.

            Args:
                request (~.revision.GetRevisionRequest):
                    The request object. Request message for obtaining a
                Revision by its full name.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.revision.Revision:
                    A Revision is an immutable snapshot
                of code and configuration.  A Revision
                references a container image. Revisions
                are only created by updates to its
                parent Service.

            """

            http_options = (
                _BaseRevisionsRestTransport._BaseGetRevision._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_revision(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseGetRevision._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseGetRevision._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._GetRevision._get_response(
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
            resp = revision.Revision()
            pb_resp = revision.Revision.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_revision(resp)
            return resp

    class _ListRevisions(
        _BaseRevisionsRestTransport._BaseListRevisions, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.ListRevisions")

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
            request: revision.ListRevisionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> revision.ListRevisionsResponse:
            r"""Call the list revisions method over HTTP.

            Args:
                request (~.revision.ListRevisionsRequest):
                    The request object. Request message for retrieving a list
                of Revisions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.revision.ListRevisionsResponse:
                    Response message containing a list of
                Revisions.

            """

            http_options = (
                _BaseRevisionsRestTransport._BaseListRevisions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_revisions(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseListRevisions._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseListRevisions._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._ListRevisions._get_response(
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
            resp = revision.ListRevisionsResponse()
            pb_resp = revision.ListRevisionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_revisions(resp)
            return resp

    @property
    def delete_revision(
        self,
    ) -> Callable[[revision.DeleteRevisionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_revision(
        self,
    ) -> Callable[[revision.GetRevisionRequest], revision.Revision]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRevision(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_revisions(
        self,
    ) -> Callable[[revision.ListRevisionsRequest], revision.ListRevisionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRevisions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseRevisionsRestTransport._BaseDeleteOperation, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.DeleteOperation")

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
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseRevisionsRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseRevisionsRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseRevisionsRestTransport._BaseGetOperation, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.GetOperation")

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
                _BaseRevisionsRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._GetOperation._get_response(
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
        _BaseRevisionsRestTransport._BaseListOperations, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.ListOperations")

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
                _BaseRevisionsRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._ListOperations._get_response(
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
    def wait_operation(self):
        return self._WaitOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _WaitOperation(
        _BaseRevisionsRestTransport._BaseWaitOperation, RevisionsRestStub
    ):
        def __hash__(self):
            return hash("RevisionsRestTransport.WaitOperation")

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
            request: operations_pb2.WaitOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the wait operation method over HTTP.

            Args:
                request (operations_pb2.WaitOperationRequest):
                    The request object for WaitOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from WaitOperation method.
            """

            http_options = (
                _BaseRevisionsRestTransport._BaseWaitOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_wait_operation(request, metadata)
            transcoded_request = (
                _BaseRevisionsRestTransport._BaseWaitOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseRevisionsRestTransport._BaseWaitOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseRevisionsRestTransport._BaseWaitOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = RevisionsRestTransport._WaitOperation._get_response(
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

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_wait_operation(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("RevisionsRestTransport",)
