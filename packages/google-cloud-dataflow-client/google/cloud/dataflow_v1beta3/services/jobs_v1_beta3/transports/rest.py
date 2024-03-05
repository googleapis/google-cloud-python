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


from google.cloud.dataflow_v1beta3.types import jobs, snapshots

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import JobsV1Beta3Transport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class JobsV1Beta3RestInterceptor:
    """Interceptor for JobsV1Beta3.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the JobsV1Beta3RestTransport.

    .. code-block:: python
        class MyCustomJobsV1Beta3Interceptor(JobsV1Beta3RestInterceptor):
            def pre_aggregated_list_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_check_active_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_active_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_job(self, response):
                logging.log(f"Received response: {response}")
                return response

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

            def pre_snapshot_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_snapshot_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_job(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = JobsV1Beta3RestTransport(interceptor=MyCustomJobsV1Beta3Interceptor())
        client = JobsV1Beta3Client(transport=transport)


    """

    def pre_aggregated_list_jobs(
        self, request: jobs.ListJobsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.ListJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for aggregated_list_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_aggregated_list_jobs(
        self, response: jobs.ListJobsResponse
    ) -> jobs.ListJobsResponse:
        """Post-rpc interceptor for aggregated_list_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_create_job(
        self, request: jobs.CreateJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.CreateJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_create_job(self, response: jobs.Job) -> jobs.Job:
        """Post-rpc interceptor for create_job

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_get_job(
        self, request: jobs.GetJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.GetJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_get_job(self, response: jobs.Job) -> jobs.Job:
        """Post-rpc interceptor for get_job

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_list_jobs(
        self, request: jobs.ListJobsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.ListJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_list_jobs(self, response: jobs.ListJobsResponse) -> jobs.ListJobsResponse:
        """Post-rpc interceptor for list_jobs

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_snapshot_job(
        self, request: jobs.SnapshotJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.SnapshotJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for snapshot_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_snapshot_job(self, response: snapshots.Snapshot) -> snapshots.Snapshot:
        """Post-rpc interceptor for snapshot_job

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response

    def pre_update_job(
        self, request: jobs.UpdateJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[jobs.UpdateJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the JobsV1Beta3 server.
        """
        return request, metadata

    def post_update_job(self, response: jobs.Job) -> jobs.Job:
        """Post-rpc interceptor for update_job

        Override in a subclass to manipulate the response
        after it is returned by the JobsV1Beta3 server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class JobsV1Beta3RestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: JobsV1Beta3RestInterceptor


class JobsV1Beta3RestTransport(JobsV1Beta3Transport):
    """REST backend transport for JobsV1Beta3.

    Provides a method to create and modify Google Cloud Dataflow
    jobs. A Job is a multi-stage computation graph run by the Cloud
    Dataflow service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dataflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[JobsV1Beta3RestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataflow.googleapis.com').
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
        self._interceptor = interceptor or JobsV1Beta3RestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedListJobs(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("AggregatedListJobs")

        def __call__(
            self,
            request: jobs.ListJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.ListJobsResponse:
            r"""Call the aggregated list jobs method over HTTP.

            Args:
                request (~.jobs.ListJobsRequest):
                    The request object. Request to list Cloud Dataflow jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.jobs.ListJobsResponse:
                    Response to a request to list Cloud
                Dataflow jobs in a project. This might
                be a partial response, depending on the
                page size in the ListJobsRequest.
                However, if the project does not have
                any jobs, an instance of
                ListJobsResponse is not returned and the
                requests's response body is empty {}.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/jobs:aggregated",
                },
            ]
            request, metadata = self._interceptor.pre_aggregated_list_jobs(
                request, metadata
            )
            pb_request = jobs.ListJobsRequest.pb(request)
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
            resp = jobs.ListJobsResponse()
            pb_resp = jobs.ListJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_aggregated_list_jobs(resp)
            return resp

    class _CheckActiveJobs(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("CheckActiveJobs")

        def __call__(
            self,
            request: jobs.CheckActiveJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.CheckActiveJobsResponse:
            raise NotImplementedError(
                "Method CheckActiveJobs is not available over REST transport"
            )

    class _CreateJob(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("CreateJob")

        def __call__(
            self,
            request: jobs.CreateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.Job:
            r"""Call the create job method over HTTP.

            Args:
                request (~.jobs.CreateJobRequest):
                    The request object. Request to create a Cloud Dataflow
                job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.jobs.Job:
                    Defines a job to be run by the Cloud
                Dataflow service.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs",
                    "body": "job",
                },
                {
                    "method": "post",
                    "uri": "/v1b3/projects/{project_id}/jobs",
                    "body": "job",
                },
            ]
            request, metadata = self._interceptor.pre_create_job(request, metadata)
            pb_request = jobs.CreateJobRequest.pb(request)
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
            resp = jobs.Job()
            pb_resp = jobs.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_job(resp)
            return resp

    class _GetJob(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("GetJob")

        def __call__(
            self,
            request: jobs.GetJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.Job:
            r"""Call the get job method over HTTP.

            Args:
                request (~.jobs.GetJobRequest):
                    The request object. Request to get the state of a Cloud
                Dataflow job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.jobs.Job:
                    Defines a job to be run by the Cloud
                Dataflow service.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs/{job_id}",
                },
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/jobs/{job_id}",
                },
            ]
            request, metadata = self._interceptor.pre_get_job(request, metadata)
            pb_request = jobs.GetJobRequest.pb(request)
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
            resp = jobs.Job()
            pb_resp = jobs.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_job(resp)
            return resp

    class _ListJobs(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("ListJobs")

        def __call__(
            self,
            request: jobs.ListJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.ListJobsResponse:
            r"""Call the list jobs method over HTTP.

            Args:
                request (~.jobs.ListJobsRequest):
                    The request object. Request to list Cloud Dataflow jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.jobs.ListJobsResponse:
                    Response to a request to list Cloud
                Dataflow jobs in a project. This might
                be a partial response, depending on the
                page size in the ListJobsRequest.
                However, if the project does not have
                any jobs, an instance of
                ListJobsResponse is not returned and the
                requests's response body is empty {}.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs",
                },
                {
                    "method": "get",
                    "uri": "/v1b3/projects/{project_id}/jobs",
                },
            ]
            request, metadata = self._interceptor.pre_list_jobs(request, metadata)
            pb_request = jobs.ListJobsRequest.pb(request)
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
            resp = jobs.ListJobsResponse()
            pb_resp = jobs.ListJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_jobs(resp)
            return resp

    class _SnapshotJob(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("SnapshotJob")

        def __call__(
            self,
            request: jobs.SnapshotJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> snapshots.Snapshot:
            r"""Call the snapshot job method over HTTP.

            Args:
                request (~.jobs.SnapshotJobRequest):
                    The request object. Request to create a snapshot of a
                job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.snapshots.Snapshot:
                    Represents a snapshot of a job.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs/{job_id}:snapshot",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1b3/projects/{project_id}/jobs/{job_id}:snapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_snapshot_job(request, metadata)
            pb_request = jobs.SnapshotJobRequest.pb(request)
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
            resp = snapshots.Snapshot()
            pb_resp = snapshots.Snapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_snapshot_job(resp)
            return resp

    class _UpdateJob(JobsV1Beta3RestStub):
        def __hash__(self):
            return hash("UpdateJob")

        def __call__(
            self,
            request: jobs.UpdateJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> jobs.Job:
            r"""Call the update job method over HTTP.

            Args:
                request (~.jobs.UpdateJobRequest):
                    The request object. Request to update a Cloud Dataflow
                job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.jobs.Job:
                    Defines a job to be run by the Cloud
                Dataflow service.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1b3/projects/{project_id}/locations/{location}/jobs/{job_id}",
                    "body": "job",
                },
                {
                    "method": "put",
                    "uri": "/v1b3/projects/{project_id}/jobs/{job_id}",
                    "body": "job",
                },
            ]
            request, metadata = self._interceptor.pre_update_job(request, metadata)
            pb_request = jobs.UpdateJobRequest.pb(request)
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
            resp = jobs.Job()
            pb_resp = jobs.Job.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_job(resp)
            return resp

    @property
    def aggregated_list_jobs(
        self,
    ) -> Callable[[jobs.ListJobsRequest], jobs.ListJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedListJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def check_active_jobs(
        self,
    ) -> Callable[[jobs.CheckActiveJobsRequest], jobs.CheckActiveJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckActiveJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_job(self) -> Callable[[jobs.CreateJobRequest], jobs.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_job(self) -> Callable[[jobs.GetJobRequest], jobs.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_jobs(self) -> Callable[[jobs.ListJobsRequest], jobs.ListJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def snapshot_job(self) -> Callable[[jobs.SnapshotJobRequest], snapshots.Snapshot]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SnapshotJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_job(self) -> Callable[[jobs.UpdateJobRequest], jobs.Job]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("JobsV1Beta3RestTransport",)
