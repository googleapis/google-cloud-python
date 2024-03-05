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


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.osconfig_v1.types import patch_deployments, patch_jobs

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import OsConfigServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class OsConfigServiceRestInterceptor:
    """Interceptor for OsConfigService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the OsConfigServiceRestTransport.

    .. code-block:: python
        class MyCustomOsConfigServiceInterceptor(OsConfigServiceRestInterceptor):
            def pre_cancel_patch_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_patch_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_patch_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_execute_patch_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_execute_patch_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_patch_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_patch_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_patch_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_patch_deployments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_patch_deployments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_patch_job_instance_details(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_patch_job_instance_details(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_patch_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_patch_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_pause_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_pause_patch_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resume_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resume_patch_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_patch_deployment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_patch_deployment(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OsConfigServiceRestTransport(interceptor=MyCustomOsConfigServiceInterceptor())
        client = OsConfigServiceClient(transport=transport)


    """

    def pre_cancel_patch_job(
        self,
        request: patch_jobs.CancelPatchJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[patch_jobs.CancelPatchJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_patch_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_cancel_patch_job(
        self, response: patch_jobs.PatchJob
    ) -> patch_jobs.PatchJob:
        """Post-rpc interceptor for cancel_patch_job

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_create_patch_deployment(
        self,
        request: patch_deployments.CreatePatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.CreatePatchDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_create_patch_deployment(
        self, response: patch_deployments.PatchDeployment
    ) -> patch_deployments.PatchDeployment:
        """Post-rpc interceptor for create_patch_deployment

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_patch_deployment(
        self,
        request: patch_deployments.DeletePatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.DeletePatchDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def pre_execute_patch_job(
        self,
        request: patch_jobs.ExecutePatchJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[patch_jobs.ExecutePatchJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for execute_patch_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_execute_patch_job(
        self, response: patch_jobs.PatchJob
    ) -> patch_jobs.PatchJob:
        """Post-rpc interceptor for execute_patch_job

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_get_patch_deployment(
        self,
        request: patch_deployments.GetPatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[patch_deployments.GetPatchDeploymentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_get_patch_deployment(
        self, response: patch_deployments.PatchDeployment
    ) -> patch_deployments.PatchDeployment:
        """Post-rpc interceptor for get_patch_deployment

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_get_patch_job(
        self,
        request: patch_jobs.GetPatchJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[patch_jobs.GetPatchJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_patch_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_get_patch_job(self, response: patch_jobs.PatchJob) -> patch_jobs.PatchJob:
        """Post-rpc interceptor for get_patch_job

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_list_patch_deployments(
        self,
        request: patch_deployments.ListPatchDeploymentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.ListPatchDeploymentsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_patch_deployments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_list_patch_deployments(
        self, response: patch_deployments.ListPatchDeploymentsResponse
    ) -> patch_deployments.ListPatchDeploymentsResponse:
        """Post-rpc interceptor for list_patch_deployments

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_list_patch_job_instance_details(
        self,
        request: patch_jobs.ListPatchJobInstanceDetailsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_jobs.ListPatchJobInstanceDetailsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_patch_job_instance_details

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_list_patch_job_instance_details(
        self, response: patch_jobs.ListPatchJobInstanceDetailsResponse
    ) -> patch_jobs.ListPatchJobInstanceDetailsResponse:
        """Post-rpc interceptor for list_patch_job_instance_details

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_list_patch_jobs(
        self,
        request: patch_jobs.ListPatchJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[patch_jobs.ListPatchJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_patch_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_list_patch_jobs(
        self, response: patch_jobs.ListPatchJobsResponse
    ) -> patch_jobs.ListPatchJobsResponse:
        """Post-rpc interceptor for list_patch_jobs

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_pause_patch_deployment(
        self,
        request: patch_deployments.PausePatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.PausePatchDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for pause_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_pause_patch_deployment(
        self, response: patch_deployments.PatchDeployment
    ) -> patch_deployments.PatchDeployment:
        """Post-rpc interceptor for pause_patch_deployment

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_resume_patch_deployment(
        self,
        request: patch_deployments.ResumePatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.ResumePatchDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for resume_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_resume_patch_deployment(
        self, response: patch_deployments.PatchDeployment
    ) -> patch_deployments.PatchDeployment:
        """Post-rpc interceptor for resume_patch_deployment

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response

    def pre_update_patch_deployment(
        self,
        request: patch_deployments.UpdatePatchDeploymentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        patch_deployments.UpdatePatchDeploymentRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_patch_deployment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OsConfigService server.
        """
        return request, metadata

    def post_update_patch_deployment(
        self, response: patch_deployments.PatchDeployment
    ) -> patch_deployments.PatchDeployment:
        """Post-rpc interceptor for update_patch_deployment

        Override in a subclass to manipulate the response
        after it is returned by the OsConfigService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class OsConfigServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: OsConfigServiceRestInterceptor


class OsConfigServiceRestTransport(OsConfigServiceTransport):
    """REST backend transport for OsConfigService.

    OS Config API

    The OS Config service is a server-side component that you can
    use to manage package installations and patch jobs for virtual
    machine instances.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "osconfig.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[OsConfigServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'osconfig.googleapis.com').
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
        self._interceptor = interceptor or OsConfigServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CancelPatchJob(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("CancelPatchJob")

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
            request: patch_jobs.CancelPatchJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_jobs.PatchJob:
            r"""Call the cancel patch job method over HTTP.

            Args:
                request (~.patch_jobs.CancelPatchJobRequest):
                    The request object. Message for canceling a patch job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_jobs.PatchJob:
                    A high level representation of a patch job that is
                either in progress or has completed.

                Instance details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/patchJobs/*}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_patch_job(
                request, metadata
            )
            pb_request = patch_jobs.CancelPatchJobRequest.pb(request)
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
            resp = patch_jobs.PatchJob()
            pb_resp = patch_jobs.PatchJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_cancel_patch_job(resp)
            return resp

    class _CreatePatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("CreatePatchDeployment")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "patchDeploymentId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: patch_deployments.CreatePatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.PatchDeployment:
            r"""Call the create patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.CreatePatchDeploymentRequest):
                    The request object. A request message for creating a
                patch deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.PatchDeployment:
                    Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/patchDeployments",
                    "body": "patch_deployment",
                },
            ]
            request, metadata = self._interceptor.pre_create_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.CreatePatchDeploymentRequest.pb(request)
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
            resp = patch_deployments.PatchDeployment()
            pb_resp = patch_deployments.PatchDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_patch_deployment(resp)
            return resp

    class _DeletePatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("DeletePatchDeployment")

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
            request: patch_deployments.DeletePatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.DeletePatchDeploymentRequest):
                    The request object. A request message for deleting a
                patch deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/patchDeployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.DeletePatchDeploymentRequest.pb(request)
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

    class _ExecutePatchJob(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("ExecutePatchJob")

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
            request: patch_jobs.ExecutePatchJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_jobs.PatchJob:
            r"""Call the execute patch job method over HTTP.

            Args:
                request (~.patch_jobs.ExecutePatchJobRequest):
                    The request object. A request message to initiate
                patching across Compute Engine
                instances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_jobs.PatchJob:
                    A high level representation of a patch job that is
                either in progress or has completed.

                Instance details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*}/patchJobs:execute",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_execute_patch_job(
                request, metadata
            )
            pb_request = patch_jobs.ExecutePatchJobRequest.pb(request)
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
            resp = patch_jobs.PatchJob()
            pb_resp = patch_jobs.PatchJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_execute_patch_job(resp)
            return resp

    class _GetPatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("GetPatchDeployment")

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
            request: patch_deployments.GetPatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.PatchDeployment:
            r"""Call the get patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.GetPatchDeploymentRequest):
                    The request object. A request message for retrieving a
                patch deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.PatchDeployment:
                    Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/patchDeployments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.GetPatchDeploymentRequest.pb(request)
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
            resp = patch_deployments.PatchDeployment()
            pb_resp = patch_deployments.PatchDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_patch_deployment(resp)
            return resp

    class _GetPatchJob(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("GetPatchJob")

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
            request: patch_jobs.GetPatchJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_jobs.PatchJob:
            r"""Call the get patch job method over HTTP.

            Args:
                request (~.patch_jobs.GetPatchJobRequest):
                    The request object. Request to get an active or completed
                patch job.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_jobs.PatchJob:
                    A high level representation of a patch job that is
                either in progress or has completed.

                Instance details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/patchJobs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_patch_job(request, metadata)
            pb_request = patch_jobs.GetPatchJobRequest.pb(request)
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
            resp = patch_jobs.PatchJob()
            pb_resp = patch_jobs.PatchJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_patch_job(resp)
            return resp

    class _ListPatchDeployments(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("ListPatchDeployments")

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
            request: patch_deployments.ListPatchDeploymentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.ListPatchDeploymentsResponse:
            r"""Call the list patch deployments method over HTTP.

            Args:
                request (~.patch_deployments.ListPatchDeploymentsRequest):
                    The request object. A request message for listing patch
                deployments.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.ListPatchDeploymentsResponse:
                    A response message for listing patch
                deployments.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/patchDeployments",
                },
            ]
            request, metadata = self._interceptor.pre_list_patch_deployments(
                request, metadata
            )
            pb_request = patch_deployments.ListPatchDeploymentsRequest.pb(request)
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
            resp = patch_deployments.ListPatchDeploymentsResponse()
            pb_resp = patch_deployments.ListPatchDeploymentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_patch_deployments(resp)
            return resp

    class _ListPatchJobInstanceDetails(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("ListPatchJobInstanceDetails")

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
            request: patch_jobs.ListPatchJobInstanceDetailsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_jobs.ListPatchJobInstanceDetailsResponse:
            r"""Call the list patch job instance
            details method over HTTP.

                Args:
                    request (~.patch_jobs.ListPatchJobInstanceDetailsRequest):
                        The request object. Request to list details for all
                    instances that are part of a patch job.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.patch_jobs.ListPatchJobInstanceDetailsResponse:
                        A response message for listing the
                    instances details for a patch job.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/patchJobs/*}/instanceDetails",
                },
            ]
            request, metadata = self._interceptor.pre_list_patch_job_instance_details(
                request, metadata
            )
            pb_request = patch_jobs.ListPatchJobInstanceDetailsRequest.pb(request)
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
            resp = patch_jobs.ListPatchJobInstanceDetailsResponse()
            pb_resp = patch_jobs.ListPatchJobInstanceDetailsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_patch_job_instance_details(resp)
            return resp

    class _ListPatchJobs(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("ListPatchJobs")

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
            request: patch_jobs.ListPatchJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_jobs.ListPatchJobsResponse:
            r"""Call the list patch jobs method over HTTP.

            Args:
                request (~.patch_jobs.ListPatchJobsRequest):
                    The request object. A request message for listing patch
                jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_jobs.ListPatchJobsResponse:
                    A response message for listing patch
                jobs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*}/patchJobs",
                },
            ]
            request, metadata = self._interceptor.pre_list_patch_jobs(request, metadata)
            pb_request = patch_jobs.ListPatchJobsRequest.pb(request)
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
            resp = patch_jobs.ListPatchJobsResponse()
            pb_resp = patch_jobs.ListPatchJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_patch_jobs(resp)
            return resp

    class _PausePatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("PausePatchDeployment")

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
            request: patch_deployments.PausePatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.PatchDeployment:
            r"""Call the pause patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.PausePatchDeploymentRequest):
                    The request object. A request message for pausing a patch
                deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.PatchDeployment:
                    Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/patchDeployments/*}:pause",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_pause_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.PausePatchDeploymentRequest.pb(request)
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
            resp = patch_deployments.PatchDeployment()
            pb_resp = patch_deployments.PatchDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_pause_patch_deployment(resp)
            return resp

    class _ResumePatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("ResumePatchDeployment")

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
            request: patch_deployments.ResumePatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.PatchDeployment:
            r"""Call the resume patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.ResumePatchDeploymentRequest):
                    The request object. A request message for resuming a
                patch deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.PatchDeployment:
                    Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/patchDeployments/*}:resume",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_resume_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.ResumePatchDeploymentRequest.pb(request)
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
            resp = patch_deployments.PatchDeployment()
            pb_resp = patch_deployments.PatchDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resume_patch_deployment(resp)
            return resp

    class _UpdatePatchDeployment(OsConfigServiceRestStub):
        def __hash__(self):
            return hash("UpdatePatchDeployment")

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
            request: patch_deployments.UpdatePatchDeploymentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> patch_deployments.PatchDeployment:
            r"""Call the update patch deployment method over HTTP.

            Args:
                request (~.patch_deployments.UpdatePatchDeploymentRequest):
                    The request object. A request message for updating a
                patch deployment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.patch_deployments.PatchDeployment:
                    Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{patch_deployment.name=projects/*/patchDeployments/*}",
                    "body": "patch_deployment",
                },
            ]
            request, metadata = self._interceptor.pre_update_patch_deployment(
                request, metadata
            )
            pb_request = patch_deployments.UpdatePatchDeploymentRequest.pb(request)
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
            resp = patch_deployments.PatchDeployment()
            pb_resp = patch_deployments.PatchDeployment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_patch_deployment(resp)
            return resp

    @property
    def cancel_patch_job(
        self,
    ) -> Callable[[patch_jobs.CancelPatchJobRequest], patch_jobs.PatchJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelPatchJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_patch_deployment(
        self,
    ) -> Callable[
        [patch_deployments.CreatePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_patch_deployment(
        self,
    ) -> Callable[[patch_deployments.DeletePatchDeploymentRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def execute_patch_job(
        self,
    ) -> Callable[[patch_jobs.ExecutePatchJobRequest], patch_jobs.PatchJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExecutePatchJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_patch_deployment(
        self,
    ) -> Callable[
        [patch_deployments.GetPatchDeploymentRequest], patch_deployments.PatchDeployment
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_patch_job(
        self,
    ) -> Callable[[patch_jobs.GetPatchJobRequest], patch_jobs.PatchJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPatchJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_patch_deployments(
        self,
    ) -> Callable[
        [patch_deployments.ListPatchDeploymentsRequest],
        patch_deployments.ListPatchDeploymentsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPatchDeployments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_patch_job_instance_details(
        self,
    ) -> Callable[
        [patch_jobs.ListPatchJobInstanceDetailsRequest],
        patch_jobs.ListPatchJobInstanceDetailsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPatchJobInstanceDetails(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_patch_jobs(
        self,
    ) -> Callable[[patch_jobs.ListPatchJobsRequest], patch_jobs.ListPatchJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPatchJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pause_patch_deployment(
        self,
    ) -> Callable[
        [patch_deployments.PausePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PausePatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_patch_deployment(
        self,
    ) -> Callable[
        [patch_deployments.ResumePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumePatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_patch_deployment(
        self,
    ) -> Callable[
        [patch_deployments.UpdatePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePatchDeployment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("OsConfigServiceRestTransport",)
