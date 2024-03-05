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

from google.cloud.storage_transfer_v1.types import transfer, transfer_types

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import StorageTransferServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class StorageTransferServiceRestInterceptor:
    """Interceptor for StorageTransferService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the StorageTransferServiceRestTransport.

    .. code-block:: python
        class MyCustomStorageTransferServiceInterceptor(StorageTransferServiceRestInterceptor):
            def pre_create_agent_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_agent_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_transfer_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_transfer_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_agent_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_transfer_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_agent_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_agent_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_google_service_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_google_service_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_transfer_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_transfer_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_agent_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_agent_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transfer_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transfer_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_pause_transfer_operation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_resume_transfer_operation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_run_transfer_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_transfer_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_agent_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_agent_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_transfer_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_transfer_job(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = StorageTransferServiceRestTransport(interceptor=MyCustomStorageTransferServiceInterceptor())
        client = StorageTransferServiceClient(transport=transport)


    """

    def pre_create_agent_pool(
        self,
        request: transfer.CreateAgentPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.CreateAgentPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_agent_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_create_agent_pool(
        self, response: transfer_types.AgentPool
    ) -> transfer_types.AgentPool:
        """Post-rpc interceptor for create_agent_pool

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_create_transfer_job(
        self,
        request: transfer.CreateTransferJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.CreateTransferJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_transfer_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_create_transfer_job(
        self, response: transfer_types.TransferJob
    ) -> transfer_types.TransferJob:
        """Post-rpc interceptor for create_transfer_job

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_agent_pool(
        self,
        request: transfer.DeleteAgentPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.DeleteAgentPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_agent_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def pre_delete_transfer_job(
        self,
        request: transfer.DeleteTransferJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.DeleteTransferJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_transfer_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def pre_get_agent_pool(
        self, request: transfer.GetAgentPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[transfer.GetAgentPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_agent_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_get_agent_pool(
        self, response: transfer_types.AgentPool
    ) -> transfer_types.AgentPool:
        """Post-rpc interceptor for get_agent_pool

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_get_google_service_account(
        self,
        request: transfer.GetGoogleServiceAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.GetGoogleServiceAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_google_service_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_get_google_service_account(
        self, response: transfer_types.GoogleServiceAccount
    ) -> transfer_types.GoogleServiceAccount:
        """Post-rpc interceptor for get_google_service_account

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_get_transfer_job(
        self,
        request: transfer.GetTransferJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.GetTransferJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_transfer_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_get_transfer_job(
        self, response: transfer_types.TransferJob
    ) -> transfer_types.TransferJob:
        """Post-rpc interceptor for get_transfer_job

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_agent_pools(
        self,
        request: transfer.ListAgentPoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.ListAgentPoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_agent_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_list_agent_pools(
        self, response: transfer.ListAgentPoolsResponse
    ) -> transfer.ListAgentPoolsResponse:
        """Post-rpc interceptor for list_agent_pools

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transfer_jobs(
        self,
        request: transfer.ListTransferJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.ListTransferJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transfer_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_list_transfer_jobs(
        self, response: transfer.ListTransferJobsResponse
    ) -> transfer.ListTransferJobsResponse:
        """Post-rpc interceptor for list_transfer_jobs

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_pause_transfer_operation(
        self,
        request: transfer.PauseTransferOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.PauseTransferOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for pause_transfer_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def pre_resume_transfer_operation(
        self,
        request: transfer.ResumeTransferOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.ResumeTransferOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resume_transfer_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def pre_run_transfer_job(
        self,
        request: transfer.RunTransferJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.RunTransferJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_transfer_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_run_transfer_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for run_transfer_job

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_update_agent_pool(
        self,
        request: transfer.UpdateAgentPoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.UpdateAgentPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_agent_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_update_agent_pool(
        self, response: transfer_types.AgentPool
    ) -> transfer_types.AgentPool:
        """Post-rpc interceptor for update_agent_pool

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response

    def pre_update_transfer_job(
        self,
        request: transfer.UpdateTransferJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[transfer.UpdateTransferJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_transfer_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_update_transfer_job(
        self, response: transfer_types.TransferJob
    ) -> transfer_types.TransferJob:
        """Post-rpc interceptor for update_transfer_job

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
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
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
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
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
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
        before they are sent to the StorageTransferService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the StorageTransferService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class StorageTransferServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: StorageTransferServiceRestInterceptor


class StorageTransferServiceRestTransport(StorageTransferServiceTransport):
    """REST backend transport for StorageTransferService.

    Storage Transfer Service and its protos.
    Transfers data between between Google Cloud Storage buckets or
    from a data source external to Google to a Cloud Storage bucket.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "storagetransfer.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[StorageTransferServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'storagetransfer.googleapis.com').
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
        self._interceptor = interceptor or StorageTransferServiceRestInterceptor()
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
                        "uri": "/v1/{name=transferOperations/**}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=transferOperations/**}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=transferOperations}",
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

    class _CreateAgentPool(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("CreateAgentPool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "agentPoolId": "",
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
            request: transfer.CreateAgentPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.AgentPool:
            r"""Call the create agent pool method over HTTP.

            Args:
                request (~.transfer.CreateAgentPoolRequest):
                    The request object. Specifies the request passed to
                CreateAgentPool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.AgentPool:
                    Represents an On-Premises Agent pool.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/projects/{project_id=*}/agentPools",
                    "body": "agent_pool",
                },
            ]
            request, metadata = self._interceptor.pre_create_agent_pool(
                request, metadata
            )
            pb_request = transfer.CreateAgentPoolRequest.pb(request)
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
            resp = transfer_types.AgentPool()
            pb_resp = transfer_types.AgentPool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_agent_pool(resp)
            return resp

    class _CreateTransferJob(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("CreateTransferJob")

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
            request: transfer.CreateTransferJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.TransferJob:
            r"""Call the create transfer job method over HTTP.

            Args:
                request (~.transfer.CreateTransferJobRequest):
                    The request object. Request passed to CreateTransferJob.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.TransferJob:
                    This resource represents the
                configuration of a transfer job that
                runs periodically.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/transferJobs",
                    "body": "transfer_job",
                },
            ]
            request, metadata = self._interceptor.pre_create_transfer_job(
                request, metadata
            )
            pb_request = transfer.CreateTransferJobRequest.pb(request)
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
            resp = transfer_types.TransferJob()
            pb_resp = transfer_types.TransferJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_transfer_job(resp)
            return resp

    class _DeleteAgentPool(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("DeleteAgentPool")

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
            request: transfer.DeleteAgentPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete agent pool method over HTTP.

            Args:
                request (~.transfer.DeleteAgentPoolRequest):
                    The request object. Specifies the request passed to
                DeleteAgentPool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/agentPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_agent_pool(
                request, metadata
            )
            pb_request = transfer.DeleteAgentPoolRequest.pb(request)
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

    class _DeleteTransferJob(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("DeleteTransferJob")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "projectId": "",
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
            request: transfer.DeleteTransferJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete transfer job method over HTTP.

            Args:
                request (~.transfer.DeleteTransferJobRequest):
                    The request object. Request passed to DeleteTransferJob.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{job_name=transferJobs/**}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_transfer_job(
                request, metadata
            )
            pb_request = transfer.DeleteTransferJobRequest.pb(request)
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

    class _GetAgentPool(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("GetAgentPool")

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
            request: transfer.GetAgentPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.AgentPool:
            r"""Call the get agent pool method over HTTP.

            Args:
                request (~.transfer.GetAgentPoolRequest):
                    The request object. Specifies the request passed to
                GetAgentPool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.AgentPool:
                    Represents an On-Premises Agent pool.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/agentPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_agent_pool(request, metadata)
            pb_request = transfer.GetAgentPoolRequest.pb(request)
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
            resp = transfer_types.AgentPool()
            pb_resp = transfer_types.AgentPool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_agent_pool(resp)
            return resp

    class _GetGoogleServiceAccount(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("GetGoogleServiceAccount")

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
            request: transfer.GetGoogleServiceAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.GoogleServiceAccount:
            r"""Call the get google service
            account method over HTTP.

                Args:
                    request (~.transfer.GetGoogleServiceAccountRequest):
                        The request object. Request passed to
                    GetGoogleServiceAccount.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.transfer_types.GoogleServiceAccount:
                        Google service account
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/googleServiceAccounts/{project_id}",
                },
            ]
            request, metadata = self._interceptor.pre_get_google_service_account(
                request, metadata
            )
            pb_request = transfer.GetGoogleServiceAccountRequest.pb(request)
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
            resp = transfer_types.GoogleServiceAccount()
            pb_resp = transfer_types.GoogleServiceAccount.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_google_service_account(resp)
            return resp

    class _GetTransferJob(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("GetTransferJob")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "projectId": "",
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
            request: transfer.GetTransferJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.TransferJob:
            r"""Call the get transfer job method over HTTP.

            Args:
                request (~.transfer.GetTransferJobRequest):
                    The request object. Request passed to GetTransferJob.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.TransferJob:
                    This resource represents the
                configuration of a transfer job that
                runs periodically.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{job_name=transferJobs/**}",
                },
            ]
            request, metadata = self._interceptor.pre_get_transfer_job(
                request, metadata
            )
            pb_request = transfer.GetTransferJobRequest.pb(request)
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
            resp = transfer_types.TransferJob()
            pb_resp = transfer_types.TransferJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_transfer_job(resp)
            return resp

    class _ListAgentPools(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("ListAgentPools")

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
            request: transfer.ListAgentPoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.ListAgentPoolsResponse:
            r"""Call the list agent pools method over HTTP.

            Args:
                request (~.transfer.ListAgentPoolsRequest):
                    The request object. The request passed to ListAgentPools.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.ListAgentPoolsResponse:
                    Response from ListAgentPools.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/projects/{project_id=*}/agentPools",
                },
            ]
            request, metadata = self._interceptor.pre_list_agent_pools(
                request, metadata
            )
            pb_request = transfer.ListAgentPoolsRequest.pb(request)
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
            resp = transfer.ListAgentPoolsResponse()
            pb_resp = transfer.ListAgentPoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_agent_pools(resp)
            return resp

    class _ListTransferJobs(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("ListTransferJobs")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "filter": "",
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
            request: transfer.ListTransferJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer.ListTransferJobsResponse:
            r"""Call the list transfer jobs method over HTTP.

            Args:
                request (~.transfer.ListTransferJobsRequest):
                    The request object. ``projectId``, ``jobNames``, and ``jobStatuses`` are
                query parameters that can be specified when listing
                transfer jobs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer.ListTransferJobsResponse:
                    Response from ListTransferJobs.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/transferJobs",
                },
            ]
            request, metadata = self._interceptor.pre_list_transfer_jobs(
                request, metadata
            )
            pb_request = transfer.ListTransferJobsRequest.pb(request)
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
            resp = transfer.ListTransferJobsResponse()
            pb_resp = transfer.ListTransferJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transfer_jobs(resp)
            return resp

    class _PauseTransferOperation(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("PauseTransferOperation")

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
            request: transfer.PauseTransferOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the pause transfer operation method over HTTP.

            Args:
                request (~.transfer.PauseTransferOperationRequest):
                    The request object. Request passed to
                PauseTransferOperation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=transferOperations/**}:pause",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_pause_transfer_operation(
                request, metadata
            )
            pb_request = transfer.PauseTransferOperationRequest.pb(request)
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

    class _ResumeTransferOperation(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("ResumeTransferOperation")

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
            request: transfer.ResumeTransferOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the resume transfer operation method over HTTP.

            Args:
                request (~.transfer.ResumeTransferOperationRequest):
                    The request object. Request passed to
                ResumeTransferOperation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=transferOperations/**}:resume",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_resume_transfer_operation(
                request, metadata
            )
            pb_request = transfer.ResumeTransferOperationRequest.pb(request)
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

    class _RunTransferJob(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("RunTransferJob")

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
            request: transfer.RunTransferJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the run transfer job method over HTTP.

            Args:
                request (~.transfer.RunTransferJobRequest):
                    The request object. Request passed to RunTransferJob.
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
                    "uri": "/v1/{job_name=transferJobs/**}:run",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_transfer_job(
                request, metadata
            )
            pb_request = transfer.RunTransferJobRequest.pb(request)
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
            resp = self._interceptor.post_run_transfer_job(resp)
            return resp

    class _UpdateAgentPool(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("UpdateAgentPool")

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
            request: transfer.UpdateAgentPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.AgentPool:
            r"""Call the update agent pool method over HTTP.

            Args:
                request (~.transfer.UpdateAgentPoolRequest):
                    The request object. Specifies the request passed to
                UpdateAgentPool.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.AgentPool:
                    Represents an On-Premises Agent pool.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{agent_pool.name=projects/*/agentPools/*}",
                    "body": "agent_pool",
                },
            ]
            request, metadata = self._interceptor.pre_update_agent_pool(
                request, metadata
            )
            pb_request = transfer.UpdateAgentPoolRequest.pb(request)
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
            resp = transfer_types.AgentPool()
            pb_resp = transfer_types.AgentPool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_agent_pool(resp)
            return resp

    class _UpdateTransferJob(StorageTransferServiceRestStub):
        def __hash__(self):
            return hash("UpdateTransferJob")

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
            request: transfer.UpdateTransferJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> transfer_types.TransferJob:
            r"""Call the update transfer job method over HTTP.

            Args:
                request (~.transfer.UpdateTransferJobRequest):
                    The request object. Request passed to UpdateTransferJob.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.transfer_types.TransferJob:
                    This resource represents the
                configuration of a transfer job that
                runs periodically.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{job_name=transferJobs/**}",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_transfer_job(
                request, metadata
            )
            pb_request = transfer.UpdateTransferJobRequest.pb(request)
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
            resp = transfer_types.TransferJob()
            pb_resp = transfer_types.TransferJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_transfer_job(resp)
            return resp

    @property
    def create_agent_pool(
        self,
    ) -> Callable[[transfer.CreateAgentPoolRequest], transfer_types.AgentPool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAgentPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_transfer_job(
        self,
    ) -> Callable[[transfer.CreateTransferJobRequest], transfer_types.TransferJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTransferJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_agent_pool(
        self,
    ) -> Callable[[transfer.DeleteAgentPoolRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAgentPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_transfer_job(
        self,
    ) -> Callable[[transfer.DeleteTransferJobRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTransferJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_agent_pool(
        self,
    ) -> Callable[[transfer.GetAgentPoolRequest], transfer_types.AgentPool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAgentPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_google_service_account(
        self,
    ) -> Callable[
        [transfer.GetGoogleServiceAccountRequest], transfer_types.GoogleServiceAccount
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGoogleServiceAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_transfer_job(
        self,
    ) -> Callable[[transfer.GetTransferJobRequest], transfer_types.TransferJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTransferJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_agent_pools(
        self,
    ) -> Callable[[transfer.ListAgentPoolsRequest], transfer.ListAgentPoolsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAgentPools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transfer_jobs(
        self,
    ) -> Callable[
        [transfer.ListTransferJobsRequest], transfer.ListTransferJobsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTransferJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pause_transfer_operation(
        self,
    ) -> Callable[[transfer.PauseTransferOperationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PauseTransferOperation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_transfer_operation(
        self,
    ) -> Callable[[transfer.ResumeTransferOperationRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumeTransferOperation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def run_transfer_job(
        self,
    ) -> Callable[[transfer.RunTransferJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunTransferJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_agent_pool(
        self,
    ) -> Callable[[transfer.UpdateAgentPoolRequest], transfer_types.AgentPool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAgentPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_transfer_job(
        self,
    ) -> Callable[[transfer.UpdateTransferJobRequest], transfer_types.TransferJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTransferJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(StorageTransferServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=transferOperations/**}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(StorageTransferServiceRestStub):
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
                    "uri": "/v1/{name=transferOperations/**}",
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

    class _ListOperations(StorageTransferServiceRestStub):
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
                    "uri": "/v1/{name=transferOperations}",
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


__all__ = ("StorageTransferServiceRestTransport",)
