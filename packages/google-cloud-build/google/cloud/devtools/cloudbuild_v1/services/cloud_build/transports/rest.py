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

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
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


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.devtools.cloudbuild_v1.types import cloudbuild

from .base import CloudBuildTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CloudBuildRestInterceptor:
    """Interceptor for CloudBuild.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudBuildRestTransport.

    .. code-block:: python
        class MyCustomCloudBuildInterceptor(CloudBuildRestInterceptor):
            def pre_approve_build(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_build(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_build(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_build(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_build(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_build(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_build_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_build_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_worker_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_worker_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_build_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_worker_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_worker_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_build(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_build(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_build_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_build_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_worker_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_worker_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_builds(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_builds(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_build_triggers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_build_triggers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_worker_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_worker_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_receive_trigger_webhook(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_receive_trigger_webhook(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retry_build(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retry_build(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_build_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_build_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_build_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_build_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_worker_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_worker_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudBuildRestTransport(interceptor=MyCustomCloudBuildInterceptor())
        client = CloudBuildClient(transport=transport)


    """

    def pre_approve_build(
        self,
        request: cloudbuild.ApproveBuildRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.ApproveBuildRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for approve_build

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_approve_build(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for approve_build

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_build(
        self,
        request: cloudbuild.CancelBuildRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.CancelBuildRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_build

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_cancel_build(self, response: cloudbuild.Build) -> cloudbuild.Build:
        """Post-rpc interceptor for cancel_build

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_create_build(
        self,
        request: cloudbuild.CreateBuildRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.CreateBuildRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_build

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_create_build(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_build

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_create_build_trigger(
        self,
        request: cloudbuild.CreateBuildTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.CreateBuildTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_build_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_create_build_trigger(
        self, response: cloudbuild.BuildTrigger
    ) -> cloudbuild.BuildTrigger:
        """Post-rpc interceptor for create_build_trigger

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_create_worker_pool(
        self,
        request: cloudbuild.CreateWorkerPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.CreateWorkerPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_worker_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_create_worker_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_worker_pool

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_delete_build_trigger(
        self,
        request: cloudbuild.DeleteBuildTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.DeleteBuildTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_build_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def pre_delete_worker_pool(
        self,
        request: cloudbuild.DeleteWorkerPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.DeleteWorkerPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_worker_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_delete_worker_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_worker_pool

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_get_build(
        self, request: cloudbuild.GetBuildRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloudbuild.GetBuildRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_build

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_get_build(self, response: cloudbuild.Build) -> cloudbuild.Build:
        """Post-rpc interceptor for get_build

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_get_build_trigger(
        self,
        request: cloudbuild.GetBuildTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.GetBuildTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_build_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_get_build_trigger(
        self, response: cloudbuild.BuildTrigger
    ) -> cloudbuild.BuildTrigger:
        """Post-rpc interceptor for get_build_trigger

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_get_worker_pool(
        self,
        request: cloudbuild.GetWorkerPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.GetWorkerPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_worker_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_get_worker_pool(
        self, response: cloudbuild.WorkerPool
    ) -> cloudbuild.WorkerPool:
        """Post-rpc interceptor for get_worker_pool

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_list_builds(
        self, request: cloudbuild.ListBuildsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloudbuild.ListBuildsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_builds

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_list_builds(
        self, response: cloudbuild.ListBuildsResponse
    ) -> cloudbuild.ListBuildsResponse:
        """Post-rpc interceptor for list_builds

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_list_build_triggers(
        self,
        request: cloudbuild.ListBuildTriggersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.ListBuildTriggersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_build_triggers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_list_build_triggers(
        self, response: cloudbuild.ListBuildTriggersResponse
    ) -> cloudbuild.ListBuildTriggersResponse:
        """Post-rpc interceptor for list_build_triggers

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_list_worker_pools(
        self,
        request: cloudbuild.ListWorkerPoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.ListWorkerPoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_worker_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_list_worker_pools(
        self, response: cloudbuild.ListWorkerPoolsResponse
    ) -> cloudbuild.ListWorkerPoolsResponse:
        """Post-rpc interceptor for list_worker_pools

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_receive_trigger_webhook(
        self,
        request: cloudbuild.ReceiveTriggerWebhookRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.ReceiveTriggerWebhookRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for receive_trigger_webhook

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_receive_trigger_webhook(
        self, response: cloudbuild.ReceiveTriggerWebhookResponse
    ) -> cloudbuild.ReceiveTriggerWebhookResponse:
        """Post-rpc interceptor for receive_trigger_webhook

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_retry_build(
        self, request: cloudbuild.RetryBuildRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloudbuild.RetryBuildRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for retry_build

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_retry_build(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for retry_build

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_run_build_trigger(
        self,
        request: cloudbuild.RunBuildTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.RunBuildTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_build_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_run_build_trigger(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for run_build_trigger

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_update_build_trigger(
        self,
        request: cloudbuild.UpdateBuildTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.UpdateBuildTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_build_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_update_build_trigger(
        self, response: cloudbuild.BuildTrigger
    ) -> cloudbuild.BuildTrigger:
        """Post-rpc interceptor for update_build_trigger

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response

    def pre_update_worker_pool(
        self,
        request: cloudbuild.UpdateWorkerPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloudbuild.UpdateWorkerPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_worker_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudBuild server.
        """
        return request, metadata

    def post_update_worker_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_worker_pool

        Override in a subclass to manipulate the response
        after it is returned by the CloudBuild server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudBuildRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudBuildRestInterceptor


class CloudBuildRestTransport(CloudBuildTransport):
    """REST backend transport for CloudBuild.

    Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a ``Build``, which describes
    the location of the source to build, how to build the source, and
    where to store the built artifacts, if any.

    A user can list previously-requested builds or get builds by their
    ID to determine the status of the build.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudbuild.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudBuildRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudbuild.googleapis.com').
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
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CloudBuildRestInterceptor()
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
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=operations/**}:cancel",
                        "body": "*",
                    },
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=operations/**}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _ApproveBuild(CloudBuildRestStub):
        def __hash__(self):
            return hash("ApproveBuild")

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
            request: cloudbuild.ApproveBuildRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the approve build method over HTTP.

            Args:
                request (~.cloudbuild.ApproveBuildRequest):
                    The request object. Request to approve or reject a
                pending build.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/builds/*}:approve",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/builds/*}:approve",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_approve_build(request, metadata)
            pb_request = cloudbuild.ApproveBuildRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_build(resp)
            return resp

    class _CancelBuild(CloudBuildRestStub):
        def __hash__(self):
            return hash("CancelBuild")

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
            request: cloudbuild.CancelBuildRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.Build:
            r"""Call the cancel build method over HTTP.

            Args:
                request (~.cloudbuild.CancelBuildRequest):
                    The request object. Request to cancel an ongoing build.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.Build:
                    A build resource in the Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $PROJECT_NUMBER: the project number of the build.
                -  $LOCATION: the location/region of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/builds/{id}:cancel",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/builds/*}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_build(request, metadata)
            pb_request = cloudbuild.CancelBuildRequest.pb(request)
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
            resp = cloudbuild.Build()
            pb_resp = cloudbuild.Build.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_cancel_build(resp)
            return resp

    class _CreateBuild(CloudBuildRestStub):
        def __hash__(self):
            return hash("CreateBuild")

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
            request: cloudbuild.CreateBuildRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create build method over HTTP.

            Args:
                request (~.cloudbuild.CreateBuildRequest):
                    The request object. Request to create a new build.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/builds",
                    "body": "build",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/builds",
                    "body": "build",
                },
            ]
            request, metadata = self._interceptor.pre_create_build(request, metadata)
            pb_request = cloudbuild.CreateBuildRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_build(resp)
            return resp

    class _CreateBuildTrigger(CloudBuildRestStub):
        def __hash__(self):
            return hash("CreateBuildTrigger")

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
            request: cloudbuild.CreateBuildTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.BuildTrigger:
            r"""Call the create build trigger method over HTTP.

            Args:
                request (~.cloudbuild.CreateBuildTriggerRequest):
                    The request object. Request to create a new ``BuildTrigger``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.BuildTrigger:
                    Configuration for an automated build
                in response to source repository
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/triggers",
                    "body": "trigger",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/triggers",
                    "body": "trigger",
                },
            ]
            request, metadata = self._interceptor.pre_create_build_trigger(
                request, metadata
            )
            pb_request = cloudbuild.CreateBuildTriggerRequest.pb(request)
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
            resp = cloudbuild.BuildTrigger()
            pb_resp = cloudbuild.BuildTrigger.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_build_trigger(resp)
            return resp

    class _CreateWorkerPool(CloudBuildRestStub):
        def __hash__(self):
            return hash("CreateWorkerPool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workerPoolId": "",
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
            request: cloudbuild.CreateWorkerPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create worker pool method over HTTP.

            Args:
                request (~.cloudbuild.CreateWorkerPoolRequest):
                    The request object. Request to create a new ``WorkerPool``.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/workerPools",
                    "body": "worker_pool",
                },
            ]
            request, metadata = self._interceptor.pre_create_worker_pool(
                request, metadata
            )
            pb_request = cloudbuild.CreateWorkerPoolRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_worker_pool(resp)
            return resp

    class _DeleteBuildTrigger(CloudBuildRestStub):
        def __hash__(self):
            return hash("DeleteBuildTrigger")

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
            request: cloudbuild.DeleteBuildTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete build trigger method over HTTP.

            Args:
                request (~.cloudbuild.DeleteBuildTriggerRequest):
                    The request object. Request to delete a ``BuildTrigger``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/projects/{project_id}/triggers/{trigger_id}",
                },
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/triggers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_build_trigger(
                request, metadata
            )
            pb_request = cloudbuild.DeleteBuildTriggerRequest.pb(request)
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

    class _DeleteWorkerPool(CloudBuildRestStub):
        def __hash__(self):
            return hash("DeleteWorkerPool")

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
            request: cloudbuild.DeleteWorkerPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete worker pool method over HTTP.

            Args:
                request (~.cloudbuild.DeleteWorkerPoolRequest):
                    The request object. Request to delete a ``WorkerPool``.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/workerPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_worker_pool(
                request, metadata
            )
            pb_request = cloudbuild.DeleteWorkerPoolRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_worker_pool(resp)
            return resp

    class _GetBuild(CloudBuildRestStub):
        def __hash__(self):
            return hash("GetBuild")

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
            request: cloudbuild.GetBuildRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.Build:
            r"""Call the get build method over HTTP.

            Args:
                request (~.cloudbuild.GetBuildRequest):
                    The request object. Request to get a build.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.Build:
                    A build resource in the Cloud Build API.

                At a high level, a ``Build`` describes where to find
                source code, how to build it (for example, the builder
                image to run on the source), and where to store the
                built artifacts.

                Fields can include the following variables, which will
                be expanded when the build is created:

                -  $PROJECT_ID: the project ID of the build.
                -  $PROJECT_NUMBER: the project number of the build.
                -  $LOCATION: the location/region of the build.
                -  $BUILD_ID: the autogenerated ID of the build.
                -  $REPO_NAME: the source repository name specified by
                   RepoSource.
                -  $BRANCH_NAME: the branch name specified by
                   RepoSource.
                -  $TAG_NAME: the tag name specified by RepoSource.
                -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified
                   by RepoSource or resolved from the specified branch
                   or tag.
                -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                   $COMMIT_SHA.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/builds/{id}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/builds/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_build(request, metadata)
            pb_request = cloudbuild.GetBuildRequest.pb(request)
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
            resp = cloudbuild.Build()
            pb_resp = cloudbuild.Build.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_build(resp)
            return resp

    class _GetBuildTrigger(CloudBuildRestStub):
        def __hash__(self):
            return hash("GetBuildTrigger")

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
            request: cloudbuild.GetBuildTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.BuildTrigger:
            r"""Call the get build trigger method over HTTP.

            Args:
                request (~.cloudbuild.GetBuildTriggerRequest):
                    The request object. Returns the ``BuildTrigger`` with the specified ID.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.BuildTrigger:
                    Configuration for an automated build
                in response to source repository
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/triggers/{trigger_id}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/triggers/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_build_trigger(
                request, metadata
            )
            pb_request = cloudbuild.GetBuildTriggerRequest.pb(request)
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
            resp = cloudbuild.BuildTrigger()
            pb_resp = cloudbuild.BuildTrigger.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_build_trigger(resp)
            return resp

    class _GetWorkerPool(CloudBuildRestStub):
        def __hash__(self):
            return hash("GetWorkerPool")

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
            request: cloudbuild.GetWorkerPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.WorkerPool:
            r"""Call the get worker pool method over HTTP.

            Args:
                request (~.cloudbuild.GetWorkerPoolRequest):
                    The request object. Request to get a ``WorkerPool`` with the specified name.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.WorkerPool:
                    Configuration for a ``WorkerPool``.

                Cloud Build owns and maintains a pool of workers for
                general use and have no access to a project's private
                network. By default, builds submitted to Cloud Build
                will use a worker from this pool.

                If your build needs access to resources on a private
                network, create and use a ``WorkerPool`` to run your
                builds. Private ``WorkerPool``\ s give your builds
                access to any single VPC network that you administer,
                including any on-prem resources connected to that VPC
                network. For an overview of private pools, see `Private
                pools
                overview <https://cloud.google.com/build/docs/private-pools/private-pools-overview>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/workerPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_worker_pool(request, metadata)
            pb_request = cloudbuild.GetWorkerPoolRequest.pb(request)
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
            resp = cloudbuild.WorkerPool()
            pb_resp = cloudbuild.WorkerPool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_worker_pool(resp)
            return resp

    class _ListBuilds(CloudBuildRestStub):
        def __hash__(self):
            return hash("ListBuilds")

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
            request: cloudbuild.ListBuildsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.ListBuildsResponse:
            r"""Call the list builds method over HTTP.

            Args:
                request (~.cloudbuild.ListBuildsRequest):
                    The request object. Request to list builds.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.ListBuildsResponse:
                    Response including listed builds.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/builds",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/builds",
                },
            ]
            request, metadata = self._interceptor.pre_list_builds(request, metadata)
            pb_request = cloudbuild.ListBuildsRequest.pb(request)
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
            resp = cloudbuild.ListBuildsResponse()
            pb_resp = cloudbuild.ListBuildsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_builds(resp)
            return resp

    class _ListBuildTriggers(CloudBuildRestStub):
        def __hash__(self):
            return hash("ListBuildTriggers")

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
            request: cloudbuild.ListBuildTriggersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.ListBuildTriggersResponse:
            r"""Call the list build triggers method over HTTP.

            Args:
                request (~.cloudbuild.ListBuildTriggersRequest):
                    The request object. Request to list existing ``BuildTriggers``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.ListBuildTriggersResponse:
                    Response containing existing ``BuildTriggers``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id}/triggers",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/triggers",
                },
            ]
            request, metadata = self._interceptor.pre_list_build_triggers(
                request, metadata
            )
            pb_request = cloudbuild.ListBuildTriggersRequest.pb(request)
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
            resp = cloudbuild.ListBuildTriggersResponse()
            pb_resp = cloudbuild.ListBuildTriggersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_build_triggers(resp)
            return resp

    class _ListWorkerPools(CloudBuildRestStub):
        def __hash__(self):
            return hash("ListWorkerPools")

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
            request: cloudbuild.ListWorkerPoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.ListWorkerPoolsResponse:
            r"""Call the list worker pools method over HTTP.

            Args:
                request (~.cloudbuild.ListWorkerPoolsRequest):
                    The request object. Request to list ``WorkerPool``\ s.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.ListWorkerPoolsResponse:
                    Response containing existing ``WorkerPools``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/workerPools",
                },
            ]
            request, metadata = self._interceptor.pre_list_worker_pools(
                request, metadata
            )
            pb_request = cloudbuild.ListWorkerPoolsRequest.pb(request)
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
            resp = cloudbuild.ListWorkerPoolsResponse()
            pb_resp = cloudbuild.ListWorkerPoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_worker_pools(resp)
            return resp

    class _ReceiveTriggerWebhook(CloudBuildRestStub):
        def __hash__(self):
            return hash("ReceiveTriggerWebhook")

        def __call__(
            self,
            request: cloudbuild.ReceiveTriggerWebhookRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.ReceiveTriggerWebhookResponse:
            r"""Call the receive trigger webhook method over HTTP.

            Args:
                request (~.cloudbuild.ReceiveTriggerWebhookRequest):
                    The request object. ReceiveTriggerWebhookRequest [Experimental] is the
                request object accepted by the ReceiveTriggerWebhook
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.ReceiveTriggerWebhookResponse:
                    ReceiveTriggerWebhookResponse [Experimental] is the
                response object for the ReceiveTriggerWebhook method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/triggers/{trigger}:webhook",
                    "body": "body",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/triggers/*}:webhook",
                    "body": "body",
                },
            ]
            request, metadata = self._interceptor.pre_receive_trigger_webhook(
                request, metadata
            )
            pb_request = cloudbuild.ReceiveTriggerWebhookRequest.pb(request)
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
            resp = cloudbuild.ReceiveTriggerWebhookResponse()
            pb_resp = cloudbuild.ReceiveTriggerWebhookResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_receive_trigger_webhook(resp)
            return resp

    class _RetryBuild(CloudBuildRestStub):
        def __hash__(self):
            return hash("RetryBuild")

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
            request: cloudbuild.RetryBuildRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the retry build method over HTTP.

            Args:
                request (~.cloudbuild.RetryBuildRequest):
                    The request object. Specifies a build to retry.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/builds/{id}:retry",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/builds/*}:retry",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_retry_build(request, metadata)
            pb_request = cloudbuild.RetryBuildRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_retry_build(resp)
            return resp

    class _RunBuildTrigger(CloudBuildRestStub):
        def __hash__(self):
            return hash("RunBuildTrigger")

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
            request: cloudbuild.RunBuildTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the run build trigger method over HTTP.

            Args:
                request (~.cloudbuild.RunBuildTriggerRequest):
                    The request object. Specifies a build trigger to run and
                the source to use.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id}/triggers/{trigger_id}:run",
                    "body": "source",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/triggers/*}:run",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_build_trigger(
                request, metadata
            )
            pb_request = cloudbuild.RunBuildTriggerRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_build_trigger(resp)
            return resp

    class _UpdateBuildTrigger(CloudBuildRestStub):
        def __hash__(self):
            return hash("UpdateBuildTrigger")

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
            request: cloudbuild.UpdateBuildTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloudbuild.BuildTrigger:
            r"""Call the update build trigger method over HTTP.

            Args:
                request (~.cloudbuild.UpdateBuildTriggerRequest):
                    The request object. Request to update an existing ``BuildTrigger``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloudbuild.BuildTrigger:
                    Configuration for an automated build
                in response to source repository
                changes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/projects/{project_id}/triggers/{trigger_id}",
                    "body": "trigger",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{trigger.resource_name=projects/*/locations/*/triggers/*}",
                    "body": "trigger",
                },
            ]
            request, metadata = self._interceptor.pre_update_build_trigger(
                request, metadata
            )
            pb_request = cloudbuild.UpdateBuildTriggerRequest.pb(request)
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
            resp = cloudbuild.BuildTrigger()
            pb_resp = cloudbuild.BuildTrigger.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_build_trigger(resp)
            return resp

    class _UpdateWorkerPool(CloudBuildRestStub):
        def __hash__(self):
            return hash("UpdateWorkerPool")

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
            request: cloudbuild.UpdateWorkerPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update worker pool method over HTTP.

            Args:
                request (~.cloudbuild.UpdateWorkerPoolRequest):
                    The request object. Request to update a ``WorkerPool``.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{worker_pool.name=projects/*/locations/*/workerPools/*}",
                    "body": "worker_pool",
                },
            ]
            request, metadata = self._interceptor.pre_update_worker_pool(
                request, metadata
            )
            pb_request = cloudbuild.UpdateWorkerPoolRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_worker_pool(resp)
            return resp

    @property
    def approve_build(
        self,
    ) -> Callable[[cloudbuild.ApproveBuildRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveBuild(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_build(
        self,
    ) -> Callable[[cloudbuild.CancelBuildRequest], cloudbuild.Build]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelBuild(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_build(
        self,
    ) -> Callable[[cloudbuild.CreateBuildRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBuild(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_build_trigger(
        self,
    ) -> Callable[[cloudbuild.CreateBuildTriggerRequest], cloudbuild.BuildTrigger]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBuildTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_worker_pool(
        self,
    ) -> Callable[[cloudbuild.CreateWorkerPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkerPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_build_trigger(
        self,
    ) -> Callable[[cloudbuild.DeleteBuildTriggerRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBuildTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_worker_pool(
        self,
    ) -> Callable[[cloudbuild.DeleteWorkerPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkerPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_build(self) -> Callable[[cloudbuild.GetBuildRequest], cloudbuild.Build]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBuild(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_build_trigger(
        self,
    ) -> Callable[[cloudbuild.GetBuildTriggerRequest], cloudbuild.BuildTrigger]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBuildTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_worker_pool(
        self,
    ) -> Callable[[cloudbuild.GetWorkerPoolRequest], cloudbuild.WorkerPool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkerPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_builds(
        self,
    ) -> Callable[[cloudbuild.ListBuildsRequest], cloudbuild.ListBuildsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBuilds(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_build_triggers(
        self,
    ) -> Callable[
        [cloudbuild.ListBuildTriggersRequest], cloudbuild.ListBuildTriggersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBuildTriggers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_worker_pools(
        self,
    ) -> Callable[
        [cloudbuild.ListWorkerPoolsRequest], cloudbuild.ListWorkerPoolsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkerPools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def receive_trigger_webhook(
        self,
    ) -> Callable[
        [cloudbuild.ReceiveTriggerWebhookRequest],
        cloudbuild.ReceiveTriggerWebhookResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ReceiveTriggerWebhook(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retry_build(
        self,
    ) -> Callable[[cloudbuild.RetryBuildRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetryBuild(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_build_trigger(
        self,
    ) -> Callable[[cloudbuild.RunBuildTriggerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunBuildTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_build_trigger(
        self,
    ) -> Callable[[cloudbuild.UpdateBuildTriggerRequest], cloudbuild.BuildTrigger]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBuildTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_worker_pool(
        self,
    ) -> Callable[[cloudbuild.UpdateWorkerPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkerPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudBuildRestTransport",)
