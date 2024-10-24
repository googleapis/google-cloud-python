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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.scheduler_v1.types import cloudscheduler
from google.cloud.scheduler_v1.types import job
from google.cloud.scheduler_v1.types import job as gcs_job

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseCloudSchedulerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class CloudSchedulerRestInterceptor:
    """Interceptor for CloudScheduler.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudSchedulerRestTransport.

    .. code-block:: python
        class MyCustomCloudSchedulerInterceptor(CloudSchedulerRestInterceptor):
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

            def pre_pause_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_pause_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resume_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resume_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_job(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudSchedulerRestTransport(interceptor=MyCustomCloudSchedulerInterceptor())
        client = CloudSchedulerClient(transport=transport)


    """

    def pre_create_job(
        self,
        request: cloudscheduler.CreateJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.CreateJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_create_job(self, response: gcs_job.Job) -> gcs_job.Job:
        """Post-rpc interceptor for create_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_delete_job(
        self,
        request: cloudscheduler.DeleteJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.DeleteJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def pre_get_job(
        self, request: cloudscheduler.GetJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloudscheduler.GetJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_get_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for get_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_list_jobs(
        self,
        request: cloudscheduler.ListJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.ListJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_list_jobs(
        self, response: cloudscheduler.ListJobsResponse
    ) -> cloudscheduler.ListJobsResponse:
        """Post-rpc interceptor for list_jobs

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_pause_job(
        self,
        request: cloudscheduler.PauseJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.PauseJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for pause_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_pause_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for pause_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_resume_job(
        self,
        request: cloudscheduler.ResumeJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.ResumeJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resume_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_resume_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for resume_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_run_job(
        self, request: cloudscheduler.RunJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloudscheduler.RunJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_run_job(self, response: job.Job) -> job.Job:
        """Post-rpc interceptor for run_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response

    def pre_update_job(
        self,
        request: cloudscheduler.UpdateJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudscheduler.UpdateJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_update_job(self, response: gcs_job.Job) -> gcs_job.Job:
        """Post-rpc interceptor for update_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
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
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
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
        before they are sent to the CloudScheduler server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the CloudScheduler server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudSchedulerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudSchedulerRestInterceptor


class CloudSchedulerRestTransport(_BaseCloudSchedulerRestTransport):
    """REST backend synchronous transport for CloudScheduler.

    The Cloud Scheduler API allows external entities to reliably
    schedule asynchronous jobs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "cloudscheduler.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudSchedulerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudscheduler.googleapis.com').
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
        self._interceptor = interceptor or CloudSchedulerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateJob(
        _BaseCloudSchedulerRestTransport._BaseCreateJob, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.CreateJob")

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
            request: cloudscheduler.CreateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_job.Job:
            r"""Call the create job method over HTTP.

            Args:
                request (~.cloudscheduler.CreateJobRequest):
                    The request object. Request message for
                [CreateJob][google.cloud.scheduler.v1.CloudScheduler.CreateJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseCreateJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseCreateJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseCloudSchedulerRestTransport._BaseCreateJob._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseCreateJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._CreateJob._get_response(
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
            resp = gcs_job.Job()
            pb_resp = gcs_job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_job(resp)
            return resp

    class _DeleteJob(
        _BaseCloudSchedulerRestTransport._BaseDeleteJob, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.DeleteJob")

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
            request: cloudscheduler.DeleteJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete job method over HTTP.

            Args:
                request (~.cloudscheduler.DeleteJobRequest):
                    The request object. Request message for deleting a job using
                [DeleteJob][google.cloud.scheduler.v1.CloudScheduler.DeleteJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseDeleteJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseDeleteJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseDeleteJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._DeleteJob._get_response(
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

    class _GetJob(_BaseCloudSchedulerRestTransport._BaseGetJob, CloudSchedulerRestStub):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.GetJob")

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
            request: cloudscheduler.GetJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> job.Job:
            r"""Call the get job method over HTTP.

            Args:
                request (~.cloudscheduler.GetJobRequest):
                    The request object. Request message for
                [GetJob][google.cloud.scheduler.v1.CloudScheduler.GetJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseGetJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseGetJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseGetJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._GetJob._get_response(
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
            return resp

    class _ListJobs(
        _BaseCloudSchedulerRestTransport._BaseListJobs, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.ListJobs")

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
            request: cloudscheduler.ListJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudscheduler.ListJobsResponse:
            r"""Call the list jobs method over HTTP.

            Args:
                request (~.cloudscheduler.ListJobsRequest):
                    The request object. Request message for listing jobs using
                [ListJobs][google.cloud.scheduler.v1.CloudScheduler.ListJobs].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudscheduler.ListJobsResponse:
                    Response message for listing jobs using
                [ListJobs][google.cloud.scheduler.v1.CloudScheduler.ListJobs].

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseListJobs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_jobs(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseListJobs._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseListJobs._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._ListJobs._get_response(
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
            resp = cloudscheduler.ListJobsResponse()
            pb_resp = cloudscheduler.ListJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_jobs(resp)
            return resp

    class _PauseJob(
        _BaseCloudSchedulerRestTransport._BasePauseJob, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.PauseJob")

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
            request: cloudscheduler.PauseJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> job.Job:
            r"""Call the pause job method over HTTP.

            Args:
                request (~.cloudscheduler.PauseJobRequest):
                    The request object. Request message for
                [PauseJob][google.cloud.scheduler.v1.CloudScheduler.PauseJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BasePauseJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_pause_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BasePauseJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseCloudSchedulerRestTransport._BasePauseJob._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BasePauseJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._PauseJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_pause_job(resp)
            return resp

    class _ResumeJob(
        _BaseCloudSchedulerRestTransport._BaseResumeJob, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.ResumeJob")

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
            request: cloudscheduler.ResumeJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> job.Job:
            r"""Call the resume job method over HTTP.

            Args:
                request (~.cloudscheduler.ResumeJobRequest):
                    The request object. Request message for
                [ResumeJob][google.cloud.scheduler.v1.CloudScheduler.ResumeJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseResumeJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_resume_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseResumeJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseCloudSchedulerRestTransport._BaseResumeJob._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseResumeJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._ResumeJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resume_job(resp)
            return resp

    class _RunJob(_BaseCloudSchedulerRestTransport._BaseRunJob, CloudSchedulerRestStub):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.RunJob")

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
            request: cloudscheduler.RunJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> job.Job:
            r"""Call the run job method over HTTP.

            Args:
                request (~.cloudscheduler.RunJobRequest):
                    The request object. Request message for forcing a job to run now using
                [RunJob][google.cloud.scheduler.v1.CloudScheduler.RunJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseRunJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_run_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseRunJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseCloudSchedulerRestTransport._BaseRunJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseRunJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._RunJob._get_response(
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
            resp = job.Job()
            pb_resp = job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_job(resp)
            return resp

    class _UpdateJob(
        _BaseCloudSchedulerRestTransport._BaseUpdateJob, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.UpdateJob")

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
            request: cloudscheduler.UpdateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_job.Job:
            r"""Call the update job method over HTTP.

            Args:
                request (~.cloudscheduler.UpdateJobRequest):
                    The request object. Request message for
                [UpdateJob][google.cloud.scheduler.v1.CloudScheduler.UpdateJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_job.Job:
                    Configuration for a job.
                The maximum allowed size for a job is
                1MB.

            """

            http_options = (
                _BaseCloudSchedulerRestTransport._BaseUpdateJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_job(request, metadata)
            transcoded_request = (
                _BaseCloudSchedulerRestTransport._BaseUpdateJob._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseCloudSchedulerRestTransport._BaseUpdateJob._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseCloudSchedulerRestTransport._BaseUpdateJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = CloudSchedulerRestTransport._UpdateJob._get_response(
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
            resp = gcs_job.Job()
            pb_resp = gcs_job.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_job(resp)
            return resp

    @property
    def create_job(self) -> Callable[[cloudscheduler.CreateJobRequest], gcs_job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_job(
        self,
    ) -> Callable[[cloudscheduler.DeleteJobRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_job(self) -> Callable[[cloudscheduler.GetJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_jobs(
        self,
    ) -> Callable[[cloudscheduler.ListJobsRequest], cloudscheduler.ListJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pause_job(self) -> Callable[[cloudscheduler.PauseJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PauseJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_job(self) -> Callable[[cloudscheduler.ResumeJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumeJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_job(self) -> Callable[[cloudscheduler.RunJobRequest], job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_job(self) -> Callable[[cloudscheduler.UpdateJobRequest], gcs_job.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseCloudSchedulerRestTransport._BaseGetLocation, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.GetLocation")

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
                _BaseCloudSchedulerRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseCloudSchedulerRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudSchedulerRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudSchedulerRestTransport._GetLocation._get_response(
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
        _BaseCloudSchedulerRestTransport._BaseListLocations, CloudSchedulerRestStub
    ):
        def __hash__(self):
            return hash("CloudSchedulerRestTransport.ListLocations")

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
                _BaseCloudSchedulerRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseCloudSchedulerRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseCloudSchedulerRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = CloudSchedulerRestTransport._ListLocations._get_response(
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudSchedulerRestTransport",)
