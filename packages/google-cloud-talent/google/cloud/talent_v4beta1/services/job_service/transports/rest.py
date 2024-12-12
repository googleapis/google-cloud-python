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

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.talent_v4beta1.types import job
from google.cloud.talent_v4beta1.types import job as gct_job
from google.cloud.talent_v4beta1.types import job_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseJobServiceRestTransport

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


class JobServiceRestInterceptor:
    """Interceptor for JobService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the JobServiceRestTransport.

    .. code-block:: python
        class MyCustomJobServiceInterceptor(JobServiceRestInterceptor):
            def pre_batch_create_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_update_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_jobs_for_alert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_jobs_for_alert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_job(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = JobServiceRestTransport(interceptor=MyCustomJobServiceInterceptor())
        client = JobServiceClient(transport=transport)


    """

    def pre_batch_create_jobs(
        self,
        request: job_service.BatchCreateJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        job_service.BatchCreateJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for batch_create_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_batch_create_jobs(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_create_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_jobs(
        self,
        request: job_service.BatchDeleteJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        job_service.BatchDeleteJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for batch_delete_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def pre_batch_update_jobs(
        self,
        request: job_service.BatchUpdateJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        job_service.BatchUpdateJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for batch_update_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_batch_update_jobs(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for batch_update_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_create_job(
        self,
        request: job_service.CreateJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.CreateJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for create_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_create_job(self, response: gct_job.Job) -> gct_job.Job:
        """Post-rpc interceptor for create_job

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_job(
        self,
        request: job_service.DeleteJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.DeleteJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for delete_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def pre_get_job(
        self,
        request: job_service.GetJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.GetJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for get_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_get_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for get_job

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_list_jobs(
        self,
        request: job_service.ListJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.ListJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for list_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_list_jobs(
        self, response: job_service.ListJobsResponse
    ) -> job_service.ListJobsResponse:
        """Post-rpc interceptor for list_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_search_jobs(
        self,
        request: job_service.SearchJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.SearchJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for search_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_search_jobs(
        self, response: job_service.SearchJobsResponse
    ) -> job_service.SearchJobsResponse:
        """Post-rpc interceptor for search_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_search_jobs_for_alert(
        self,
        request: job_service.SearchJobsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.SearchJobsRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for search_jobs_for_alert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_search_jobs_for_alert(
        self, response: job_service.SearchJobsResponse
    ) -> job_service.SearchJobsResponse:
        """Post-rpc interceptor for search_jobs_for_alert

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_update_job(
        self,
        request: job_service.UpdateJobRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[job_service.UpdateJobRequest, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Pre-rpc interceptor for update_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_update_job(self, response: gct_job.Job) -> gct_job.Job:
        """Post-rpc interceptor for update_job

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        operations_pb2.GetOperationRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the JobService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class JobServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: JobServiceRestInterceptor


class JobServiceRestTransport(_BaseJobServiceRestTransport):
    """REST backend synchronous transport for JobService.

    A service handles job management, including job CRUD,
    enumeration and search.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "jobs.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[JobServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'jobs.googleapis.com').
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
        self._interceptor = interceptor or JobServiceRestInterceptor()
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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v4beta1/{name=projects/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v4beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateJobs(
        _BaseJobServiceRestTransport._BaseBatchCreateJobs, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.BatchCreateJobs")

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
            request: job_service.BatchCreateJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch create jobs method over HTTP.

            Args:
                request (~.job_service.BatchCreateJobsRequest):
                    The request object. Request to create a batch of jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseBatchCreateJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_create_jobs(
                request, metadata
            )
            transcoded_request = _BaseJobServiceRestTransport._BaseBatchCreateJobs._get_transcoded_request(
                http_options, request
            )

            body = _BaseJobServiceRestTransport._BaseBatchCreateJobs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseJobServiceRestTransport._BaseBatchCreateJobs._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.BatchCreateJobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "BatchCreateJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._BatchCreateJobs._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_create_jobs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.batch_create_jobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "BatchCreateJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _BatchDeleteJobs(
        _BaseJobServiceRestTransport._BaseBatchDeleteJobs, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.BatchDeleteJobs")

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
            request: job_service.BatchDeleteJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the batch delete jobs method over HTTP.

            Args:
                request (~.job_service.BatchDeleteJobsRequest):
                    The request object. Batch delete jobs request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseBatchDeleteJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_delete_jobs(
                request, metadata
            )
            transcoded_request = _BaseJobServiceRestTransport._BaseBatchDeleteJobs._get_transcoded_request(
                http_options, request
            )

            body = _BaseJobServiceRestTransport._BaseBatchDeleteJobs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseJobServiceRestTransport._BaseBatchDeleteJobs._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.BatchDeleteJobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "BatchDeleteJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._BatchDeleteJobs._get_response(
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

    class _BatchUpdateJobs(
        _BaseJobServiceRestTransport._BaseBatchUpdateJobs, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.BatchUpdateJobs")

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
            request: job_service.BatchUpdateJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the batch update jobs method over HTTP.

            Args:
                request (~.job_service.BatchUpdateJobsRequest):
                    The request object. Request to update a batch of jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseBatchUpdateJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_batch_update_jobs(
                request, metadata
            )
            transcoded_request = _BaseJobServiceRestTransport._BaseBatchUpdateJobs._get_transcoded_request(
                http_options, request
            )

            body = _BaseJobServiceRestTransport._BaseBatchUpdateJobs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseJobServiceRestTransport._BaseBatchUpdateJobs._get_query_params_json(
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
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.BatchUpdateJobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "BatchUpdateJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._BatchUpdateJobs._get_response(
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_batch_update_jobs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.batch_update_jobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "BatchUpdateJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _CreateJob(_BaseJobServiceRestTransport._BaseCreateJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.CreateJob")

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
            request: job_service.CreateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gct_job.Job:
            r"""Call the create job method over HTTP.

            Args:
                request (~.job_service.CreateJobRequest):
                    The request object. Create job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gct_job.Job:
                    A Job resource represents a job posting (also referred
                to as a "job listing" or "job requisition"). A job
                belongs to a
                [Company][google.cloud.talent.v4beta1.Company], which is
                the hiring entity responsible for the job.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseCreateJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_create_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseCreateJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseJobServiceRestTransport._BaseCreateJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseCreateJob._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.CreateJob",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "CreateJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._CreateJob._get_response(
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
            resp = gct_job.Job()
            pb_resp = gct_job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_create_job(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gct_job.Job.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.create_job",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "CreateJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DeleteJob(_BaseJobServiceRestTransport._BaseDeleteJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.DeleteJob")

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
            request: job_service.DeleteJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ):
            r"""Call the delete job method over HTTP.

            Args:
                request (~.job_service.DeleteJobRequest):
                    The request object. Delete job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseDeleteJob._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.DeleteJob",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "DeleteJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._DeleteJob._get_response(
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

    class _GetJob(_BaseJobServiceRestTransport._BaseGetJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.GetJob")

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
            request: job_service.GetJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job.Job:
            r"""Call the get job method over HTTP.

            Args:
                request (~.job_service.GetJobRequest):
                    The request object. Get job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job.Job:
                    A Job resource represents a job posting (also referred
                to as a "job listing" or "job requisition"). A job
                belongs to a
                [Company][google.cloud.talent.v4beta1.Company], which is
                the hiring entity responsible for the job.

            """

            http_options = _BaseJobServiceRestTransport._BaseGetJob._get_http_options()

            request, metadata = self._interceptor.pre_get_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseGetJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseGetJob._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.GetJob",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "GetJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._GetJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get_job(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job.Job.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.get_job",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "GetJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListJobs(_BaseJobServiceRestTransport._BaseListJobs, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.ListJobs")

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
            request: job_service.ListJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job_service.ListJobsResponse:
            r"""Call the list jobs method over HTTP.

            Args:
                request (~.job_service.ListJobsRequest):
                    The request object. List jobs request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job_service.ListJobsResponse:
                    List jobs response.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseListJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_jobs(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseListJobs._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseListJobs._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.ListJobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "ListJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._ListJobs._get_response(
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
            resp = job_service.ListJobsResponse()
            pb_resp = job_service.ListJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_jobs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job_service.ListJobsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.list_jobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "ListJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SearchJobs(_BaseJobServiceRestTransport._BaseSearchJobs, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.SearchJobs")

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
            request: job_service.SearchJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job_service.SearchJobsResponse:
            r"""Call the search jobs method over HTTP.

            Args:
                request (~.job_service.SearchJobsRequest):
                    The request object. The Request body of the ``SearchJobs`` call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job_service.SearchJobsResponse:
                    Response for SearchJob method.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseSearchJobs._get_http_options()
            )

            request, metadata = self._interceptor.pre_search_jobs(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseSearchJobs._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseJobServiceRestTransport._BaseSearchJobs._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseSearchJobs._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.SearchJobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "SearchJobs",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._SearchJobs._get_response(
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
            resp = job_service.SearchJobsResponse()
            pb_resp = job_service.SearchJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_search_jobs(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job_service.SearchJobsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.search_jobs",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "SearchJobs",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _SearchJobsForAlert(
        _BaseJobServiceRestTransport._BaseSearchJobsForAlert, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.SearchJobsForAlert")

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
            request: job_service.SearchJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> job_service.SearchJobsResponse:
            r"""Call the search jobs for alert method over HTTP.

            Args:
                request (~.job_service.SearchJobsRequest):
                    The request object. The Request body of the ``SearchJobs`` call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.job_service.SearchJobsResponse:
                    Response for SearchJob method.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseSearchJobsForAlert._get_http_options()
            )

            request, metadata = self._interceptor.pre_search_jobs_for_alert(
                request, metadata
            )
            transcoded_request = _BaseJobServiceRestTransport._BaseSearchJobsForAlert._get_transcoded_request(
                http_options, request
            )

            body = _BaseJobServiceRestTransport._BaseSearchJobsForAlert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseJobServiceRestTransport._BaseSearchJobsForAlert._get_query_params_json(
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.SearchJobsForAlert",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "SearchJobsForAlert",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._SearchJobsForAlert._get_response(
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
            resp = job_service.SearchJobsResponse()
            pb_resp = job_service.SearchJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_search_jobs_for_alert(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = job_service.SearchJobsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.search_jobs_for_alert",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "SearchJobsForAlert",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateJob(_BaseJobServiceRestTransport._BaseUpdateJob, JobServiceRestStub):
        def __hash__(self):
            return hash("JobServiceRestTransport.UpdateJob")

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
            request: job_service.UpdateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> gct_job.Job:
            r"""Call the update job method over HTTP.

            Args:
                request (~.job_service.UpdateJobRequest):
                    The request object. Update job request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.gct_job.Job:
                    A Job resource represents a job posting (also referred
                to as a "job listing" or "job requisition"). A job
                belongs to a
                [Company][google.cloud.talent.v4beta1.Company], which is
                the hiring entity responsible for the job.

            """

            http_options = (
                _BaseJobServiceRestTransport._BaseUpdateJob._get_http_options()
            )

            request, metadata = self._interceptor.pre_update_job(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseUpdateJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseJobServiceRestTransport._BaseUpdateJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseUpdateJob._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.UpdateJob",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "UpdateJob",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._UpdateJob._get_response(
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
            resp = gct_job.Job()
            pb_resp = gct_job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_update_job(resp)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = gct_job.Job.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceClient.update_job",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "UpdateJob",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def batch_create_jobs(
        self,
    ) -> Callable[[job_service.BatchCreateJobsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_jobs(
        self,
    ) -> Callable[[job_service.BatchDeleteJobsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_jobs(
        self,
    ) -> Callable[[job_service.BatchUpdateJobsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_job(self) -> Callable[[job_service.CreateJobRequest], gct_job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_job(self) -> Callable[[job_service.DeleteJobRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_job(self) -> Callable[[job_service.GetJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_jobs(
        self,
    ) -> Callable[[job_service.ListJobsRequest], job_service.ListJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_jobs(
        self,
    ) -> Callable[[job_service.SearchJobsRequest], job_service.SearchJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_jobs_for_alert(
        self,
    ) -> Callable[[job_service.SearchJobsRequest], job_service.SearchJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchJobsForAlert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_job(self) -> Callable[[job_service.UpdateJobRequest], gct_job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseJobServiceRestTransport._BaseGetOperation, JobServiceRestStub
    ):
        def __hash__(self):
            return hash("JobServiceRestTransport.GetOperation")

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
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseJobServiceRestTransport._BaseGetOperation._get_http_options()
            )

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseJobServiceRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseJobServiceRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = json_format.MessageToJson(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.talent_v4beta1.JobServiceClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "GetOperation",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = JobServiceRestTransport._GetOperation._get_response(
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
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = json_format.MessageToJson(resp)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.talent_v4beta1.JobServiceAsyncClient.GetOperation",
                    extra={
                        "serviceName": "google.cloud.talent.v4beta1.JobService",
                        "rpcName": "GetOperation",
                        "httpResponse": http_response,
                        "metadata": http_response["headers"],
                    },
                )
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("JobServiceRestTransport",)
